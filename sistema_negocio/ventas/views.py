from decimal import Decimal
import json
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q, Sum
from django.http import FileResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from caja.models import CajaDiaria, MovimientoCaja
from core.utils import obtener_valor_dolar_blue
from crm.models import Cliente
from inventario.models import Precio, ProductoVariante
from historial.models import RegistroHistorial
from locales.models import Local

from .models import CarritoRemoto, DetalleVenta, Venta
from .pdf import generar_comprobante_pdf


def pos_view(request):
    # Obtener el precio del dólar blue para mostrar en el POS
    dolar_blue = obtener_valor_dolar_blue()
    context = {
        'dolar_blue': dolar_blue,
    }
    return render(request, "ventas/pos.html", context)

@login_required
def pos_remoto_view(request):
    """Vista móvil para POS remoto con escáner de códigos."""
    return render(request, "ventas/pos_remoto.html")


@login_required
def pos_remoto_ping(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    carrito, _ = CarritoRemoto.objects.get_or_create(usuario=request.user, defaults={"items": []})
    CarritoRemoto.objects.filter(pk=carrito.pk).update(actualizado=timezone.now())
    return JsonResponse({"status": "ok"})


@login_required
def escaner_productos_view(request):
    """Vista de escáner de productos con información completa y edición rápida."""
    dolar_blue = obtener_valor_dolar_blue()
    context = {
        'dolar_blue': dolar_blue,
    }
    return render(request, "ventas/escaner_productos.html", context)


def _formatear_variante(variante, modo_precio=None):
    precios = variante.precios.filter(activo=True)
    mapa = {}
    for precio in precios:
        clave = f"{precio.tipo.lower()}_{precio.moneda.lower()}"
        mapa[clave] = str(precio.precio)
    
    # Determinar estado de stock
    stock_actual = variante.stock_actual or 0
    stock_status = "sin stock" if stock_actual <= 0 else "disponible"
    
    # Obtener categoría
    categoria = variante.producto.categoria.nombre if variante.producto.categoria else ""
    
    # Obtener precio según modo_precio (priorizar el tipo seleccionado)
    tipo_precio = modo_precio if modo_precio in [Precio.Tipo.MINORISTA, Precio.Tipo.MAYORISTA] else Precio.Tipo.MINORISTA
    precio_principal_ars = precios.filter(tipo=tipo_precio, moneda=Precio.Moneda.ARS, activo=True).first()
    precio_principal_usd = precios.filter(tipo=tipo_precio, moneda=Precio.Moneda.USD, activo=True).first()
    
    # Agregar campos de precio principal para fácil acceso
    precio_principal = None
    if precio_principal_ars:
        precio_principal = str(precio_principal_ars.precio)
    elif precio_principal_usd:
        precio_principal = str(precio_principal_usd.precio)
    
    return {
        "id": variante.id,
        "sku": variante.sku or "",
        "nombre": variante.producto.nombre,
        "descripcion": f"{variante.producto.nombre} {variante.atributos_display}".strip(),
        "stock_actual": stock_actual,
        "stock_status": stock_status,
        "precios": mapa,
        "precio_principal": precio_principal,  # Precio según modo_precio
        "tipo_precio": tipo_precio.lower(),  # "minorista" o "mayorista"
        "categoria": categoria,
    }

def _formatear_variante_completa(variante, dolar_blue=None, modo_precio=None):
    """Formatea una variante con toda la información detallada para el escáner."""
    precios = variante.precios.filter(activo=True)
    precios_map = {}
    for precio in precios:
        clave = f"{precio.tipo.lower()}_{precio.moneda.lower()}"
        precios_map[clave] = {
            "valor": str(precio.precio),
            "id": precio.id
        }
    
    # Determinar tipo de precio a usar
    tipo_precio = modo_precio if modo_precio in [Precio.Tipo.MINORISTA, Precio.Tipo.MAYORISTA] else Precio.Tipo.MINORISTA
    
    # Obtener precios específicos
    precio_minorista_ars = precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.ARS, activo=True).first()
    precio_mayorista_ars = precios.filter(tipo=Precio.Tipo.MAYORISTA, moneda=Precio.Moneda.ARS, activo=True).first()
    precio_minorista_usd = precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.USD, activo=True).first()
    precio_mayorista_usd = precios.filter(tipo=Precio.Tipo.MAYORISTA, moneda=Precio.Moneda.USD, activo=True).first()
    
    # Obtener precio principal según modo_precio
    precio_principal_ars = precios.filter(tipo=tipo_precio, moneda=Precio.Moneda.ARS, activo=True).first()
    precio_principal_usd = precios.filter(tipo=tipo_precio, moneda=Precio.Moneda.USD, activo=True).first()
    
    # Convertir USD a ARS si es necesario
    precio_minorista_ars_convertido = None
    precio_mayorista_ars_convertido = None
    precio_principal_ars_convertido = None
    if precio_minorista_usd and dolar_blue:
        precio_minorista_ars_convertido = float(precio_minorista_usd.precio) * float(dolar_blue)
    if precio_mayorista_usd and dolar_blue:
        precio_mayorista_ars_convertido = float(precio_mayorista_usd.precio) * float(dolar_blue)
    if precio_principal_usd and dolar_blue:
        precio_principal_ars_convertido = float(precio_principal_usd.precio) * float(dolar_blue)
    
    stock_actual = variante.stock_actual or 0
    stock_status = "sin stock" if stock_actual <= 0 else "disponible"
    
    # Determinar precio principal a mostrar
    precio_principal_valor = None
    if precio_principal_ars:
        precio_principal_valor = str(precio_principal_ars.precio)
    elif precio_principal_ars_convertido:
        precio_principal_valor = str(precio_principal_ars_convertido)
    elif precio_principal_usd:
        precio_principal_valor = str(precio_principal_usd.precio)
    
    return {
        "id": variante.id,
        "sku": variante.sku or "",
        "codigo_barras": variante.codigo_barras or "",
        "qr_code": variante.qr_code or "",
        "nombre": variante.producto.nombre,
        "descripcion": f"{variante.producto.nombre} {variante.atributos_display}".strip(),
        "precio_principal": precio_principal_valor,  # Precio según modo_precio
        "tipo_precio": tipo_precio.lower(),  # "minorista" o "mayorista"
        "atributos": variante.atributos_display,
        "stock_actual": stock_actual,
        "stock_status": stock_status,
        "categoria": variante.producto.categoria.nombre if variante.producto.categoria else "",
        "proveedor": variante.producto.proveedor.nombre if variante.producto.proveedor else "",
        "precio_minorista_ars": str(precio_minorista_ars.precio) if precio_minorista_ars else None,
        "precio_mayorista_ars": str(precio_mayorista_ars.precio) if precio_mayorista_ars else None,
        "precio_minorista_usd": str(precio_minorista_usd.precio) if precio_minorista_usd else None,
        "precio_mayorista_usd": str(precio_mayorista_usd.precio) if precio_mayorista_usd else None,
        "precio_minorista_ars_convertido": precio_minorista_ars_convertido,
        "precio_mayorista_ars_convertido": precio_mayorista_ars_convertido,
        "precios_ids": {
            "minorista_ars": precio_minorista_ars.id if precio_minorista_ars else None,
            "mayorista_ars": precio_mayorista_ars.id if precio_mayorista_ars else None,
            "minorista_usd": precio_minorista_usd.id if precio_minorista_usd else None,
            "mayorista_usd": precio_mayorista_usd.id if precio_mayorista_usd else None,
        },
        "es_iphone": variante.producto.categoria and variante.producto.categoria.nombre.lower() == "celulares",
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

    # Obtener modo_precio de la sesión
    modo_precio = request.session.get("modo_precio", Precio.Tipo.MINORISTA)
    
    return JsonResponse({"results": [_formatear_variante(v, modo_precio) for v in variantes]})

@csrf_exempt
@login_required
def buscar_producto_por_codigo_api(request):
    """Busca un producto por SKU, código de barras o QR code exacto (para escáner)."""
    codigo = request.GET.get("codigo", "").strip()
    if not codigo:
        return JsonResponse({"error": "Código requerido"}, status=400)
    
    # Limpiar el código (por si viene con URL completa del QR)
    codigo_original = codigo
    codigo_limpio = codigo.strip()
    
    # Si es una URL, intentar extraer el código del final
    if '/' in codigo_limpio:
        partes = codigo_limpio.split('/')
        codigo_limpio = partes[-1]
    
    # Si tiene parámetros de URL, extraer solo el código
    if '?' in codigo_limpio:
        codigo_limpio = codigo_limpio.split('?')[0]
    
    # Si tiene hash, extraer solo el código
    if '#' in codigo_limpio:
        codigo_limpio = codigo_limpio.split('#')[0]
    
    # Buscar por SKU exacto, código de barras exacto o QR code
    # Intentar primero con el código limpio, luego con el original
    variante = None
    
    # Primera búsqueda: código limpio
    if codigo_limpio:
        variante = (
            ProductoVariante.objects.select_related("producto", "producto__proveedor")
            .filter(producto__activo=True)
            .prefetch_related("precios")
            .filter(
                Q(sku=codigo_limpio) | 
                Q(codigo_barras=codigo_limpio) |
                Q(qr_code=codigo_limpio) |
                Q(qr_code__icontains=codigo_limpio)  # Por si el QR tiene URL completa
            )
            .first()
        )
    
    # Segunda búsqueda: código original (si no se encontró con el limpio)
    if not variante and codigo_original != codigo_limpio:
        variante = (
            ProductoVariante.objects.select_related("producto", "producto__proveedor")
            .filter(producto__activo=True)
            .prefetch_related("precios")
            .filter(
                Q(sku=codigo_original) | 
                Q(codigo_barras=codigo_original) |
                Q(qr_code=codigo_original) |
                Q(qr_code__icontains=codigo_original)  # Por si el QR tiene URL completa
            )
            .first()
        )
    
    # Tercera búsqueda: búsqueda parcial (solo si las anteriores fallaron)
    if not variante:
        # Buscar si el código está contenido en algún campo
        variante = (
            ProductoVariante.objects.select_related("producto", "producto__proveedor")
            .filter(producto__activo=True)
            .prefetch_related("precios")
            .filter(
                Q(sku__icontains=codigo_limpio) | 
                Q(codigo_barras__icontains=codigo_limpio) |
                Q(qr_code__icontains=codigo_limpio)
            )
            .first()
        )
    
    if not variante:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    
    # Obtener modo_precio de la sesión
    modo_precio = request.session.get("modo_precio", Precio.Tipo.MINORISTA)
    
    # Si se solicita información completa (para el escáner de productos)
    completo = request.GET.get("completo", "false").lower() == "true"
    if completo:
        dolar_blue = obtener_valor_dolar_blue()
        return JsonResponse({"result": _formatear_variante_completa(variante, dolar_blue, modo_precio)})
    
    return JsonResponse({"result": _formatear_variante(variante, modo_precio)})

@csrf_exempt
@login_required
def actualizar_producto_rapido_api(request):
    """API para actualización rápida de producto (stock, precios, etc.)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    
    variante_id = data.get("variante_id")
    if not variante_id:
        return JsonResponse({"error": "variante_id requerido"}, status=400)
    
    try:
        variante = ProductoVariante.objects.select_related("producto").prefetch_related("precios").get(pk=variante_id)
    except ProductoVariante.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    
    cambios = []
    
    # Actualizar stock
    if "stock_actual" in data:
        nuevo_stock = int(data["stock_actual"])
        variante.stock_actual = nuevo_stock
        variante.save(update_fields=["stock_actual"])
        cambios.append(f"Stock actualizado a {nuevo_stock}")
    
    # Actualizar precios
    precios_actualizados = []
    if "precio_minorista_ars" in data and data["precio_minorista_ars"]:
        precio_id = data.get("precio_minorista_ars_id")
        nuevo_precio = Decimal(str(data["precio_minorista_ars"]))
        if precio_id:
            try:
                precio = Precio.objects.get(pk=precio_id)
                precio.precio = nuevo_precio
                precio.save(update_fields=["precio"])
                precios_actualizados.append("Precio minorista ARS")
            except Precio.DoesNotExist:
                pass
        else:
            # Crear nuevo precio
            Precio.objects.create(
                variante=variante,
                tipo=Precio.Tipo.MINORISTA,
                moneda=Precio.Moneda.ARS,
                precio=nuevo_precio,
                activo=True
            )
            precios_actualizados.append("Precio minorista ARS (creado)")
    
    if "precio_mayorista_ars" in data and data["precio_mayorista_ars"]:
        precio_id = data.get("precio_mayorista_ars_id")
        nuevo_precio = Decimal(str(data["precio_mayorista_ars"]))
        if precio_id:
            try:
                precio = Precio.objects.get(pk=precio_id)
                precio.precio = nuevo_precio
                precio.save(update_fields=["precio"])
                precios_actualizados.append("Precio mayorista ARS")
            except Precio.DoesNotExist:
                pass
        else:
            Precio.objects.create(
                variante=variante,
                tipo=Precio.Tipo.MAYORISTA,
                moneda=Precio.Moneda.ARS,
                precio=nuevo_precio,
                activo=True
            )
            precios_actualizados.append("Precio mayorista ARS (creado)")
    
    if "precio_minorista_usd" in data and data["precio_minorista_usd"]:
        precio_id = data.get("precio_minorista_usd_id")
        nuevo_precio = Decimal(str(data["precio_minorista_usd"]))
        if precio_id:
            try:
                precio = Precio.objects.get(pk=precio_id)
                precio.precio = nuevo_precio
                precio.save(update_fields=["precio"])
                precios_actualizados.append("Precio minorista USD")
            except Precio.DoesNotExist:
                pass
        else:
            Precio.objects.create(
                variante=variante,
                tipo=Precio.Tipo.MINORISTA,
                moneda=Precio.Moneda.USD,
                precio=nuevo_precio,
                activo=True
            )
            precios_actualizados.append("Precio minorista USD (creado)")
    
    if "precio_mayorista_usd" in data and data["precio_mayorista_usd"]:
        precio_id = data.get("precio_mayorista_usd_id")
        nuevo_precio = Decimal(str(data["precio_mayorista_usd"]))
        if precio_id:
            try:
                precio = Precio.objects.get(pk=precio_id)
                precio.precio = nuevo_precio
                precio.save(update_fields=["precio"])
                precios_actualizados.append("Precio mayorista USD")
            except Precio.DoesNotExist:
                pass
        else:
            Precio.objects.create(
                variante=variante,
                tipo=Precio.Tipo.MAYORISTA,
                moneda=Precio.Moneda.USD,
                precio=nuevo_precio,
                activo=True
            )
            precios_actualizados.append("Precio mayorista USD (creado)")
    
    if precios_actualizados:
        cambios.extend(precios_actualizados)
    
    # Recargar variante para obtener datos actualizados
    variante.refresh_from_db()
    dolar_blue = obtener_valor_dolar_blue()
    
    # Obtener modo_precio de la sesión
    modo_precio = request.session.get("modo_precio", Precio.Tipo.MINORISTA)
    
    return JsonResponse({
        "status": "ok",
        "mensaje": "Producto actualizado correctamente",
        "cambios": cambios,
        "producto": _formatear_variante_completa(variante, dolar_blue, modo_precio)
    })

@csrf_exempt
@login_required
def agregar_producto_carrito_remoto_api(request):
    """Agrega un producto al carrito remoto compartido por usuario (compartido entre dispositivos)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    
    variante_id = data.get("variante_id")
    if not variante_id:
        return JsonResponse({"error": "variante_id requerido"}, status=400)
    
    try:
        variante = ProductoVariante.objects.select_related("producto").prefetch_related("precios").get(pk=variante_id)
    except ProductoVariante.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    
    # Obtener o crear carrito remoto del usuario (compartido entre dispositivos)
    carrito_remoto_obj, _ = CarritoRemoto.objects.get_or_create(
        usuario=request.user,
        defaults={"items": []}
    )
    
    carrito_remoto = carrito_remoto_obj.items if isinstance(carrito_remoto_obj.items, list) else []
    
    # Buscar si ya existe en el carrito
    item_existente = None
    for item in carrito_remoto:
        if isinstance(item, dict) and item.get("variante_id") == variante_id:
            item_existente = item
            break
    
    # Obtener modo_precio de la sesión
    modo_precio = request.session.get("modo_precio", Precio.Tipo.MINORISTA)
    
    # Verificar stock antes de agregar
    cantidad_a_agregar = 1
    if item_existente:
        cantidad_a_agregar = item_existente.get("cantidad", 1) + 1
    
    # Verificar stock disponible - Solo retornar mensaje simple para POS remoto
    stock_actual = variante.stock_actual or 0
    if stock_actual < cantidad_a_agregar:
        return JsonResponse({
            "error": f"Stock insuficiente para {variante.producto.nombre} ({variante.sku}). Disponible: {stock_actual}"
        }, status=400)
    
    if item_existente:
        # Incrementar cantidad
        item_existente["cantidad"] = item_existente.get("cantidad", 1) + 1
    else:
        # Agregar nuevo item
        variante_formateada = _formatear_variante(variante, modo_precio)
        
        # Obtener precio ARS según modo_precio
        precio_ars = variante.precios.filter(
            tipo=modo_precio,
            moneda=Precio.Moneda.ARS,
            activo=True
        ).order_by("-actualizado").first()
        
        precio_usd = variante.precios.filter(
            tipo=Precio.Tipo.MINORISTA,
            moneda=Precio.Moneda.USD,
            activo=True
        ).order_by("-actualizado").first()
        
        # Resolver precio ARS (convertir USD si es necesario)
        precio_ars_valor = None
        precio_usd_original = None
        if precio_ars:
            precio_ars_valor = float(precio_ars.precio)
        elif precio_usd:
            precio_usd_original = float(precio_usd.precio)
            dolar_blue = obtener_valor_dolar_blue()
            if dolar_blue:
                precio_ars_valor = precio_usd_original * float(dolar_blue)
        
        if precio_ars_valor is None:
            return JsonResponse({"error": "Producto sin precio"}, status=400)
        
        # Verificar si es iPhone
        es_iphone = (
            variante.producto.categoria 
            and variante.producto.categoria.nombre.lower() == "celulares"
        )
        
        nuevo_item = {
            "variante_id": variante_id,
            "sku": variante.sku,
            "nombre": variante.producto.nombre,
            "descripcion": f"{variante.producto.nombre} {variante.atributos_display}".strip(),
            "cantidad": 1,
            "precio_unitario_ars": precio_ars_valor,
            "precio_usd_original": precio_usd_original,
            "es_iphone": es_iphone,
            "es_custom": False,
            "stock_actual": variante.stock_actual or 0,  # Incluir stock actual
            "precios": variante_formateada.get("precios", {}),
        }
        carrito_remoto.append(nuevo_item)
    
    # Guardar carrito en base de datos (compartido entre dispositivos)
    carrito_remoto_obj.items = carrito_remoto
    carrito_remoto_obj.save(update_fields=["items", "actualizado"])
    
    # Calcular total de items correctamente
    total_items = sum(int(item.get("cantidad", 1)) for item in carrito_remoto if isinstance(item, dict))
    
    return JsonResponse({
        "status": "ok",
        "carrito": carrito_remoto,
        "total_items": total_items
    })


@csrf_exempt
@login_required
@transaction.atomic
def actualizar_stock_variante_api(request):
    """API para actualizar el stock de una variante rápidamente desde el POS."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    
    variante_id = data.get("variante_id")
    nuevo_stock = data.get("stock")
    
    if not variante_id:
        return JsonResponse({"error": "variante_id requerido"}, status=400)
    
    if nuevo_stock is None:
        return JsonResponse({"error": "stock requerido"}, status=400)
    
    try:
        nuevo_stock = int(nuevo_stock)
        if nuevo_stock < 0:
            return JsonResponse({"error": "El stock no puede ser negativo"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Stock debe ser un número entero"}, status=400)
    
    try:
        variante = ProductoVariante.objects.select_related("producto").get(pk=variante_id)
    except ProductoVariante.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    
    # Actualizar stock
    variante.stock_actual = nuevo_stock
    variante.save(update_fields=["stock_actual", "actualizado"])
    
    return JsonResponse({
        "status": "ok",
        "variante_id": variante_id,
        "stock_actual": nuevo_stock,
        "mensaje": f"Stock actualizado a {nuevo_stock}"
    })

@login_required
def obtener_carrito_remoto_api(request):
    """Obtiene el carrito remoto compartido por usuario (compartido entre dispositivos)."""
    # Obtener carrito remoto del usuario desde la base de datos
    carrito_remoto_obj = None
    try:
        carrito_remoto_obj = CarritoRemoto.objects.get(usuario=request.user)
        carrito_remoto = carrito_remoto_obj.items if isinstance(carrito_remoto_obj.items, list) else []
    except CarritoRemoto.DoesNotExist:
        carrito_remoto = []
    
    # Calcular total de items correctamente
    total_items = sum(int(item.get("cantidad", 1)) for item in carrito_remoto if isinstance(item, dict))
    
    return JsonResponse({
        "carrito": carrito_remoto,
        "total_items": total_items,
        "actualizado": carrito_remoto_obj.actualizado.isoformat() if carrito_remoto_obj else None
    })

@csrf_exempt
@login_required
def limpiar_carrito_remoto_api(request):
    """Limpia el carrito remoto compartido por usuario."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    # Limpiar carrito remoto del usuario en la base de datos
    CarritoRemoto.objects.update_or_create(
        usuario=request.user,
        defaults={"items": []}
    )
    
    return JsonResponse({"status": "ok"})


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


def _resolver_precio_ars(variante: ProductoVariante, modo_precio: str = None) -> tuple[Decimal, Decimal | None, Decimal | None]:
    """
    Resuelve el precio en ARS de una variante.
    Si es un iPhone (categoría Celulares) y tiene precio en USD, lo convierte a ARS.
    Retorna: (precio_ars, precio_usd_original, tipo_cambio_usado)
    
    Args:
        variante: La variante del producto
        modo_precio: "MINORISTA" o "MAYORISTA" (por defecto "MINORISTA")
    """
    # Usar modo_precio o default a MINORISTA
    tipo_precio = modo_precio if modo_precio in [Precio.Tipo.MINORISTA, Precio.Tipo.MAYORISTA] else Precio.Tipo.MINORISTA
    
    # Verificar si es un iPhone (categoría Celulares)
    es_iphone = (
        variante.producto.categoria 
        and variante.producto.categoria.nombre.lower() == "celulares"
    )
    
    # Primero intentar precio en ARS
    precio_ars = variante.precios.filter(
        activo=True,
        tipo=tipo_precio,
        moneda=Precio.Moneda.ARS,
    ).order_by("-actualizado").first()
    
    if precio_ars:
        return (Decimal(precio_ars.precio), None, None)
    
    # Si no hay precio en ARS, buscar en USD
    precio_usd = variante.precios.filter(
        activo=True,
        tipo=tipo_precio,
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
            # Asegurarse de obtener el nombre correctamente
            nombre_raw = item.get("nombre") or item.get("descripcion") or ""
            nombre = nombre_raw.strip() if nombre_raw else "Producto varios"
            if not nombre or nombre == "":
                nombre = "Producto varios"
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
            # Obtener modo_precio de la sesión
            modo_precio = request.session.get("modo_precio", Precio.Tipo.MINORISTA)
            precio_ars, precio_usd_original, tipo_cambio_usado = _resolver_precio_ars(variante, modo_precio)
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

    # Calcular descuento por método de pago
    # NOTA: El descuento por método de pago se aplica sobre la base antes de impuestos
    # En pago mixto, se calcula proporcionalmente según los montos de cada método
    descuento_metodo_pago_valor = Decimal("0")
    es_pago_mixto = data.get("es_pago_mixto", False)
    base_antes_descuento_metodo = subtotal - descuento_items_total - descuento_general_valor
    
    if es_pago_mixto:
        # Pago mixto: calcular descuento proporcional para cada método
        descuento_metodo_pago_1 = data.get("descuento_metodo_pago_1")
        descuento_metodo_pago_2 = data.get("descuento_metodo_pago_2")
        monto_pago_1 = data.get("monto_pago_1")
        monto_pago_2 = data.get("monto_pago_2")
        
        # Calcular el total antes de aplicar descuentos por método de pago (para proporción)
        # En pago mixto, los montos de pago deben sumar el total antes de aplicar descuentos por método
        total_antes_descuento_metodo = base_antes_descuento_metodo
        
        if descuento_metodo_pago_1 and monto_pago_1 and total_antes_descuento_metodo > 0:
            monto1 = Decimal(str(monto_pago_1))
            porcentaje1 = Decimal(str(descuento_metodo_pago_1))
            # Calcular proporción del monto1 sobre el total antes de descuentos
            proporcion1 = monto1 / total_antes_descuento_metodo if total_antes_descuento_metodo > 0 else Decimal("0")
            # Aplicar descuento proporcionalmente
            descuento_metodo_pago_valor += base_antes_descuento_metodo * proporcion1 * (porcentaje1 / Decimal("100"))
        
        if descuento_metodo_pago_2 and monto_pago_2 and total_antes_descuento_metodo > 0:
            monto2 = Decimal(str(monto_pago_2))
            porcentaje2 = Decimal(str(descuento_metodo_pago_2))
            # Calcular proporción del monto2 sobre el total antes de descuentos
            proporcion2 = monto2 / total_antes_descuento_metodo if total_antes_descuento_metodo > 0 else Decimal("0")
            # Aplicar descuento proporcionalmente
            descuento_metodo_pago_valor += base_antes_descuento_metodo * proporcion2 * (porcentaje2 / Decimal("100"))
    else:
        # Pago simple: calcular descuento para el método seleccionado
        descuento_metodo_pago = data.get("descuento_metodo_pago")
        if descuento_metodo_pago:
            porcentaje = Decimal(str(descuento_metodo_pago))
            descuento_metodo_pago_valor = base_antes_descuento_metodo * (porcentaje / Decimal("100"))

    neto = base_antes_descuento_metodo - descuento_metodo_pago_valor
    impuestos = Decimal("0")
    if aplicar_iva:
        impuestos = (neto * iva_porcentaje) / Decimal("100")

    total = neto + impuestos

    venta_id = data.get("orden_id") or _generar_id_venta()
    status = data.get("status")
    if status not in dict(Venta.Status.choices):
        status = Venta.Status.COMPLETADO
    
    # Manejar pago mixto (se usa más abajo, pero se necesita aquí para el cálculo del descuento)
    es_pago_mixto = data.get("es_pago_mixto", False)
    metodo_pago_2 = data.get("metodo_pago_2")
    monto_pago_1 = data.get("monto_pago_1")
    monto_pago_2 = data.get("monto_pago_2")
    
    if es_pago_mixto and metodo_pago_2:
        # Validar que los montos sumen la base ANTES de aplicar descuentos por método de pago
        # Los montos de pago deben sumar base_antes_descuento_metodo (no el total final)
        # Convertir a string y reemplazar comas por puntos para Decimal
        monto1_str = str(monto_pago_1 or 0).replace(',', '.')
        monto2_str = str(monto_pago_2 or 0).replace(',', '.')
        monto1 = Decimal(monto1_str)
        monto2 = Decimal(monto2_str)
        suma = monto1 + monto2
        diferencia = abs(suma - base_antes_descuento_metodo)
        if diferencia > Decimal("0.01"):  # Tolerancia de 1 centavo
            return JsonResponse({
                "error": f"Los montos de pago mixto no suman la base correcta. Base: ${base_antes_descuento_metodo:,.2f}, Suma: ${suma:,.2f}, Diferencia: ${diferencia:,.2f}. Los montos deben sumar la base antes de aplicar descuentos por método de pago."
            }, status=400)

    venta = Venta.objects.create(
        id=venta_id,
        fecha=timezone.now(),
        cliente=cliente_obj,
        cliente_nombre=cliente_nombre,
        cliente_documento=cliente_documento,
        subtotal_ars=subtotal,
        descuento_total_ars=descuento_items_total + descuento_general_valor + descuento_metodo_pago_valor,
        descuento_metodo_pago_ars=descuento_metodo_pago_valor,
        impuestos_ars=impuestos,
        total_ars=total,
        metodo_pago=metodo_pago,
        status=status,
        nota=nota,
        vendedor=request.user if request.user.is_authenticated else None,
        es_pago_mixto=es_pago_mixto,
        metodo_pago_2=metodo_pago_2 if es_pago_mixto else None,
        monto_pago_1=Decimal(str(monto_pago_1)) if es_pago_mixto and monto_pago_1 else None,
        monto_pago_2=Decimal(str(monto_pago_2)) if es_pago_mixto and monto_pago_2 else None,
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
                "descuento_total_ars": str(descuento_items_total + descuento_general_valor + descuento_metodo_pago_valor),
                "descuento_metodo_pago_ars": str(descuento_metodo_pago_valor),
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
def imprimir_voucher(request, venta_id: str):
    """Vista para imprimir el voucher desde el celular - abre el PDF en una nueva ventana con diálogo de impresión."""
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from django.urls import reverse
    
    venta = get_object_or_404(Venta.objects.prefetch_related("detalles"), pk=venta_id)
    pdf_url = request.build_absolute_uri(reverse('ventas:voucher', args=[venta_id]))
    
    # Renderizar template HTML que muestra el PDF y abre el diálogo de impresión
    html = render_to_string('ventas/imprimir_voucher.html', {
        'venta': venta,
        'pdf_url': pdf_url,
    })
    return HttpResponse(html)


@csrf_exempt
@login_required
def solicitar_impresion_remota_api(request):
    """API para solicitar impresión remota desde el celular (agrega a la cola)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    
    venta_id = data.get("venta_id")
    if not venta_id:
        return JsonResponse({"error": "venta_id requerido"}, status=400)
    
    try:
        venta = Venta.objects.get(pk=venta_id)
    except Venta.DoesNotExist:
        return JsonResponse({"error": "Venta no encontrada"}, status=404)
    
    # Crear solicitud de impresión
    from ventas.models import SolicitudImpresion
    solicitud = SolicitudImpresion.objects.create(
        venta=venta,
        usuario=request.user,
        estado=SolicitudImpresion.Estado.PENDIENTE
    )
    
    return JsonResponse({
        "status": "ok",
        "solicitud_id": solicitud.id,
        "mensaje": "Solicitud de impresión agregada a la cola"
    })


@login_required
def obtener_solicitudes_impresion_api(request):
    """API para obtener solicitudes de impresión pendientes (para la PC)."""
    from ventas.models import SolicitudImpresion
    from django.utils import timezone
    
    # Obtener solicitudes pendientes del usuario
    solicitudes = SolicitudImpresion.objects.filter(
        usuario=request.user,
        estado=SolicitudImpresion.Estado.PENDIENTE
    ).select_related("venta").order_by("creado")[:10]  # Máximo 10 a la vez
    
    return JsonResponse({
        "solicitudes": [
            {
                "id": s.id,
                "venta_id": s.venta.id,
                "creado": s.creado.isoformat(),
            }
            for s in solicitudes
        ]
    })


@csrf_exempt
@login_required
def marcar_impresion_completada_api(request):
    """API para marcar una solicitud de impresión como completada o con error."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    
    solicitud_id = data.get("solicitud_id")
    estado = data.get("estado")  # "COMPLETADA" o "ERROR"
    error = data.get("error", "")
    
    if not solicitud_id:
        return JsonResponse({"error": "solicitud_id requerido"}, status=400)
    
    from ventas.models import SolicitudImpresion
    from django.utils import timezone
    
    try:
        solicitud = SolicitudImpresion.objects.get(pk=solicitud_id, usuario=request.user)
    except SolicitudImpresion.DoesNotExist:
        return JsonResponse({"error": "Solicitud no encontrada"}, status=404)
    
    solicitud.estado = estado
    if error:
        solicitud.error = error
    if estado == SolicitudImpresion.Estado.COMPLETADA:
        solicitud.procesado = timezone.now()
    solicitud.save()
    
    return JsonResponse({"status": "ok"})


@login_required
def listado_ventas(request):
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    status = request.GET.get("estado", "")
    metodo_pago = request.GET.get("metodo_pago", "")
    q = request.GET.get("q", "").strip()

    # Filtrar solo ventas POS (no web)
    ventas_qs = Venta.objects.filter(origen=Venta.Origen.POS).select_related("vendedor", "cliente").prefetch_related("detalles")

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


@login_required
def detalle_venta(request, venta_id: str):
    try:
        venta = Venta.objects.select_related("cliente", "vendedor").prefetch_related("detalles__variante__producto").get(id=venta_id)
    except Venta.DoesNotExist:
        messages.error(request, "La venta no existe.")
        return redirect("ventas:listado")
    
    context = {
        "venta": venta,
        "estados": Venta.Status.choices,
    }
    return render(request, "ventas/detalle.html", context)


@login_required
@transaction.atomic
def anular_venta(request, venta_id: str):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        venta = Venta.objects.select_related().prefetch_related("detalles__variante").get(id=venta_id)
    except Venta.DoesNotExist:
        return JsonResponse({"error": "La venta no existe"}, status=404)
    
    if venta.status == Venta.Status.CANCELADO:
        return JsonResponse({"error": "La venta ya está cancelada"}, status=400)
    
    devolver_stock = request.POST.get("devolver_stock", "false").lower() == "true"
    motivo = request.POST.get("motivo", "").strip()
    
    # Devolver stock si se solicita
    if devolver_stock:
        for detalle in venta.detalles.all():
            if detalle.variante:
                variante = detalle.variante
                if variante.stock_actual is not None:
                    variante.stock_actual += detalle.cantidad
                    variante.save(update_fields=["stock_actual"])
    
    # Cambiar estado a cancelado
    venta.status = Venta.Status.CANCELADO
    if motivo:
        venta.nota = f"{venta.nota}\n\n[ANULADA] {motivo}".strip()
    venta.save(update_fields=["status", "nota"])
    
    # Registrar en historial
    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.ELIMINACION,
        descripcion=f"Venta {venta.id} anulada. {'Stock devuelto.' if devolver_stock else 'Stock no devuelto.'} {f'Motivo: {motivo}' if motivo else ''}",
    )
    
    messages.success(request, f"Venta {venta.id} anulada exitosamente.")
    return redirect("ventas:detalle", venta_id=venta_id)


@login_required
@transaction.atomic
def actualizar_estado_venta(request, venta_id: str):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        venta = Venta.objects.get(id=venta_id)
    except Venta.DoesNotExist:
        return JsonResponse({"error": "La venta no existe"}, status=404)
    
    nuevo_estado = request.POST.get("estado", "").strip()
    if nuevo_estado not in dict(Venta.Status.choices):
        return JsonResponse({"error": "Estado inválido"}, status=400)
    
    estado_anterior = venta.status
    nota = request.POST.get("nota", "").strip()
    motivo = request.POST.get("motivo", "").strip()
    
    venta.status = nuevo_estado
    
    # Si se cancela o devuelve, guardar motivo
    if nuevo_estado in [Venta.Status.CANCELADO, Venta.Status.DEVUELTO]:
        venta.motivo_cancelacion = motivo or nota
    
    venta.save(update_fields=["status", "motivo_cancelacion"])
    
    # Registrar en historial de estados
    from ventas.models import HistorialEstadoVenta
    HistorialEstadoVenta.objects.create(
        venta=venta,
        estado_anterior=estado_anterior,
        estado_nuevo=nuevo_estado,
        usuario=request.user,
        nota=nota
    )
    
    # También registrar en historial general
    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.CAMBIO_ESTADO,
        descripcion=f"Estado de venta {venta.id} cambiado de {Venta.Status(estado_anterior).label} a {venta.get_status_display()}",
    )
    
    messages.success(request, f"Estado de la venta {venta.id} actualizado a {venta.get_status_display()}.")
    return redirect("ventas:detalle", venta_id=venta_id)
