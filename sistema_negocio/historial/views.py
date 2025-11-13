from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import RegistroHistorial

@login_required
def historial_view(request):
    lista_registros = RegistroHistorial.objects.all()
    
    # Filtros
    tipo_accion = request.GET.get('tipo_accion', '')
    periodo = request.GET.get('periodo', '')
    
    # Filtrar por tipo de acción
    if tipo_accion:
        lista_registros = lista_registros.filter(tipo_accion=tipo_accion)
    
    # Filtrar por período
    ahora = timezone.now()
    if periodo == 'hoy':
        lista_registros = lista_registros.filter(fecha__date=ahora.date())
    elif periodo == 'ayer':
        ayer = ahora - timedelta(days=1)
        lista_registros = lista_registros.filter(fecha__date=ayer.date())
    elif periodo == 'semana':
        semana_pasada = ahora - timedelta(days=7)
        lista_registros = lista_registros.filter(fecha__gte=semana_pasada)
    elif periodo == 'mes':
        mes_pasado = ahora - timedelta(days=30)
        lista_registros = lista_registros.filter(fecha__gte=mes_pasado)
    elif periodo == '3meses':
        tres_meses = ahora - timedelta(days=90)
        lista_registros = lista_registros.filter(fecha__gte=tres_meses)
    
    paginator = Paginator(lista_registros, 20) # 20 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipos_accion': RegistroHistorial.TipoAccion.choices,
        'filtros': {
            'tipo_accion': tipo_accion,
            'periodo': periodo,
        },
    }
    return render(request, 'historial/historial_lista.html', context)
