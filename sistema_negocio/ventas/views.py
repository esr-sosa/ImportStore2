from decimal import Decimal
import json
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q, Sum
from django.http import FileResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from caja.models import CajaDiaria, MovimientoCaja
from core.utils import obtener_valor_dolar_blue
from crm.models import Cliente
from inventario.models import Precio, ProductoVariante
from historial.models import RegistroHistorial
from locales.models import Local

from .models import DetalleVenta, Venta
from .pdf import generar_comprobante_pdf


def pos_view(request):
    # Obtener el precio del dólar blue para mostrar en el POS
    dolar_blue = obtener_valor_dolar_blue()
    context = {
        'dolar_blue': dolar_blue,
    }
    return render(request, "ventas/pos.html", context)


def _formatear_variante(variante):
    precios = variante.precios.filter(activo=True)
    mapa = {}
    for precio in precios:
        clave = f"{precio.tipo.lower()}_{precio.moneda.lower()}"
        mapa[clave] = str(precio.precio)
    
    # Determinar estado de stock
    stock_actual = variante.stock_actual or 0
    stock_status = "sin stock" if stock_actual <= 0 else "disponible"
    
    return {
        "id": variante.id,
        "sku": variante.sku,
        "producto": variante.producto.nombre,
        "atributos": variante.atributos_display,
        "stock": stock_actual,
        "stock_status": stock_status,
        "precios": mapa,
        "categoria": variante.producto.categoria.nombre if variante.producto.categoria else "",
    }


def buscar_productos_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})

    variantes = (
        ProductoVariante.objects.select_related("producto")
        .filter(producto__activo=True)
        .prefetch_related("precios")
        .filter(
            Q(producto__nombre__icontains=query)
            | Q(sku__icontains=query)
            | Q(atributo_1__icontains=query)
            | Q(atributo_2__icontains=query)
        )
        .order_by("producto__nombre")[:15]
    )

    return JsonResponse({"results": [_formatear_variante(v) for v in variantes]})


def buscar_clientes_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})
    
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=query) | Q(telefono__icontains=query) | Q(email__icontains=query)
    ).order_by("nombre")[:10]
    
    results = [
        {
            "id": c.id,
            "nombre": c.nombre,
            "telefono": c.telefono,
            "email": c.email or "",
        }
        for c in clientes
    ]
    
    return JsonResponse({"results": results})


def _generar_id_venta(prefix: str = "POS") -> str:
    base = f"{prefix}-{uuid4().hex[:8].upper()}"
    while Venta.objects.filter(pk=base).exists():
        base = f"{prefix}-{uuid4().hex[:8].upper()}"
    return base


def _resolver_precio_ars(variante: ProductoVariante) -> tuple[Decimal, Decimal | None, Decimal | None]:
    """
    Resuelve el precio en ARS de una variante.
    Si es un iPhone (categoría Celulares) y tiene precio en USD, lo convierte a ARS.
    Retorna: (precio_ars, precio_usd_original, tipo_cambio_usado)
    """
    # Verificar si es un iPhone (categoría Celulares)
    es_iphone = (
        variante.producto.categoria 
        and variante.producto.categoria.nombre.lower() == "celulares"
    )
    
    # Primero intentar precio en ARS
    precio_ars = variante.precios.filter(
        activo=True,
        tipo=Precio.Tipo.MINORISTA,
        moneda=Precio.Moneda.ARS,
    ).order_by("-actualizado").first()
    
    if precio_ars:
        return (Decimal(precio_ars.precio), None, None)
    
    # Si no hay precio en ARS, buscar en USD
    precio_usd = variante.precios.filter(
        activo=True,
        tipo=Precio.Tipo.MINORISTA,
        moneda=Precio.Moneda.USD,
    ).order_by("-actualizado").first()
    
    if precio_usd:
        precio_usd_valor = Decimal(precio_usd.precio)
        
        # Si es iPhone, convertir USD a ARS usando dólar blue
        if es_iphone:
            dolar_blue = obtener_valor_dolar_blue()
            if dolar_blue:
                precio_ars_convertido = precio_usd_valor * Decimal(str(dolar_blue))
                return (precio_ars_convertido, precio_usd_valor, Decimal(str(dolar_blue)))
        
        # Si no es iPhone o no hay dólar blue, devolver el precio USD como está (será 0)
        return (precio_usd_valor, precio_usd_valor, None)
    
    return (Decimal("0"), None, None)


@csrf_exempt
@transaction.atomic
def crear_venta_api(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)

    items = data.get("items") or []
    if not items:
        return JsonResponse({"error": "La venta no contiene productos"}, status=400)

    metodo_pago = data.get("metodo_pago", Venta.MetodoPago.EFECTIVO_ARS)
    if metodo_pago not in dict(Venta.MetodoPago.choices):
        return JsonResponse({"error": "Método de pago inválido"}, status=400)

    nota = data.get("nota", "")
    aplicar_iva = data.get("aplicar_iva", False)
    iva_porcentaje = Decimal(str(data.get("iva_porcentaje", 21)))
    descuento_general = data.get("descuento_general", {"tipo": "monto", "valor": 0})

    cliente_obj = None
    cliente_id = data.get("cliente_id")
    cliente_nombre = data.get("cliente_nombre", "").strip()
    cliente_documento = data.get("cliente_documento", "").strip()
    cliente_telefono = data.get("cliente_telefono", "").strip()
    
    # Si hay cliente_id, buscar el cliente existente
    if cliente_id:
        cliente_obj = Cliente.objects.filter(pk=cliente_id).first()
        if cliente_obj:
            cliente_nombre = cliente_obj.nombre
            cliente_documento = cliente_obj.telefono  # Usar teléfono como documento si no hay otro
    
    # Si no hay cliente_id pero hay nombre y teléfono, crear o buscar cliente
    elif cliente_nombre and cliente_telefono:
        cliente_obj, created = Cliente.objects.get_or_create(
            telefono=cliente_telefono,
            defaults={
                "nombre": cliente_nombre,
                "email": data.get("cliente_email", "").strip() or None,
                "tipo_cliente": "Minorista",
            }
        )
        if not created:
            # Si ya existe, actualizar nombre si es diferente
            if cliente_obj.nombre != cliente_nombre:
                cliente_obj.nombre = cliente_nombre
                cliente_obj.save(update_fields=["nombre", "ultima_actualizacion"])
    
    # Si solo hay nombre sin teléfono, usar nombre como consumidor final
    elif cliente_nombre and not cliente_telefono:
        cliente_nombre = cliente_nombre
        cliente_obj = None
    
    # Si no hay nada, consumidor final
    else:
        cliente_nombre = ""
        cliente_obj = None

    subtotal = Decimal("0")
    descuento_items_total = Decimal("0")
    detalles = []

    for item in items:
        variante_id = item.get("variante_id")
        es_custom = item.get("es_custom", False)
        
        cantidad = int(item.get("cantidad", 1))
        cantidad = max(1, cantidad)
        
        # Productos varios (sin variante_id)
        if es_custom or not variante_id:
            precio_ars = Decimal(str(item.get("precio_unitario_ars", 0)))
            if precio_ars <= 0:
                return JsonResponse({"error": "Precio inválido para producto varios"}, status=400)
            
            # Para productos varios, priorizar el nombre que viene en "nombre" o "descripcion"
            nombre = item.get("nombre") or item.get("descripcion") or "Producto varios"
            sku = item.get("sku", f"VAR-{timezone.now().timestamp()}")
            # Usar el nombre como descripción para productos varios
            descripcion = nombre
            
            bruto = precio_ars * cantidad
            
            descuento_linea_valor = Decimal("0")
            descuento_linea = item.get("descuento", {})
            if descuento_linea:
                tipo = descuento_linea.get("tipo")
                valor = Decimal(str(descuento_linea.get("valor", 0)))
                if tipo == "porcentaje":
                    descuento_linea_valor = (bruto * valor) / Decimal("100")
                elif tipo == "monto":
                    descuento_linea_valor = min(bruto, valor)
            
            subtotal += bruto
            descuento_items_total += descuento_linea_valor
            total_linea = bruto - descuento_linea_valor
            
            detalles.append(
                {
                    "variante": None,  # Sin variante para productos varios
                    "sku": sku,
                    "descripcion": descripcion,
                    "cantidad": cantidad,
                    "precio": precio_ars,
                    "subtotal": total_linea,
                    "precio_usd_original": None,
                    "tipo_cambio_usado": None,
                    "es_custom": True,
                }
            )
            continue
        
        # Productos del catálogo (con variante_id)
        variante = ProductoVariante.objects.select_related("producto").get(pk=variante_id)

        if variante.stock_actual is not None and variante.stock_actual < cantidad:
            return JsonResponse(
                {
                    "error": f"Stock insuficiente para {variante.producto.nombre} ({variante.sku}). Disponible: {variante.stock_actual}",
                },
                status=400,
            )

        precio_ars = item.get("precio_unitario_ars")
        precio_usd_original = None
        tipo_cambio_usado = None
        
        # Verificar si es iPhone (categoría Celulares)
        es_iphone = (
            variante.producto.categoria 
            and variante.producto.categoria.nombre.lower() == "celulares"
        )
        
        if precio_ars is None:
            # Si no viene precio del frontend, resolverlo
            precio_ars, precio_usd_original, tipo_cambio_usado = _resolver_precio_ars(variante)
        else:
            precio_ars = Decimal(str(precio_ars))
            # Si el precio viene del frontend, verificar si es iPhone y tiene precio USD
            if es_iphone:
                precio_usd = variante.precios.filter(
                    activo=True,
                    tipo=Precio.Tipo.MINORISTA,
                    moneda=Precio.Moneda.USD,
                ).order_by("-actualizado").first()
                precio_ars_db = variante.precios.filter(
                    activo=True,
                    tipo=Precio.Tipo.MINORISTA,
                    moneda=Precio.Moneda.ARS,
                ).order_by("-actualizado").first()
                
                # Si tiene precio USD pero no ARS, convertir
                if precio_usd and not precio_ars_db:
                    precio_usd_original = Decimal(precio_usd.precio)
                    dolar_blue = obtener_valor_dolar_blue()
                    if dolar_blue:
                        tipo_cambio_usado = Decimal(str(dolar_blue))
                        # Convertir el precio USD a ARS usando el tipo de cambio
                        precio_ars = precio_usd_original * tipo_cambio_usado
                elif precio_usd and precio_ars_db:
                    # Tiene ambos precios, usar el USD como referencia si el precio del frontend parece ser USD
                    # Comparar si el precio del frontend es similar al USD (con margen de error)
                    precio_usd_val = Decimal(precio_usd.precio)
                    # Si el precio del frontend es similar al USD (dentro de un 10%), asumir que es USD
                    if abs(precio_ars - precio_usd_val) < (precio_usd_val * Decimal("0.1")):
                        precio_usd_original = precio_usd_val
                        dolar_blue = obtener_valor_dolar_blue()
                        if dolar_blue:
                            tipo_cambio_usado = Decimal(str(dolar_blue))
                            precio_ars = precio_usd_original * tipo_cambio_usado

        bruto = precio_ars * cantidad

        descuento_linea_valor = Decimal("0")
        descuento_linea = item.get("descuento", {})
        if descuento_linea:
            tipo = descuento_linea.get("tipo")
            valor = Decimal(str(descuento_linea.get("valor", 0)))
            if tipo == "porcentaje":
                descuento_linea_valor = (bruto * valor) / Decimal("100")
            elif tipo == "monto":
                descuento_linea_valor = min(bruto, valor)

        subtotal += bruto
        descuento_items_total += descuento_linea_valor
        total_linea = bruto - descuento_linea_valor

        detalles.append(
            {
                "variante": variante,
                "sku": variante.sku,
                "descripcion": f"{variante.producto.nombre} {variante.atributos_display}",
                "cantidad": cantidad,
                "precio": precio_ars,
                "subtotal": total_linea,
                "precio_usd_original": precio_usd_original,
                "tipo_cambio_usado": tipo_cambio_usado,
                "es_custom": False,
            }
        )

    descuento_general_valor = Decimal("0")
    if descuento_general:
        tipo_general = descuento_general.get("tipo")
        valor_general = Decimal(str(descuento_general.get("valor", 0)))
        base = subtotal - descuento_items_total
        if tipo_general == "porcentaje":
            descuento_general_valor = (base * valor_general) / Decimal("100")
        elif tipo_general == "monto":
            descuento_general_valor = min(base, valor_general)

    neto = subtotal - descuento_items_total - descuento_general_valor
    impuestos = Decimal("0")
    if aplicar_iva:
        impuestos = (neto * iva_porcentaje) / Decimal("100")

    total = neto + impuestos

    venta_id = data.get("orden_id") or _generar_id_venta()
    status = data.get("status")
    if status not in dict(Venta.Status.choices):
        status = Venta.Status.COMPLETADO

    venta = Venta.objects.create(
        id=venta_id,
        fecha=timezone.now(),
        cliente=cliente_obj,
        cliente_nombre=cliente_nombre,
        cliente_documento=cliente_documento,
        subtotal_ars=subtotal,
        descuento_total_ars=descuento_items_total + descuento_general_valor,
        impuestos_ars=impuestos,
        total_ars=total,
        metodo_pago=metodo_pago,
        status=status,
        nota=nota,
        vendedor=request.user if request.user.is_authenticated else None,
    )

    for detalle in detalles:
        DetalleVenta.objects.create(
            venta=venta,
            variante=detalle["variante"],  # Puede ser None para productos varios
            sku=detalle["sku"],
            descripcion=detalle["descripcion"],
            cantidad=detalle["cantidad"],
            precio_unitario_ars_congelado=detalle["precio"],
            subtotal_ars=detalle["subtotal"],
            precio_unitario_usd_original=detalle.get("precio_usd_original"),
            tipo_cambio_usado=detalle.get("tipo_cambio_usado"),
        )
        # Solo descontar stock si es un producto del catálogo (tiene variante)
        if detalle["variante"]:
            ProductoVariante.objects.filter(pk=detalle["variante"].pk).update(
                stock_actual=F("stock_actual") - detalle["cantidad"]
            )

    RegistroHistorial.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        tipo_accion=RegistroHistorial.TipoAccion.VENTA,
        descripcion=f"Venta {venta.id} por ${venta.total_ars:.2f} ({venta.metodo_pago}).",
    )

    pdf_file = generar_comprobante_pdf(venta)
    venta.comprobante_pdf.save(pdf_file.name, pdf_file, save=True)

    # ========== INTEGRACIÓN CON CAJA ==========
    # Buscar caja abierta para el local (por defecto el primero, o el que se pase en el request)
    local_id = data.get("local_id")
    if local_id:
        try:
            local = Local.objects.get(pk=local_id)
        except Local.DoesNotExist:
            local = None
    else:
        local = Local.objects.first()  # Local por defecto

    if local:
        caja_abierta = CajaDiaria.objects.filter(local=local, estado=CajaDiaria.Estado.ABIERTA).first()
        if caja_abierta:
            # Crear movimiento de caja
            MovimientoCaja.objects.create(
                caja_diaria=caja_abierta,
                tipo=MovimientoCaja.Tipo.VENTA,
                metodo_pago=venta.metodo_pago,
                monto_ars=venta.total_ars,
                descripcion=f"Venta {venta.id}",
                venta_asociada=venta,
                usuario=request.user if request.user.is_authenticated else None,
            )

    return JsonResponse(
        {
            "status": "ok",
            "venta": {
                "id": venta.id,
                "status": venta.status,
                "status_label": venta.get_status_display(),
                "subtotal_ars": str(subtotal),
                "descuento_total_ars": str(descuento_items_total + descuento_general_valor),
                "impuestos_ars": str(impuestos),
                "total_ars": str(total),
                "pdf": venta.comprobante_pdf.url if venta.comprobante_pdf else None,
            },
        }
    )


@csrf_exempt
def ultima_venta_api(request):
    """API para obtener la última venta registrada."""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    ultima_venta = Venta.objects.order_by("-fecha").first()
    
    if not ultima_venta:
        return JsonResponse({"error": "No se encontró ninguna venta"}, status=404)
    
    return JsonResponse(
        {
            "status": "ok",
            "venta": {
                "id": ultima_venta.id,
                "fecha": ultima_venta.fecha.isoformat(),
                "total_ars": str(ultima_venta.total_ars),
                "pdf": ultima_venta.comprobante_pdf.url if ultima_venta.comprobante_pdf else None,
            },
        }
    )


@login_required
def generar_voucher_pdf(request, venta_id: str):
    venta = get_object_or_404(Venta.objects.prefetch_related("detalles"), pk=venta_id)
    if not venta.comprobante_pdf:
        pdf = generar_comprobante_pdf(venta)
        venta.comprobante_pdf.save(pdf.name, pdf, save=True)
    if not venta.comprobante_pdf:
        return HttpResponseNotFound("No se pudo generar el comprobante")
    venta.comprobante_pdf.open("rb")
    filename = venta.comprobante_pdf.name.split("/")[-1]
    return FileResponse(venta.comprobante_pdf, as_attachment=True, filename=filename)


@login_required
def listado_ventas(request):
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    status = request.GET.get("estado", "")
    metodo_pago = request.GET.get("metodo_pago", "")
    q = request.GET.get("q", "").strip()

    ventas_qs = Venta.objects.select_related("vendedor", "cliente").prefetch_related("detalles")

    if fecha_desde:
        try:
            desde = timezone.datetime.strptime(fecha_desde, "%Y-%m-%d").date()
            ventas_qs = ventas_qs.filter(fecha__gte=desde)
        except ValueError:
            pass

    if fecha_hasta:
        try:
            hasta = timezone.datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
            ventas_qs = ventas_qs.filter(fecha__lte=hasta)
        except ValueError:
            pass

    if status:
        ventas_qs = ventas_qs.filter(status=status)

    if metodo_pago:
        ventas_qs = ventas_qs.filter(metodo_pago=metodo_pago)

    if q:
        ventas_qs = ventas_qs.filter(
            Q(id__icontains=q)
            | Q(cliente_nombre__icontains=q)
            | Q(cliente_documento__icontains=q)
        )

    ventas_qs = ventas_qs.order_by("-fecha", "-id")

    total_ventas = ventas_qs.count()
    total_facturado = ventas_qs.aggregate(total=Sum("total_ars"))["total"] or Decimal("0")
    promedio_ticket = total_facturado / total_ventas if total_ventas > 0 else Decimal("0")

    paginator = Paginator(ventas_qs, 20)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    context = {
        "ventas": page_obj.object_list,
        "page_obj": page_obj,
        "total_ventas": total_ventas,
        "total_facturado": total_facturado,
        "promedio_ticket": promedio_ticket,
        "filtros": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "estado": status,
            "metodo_pago": metodo_pago,
            "q": q,
        },
        "estados": Venta.Status.choices,
        "metodos_pago": Venta.MetodoPago.choices,
    }

    return render(request, "ventas/listado.html", context)
