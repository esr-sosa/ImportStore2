# dashboard/views.py

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render

from inventario.models import Precio, Producto, ProductoVariante

@login_required
def dashboard_view(request):
    # Esta vista simplemente muestra la página de bienvenida.
    return render(request, 'dashboard/main.html')


@login_required
def tienda_preview(request):
    productos = (
        Producto.objects.filter(activo=True)
        .select_related('categoria')
        .prefetch_related(
            Prefetch(
                'variantes',
                queryset=ProductoVariante.objects.filter(activo=True).prefetch_related('precios'),
            )
        )
        .order_by('nombre')
    )

    catalogo = []
    for producto in productos:
        variantes_info = []
        for variante in producto.variantes.all():
            precio = variante.precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.USD, activo=True).order_by('-actualizado').first()
            if not precio:
                precio = variante.precios.filter(activo=True).order_by('-actualizado').first()
            variantes_info.append(
                {
                    'sku': variante.sku,
                    'atributos': variante.atributos_display,
                    'precio': precio.precio if precio else None,
                    'moneda': precio.moneda if precio else None,
                }
            )

        catalogo.append(
            {
                'producto': producto,
                'variantes': variantes_info,
            }
        )

    return render(request, 'dashboard/preview.html', {'catalogo': catalogo})
