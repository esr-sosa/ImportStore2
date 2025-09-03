from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import RegistroHistorial

@login_required
def historial_view(request):
    lista_registros = RegistroHistorial.objects.all()
    
    paginator = Paginator(lista_registros, 20) # 20 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'historial/historial_lista.html', context)
