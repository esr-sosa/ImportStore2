# inventario/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction 
from django.db.models import Q

# ¡Asegúrate de importar los modelos y el formulario nuevo!
from .models import Producto, ProductoVariante, Categoria, Proveedor, Precio
from .forms import ProductoForm 
# Ya no importamos VarianteFormSet desde aquí

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


# --- ¡AQUÍ ESTÁ LA VISTA COMPLETAMENTE REESCRITA! ---
@login_required
@transaction.atomic
def agregar_producto(request):
    if request.method == 'POST':
        # 1. Usamos solo ProductoForm. Ya no hay VarianteFormSet.
        form = ProductoForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 2. Guardamos el producto principal (Nombre, Desc, Categoría, etc.)
            producto = form.save() # Se guarda el Producto en la BD

            # 3. Extraemos los datos extra del formulario
            data = form.cleaned_data
            
            # 4. Creamos la Variante "default" automáticamente
            # Usamos "Único" como nombre_variante para productos simples.
            variante = ProductoVariante.objects.create(
                producto=producto,
                nombre_variante="Único", 
                stock=data['stock']
            )
            
            # 5. Creamos el Precio "default" automáticamente
            # Asumimos 'Minorista' y 'USD' como defaults.
            Precio.objects.create(
                variante=variante,
                moneda='USD', 
                tipo_precio='Minorista',
                costo=data['costo'],
                precio_venta_normal=data['precio_venta_normal'],
                # Aseguramos que el precio mínimo sea al menos el costo
                precio_venta_minimo=data['costo'], 
                precio_venta_descuento=data.get('precio_venta_descuento')
            )
            
            return redirect('inventario:dashboard')
    else:
        # 6. Si es GET, solo mostramos el formulario simple.
        form = ProductoForm()

    context = {
        'form': form,
        # 'variante_formset' ya no se pasa al contexto
    }
    return render(request, 'inventario/producto_form.html', context)