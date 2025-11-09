from django import forms

from .models import ConfiguracionSistema, PreferenciaUsuario


class ConfiguracionSistemaForm(forms.ModelForm):
    TEXT_INPUT_CLASS = (
        "mt-1 w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm "
        "font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none "
        "focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 "
        "dark:text-slate-100 dark:focus:border-slate-500"
    )

    class Meta:
        model = ConfiguracionSistema
        fields = [
            "nombre_comercial",
            "lema",
            "logo",
            "color_principal",
            "modo_oscuro_predeterminado",
            "mostrar_alertas",
            "whatsapp_numero",
            "acceso_admin_habilitado",
            "contacto_email",
            "domicilio_comercial",
            "notas_sistema",
            "dolar_blue_manual",
        ]
        widgets = {
            "color_principal": forms.TextInput(attrs={"type": "color", "class": "h-10 w-20"}),
            "notas_sistema": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, campo in self.fields.items():
            if nombre == "color_principal":
                campo.widget.attrs.setdefault("class", "h-10 w-20 rounded-full border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900")
                continue
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs.update(
                    {
                        "class": "h-5 w-5 rounded border-slate-300 text-slate-700 focus:ring-slate-400 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200",
                    }
                )
                continue
            if isinstance(campo.widget, forms.FileInput):
                campo.widget.attrs.update(
                    {
                        "class": "mt-1 block w-full text-sm text-slate-600 file:mr-4 file:rounded-full file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-slate-700 dark:text-slate-200",
                        "accept": "image/png,image/jpeg,image/svg+xml",
                    }
                )
                continue
            if isinstance(campo.widget, forms.Textarea):
                campo.widget.attrs.setdefault("class", self.TEXT_INPUT_CLASS + " min-h-[120px]")
            else:
                campo.widget.attrs.setdefault("class", self.TEXT_INPUT_CLASS)


class PreferenciaUsuarioForm(forms.ModelForm):
    class Meta:
        model = PreferenciaUsuario
        fields = ["usa_modo_oscuro"]
        widgets = {
            "usa_modo_oscuro": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 rounded border-slate-300 text-slate-700 focus:ring-slate-400 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200",
                }
            ),
        }
