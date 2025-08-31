# inventario/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import ProductoVariante, Categoria, Proveedor

@login_required
def inventario_dashboard(request):
    # Obtenemos todas las variantes de productos como base
    variantes_list = ProductoVariante.objects.select_related(
        'producto', 
        'producto__categoria', 
        'producto__proveedor'
    ).prefetch_related('precios').all().order_by('producto__nombre')

    # Obtenemos los objetos para los filtros del frontend
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    # Paginación: Mostramos 25 productos por página
    paginator = Paginator(variantes_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Preparamos los datos para la plantilla, buscando ambos precios
    for variante in page_obj:
        precios = {p.tipo_precio: p.precio_venta_normal for p in variante.precios.all()}
        variante.precio_minorista = precios.get('Minorista')
        variante.precio_mayorista = precios.get('Mayorista')

    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'proveedores': proveedores,
    }
    return render(request, 'inventario/dashboard.html', context)