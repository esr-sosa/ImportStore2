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


def _generar_sku_unico(nombre: str, attr1: str = "", attr2: str = "", sku_base: str = None) -> str:
    """
    Genera un SKU único basado en el nombre y atributos del producto.
    Si el SKU base ya existe, agrega un contador incremental.
    """
    from django.utils.text import slugify
    
    if sku_base:
        sku_base = sku_base.strip().upper()
    else:
        # Generar SKU base desde nombre y atributos
        sku_base = slugify(f"{nombre}-{attr1}-{attr2}".strip("-")).upper()
        if not sku_base:
            sku_base = slugify(nombre).upper() or "PROD"
    
    # Verificar unicidad
    sku_final = sku_base
    if ProductoVariante.objects.filter(sku=sku_final).exists():
        # Buscar el siguiente número disponible de forma más eficiente
        # Primero intentar con números bajos
        contador = 1
        max_intentos = 1000  # Límite de seguridad
        while contador < max_intentos:
            sku_final = f"{sku_base}-{contador}"
            if not ProductoVariante.objects.filter(sku=sku_final).exists():
                break
            contador += 1
        else:
            # Si llegamos al límite, usar UUID como fallback
            from uuid import uuid4
            sku_final = f"{sku_base}-{str(uuid4())[:8].upper()}"
    
    return sku_final


def _sincronizar_precios(variante: ProductoVariante, data: dict) -> None:
    """
    Sincroniza los precios de una variante con los datos proporcionados.
    Maneja correctamente todos los campos obligatorios de la tabla inventario_precio.
    """
    # Precio venta = minorista (si no hay minorista explícito)
    precio_venta_ars = data.get("precio_venta_ars") or data.get("precio_minorista_ars")
    precio_minimo_ars = data.get("precio_minimo_ars")
    precio_mayorista_ars = data.get("precio_mayorista_ars")
    
    # Validar que el valor sea un Decimal válido
    def _validar_precio(valor):
        if valor in (None, "", "None"):
            return None
        try:
            return Decimal(str(valor))
        except (ValueError, TypeError):
            logger.warning(f"Precio inválido: {valor}")
            return None
    
    # Sincronizar precios: minorista y mayorista
    combinaciones = [
        (Precio.Tipo.MINORISTA, Precio.Moneda.ARS, _validar_precio(precio_venta_ars or data.get("precio_minorista_ars"))),
        (Precio.Tipo.MAYORISTA, Precio.Moneda.ARS, _validar_precio(precio_mayorista_ars)),
    ]

    from django.db import connection
    from core.db_inspector import column_exists
    
    # Verificar qué campos existen en la tabla (cachear para evitar múltiples consultas)
    tiene_tipo_precio = column_exists("inventario_precio", "tipo_precio")
    tiene_costo = column_exists("inventario_precio", "costo")
    tiene_precio_venta_normal = column_exists("inventario_precio", "precio_venta_normal")
    tiene_precio_venta_minimo = column_exists("inventario_precio", "precio_venta_minimo")
    tiene_precio_venta_descuento = column_exists("inventario_precio", "precio_venta_descuento")

    for tipo, moneda, valor in combinaciones:
        # Si no hay valor, desactivar precios existentes
        if valor is None:
            variante.precios.filter(tipo=tipo, moneda=moneda).update(activo=False)
            continue
        
        # Validar que el valor sea positivo
        if valor < 0:
            logger.warning(f"Precio negativo ignorado: {valor} para {variante.sku} - {tipo} {moneda}")
            continue
        
        # Verificar si existe el registro
        precio_existente = Precio.objects.filter(
            variante=variante,
            tipo=tipo,
            moneda=moneda
        ).first()
        
        # Obtener costo de los datos
        costo_valor = _validar_precio(data.get("costo_ars") or data.get("costo_usd")) or Decimal("0.00")
        precio_min = _validar_precio(precio_minimo_ars) or valor
        
        if precio_existente:
            # Actualizar precio existente
            try:
                # Construir UPDATE dinámicamente según los campos que existan
                update_fields = ["precio = %s", "activo = %s", "actualizado = NOW()"]
                update_values = [valor, True]
                
                if tiene_tipo_precio:
                    update_fields.append("tipo_precio = %s")
                    update_values.append(tipo)
                
                if tiene_costo:
                    update_fields.append("costo = %s")
                    update_values.append(costo_valor)
                
                if tiene_precio_venta_normal:
                    update_fields.append("precio_venta_normal = %s")
                    update_values.append(valor)
                
                if tiene_precio_venta_minimo:
                    update_fields.append("precio_venta_minimo = %s")
                    update_values.append(precio_min)
                
                update_values.append(precio_existente.pk)
                
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        UPDATE inventario_precio 
                        SET {', '.join(update_fields)}
                        WHERE id = %s
                    """, update_values)
            except Exception as e:
                logger.error(f"Error al actualizar precio: {e}")
                raise
        else:
            # Crear nuevo precio con SQL directo, incluyendo todos los campos NOT NULL
            try:
                insert_fields = ["variante_id", "tipo", "moneda", "precio", "activo"]
                insert_values = [variante.pk, tipo, moneda, valor, True]
                
                if tiene_tipo_precio:
                    insert_fields.append("tipo_precio")
                    insert_values.append(tipo)
                
                if tiene_costo:
                    insert_fields.append("costo")
                    insert_values.append(costo_valor)
                
                if tiene_precio_venta_normal:
                    insert_fields.append("precio_venta_normal")
                    insert_values.append(valor)
                
                if tiene_precio_venta_minimo:
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
            except Exception as e:
                logger.error(f"Error al crear precio: {e}")
                raise


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
            # Validar SKU antes de continuar
            sku_valor = variante_form.cleaned_data.get("sku", "").strip()
            
            # Generar SKU automático si está habilitado o si está vacío
            if variante_form.cleaned_data.get("sku_auto", True) or not sku_valor:
                nombre = producto_form.cleaned_data.get("nombre", "")
                attr1 = variante_form.cleaned_data.get("atributo_1", "")
                attr2 = variante_form.cleaned_data.get("atributo_2", "")
                
                sku_final = _generar_sku_unico(nombre, attr1, attr2)
                variante_form.cleaned_data["sku"] = sku_final
                variante_form.instance.sku = sku_final
            else:
                # Validar que el SKU manual no esté duplicado
                sku_final = sku_valor.upper()
                if ProductoVariante.objects.filter(sku=sku_final).exclude(pk=variante_form.instance.pk if variante_form.instance.pk else None).exists():
                    variante_form.add_error("sku", "Este SKU ya existe. Por favor, elegí otro o activá la generación automática.")
                    imagenes_validas = False
                else:
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
            
            try:
                producto = producto_form.save()
                variante = variante_form.save(commit=False)
                variante.producto = producto
                
                # Validar y asegurar que stock_actual y stock_minimo tengan valores por defecto
                stock_actual_val = variante.stock_actual if variante.stock_actual is not None else 0
                stock_minimo_val = variante.stock_minimo if variante.stock_minimo is not None else 0
                
                # Validar que los valores de stock sean no negativos
                if stock_actual_val < 0:
                    variante_form.add_error("stock_actual", "El stock no puede ser negativo.")
                    imagenes_validas = False
                if stock_minimo_val < 0:
                    variante_form.add_error("stock_minimo", "El stock mínimo no puede ser negativo.")
                    imagenes_validas = False
                
                if not imagenes_validas:
                    # Si hay errores, no continuar
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
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                UPDATE inventario_productovariante 
                                SET costo = %s 
                                WHERE id = %s AND costo IS NULL
                            """, [0, variante.pk])
                
                # Sincronizar precios
                _sincronizar_precios(variante, variante_form.cleaned_data)

                # Guardar imágenes
                if imagenes_nuevas:
                    if len(imagenes_nuevas) > MAX_PRODUCT_IMAGES:
                        imagenes_nuevas = imagenes_nuevas[:MAX_PRODUCT_IMAGES]
                    _guardar_imagenes_producto(producto, imagenes_nuevas)

                messages.success(request, f"Producto '{producto.nombre}' creado correctamente con SKU: {variante.sku}")
                return redirect("inventario:dashboard")
            except Exception as e:
                logger.error(f"Error al crear producto: {e}", exc_info=True)
                messages.error(request, f"Error al crear el producto: {str(e)}")
                # No hacer redirect para que el usuario pueda ver los errores

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
            # Validar SKU antes de continuar
            sku_valor = variante_form.cleaned_data.get("sku", "").strip()
            
            # Generar SKU automático si está habilitado o si está vacío
            if variante_form.cleaned_data.get("sku_auto", False) or not sku_valor:
                nombre = producto_form.cleaned_data.get("nombre", "")
                attr1 = variante_form.cleaned_data.get("atributo_1", "")
                attr2 = variante_form.cleaned_data.get("atributo_2", "")
                
                sku_final = _generar_sku_unico(nombre, attr1, attr2, sku_base=variante.sku if variante.sku else None)
                variante_form.cleaned_data["sku"] = sku_final
                variante_form.instance.sku = sku_final
            else:
                # Validar que el SKU manual no esté duplicado (excluyendo la variante actual)
                sku_final = sku_valor.upper()
                if ProductoVariante.objects.filter(sku=sku_final).exclude(pk=variante.pk).exists():
                    variante_form.add_error("sku", "Este SKU ya existe. Por favor, elegí otro o activá la generación automática.")
                    imagenes_validas = False
                else:
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
            
            try:
                producto_form.save()
                
                # Validar stock antes de guardar
                stock_actual_val = variante_form.instance.stock_actual if variante_form.instance.stock_actual is not None else 0
                stock_minimo_val = variante_form.instance.stock_minimo if variante_form.instance.stock_minimo is not None else 0
                
                if stock_actual_val < 0:
                    variante_form.add_error("stock_actual", "El stock no puede ser negativo.")
                    imagenes_validas = False
                if stock_minimo_val < 0:
                    variante_form.add_error("stock_minimo", "El stock mínimo no puede ser negativo.")
                    imagenes_validas = False
                
                if not imagenes_validas:
                    # Si hay errores, no continuar
                    context = {
                        "producto_form": producto_form,
                        "variante_form": variante_form,
                        "modo": "editar",
                        "precio_fields": PRECIO_FIELDS,
                        "valor_dolar": obtener_valor_dolar_blue(),
                        "imagenes": producto.imagenes.all(),
                        "max_imagenes": MAX_PRODUCT_IMAGES,
                    }
                    return render(request, "inventario/producto_form.html", context)
                
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

                messages.success(request, f"Producto '{producto.nombre}' actualizado correctamente")
                return redirect("inventario:dashboard")
            except Exception as e:
                logger.error(f"Error al actualizar producto: {e}", exc_info=True)
                messages.error(request, f"Error al actualizar el producto: {str(e)}")
                # No hacer redirect para que el usuario pueda ver los errores
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


@login_required
def generar_descripcion_ia_api(request):
    """
    API para generar descripción de producto usando IA con Gemini Vision.
    Analiza las imágenes del producto junto con nombre y atributos para crear una descripción profesional.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        import base64
        from PIL import Image
        import io
        import google.generativeai as genai
        from django.conf import settings
        
        # Verificar y configurar API key de Gemini
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not api_key:
            logger.error("GEMINI_API_KEY no está configurada en settings")
            return JsonResponse({
                "error": "La API key de Gemini no está configurada. Por favor, configurá GEMINI_API_KEY en las variables de entorno."
            }, status=500)
        
        # Configurar Gemini (debe hacerse antes de crear el modelo)
        genai.configure(api_key=api_key)
        
        data = json.loads(request.body or "{}")
        producto_id = data.get("producto_id")
        imagenes_base64 = data.get("imagenes", [])  # Imágenes en base64 desde el frontend
        nombre_producto = data.get("nombre", "")  # Nombre desde el formulario (modo creación)
        categoria_nombre = data.get("categoria", "")  # Categoría desde el formulario
        atributo_1 = data.get("atributo_1", "")
        atributo_2 = data.get("atributo_2", "")
        
        # Si hay producto_id, obtener datos de la BD
        if producto_id:
            producto = get_object_or_404(Producto.objects.prefetch_related("imagenes", "variantes"), pk=producto_id)
            nombre_producto = producto.nombre
            categoria_nombre = producto.categoria.nombre if producto.categoria else "producto"
            atributos = []
            variante = producto.variantes.first() if hasattr(producto, 'variantes') else None
            if variante:
                if variante.atributo_1:
                    atributos.append(variante.atributo_1)
                if variante.atributo_2:
                    atributos.append(variante.atributo_2)
            atributos_texto = " · ".join(atributos) if atributos else "Sin atributos específicos"
        else:
            # Modo creación: usar datos del formulario
            if not nombre_producto:
                return JsonResponse({"error": "El nombre del producto es requerido"}, status=400)
            atributos = []
            if atributo_1:
                atributos.append(atributo_1)
            if atributo_2:
                atributos.append(atributo_2)
            atributos_texto = " · ".join(atributos) if atributos else "Sin atributos específicos"
            producto = None  # No hay producto aún
        
        # Recopilar imágenes: primero las nuevas (base64), luego las existentes del producto
        imagenes_para_ia = []
        
        # Procesar imágenes nuevas desde el frontend (base64)
        for img_base64 in imagenes_base64[:3]:  # Máximo 3 imágenes para no exceder límites
            try:
                # Remover el prefijo data:image/...;base64, si existe
                if ',' in img_base64:
                    img_base64 = img_base64.split(',')[1]
                img_data = base64.b64decode(img_base64)
                img = Image.open(io.BytesIO(img_data))
                imagenes_para_ia.append(img)
            except Exception as e:
                logger.warning(f"Error procesando imagen base64: {e}")
                continue
        
        # Si no hay imágenes nuevas, usar las existentes del producto (solo si existe)
        if not imagenes_para_ia and producto and producto.imagenes.exists():
            for imagen_obj in producto.imagenes.all()[:3]:  # Máximo 3 imágenes
                try:
                    if imagen_obj.imagen:
                        img_path = imagen_obj.imagen.path
                        img = Image.open(img_path)
                        imagenes_para_ia.append(img)
                except Exception as e:
                    logger.warning(f"Error cargando imagen {imagen_obj.pk}: {e}")
                    continue
        
        # Construir prompt profesional de marketing
        prompt = f"""Eres un experto en marketing y copywriting especializado en productos de tecnología y accesorios.

INFORMACIÓN DEL PRODUCTO:
- Nombre: {nombre_producto}
- Categoría: {categoria_nombre if categoria_nombre else "Sin categoría específica"}
- Atributos/Variantes: {atributos_texto}

TAREA:
Crea una descripción profesional y atractiva para este producto. La descripción debe:

1. **Ser persuasiva y orientada a la venta**: Destacá los beneficios y características que más importan al cliente
2. **Usar lenguaje claro y profesional**: Evitá tecnicismos innecesarios, pero mostrá expertise
3. **Tener entre 150-250 palabras**: Suficiente para informar sin aburrir
4. **Estar en español argentino**: Usá expresiones naturales del mercado local
5. **Estructura sugerida**:
   - Apertura impactante (1-2 líneas)
   - Características principales (3-4 puntos destacados)
   - Beneficios para el usuario
   - Mencionar garantía y servicio post venta
   - Cierre que invite a la acción

6. **REGLAS CRÍTICAS**:
   - **NUNCA uses la palabra "original"** ni menciones si es original o no. Algunos productos son AAA o réplicas, así que evitá cualquier referencia a originalidad.
   - **SIEMPRE incluye información sobre la garantía** del producto. Mencioná que incluye garantía y nuestro servicio post venta profesional.
   - **NO incluir**: Precios, stock
   - **SÍ incluir**: Características técnicas relevantes, beneficios, casos de uso, garantía y servicio post venta

7. **Sobre garantía y post venta**: Siempre mencioná que el producto incluye garantía y que contamos con un servicio post venta profesional para asistir al cliente. Usá frases como "Incluye garantía" o "Con garantía y servicio post venta" o "Garantía incluida con nuestro servicio de post venta profesional".

Si hay imágenes, analizalas para describir el diseño, calidad visual, y características que se vean.

Generá SOLO la descripción, sin títulos ni prefijos como "Descripción:"."""

        # Intentar con diferentes modelos disponibles en la API
        # Usar modelos Gemini 2.0/2.5 que son los disponibles actualmente
        # Orden de preferencia: modelos más recientes primero
        model_candidates = []
        if imagenes_para_ia:
            # Si hay imágenes, priorizar modelos con visión (todos los Gemini 2.x soportan visión)
            model_candidates = [
                "gemini-2.5-flash",      # Modelo más reciente y rápido
                "gemini-2.0-flash",      # Fallback estable
                "gemini-2.5-pro",        # Modelo más potente si está disponible
                "gemini-flash-latest",   # Alias al último flash
                "gemini-pro-latest"      # Alias al último pro
            ]
        else:
            # Solo texto, cualquier modelo sirve
            model_candidates = [
                "gemini-2.5-flash",      # Modelo más reciente y rápido
                "gemini-2.0-flash",      # Fallback estable
                "gemini-2.5-pro",        # Modelo más potente
                "gemini-flash-latest",   # Alias al último flash
                "gemini-pro-latest"      # Alias al último pro
            ]
        
        # Intentar con cada modelo hasta que uno funcione
        model = None
        response = None
        last_error = None
        
        for model_name in model_candidates:
            try:
                model = genai.GenerativeModel(model_name)
                
                # Si hay imágenes, enviarlas junto con el prompt
                if imagenes_para_ia:
                    content_parts = [prompt]
                    for img in imagenes_para_ia:
                        content_parts.append(img)
                    response = model.generate_content(content_parts)
                else:
                    # Sin imágenes, solo texto
                    response = model.generate_content(prompt)
                
                # Si llegamos aquí, el modelo funcionó
                logger.info(f"Modelo Gemini '{model_name}' funcionó correctamente")
                break
            except Exception as e:
                last_error = e
                error_msg = str(e)
                # Si es un error 404 o "not found", intentar con el siguiente modelo
                if "404" in error_msg or "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                    logger.warning(f"Modelo Gemini '{model_name}' no disponible ({error_msg}). Intentando siguiente...")
                    continue
                # Si es otro tipo de error, lanzarlo
                raise
        
        if not model or not response:
            # Si ningún modelo funcionó, intentar listar modelos disponibles
            try:
                available_models = genai.list_models()
                model_names = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
                logger.error(f"Modelos disponibles: {model_names}")
                raise Exception(
                    f"Ningún modelo de Gemini está disponible. "
                    f"Modelos probados: {model_candidates}. "
                    f"Modelos disponibles en tu API: {model_names if model_names else 'ninguno detectado'}. "
                    f"Último error: {last_error}"
                )
            except Exception as list_error:
                raise Exception(
                    f"Ningún modelo de Gemini está disponible. "
                    f"Modelos probados: {model_candidates}. "
                    f"Último error: {last_error}. "
                    f"Error al listar modelos: {list_error}"
                )
        
        descripcion = response.text.strip()
        
        # Limpiar la descripción (remover posibles prefijos)
        prefixes_to_remove = ["descripción:", "descripcion:", "descripción", "descripcion"]
        for prefix in prefixes_to_remove:
            if descripcion.lower().startswith(prefix):
                descripcion = descripcion[len(prefix):].strip()
                if descripcion.startswith(":"):
                    descripcion = descripcion[1:].strip()
        
        return JsonResponse({
            "success": True,
            "descripcion": descripcion,
            "imagenes_usadas": len(imagenes_para_ia)
        })
    except Exception as e:
        logger.error(f"Error generando descripción con IA: {e}", exc_info=True)
        error_msg = str(e)
        
        # Manejar errores específicos
        if "API_KEY" in error_msg or "API key" in error_msg or "No API_KEY" in error_msg:
            return JsonResponse({
                "error": "La API key de Gemini no está configurada. Por favor, configurá la variable de entorno GEMINI_API_KEY en tu archivo .env"
            }, status=500)
        elif "429" in error_msg or "quota" in error_msg.lower():
            return JsonResponse({
                "error": "Límite de consultas a la IA alcanzado. Intentá nuevamente en unos minutos."
            }, status=429)
        else:
            return JsonResponse({
                "error": f"Error al generar descripción: {error_msg}"
            }, status=500)


@login_required
@require_POST
def actualizar_stock_rapido_api(request):
    """API para actualizar stock de una variante rápidamente."""
    try:
        data = json.loads(request.body)
        variante_id = data.get('variante_id')
        nuevo_stock = data.get('stock')
        
        if variante_id is None or nuevo_stock is None:
            return JsonResponse({"error": "variante_id y stock son requeridos"}, status=400)
        
        try:
            nuevo_stock = int(nuevo_stock)
            if nuevo_stock < 0:
                return JsonResponse({"error": "El stock no puede ser negativo"}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"error": "El stock debe ser un número entero"}, status=400)
        
        variante = get_object_or_404(ProductoVariante, pk=variante_id)
        stock_anterior = variante.stock_actual or 0
        
        with transaction.atomic():
            variante.stock_actual = nuevo_stock
            variante.save()
            
            # Registrar en historial
            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.MODIFICACION,
                descripcion=f"Stock actualizado: {variante.producto.nombre} ({variante.sku}) - {stock_anterior} → {nuevo_stock}"
            )
        
        return JsonResponse({
            "success": True,
            "stock": nuevo_stock,
            "message": "Stock actualizado correctamente"
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Exception as e:
        logger.error(f"Error en actualizar_stock_rapido_api: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def actualizar_precio_rapido_api(request):
    """API para actualizar precio de una variante rápidamente."""
    try:
        data = json.loads(request.body)
        variante_id = data.get('variante_id')
        tipo = data.get('tipo')  # MINORISTA o MAYORISTA
        moneda = data.get('moneda')  # ARS o USD
        nuevo_precio = data.get('precio')
        
        if not all([variante_id, tipo, moneda, nuevo_precio is not None]):
            return JsonResponse({"error": "variante_id, tipo, moneda y precio son requeridos"}, status=400)
        
        if tipo not in [Precio.Tipo.MINORISTA, Precio.Tipo.MAYORISTA]:
            return JsonResponse({"error": "tipo debe ser MINORISTA o MAYORISTA"}, status=400)
        
        if moneda not in [Precio.Moneda.ARS, Precio.Moneda.USD]:
            return JsonResponse({"error": "moneda debe ser ARS o USD"}, status=400)
        
        try:
            nuevo_precio = Decimal(str(nuevo_precio))
            if nuevo_precio < 0:
                return JsonResponse({"error": "El precio no puede ser negativo"}, status=400)
        except (ValueError, TypeError, Exception):
            return JsonResponse({"error": "El precio debe ser un número válido"}, status=400)
        
        variante = get_object_or_404(ProductoVariante, pk=variante_id)
        
        with transaction.atomic():
            # Verificar si existe la columna tipo_precio en la base de datos
            from django.db import connection
            from core.db_inspector import column_exists
            
            tiene_tipo_precio = column_exists("inventario_precio", "tipo_precio")
            
            # Buscar precio existente
            try:
                precio = Precio.objects.get(
                    variante=variante,
                    tipo=tipo,
                    moneda=moneda
                )
                created = False
            except Precio.DoesNotExist:
                # Verificar qué campos adicionales existen en la base de datos
                tiene_costo = column_exists("inventario_precio", "costo")
                tiene_precio_venta_normal = column_exists("inventario_precio", "precio_venta_normal")
                tiene_precio_venta_minimo = column_exists("inventario_precio", "precio_venta_minimo")
                
                # Crear nuevo precio usando SQL directo para incluir todos los campos obligatorios
                if tiene_tipo_precio or tiene_costo or tiene_precio_venta_normal:
                    insert_fields = ["variante_id", "tipo", "moneda", "precio", "activo"]
                    insert_values = [variante.pk, tipo, moneda, nuevo_precio, True]
                    
                    if tiene_tipo_precio:
                        insert_fields.append("tipo_precio")
                        insert_values.append(tipo)
                    
                    if tiene_costo:
                        insert_fields.append("costo")
                        insert_values.append(0.00)  # Valor por defecto
                    
                    if tiene_precio_venta_normal:
                        insert_fields.append("precio_venta_normal")
                        insert_values.append(nuevo_precio)
                    
                    if tiene_precio_venta_minimo:
                        insert_fields.append("precio_venta_minimo")
                        insert_values.append(nuevo_precio)
                    
                    # Agregar timestamps
                    insert_fields.extend(["creado", "actualizado"])
                    
                    with connection.cursor() as cursor:
                        placeholders = ", ".join(["%s"] * len(insert_values) + ["NOW()", "NOW()"])
                        cursor.execute(f"""
                            INSERT INTO inventario_precio 
                            ({', '.join(insert_fields)})
                            VALUES ({placeholders})
                        """, insert_values)
                        precio_id = cursor.lastrowid
                        precio = Precio.objects.get(pk=precio_id)
                else:
                    # Si no existen campos adicionales, usar el ORM normal
                    precio = Precio.objects.create(
                        variante=variante,
                        tipo=tipo,
                        moneda=moneda,
                        precio=nuevo_precio,
                        activo=True
                    )
                created = True
            
            precio_anterior = precio.precio
            precio.precio = nuevo_precio
            precio.activo = True
            precio.save()
            
            # Registrar en historial
            accion = "creado" if created else "actualizado"
            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.MODIFICACION,
                descripcion=f"Precio {accion}: {variante.producto.nombre} ({variante.sku}) - {tipo} {moneda} - {precio_anterior} → {nuevo_precio}"
            )
        
        return JsonResponse({
            "success": True,
            "precio": str(nuevo_precio),
            "tipo": tipo,
            "moneda": moneda,
            "message": f"Precio {accion} correctamente"
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Exception as e:
        logger.error(f"Error en actualizar_precio_rapido_api: {e}")
        return JsonResponse({"error": str(e)}, status=500)