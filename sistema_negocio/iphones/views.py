# iphones/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.humanize.templatetags.humanize import intcomma
from inventario.models import Producto, ProductoVariante, Categoria, Precio

# Compatibilidad temporal: si DetalleIphone ya no existe, lo definimos como None
try:
    from inventario.models import DetalleIphone
except Exception:
    DetalleIphone = None





from core.utils import obtener_valor_dolar_blue
from .forms import AgregarIphoneForm 
from decimal import Decimal
from historial.models import RegistroHistorial

@login_required
def iphone_dashboard(request):
    valor_dolar = obtener_valor_dolar_blue()
    
    try:
        categoria_iphone = Categoria.objects.get(nombre__iexact="Celulares")
        base_query = ProductoVariante.objects.filter(producto__categoria=categoria_iphone).select_related('producto').order_by('-producto__fecha_creacion')
    except Categoria.DoesNotExist:
        base_query = ProductoVariante.objects.none()

    # --- Lógica de KPIs (se calcula sobre el total) ---
    total_stock = base_query.count()
    valor_total_usd = Decimal(0)
    for v in base_query.prefetch_related('precios'):
        precio_obj = v.precios.filter(moneda='USD').first()
        if precio_obj:
            valor_total_usd += precio_obj.precio_venta_normal
    
    valor_total_ars = valor_total_usd * Decimal(str(valor_dolar)) if valor_dolar else Decimal(0)

    # --- Lógica de Búsqueda ---
    search_query = request.GET.get('q', None)
    if search_query:
        variantes_list = base_query.filter(
            Q(producto__nombre__icontains=search_query) |
            Q(nombre_variante__icontains=search_query) |
            Q(detalle_iphone__imei__icontains=search_query)
        ).distinct()
    else:
        variantes_list = base_query

    # --- Preparación de datos para la tabla ---
    for variante in variantes_list:
        precio_usd_obj = variante.precios.filter(moneda='USD').first()
        if precio_usd_obj and valor_dolar:
            variante.precio_usd = precio_usd_obj.precio_venta_normal
            variante.precio_ars_calculado = precio_usd_obj.precio_venta_normal * Decimal(str(valor_dolar))
        else:
            variante.precio_usd = None
            variante.precio_ars_calculado = None

    context = {
        'variantes': variantes_list,
        'valor_dolar': valor_dolar,
        'total_stock': total_stock,
        'valor_total_usd': valor_total_usd,
        'valor_total_ars': valor_total_ars,
        'search_query': search_query,
    }
    return render(request, 'iphones/dashboard.html', context)


@login_required
@transaction.atomic
def agregar_iphone(request):
    if request.method == 'POST':
        form = AgregarIphoneForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            categoria_celulares, _ = Categoria.objects.get_or_create(nombre="Celulares")
            
            producto_base = Producto.objects.create(
                nombre=data['modelo'],
                categoria=categoria_celulares,
                activo=data['activo'],
                imagen=data.get('imagen')
            )
            
            nombre_variante = f"{data['capacidad']} / {data['color']}"
            variante = ProductoVariante.objects.create(
                producto=producto_base,
                nombre_variante=nombre_variante,
                stock=1 
            )
            
            Precio.objects.create(
                variante=variante,
                moneda='USD',
                tipo_precio='Minorista',
                costo=data['costo_usd'],
                precio_venta_normal=data['precio_venta_usd'],
                precio_venta_minimo=data['costo_usd'],
                precio_venta_descuento=data.get('precio_oferta_usd')
            )
            
            if data.get('imei') or data.get('salud_bateria') or data.get('fallas_observaciones'):
                DetalleIphone.objects.create(
                    variante=variante,
                    imei=data.get('imei'),
                    salud_bateria=data.get('salud_bateria'),
                    fallas_detectadas=data.get('fallas_observaciones'),
                    es_plan_canje=data.get('es_plan_canje', False)
                )

            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.CREACION,
                descripcion=f"Se agregó el nuevo iPhone: {variante}."
            )
            return redirect('iphones:dashboard')
    else:
        form = AgregarIphoneForm()
        
    context = { 'form': form }
    return render(request, 'iphones/agregar_iphone.html', context)


@login_required
@transaction.atomic
def editar_iphone(request, variante_id):
    variante = get_object_or_404(ProductoVariante, id=variante_id)
    producto = variante.producto
    precio = variante.precios.filter(moneda='USD').first()
    detalle = getattr(variante, 'detalle_iphone', None)

    if request.method == 'POST':
        form = AgregarIphoneForm(request.POST, request.FILES, initial={'imagen': producto.imagen})
        if form.is_valid():
            data = form.cleaned_data
            
            producto.nombre = data['modelo']
            producto.activo = data['activo']
            if data.get('imagen') is not None:
                producto.imagen = data['imagen']
            producto.save()
            
            variante.nombre_variante = f"{data['capacidad']} / {data['color']}"
            variante.save()
            
            if precio:
                precio.costo = data['costo_usd']
                precio.precio_venta_normal = data['precio_venta_usd']
                precio.precio_venta_minimo = data['costo_usd']
                precio.precio_venta_descuento = data.get('precio_oferta_usd')
                precio.save()
            
            if detalle:
                detalle.imei = data.get('imei')
                detalle.salud_bateria = data.get('salud_bateria')
                detalle.fallas_detectadas = data.get('fallas_observaciones')
                detalle.es_plan_canje = data.get('es_plan_canje', False)
                detalle.save()
            elif data.get('imei'):
                DetalleIphone.objects.create(
                    variante=variante,
                    imei=data.get('imei'),
                    salud_bateria=data.get('salud_bateria'),
                    fallas_detectadas=data.get('fallas_observaciones'),
                    es_plan_canje=data.get('es_plan_canje', False)
                )

            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.MODIFICACION,
                descripcion=f"Se modificó el iPhone: {variante}."
            )
            return redirect('iphones:dashboard')
    else:
        initial_data = {
            'modelo': producto.nombre,
            'capacidad': variante.nombre_variante.split(' / ')[0] if ' / ' in variante.nombre_variante else '',
            'color': variante.nombre_variante.split(' / ')[1] if ' / ' in variante.nombre_variante else '',
            'activo': producto.activo,
            'imagen': producto.imagen,
            'costo_usd': precio.costo if precio else 0,
            'precio_venta_usd': precio.precio_venta_normal if precio else 0,
            'precio_oferta_usd': precio.precio_venta_descuento if precio else None,
            'imei': detalle.imei if detalle else '',
            'salud_bateria': detalle.salud_bateria if detalle else None,
            'fallas_observaciones': detalle.fallas_detectadas if detalle else '',
            'es_plan_canje': detalle.es_plan_canje if detalle else False
        }
        form = AgregarIphoneForm(initial=initial_data)
        
    context = {
        'form': form,
        'variante': variante 
    }
    return render(request, 'iphones/editar_iphone.html', context)


@require_POST
@login_required
def eliminar_iphone(request, variante_id):
    variante = get_object_or_404(ProductoVariante, id=variante_id)
    producto = variante.producto
    
    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.ELIMINACION,
        descripcion=f"Se eliminó el iPhone: {variante}."
    )
    
    producto.delete()
    return redirect('iphones:dashboard')

@require_POST
@login_required
def toggle_iphone_status(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = not producto.activo
    producto.save()
    
    nuevo_estado = "Activado" if producto.activo else "Desactivado"
    RegistroHistorial.objects.create(
        usuario=request.user,
        tipo_accion=RegistroHistorial.TipoAccion.CAMBIO_ESTADO,
        descripcion=f"Se cambió el estado a '{nuevo_estado}' para el producto: {producto.nombre}."
    )
    
    return redirect('iphones:dashboard')

# --- ¡NUEVAS VISTAS DE ACCIÓN AÑADIDAS AQUÍ! ---