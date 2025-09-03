# iphones/forms.py

from django import forms
from .constants import IPHONE_MODELS, CAPACITIES, COLORS

class AgregarIphoneForm(forms.Form):
    # --- Sección 1: Información General ---
    modelo = forms.ChoiceField(
        choices=[(m, m) for m in IPHONE_MODELS],
        label="Modelo del iPhone",
        widget=forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black'})
    )
    capacidad = forms.ChoiceField(
        choices=[(c, c) for c in CAPACITIES],
        label="Capacidad de Almacenamiento",
        widget=forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black'})
    )
    color = forms.ChoiceField(
        choices=[(c, c) for c in COLORS],
        label="Color del Equipo",
        widget=forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black'})
    )
    
    # --- Sección 2: Detalles del Equipo ---
    imei = forms.CharField(
        max_length=15,
        required=False,
        label="IMEI (Opcional)",
        help_text="Debe ser un número de 15 dígitos.",
        widget=forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black', 'placeholder': 'Ej: 358...'})
    )
    salud_bateria = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        label="Salud de la Batería (%)",
        widget=forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black', 'placeholder': 'Ej: 98'})
    )
    fallas_observaciones = forms.CharField(
        required=False,
        label="Fallas u Observaciones (Opcional)",
        widget=forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black', 'rows': 4, 'placeholder': 'Ej: Pequeña marca en la esquina superior derecha.'})
    )
    
    # --- Sección 3: Precio y Estado ---
    costo_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Precio de Costo (USD)",
        widget=forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black', 'placeholder': 'Ej: 950.00'})
    )
    precio_venta_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Precio de Venta (USD)",
        widget=forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black', 'placeholder': 'Ej: 1200.00'})
    )
    precio_oferta_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Precio de Oferta (USD, Opcional)",
        widget=forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-black focus:ring-black', 'placeholder': 'Ej: 1150.00'})
    )
    
    # --- Sección 4: Origen y Visibilidad ---
    es_plan_canje = forms.BooleanField(
        required=False,
        label="Recibido por Plan Canje",
        widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 rounded border-gray-300 text-black focus:ring-black'})
    )
    activo = forms.BooleanField(
        required=False,
        initial=True,
        label="Activo para la venta",
        widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 rounded border-gray-300 text-black focus:ring-black'})
    )
    
    # --- Sección 5: Imágenes ---
    imagen = forms.ImageField(
        required=False,
        label="Foto Principal del Equipo",
        widget=forms.ClearableFileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-gray-200 file:text-gray-800 hover:file:bg-gray-300'})
    )

    def clean_imei(self):
        imei = self.cleaned_data.get('imei')
        if imei and (not imei.isdigit() or len(imei) != 15):
            raise forms.ValidationError("El IMEI debe ser un número de 15 dígitos.")
        return imei
