# inventario/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import ProductoVariante, Categoria, Proveedor
from .forms import ProductoForm # Importamos nuestro nuevo formulario

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
    context = { 'page_obj': page_obj, 'categorias': categorias, 'proveedores': proveedores, }
    return render(request, 'inventario/dashboard.html', context)

# --- ¡NUEVA VISTA AÑADIDA AQUÍ! ---
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            # Aquí, en el futuro, manejaremos la lógica para crear variantes y precios.
            # Por ahora, solo creamos el producto principal.
            return redirect('inventario:dashboard')
    else:
        form = ProductoForm()

    context = {
        'form': form
    }
    return render(request, 'inventario/producto_form.html', context)