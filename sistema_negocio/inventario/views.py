import base64
import json
import logging
import os
from decimal import Decimal

import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db import models, transaction
from django.db.models import DecimalField, OuterRef, Subquery, F, Sum
from django.db.models.functions import Cast, Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from core.db_inspector import column_exists
from core.utils import obtener_valor_dolar_blue
from historial.models import RegistroHistorial

from .forms import (
    CategoriaForm,
    ImportacionInventarioForm,
    InventarioFiltroForm,
    ProductoForm,
    ProductoVarianteForm,
    ProveedorForm,
)
from .models import Categoria, Precio, Producto, ProductoImagen, ProductoVariante, Proveedor
from .utils import is_detalleiphone_variante_ready
from .importers import exportar_catalogo_a_csv, exportar_catalogo_a_excel, importar_catalogo_desde_archivo, generar_excel_vacio
from asistente_ia.interpreter import _invoke_gemini


logger = logging.getLogger(__name__)


SCHEMA_REQUIREMENTS = (
    ("inventario_productovariante", "sku"),
    ("inventario_productovariante", "stock_actual"),
    ("inventario_productovariante", "stock_minimo"),
    ("inventario_productovariante", "activo"),
    ("inventario_producto", "activo"),
    ("inventario_precio", "precio"),
)


PRECIO_FIELDS = (
    "costo_usd",
    "costo_ars",
    "precio_venta_usd",
    "precio_venta_ars",
    "precio_minimo_usd",
    "precio_minimo_ars",
    "precio_minorista_usd",
    "precio_minorista_ars",
    "precio_mayorista_usd",
    "precio_mayorista_ars",
)

MAX_PRODUCT_IMAGES = 5


def _reordenar_imagenes(producto: Producto) -> None:
    for orden, imagen in enumerate(producto.imagenes.order_by("orden", "id"), start=0):
        if imagen.orden != orden:
            ProductoImagen.objects.filter(pk=imagen.pk).update(orden=orden)


def _guardar_imagenes_producto(producto: Producto, archivos) -> None:
    if not archivos:
        return
    inicio = producto.imagenes.count()
    for offset, archivo in enumerate(archivos):
        ProductoImagen.objects.create(
            producto=producto,
            imagen=archivo,
            orden=inicio + offset,
        )


def _procesar_remove_bg(uploaded_file):
    api_key = getattr(settings, "REMOVEBG_API_KEY", "")
    if not api_key:
        raise RuntimeError("Configura la variable REMOVEBG_API_KEY para usar quitar fondo.")

    try:
        uploaded_file.seek(0)
        files = {
            "image_file": (
                uploaded_file.name,
                uploaded_file.read(),
                uploaded_file.content_type or "image/png",
            )
        }
        uploaded_file.seek(0)
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            data={"size": "auto"},
            files=files,
            headers={"X-Api-Key": api_key},
            timeout=getattr(settings, "REQUESTS_TIMEOUT_SECONDS", 30),
        )
    except requests.RequestException as exc:
        logger.warning("Error comunicando con remove.bg: %s", exc)
        raise RuntimeError("No se pudo conectar con el servicio de quitar fondo.") from exc

    if response.status_code != 200:
        detail = ""
        try:
            detail = response.json().get("errors", [{}])[0].get("title", "")
        except Exception:
            detail = response.text[:120]
        logger.warning("Respuesta de remove.bg: %s %s", response.status_code, detail)
        raise RuntimeError(detail or "El servicio de quitar fondo devolvió un error.")

    content_type = response.headers.get("Content-Type", "image/png")
    filename = os.path.splitext(uploaded_file.name or "imagen")[0] + "-nobg.png"
    return ContentFile(response.content, name=filename), content_type


def _precio_subquery(tipo, moneda):
    return Subquery(
        Precio.objects.filter(
            variante=OuterRef("pk"),
            tipo=tipo,
            moneda=moneda,
            activo=True,
        ).order_by("-actualizado").values("precio")[:1]
    )


def _sincronizar_precios(variante: ProductoVariante, data: dict) -> None:
    # Precio venta = minorista (si no hay minorista explícito)
    precio_venta_ars = data.get("precio_venta_ars") or data.get("precio_minorista_ars")
    precio_minimo_ars = data.get("precio_minimo_ars")
    
    # Sincronizar precios: minorista y mayorista
    combinaciones = [
        (Precio.Tipo.MINORISTA, Precio.Moneda.ARS, precio_venta_ars or data.get("precio_minorista_ars")),
        (Precio.Tipo.MAYORISTA, Precio.Moneda.ARS, data.get("precio_mayorista_ars")),
    ]

    from django.db import connection
    from core.db_inspector import column_exists
    
    # Verificar qué campos existen en la tabla
    tiene_tipo_precio = column_exists("inventario_precio", "tipo_precio")
    tiene_costo = column_exists("inventario_precio", "costo")
    tiene_precio_venta_normal = column_exists("inventario_precio", "precio_venta_normal")
    tiene_precio_venta_minimo = column_exists("inventario_precio", "precio_venta_minimo")
    tiene_precio_venta_descuento = column_exists("inventario_precio", "precio_venta_descuento")

    for tipo, moneda, valor in combinaciones:
        if valor in (None, ""):
            variante.precios.filter(tipo=tipo, moneda=moneda).update(activo=False)
            continue
        
        # Verificar si existe el registro
        precio_existente = Precio.objects.filter(
            variante=variante,
            tipo=tipo,
            moneda=moneda
        ).first()
        
        if precio_existente:
            # Actualizar precio existente
            precio_existente.precio = valor
            precio_existente.activo = True
            
            # Construir UPDATE dinámicamente según los campos que existan
            update_fields = ["precio = %s", "activo = %s", "actualizado = NOW()"]
            update_values = [valor, True]
            
            if tiene_tipo_precio:
                update_fields.append("tipo_precio = %s")
                update_values.append(tipo)
            
            if tiene_costo:
                # Si hay costo en los datos, usarlo; si no, mantener el existente o usar 0
                costo_valor = data.get("costo_ars") or data.get("costo_usd") or 0
                update_fields.append("costo = %s")
                update_values.append(costo_valor)
            
            if tiene_precio_venta_normal:
                update_fields.append("precio_venta_normal = %s")
                update_values.append(valor)
            
            if tiene_precio_venta_minimo:
                precio_min = precio_minimo_ars or valor
                update_fields.append("precio_venta_minimo = %s")
                update_values.append(precio_min)
            
            update_values.append(precio_existente.pk)
            
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE inventario_precio 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """, update_values)
        else:
            # Crear nuevo precio con SQL directo, incluyendo todos los campos NOT NULL
            insert_fields = ["variante_id", "tipo", "moneda", "precio", "activo"]
            insert_values = [variante.pk, tipo, moneda, valor, True]
            
            if tiene_tipo_precio:
                insert_fields.append("tipo_precio")
                insert_values.append(tipo)
            
            if tiene_costo:
                # Obtener costo de los datos o usar 0 por defecto
                costo_valor = data.get("costo_ars") or data.get("costo_usd") or 0
                insert_fields.append("costo")
                insert_values.append(costo_valor)
            
            if tiene_precio_venta_normal:
                insert_fields.append("precio_venta_normal")
                insert_values.append(valor)
            
            if tiene_precio_venta_minimo:
                precio_min = precio_minimo_ars or valor
                insert_fields.append("precio_venta_minimo")
                insert_values.append(precio_min)
            
            if tiene_precio_venta_descuento:
                # Precio de descuento es opcional, puede ser NULL
                insert_fields.append("precio_venta_descuento")
                insert_values.append(None)
            
            # Agregar timestamps al final (usando NOW() directamente en SQL)
            insert_fields.extend(["creado", "actualizado"])
            
            # Los timestamps se agregan directamente en el SQL, no en los valores
            with connection.cursor() as cursor:
                placeholders = ", ".join(["%s"] * len(insert_values) + ["NOW()", "NOW()"])
                cursor.execute(f"""
                    INSERT INTO inventario_precio 
                    ({', '.join(insert_fields)})
                    VALUES ({placeholders})
                """, insert_values)
    
    # Precio mínimo se guarda como minorista con un flag especial o simplemente como minorista
    # Por ahora, si hay precio_minimo_ars, lo guardamos como minorista también
    if precio_minimo_ars:
        # El precio mínimo se puede usar como referencia, pero se guarda como minorista
        pass


@login_required
def inventario_dashboard(request):
    form = InventarioFiltroForm(request.GET or None)

    missing_columns = [
        f"{table}.{column}"
        for table, column in SCHEMA_REQUIREMENTS
        if not column_exists(table, column)
    ]

    detalleiphone_ready = False

    if missing_columns:
        messages.warning(
            request,
            "Faltan columnas críticas en la base de datos de Inventario. Ejecutá `python manage.py migrate` "
            "para agregar: " + ", ".join(missing_columns),
        )
        paginator = Paginator([], 1)
        context = {
            "form": form,
            "page_obj": paginator.get_page(1),
            "total": 0,
            "valor_dolar": None,
            "stats": {
                "total_variantes": 0,
                "total_activos": 0,
                "total_bajo_stock": 0,
                "unidades_totales": 0,
                "valor_total_usd": Decimal("0"),
                "valor_total_ars": None,
            },
            "detalleiphone_ready": False,
            "detalleiphone_warning": None,
            "applied_filters": [],
            "schema_missing_columns": missing_columns,
        }
        return render(request, "inventario/dashboard.html", context)

    detalleiphone_ready = is_detalleiphone_variante_ready()

    qs = ProductoVariante.objects.select_related(
        "producto",
        "producto__categoria",
        "producto__proveedor",
    )

    if detalleiphone_ready:
        qs = qs.select_related("detalle_iphone")

    # Excluir iPhones (categoría "Celulares") del inventario general
    qs = (
        qs.prefetch_related("precios")
        .filter(producto__activo=True)
        .exclude(producto__categoria__nombre__iexact="Celulares")
        .order_by("producto__nombre", "sku")
    )

    if form.is_valid():
        q = form.cleaned_data.get("q") or ""
        categoria = form.cleaned_data.get("categoria")
        proveedor = form.cleaned_data.get("proveedor")
        solo_activos = form.cleaned_data.get("solo_activos")
        bajo_stock = form.cleaned_data.get("bajo_stock")

        if q:
            qs = qs.filter(
                models.Q(producto__nombre__icontains=q)
                | models.Q(sku__icontains=q)
                | models.Q(producto__codigo_barras__icontains=q)
            )
        if categoria:
            # Incluir productos de la categoría y todas sus subcategorías
            def get_all_subcategorias_ids(cat):
                """Obtiene todos los IDs de subcategorías recursivamente."""
                ids = [cat.pk]
                for subcat in cat.subcategorias.all():
                    ids.extend(get_all_subcategorias_ids(subcat))
                return ids
            
            categoria_ids = get_all_subcategorias_ids(categoria)
            qs = qs.filter(producto__categoria_id__in=categoria_ids)
        if proveedor:
            qs = qs.filter(producto__proveedor=proveedor)
        if solo_activos:
            qs = qs.filter(activo=True)
        if bajo_stock:
            qs = qs.filter(stock_minimo__gt=0, stock_actual__lte=models.F("stock_minimo"))

    # Anotar precios (último activo por tipo y moneda)
    qs = qs.annotate(
        precio_min_usd=_precio_subquery(Precio.Tipo.MINORISTA, Precio.Moneda.USD),
        precio_may_usd=_precio_subquery(Precio.Tipo.MAYORISTA, Precio.Moneda.USD),
        precio_min_ars=_precio_subquery(Precio.Tipo.MINORISTA, Precio.Moneda.ARS),
        precio_may_ars=_precio_subquery(Precio.Tipo.MAYORISTA, Precio.Moneda.ARS),
    )

    # Normalizar tipo Decimal para evitar warnings en template
    qs = qs.annotate(
        precio_min_usd_cast=Cast("precio_min_usd", DecimalField(max_digits=12, decimal_places=2)),
        precio_may_usd_cast=Cast("precio_may_usd", DecimalField(max_digits=12, decimal_places=2)),
        precio_min_ars_cast=Cast("precio_min_ars", DecimalField(max_digits=12, decimal_places=2)),
        precio_may_ars_cast=Cast("precio_may_ars", DecimalField(max_digits=12, decimal_places=2)),
    )

    variantes = list(qs)

    valor_dolar = obtener_valor_dolar_blue()
    dolar_decimal = Decimal(str(valor_dolar)) if valor_dolar else None

    total_variantes = len(variantes)
    total_activos = sum(1 for v in variantes if v.activo)
    # Bajo stock siempre es 0, sin stock cuenta productos con stock_actual = 0
    total_bajo_stock = 0
    total_sin_stock = sum(1 for v in variantes if v.stock_actual == 0)
    unidades_totales = sum(v.stock_actual for v in variantes)

    valor_total_usd = sum(
        (v.precio_min_usd_cast or Decimal("0")) * Decimal(v.stock_actual or 0)
        for v in variantes
    )
    valor_total_ars = (
        (valor_total_usd * dolar_decimal) if dolar_decimal is not None else None
    )
    
    # Convertir valor_total_ars a USD para mostrar referencia
    valor_total_ars_en_usd = None
    if valor_dolar and valor_total_ars:
        valor_total_ars_en_usd = valor_total_ars / dolar_decimal
    
    # Calcular valor catálogo (similar a dashboard_view)
    valor_catalogo_usd = Precio.objects.filter(
        activo=True,
        tipo=Precio.Tipo.MINORISTA,
        moneda=Precio.Moneda.USD,
        variante__producto__activo=True,
    ).exclude(
        variante__producto__categoria__nombre__iexact="Celulares"
    ).aggregate(
        total=Coalesce(
            Sum(
                F("precio") * F("variante__stock_actual"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            Decimal("0"),
        )
    )["total"]

    valor_catalogo_ars = Precio.objects.filter(
        activo=True,
        tipo=Precio.Tipo.MINORISTA,
        moneda=Precio.Moneda.ARS,
        variante__producto__activo=True,
    ).exclude(
        variante__producto__categoria__nombre__iexact="Celulares"
    ).aggregate(total=Coalesce(Sum(F("precio") * F("variante__stock_actual")), Decimal("0")))["total"]
    
    # Convertir ARS a USD para mostrar referencia
    valor_catalogo_ars_en_usd = None
    if valor_dolar and valor_catalogo_ars:
        valor_catalogo_ars_en_usd = valor_catalogo_ars / dolar_decimal
    
    inventario_metrics = {
        "valor_catalogo_usd": valor_catalogo_usd,
        "valor_catalogo_ars": valor_catalogo_ars,
        "valor_catalogo_ars_en_usd": valor_catalogo_ars_en_usd,
    }

    paginator = Paginator(variantes, 20)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)

    applied_filters = []
    if request.GET:
        for key, values in request.GET.lists():
            if key in {"page", "csrfmiddlewaretoken"}:
                continue
            for value in values:
                if value:
                    applied_filters.append({"key": key, "value": value})

    detalleiphone_warning = None
    if not detalleiphone_ready:
        detalleiphone_warning = (
            "Debés ejecutar `python manage.py migrate` para terminar las migraciones"
            " pendientes del módulo Inventario."
        )

    ctx = {
        "form": form,
        "page_obj": page_obj,
        "categorias": [cat for cat in _get_categorias_jerarquicas() if cat["categoria"].nombre.lower() != "celulares"],
        "categorias_flat": Categoria.objects.exclude(nombre__iexact="Celulares").select_related("parent").order_by("parent__nombre", "nombre"),
        "total": paginator.count,
        "valor_dolar": valor_dolar,
        "inventario_metrics": inventario_metrics,
        "stats": {
            "total_variantes": total_variantes,
            "total_activos": total_activos,
            "total_bajo_stock": total_bajo_stock,
            "total_sin_stock": total_sin_stock,
            "unidades_totales": unidades_totales,
            "valor_total_usd": valor_total_usd,
            "valor_total_ars": valor_total_ars,
            "valor_total_ars_en_usd": valor_total_ars_en_usd,
        },
        "detalleiphone_ready": detalleiphone_ready,
        "detalleiphone_warning": detalleiphone_warning,
        "applied_filters": applied_filters,
        "schema_missing_columns": [],
    }
    return render(request, "inventario/dashboard.html", ctx)


@login_required
@transaction.atomic
def producto_crear(request):
    producto_form = ProductoForm(request.POST or None, request.FILES or None)
    variante_form = ProductoVarianteForm(request.POST or None)
    imagenes_nuevas = request.FILES.getlist("imagenes")
    imagenes_validas = True

    if request.method == "POST":
        if len(imagenes_nuevas) > MAX_PRODUCT_IMAGES:
            producto_form.add_error(
                "imagenes",
                f"Podés cargar hasta {MAX_PRODUCT_IMAGES} imágenes por producto.",
            )
            imagenes_validas = False

        # Debug: mostrar errores si los hay
        if not producto_form.is_valid():
            messages.error(request, f"Errores en el formulario de producto: {producto_form.errors}")
        if not variante_form.is_valid():
            messages.error(request, f"Errores en el formulario de variante: {variante_form.errors}")
        
        if producto_form.is_valid() and variante_form.is_valid() and imagenes_validas:
            # Generar SKU automático si está habilitado o si está vacío
            sku_valor = variante_form.cleaned_data.get("sku", "").strip()
            if variante_form.cleaned_data.get("sku_auto", True) or not sku_valor:
                nombre = producto_form.cleaned_data.get("nombre", "")
                attr1 = variante_form.cleaned_data.get("atributo_1", "")
                attr2 = variante_form.cleaned_data.get("atributo_2", "")
                from django.utils.text import slugify
                from uuid import uuid4
                
                # Generar SKU base
                sku_base = slugify(f"{nombre}-{attr1}-{attr2}".strip("-"))
                if not sku_base:
                    sku_base = slugify(nombre) or "PROD"
                
                # Asegurar unicidad
                sku_final = sku_base
                contador = 1
                while ProductoVariante.objects.filter(sku=sku_final).exists():
                    sku_final = f"{sku_base}-{contador}"
                    contador += 1
                
                variante_form.cleaned_data["sku"] = sku_final
                variante_form.instance.sku = sku_final
            
            # Generar código de barras para la variante si está habilitado
            if producto_form.cleaned_data.get("generar_codigo_barras") or variante_form.cleaned_data.get("generar_codigo_barras", False):
                import random
                # Generar EAN-13 (13 dígitos)
                codigo = f"{random.randint(100000000000, 999999999999)}"
                # Si la variante no tiene código de barras, usar el del producto o generar uno nuevo
                if not variante_form.instance.codigo_barras:
                    variante_form.instance.codigo_barras = codigo
                    variante_form.cleaned_data["codigo_barras"] = codigo
                # También para el producto si no tiene
                if not producto_form.instance.codigo_barras:
                    producto_form.instance.codigo_barras = codigo
                    producto_form.cleaned_data["codigo_barras"] = codigo
            
            # Generar QR code para la variante (URL del producto o SKU)
            if producto_form.cleaned_data.get("generar_qr") or variante_form.cleaned_data.get("generar_qr", False):
                from django.urls import reverse
                sku_final = variante_form.cleaned_data.get("sku") or variante_form.instance.sku
                if sku_final:
                    # URL futura del producto (puede ser la URL de la tienda o una URL personalizada)
                    qr_url = f"https://importstore.com/producto/{sku_final}"
                    variante_form.instance.qr_code = qr_url
                    variante_form.cleaned_data["qr_code"] = qr_url
            
            producto = producto_form.save()
            variante = variante_form.save(commit=False)
            variante.producto = producto
            # Asegurar que stock_actual y stock_minimo tengan valores por defecto si no se proporcionaron
            stock_actual_val = variante.stock_actual if variante.stock_actual is not None else 0
            stock_minimo_val = variante.stock_minimo if variante.stock_minimo is not None else 0
            variante.stock_actual = stock_actual_val
            variante.stock_minimo = stock_minimo_val
            
            # Verificar si existe el campo 'stock' antiguo en la base de datos
            # Si existe, debemos insertar directamente con SQL para proporcionar el valor
            from django.db import connection
            if column_exists("inventario_productovariante", "stock"):
                # Usar SQL directo para insertar con el campo stock
                with connection.cursor() as cursor:
                    # Obtener todos los campos necesarios para el INSERT
                    sku_val = variante.sku or ""
                    nombre_var_val = variante.nombre_variante or ""
                    codigo_barras_val = variante.codigo_barras or None
                    qr_code_val = variante.qr_code or None
                    atributo_1_val = variante.atributo_1 or ""
                    atributo_2_val = variante.atributo_2 or ""
                    activo_val = 1 if variante.activo else 0
                    
                    from django.utils import timezone
                    ahora = timezone.now()
                    
                    # Verificar si existen campos adicionales
                    tiene_peso = column_exists("inventario_productovariante", "peso")
                    tiene_costo = column_exists("inventario_productovariante", "costo")
                    
                    # Construir el INSERT dinámicamente según los campos que existan
                    columnas = [
                        "producto_id", "sku", "nombre_variante", "codigo_barras", "qr_code", 
                        "atributo_1", "atributo_2", "stock_actual", "stock_minimo", "stock", "activo", 
                        "creado", "actualizado"
                    ]
                    valores = [
                        producto.pk, sku_val, nombre_var_val, codigo_barras_val, qr_code_val,
                        atributo_1_val, atributo_2_val, stock_actual_val, stock_minimo_val,
                        stock_actual_val, activo_val, ahora, ahora
                    ]
                    
                    if tiene_peso:
                        columnas.insert(-3, "peso")  # Insertar antes de activo
                        valores.insert(-3, 0)  # Valor por defecto para peso
                    
                    if tiene_costo:
                        columnas.insert(-3, "costo")  # Insertar antes de activo
                        valores.insert(-3, 0)  # Valor por defecto para costo
                    
                    placeholders = ", ".join(["%s"] * len(valores))
                    cursor.execute(f"""
                        INSERT INTO inventario_productovariante 
                        ({", ".join(columnas)})
                        VALUES ({placeholders})
                    """, valores)
                    variante.pk = cursor.lastrowid
            else:
                # Si no existe el campo stock, guardar normalmente
                variante.save()
                # Si existe el campo costo en la BD pero no en el modelo, actualizarlo
                tiene_costo = column_exists("inventario_productovariante", "costo")
                if tiene_costo:
                    from django.db import connection
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE inventario_productovariante 
                            SET costo = %s 
                            WHERE id = %s AND costo IS NULL
                        """, [0, variante.pk])
            _sincronizar_precios(variante, variante_form.cleaned_data)

            if imagenes_nuevas:
                if len(imagenes_nuevas) > MAX_PRODUCT_IMAGES:
                    imagenes_nuevas = imagenes_nuevas[:MAX_PRODUCT_IMAGES]
                _guardar_imagenes_producto(producto, imagenes_nuevas)

            messages.success(request, "Producto creado correctamente")
            return redirect("inventario:dashboard")

    context = {
        "producto_form": producto_form,
        "variante_form": variante_form,
        "modo": "crear",
        "precio_fields": PRECIO_FIELDS,
        "valor_dolar": obtener_valor_dolar_blue(),
        "imagenes": [],
        "max_imagenes": MAX_PRODUCT_IMAGES,
    }
    return render(request, "inventario/producto_form.html", context)


@login_required
@transaction.atomic
def variante_editar(request, pk: int):
    variante = get_object_or_404(
        ProductoVariante.objects.select_related("producto").prefetch_related("precios"), pk=pk
    )
    producto = variante.producto

    producto_form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    variante_form = ProductoVarianteForm(request.POST or None, instance=variante)
    imagenes_nuevas = request.FILES.getlist("imagenes")
    imagenes_a_borrar = {int(x) for x in request.POST.getlist("imagenes_eliminar") if x.isdigit()}
    imagenes_validas = True

    if request.method == "POST":
        restantes = producto.imagenes.exclude(pk__in=imagenes_a_borrar).count()
        if restantes + len(imagenes_nuevas) > MAX_PRODUCT_IMAGES:
            disponible = max(0, MAX_PRODUCT_IMAGES - restantes)
            producto_form.add_error(
                "imagenes",
                f"Podés sumar {disponible} imágenes adicionales como máximo.",
            )
            imagenes_validas = False

        if producto_form.is_valid() and variante_form.is_valid() and imagenes_validas:
            # Generar SKU automático si está habilitado o si está vacío
            sku_valor = variante_form.cleaned_data.get("sku", "").strip()
            if variante_form.cleaned_data.get("sku_auto", False) or not sku_valor:
                nombre = producto_form.cleaned_data.get("nombre", "")
                attr1 = variante_form.cleaned_data.get("atributo_1", "")
                attr2 = variante_form.cleaned_data.get("atributo_2", "")
                from django.utils.text import slugify
                
                # Generar SKU base
                sku_base = slugify(f"{nombre}-{attr1}-{attr2}".strip("-"))
                if not sku_base:
                    sku_base = slugify(nombre) or "PROD"
                
                # Asegurar unicidad (excluyendo la variante actual)
                sku_final = sku_base
                contador = 1
                while ProductoVariante.objects.filter(sku=sku_final).exclude(pk=variante.pk).exists():
                    sku_final = f"{sku_base}-{contador}"
                    contador += 1
                
                variante_form.cleaned_data["sku"] = sku_final
                variante_form.instance.sku = sku_final
            
            # Generar código de barras si está habilitado
            if variante_form.cleaned_data.get("generar_codigo_barras", False):
                import random
                # Generar EAN-13 (13 dígitos)
                codigo = f"{random.randint(100000000000, 999999999999)}"
                variante_form.instance.codigo_barras = codigo
                variante_form.cleaned_data["codigo_barras"] = codigo
            
            # Generar QR code si está habilitado
            if variante_form.cleaned_data.get("generar_qr", False):
                sku_final = variante_form.cleaned_data.get("sku") or variante_form.instance.sku
                if sku_final:
                    qr_url = f"https://importstore.com/producto/{sku_final}"
                    variante_form.instance.qr_code = qr_url
                    variante_form.cleaned_data["qr_code"] = qr_url
            
            producto_form.save()
            
            # Guardar variante
            variante = variante_form.save()
            
            # Si existe el campo costo en la BD pero no en el modelo, actualizarlo después de guardar
            from core.db_inspector import column_exists
            tiene_costo = column_exists("inventario_productovariante", "costo")
            if tiene_costo:
                from django.db import connection
                with connection.cursor() as cursor:
                    # Verificar si el costo es NULL y actualizarlo a 0
                    cursor.execute("""
                        UPDATE inventario_productovariante 
                        SET costo = %s 
                        WHERE id = %s AND (costo IS NULL OR costo = 0)
                    """, [0, variante.pk])
            
            _sincronizar_precios(variante, variante_form.cleaned_data)

            if imagenes_a_borrar:
                ProductoImagen.objects.filter(producto=producto, pk__in=imagenes_a_borrar).delete()
                _reordenar_imagenes(producto)

            if imagenes_nuevas:
                disponibles = MAX_PRODUCT_IMAGES - producto.imagenes.count()
                if disponibles > 0:
                    _guardar_imagenes_producto(producto, imagenes_nuevas[:disponibles])
                    _reordenar_imagenes(producto)

            messages.success(request, "Variante actualizada correctamente")
            return redirect("inventario:dashboard")
    else:
        variante_form.inicializar_precios(variante)

    context = {
        "producto_form": producto_form,
        "variante_form": variante_form,
        "producto": producto,
        "variante": variante,
        "modo": "editar",
        "precio_fields": PRECIO_FIELDS,
        "imagenes": producto.imagenes.order_by("orden", "id"),
        "max_imagenes": MAX_PRODUCT_IMAGES,
    }
    return render(request, "inventario/variante_form.html", context)


@login_required
def inventario_importar(request):
    form = ImportacionInventarioForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        archivo = form.cleaned_data["archivo"]
        actualizar = form.cleaned_data["actualizar_existentes"]
        try:
            resultado = importar_catalogo_desde_archivo(archivo, actualizar)
            resumen = resultado
            if resultado.creados:
                messages.success(request, f"Se crearon {resultado.creados} variantes nuevas.")
            if resultado.actualizados:
                messages.info(request, f"Se actualizaron {resultado.actualizados} variantes existentes.")
            if resultado.errores:
                for error in resultado.errores:
                    messages.warning(request, error)
            return redirect("inventario:dashboard")
        except Exception as exc:  # pragma: no cover - feedback al usuario
            messages.error(request, f"No se pudo procesar el archivo: {exc}")

    return render(request, "inventario/importar.html", {"form": form})


@login_required
def inventario_exportar(request):
    formato = request.GET.get("formato", "excel")
    categoria_id = request.GET.get("categoria_id")
    template = request.GET.get("template", "false").lower() == "true"
    
    # Si es template, generar Excel vacío
    if template:
        buffer = generar_excel_vacio()
        respuesta = HttpResponse(buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        respuesta["Content-Disposition"] = "attachment; filename=plantilla_productos.xlsx"
        return respuesta
    
    # Convertir categoria_id a int si existe
    categoria_id_int = None
    if categoria_id:
        try:
            categoria_id_int = int(categoria_id)
        except (ValueError, TypeError):
            categoria_id_int = None
    
    if formato == "excel":
        buffer = exportar_catalogo_a_excel(categoria_id=categoria_id_int)
        respuesta = HttpResponse(buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        nombre_archivo = "inventario_exportado.xlsx"
        if categoria_id_int:
            from .models import Categoria
            try:
                categoria = Categoria.objects.get(pk=categoria_id_int)
                nombre_archivo = f"inventario_{categoria.nombre.lower().replace(' ', '_')}.xlsx"
            except Categoria.DoesNotExist:
                pass
        respuesta["Content-Disposition"] = f"attachment; filename={nombre_archivo}"
    else:
        buffer = exportar_catalogo_a_csv(categoria_id=categoria_id_int)
        respuesta = HttpResponse(buffer.getvalue(), content_type="text/csv")
        nombre_archivo = "inventario_exportado.csv"
        if categoria_id_int:
            from .models import Categoria
            try:
                categoria = Categoria.objects.get(pk=categoria_id_int)
                nombre_archivo = f"inventario_{categoria.nombre.lower().replace(' ', '_')}.csv"
            except Categoria.DoesNotExist:
                pass
        respuesta["Content-Disposition"] = f"attachment; filename={nombre_archivo}"
    return respuesta


def _get_categorias_jerarquicas():
    """Retorna las categorías organizadas en jerarquía para mostrar en templates."""
    def _build_tree(categoria):
        """Construye el árbol de categorías recursivamente."""
        tree = {
            "categoria": categoria,
            "subcategorias": []
        }
        for subcat in categoria.subcategorias.all().order_by("nombre"):
            tree["subcategorias"].append(_build_tree(subcat))
        return tree
    
    categorias_principales = Categoria.objects.filter(parent__isnull=True).order_by("nombre")
    return [_build_tree(cat) for cat in categorias_principales]


def _maestros_context(categoria_form=None, proveedor_form=None):
    return {
        "categoria_form": categoria_form or CategoriaForm(prefix="categoria"),
        "proveedor_form": proveedor_form or ProveedorForm(prefix="proveedor"),
        "categorias": _get_categorias_jerarquicas(),
        "categorias_flat": Categoria.objects.select_related("parent").order_by("parent__nombre", "nombre"),
        "proveedores": Proveedor.objects.order_by("nombre"),
    }


@login_required
def maestros(request):
    categoria_form = CategoriaForm(prefix="categoria")
    proveedor_form = ProveedorForm(prefix="proveedor")

    if request.method == "POST":
        form_tipo = request.POST.get("form_tipo")
        if form_tipo == "categoria":
            categoria_id = request.POST.get("categoria_id")
            if categoria_id:  # Editar categoría existente
                categoria = get_object_or_404(Categoria, pk=categoria_id)
                categoria_form = CategoriaForm(request.POST, instance=categoria, prefix="categoria")
                accion = "actualizada"
            else:  # Crear nueva categoría
                categoria_form = CategoriaForm(request.POST, prefix="categoria")
                accion = "creada"
            
            if categoria_form.is_valid():
                categoria = categoria_form.save()
                if request.headers.get("HX-Request"):
                    contexto = _maestros_context()
                    response = render(request, "inventario/maestros/_panel.html", contexto)
                    response["HX-Trigger"] = json.dumps(
                        {
                            "showToast": {
                                "message": f"Categoría {categoria.nombre} {accion} correctamente.",
                                "level": "success",
                            }
                        }
                    )
                    return response
                messages.success(request, f"Categoría {categoria.nombre} {accion} correctamente.")
                return redirect("inventario:maestros")
        elif form_tipo == "proveedor":
            proveedor_form = ProveedorForm(request.POST, prefix="proveedor")
            if proveedor_form.is_valid():
                proveedor = proveedor_form.save()
                if request.headers.get("HX-Request"):
                    contexto = _maestros_context()
                    response = render(request, "inventario/maestros/_panel.html", contexto)
                    response["HX-Trigger"] = json.dumps(
                        {
                            "showToast": {
                                "message": f"Proveedor {proveedor.nombre} agregado correctamente.",
                                "level": "success",
                            }
                        }
                    )
                    return response
                messages.success(request, f"Proveedor {proveedor.nombre} agregado correctamente.")
                return redirect("inventario:maestros")

        if request.headers.get("HX-Request"):
            contexto = _maestros_context(categoria_form=categoria_form, proveedor_form=proveedor_form)
            return render(request, "inventario/maestros/_panel.html", contexto)

    contexto = _maestros_context(categoria_form=categoria_form, proveedor_form=proveedor_form)
    template = "inventario/maestros/_panel.html" if request.headers.get("HX-Request") else "inventario/maestros/panel.html"
    return render(request, template, contexto)


@require_POST
@login_required
def variante_toggle_activo(request, pk: int):
    """Toggle del estado activo de una variante de producto."""
    variante = get_object_or_404(ProductoVariante, pk=pk)
    variante.activo = not variante.activo
    variante.save()
    
    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.CAMBIO_ESTADO,
        descripcion=f"Estado {('activo' if variante.activo else 'inactivo')} → {variante.producto.nombre} ({variante.atributos_display})",
    )
    
    messages.success(request, f"Variante {('activada' if variante.activo else 'desactivada')} correctamente.")
    return redirect("inventario:dashboard")


@require_POST
@login_required
def proveedor_toggle_activo(request, pk: int):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.activo = not proveedor.activo
    proveedor.save(update_fields=["activo"])

    if request.headers.get("HX-Request"):
        contexto = _maestros_context()
        response = render(request, "inventario/maestros/_panel.html", contexto)
        response["HX-Trigger"] = json.dumps(
            {
                "showToast": {
                    "message": f"Proveedor {proveedor.nombre} ahora está {'activo' if proveedor.activo else 'inactivo'}.",
                    "level": "info",
                }
            }
        )
        return response

    messages.info(
        request,
        f"Proveedor {proveedor.nombre} ahora está {'activo' if proveedor.activo else 'inactivo'}.",
    )
    return redirect("inventario:maestros")


@login_required
def descargar_etiqueta(request, variante_id):
    """Descarga una etiqueta individual en PDF."""
    from .etiquetas import generar_etiqueta_individual_pdf
    
    variante = get_object_or_404(ProductoVariante.objects.select_related('producto').prefetch_related('precios'), pk=variante_id)
    pdf_buffer = generar_etiqueta_individual_pdf(variante)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="etiqueta_{variante.sku}.pdf"'
    return response


@login_required
def descargar_etiquetas_multiples(request):
    """Descarga etiquetas de múltiples productos seleccionados."""
    from .etiquetas import generar_etiqueta_pdf
    
    variante_ids = request.GET.getlist('variantes')
    if not variante_ids:
        messages.error(request, "No se seleccionaron productos.")
        return redirect("inventario:dashboard")
    
    variantes = ProductoVariante.objects.filter(pk__in=variante_ids).select_related('producto').prefetch_related('precios')
    pdf_file = generar_etiqueta_pdf(list(variantes))
    
    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiquetas_productos.pdf"'
    return response


@login_required
def descargar_etiquetas_categoria(request, categoria_id):
    """Descarga etiquetas de todos los productos de una categoría."""
    from .etiquetas import generar_etiqueta_pdf
    
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    
    # Obtener todas las subcategorías recursivamente
    def get_all_subcategorias_ids(cat):
        """Obtiene todos los IDs de subcategorías recursivamente."""
        ids = [cat.pk]
        for subcat in cat.subcategorias.all():
            ids.extend(get_all_subcategorias_ids(subcat))
        return ids
    
    # Obtener IDs de la categoría y todas sus subcategorías
    categoria_ids = get_all_subcategorias_ids(categoria)
    
    variantes = ProductoVariante.objects.filter(
        producto__categoria_id__in=categoria_ids,
        producto__activo=True
    ).exclude(
        producto__categoria__nombre__iexact="Celulares"
    ).select_related('producto').prefetch_related('precios').order_by('producto__nombre', 'sku')
    
    if not variantes.exists():
        messages.error(request, f"No hay productos activos en la categoría {categoria.nombre}.")
        return redirect("inventario:dashboard")
    
    pdf_file = generar_etiqueta_pdf(list(variantes))
    
    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="etiquetas_{categoria.nombre}.pdf"'
    return response


@login_required
def remove_background_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    imagen = request.FILES.get("imagen")
    if not imagen:
        return JsonResponse({"error": "No se recibió ninguna imagen."}, status=400)

    try:
        procesada, content_type = _procesar_remove_bg(imagen)
    except RuntimeError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    procesada.seek(0)
    encoded = base64.b64encode(procesada.read()).decode("ascii")
    return JsonResponse({"image": encoded, "content_type": content_type})


@login_required
@require_POST
def categoria_eliminar(request, pk):
    """Elimina una categoría si no tiene productos asociados."""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    # Verificar que no tenga productos asociados
    if categoria.productos.exists():
        if request.headers.get("HX-Request"):
            return JsonResponse({
                "error": f"No se puede eliminar '{categoria.nombre}' porque tiene productos asociados."
            }, status=400)
        messages.error(request, f"No se puede eliminar '{categoria.nombre}' porque tiene productos asociados.")
        return redirect("inventario:maestros")
    
    # Verificar que no tenga subcategorías
    if categoria.subcategorias.exists():
        if request.headers.get("HX-Request"):
            return JsonResponse({
                "error": f"No se puede eliminar '{categoria.nombre}' porque tiene subcategorías."
            }, status=400)
        messages.error(request, f"No se puede eliminar '{categoria.nombre}' porque tiene subcategorías.")
        return redirect("inventario:maestros")
    
    nombre = categoria.nombre
    categoria.delete()
    
    if request.headers.get("HX-Request"):
        contexto = _maestros_context()
        response = render(request, "inventario/maestros/_panel.html", contexto)
        response["HX-Trigger"] = json.dumps(
            {
                "showToast": {
                    "message": f"Categoría {nombre} eliminada correctamente.",
                    "level": "success",
                }
            }
        )
        return response
    
    messages.success(request, f"Categoría {nombre} eliminada correctamente.")
    return redirect("inventario:maestros")


@csrf_exempt
@login_required
def generar_descripcion_ia_api(request):
    """API para generar descripción de producto usando IA."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body or "{}")
        producto_id = data.get("producto_id")
        
        if not producto_id:
            return JsonResponse({"error": "producto_id es requerido"}, status=400)
        
        producto = get_object_or_404(Producto, pk=producto_id)
        
        # Construir prompt para la IA
        categoria_nombre = producto.categoria.nombre if producto.categoria else "producto"
        atributos = []
        if hasattr(producto, 'variantes'):
            variante = producto.variantes.first()
            if variante:
                if variante.atributo_1:
                    atributos.append(f"Atributo 1: {variante.atributo_1}")
                if variante.atributo_2:
                    atributos.append(f"Atributo 2: {variante.atributo_2}")
        
        atributos_texto = "\n".join(atributos) if atributos else "Sin atributos específicos"
        
        prompt = f"""Eres un asistente de IA especializado en crear descripciones de productos para una tienda de tecnología y accesorios.

Información del producto:
- Nombre: {producto.nombre}
- Categoría: {categoria_nombre}
- Atributos: {atributos_texto}

Crea una descripción profesional, atractiva y concisa (máximo 200 palabras) para este producto. La descripción debe:
1. Ser clara y fácil de entender
2. Destacar las características principales
3. Ser atractiva para potenciales compradores
4. Estar en español argentino
5. No incluir precios ni información de stock

Descripción:"""
        
        try:
            response = _invoke_gemini(prompt)
            descripcion = response.text.strip()
            
            # Limpiar la descripción (remover posibles prefijos como "Descripción:" o similares)
            if descripcion.lower().startswith("descripción:"):
                descripcion = descripcion[12:].strip()
            
            return JsonResponse({
                "success": True,
                "descripcion": descripcion
            })
        except Exception as e:
            logger.error(f"Error generando descripción con IA: {e}")
            return JsonResponse({
                "error": f"Error al generar descripción: {str(e)}"
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Exception as e:
        logger.error(f"Error en generar_descripcion_ia_api: {e}")
        return JsonResponse({"error": str(e)}, status=500)
