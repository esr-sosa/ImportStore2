from django import forms
from .models import Categoria, Proveedor


class InventarioFiltroForm(forms.Form):
    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Producto, SKU o código de barras…",
            "class": "w-full md:w-80 input input-bordered",
        }),
    )
    categoria = forms.ModelChoiceField(
        label="Categoría",
        required=False,
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={"class": "select select-bordered"}),
    )
    proveedor = forms.ModelChoiceField(
        label="Proveedor",
        required=False,
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={"class": "select select-bordered"}),
    )
    solo_activos = forms.BooleanField(
        label="Solo activos",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )
    bajo_stock = forms.BooleanField(
        label="Bajo stock",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )
