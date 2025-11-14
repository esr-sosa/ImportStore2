from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nombre",
            "telefono",
            "email",
            "tipo_cliente",
            "instagram_handle",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Nombre y apellido",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "+54 9 11 0000 0000",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "cliente@correo.com",
                }
            ),
            "instagram_handle": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "@importstore",
                }
            ),
            "tipo_cliente": forms.Select(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                }
            ),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono", "").strip()
        return telefono.replace(" ", "")
