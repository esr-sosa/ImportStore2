from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.db.models import DecimalField, OuterRef, Subquery
from django.db.models.functions import Cast
from django.shortcuts import render

from core.utils import obtener_valor_dolar_blue

from .forms import InventarioFiltroForm
from .models import Precio, ProductoVariante
from .utils import is_detalleiphone_variante_ready


def _precio_subquery(tipo, moneda):
    return Subquery(
        Precio.objects.filter(
            variante=OuterRef("pk"),
            tipo=tipo,
            moneda=moneda,
            activo=True,
        ).order_by("-actualizado").values("precio")[:1]
    )


@login_required
def inventario_dashboard(request):
    form = InventarioFiltroForm(request.GET or None)

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
    }
    return render(request, "inventario/dashboard.html", ctx)
