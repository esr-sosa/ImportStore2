# inventario/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction # Para asegurar que todo se guarde correctamente

from .models import Producto, ProductoVariante, Categoria, Proveedor
from .forms import ProductoForm, VarianteFormSet # Importamos nuestros nuevos formularios

@login_required
def inventario_dashboard(request):
    variantes_list = ProductoVariante.objects.select_related('producto', 'producto__categoria', 'producto__proveedor').prefetch_related('precios').all().order_by('producto__nombre')
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    paginator = Paginator(variantes_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for variante in page_obj:
        precios = {p.tipo_precio: p.precio_venta_normal for p in variante.precios.all()}
        variante.precio_minorista = precios.get('Minorista')
        variante.precio_mayorista = precios.get('Mayorista')
    context = { 'page_obj': page_obj, 'categorias': categorias, 'proveedores': proveedores }
    return render(request, 'inventario/dashboard.html', context)

@login_required
@transaction.atomic # Si algo falla durante el guardado, se deshace todo.
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        variante_formset = VarianteFormSet(request.POST, prefix='variantes')
        
        if form.is_valid() and variante_formset.is_valid():
            producto = form.save() # Guardamos el producto principal

            # Ahora guardamos las variantes asociadas a ese producto
            variantes = variante_formset.save(commit=False)
            for variante in variantes:
                variante.producto = producto
                variante.save()
            
            # (En el futuro, aquí también guardaremos los precios de cada variante)

            return redirect('inventario:dashboard')
    else:
        form = ProductoForm()
        variante_formset = VarianteFormSet(prefix='variantes')

    context = {
        'form': form,
        'variante_formset': variante_formset
    }
    return render(request, 'inventario/producto_form.html', context)
