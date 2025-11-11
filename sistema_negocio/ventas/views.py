from decimal import Decimal
import json
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q, Sum, Count
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta

from inventario.models import Precio, ProductoVariante
from historial.models import RegistroHistorial

from .models import LineaVenta, Venta
from .pdf import generar_comprobante_pdf


def pos_view(request):
    return render(request, "ventas/pos.html")


def _formatear_variante(variante):
    precios = variante.precios.filter(activo=True)
    mapa = {}
    for precio in precios:
        clave = f"{precio.tipo.lower()}_{precio.moneda.lower()}"
        mapa[clave] = str(precio.precio)
    return {
        "id": variante.id,
        "sku": variante.sku,
        "producto": variante.producto.nombre,
        "atributos": variante.atributos_display,
        "stock": variante.stock_actual,
        "precios": mapa,
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


@csrf_exempt
@transaction.atomic
def crear_venta_api(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    try:
        data = json.loads(request.body or "{}")
        items = data.get("items") or []
        metodo_pago = data.get("metodo_pago", Venta.MetodoPago.EFECTIVO)
        nota = data.get("nota", "")
        descuento_general = data.get("descuento_general", {"tipo": "monto", "valor": 0})
        aplicar_iva = data.get("aplicar_iva", False)
        iva_porcentaje = Decimal(str(data.get("iva_porcentaje", 21)))
        estado = data.get("estado", Venta.Estado.COBRADA)
        cliente_info = data.get("cliente") or {}
        cliente_nombre = cliente_info.get("nombre") or data.get("cliente_nombre", "")
        cliente_documento = cliente_info.get("documento") or data.get("cliente_documento", "")

        if not items:
            return JsonResponse({"error": "La venta no contiene productos"}, status=400)

        subtotal = Decimal("0")
        descuento_items_total = Decimal("0")
        lineas = []

        for item in items:
            variante_id = item.get("variante_id")
            cantidad = int(item.get("cantidad", 1))
            descuento_linea = item.get("descuento", {})

            variante = ProductoVariante.objects.select_related("producto").get(pk=variante_id)

            precio = item.get("precio_unitario")
            if precio is None:
                precio_obj = variante.precios.filter(activo=True, tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.USD).first()
                if not precio_obj:
                    precio_obj = variante.precios.filter(activo=True).order_by("-actualizado").first()
                precio = precio_obj.precio if precio_obj else Decimal("0")

            precio = Decimal(str(precio))
            cantidad = max(1, cantidad)
            bruto = precio * cantidad

            descuento_linea_valor = Decimal("0")
            if descuento_linea:
                tipo = descuento_linea.get("tipo")
                valor = Decimal(str(descuento_linea.get("valor", 0)))
                if tipo == "porcentaje":
                    descuento_linea_valor = (bruto * valor) / Decimal("100")
                elif tipo == "monto":
                    descuento_linea_valor = min(bruto, valor)

            total_linea = bruto - descuento_linea_valor
            subtotal += bruto
            descuento_items_total += descuento_linea_valor

            lineas.append({
                "variante": variante,
                "descripcion": f"{variante.producto.nombre} {variante.atributos_display}",
                "cantidad": cantidad,
                "precio": precio,
                "descuento": descuento_linea_valor,
                "total": total_linea,
            })

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

        venta = Venta.objects.create(
            numero=f"POS-{uuid4().hex[:8].upper()}",
            subtotal=subtotal,
            descuento_items=descuento_items_total,
            descuento_general=descuento_general_valor,
            impuestos=impuestos,
            total=total,
            metodo_pago=metodo_pago,
            nota=nota,
            estado=estado,
            vendedor=request.user if request.user.is_authenticated else None,
            cliente_nombre=cliente_nombre,
            cliente_documento=cliente_documento,
        )

        for linea in lineas:
            LineaVenta.objects.create(
                venta=venta,
                variante=linea["variante"],
                descripcion=linea["descripcion"],
                cantidad=linea["cantidad"],
                precio_unitario=linea["precio"],
                descuento=linea["descuento"],
                total_linea=linea["total"],
            )
            ProductoVariante.objects.filter(pk=linea["variante"].pk).update(
                stock_actual=F("stock_actual") - linea["cantidad"]
            )

        venta.refresh_from_db()

        RegistroHistorial.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            tipo_accion=RegistroHistorial.TipoAccion.VENTA,
            descripcion=f"Venta {venta.numero} por {venta.total} ({venta.metodo_pago}).",
        )

        pdf_file = generar_comprobante_pdf(venta)
        venta.comprobante_pdf.save(pdf_file.name, pdf_file, save=True)

        return JsonResponse(
            {
                "status": "ok",
                "venta": {
                    "numero": venta.numero,
                    "estado": venta.estado,
                    "subtotal": str(subtotal),
                    "descuento_items": str(descuento_items_total),
                    "descuento_general": str(descuento_general_valor),
                    "impuestos": str(impuestos),
                    "total": str(total),
                    "pdf": venta.comprobante_pdf.url if venta.comprobante_pdf else None,
                },
            }
        )

    except ProductoVariante.DoesNotExist:
        return JsonResponse({"error": "Algún producto seleccionado ya no existe"}, status=404)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)


@login_required
def listado_ventas(request):
    """Vista de listado de ventas con filtros y paginación."""
    # Filtros
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    estado = request.GET.get("estado", "")
    metodo_pago = request.GET.get("metodo_pago", "")
    q = request.GET.get("q", "").strip()
    
    ventas_qs = Venta.objects.select_related("vendedor").prefetch_related("lineas").all()
    
    if fecha_desde:
        try:
            desde = timezone.datetime.strptime(fecha_desde, "%Y-%m-%d").date()
            ventas_qs = ventas_qs.filter(fecha__gte=desde)
        except:
            pass
    
    if fecha_hasta:
        try:
            hasta = timezone.datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
            ventas_qs = ventas_qs.filter(fecha__lte=hasta)
        except:
            pass
    
    if estado:
        ventas_qs = ventas_qs.filter(estado=estado)
    
    if metodo_pago:
        ventas_qs = ventas_qs.filter(metodo_pago=metodo_pago)
    
    if q:
        ventas_qs = ventas_qs.filter(
            Q(numero__icontains=q) |
            Q(cliente_nombre__icontains=q) |
            Q(cliente_documento__icontains=q)
        )
    
    ventas_qs = ventas_qs.order_by("-fecha", "-id")
    
    # Estadísticas
    total_ventas = ventas_qs.count()
    total_facturado = ventas_qs.aggregate(total=Sum("total"))["total"] or 0
    promedio_ticket = total_facturado / total_ventas if total_ventas > 0 else 0
    
    # Paginación
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
            "estado": estado,
            "metodo_pago": metodo_pago,
            "q": q,
        },
        "estados": Venta.Estado.choices,
        "metodos_pago": Venta.MetodoPago.choices,
    }
    
    template = "ventas/listado.html" if request.headers.get("HX-Request") else "ventas/listado.html"
    return render(request, template, context)
