from django import forms

from .constants import CAPACITIES, COLORS, IPHONE_MODELS


IOS_INPUT = "w-full rounded-2xl border-2 border-slate-600/40 bg-slate-800/90 px-4 py-3 text-sm font-medium text-slate-100 shadow-lg placeholder-slate-400 focus:border-blue-500 focus:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/30 transition-all"
IOS_SELECT = f"{IOS_INPUT} appearance-none bg-slate-800/90 text-slate-100"
IOS_TEXTAREA = IOS_INPUT + " min-h-[120px]"
IOS_NUMBER = IOS_INPUT + " text-right"
IOS_CHECK = "h-5 w-5 rounded border-slate-500 bg-slate-700 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-800"


class AgregarIphoneForm(forms.Form):
    modelo = forms.ChoiceField(
        choices=[(m, m) for m in IPHONE_MODELS],
        label="Modelo",
        widget=forms.Select(attrs={"class": IOS_SELECT}),
    )
    capacidad = forms.ChoiceField(
        choices=[(c, c) for c in CAPACITIES],
        label="Capacidad",
        widget=forms.Select(attrs={"class": IOS_SELECT}),
    )
    color = forms.ChoiceField(
        choices=[(c, c) for c in COLORS],
        label="Color",
        widget=forms.Select(attrs={"class": IOS_SELECT}),
    )
    sku = forms.CharField(
        label="SKU interno",
        max_length=64,
        required=False,
        widget=forms.TextInput(
            attrs={"class": IOS_INPUT, "placeholder": "Ej: IPH-16PM-256-NAT (se genera automáticamente)", "id": "sku-input"}
        ),
    )
    sku_auto = forms.BooleanField(
        required=False,
        initial=True,
        label="SKU automático",
        widget=forms.CheckboxInput(attrs={"class": "switch-container", "id": "sku-auto-toggle"}),
    )
    codigo_barras = forms.CharField(
        label="Código de barras",
        max_length=64,
        required=False,
        widget=forms.TextInput(
            attrs={"class": IOS_INPUT, "placeholder": "EAN/UPC (se genera automáticamente)", "id": "codigo-barras-input"}
        ),
    )
    generar_codigo_barras = forms.BooleanField(
        required=False,
        initial=False,
        label="Generar código de barras",
        widget=forms.CheckboxInput(attrs={"class": "switch-container"}),
    )
    qr_code = forms.CharField(
        label="QR code",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"class": IOS_INPUT, "placeholder": "URL o texto (se genera automáticamente)", "id": "qr-code-input"}
        ),
    )
    generar_qr = forms.BooleanField(
        required=False,
        initial=False,
        label="Generar QR code",
        widget=forms.CheckboxInput(attrs={"class": "switch-container"}),
    )
    stock_actual = forms.IntegerField(
        label="Unidades",
        min_value=0,
        initial=1,
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER}),
    )
    stock_minimo = forms.IntegerField(
        label="Stock mínimo",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER}),
    )

    imei = forms.CharField(
        max_length=15,
        required=False,
        label="IMEI",
        widget=forms.TextInput(
            attrs={"class": IOS_INPUT, "placeholder": "15 dígitos"}
        ),
    )
    es_nuevo = forms.BooleanField(
        required=False,
        initial=False,
        label="Equipo nuevo (sin uso)",
        widget=forms.CheckboxInput(attrs={"class": "switch-container", "id": "es-nuevo-toggle"}),
    )
    salud_bateria = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        label="Salud batería (%)",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "id": "salud-bateria-input"}),
    )
    fallas_observaciones = forms.CharField(
        required=False,
        label="Condición / fallas",
        widget=forms.Textarea(attrs={"class": IOS_TEXTAREA, "placeholder": "Ej: Micro rayón en esquina."}),
    )
    notas = forms.CharField(
        required=False,
        label="Notas internas",
        widget=forms.Textarea(attrs={"class": IOS_TEXTAREA, "placeholder": "Observaciones para el equipo de ventas."}),
    )

    costo_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Costo USD",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "placeholder": "Ej: 900.00"}),
    )
    precio_venta_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Precio minorista USD",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "placeholder": "Ej: 1199.00"}),
    )
    precio_oferta_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Precio oferta USD",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "placeholder": "Opcional"}),
    )
    precio_venta_ars = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        label="Precio minorista ARS",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "placeholder": "Opcional"}),
    )
    precio_mayorista_usd = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Precio mayorista USD",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "placeholder": "Opcional"}),
    )
    precio_mayorista_ars = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        label="Precio mayorista ARS",
        widget=forms.NumberInput(attrs={"class": IOS_NUMBER, "placeholder": "Opcional"}),
    )

    es_plan_canje = forms.BooleanField(
        required=False,
        initial=False,
        label="Recibido por plan canje",
        widget=forms.CheckboxInput(attrs={"class": IOS_CHECK}),
    )
    activo = forms.BooleanField(
        required=False,
        initial=True,
        label="Disponible para la venta",
        widget=forms.CheckboxInput(attrs={"class": IOS_CHECK}),
    )

    foto = forms.ImageField(
        required=False,
        label="Fotografía principal",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full text-sm text-slate-500 file:mr-4 file:rounded-xl file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-slate-700",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        es_nuevo = cleaned_data.get("es_nuevo", False)
        salud_bateria = cleaned_data.get("salud_bateria")
        
        # Si no es nuevo, la salud de batería es obligatoria
        if not es_nuevo and not salud_bateria:
            raise forms.ValidationError({
                "salud_bateria": "La salud de batería es obligatoria para equipos usados. Si el equipo es nuevo, marcá el switch 'Equipo nuevo'."
            })
        
        # Si es nuevo, establecer salud_bateria a 100 automáticamente
        if es_nuevo and not salud_bateria:
            cleaned_data["salud_bateria"] = 100
        
        return cleaned_data

    def clean_imei(self):
        imei = self.cleaned_data.get("imei")
        if imei and (not imei.isdigit() or len(imei) != 15):
            raise forms.ValidationError("El IMEI debe contener 15 dígitos numéricos.")
        return imei

    def clean_sku(self):
        sku = self.cleaned_data.get("sku", "")
        return sku.strip().upper()
