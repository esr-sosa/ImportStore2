from django import forms

from .models import Local


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ["nombre", "direccion"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "mt-1 w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Nombre del local",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "mt-1 w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Dirección completa",
                }
            ),
        }
