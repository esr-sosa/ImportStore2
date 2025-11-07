from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from inventario.models import Producto, Precio, ProductoVariante
from django.views.decorators.csrf import csrf_exempt
import json

# Vista principal del punto de venta
def pos_view(request):
    return render(request, "ventas/pos.html")

# Buscar productos por nombre o SKU
def buscar_productos_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})

    productos = Producto.objects.filter(nombre__icontains=query, activo=True).values(
        "id", "nombre", "descripcion"
    )[:10]
    return JsonResponse({"results": list(productos)})

# Crear venta (API)
@csrf_exempt
def crear_venta_api(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    try:
        data = json.loads(request.body)
        productos = data.get("productos", [])
        total = 0

        # ejemplo básico: validar y calcular total
        for item in productos:
            producto_id = item.get("id")
            cantidad = int(item.get("cantidad", 1))
            precio_obj = Precio.objects.filter(variante__producto_id=producto_id, activo=True).first()

            if not precio_obj:
                continue

            total += float(precio_obj.precio) * cantidad

        # respuesta
        return JsonResponse({
            "status": "ok",
            "message": "Venta registrada correctamente (demo)",
            "total": total
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)
