"""
Vistas para gestionar ventas web en el dashboard
"""
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ventas.models import Venta, DetalleVenta, HistorialEstadoVenta


@login_required
def ventas_web_list(request):
    """
    Lista todas las ventas web con filtros por estado
    """
    estado_filter = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    q = request.GET.get('q', '').strip()
    
    # Filtrar solo ventas web
    ventas_qs = Venta.objects.filter(origen=Venta.Origen.WEB).select_related(
        'vendedor', 'cliente'
    ).prefetch_related('detalles').order_by('-fecha')
    
    if estado_filter:
        ventas_qs = ventas_qs.filter(status=estado_filter)
    
    if fecha_desde:
        try:
            desde = timezone.datetime.strptime(fecha_desde, "%Y-%m-%d").date()
            ventas_qs = ventas_qs.filter(fecha__gte=desde)
        except ValueError:
            pass
    
    if fecha_hasta:
        try:
            hasta = timezone.datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
            ventas_qs = ventas_qs.filter(fecha__lte=hasta)
        except ValueError:
            pass
    
    if q:
        ventas_qs = ventas_qs.filter(
            Q(id__icontains=q)
            | Q(cliente_nombre__icontains=q)
            | Q(cliente_documento__icontains=q)
        )
    
    # Estadísticas
    total_ventas = ventas_qs.count()
    total_facturado = ventas_qs.aggregate(total=Sum("total_ars"))["total"] or Decimal("0")
    promedio_ticket = total_facturado / total_ventas if total_ventas > 0 else Decimal("0")
    
    # Contar por estado
    estados_count = {}
    for estado_code, estado_label in Venta.Status.choices:
        estados_count[estado_code] = Venta.objects.filter(
            origen=Venta.Origen.WEB,
            status=estado_code
        ).count()
    
    paginator = Paginator(ventas_qs, 20)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)
    
    context = {
        "ventas": page_obj.object_list,
        "page_obj": page_obj,
        "total_ventas": total_ventas,
        "total_facturado": total_facturado,
        "promedio_ticket": promedio_ticket,
        "estados_count": estados_count,
        "filtros": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "estado": estado_filter,
            "q": q,
        },
        "estados": Venta.Status.choices,
    }
    
    return render(request, "ventas/ventas_web_list.html", context)


@login_required
def venta_web_detalle(request, venta_id):
    """
    Detalle de una venta web con historial de estados
    """
    venta = get_object_or_404(
        Venta.objects.prefetch_related('detalles', 'historial_estados'),
        pk=venta_id,
        origen=Venta.Origen.WEB
    )
    
    historial = venta.historial_estados.all().order_by('-creado')
    
    context = {
        'venta': venta,
        'historial': historial,
    }
    
    return render(request, "ventas/venta_web_detalle.html", context)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def cambiar_estado_venta_web(request, venta_id):
    """
    Cambia el estado de una venta web y registra en historial
    """
    venta = get_object_or_404(Venta, pk=venta_id, origen=Venta.Origen.WEB)
    
    try:
        import json
        data = json.loads(request.body)
        nuevo_estado = data.get('estado')
        nota = data.get('nota', '').strip()
        motivo = data.get('motivo', '').strip()
        
        if nuevo_estado not in [choice[0] for choice in Venta.Status.choices]:
            return JsonResponse({'error': 'Estado inválido'}, status=400)
        
        estado_anterior = venta.status
        venta.status = nuevo_estado
        
        # Si se cancela o devuelve, guardar motivo
        if nuevo_estado in [Venta.Status.CANCELADO, Venta.Status.DEVUELTO]:
            venta.motivo_cancelacion = motivo or nota
        
        venta.save()
        
        # Registrar en historial (usar save() para evitar RETURNING en MariaDB 10.4)
        historial = HistorialEstadoVenta(
            venta=venta,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=request.user,
            nota=nota
        )
        historial.save()
        
        return JsonResponse({
            'success': True,
            'estado': nuevo_estado,
            'estado_display': venta.get_status_display()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

