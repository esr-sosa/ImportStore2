from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from locales.models import Local

from .models import CajaDiaria, MovimientoCaja


@login_required
def vista_caja(request):
    """Vista combinada para apertura y cierre de caja."""
    # Buscar caja abierta
    caja_abierta = CajaDiaria.objects.filter(estado=CajaDiaria.Estado.ABIERTA).first()
    
    # Si hay una caja abierta, mostrar vista de cierre
    if caja_abierta:
        return _vista_cierre_interna(request, caja_abierta)
    else:
        return _vista_apertura_interna(request)


def _vista_apertura_interna(request):
    """Vista interna para apertura de caja."""
    if request.method == "POST":
        local_id = request.POST.get("local_id")
        monto_inicial = Decimal(request.POST.get("monto_inicial_ars", "0"))

        if not local_id:
            return JsonResponse({"error": "Debe seleccionar un local"}, status=400)

        local = get_object_or_404(Local, pk=local_id)

        # Verificar que no haya una caja abierta para este local
        caja_abierta = CajaDiaria.objects.filter(local=local, estado=CajaDiaria.Estado.ABIERTA).first()
        if caja_abierta:
            return JsonResponse(
                {"error": f"Ya existe una caja abierta para {local.nombre}. Debe cerrarla primero."},
                status=400,
            )

        with transaction.atomic():
            caja = CajaDiaria.objects.create(
                local=local,
                monto_inicial_ars=monto_inicial,
                usuario_apertura=request.user,
            )

            # Crear movimiento de apertura
            MovimientoCaja.objects.create(
                caja_diaria=caja,
                tipo=MovimientoCaja.Tipo.APERTURA,
                metodo_pago=MovimientoCaja.MetodoPago.EFECTIVO_ARS,
                monto_ars=monto_inicial,
                descripcion=f"Apertura de caja - Monto inicial",
                usuario=request.user,
            )

        if request.headers.get("HX-Request"):
            return JsonResponse({"status": "ok", "caja_id": caja.pk, "message": f"Caja abierta para {local.nombre}"})

        return redirect("caja:caja")

    locales = Local.objects.order_by("nombre")
    context = {
        "modo": "apertura",
        "locales": locales,
    }
    return render(request, "caja/caja.html", context)


def _vista_cierre_interna(request, caja):
    """Vista interna para cierre de caja."""
    if request.method == "POST":
        monto_cierre_real = Decimal(request.POST.get("monto_cierre_real_ars", "0"))

        if caja.estado == CajaDiaria.Estado.CERRADA:
            return JsonResponse({"error": "Esta caja ya está cerrada"}, status=400)

        with transaction.atomic():
            caja.monto_cierre_real_ars = monto_cierre_real
            caja.fecha_cierre = timezone.now()
            caja.estado = CajaDiaria.Estado.CERRADA
            caja.save()

        diferencia = caja.diferencia_ars

        if request.headers.get("HX-Request"):
            return JsonResponse(
                {
                    "status": "ok",
                    "message": f"Caja cerrada. Diferencia: ${diferencia:.2f}",
                    "diferencia": str(diferencia),
                }
            )

        return redirect("caja:caja")

    # Calcular resumen
    movimientos = caja.movimientos.all()
    total_ventas = movimientos.filter(tipo=MovimientoCaja.Tipo.VENTA).aggregate(total=Sum("monto_ars"))["total"] or Decimal("0")
    
    # Desglose por método de pago
    desglose_pago = {}
    for metodo in MovimientoCaja.MetodoPago.choices:
        metodo_code = metodo[0]
        total_metodo = movimientos.filter(tipo=MovimientoCaja.Tipo.VENTA, metodo_pago=metodo_code).aggregate(
            total=Sum("monto_ars")
        )["total"] or Decimal("0")
        if total_metodo > 0:
            desglose_pago[metodo[1]] = total_metodo

    total_esperado = caja.total_esperado_ars

    context = {
        "modo": "cierre",
        "caja": caja,
        "total_ventas": total_ventas,
        "desglose_pago": desglose_pago,
        "total_esperado": total_esperado,
        "monto_inicial": caja.monto_inicial_ars,
    }

    return render(request, "caja/caja.html", context)


@login_required
def vista_apertura(request):
    """Vista legacy para apertura de caja (redirige a vista combinada)."""
    return redirect("caja:caja")


@login_required
def vista_cierre(request, caja_id=None):
    """Vista legacy para cierre de caja (redirige a vista combinada)."""
    if caja_id:
        caja = get_object_or_404(CajaDiaria, pk=caja_id)
        if caja.estado == CajaDiaria.Estado.ABIERTA:
            return _vista_cierre_interna(request, caja)
    return redirect("caja:caja")


@login_required
def listado_cajas(request):
    """Listado de todas las cajas (abiertas y cerradas)."""
    from django.core.paginator import Paginator
    
    cajas = CajaDiaria.objects.select_related("local", "usuario_apertura").order_by("-fecha_apertura")
    
    # Filtros opcionales
    estado_filtro = request.GET.get("estado", "")
    if estado_filtro:
        cajas = cajas.filter(estado=estado_filtro)
    
    local_filtro = request.GET.get("local", "")
    if local_filtro:
        cajas = cajas.filter(local_id=local_filtro)
    
    # Paginación
    paginator = Paginator(cajas, 20)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)
    
    # Estadísticas
    total_cajas = cajas.count()
    cajas_abiertas = CajaDiaria.objects.filter(estado=CajaDiaria.Estado.ABIERTA).count()
    cajas_cerradas = CajaDiaria.objects.filter(estado=CajaDiaria.Estado.CERRADA).count()
    
    # Totales de cajas cerradas
    total_ventas_cerradas = (
        CajaDiaria.objects.filter(estado=CajaDiaria.Estado.CERRADA)
        .aggregate(total=Sum("movimientos__monto_ars"))["total"] or Decimal("0")
    )
    
    context = {
        "page_obj": page_obj,
        "cajas": page_obj.object_list,
        "estado_filtro": estado_filtro,
        "local_filtro": local_filtro,
        "locales": Local.objects.order_by("nombre"),
        "total_cajas": total_cajas,
        "cajas_abiertas": cajas_abiertas,
        "cajas_cerradas": cajas_cerradas,
        "total_ventas_cerradas": total_ventas_cerradas,
    }
    
    return render(request, "caja/listado.html", context)
