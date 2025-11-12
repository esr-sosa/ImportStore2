"""Vistas principales del panel de control."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Prefetch, Sum, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from core.db_inspector import column_exists, table_exists
from core.utils import obtener_valor_dolar_blue
from configuracion.models import ConfiguracionSistema, ConfiguracionTienda
from crm.models import Cliente, Conversacion
from historial.models import RegistroHistorial
from inventario.models import Precio, Producto, ProductoVariante
from locales.models import Local
from ventas.models import Venta


@login_required
def dashboard_view(request):
    schema_warnings: list[str] = []

    inventario_ready = table_exists("inventario_productovariante") and column_exists(
        "inventario_productovariante", "stock_actual"
    )

    inventario_metrics: dict[str, object] = {}
    low_stock_variantes: list[ProductoVariante] = []
    valor_blue: float | None = None

    if inventario_ready:
        variantes_qs = (
            ProductoVariante.objects.select_related("producto", "producto__categoria", "producto__proveedor")
            .filter(producto__activo=True)
        )

        total_variantes = variantes_qs.count()
        total_activos = variantes_qs.filter(activo=True).count()
        total_bajo_stock = variantes_qs.filter(stock_minimo__gt=0, stock_actual__lte=F("stock_minimo")).count()
        unidades_totales = variantes_qs.aggregate(total=Coalesce(Sum("stock_actual"), 0))["total"]

        valor_blue = obtener_valor_dolar_blue()

        valor_catalogo_usd = Precio.objects.filter(
            activo=True,
            tipo=Precio.Tipo.MINORISTA,
            moneda=Precio.Moneda.USD,
            variante__producto__activo=True,
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
        ).aggregate(total=Coalesce(Sum(F("precio") * F("variante__stock_actual")), Decimal("0")))["total"]

        low_stock_variantes = list(
            variantes_qs.filter(stock_minimo__gt=0, stock_actual__lte=F("stock_minimo"))
            .order_by("stock_actual", "sku")[:5]
        )

        inventario_metrics = {
            "total_variantes": total_variantes,
            "total_activos": total_activos,
            "total_bajo_stock": total_bajo_stock,
            "unidades_totales": unidades_totales,
            "valor_catalogo_usd": valor_catalogo_usd,
            "valor_catalogo_ars": valor_catalogo_ars,
        }
    else:
        schema_warnings.append(
            "El módulo de inventario necesita las migraciones recientes. Ejecutá `python manage.py migrate` y volvé a intentar."
        )

    crm_metrics: dict[str, object] = {}
    try:
        crm_metrics = {
            "clientes": Cliente.objects.count(),
            "conversaciones_abiertas": Conversacion.objects.filter(estado__in=["Abierta", "En seguimiento"]).count(),
            "sla_vencidos": Conversacion.objects.filter(
                sla_vencimiento__lt=timezone.now(),
                estado__in=["Pendiente", "En seguimiento"],
            ).count(),
        }
    except Exception:
        schema_warnings.append(
            "No se pudo leer el estado del CRM. Confirmá que las migraciones del app `crm` estén aplicadas."
        )

    ventas_metrics: dict[str, object] = {}
    ultimas_ventas: list[Venta] = []
    if table_exists("ventas_venta"):
        periodo_inicio = timezone.now() - timedelta(days=30)
        ventas_qs = Venta.objects.filter(fecha__gte=periodo_inicio)
        ventas_resumen = ventas_qs.aggregate(
            total=Coalesce(Sum("total_ars"), Decimal("0")),
            tickets=Count("id"),
        )
        tickets = ventas_resumen["tickets"] or 0
        total = ventas_resumen["total"] or Decimal("0")
        promedio = total / tickets if tickets else Decimal("0")
        ventas_metrics = {
            "total_periodo": total,
            "tickets_periodo": tickets,
            "ticket_promedio": promedio,
        }
        ultimas_ventas = list(ventas_qs.select_related("vendedor").order_by("-fecha")[:5])
    else:
        schema_warnings.append(
            "El módulo de ventas todavía no está migrado. Corré `python manage.py migrate ventas`."
        )

    recent_activity: list[RegistroHistorial] = []
    if table_exists("historial_registrohistorial"):
        recent_activity = list(RegistroHistorial.objects.select_related("usuario").order_by("-fecha")[:6])

    quick_actions = [
        {
            "title": "Nuevo producto",
            "description": "Cargá un producto y su primera variante en el inventario.",
            "url": reverse("inventario:producto_crear"),
            "accent": "bg-blue-500/15 text-blue-600",
        },
        {
            "title": "Registrar venta",
            "description": "Abrí el POS para generar un ticket con descuentos e impuestos.",
            "url": reverse("ventas:pos"),
            "accent": "bg-emerald-500/15 text-emerald-600",
        },
        {
            "title": "Panel de chat",
            "description": "Gestioná conversaciones pendientes y vencidas por SLA.",
            "url": reverse("crm:panel_chat"),
            "accent": "bg-indigo-500/15 text-indigo-600",
        },
        {
            "title": "Vista previa web",
            "description": "Revisá cómo se verán los productos en la tienda pública.",
            "url": reverse("dashboard:tienda_preview"),
            "accent": "bg-slate-500/15 text-slate-600",
        },
    ]

    context = {
        "schema_warnings": schema_warnings,
        "inventario_metrics": inventario_metrics,
        "crm_metrics": crm_metrics,
        "ventas_metrics": ventas_metrics,
        "low_stock_variantes": low_stock_variantes,
        "recent_activity": recent_activity,
        "quick_actions": quick_actions,
        "valor_blue": valor_blue,
        "ultimas_ventas": ultimas_ventas,
    }

    return render(request, "dashboard/main.html", context)


@login_required
def tienda_preview(request):
    required_columns = [
        ("inventario_producto", "creado"),
        ("inventario_productovariante", "sku"),
        ("inventario_precio", "precio"),
    ]

    missing = [column for table, column in required_columns if not column_exists(table, column)]
    if missing:
        messages.warning(
            request,
            "Para usar la vista previa necesitás aplicar las migraciones de inventario (faltan columnas: "
            + ", ".join(missing)
            + ").",
        )
        return redirect("dashboard:dashboard")

    productos = (
        Producto.objects.filter(activo=True)
        .select_related("categoria")
        .prefetch_related(
            Prefetch(
                "variantes",
                queryset=ProductoVariante.objects.filter(activo=True).prefetch_related("precios"),
            )
        )
        .order_by("nombre")
    )

    catalogo = []
    for producto in productos:
        variantes_info = []
        for variante in producto.variantes.all():
            precio = variante.precios.filter(
                tipo=Precio.Tipo.MINORISTA,
                moneda=Precio.Moneda.USD,
                activo=True,
            ).order_by("-actualizado").first()
            if not precio:
                precio = variante.precios.filter(activo=True).order_by("-actualizado").first()
            variantes_info.append(
                {
                    "sku": variante.sku,
                    "atributos": variante.atributos_display,
                    "precio": precio.precio if precio else None,
                    "moneda": precio.moneda if precio else None,
                }
            )

        catalogo.append(
            {
                "producto": producto,
                "variantes": variantes_info,
            }
        )

    configuracion_sistema = ConfiguracionSistema.carga()
    configuracion_tienda = ConfiguracionTienda.obtener_unica()
    locales = Local.objects.order_by("nombre")
    return render(request, "dashboard/preview.html", {
        "catalogo": catalogo,
        "configuracion_sistema": configuracion_sistema,
        "configuracion_tienda": configuracion_tienda,
        "locales": locales,
    })
