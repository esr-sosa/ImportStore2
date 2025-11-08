from django import forms
from .models import Categoria, Proveedor


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
