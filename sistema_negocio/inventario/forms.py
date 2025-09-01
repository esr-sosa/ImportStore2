# inventario/forms.py

from django import forms
from .models import Producto, ProductoVariante, Precio, Categoria, Proveedor

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'proveedor', 'imagen', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm'}),
            'proveedor': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm'}),
            'activo': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-blue-600'}),
        }

class ProductoVarianteForm(forms.ModelForm):
    class Meta:
        model = ProductoVariante
        fields = ['nombre_variante', 'stock']

class PrecioForm(forms.ModelForm):
    class Meta:
        model = Precio
        fields = ['tipo_precio', 'costo', 'precio_venta_normal', 'precio_venta_minimo']