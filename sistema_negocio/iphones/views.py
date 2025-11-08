from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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
        variante.precios.update_or_create(
            tipo=tipo,
            moneda=moneda,
            defaults={"precio": valor, "activo": True},
        )


@login_required
def iphone_dashboard(request):
    valor_dolar = obtener_valor_dolar_blue()

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
                },
            )
            producto.categoria = categoria
            producto.activo = data["activo"]
            producto.save()

            variante = ProductoVariante.objects.create(
                producto=producto,
                sku=data["sku"],
                atributo_1=data["capacidad"],
                atributo_2=data["color"],
                stock_actual=data["stock_actual"],
                stock_minimo=data["stock_minimo"],
                activo=data["activo"],
            )

            _sincronizar_precios(variante, data)

            detalle = DetalleIphone.objects.create(
                variante=variante,
                imei=data.get("imei"),
                salud_bateria=data.get("salud_bateria"),
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

            variante.sku = data["sku"]
            variante.atributo_1 = data["capacidad"]
            variante.atributo_2 = data["color"]
            variante.stock_actual = data["stock_actual"]
            variante.stock_minimo = data["stock_minimo"]
            variante.activo = data["activo"]
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
        form = AgregarIphoneForm(
            initial={
                "modelo": producto.nombre,
                "capacidad": variante.atributo_1,
                "color": variante.atributo_2,
                "sku": variante.sku,
                "stock_actual": variante.stock_actual,
                "stock_minimo": variante.stock_minimo,
                "activo": variante.activo,
                "costo_usd": detalle.costo_usd if detalle else None,
                "precio_venta_usd": detalle.precio_venta_usd if detalle else None,
                "precio_oferta_usd": detalle.precio_oferta_usd if detalle else None,
                "precio_venta_ars": variante.precio_activo(Precio.Tipo.MINORISTA, Precio.Moneda.ARS).precio if variante.precio_activo(Precio.Tipo.MINORISTA, Precio.Moneda.ARS) else None,
                "precio_mayorista_usd": variante.precio_activo(Precio.Tipo.MAYORISTA, Precio.Moneda.USD).precio if variante.precio_activo(Precio.Tipo.MAYORISTA, Precio.Moneda.USD) else None,
                "precio_mayorista_ars": variante.precio_activo(Precio.Tipo.MAYORISTA, Precio.Moneda.ARS).precio if variante.precio_activo(Precio.Tipo.MAYORISTA, Precio.Moneda.ARS) else None,
                "imei": detalle.imei if detalle else "",
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
def toggle_iphone_status(request, producto_id):
    if not is_detalleiphone_variante_ready():
        messages.error(
            request,
            "Aplicá `python manage.py migrate` para habilitar la gestión avanzada de iPhones.",
        )
        return redirect("inventario:dashboard")

    producto = get_object_or_404(Producto, pk=producto_id)
    producto.activo = not producto.activo
    producto.save()

    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.CAMBIO_ESTADO,
        descripcion=f"Estado {('activo' if producto.activo else 'inactivo')} → {producto.nombre}",
    )

    return redirect("iphones:dashboard")
