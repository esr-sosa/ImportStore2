from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import models, transaction
from django.db.models import DecimalField, OuterRef, Subquery
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404, redirect, render

from core.db_inspector import column_exists
from core.utils import obtener_valor_dolar_blue

from .forms import (
    ImportacionInventarioForm,
    InventarioFiltroForm,
    ProductoForm,
    ProductoVarianteForm,
)
from .models import Precio, Producto, ProductoVariante
from .utils import is_detalleiphone_variante_ready
from .importers import exportar_catalogo_a_csv, importar_catalogo_desde_archivo


SCHEMA_REQUIREMENTS = (
    ("inventario_productovariante", "sku"),
    ("inventario_productovariante", "stock_actual"),
    ("inventario_productovariante", "stock_minimo"),
    ("inventario_productovariante", "activo"),
    ("inventario_producto", "activo"),
    ("inventario_precio", "precio"),
)


PRECIO_FIELDS = (
    "precio_minorista_usd",
    "precio_minorista_ars",
    "precio_mayorista_usd",
    "precio_mayorista_ars",
)


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
    combinaciones = [
        ("precio_minorista_usd", Precio.Tipo.MINORISTA, Precio.Moneda.USD),
        ("precio_minorista_ars", Precio.Tipo.MINORISTA, Precio.Moneda.ARS),
        ("precio_mayorista_usd", Precio.Tipo.MAYORISTA, Precio.Moneda.USD),
        ("precio_mayorista_ars", Precio.Tipo.MAYORISTA, Precio.Moneda.ARS),
    ]

    for campo, tipo, moneda in combinaciones:
        valor = data.get(campo)
        if valor in (None, ""):
            variante.precios.filter(tipo=tipo, moneda=moneda).update(activo=False)
            continue
        Precio.objects.update_or_create(
            variante=variante,
            tipo=tipo,
            moneda=moneda,
            defaults={"precio": valor, "activo": True},
        )


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

    qs = (
        qs.prefetch_related("precios")
        .filter(producto__activo=True)
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
            qs = qs.filter(producto__categoria=categoria)
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
    total_bajo_stock = sum(1 for v in variantes if v.bajo_stock)
    unidades_totales = sum(v.stock_actual for v in variantes)

    valor_total_usd = sum(
        (v.precio_min_usd_cast or Decimal("0")) * Decimal(v.stock_actual or 0)
        for v in variantes
    )
    valor_total_ars = (
        (valor_total_usd * dolar_decimal) if dolar_decimal is not None else None
    )

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
        "total": paginator.count,
        "valor_dolar": valor_dolar,
        "stats": {
            "total_variantes": total_variantes,
            "total_activos": total_activos,
            "total_bajo_stock": total_bajo_stock,
            "unidades_totales": unidades_totales,
            "valor_total_usd": valor_total_usd,
            "valor_total_ars": valor_total_ars,
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
    producto_form = ProductoForm(request.POST or None)
    variante_form = ProductoVarianteForm(request.POST or None)

    if request.method == "POST":
        if producto_form.is_valid() and variante_form.is_valid():
            producto = producto_form.save()
            variante = variante_form.save(commit=False)
            variante.producto = producto
            variante.save()
            _sincronizar_precios(variante, variante_form.cleaned_data)
            messages.success(request, "Producto creado correctamente")
            return redirect("inventario:dashboard")

    context = {
        "producto_form": producto_form,
        "variante_form": variante_form,
        "modo": "crear",
        "precio_fields": PRECIO_FIELDS,
    }
    return render(request, "inventario/producto_form.html", context)


@login_required
@transaction.atomic
def variante_editar(request, pk: int):
    variante = get_object_or_404(
        ProductoVariante.objects.select_related("producto").prefetch_related("precios"), pk=pk
    )
    producto = variante.producto

    producto_form = ProductoForm(request.POST or None, instance=producto)
    variante_form = ProductoVarianteForm(request.POST or None, instance=variante)

    if request.method == "POST":
        if producto_form.is_valid() and variante_form.is_valid():
            producto_form.save()
            variante = variante_form.save()
            _sincronizar_precios(variante, variante_form.cleaned_data)
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
    buffer = exportar_catalogo_a_csv()
    respuesta = HttpResponse(buffer.getvalue(), content_type="text/csv")
    respuesta["Content-Disposition"] = "attachment; filename=inventario_exportado.csv"
    return respuesta
