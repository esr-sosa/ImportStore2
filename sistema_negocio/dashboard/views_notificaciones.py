"""
Vistas para gestionar notificaciones internas
"""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from core.models import NotificacionInterna


@login_required
def notificaciones_view(request):
    """Vista para listar todas las notificaciones"""
    filtro_tipo = request.GET.get('tipo', '')
    filtro_leida = request.GET.get('leida', '')
    
    notificaciones = NotificacionInterna.objects.all().select_related('leida_por').order_by('-creada')
    
    if filtro_tipo:
        notificaciones = notificaciones.filter(tipo=filtro_tipo)
    
    if filtro_leida == 'true':
        notificaciones = notificaciones.filter(leida=True)
    elif filtro_leida == 'false':
        notificaciones = notificaciones.filter(leida=False)
    
    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(notificaciones, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'notificaciones': page_obj,
        'tipos': NotificacionInterna.Tipo.choices,
        'filtro_tipo': filtro_tipo,
        'filtro_leida': filtro_leida,
        'total_no_leidas': NotificacionInterna.objects.filter(leida=False).count(),
    }
    
    return render(request, 'dashboard/notificaciones.html', context)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def marcar_notificacion_leida(request, notificacion_id):
    """Marca una notificación como leída"""
    try:
        notificacion = get_object_or_404(NotificacionInterna, pk=notificacion_id)
        notificacion.marcar_como_leida(request.user)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def marcar_todas_leidas(request):
    """Marca todas las notificaciones como leídas"""
    try:
        NotificacionInterna.objects.filter(leida=False).update(
            leida=True,
            leida_por=request.user,
            fecha_lectura=timezone.now()
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

