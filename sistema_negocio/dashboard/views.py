"""Vistas principales del panel de control."""

from __future__ import annotations

import os
from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Prefetch, Sum, DecimalField
from django.db.models.functions import Coalesce, Cast
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from core.db_inspector import column_exists, table_exists
from core.utils import obtener_valor_dolar_blue
from core.models import NotificacionInterna
from configuracion.models import ConfiguracionSistema, ConfiguracionTienda
from crm.models import Cliente, Conversacion
from historial.models import RegistroHistorial
from inventario.models import Precio, Producto, ProductoVariante, DetalleIphone
from locales.models import Local
from ventas.models import Venta, DetalleVenta


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
            ProductoVariante.objects.select_related("producto", "producto__proveedor")
            .filter(producto__activo=True)
        )

        total_variantes = variantes_qs.count()
        total_activos = variantes_qs.filter(activo=True).count()
        # Bajo stock siempre es 0, sin stock cuenta productos con stock_actual = 0
        total_bajo_stock = 0
        total_sin_stock = variantes_qs.filter(stock_actual=0).count()
        unidades_totales = variantes_qs.aggregate(total=Coalesce(Sum("stock_actual"), 0))["total"]

        valor_blue = obtener_valor_dolar_blue()

        # Valor catálogo inventario normal (excluyendo iPhones)
        valor_catalogo_usd_normal = Precio.objects.filter(
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

        valor_catalogo_ars_normal = Precio.objects.filter(
            activo=True,
            tipo=Precio.Tipo.MINORISTA,
            moneda=Precio.Moneda.ARS,
            variante__producto__activo=True,
        ).exclude(
            variante__producto__categoria__nombre__iexact="Celulares"
        ).aggregate(total=Coalesce(Sum(F("precio") * F("variante__stock_actual")), Decimal("0")))["total"]
        
        # Valor catálogo iPhones (en USD, convertir a ARS)
        valor_catalogo_usd_iphones = Precio.objects.filter(
            activo=True,
            tipo=Precio.Tipo.MINORISTA,
            moneda=Precio.Moneda.USD,
            variante__producto__activo=True,
            variante__producto__categoria__nombre__iexact="Celulares",
        ).aggregate(
            total=Coalesce(
                Sum(
                    F("precio") * F("variante__stock_actual"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                Decimal("0"),
            )
        )["total"]
        
        # Convertir iPhones USD a ARS
        valor_catalogo_ars_iphones = Decimal("0")
        if valor_blue and valor_catalogo_usd_iphones:
            valor_catalogo_ars_iphones = valor_catalogo_usd_iphones * Decimal(str(valor_blue))
        
        # Convertir ARS normal a USD para mostrar referencia
        valor_catalogo_ars_normal_en_usd = Decimal("0")
        if valor_blue and valor_catalogo_ars_normal > 0:
            valor_catalogo_ars_normal_en_usd = valor_catalogo_ars_normal / Decimal(str(valor_blue))
        
        # Totales combinados
        # USD total = USD de iPhones + conversión de ARS normal a USD
        valor_catalogo_usd_total = valor_catalogo_usd_iphones + valor_catalogo_ars_normal_en_usd + valor_catalogo_usd_normal
        valor_catalogo_ars_total = valor_catalogo_ars_normal + valor_catalogo_ars_iphones

        # ===== Valores catálogo mayorista =====
        valor_catalogo_mayorista_usd_normal = Precio.objects.filter(
            activo=True,
            tipo=Precio.Tipo.MAYORISTA,
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

        valor_catalogo_mayorista_ars_normal = Precio.objects.filter(
            activo=True,
            tipo=Precio.Tipo.MAYORISTA,
            moneda=Precio.Moneda.ARS,
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

        valor_catalogo_mayorista_usd_iphones = Precio.objects.filter(
            activo=True,
            tipo=Precio.Tipo.MAYORISTA,
            moneda=Precio.Moneda.USD,
            variante__producto__activo=True,
            variante__producto__categoria__nombre__iexact="Celulares",
        ).aggregate(
            total=Coalesce(
                Sum(
                    F("precio") * F("variante__stock_actual"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                Decimal("0"),
            )
        )["total"]

        valor_catalogo_mayorista_ars_iphones = Decimal("0")
        if valor_blue and valor_catalogo_mayorista_usd_iphones:
            valor_catalogo_mayorista_ars_iphones = valor_catalogo_mayorista_usd_iphones * Decimal(str(valor_blue))

        valor_catalogo_mayorista_ars_normal_en_usd = Decimal("0")
        if valor_blue and valor_catalogo_mayorista_ars_normal > 0:
            valor_catalogo_mayorista_ars_normal_en_usd = valor_catalogo_mayorista_ars_normal / Decimal(str(valor_blue))

        valor_catalogo_mayorista_usd_total = (
            valor_catalogo_mayorista_usd_iphones
            + valor_catalogo_mayorista_ars_normal_en_usd
            + valor_catalogo_mayorista_usd_normal
        )
        valor_catalogo_mayorista_ars_total = valor_catalogo_mayorista_ars_normal + valor_catalogo_mayorista_ars_iphones

        # Totales normal (sin iPhones) para mostrar en tarjeta principal
        valor_catalogo_minorista_usd_normal_total = valor_catalogo_usd_normal + valor_catalogo_ars_normal_en_usd
        valor_catalogo_mayorista_usd_normal_total = (
            valor_catalogo_mayorista_usd_normal + valor_catalogo_mayorista_ars_normal_en_usd
        )

        low_stock_variantes = list(
            variantes_qs.filter(stock_minimo__gt=0, stock_actual__lte=F("stock_minimo"))
            .order_by("stock_actual", "sku")[:5]
        )

        inventario_metrics = {
            "total_variantes": total_variantes,
            "total_activos": total_activos,
            "total_bajo_stock": total_bajo_stock,
            "total_sin_stock": total_sin_stock,
            "unidades_totales": unidades_totales,
            "valor_catalogo_usd": valor_catalogo_usd_total,
            "valor_catalogo_ars": valor_catalogo_ars_total,
            "valor_catalogo_ars_normal_en_usd": valor_catalogo_ars_normal_en_usd,
            "valor_catalogo_usd_iphones": valor_catalogo_usd_iphones,
            "valor_catalogo_ars_iphones": valor_catalogo_ars_iphones,
            "valor_catalogo_usd_normal": valor_catalogo_usd_normal,
            "valor_catalogo_ars_normal": valor_catalogo_ars_normal,
            "valor_catalogo_mayorista_ars": valor_catalogo_mayorista_ars_total,
            "valor_catalogo_mayorista_usd": valor_catalogo_mayorista_usd_total,
            "valor_catalogo_minorista_ars_normal": valor_catalogo_ars_normal,
            "valor_catalogo_minorista_usd_normal": valor_catalogo_minorista_usd_normal_total,
            "valor_catalogo_mayorista_ars_normal": valor_catalogo_mayorista_ars_normal,
            "valor_catalogo_mayorista_usd_normal": valor_catalogo_mayorista_usd_normal_total,
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
    ventas_por_metodo: list[dict] = []
    ventas_ultimos_7_dias: list[dict] = []
    analisis_financiero: dict[str, object] = {}
    margenes_por_metodo: list[dict] = []
    analisis_mayorista: dict[str, object] = {}
    margenes_mayorista_por_metodo: list[dict] = []
    ventas_por_origen: list[dict] = []
    ventas_por_vendedor: list[dict] = []
    top_productos: list[dict] = []
    ventas_por_categoria: list[dict] = []
    comparativa_mensual: dict[str, object] = {}
    ventas_por_hora: list[dict] = []
    
    if table_exists("ventas_venta"):
        periodo_inicio = timezone.now() - timedelta(days=30)
        mes_actual_inicio = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ventas_qs = Venta.objects.filter(fecha__gte=periodo_inicio)
        ventas_mes_actual = Venta.objects.filter(fecha__gte=mes_actual_inicio)
        
        ventas_resumen = ventas_qs.aggregate(
            total=Coalesce(Sum("total_ars"), Decimal("0")),
            tickets=Count("id"),
        )
        tickets = ventas_resumen["tickets"] or 0
        total = ventas_resumen["total"] or Decimal("0")
        promedio = total / tickets if tickets else Decimal("0")
        
        # Ventas por día (últimos 7 días)
        from django.db.models.functions import TruncDate
        ultimos_7_dias = timezone.now() - timedelta(days=7)
        ventas_7_dias = ventas_qs.filter(fecha__gte=ultimos_7_dias).annotate(
            fecha_dia=TruncDate("fecha")
        ).values("fecha_dia").annotate(
            total_dia=Coalesce(Sum("total_ars"), Decimal("0")),
            cantidad=Count("id")
        ).order_by("fecha_dia")
        
        ventas_ultimos_7_dias = [
            {
                "fecha": v["fecha_dia"].strftime("%d/%m") if v["fecha_dia"] else "",
                "total": float(v["total_dia"]),
                "cantidad": v["cantidad"]
            }
            for v in ventas_7_dias
        ]
        
        # Ventas por método de pago
        ventas_por_metodo_raw = ventas_qs.values("metodo_pago").annotate(
            total=Coalesce(Sum("total_ars"), Decimal("0")),
            cantidad=Count("id")
        )
        
        metodo_pago_dict = dict(Venta.MetodoPago.choices)
        ventas_por_metodo = [
            {
                "metodo": metodo_pago_dict.get(v["metodo_pago"], v["metodo_pago"] or "Sin método"),
                "total": float(v["total"]),
                "cantidad": v["cantidad"]
            }
            for v in ventas_por_metodo_raw
        ]
        
        # Análisis financiero del mes actual
        if table_exists("ventas_detalleventa") and valor_blue:
            total_ventas_mes = ventas_mes_actual.aggregate(
                total=Coalesce(Sum("total_ars"), Decimal("0"))
            )["total"] or Decimal("0")
            
            detalles_mes = DetalleVenta.objects.filter(
                venta__fecha__gte=mes_actual_inicio,
                variante__isnull=False
            ).select_related("variante", "venta").prefetch_related(
                "variante__detalle_iphone",
                "variante__precios"
            )
            
            total_costo_estimado = Decimal("0")
            total_ganancia_estimada = Decimal("0")
            items_con_costo = 0
            items_sin_costo = 0
            
            for detalle in detalles_mes:
                precio_venta = detalle.precio_unitario_ars_congelado * detalle.cantidad
                costo_ars = None
                
                # Intentar obtener costo desde DetalleIphone
                try:
                    if detalle.variante:
                        detalle_iphone = getattr(detalle.variante, 'detalle_iphone', None)
                        if detalle_iphone and detalle_iphone.costo_usd:
                            # Convertir USD a ARS usando el dólar blue
                            costo_ars = Decimal(str(detalle_iphone.costo_usd)) * Decimal(str(valor_blue))
                except Exception:
                    pass
                
                # Si no hay costo, estimar como 60% del precio de venta (margen típico)
                if not costo_ars or costo_ars <= 0:
                    costo_ars = precio_venta * Decimal("0.60")  # Estimación conservadora
                    items_sin_costo += detalle.cantidad
                else:
                    items_con_costo += detalle.cantidad
                
                ganancia = precio_venta - costo_ars
                total_costo_estimado += costo_ars
                total_ganancia_estimada += ganancia
            
            # Calcular márgenes
            margen_porcentaje = Decimal("0")
            if total_ventas_mes > 0:
                margen_porcentaje = (total_ganancia_estimada / total_ventas_mes) * Decimal("100")
            
            # Análisis por método de pago del mes
            margenes_por_metodo_raw = []
            for metodo in Venta.MetodoPago.choices:
                ventas_metodo = ventas_mes_actual.filter(metodo_pago=metodo[0])
                total_metodo = ventas_metodo.aggregate(
                    total=Coalesce(Sum("total_ars"), Decimal("0"))
                )["total"] or Decimal("0")
                
                detalles_metodo = DetalleVenta.objects.filter(
                    venta__in=ventas_metodo,
                    variante__isnull=False
                ).select_related("variante").prefetch_related("variante__detalle_iphone")
                
                costo_metodo = Decimal("0")
                ganancia_metodo = Decimal("0")
                
                for detalle in detalles_metodo:
                    precio_venta = detalle.precio_unitario_ars_congelado * detalle.cantidad
                    costo_ars = None
                    
                    try:
                        if detalle.variante:
                            detalle_iphone = getattr(detalle.variante, 'detalle_iphone', None)
                            if detalle_iphone and detalle_iphone.costo_usd:
                                costo_ars = Decimal(str(detalle_iphone.costo_usd)) * Decimal(str(valor_blue))
                    except Exception:
                        pass
                    
                    if not costo_ars or costo_ars <= 0:
                        costo_ars = precio_venta * Decimal("0.60")
                    
                    ganancia_metodo += precio_venta - costo_ars
                    costo_metodo += costo_ars
                
                margen_metodo = Decimal("0")
                if total_metodo > 0:
                    margen_metodo = (ganancia_metodo / total_metodo) * Decimal("100")
                
                if total_metodo > 0:
                    margenes_por_metodo_raw.append({
                        "metodo": metodo[1],
                        "total_ventas": float(total_metodo),
                        "costo": float(costo_metodo),
                        "ganancia": float(ganancia_metodo),
                        "margen_porcentaje": float(margen_metodo),
                        "cantidad": ventas_metodo.count()
                    })
            
            margenes_por_metodo = sorted(margenes_por_metodo_raw, key=lambda x: x["total_ventas"], reverse=True)
            
            # Convertir costo estimado a USD
            costo_estimado_usd = Decimal("0")
            if valor_blue and total_costo_estimado > 0:
                costo_estimado_usd = total_costo_estimado / Decimal(str(valor_blue))
            
            analisis_financiero = {
                "total_ventas_mes": float(total_ventas_mes),
                "total_costo_estimado": float(total_costo_estimado),
                "total_costo_estimado_usd": float(costo_estimado_usd),
                "total_ganancia_estimada": float(total_ganancia_estimada),
                "margen_porcentaje": float(margen_porcentaje),
                "items_con_costo": items_con_costo,
                "items_sin_costo": items_sin_costo,
                "es_ganancia": total_ganancia_estimada >= 0,
            }
            
            # Análisis de ventas mayoristas del mes actual
            
            # Identificar detalles de ventas mayoristas comparando precios
            detalles_mayorista = []
            for detalle in detalles_mes:
                if not detalle.variante:
                    continue
                
                # Obtener precio mayorista de la variante
                precio_mayorista = detalle.variante.precios.filter(
                    tipo=Precio.Tipo.MAYORISTA,
                    moneda=Precio.Moneda.ARS,
                    activo=True
                ).order_by("-actualizado").first()
                
                if precio_mayorista:
                    precio_mayorista_val = Decimal(str(precio_mayorista.precio))
                    precio_venta_val = detalle.precio_unitario_ars_congelado
                    
                    # Tolerancia del 5% para considerar que es venta mayorista
                    diferencia = abs(precio_venta_val - precio_mayorista_val)
                    tolerancia = precio_mayorista_val * Decimal("0.05")
                    
                    if diferencia <= tolerancia:
                        detalles_mayorista.append(detalle)
            
            # Inicializar analisis_mayorista siempre, incluso si no hay ventas mayoristas
            total_ventas_mayorista = Decimal("0")
            total_costo_mayorista = Decimal("0")
            total_ganancia_mayorista = Decimal("0")
            items_mayorista_con_costo = 0
            items_mayorista_sin_costo = 0
            
            if detalles_mayorista:
                # Calcular totales de ventas mayoristas
                ventas_mayorista_ids = list(set([d.venta_id for d in detalles_mayorista]))
                ventas_mayorista = ventas_mes_actual.filter(id__in=ventas_mayorista_ids)
                total_ventas_mayorista = ventas_mayorista.aggregate(
                    total=Coalesce(Sum("total_ars"), Decimal("0"))
                )["total"] or Decimal("0")
                
                # Calcular costos y ganancias de ventas mayoristas
                for detalle in detalles_mayorista:
                    precio_venta = detalle.precio_unitario_ars_congelado * detalle.cantidad
                    costo_ars = None
                    
                    try:
                        if detalle.variante:
                            detalle_iphone = getattr(detalle.variante, 'detalle_iphone', None)
                            if detalle_iphone and detalle_iphone.costo_usd:
                                costo_ars = Decimal(str(detalle_iphone.costo_usd)) * Decimal(str(valor_blue))
                    except Exception:
                        pass
                    
                    if not costo_ars or costo_ars <= 0:
                        costo_ars = precio_venta * Decimal("0.60")
                        items_mayorista_sin_costo += detalle.cantidad
                    else:
                        items_mayorista_con_costo += detalle.cantidad
                    
                    ganancia = precio_venta - costo_ars
                    total_costo_mayorista += costo_ars
                    total_ganancia_mayorista += ganancia
                
                # Análisis por método de pago para ventas mayoristas
                for metodo in Venta.MetodoPago.choices:
                    ventas_metodo_mayorista = ventas_mayorista.filter(metodo_pago=metodo[0])
                    total_metodo_mayorista = ventas_metodo_mayorista.aggregate(
                        total=Coalesce(Sum("total_ars"), Decimal("0"))
                    )["total"] or Decimal("0")
                    
                    if total_metodo_mayorista <= 0:
                        continue
                    
                    detalles_metodo_mayorista = [d for d in detalles_mayorista if d.venta_id in ventas_metodo_mayorista.values_list('id', flat=True)]
                    
                    costo_metodo_mayorista = Decimal("0")
                    ganancia_metodo_mayorista = Decimal("0")
                    
                    for detalle in detalles_metodo_mayorista:
                        precio_venta = detalle.precio_unitario_ars_congelado * detalle.cantidad
                        costo_ars = None
                        
                        try:
                            if detalle.variante:
                                detalle_iphone = getattr(detalle.variante, 'detalle_iphone', None)
                                if detalle_iphone and detalle_iphone.costo_usd:
                                    costo_ars = Decimal(str(detalle_iphone.costo_usd)) * Decimal(str(valor_blue))
                        except Exception:
                            pass
                        
                        if not costo_ars or costo_ars <= 0:
                            costo_ars = precio_venta * Decimal("0.60")
                        
                        ganancia_metodo_mayorista += precio_venta - costo_ars
                        costo_metodo_mayorista += costo_ars
                    
                    margen_metodo_mayorista = Decimal("0")
                    if total_metodo_mayorista > 0:
                        margen_metodo_mayorista = (ganancia_metodo_mayorista / total_metodo_mayorista) * Decimal("100")
                    
                    margenes_mayorista_por_metodo.append({
                        "metodo": metodo[1],
                        "total_ventas": float(total_metodo_mayorista),
                        "costo": float(costo_metodo_mayorista),
                        "ganancia": float(ganancia_metodo_mayorista),
                        "margen_porcentaje": float(margen_metodo_mayorista),
                        "cantidad": ventas_metodo_mayorista.count()
                    })
                
                margenes_mayorista_por_metodo = sorted(margenes_mayorista_por_metodo, key=lambda x: x["total_ventas"], reverse=True)
            
            # Inicializar analisis_mayorista siempre (con valores en 0 si no hay ventas)
            margen_mayorista_porcentaje = Decimal("0")
            if total_ventas_mayorista > 0:
                margen_mayorista_porcentaje = (total_ganancia_mayorista / total_ventas_mayorista) * Decimal("100")
            
            # Convertir costo estimado mayorista a USD
            costo_estimado_mayorista_usd = Decimal("0")
            if valor_blue and total_costo_mayorista > 0:
                costo_estimado_mayorista_usd = total_costo_mayorista / Decimal(str(valor_blue))
            
            analisis_mayorista = {
                "total_ventas_mes": float(total_ventas_mayorista),
                "total_costo_estimado": float(total_costo_mayorista),
                "total_costo_estimado_usd": float(costo_estimado_mayorista_usd),
                "total_ganancia_estimada": float(total_ganancia_mayorista),
                "margen_porcentaje": float(margen_mayorista_porcentaje),
                "items_con_costo": items_mayorista_con_costo,
                "items_sin_costo": items_mayorista_sin_costo,
                "es_ganancia": total_ganancia_mayorista >= 0,
            }
        
        # Ventas por origen (POS vs WEB vs MAYORISTA)
        ventas_por_origen_raw = ventas_qs.values("origen").annotate(
            total=Coalesce(Sum("total_ars"), Decimal("0")),
            cantidad=Count("id")
        )
        origen_dict = dict(Venta.Origen.choices)
        ventas_por_origen = [
            {
                "origen": origen_dict.get(v["origen"], v["origen"] or "Sin origen"),
                "total": float(v["total"]),
                "cantidad": v["cantidad"]
            }
            for v in ventas_por_origen_raw
        ]
        
        # Ventas por vendedor
        ventas_por_vendedor_raw = ventas_qs.filter(vendedor__isnull=False).values(
            "vendedor__username", "vendedor__first_name", "vendedor__last_name"
        ).annotate(
            total=Coalesce(Sum("total_ars"), Decimal("0")),
            cantidad=Count("id")
        ).order_by("-total")[:10]
        
        ventas_por_vendedor = [
            {
                "vendedor": f"{v['vendedor__first_name'] or ''} {v['vendedor__last_name'] or ''}".strip() or v['vendedor__username'],
                "total": float(v["total"]),
                "cantidad": v["cantidad"]
            }
            for v in ventas_por_vendedor_raw
        ]
        
        # Top productos vendidos (últimos 30 días)
        top_productos = []
        if table_exists("ventas_detalleventa"):
            # Usar subtotal_ars que ya está calculado en el modelo
            # Convertir cantidad a DecimalField para evitar problemas de tipos mixtos
            from django.db.models.functions import Cast
            top_productos_raw = DetalleVenta.objects.filter(
                venta__fecha__gte=periodo_inicio,
                variante__isnull=False
            ).values(
                "variante__producto__nombre", "variante__sku"
            ).annotate(
                cantidad_vendida=Coalesce(
                    Sum(Cast("cantidad", DecimalField(max_digits=10, decimal_places=0))),
                    Decimal("0")
                ),
                total_ventas=Coalesce(Sum("subtotal_ars"), Decimal("0"))
            ).order_by("-cantidad_vendida")[:10]
            
            top_productos = [
                {
                    "producto": v["variante__producto__nombre"] or "Sin nombre",
                    "sku": v["variante__sku"] or "",
                    "cantidad": int(v["cantidad_vendida"]),
                    "total": float(v["total_ventas"])
                }
                for v in top_productos_raw
            ]
        
        # Ventas por categoría
        ventas_por_categoria = []
        if table_exists("ventas_detalleventa") and table_exists("inventario_categoria"):
            from inventario.models import Categoria
            # Usar subtotal_ars que ya está calculado en el modelo
            ventas_categoria_raw = DetalleVenta.objects.filter(
                venta__fecha__gte=periodo_inicio,
                variante__producto__categoria__isnull=False
            ).values("variante__producto__categoria__nombre").annotate(
                total=Coalesce(Sum("subtotal_ars"), Decimal("0")),
                cantidad=Count("id")
            ).order_by("-total")[:10]
            
            ventas_por_categoria = [
                {
                    "categoria": v["variante__producto__categoria__nombre"] or "Sin categoría",
                    "total": float(v["total"]),
                    "cantidad": v["cantidad"]
                }
                for v in ventas_categoria_raw
            ]
        
        # Comparativa mensual (mes actual vs mes anterior)
        mes_anterior_inicio = (mes_actual_inicio - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mes_anterior_fin = mes_actual_inicio - timedelta(seconds=1)
        
        ventas_mes_anterior = Venta.objects.filter(
            fecha__gte=mes_anterior_inicio,
            fecha__lte=mes_anterior_fin
        )
        
        total_mes_anterior = ventas_mes_anterior.aggregate(
            total=Coalesce(Sum("total_ars"), Decimal("0"))
        )["total"] or Decimal("0")
        
        tickets_mes_anterior = ventas_mes_anterior.count()
        
        comparativa_mensual = {
            "mes_actual": {
                "total": float(total),
                "tickets": tickets,
                "promedio": float(promedio)
            },
            "mes_anterior": {
                "total": float(total_mes_anterior),
                "tickets": tickets_mes_anterior,
                "promedio": float(total_mes_anterior / tickets_mes_anterior) if tickets_mes_anterior > 0 else 0
            },
            "variacion_total": float((total - total_mes_anterior) / total_mes_anterior * 100) if total_mes_anterior > 0 else 0,
            "variacion_tickets": float((tickets - tickets_mes_anterior) / tickets_mes_anterior * 100) if tickets_mes_anterior > 0 else 0
        }
        
        # Ventas por hora del día (últimos 7 días)
        from django.db.models.functions import ExtractHour
        ventas_por_hora_raw = ventas_qs.filter(fecha__gte=ultimos_7_dias).annotate(
            hora=ExtractHour("fecha")
        ).values("hora").annotate(
            total=Coalesce(Sum("total_ars"), Decimal("0")),
            cantidad=Count("id")
        ).order_by("hora")
        
        ventas_por_hora = [
            {
                "hora": f"{v['hora']:02d}:00" if v.get('hora') is not None else "00:00",
                "total": float(v["total"]),
                "cantidad": v["cantidad"]
            }
            for v in ventas_por_hora_raw
            if v.get('hora') is not None
        ]
        
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

    # URL del frontend (configurable desde .env o default)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
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
            "title": "Ir a la Web",
            "description": "Abrí la tienda online en una nueva pestaña.",
            "url": frontend_url,
            "accent": "bg-purple-500/15 text-purple-600",
            "external": True,  # Marca que es un link externo
        },
        {
            "title": "Vista previa web",
            "description": "Revisá cómo se verán los productos en la tienda pública.",
            "url": reverse("dashboard:tienda_preview"),
            "accent": "bg-slate-500/15 text-slate-600",
        },
    ]

    # Obtener notificaciones no leídas
    notificaciones_no_leidas = NotificacionInterna.objects.filter(leida=False).order_by('-creada')[:10]
    total_notificaciones_no_leidas = NotificacionInterna.objects.filter(leida=False).count()
    
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
        "ventas_ultimos_7_dias": ventas_ultimos_7_dias,
        "ventas_por_metodo": ventas_por_metodo,
        "analisis_financiero": analisis_financiero,
        "margenes_por_metodo": margenes_por_metodo,
        "analisis_mayorista": analisis_mayorista,
        "margenes_mayorista_por_metodo": margenes_mayorista_por_metodo,
        "ventas_por_origen": ventas_por_origen,
        "ventas_por_vendedor": ventas_por_vendedor,
        "top_productos": top_productos,
        "ventas_por_categoria": ventas_por_categoria,
        "comparativa_mensual": comparativa_mensual,
        "ventas_por_hora": ventas_por_hora,
        "notificaciones_no_leidas": notificaciones_no_leidas,
        "total_notificaciones_no_leidas": total_notificaciones_no_leidas,
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
            # Priorizar precio ARS, luego USD
            precio_ars = variante.precios.filter(
                tipo=Precio.Tipo.MINORISTA,
                moneda=Precio.Moneda.ARS,
                activo=True,
            ).order_by("-actualizado").first()
            
            precio_usd = variante.precios.filter(
                tipo=Precio.Tipo.MINORISTA,
                moneda=Precio.Moneda.USD,
                activo=True,
            ).order_by("-actualizado").first()
            
            # Usar ARS si existe, sino USD
            precio = precio_ars or precio_usd
            if not precio:
                precio = variante.precios.filter(activo=True).order_by("-actualizado").first()
            
            variantes_info.append(
                {
                    "id": variante.id,
                    "sku": variante.sku,
                    "atributos": variante.atributos_display,
                    "precio_ars": precio_ars.precio if precio_ars else None,
                    "precio_usd": precio_usd.precio if precio_usd else None,
                    "precio": precio.precio if precio else None,
                    "moneda": precio.moneda if precio else None,
                    "stock_actual": variante.stock_actual or 0,
                }
            )

        catalogo.append(
            {
                "producto": producto,
                "variantes": variantes_info,
            }
        )

    configuracion_sistema = ConfiguracionSistema.obtener_unica()
    configuracion_tienda = ConfiguracionTienda.obtener_unica()
    locales = Local.objects.order_by("nombre")
    dolar_blue = obtener_valor_dolar_blue()
    return render(request, "dashboard/preview.html", {
        "catalogo": catalogo,
        "configuracion_sistema": configuracion_sistema,
        "configuracion_tienda": configuracion_tienda,
        "locales": locales,
        "dolar_blue": dolar_blue,
    })
