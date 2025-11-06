# inventario/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction 
from django.db.models import Q
from .models import Producto, ProductoVariante, Categoria, Proveedor, Precio
from .forms import ProductoForm, VarianteFormSet, PrecioFormSet
from django.forms import ValidationError # Importar ValidationError
from django.forms.models import inlineformset_factory # Importar
import logging

logger = logging.getLogger(__name__)

@login_required
def inventario_dashboard(request):
    # Esta vista (el listado) no cambia y sigue funcionando bien.
    variantes_list = ProductoVariante.objects.select_related(
        'producto', 'producto__categoria', 'producto__proveedor'
    ).prefetch_related('precios').exclude(
        producto__categoria__nombre__iexact="Celulares"
    ).order_by('producto__nombre')

    categorias = Categoria.objects.exclude(nombre__iexact="Celulares")
    proveedores = Proveedor.objects.all()
    
    paginator = Paginator(variantes_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for variante in page_obj:
        # Preparamos los precios para mostrar en el dashboard
        precios = {f"{p.moneda}_{p.tipo_precio}": p.precio_venta_normal for p in variante.precios.all()}
        variante.precio_minorista_ars = precios.get('ARS_Minorista')
        variante.precio_minorista_usd = precios.get('USD_Minorista')
        
    context = { 
        'page_obj': page_obj, 
        'categorias': categorias, 
        'proveedores': proveedores 
    }
    return render(request, 'inventario/dashboard.html', context)


# --- VISTA "AGREGAR PRODUCTO" REFACTORIZADA (ESTILO TIENDA NUBE) ---
@login_required
@transaction.atomic
def agregar_producto(request):
    
    # Detectamos si el usuario marcó el checkbox de variantes
    # El name del checkbox será 'tiene_variantes' (lo definimos en el HTML)
    usa_variantes = request.POST.get('tiene_variantes') == 'on'

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        # Usamos 'instance=Producto()' para un formset vacío en un POST
        variante_formset = VarianteFormSet(request.POST, prefix='variantes', instance=Producto())

        if form.is_valid():
            producto = form.save()

            if usa_variantes:
                # --- LÓGICA PARA PRODUCTO CON VARIANTES ---
                
                # Le decimos al formset que se vincule al producto recién creado
                variante_formset.instance = producto
                
                if not variante_formset.is_valid():
                    logger.error(f"Errores en VarianteFormSet: {variante_formset.errors}")
                    logger.error(f"Non-form errors: {variante_formset.non_form_errors()}")
                    
                    # Si usa variantes pero el formset es inválido, mostramos error
                    context = {'form': form, 'variante_formset': variante_formset}
                    # Recargamos los precios de los formsets que SÍ se enviaron
                    
                    # Esta parte es compleja: necesitamos recrear los formsets de precios para cada form de variante
                    nested_precio_formsets = []
                    for v_form in variante_formset:
                        # Creamos un prefijo único para el formset de precios
                        precio_prefix = f'precios-{v_form.prefix}'
                        v_form.precio_formset = PrecioFormSet(request.POST, instance=v_form.instance, prefix=precio_prefix)
                        nested_precio_formsets.append(v_form.precio_formset)
                        logger.error(f"Errores en PrecioFormSet anidado ({precio_prefix}): {v_form.precio_formset.errors}")

                    context['tiene_variantes'] = True # Dejamos el toggle marcado
                    return render(request, 'inventario/producto_form.html', context)

                variantes = variante_formset.save(commit=False)
                for i, variante in enumerate(variantes):
                    variante.producto = producto
                    variante.save()
                    
                    # Procesamos el FormSet de Precios para CADA variante
                    # El prefijo debe coincidir con el que genera el Javascript
                    precio_prefix = f'precios-variantes-{i}'
                    precio_formset = PrecioFormSet(request.POST, instance=variante, prefix=precio_prefix)
                    
                    if precio_formset.is_valid():
                        precios = precio_formset.save(commit=False)
                        for precio in precios:
                            precio.variante = variante
                            precio.save()
                    else:
                        logger.error(f"Error en PrecioFormSet ({precio_prefix}): {precio_formset.errors}")
                        raise ValidationError(f"Error en los precios de la variante '{variante.nombre_variante}': {precio_formset.errors}")
                
                variante_formset.save_m2m()

            else:
                # --- LÓGICA PARA PRODUCTO SIMPLE ---
                # Creamos una única variante "Única" con los datos del form principal
                data = form.cleaned_data
                variante_unica = ProductoVariante.objects.create(
                    producto=producto,
                    nombre_variante="Único", 
                    stock=data.get('stock') or 0
                )
                
                # Creamos los precios (ARS y/o USD) para esta variante única
                if data.get('precio_ars') or data.get('costo_ars'):
                    Precio.objects.create(
                        variante=variante_unica,
                        moneda='ARS',
                        tipo_precio='Minorista',
                        costo=data.get('costo_ars') or 0,
                        precio_venta_normal=data.get('precio_ars') or data.get('costo_ars') or 0,
                        precio_venta_minimo=data.get('costo_ars') or 0
                    )
                if data.get('precio_usd') or data.get('costo_usd'):
                    Precio.objects.create(
                        variante=variante_unica,
                        moneda='USD',
                        tipo_precio='Minorista',
                        costo=data.get('costo_usd') or 0,
                        precio_venta_normal=data.get('precio_usd') or data.get('costo_usd') or 0,
                        precio_venta_minimo=data.get('costo_usd') or 0
                    )

            return redirect('inventario:dashboard')
        
        else:
            # Si el ProductoForm principal no es válido
            logger.error(f"Errores en ProductoForm: {form.errors}")
            context = {'form': form, 'variante_formset': variante_formset}
            if usa_variantes:
                # Re-adjuntamos los formsets de precios para mostrar los errores
                for v_form in variante_formset:
                    precio_prefix = f'precios-{v_form.prefix}'
                    v_form.precio_formset = PrecioFormSet(request.POST, instance=v_form.instance, prefix=precio_prefix)
                context['tiene_variantes'] = True
            return render(request, 'inventario/producto_form.html', context)

    else:
        # --- LÓGICA PARA GET (Página vacía) ---
        form = ProductoForm()
        variante_formset = VarianteFormSet(prefix='variantes', instance=Producto()) # Usamos una instancia vacía
        
        # --- CORRECCIÓN CLAVE PARA EL BUG DE "NO HAY PRECIOS" ---
        # 1. Creamos un formset de precios "template"
        precio_formset_template = PrecioFormSet(
            instance=ProductoVariante(), # Instancia vacía
            prefix=f'precios-variantes-__prefix__' # Prefijo JS especial
        )
        # 2. Se lo adjuntamos al "empty_form" de las variantes
        variante_formset.empty_form.precio_formset = precio_formset_template
        # --- FIN DE LA CORRECCIÓN ---

    context = {
        'form': form,
        'variante_formset': variante_formset,
        'tiene_variantes': False # Por defecto, está en modo "Simple"
    }
    return render(request, 'inventario/producto_form.html', context)