from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from django.contrib import messages
from core.db_inspector import column_exists
from core.utils import obtener_valor_dolar_blue
from historial.models import RegistroHistorial
from inventario.models import (
    Categoria,
    DetalleIphone,
    Precio,
    Producto,
    ProductoVariante,
)
from inventario.utils import is_detalleiphone_variante_ready

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
    combinaciones = [
        (Precio.Tipo.MINORISTA, Precio.Moneda.USD, data.get("precio_venta_usd")),
        (Precio.Tipo.MINORISTA, Precio.Moneda.ARS, data.get("precio_venta_ars")),
        (Precio.Tipo.MAYORISTA, Precio.Moneda.USD, data.get("precio_mayorista_usd") or data.get("precio_venta_usd")),
        (Precio.Tipo.MAYORISTA, Precio.Moneda.ARS, data.get("precio_mayorista_ars") or data.get("precio_venta_ars")),
    ]

    for tipo, moneda, valor in combinaciones:
        if valor is None or valor == "":
            variante.precios.filter(tipo=tipo, moneda=moneda).update(activo=False)
            continue
        try:
            variante.precios.update_or_create(
                tipo=tipo,
                moneda=moneda,
                defaults={"precio": valor, "activo": True, "tipo": tipo, "moneda": moneda},
            )
        except Exception as e:
            # Si falla por tipo_precio o costo, intentar crear directamente con SQL
            from django.db import connection
            from core.db_inspector import column_exists
            
            with connection.cursor() as cursor:
                # Verificar si existe el precio
                cursor.execute(
                    "SELECT id FROM inventario_precio WHERE variante_id = %s AND tipo = %s AND moneda = %s",
                    [variante.id, tipo, moneda]
                )
                existing = cursor.fetchone()
                if existing:
                    # Actualizar existente - solo campos que existen
                    try:
                        cursor.execute(
                            "UPDATE inventario_precio SET precio = %s, activo = 1, tipo = %s, moneda = %s, actualizado = NOW() WHERE id = %s",
                            [valor, tipo, moneda, existing[0]]
                        )
                    except Exception as e2:
                        # Si falla, intentar sin actualizar tipo/moneda
                        cursor.execute(
                            "UPDATE inventario_precio SET precio = %s, activo = 1, actualizado = NOW() WHERE id = %s",
                            [valor, existing[0]]
                        )
                else:
                    # Crear nuevo - verificar qué columnas existen
                    table_name = "inventario_precio"
                    has_tipo_precio = column_exists(table_name, "tipo_precio")
                    has_costo = column_exists(table_name, "costo")
                    has_precio_venta_normal = column_exists(table_name, "precio_venta_normal")
                    has_precio_venta_minimo = column_exists(table_name, "precio_venta_minimo")
                    has_precio_venta_descuento = column_exists(table_name, "precio_venta_descuento")
                    
                    # Construir INSERT dinámicamente según columnas existentes
                    columns = ["variante_id", "tipo", "moneda", "precio", "activo", "creado", "actualizado"]
                    values = [variante.id, tipo, moneda, valor, 1, "NOW()", "NOW()"]
                    placeholders = ["%s", "%s", "%s", "%s", "%s", "NOW()", "NOW()"]
                    
                    if has_tipo_precio:
                        columns.append("tipo_precio")
                        values.append(tipo)
                        placeholders.append("%s")
                    
                    if has_costo:
                        columns.append("costo")
                        values.append(0)
                        placeholders.append("%s")
                    
                    if has_precio_venta_normal:
                        columns.append("precio_venta_normal")
                        values.append(valor)
                        placeholders.append("%s")
                    
                    if has_precio_venta_minimo:
                        columns.append("precio_venta_minimo")
                        values.append(valor)
                        placeholders.append("%s")
                    
                    # Construir query SQL
                    cols_str = ", ".join(columns)
                    placeholders_str = ", ".join(placeholders)
                    sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders_str})"
                    
                    # Preparar valores para placeholders (solo los que son %s)
                    sql_values = []
                    for i, ph in enumerate(placeholders):
                        if ph == "%s":
                            sql_values.append(values[i])
                    
                    cursor.execute(sql, sql_values)


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
        ProductoVariante.objects.select_related("producto", "producto__categoria")
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
        else:
            variante.detalle_cache = None

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
            
            detalle = DetalleIphone.objects.create(
                variante=variante,
                imei=data.get("imei"),
                salud_bateria=salud_bateria,
                fallas_detectadas=data.get("fallas_observaciones"),
                es_plan_canje=data.get("es_plan_canje", False),
                costo_usd=data.get("costo_usd"),
                precio_venta_usd=data.get("precio_venta_usd"),
                precio_oferta_usd=data.get("precio_oferta_usd"),
                notas=data.get("notas"),
            )
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

            detalle.imei = data.get("imei")
            detalle.salud_bateria = data.get("salud_bateria")
            detalle.fallas_detectadas = data.get("fallas_observaciones")
            detalle.es_plan_canje = data.get("es_plan_canje", False)
            detalle.costo_usd = data.get("costo_usd")
            detalle.precio_venta_usd = data.get("precio_venta_usd")
            detalle.precio_oferta_usd = data.get("precio_oferta_usd")
            detalle.notas = data.get("notas")
            if data.get("foto"):
                detalle.foto = data["foto"]
            detalle.save()

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
