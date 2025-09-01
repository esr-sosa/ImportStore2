# iphones/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventario.models import ProductoVariante, Categoria
from core.utils import obtener_valor_dolar_blue # Importamos nuestra herramienta

@login_required
def iphone_dashboard(request):
    # Buscamos la cotización del dólar en tiempo real
    valor_dolar = obtener_valor_dolar_blue()

    # Filtramos para obtener solo los productos de la categoría 'Celulares' (o 'iPhones')
    # ¡IMPORTANTE! Asegurate de tener una categoría con este nombre.
    try:
        categoria_iphone = Categoria.objects.get(nombre__iexact="Celulares")
        variantes_list = ProductoVariante.objects.filter(producto__categoria=categoria_iphone)
    except Categoria.DoesNotExist:
        variantes_list = [] # Si no existe la categoría, no mostramos nada

    # Preparamos los datos para la plantilla
    for variante in variantes_list:
        # Buscamos el precio en USD
        precio_usd_obj = variante.precios.filter(moneda='USD').first()
        if precio_usd_obj and valor_dolar:
            variante.precio_usd = precio_usd_obj.precio_venta_normal
            # Calculamos el precio en pesos
            variante.precio_ars_calculado = precio_usd_obj.precio_venta_normal * valor_dolar
        else:
            variante.precio_usd = None
            variante.precio_ars_calculado = None

    context = {
        'variantes': variantes_list,
        'valor_dolar': valor_dolar
    }
    return render(request, 'iphones/dashboard.html', context)
