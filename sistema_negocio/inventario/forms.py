from django import forms

from .models import Categoria, Precio, Producto, ProductoVariante, Proveedor


class InventarioFiltroForm(forms.Form):
    base_input = "rounded-2xl border border-slate-200 bg-white/60 px-4 py-3 text-sm font-medium text-slate-900 shadow-sm placeholder-slate-400 focus:border-black focus:outline-none focus:ring-2 focus:ring-black/10"
    select_input = "rounded-2xl border border-slate-200 bg-white/60 px-4 py-3 text-sm font-semibold text-slate-900 shadow-sm focus:border-black focus:outline-none focus:ring-2 focus:ring-black/10"

    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Producto, SKU o código de barras…",
                "class": f"w-full md:w-80 {base_input}",
            }
        ),
    )
    categoria = forms.ModelChoiceField(
        label="Categoría",
        required=False,
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={"class": select_input}),
    )
    proveedor = forms.ModelChoiceField(
        label="Proveedor",
        required=False,
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={"class": select_input}),
    )
    solo_activos = forms.BooleanField(
        label="Solo activos",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-5 w-5 rounded-full border-slate-300 text-black focus:ring-black",
            }
        ),
    )
    bajo_stock = forms.BooleanField(
        label="Bajo stock",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-5 w-5 rounded-full border-slate-300 text-black focus:ring-black",
            }
        ),
    )


class ImportacionInventarioForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo de inventario",
        help_text="Acepta CSV o XLSX exportados desde Tienda Nube u otras plataformas.",
        widget=forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-slate-600"}),
    )
    actualizar_existentes = forms.BooleanField(
        label="Actualizar productos existentes",
        required=False,
        initial=True,
    )


class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].required = False
        self.fields["proveedor"].required = False

    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "proveedor",
            "descripcion",
            "codigo_barras",
            "activo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "categoria": forms.Select(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "proveedor": forms.Select(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "descripcion": forms.Textarea(attrs={"rows": 4, "class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "codigo_barras": forms.TextInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "activo": forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300 text-black focus:ring-black"}),
        }


class ProductoVarianteForm(forms.ModelForm):
    precio_minorista_usd = forms.DecimalField(
        required=False,
        label="P. minorista USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "rounded-2xl border border-slate-200 px-3 py-2 text-sm w-full"}),
    )
    precio_minorista_ars = forms.DecimalField(
        required=False,
        label="P. minorista ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "rounded-2xl border border-slate-200 px-3 py-2 text-sm w-full"}),
    )
    precio_mayorista_usd = forms.DecimalField(
        required=False,
        label="P. mayorista USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "rounded-2xl border border-slate-200 px-3 py-2 text-sm w-full"}),
    )
    precio_mayorista_ars = forms.DecimalField(
        required=False,
        label="P. mayorista ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "rounded-2xl border border-slate-200 px-3 py-2 text-sm w-full"}),
    )

    class Meta:
        model = ProductoVariante
        fields = [
            "sku",
            "atributo_1",
            "atributo_2",
            "stock_actual",
            "stock_minimo",
            "activo",
        ]
        widgets = {
            "sku": forms.TextInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "atributo_1": forms.TextInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "atributo_2": forms.TextInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "stock_actual": forms.NumberInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "stock_minimo": forms.NumberInput(attrs={"class": "rounded-2xl border border-slate-200 px-4 py-3 text-sm w-full"}),
            "activo": forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300 text-black focus:ring-black"}),
        }

    def inicializar_precios(self, variante: ProductoVariante) -> None:
        for tipo, moneda, campo in [
            (Precio.Tipo.MINORISTA, Precio.Moneda.USD, "precio_minorista_usd"),
            (Precio.Tipo.MINORISTA, Precio.Moneda.ARS, "precio_minorista_ars"),
            (Precio.Tipo.MAYORISTA, Precio.Moneda.USD, "precio_mayorista_usd"),
            (Precio.Tipo.MAYORISTA, Precio.Moneda.ARS, "precio_mayorista_ars"),
        ]:
            precio = variante.precios.filter(tipo=tipo, moneda=moneda, activo=True).order_by("-actualizado").first()
            if precio:
                self.fields[campo].initial = precio.precio

