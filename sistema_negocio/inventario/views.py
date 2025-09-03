# inventario/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction 
from django.db.models import Q # Importamos Q para filtros complejos

from .models import Producto, ProductoVariante, Categoria, Proveedor
from .forms import ProductoForm, VarianteFormSet

@login_required
def inventario_dashboard(request):
    # --- ¡AQUÍ ESTÁ LA LÓGICA DE SEPARACIÓN! ---
    # Excluimos la categoría 'Celulares' de la consulta principal.
    variantes_list = ProductoVariante.objects.select_related(
        'producto', 'producto__categoria', 'producto__proveedor'
    ).prefetch_related('precios').exclude(
        producto__categoria__nombre__iexact="Celulares" # Excluir si el nombre de la categoría es "Celulares"
    ).order_by('producto__nombre')

    categorias = Categoria.objects.exclude(nombre__iexact="Celulares") # También la excluimos de los filtros
    proveedores = Proveedor.objects.all()
    
    paginator = Paginator(variantes_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for variante in page_obj:
        precios = {p.tipo_precio: p.precio_venta_normal for p in variante.precios.all()}
        variante.precio_minorista = precios.get('Minorista')
        variante.precio_mayorista = precios.get('Mayorista')
        
    context = { 
        'page_obj': page_obj, 
        'categorias': categorias, 
        'proveedores': proveedores 
    }
    return render(request, 'inventario/dashboard.html', context)

@login_required
@transaction.atomic
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        variante_formset = VarianteFormSet(request.POST, prefix='variantes')
        
        if form.is_valid() and variante_formset.is_valid():
            producto = form.save() 

            variantes = variante_formset.save(commit=False)
            for variante in variantes:
                variante.producto = producto
                variante.save()
            
            return redirect('inventario:dashboard')
    else:
        form = ProductoForm()
        variante_formset = VarianteFormSet(prefix='variantes')

    context = {
        'form': form,
        'variante_formset': variante_formset
    }
    return render(request, 'inventario/producto_form.html', context)