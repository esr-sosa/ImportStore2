from decimal import Decimal
from io import BytesIO
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from django.contrib import messages
from core.db_inspector import column_exists
from core.utils import obtener_valor_dolar_blue
from historial.models import RegistroHistorial
from inventario.models import (
    Categoria,
    DetalleIphone,
    PlanCanjeConfig,
    PlanCanjeTransaccion,
    Precio,
    Producto,
    ProductoVariante,
)
from inventario.utils import is_detalleiphone_variante_ready
from inventario.etiquetas import generar_etiqueta

from .forms import AgregarIphoneForm


def _categoria_celulares():
    categoria, _ = Categoria.objects.get_or_create(
        nombre="Celulares", defaults={"descripcion": "Smartphones Apple"}
    )
    return categoria


def _ultimo_precio(variante, tipo, moneda):
    return (
        variante.precios.filter(tipo=tipo, moneda=moneda, activo=True)
        .order_by("-actualizado")
        .first()
    )


def _sincronizar_precios(variante, data):
    """Sincroniza precios usando la función consolidada de inventario."""
    from inventario.views import _sincronizar_precios as _sincronizar_precios_inventario
    
    # Mapear datos de iPhone a formato de inventario
    data_inventario = {
        "precio_venta_ars": data.get("precio_venta_ars"),
        "precio_minorista_ars": data.get("precio_venta_ars"),
        "precio_mayorista_ars": data.get("precio_mayorista_ars"),
        "precio_minimo_ars": None,
    }
    
    _sincronizar_precios_inventario(variante, data_inventario)


@login_required
def iphone_dashboard(request):
    required_columns = [
        ("inventario_productovariante", "sku"),
        ("inventario_productovariante", "stock_actual"),
        ("inventario_precio", "precio"),
    ]
    missing_columns = [
        f"{table}.{column}"
        for table, column in required_columns
        if not column_exists(table, column)
    ]

    valor_dolar = obtener_valor_dolar_blue()
    detalleiphone_ready = False

    if missing_columns:
        messages.warning(
            request,
            "El módulo de inventario todavía no está completamente migrado. Ejecutá `python manage.py migrate` para crear las "
            "columnas faltantes: " + ", ".join(missing_columns),
        )
        context = {
            "variantes": [],
            "valor_dolar": valor_dolar,
            "search_query": request.GET.get("q", "").strip(),
            "stats": {"variantes": 0, "stock": 0, "valor_usd": Decimal("0"), "valor_ars": None},
            "detalleiphone_ready": False,
            "schema_missing_columns": missing_columns,
        }
        return render(request, "iphones/dashboard.html", context)

    detalleiphone_ready = is_detalleiphone_variante_ready()

    variantes_qs = (
        ProductoVariante.objects.select_related("producto")
        .prefetch_related("precios")
        .filter(producto__categoria__nombre__iexact="Celulares")
        .order_by("producto__nombre", "sku")
    )

    if detalleiphone_ready:
        variantes_qs = variantes_qs.select_related("detalle_iphone")

    search_query = request.GET.get("q", "").strip()
    if search_query:
        filtros = Q(producto__nombre__icontains=search_query) | Q(
            atributo_1__icontains=search_query
        ) | Q(atributo_2__icontains=search_query) | Q(
            sku__icontains=search_query
        )
        if detalleiphone_ready:
            filtros |= Q(detalle_iphone__imei__icontains=search_query)
        variantes_qs = variantes_qs.filter(filtros)

    variantes = list(variantes_qs)
    dolar_decimal = Decimal(str(valor_dolar)) if valor_dolar else None

    total_stock = sum(v.stock_actual for v in variantes)
    total_usd = Decimal("0")
    total_ars = Decimal("0") if dolar_decimal else None

    for variante in variantes:
        precio_minorista_usd = _ultimo_precio(
            variante, Precio.Tipo.MINORISTA, Precio.Moneda.USD
        )
        precio_mayorista_usd = _ultimo_precio(
            variante, Precio.Tipo.MAYORISTA, Precio.Moneda.USD
        )
        precio_minorista_ars = _ultimo_precio(
            variante, Precio.Tipo.MINORISTA, Precio.Moneda.ARS
        )
        precio_mayorista_ars = _ultimo_precio(
            variante, Precio.Tipo.MAYORISTA, Precio.Moneda.ARS
        )

        detalle = None
        if detalleiphone_ready:
            detalle = getattr(variante, "detalle_iphone", None)
        if not detalle:
            detalle = DetalleIphone.objects.filter(variante=variante).first()

        variante.precio_minorista_usd = (
            precio_minorista_usd.precio if precio_minorista_usd else None
        )
        variante.precio_mayorista_usd = (
            precio_mayorista_usd.precio if precio_mayorista_usd else None
        )
        variante.precio_minorista_ars = (
            precio_minorista_ars.precio if precio_minorista_ars else None
        )
        variante.precio_mayorista_ars = (
            precio_mayorista_ars.precio if precio_mayorista_ars else None
        )

        if variante.precio_minorista_usd:
            total_usd += Decimal(variante.precio_minorista_usd) * Decimal(
                variante.stock_actual or 0
            )
        if total_ars is not None and variante.precio_minorista_usd:
            total_ars += (
                Decimal(variante.precio_minorista_usd)
                * Decimal(variante.stock_actual or 0)
                * dolar_decimal
            )

        if dolar_decimal and variante.precio_minorista_usd and not variante.precio_minorista_ars:
            variante.precio_minorista_ars = (
                Decimal(variante.precio_minorista_usd) * dolar_decimal
            )
        if dolar_decimal and variante.precio_mayorista_usd and not variante.precio_mayorista_ars:
            variante.precio_mayorista_ars = (
                Decimal(variante.precio_mayorista_usd) * dolar_decimal
            )

        if detalle:
            if detalle.precio_venta_usd and not variante.precio_minorista_usd:
                variante.precio_minorista_usd = detalle.precio_venta_usd
        variante.detalle_cache = detalle

    stats = {
        "variantes": len(variantes),
        "stock": total_stock,
        "valor_usd": total_usd,
        "valor_ars": total_ars,
    }

    context = {
        "variantes": variantes,
        "valor_dolar": valor_dolar,
        "search_query": search_query,
        "stats": stats,
        "detalleiphone_ready": detalleiphone_ready,
        "schema_missing_columns": [],
    }
    return render(request, "iphones/dashboard.html", context)


@login_required
@transaction.atomic
def agregar_iphone(request):
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("inventario:dashboard")

    if request.method == "POST":
        form = AgregarIphoneForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            categoria = _categoria_celulares()

            producto, _ = Producto.objects.get_or_create(
                nombre=data["modelo"],
                defaults={
                    "categoria": categoria,
                    "activo": data["activo"],
                    "estado": "ACTIVO",
                },
            )
            producto.categoria = categoria
            producto.activo = data["activo"]
            producto.save()

            # Generar SKU automático si está habilitado o si está vacío
            sku_valor = data.get("sku", "").strip()
            if data.get("sku_auto", True) or not sku_valor:
                from django.utils.text import slugify
                nombre = data.get("modelo", "")
                capacidad = data.get("capacidad", "")
                color = data.get("color", "")
                
                # Generar SKU base
                sku_base = slugify(f"{nombre}-{capacidad}-{color}".strip("-")).upper()
                if not sku_base:
                    sku_base = slugify(nombre).upper() or "IPH"
                
                # Asegurar unicidad
                sku_final = sku_base
                contador = 1
                while ProductoVariante.objects.filter(sku=sku_final).exists():
                    sku_final = f"{sku_base}-{contador}"
                    contador += 1
            else:
                sku_final = sku_valor.upper()
            
            # Generar código de barras si está habilitado
            codigo_barras = None
            if data.get("generar_codigo_barras"):
                import random
                codigo_barras = f"{random.randint(100000000000, 999999999999)}"
            elif data.get("codigo_barras"):
                codigo_barras = data["codigo_barras"]
            
            # Generar QR code si está habilitado
            qr_code = None
            if data.get("generar_qr"):
                if sku_final:
                    qr_code = f"https://importstore.com/producto/{sku_final}"
            elif data.get("qr_code"):
                qr_code = data["qr_code"]
            
            # Asegurar valores por defecto para stock
            stock_actual_val = data.get("stock_actual", 0) or 0
            stock_minimo_val = data.get("stock_minimo", 0) or 0
            
            # Verificar si existe el campo 'stock' antiguo en la base de datos
            from core.db_inspector import column_exists
            from django.db import connection
            
            nombre_variante_val = f"{data['modelo']} {data['capacidad']} {data['color']}".strip()
            
            if column_exists("inventario_productovariante", "stock"):
                # Usar SQL directo para insertar con el campo stock
                from django.utils import timezone
                ahora = timezone.now()
                
                # Verificar si existe el campo 'peso' también
                tiene_peso = column_exists("inventario_productovariante", "peso")
                
                with connection.cursor() as cursor:
                    if tiene_peso:
                        # Si existe el campo peso, incluirlo en el INSERT
                        cursor.execute("""
                            INSERT INTO inventario_productovariante 
                            (producto_id, sku, nombre_variante, codigo_barras, qr_code, atributo_1, atributo_2, 
                             stock_actual, stock_minimo, stock, peso, activo, creado, actualizado)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, [
                            producto.pk, sku_final, nombre_variante_val, codigo_barras, qr_code,
                            data["capacidad"], data["color"], stock_actual_val, stock_minimo_val,
                            stock_actual_val, 0, 1 if data["activo"] else 0, ahora, ahora
                        ])
                    else:
                        # Si no existe el campo peso, INSERT normal
                        cursor.execute("""
                            INSERT INTO inventario_productovariante 
                            (producto_id, sku, nombre_variante, codigo_barras, qr_code, atributo_1, atributo_2, 
                             stock_actual, stock_minimo, stock, activo, creado, actualizado)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, [
                            producto.pk, sku_final, nombre_variante_val, codigo_barras, qr_code,
                            data["capacidad"], data["color"], stock_actual_val, stock_minimo_val,
                            stock_actual_val, 1 if data["activo"] else 0, ahora, ahora
                        ])
                    variante_id = cursor.lastrowid
                
                # Recargar la variante desde la base de datos
                variante = ProductoVariante.objects.get(pk=variante_id)
            else:
                # Si no existe el campo stock, crear normalmente
                variante = ProductoVariante.objects.create(
                    producto=producto,
                    sku=sku_final,
                    nombre_variante=nombre_variante_val,
                    codigo_barras=codigo_barras,
                    qr_code=qr_code,
                    atributo_1=data["capacidad"],
                    atributo_2=data["color"],
                    stock_actual=stock_actual_val,
                    stock_minimo=stock_minimo_val,
                    activo=data["activo"],
                )

            _sincronizar_precios(variante, data)

            # Si es nuevo, establecer salud_bateria a 100
            salud_bateria = data.get("salud_bateria")
            if data.get("es_nuevo", False):
                salud_bateria = 100
            
            # Manejar IMEI: si está vacío, guardar como None para evitar conflictos con unique
            imei_value = data.get("imei", "").strip()
            imei_final = imei_value if imei_value else None
            
            # Si el IMEI está vacío, verificar si ya existe otro registro con imei=''
            # y en ese caso, asegurarse de usar None (no '')
            if not imei_final:
                from django.db.models import Q
                otros_con_imei_vacio = DetalleIphone.objects.filter(
                    Q(imei='') | Q(imei__isnull=True)
                )
                if otros_con_imei_vacio.exists():
                    imei_final = None
            
            try:
                detalle = DetalleIphone.objects.create(
                    variante=variante,
                    imei=imei_final,
                    salud_bateria=salud_bateria,
                    fallas_detectadas=data.get("fallas_observaciones"),
                    es_plan_canje=data.get("es_plan_canje", False),
                    costo_usd=data.get("costo_usd"),
                    precio_venta_usd=data.get("precio_venta_usd"),
                    precio_oferta_usd=data.get("precio_oferta_usd"),
                    notas=data.get("notas"),
                )
            except Exception as e:
                # Si hay un error de unique (por ejemplo, imei='' duplicado),
                # intentar crear con imei=None explícitamente
                if "Duplicate entry" in str(e) or "unique" in str(e).lower():
                    detalle = DetalleIphone.objects.create(
                        variante=variante,
                        imei=None,  # Forzar None explícitamente
                        salud_bateria=salud_bateria,
                        fallas_detectadas=data.get("fallas_observaciones"),
                        es_plan_canje=data.get("es_plan_canje", False),
                        costo_usd=data.get("costo_usd"),
                        precio_venta_usd=data.get("precio_venta_usd"),
                        precio_oferta_usd=data.get("precio_oferta_usd"),
                        notas=data.get("notas"),
                    )
                else:
                    raise
            
            if data.get("foto"):
                detalle.foto = data["foto"]
                detalle.save(update_fields=["foto"])

            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.CREACION,
                descripcion=f"Alta iPhone {producto.nombre} ({variante.atributos_display})",
            )
            return redirect("iphones:dashboard")
    else:
        form = AgregarIphoneForm()

    return render(request, "iphones/agregar_iphone.html", {"form": form})


@login_required
@transaction.atomic
def editar_iphone(request, variante_id):
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("inventario:dashboard")

    variante = get_object_or_404(ProductoVariante, pk=variante_id)
    producto = variante.producto
    detalle = getattr(variante, "detalle_iphone", None)

    if request.method == "POST":
        form = AgregarIphoneForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            producto.nombre = data["modelo"]
            producto.activo = data["activo"]
            producto.categoria = _categoria_celulares()
            producto.save()

            # Generar SKU automático si está habilitado o si está vacío
            sku_valor = data.get("sku", "").strip()
            if data.get("sku_auto", True) or not sku_valor:
                from django.utils.text import slugify
                nombre = data.get("modelo", "")
                capacidad = data.get("capacidad", "")
                color = data.get("color", "")
                
                # Generar SKU base
                sku_base = slugify(f"{nombre}-{capacidad}-{color}".strip("-")).upper()
                if not sku_base:
                    sku_base = slugify(nombre).upper() or "IPH"
                
                # Asegurar unicidad
                sku_final = sku_base
                contador = 1
                while ProductoVariante.objects.filter(sku=sku_final).exclude(pk=variante.pk).exists():
                    sku_final = f"{sku_base}-{contador}"
                    contador += 1
                
                variante.sku = sku_final
            else:
                variante.sku = sku_valor.upper()
            
            variante.atributo_1 = data["capacidad"]
            variante.atributo_2 = data["color"]
            variante.stock_actual = data["stock_actual"]
            variante.stock_minimo = data["stock_minimo"]
            variante.activo = data["activo"]
            
            # Generar código de barras si está habilitado
            if data.get("generar_codigo_barras"):
                import random
                codigo = f"{random.randint(100000000000, 999999999999)}"
                variante.codigo_barras = codigo
            elif data.get("codigo_barras"):
                variante.codigo_barras = data["codigo_barras"]
            
            # Generar QR code si está habilitado
            if data.get("generar_qr"):
                sku_final = variante.sku
                if sku_final:
                    qr_url = f"https://importstore.com/producto/{sku_final}"
                    variante.qr_code = qr_url
            elif data.get("qr_code"):
                variante.qr_code = data["qr_code"]
            
            variante.save()

            _sincronizar_precios(variante, data)

            if detalle is None:
                detalle = DetalleIphone(variante=variante)

            # Manejar IMEI: si está vacío, guardar como None para evitar conflictos con unique
            imei_value = data.get("imei", "").strip()
            imei_final = imei_value if imei_value else None
            
            # Si el IMEI está vacío y ya existe otro registro con imei='', 
            # necesitamos verificar y limpiar primero
            if not imei_final:
                # Verificar si hay otro registro con imei='' o imei=None
                from django.db.models import Q
                otros_con_imei_vacio = DetalleIphone.objects.filter(
                    Q(imei='') | Q(imei__isnull=True)
                ).exclude(pk=detalle.pk if detalle.pk else None)
                
                # Si hay otros con imei vacío y este también lo será, 
                # asegurarse de que este sea None (no '')
                if otros_con_imei_vacio.exists():
                    imei_final = None
            
            detalle.imei = imei_final
            # Si es nuevo, establecer salud_bateria a 100
            salud_bateria = data.get("salud_bateria")
            if data.get("es_nuevo", False):
                salud_bateria = 100
            detalle.salud_bateria = salud_bateria
            detalle.fallas_detectadas = data.get("fallas_observaciones")
            detalle.es_plan_canje = data.get("es_plan_canje", False)
            detalle.costo_usd = data.get("costo_usd")
            detalle.precio_venta_usd = data.get("precio_venta_usd")
            detalle.precio_oferta_usd = data.get("precio_oferta_usd")
            detalle.notas = data.get("notas")
            if data.get("foto"):
                detalle.foto = data["foto"]
            
            # Guardar usando update_fields para evitar problemas con unique
            try:
                detalle.save()
            except Exception as e:
                # Si hay un error de unique, intentar limpiar el IMEI a None explícitamente
                if "Duplicate entry" in str(e) or "unique" in str(e).lower():
                    detalle.imei = None
                    detalle.save()
                else:
                    raise

            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.MODIFICACION,
                descripcion=f"Actualización iPhone {producto.nombre} ({variante.atributos_display})",
            )
            return redirect("iphones:dashboard")
    else:
        detalle = getattr(variante, "detalle_iphone", None)
        precio_minorista_ars = variante.precio_activo(Precio.Tipo.MINORISTA, Precio.Moneda.ARS)
        precio_mayorista_usd = variante.precio_activo(Precio.Tipo.MAYORISTA, Precio.Moneda.USD)
        precio_mayorista_ars = variante.precio_activo(Precio.Tipo.MAYORISTA, Precio.Moneda.ARS)
        
        form = AgregarIphoneForm(
            initial={
                "modelo": producto.nombre,
                "capacidad": variante.atributo_1,
                "color": variante.atributo_2,
                "sku": variante.sku,
                "sku_auto": True,
                "codigo_barras": variante.codigo_barras or "",
                "qr_code": variante.qr_code or "",
                "stock_actual": variante.stock_actual,
                "stock_minimo": variante.stock_minimo,
                "activo": variante.activo,
                "costo_usd": detalle.costo_usd if detalle else None,
                "precio_venta_usd": detalle.precio_venta_usd if detalle else None,
                "precio_oferta_usd": detalle.precio_oferta_usd if detalle else None,
                "precio_venta_ars": precio_minorista_ars.precio if precio_minorista_ars else None,
                "precio_mayorista_usd": precio_mayorista_usd.precio if precio_mayorista_usd else None,
                "precio_mayorista_ars": precio_mayorista_ars.precio if precio_mayorista_ars else None,
                "imei": detalle.imei if detalle else "",
                "es_nuevo": detalle.salud_bateria == 100 if detalle and detalle.salud_bateria else False,
                "salud_bateria": detalle.salud_bateria if detalle else None,
                "fallas_observaciones": detalle.fallas_detectadas if detalle else "",
                "es_plan_canje": detalle.es_plan_canje if detalle else False,
                "notas": detalle.notas if detalle else "",
            }
        )

    return render(
        request,
        "iphones/editar_iphone.html",
        {"form": form, "variante": variante, "detalle": detalle},
    )


@require_POST
@login_required
def eliminar_iphone(request, variante_id):
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("inventario:dashboard")

    variante = get_object_or_404(ProductoVariante, pk=variante_id)
    producto = variante.producto

    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.ELIMINACION,
        descripcion=f"Baja iPhone {producto.nombre} ({variante.atributos_display})",
    )

    detalle = getattr(variante, "detalle_iphone", None)
    if detalle:
        detalle.delete()
    variante.delete()
    if not producto.variantes.exists():
        producto.delete()
    return redirect("iphones:dashboard")


@require_POST
@login_required
def toggle_iphone_status(request, variante_id):
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("inventario:dashboard")

    variante = get_object_or_404(ProductoVariante, pk=variante_id)
    variante.activo = not variante.activo
    variante.save()

    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.CAMBIO_ESTADO,
        descripcion=f"Estado {('activo' if variante.activo else 'inactivo')} → {variante.producto.nombre} ({variante.atributos_display})",
    )

    return redirect("iphones:dashboard")


@login_required
def iphone_historial(request):
    """Historial de iPhones vendidos (stock = 0)."""
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("inventario:dashboard")
    
    from ventas.models import DetalleVenta
    
    # Buscar iPhones vendidos (variantes con stock = 0 que tienen DetalleIphone)
    variantes_vendidas = ProductoVariante.objects.filter(
        producto__categoria__nombre__iexact="Celulares",
        stock_actual=0
    ).select_related("producto", "detalle_iphone").prefetch_related("detalles_venta__venta", "detalles_venta__venta__cliente")
    
    # Obtener información de ventas para cada variante
    historial = []
    for variante in variantes_vendidas:
        detalle_iphone = getattr(variante, "detalle_iphone", None)
        if not detalle_iphone:
            continue
        
        # Buscar la última venta de esta variante
        ultima_venta_detalle = variante.detalles_venta.select_related("venta", "venta__cliente").order_by("-venta__fecha").first()
        
        if ultima_venta_detalle:
            historial.append({
                "variante": variante,
                "detalle_iphone": detalle_iphone,
                "venta": ultima_venta_detalle.venta,
                "cliente": ultima_venta_detalle.venta.cliente,
                "cliente_nombre": ultima_venta_detalle.venta.cliente_nombre or (ultima_venta_detalle.venta.cliente.nombre if ultima_venta_detalle.venta.cliente else "Sin cliente"),
                "fecha_venta": ultima_venta_detalle.venta.fecha,
                "precio_venta": ultima_venta_detalle.precio_unitario_ars_congelado,
            })
    
    # Ordenar por fecha de venta (más reciente primero)
    historial.sort(key=lambda x: x["fecha_venta"], reverse=True)
    
    context = {
        "historial": historial,
    }
    return render(request, "iphones/historial.html", context)


@login_required
def descargar_etiqueta_iphone(request, detalle_id: int):
    """Genera y devuelve la etiqueta térmica PDF para un iPhone específico."""
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("iphones:dashboard")

    detalle = get_object_or_404(
        DetalleIphone.objects.select_related("variante", "variante__producto"),
        pk=detalle_id,
    )

    buffer = BytesIO()
    generar_etiqueta(buffer, detalle)
    pdf_bytes = buffer.getvalue()

    sku = detalle.variante.sku if detalle.variante else "iphone"
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="etiqueta_{sku}.pdf"'
    return response


# ============ PLAN CANJE ============

def _calcular_valor_canje(modelo, capacidad, bateria, estado, accesorios, pantalla=None, marco=None, botones=None, camara=None, dolar_blue=None):
    """Calcula el valor de canje de un iPhone usado."""
    try:
        config = PlanCanjeConfig.objects.get(
            modelo_iphone=modelo,
            capacidad=capacidad,
            activo=True
        )
    except PlanCanjeConfig.DoesNotExist:
        return None
    
    valor_base = Decimal(str(config.valor_base_canje_usd))
    
    # Calcular descuentos
    descuentos_bateria = config.descuentos_bateria or {}
    descuento_bateria = Decimal("0")
    if bateria < 80:
        descuento_bateria = Decimal(str(descuentos_bateria.get("<80", 0)))
    elif bateria < 90:
        descuento_bateria = Decimal(str(descuentos_bateria.get("80-90", 0)))
    else:
        descuento_bateria = Decimal(str(descuentos_bateria.get(">90", 0)))
    
    descuentos_estado = config.descuentos_estado or {}
    descuento_estado = Decimal(str(descuentos_estado.get(estado, 0)))
    
    descuentos_accesorios = config.descuentos_accesorios or {}
    descuento_accesorios = Decimal("0")
    if not accesorios.get("caja", False):
        descuento_accesorios += Decimal(str(descuentos_accesorios.get("sin_caja", 0)))
    
    # Descuentos adicionales por componentes (solo si no es "desconocido")
    descuento_pantalla = Decimal("0")
    if pantalla and pantalla != "desconocido" and config.descuentos_pantalla:
        descuento_pantalla = Decimal(str(config.descuentos_pantalla.get(pantalla, 0)))
    
    descuento_marco = Decimal("0")
    if marco and marco != "desconocido" and config.descuentos_marco:
        descuento_marco = Decimal(str(config.descuentos_marco.get(marco, 0)))
    
    descuento_botones = Decimal("0")
    if botones and botones != "desconocido" and config.descuentos_botones:
        descuento_botones = Decimal(str(config.descuentos_botones.get(botones, 0)))
    
    descuento_camara = Decimal("0")
    if camara and camara != "desconocido" and config.descuentos_camara:
        descuento_camara = Decimal(str(config.descuentos_camara.get(camara, 0)))
    
    # Calcular valor final
    descuento_total = descuento_bateria + descuento_estado + descuento_accesorios + descuento_pantalla + descuento_marco + descuento_botones + descuento_camara
    valor_final_usd = valor_base * (Decimal("1") - descuento_total)
    valor_final_ars = valor_final_usd * Decimal(str(dolar_blue)) if dolar_blue else Decimal("0")
    
    return {
        "config": config,
        "valor_base_usd": valor_base,
        "descuento_bateria": descuento_bateria,
        "descuento_estado": descuento_estado,
        "descuento_accesorios": descuento_accesorios,
        "descuento_pantalla": descuento_pantalla,
        "descuento_marco": descuento_marco,
        "descuento_botones": descuento_botones,
        "descuento_camara": descuento_camara,
        "descuento_total": descuento_total,
        "valor_final_usd": valor_final_usd,
        "valor_final_ars": valor_final_ars,
    }


@login_required
def plan_canje_calculadora(request):
    """Vista principal de la calculadora de Plan Canje."""
    dolar_blue = obtener_valor_dolar_blue() or 0
    
    # Obtener iPhones en stock (categoría Celulares)
    iphones_stock = (
        ProductoVariante.objects
        .select_related("producto", "producto__categoria")
        .prefetch_related("precios")
        .filter(
            producto__categoria__nombre__iexact="Celulares",
            stock_actual__gt=0,
            activo=True
        )
        .order_by("producto__nombre", "atributo_1", "atributo_2")
    )
    
    # Enriquecer cada iPhone con precios calculados
    iphones_con_precios = []
    for iphone in iphones_stock:
        precio_ars_obj = iphone.precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.ARS, activo=True).first()
        precio_usd_obj = iphone.precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.USD, activo=True).first()
        
        precio_ars = float(precio_ars_obj.precio) if precio_ars_obj else 0
        precio_usd = float(precio_usd_obj.precio) if precio_usd_obj else 0
        
        # Si solo tiene ARS, convertir a USD
        if precio_ars > 0 and precio_usd == 0 and dolar_blue > 0:
            precio_usd = precio_ars / dolar_blue
        # Si solo tiene USD, convertir a ARS
        elif precio_usd > 0 and precio_ars == 0 and dolar_blue > 0:
            precio_ars = precio_usd * dolar_blue
        
        iphone.precio_ars_calculado = precio_ars
        iphone.precio_usd_calculado = precio_usd
        iphones_con_precios.append(iphone)
    
    # Obtener configuraciones activas para el selector
    configs_activas_list = list(PlanCanjeConfig.objects.filter(activo=True))
    
    # Ordenar por modelo y luego por capacidad (de menor a mayor)
    configs_activas_list.sort(key=lambda x: (x.modelo_iphone, _capacidad_a_gb(x.capacidad)))
    
    # Obtener modelos únicos para el dropdown
    modelos_unicos = sorted(set(config.modelo_iphone for config in configs_activas_list))
    
    context = {
        "iphones_stock": iphones_con_precios,
        "configs_activas": configs_activas_list,
        "modelos_unicos": modelos_unicos,
        "dolar_blue": dolar_blue,
    }
    return render(request, "iphones/plan_canje_calculadora.html", context)


@login_required
def plan_canje_calcular_api(request):
    """API para calcular el valor de canje en tiempo real."""
    from django.http import JsonResponse
    import json
    
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        modelo = data.get("modelo")
        capacidad = data.get("capacidad")
        bateria = int(data.get("bateria", 100))
        estado = data.get("estado")
        accesorios = data.get("accesorios", {})
        pantalla = data.get("pantalla")
        marco = data.get("marco")
        botones = data.get("botones")
        camara = data.get("camara")
        
        dolar_blue = obtener_valor_dolar_blue() or 0
        
        resultado = _calcular_valor_canje(
            modelo, capacidad, bateria, estado, accesorios,
            pantalla=pantalla, marco=marco, botones=botones, camara=camara,
            dolar_blue=dolar_blue
        )
        
        if not resultado:
            return JsonResponse({"error": "No se encontró configuración para este modelo y capacidad"}, status=404)
        
        return JsonResponse({
            "success": True,
            "valor_base_usd": float(resultado["valor_base_usd"]),
            "descuento_bateria": float(resultado["descuento_bateria"]),
            "descuento_estado": float(resultado["descuento_estado"]),
            "descuento_accesorios": float(resultado["descuento_accesorios"]),
            "descuento_pantalla": float(resultado["descuento_pantalla"]),
            "descuento_marco": float(resultado["descuento_marco"]),
            "descuento_botones": float(resultado["descuento_botones"]),
            "descuento_camara": float(resultado["descuento_camara"]),
            "descuento_total": float(resultado["descuento_total"]),
            "valor_final_usd": float(resultado["valor_final_usd"]),
            "valor_final_ars": float(resultado["valor_final_ars"]),
            "guia_estado_excelente": resultado["config"].guia_estado_excelente or "",
            "guia_estado_bueno": resultado["config"].guia_estado_bueno or "",
            "guia_estado_regular": resultado["config"].guia_estado_regular or "",
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@transaction.atomic
def plan_canje_aplicar_api(request):
    """API para aplicar un canje y crear la transacción."""
    from django.http import JsonResponse
    from django.utils import timezone
    from ventas.models import Venta, DetalleVenta
    from ventas.views import _resolver_precio_ars, _generar_id_venta
    import json
    
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Datos del iPhone recibido
        modelo_recibido = data.get("modelo_recibido")
        capacidad_recibida = data.get("capacidad_recibida")
        color_recibido = data.get("color_recibido", "")
        imei_recibido = data.get("imei_recibido", "")
        bateria_recibida = int(data.get("bateria_recibida", 100))
        estado_recibido = data.get("estado_recibido")
        pantalla_recibida = data.get("pantalla_recibida", "")
        marco_recibido = data.get("marco_recibido", "")
        botones_recibido = data.get("botones_recibido", "")
        camara_recibida = data.get("camara_recibida", "")
        accesorios_recibidos = data.get("accesorios_recibidos", {})
        observaciones_recibido = data.get("observaciones_recibido", "")
        
        # Datos del iPhone entregado
        variante_entregada_id = data.get("variante_entregada_id")
        ajuste_manual = Decimal(str(data.get("ajuste_manual", 0)))
        
        # Cliente (opcional)
        cliente_id = data.get("cliente_id")
        cliente_nombre = data.get("cliente_nombre", "")
        cliente_documento = data.get("cliente_documento", "")
        
        # Validaciones
        if not modelo_recibido or not capacidad_recibida:
            return JsonResponse({"error": "Faltan datos del iPhone recibido"}, status=400)
        
        if not variante_entregada_id:
            return JsonResponse({"error": "Debe seleccionar un iPhone para entregar"}, status=400)
        
        variante_entregada = get_object_or_404(ProductoVariante, pk=variante_entregada_id)
        
        if variante_entregada.stock_actual < 1:
            return JsonResponse({"error": "No hay stock disponible del iPhone seleccionado"}, status=400)
        
        # Calcular valor del usado
        dolar_blue = obtener_valor_dolar_blue() or 0
        calculo = _calcular_valor_canje(
            modelo_recibido, capacidad_recibida, bateria_recibida,
            estado_recibido, accesorios_recibidos,
            pantalla=pantalla_recibida, marco=marco_recibido,
            botones=botones_recibido, camara=camara_recibida,
            dolar_blue=dolar_blue
        )
        
        if not calculo:
            return JsonResponse({"error": "No se encontró configuración para este modelo"}, status=404)
        
        # Obtener precio del iPhone nuevo
        precio_ars, precio_usd, tipo_cambio = _resolver_precio_ars(variante_entregada, "MINORISTA")
        
        if precio_ars == 0:
            return JsonResponse({"error": "El iPhone seleccionado no tiene precio configurado"}, status=400)
        
        # Calcular diferencia
        valor_usado_ars = calculo["valor_final_ars"] + ajuste_manual
        diferencia_ars = precio_ars - valor_usado_ars
        
        # Crear DetalleIphone para el usado recibido
        categoria_celulares = _categoria_celulares()
        
        # Buscar o crear producto para el iPhone recibido
        producto_recibido, _ = Producto.objects.get_or_create(
            nombre=modelo_recibido,
            categoria=categoria_celulares,
            defaults={"descripcion": f"iPhone recibido en canje - {capacidad_recibida}"}
        )
        
        # Crear variante para el iPhone recibido
        sku_recibido = f"CANJE-{timezone.now().strftime('%Y%m%d')}-{uuid4().hex[:6].upper()}"
        variante_recibida = ProductoVariante.objects.create(
            producto=producto_recibido,
            sku=sku_recibido,
            atributo_1=capacidad_recibida,
            atributo_2=color_recibido,
            stock_actual=1,
            activo=True
        )
        
        # Crear DetalleIphone
        detalle_recibido = DetalleIphone.objects.create(
            variante=variante_recibida,
            imei=imei_recibido if imei_recibido else None,
            salud_bateria=bateria_recibida,
            fallas_detectadas=observaciones_recibido,
            es_plan_canje=True,
            costo_usd=calculo["valor_final_usd"],
            precio_venta_usd=calculo["valor_final_usd"] * Decimal("1.2"),  # 20% margen
        )
        
        # Crear Venta
        venta_id = _generar_id_venta("CANJE")
        venta = Venta.objects.create(
            id=venta_id,
            cliente_id=cliente_id if cliente_id else None,
            cliente_nombre=cliente_nombre,
            cliente_documento=cliente_documento,
            subtotal_ars=precio_ars,
            descuento_total_ars=Decimal("0"),
            impuestos_ars=Decimal("0"),
            total_ars=diferencia_ars if diferencia_ars > 0 else Decimal("0"),
            metodo_pago="EFECTIVO_ARS",
            status=Venta.Status.PAGADO,
            nota=f"Plan Canje: {modelo_recibido} {capacidad_recibida} por {variante_entregada.producto.nombre}",
            vendedor=request.user,
        )
        
        # Crear DetalleVenta
        DetalleVenta.objects.create(
            venta=venta,
            variante=variante_entregada,
            sku=variante_entregada.sku,
            descripcion=f"{variante_entregada.producto.nombre} {variante_entregada.atributos_display}",
            cantidad=1,
            precio_unitario_ars_congelado=precio_ars,
            subtotal_ars=precio_ars,
            precio_unitario_usd_original=precio_usd,
            tipo_cambio_usado=tipo_cambio,
        )
        
        # Actualizar stock
        variante_entregada.stock_actual -= 1
        variante_entregada.save()
        
        # Crear transacción de canje
        transaccion = PlanCanjeTransaccion.objects.create(
            fecha=timezone.now(),
            cliente_id=cliente_id if cliente_id else None,
            cliente_nombre=cliente_nombre,
            cliente_documento=cliente_documento,
            iphone_recibido_modelo=modelo_recibido,
            iphone_recibido_capacidad=capacidad_recibida,
            iphone_recibido_color=color_recibido,
            iphone_recibido_imei=imei_recibido,
            iphone_recibido_bateria=bateria_recibida,
            iphone_recibido_estado=estado_recibido,
            iphone_recibido_estado_pantalla=pantalla_recibida,
            iphone_recibido_estado_marco=marco_recibido,
            iphone_recibido_estado_botones=botones_recibido,
            iphone_recibido_estado_camara=camara_recibida,
            iphone_recibido_accesorios=accesorios_recibidos,
            iphone_recibido_observaciones=observaciones_recibido,
            valor_base_usd=calculo["valor_base_usd"],
            descuento_bateria_porcentaje=calculo["descuento_bateria"] * 100,
            descuento_estado_porcentaje=calculo["descuento_estado"] * 100,
            descuento_accesorios_porcentaje=calculo["descuento_accesorios"] * 100,
            descuento_pantalla_porcentaje=calculo["descuento_pantalla"] * 100,
            descuento_marco_porcentaje=calculo["descuento_marco"] * 100,
            descuento_botones_porcentaje=calculo["descuento_botones"] * 100,
            descuento_camara_porcentaje=calculo["descuento_camara"] * 100,
            valor_calculado_usd=calculo["valor_final_usd"],
            valor_calculado_ars=calculo["valor_final_ars"],
            ajuste_manual_ars=ajuste_manual,
            iphone_entregado=variante_entregada,
            valor_iphone_entregado_ars=precio_ars,
            diferencia_ars=diferencia_ars,
            venta_asociada=venta,
            detalle_iphone_recibido=detalle_recibido,
            vendedor=request.user,
        )
        
        # Registrar en historial
        RegistroHistorial.objects.create(
            usuario=request.user,
            accion="PLAN_CANJE_CREADO",
            descripcion=f"Plan Canje creado: {modelo_recibido} por {variante_entregada.producto.nombre}",
            objeto_id=transaccion.id,
            objeto_tipo="PlanCanjeTransaccion",
        )
        
        return JsonResponse({
            "success": True,
            "transaccion_id": transaccion.id,
            "venta_id": venta.id,
            "diferencia_ars": float(diferencia_ars),
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({"error": str(e), "traceback": traceback.format_exc()}, status=400)


def _capacidad_a_gb(capacidad: str) -> int:
    """Convierte una capacidad (ej: '128GB', '1TB') a GB para ordenar."""
    if not capacidad:
        return 0
    capacidad_upper = capacidad.upper().strip()
    if 'TB' in capacidad_upper:
        num = float(capacidad_upper.replace('TB', '').strip())
        return int(num * 1024)  # 1TB = 1024GB
    elif 'GB' in capacidad_upper:
        return int(float(capacidad_upper.replace('GB', '').strip()))
    return 0


@login_required
def plan_canje_config(request):
    """Vista de configuración de valores base de Plan Canje."""
    configs = list(PlanCanjeConfig.objects.all())
    
    # Ordenar por modelo y luego por capacidad (de menor a mayor)
    configs.sort(key=lambda x: (x.modelo_iphone, _capacidad_a_gb(x.capacidad)))
    
    context = {
        "configs": configs,
    }
    return render(request, "iphones/plan_canje_config.html", context)


@login_required
@transaction.atomic
def plan_canje_precargar_modelos_api(request):
    """API para precargar todos los modelos de iPhone 11-17 con sus capacidades."""
    from django.http import JsonResponse
    
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    modelos_iphone = [
        {"nombre": "iPhone 11", "capacidades": ["64GB", "128GB", "256GB"], "colores": ["Negro", "Blanco", "Verde", "Amarillo", "Morado", "Rojo"]},
        {"nombre": "iPhone 11 Pro", "capacidades": ["64GB", "256GB", "512GB"], "colores": ["Gris Espacial", "Plata", "Oro", "Verde Medianoche"]},
        {"nombre": "iPhone 11 Pro Max", "capacidades": ["64GB", "256GB", "512GB"], "colores": ["Gris Espacial", "Plata", "Oro", "Verde Medianoche"]},
        {"nombre": "iPhone 12", "capacidades": ["64GB", "128GB", "256GB"], "colores": ["Negro", "Blanco", "Rojo", "Verde", "Azul", "Morado"]},
        {"nombre": "iPhone 12 mini", "capacidades": ["64GB", "128GB", "256GB"], "colores": ["Negro", "Blanco", "Rojo", "Verde", "Azul", "Morado"]},
        {"nombre": "iPhone 12 Pro", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Gris Espacial", "Plata", "Oro", "Azul Pacífico"]},
        {"nombre": "iPhone 12 Pro Max", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Gris Espacial", "Plata", "Oro", "Azul Pacífico"]},
        {"nombre": "iPhone 13", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Azul", "Medianoche", "Estelar", "Rojo"]},
        {"nombre": "iPhone 13 mini", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Azul", "Medianoche", "Estelar", "Rojo"]},
        {"nombre": "iPhone 13 Pro", "capacidades": ["128GB", "256GB", "512GB", "1TB"], "colores": ["Grafito", "Oro", "Plata", "Azul Sierra"]},
        {"nombre": "iPhone 13 Pro Max", "capacidades": ["128GB", "256GB", "512GB", "1TB"], "colores": ["Grafito", "Oro", "Plata", "Azul Sierra"]},
        {"nombre": "iPhone 14", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Azul", "Morado", "Medianoche", "Estelar", "Rojo"]},
        {"nombre": "iPhone 14 Plus", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Azul", "Morado", "Medianoche", "Estelar", "Rojo"]},
        {"nombre": "iPhone 14 Pro", "capacidades": ["128GB", "256GB", "512GB", "1TB"], "colores": ["Púrpura Profundo", "Oro", "Plata", "Negro Espacial"]},
        {"nombre": "iPhone 14 Pro Max", "capacidades": ["128GB", "256GB", "512GB", "1TB"], "colores": ["Púrpura Profundo", "Oro", "Plata", "Negro Espacial"]},
        {"nombre": "iPhone 15", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Amarillo", "Verde", "Azul", "Negro"]},
        {"nombre": "iPhone 15 Plus", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Amarillo", "Verde", "Azul", "Negro"]},
        {"nombre": "iPhone 15 Pro", "capacidades": ["128GB", "256GB", "512GB", "1TB"], "colores": ["Titanio Natural", "Titanio Azul", "Titanio Blanco", "Titanio Negro"]},
        {"nombre": "iPhone 15 Pro Max", "capacidades": ["256GB", "512GB", "1TB"], "colores": ["Titanio Natural", "Titanio Azul", "Titanio Blanco", "Titanio Negro"]},
        {"nombre": "iPhone 16", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Amarillo", "Verde", "Azul", "Negro"]},
        {"nombre": "iPhone 16 Plus", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Amarillo", "Verde", "Azul", "Negro"]},
        {"nombre": "iPhone 16 Pro", "capacidades": ["256GB", "512GB", "1TB"], "colores": ["Titanio Desértico", "Titanio Gris", "Titanio Blanco", "Titanio Negro"]},
        {"nombre": "iPhone 16 Pro Max", "capacidades": ["256GB", "512GB", "1TB"], "colores": ["Titanio Desértico", "Titanio Gris", "Titanio Blanco", "Titanio Negro"]},
        {"nombre": "iPhone 17", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Amarillo", "Verde", "Azul", "Negro"]},
        {"nombre": "iPhone 17 Plus", "capacidades": ["128GB", "256GB", "512GB"], "colores": ["Rosa", "Amarillo", "Verde", "Azul", "Negro"]},
        {"nombre": "iPhone 17 Pro", "capacidades": ["256GB", "512GB", "1TB"], "colores": ["Titanio Natural", "Titanio Azul", "Titanio Blanco", "Titanio Negro"]},
        {"nombre": "iPhone 17 Pro Max", "capacidades": ["256GB", "512GB", "1TB"], "colores": ["Titanio Natural", "Titanio Azul", "Titanio Blanco", "Titanio Negro"]},
    ]
    
    creados = 0
    actualizados = 0
    
    # Valores por defecto para descuentos
    descuentos_default = {
        "bateria": {"<80": 0.15, "80-90": 0.10, ">90": 0.0},
        "estado": {"excelente": 0.0, "bueno": 0.05, "regular": 0.15},
        "accesorios": {"sin_caja": 0.02},
        "pantalla": {"perfecta": 0.0, "rayas_menores": 0.03, "rayas_visibles": 0.08, "grieta": 0.15},
        "marco": {"perfecto": 0.0, "arañazos": 0.02, "golpes": 0.05, "deformado": 0.10},
        "botones": {"todos_funcionan": 0.0, "alguno_no_funciona": 0.05, "varios_no_funcionan": 0.10},
        "camara": {"perfecta": 0.0, "rayas_menores": 0.02, "rayas_visibles": 0.05, "rota": 0.15},
    }
    
    guias_default = {
        "excelente": "Sin rayas, sin golpes visibles, pantalla perfecta, marco sin arañazos, todos los botones funcionan correctamente, cámara sin daños",
        "bueno": "1-2 rayitas menores en pantalla o marco, pequeños arañazos, pantalla con rayas menores que no afectan uso, botones funcionan",
        "regular": "Múltiples rayas visibles, golpes en marco, pantalla con rayas que afectan uso o grietas menores, algún botón no funciona correctamente, cámara con rayas visibles"
    }
    
    for modelo_data in modelos_iphone:
        modelo_nombre = modelo_data["nombre"]
        for capacidad in modelo_data["capacidades"]:
            config, created = PlanCanjeConfig.objects.get_or_create(
                modelo_iphone=modelo_nombre,
                capacidad=capacidad,
                defaults={
                    "valor_base_canje_usd": Decimal("0"),  # El usuario lo configurará manualmente
                    "descuentos_bateria": descuentos_default["bateria"],
                    "descuentos_estado": descuentos_default["estado"],
                    "descuentos_accesorios": descuentos_default["accesorios"],
                    "descuentos_pantalla": descuentos_default["pantalla"],
                    "descuentos_marco": descuentos_default["marco"],
                    "descuentos_botones": descuentos_default["botones"],
                    "descuentos_camara": descuentos_default["camara"],
                    "guia_estado_excelente": guias_default["excelente"],
                    "guia_estado_bueno": guias_default["bueno"],
                    "guia_estado_regular": guias_default["regular"],
                    "activo": True,
                }
            )
            if created:
                creados += 1
            else:
                # Actualizar descuentos si no existen
                if not config.descuentos_pantalla:
                    config.descuentos_pantalla = descuentos_default["pantalla"]
                if not config.descuentos_marco:
                    config.descuentos_marco = descuentos_default["marco"]
                if not config.descuentos_botones:
                    config.descuentos_botones = descuentos_default["botones"]
                if not config.descuentos_camara:
                    config.descuentos_camara = descuentos_default["camara"]
                if not config.guia_estado_excelente:
                    config.guia_estado_excelente = guias_default["excelente"]
                if not config.guia_estado_bueno:
                    config.guia_estado_bueno = guias_default["bueno"]
                if not config.guia_estado_regular:
                    config.guia_estado_regular = guias_default["regular"]
                config.save()
                actualizados += 1
    
    return JsonResponse({
        "success": True,
        "creados": creados,
        "actualizados": actualizados,
        "total": creados + actualizados,
    })


@login_required
@transaction.atomic
def plan_canje_config_guardar_api(request):
    """API para crear o actualizar una configuración de Plan Canje."""
    from django.http import JsonResponse
    import json
    
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        config_id = data.get("id")
        
        # Validar campos requeridos
        modelo = data.get("modelo_iphone", "").strip()
        capacidad = data.get("capacidad", "").strip()
        valor_base = data.get("valor_base_canje_usd")
        
        if not modelo or not capacidad or not valor_base:
            return JsonResponse({"error": "Faltan campos requeridos: modelo, capacidad, valor_base_canje_usd"}, status=400)
        
        try:
            valor_base_decimal = Decimal(str(valor_base))
        except (ValueError, TypeError):
            return JsonResponse({"error": "El valor base debe ser un número válido"}, status=400)
        
        # Parsear descuentos JSON
        descuentos_bateria = data.get("descuentos_bateria", {})
        descuentos_estado = data.get("descuentos_estado", {})
        descuentos_accesorios = data.get("descuentos_accesorios", {})
        descuentos_pantalla = data.get("descuentos_pantalla", {})
        descuentos_marco = data.get("descuentos_marco", {})
        descuentos_botones = data.get("descuentos_botones", {})
        descuentos_camara = data.get("descuentos_camara", {})
        
        # Validar que sean diccionarios
        if not isinstance(descuentos_bateria, dict):
            descuentos_bateria = {}
        if not isinstance(descuentos_estado, dict):
            descuentos_estado = {}
        if not isinstance(descuentos_accesorios, dict):
            descuentos_accesorios = {}
        if not isinstance(descuentos_pantalla, dict):
            descuentos_pantalla = {}
        if not isinstance(descuentos_marco, dict):
            descuentos_marco = {}
        if not isinstance(descuentos_botones, dict):
            descuentos_botones = {}
        if not isinstance(descuentos_camara, dict):
            descuentos_camara = {}
        
        # Guías de ayuda
        guia_excelente = data.get("guia_estado_excelente", "").strip()
        guia_bueno = data.get("guia_estado_bueno", "").strip()
        guia_regular = data.get("guia_estado_regular", "").strip()
        activo = data.get("activo", True)
        
        if config_id:
            # Actualizar configuración existente
            config = get_object_or_404(PlanCanjeConfig, pk=config_id)
            # Verificar que no haya duplicado (mismo modelo y capacidad pero diferente ID)
            if PlanCanjeConfig.objects.filter(modelo_iphone=modelo, capacidad=capacidad).exclude(pk=config_id).exists():
                return JsonResponse({"error": "Ya existe una configuración para este modelo y capacidad"}, status=400)
        else:
            # Crear nueva configuración
            if PlanCanjeConfig.objects.filter(modelo_iphone=modelo, capacidad=capacidad).exists():
                return JsonResponse({"error": "Ya existe una configuración para este modelo y capacidad"}, status=400)
            config = PlanCanjeConfig()
        
        # Asignar valores
        config.modelo_iphone = modelo
        config.capacidad = capacidad
        config.valor_base_canje_usd = valor_base_decimal
        config.descuentos_bateria = descuentos_bateria
        config.descuentos_estado = descuentos_estado
        config.descuentos_accesorios = descuentos_accesorios
        config.descuentos_pantalla = descuentos_pantalla
        config.descuentos_marco = descuentos_marco
        config.descuentos_botones = descuentos_botones
        config.descuentos_camara = descuentos_camara
        config.guia_estado_excelente = guia_excelente
        config.guia_estado_bueno = guia_bueno
        config.guia_estado_regular = guia_regular
        config.activo = activo
        config.save()
        
        return JsonResponse({
            "success": True,
            "config": {
                "id": config.id,
                "modelo_iphone": config.modelo_iphone,
                "capacidad": config.capacidad,
                "valor_base_canje_usd": float(config.valor_base_canje_usd),
                "activo": config.activo,
            }
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({"error": str(e), "traceback": traceback.format_exc()}, status=400)


@login_required
def plan_canje_config_obtener_api(request, config_id):
    """API para obtener una configuración específica."""
    from django.http import JsonResponse
    
    config = get_object_or_404(PlanCanjeConfig, pk=config_id)
    
    return JsonResponse({
        "id": config.id,
        "modelo_iphone": config.modelo_iphone,
        "capacidad": config.capacidad,
        "valor_base_canje_usd": float(config.valor_base_canje_usd),
        "descuentos_bateria": config.descuentos_bateria or {},
        "descuentos_estado": config.descuentos_estado or {},
        "descuentos_accesorios": config.descuentos_accesorios or {},
        "descuentos_pantalla": config.descuentos_pantalla or {},
        "descuentos_marco": config.descuentos_marco or {},
        "descuentos_botones": config.descuentos_botones or {},
        "descuentos_camara": config.descuentos_camara or {},
        "guia_estado_excelente": config.guia_estado_excelente or "",
        "guia_estado_bueno": config.guia_estado_bueno or "",
        "guia_estado_regular": config.guia_estado_regular or "",
        "activo": config.activo,
    })


@login_required
@transaction.atomic
def plan_canje_config_eliminar_api(request, config_id):
    """API para eliminar una configuración."""
    from django.http import JsonResponse
    
    config = get_object_or_404(PlanCanjeConfig, pk=config_id)
    config.delete()
    
    return JsonResponse({"success": True})


@login_required
def plan_canje_historial(request):
    """Vista de historial de transacciones de Plan Canje."""
    transacciones = PlanCanjeTransaccion.objects.select_related(
        "cliente", "iphone_entregado", "venta_asociada", "vendedor"
    ).order_by("-fecha")
    
    context = {
        "transacciones": transacciones,
    }
    return render(request, "iphones/plan_canje_historial.html", context)
