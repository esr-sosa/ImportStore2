# inventario/forms.py

from django import forms
from .models import Producto, ProductoVariante, Precio
from django.forms.models import inlineformset_factory

# --- FORMULARIO PRINCIPAL DEL PRODUCTO ---
# Contiene la info básica + los campos para un "producto simple"
# (que en el backend será una variante "Única").
class ProductoForm(forms.ModelForm):
    
    # --- Campos para PRODUCTO SIMPLE (cuando NO hay variantes) ---
    # Los hacemos no-requeridos, la vista (views.py) los usará si es necesario.
    stock = forms.IntegerField(
        label="Stock (simple)", 
        required=False, 
        widget=forms.NumberInput(attrs={'class': 'form-input-simple w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 50'})
    )
    costo_ars = forms.DecimalField(
        label="Costo (ARS)", 
        required=False, 
        max_digits=10, decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-input-simple w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 15000.00'})
    )
    precio_ars = forms.DecimalField(
        label="Precio Venta (ARS)", 
        required=False, 
        max_digits=10, decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-input-simple w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 25000.00'})
    )
    costo_usd = forms.DecimalField(
        label="Costo (USD)", 
        required=False, 
        max_digits=10, decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-input-simple w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 15.00'})
    )
    precio_usd = forms.DecimalField(
        label="Precio Venta (USD)", 
        required=False, 
        max_digits=10, decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-input-simple w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: 25.00'})
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'proveedor', 'imagen', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'proveedor': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            'activo': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        }

# --- FORMULARIO PARA PRECIOS (anidado en Variantes) ---
class PrecioForm(forms.ModelForm):
    class Meta:
        model = Precio
        fields = ['moneda', 'tipo_precio', 'costo', 'precio_venta_normal', 'precio_venta_descuento', 'precio_venta_minimo']
        widgets = {
            'moneda': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm text-sm'}),
            'tipo_precio': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm text-sm'}),
            'costo': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Costo'}),
            'precio_venta_normal': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'P. Venta'}),
            'precio_venta_descuento': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'P. Oferta'}),
            'precio_venta_minimo': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'P. Mínimo'}),
        }

# --- FORMULARIO PARA VARIANTES (anidado en Producto) ---
class VarianteForm(forms.ModelForm):
    class Meta:
        model = ProductoVariante
        fields = ['nombre_variante', 'stock']
        widgets = {
            'nombre_variante': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Ej: "Rojo" o "Talle L"'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-lg shadow-sm', 'placeholder': 'Stock'}),
        }

# --- FORMSET anidado: Múltiples Precios para 1 Variante ---
PrecioFormSet = inlineformset_factory(
    ProductoVariante, 
    Precio, 
    form=PrecioForm, 
    extra=1,  # Empezar con 1 formulario de precio
    min_num=0, # Permitir 0 precios si se desea
    can_delete=True,
    can_delete_extra=True
)

# --- FORMSET principal: Múltiples Variantes para 1 Producto ---
VarianteFormSet = inlineformset_factory(
    Producto, 
    ProductoVariante, 
    form=VarianteForm, 
    extra=0, # Empezar con 0 formularios de variante
    min_num=0, # Permitir 0 variantes (para el caso simple)
    can_delete=True,
    can_delete_extra=True
)