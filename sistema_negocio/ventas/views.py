# ventas/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from inventario.models import ProductoVariante
from django.db.models import Q

@login_required
def pos_view(request):
    return render(request, 'ventas/pos.html')

# --- ¡NUEVA FUNCIÓN AÑADIDA AQUÍ! ---
@login_required
def buscar_productos_api(request):
    # Obtenemos el término de búsqueda que nos envía el frontend
    query = request.GET.get('q', '')

    if query:
        # Buscamos en la base de datos las variantes de productos que coincidan
        # con el término de búsqueda. Buscamos por nombre de variante O por
        # nombre del producto principal O por código de barras.
        variantes = ProductoVariante.objects.filter(
            Q(nombre_variante__icontains=query) | 
            Q(producto__nombre__icontains=query) |
            Q(producto__codigo_barras__icontains=query)
        ).select_related('producto')[:10] # Limitamos a 10 resultados para que sea rápido

        # Preparamos los datos para enviarlos de vuelta
        resultados = []
        for v in variantes:
            # Buscamos el precio minorista para mostrarlo
            precio_minorista = v.precios.filter(tipo_precio='Minorista').first()

            resultados.append({
                'id': v.id,
                'nombre': f"{v.producto.nombre} - {v.nombre_variante}",
                'stock': v.stock,
                'precio': f"{precio_minorista.precio_venta_normal:.2f}" if precio_minorista else "0.00"
            })

        return JsonResponse(resultados, safe=False)

    return JsonResponse([], safe=False)