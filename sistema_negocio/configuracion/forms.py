from django import forms

from .models import ConfiguracionSistema, ConfiguracionTienda, PreferenciaUsuario

TEXT_INPUT_BASE = (
    "mt-1 w-full rounded-2xl border-2 border-slate-600/40 bg-slate-800/90 px-3 py-2 text-sm "
    "font-medium text-slate-100 shadow-lg placeholder-slate-400 focus:border-blue-500 focus:bg-slate-800 focus:outline-none "
    "focus:ring-2 focus:ring-blue-500/30 transition-all"
)


class ConfiguracionTiendaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionTienda
        fields = ["nombre_tienda", "logo", "cuit", "direccion", "email_contacto", "telefono_contacto", "garantia_dias_general"]
        widgets = {
            "logo": forms.FileInput(
                attrs={
                    "class": "mt-1 block w-full text-sm text-slate-600 file:mr-4 file:rounded-full file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-slate-700 dark:text-slate-200",
                    "accept": "image/png,image/jpeg,image/svg+xml",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, campo in self.fields.items():
            if isinstance(campo.widget, forms.FileInput):
                continue
            campo.widget.attrs.setdefault("class", TEXT_INPUT_BASE)
            if nombre == "telefono_contacto":
                campo.widget.attrs.setdefault("placeholder", "+54 11 0000 0000")
            if nombre == "email_contacto":
                campo.widget.attrs.setdefault("placeholder", "contacto@tu-negocio.com")
            if nombre == "direccion":
                campo.widget.attrs.setdefault("placeholder", "Dirección fiscal o del local principal")
            if nombre == "cuit":
                campo.widget.attrs.setdefault("placeholder", "00-00000000-0")


class ConfiguracionSistemaForm(forms.ModelForm):
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
            "precios_escala_activos",
            "monto_minimo_mayorista",
            "cantidad_minima_mayorista",
        ]
        widgets = {
            "color_principal": forms.TextInput(attrs={"type": "color", "class": "h-10 w-20"}),
            "notas_sistema": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        """Limpiar todos los campos booleanos para asegurar que tengan valores válidos"""
        cleaned_data = super().clean()
        
        # Lista de campos booleanos en el formulario
        boolean_fields = [
            'precios_escala_activos',
            'modo_oscuro_predeterminado',
            'mostrar_alertas',
            'acceso_admin_habilitado',
        ]
        
        # Asegurar que todos los campos booleanos tengan valores válidos
        for field_name in boolean_fields:
            # Verificar si el campo está en los datos del POST (con el prefijo)
            prefixed_name = f'{self.prefix}-{field_name}' if self.prefix else field_name
            field_in_post = prefixed_name in self.data or field_name in self.data
            
            if field_name in cleaned_data:
                value = cleaned_data[field_name]
                # Si el valor es None, cadena vacía, o no es booleano válido
                if value is None or value == '':
                    # Si el campo está en POST, intentar obtener el valor
                    if field_in_post:
                        post_value = self.data.get(prefixed_name) or self.data.get(field_name)
                        if post_value in ('on', 'true', 'True', '1', 1, True):
                            cleaned_data[field_name] = True
                        else:
                            cleaned_data[field_name] = False
                    else:
                        # Si no está en POST, el checkbox no estaba marcado
                        cleaned_data[field_name] = False
                else:
                    # El valor ya es válido, asegurarse de que sea booleano
                    cleaned_data[field_name] = bool(value)
            else:
                # Si el campo no está en cleaned_data, verificar si está en POST
                if field_in_post:
                    # Si está en POST pero no en cleaned_data, puede ser un valor inválido
                    post_value = self.data.get(prefixed_name) or self.data.get(field_name)
                    if post_value in ('on', 'true', 'True', '1', 1, True):
                        cleaned_data[field_name] = True
                    else:
                        cleaned_data[field_name] = False
                else:
                    # Si no está en POST, el checkbox no estaba marcado, establecer False
                    cleaned_data[field_name] = False
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, campo in self.fields.items():
            if nombre == "color_principal":
                campo.widget.attrs.setdefault(
                    "class",
                    "h-10 w-20 rounded-full border-2 border-slate-600/40 bg-slate-800/90",
                )
                continue
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs.update(
                    {
                        "class": "h-5 w-5 rounded border-slate-500 bg-slate-700 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-800",
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
                campo.widget.attrs.setdefault("class", TEXT_INPUT_BASE + " min-h-[120px]")
            elif isinstance(campo.widget, forms.NumberInput):
                campo.widget.attrs.setdefault("class", TEXT_INPUT_BASE)
            else:
                campo.widget.attrs.setdefault("class", TEXT_INPUT_BASE)


class PreferenciaUsuarioForm(forms.ModelForm):
    class Meta:
        model = PreferenciaUsuario
        fields = ["usa_modo_oscuro"]
        widgets = {
            "usa_modo_oscuro": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 rounded border-slate-500 bg-slate-700 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-800",
                }
            ),
        }
