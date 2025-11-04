# inventario/forms.py

from django import forms
from .models import Producto, ProductoVariante, Precio

class ProductoForm(forms.ModelForm):
    # --- ¡CAMPOS NUEVOS AÑADIDOS! ---
    # Estos campos no están en el modelo 'Producto', pero los vamos a capturar aquí
    # para pasárselos a la vista.
    stock = forms.IntegerField(
        label="Stock inicial",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Ej: 50'})
    )
    costo = forms.DecimalField(
        label="Costo (USD)",
        required=True,
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Ej: 150.00'})
    )
    precio_venta_normal = forms.DecimalField(
        label="Precio de Venta (USD)",
        required=True,
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Ej: 250.00'})
    )
    precio_venta_descuento = forms.DecimalField(
        label="Precio de Oferta (USD, Opcional)",
        required=False,
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Ej: 225.00'})
    )
    
    class Meta:
        model = Producto
        # El 'stock' no está aquí, porque lo definimos arriba.
        fields = ['nombre', 'descripcion', 'categoria', 'proveedor', 'imagen', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'proveedor': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            'activo': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        }

# --- NO TOCAMOS EL RESTO DEL ARCHIVO ---
# (Dejamos los otros Formsets por si los usamos en el futuro en otro lado)

class VarianteForm(forms.ModelForm):
    class Meta:
        model = ProductoVariante
        fields = ['nombre_variante', 'stock']
        widgets = {
            'nombre_variante': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 128GB / Azul'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 10'}),
        }

class PrecioForm(forms.ModelForm):
    class Meta:
        model = Precio
        fields = ['tipo_precio', 'moneda', 'costo', 'precio_venta_normal', 'precio_venta_minimo']
        widgets = {
            'tipo_precio': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm'}),
            'moneda': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm'}),
            'costo': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Costo'}),
            'precio_venta_normal': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Precio Venta'}),
            'precio_venta_minimo': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Mínimo Venta'}),
        }

# Un FormSet para manejar múltiples precios DENTRO de una variante
PrecioFormSet = forms.inlineformset_factory(
    ProductoVariante, Precio, form=PrecioForm, extra=2, max_num=2, can_delete=False
)

# Un FormSet para manejar múltiples variantes DENTRO de un producto
VarianteFormSet = forms.inlineformset_factory(
    Producto, ProductoVariante, form=VarianteForm, extra=1, can_delete=True, can_delete_extra=True
)