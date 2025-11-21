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
    """
    Formulario para la configuración del sistema.
    Incluye validación robusta de campos booleanos y manejo de errores.
    """
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

    def _normalizar_booleano(self, field_name: str, value) -> bool:
        """
        Normaliza un valor a booleano estricto.
        Maneja todos los casos posibles: None, cadenas vacías, strings, números, etc.
        """
        if value is None:
            return False
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            value = value.strip()
            # Si es cadena vacía, retornar False
            if not value:
                return False
            value = value.lower()
            # Valores que se consideran True
            if value in ('true', '1', 'on', 'yes', 'si', 'sí'):
                return True
            # Cualquier otro string se considera False
            return False
        
        if isinstance(value, (int, float)):
            return bool(value) and value != 0
        
        # Para cualquier otro tipo, intentar convertir a bool
        try:
            return bool(value)
        except (TypeError, ValueError):
            return False

    def _obtener_valor_post_booleano(self, field_name: str) -> bool:
        """
        Obtiene el valor booleano desde el POST, considerando el prefijo del formulario.
        """
        prefixed_name = f'{self.prefix}-{field_name}' if self.prefix else field_name
        
        # Buscar en POST con prefijo
        post_value = self.data.get(prefixed_name)
        if post_value is None:
            # Buscar sin prefijo
            post_value = self.data.get(field_name)
        
        # Si el campo no está en POST, el checkbox no estaba marcado
        if post_value is None:
            return False
        
        return self._normalizar_booleano(field_name, post_value)

    def clean_precios_escala_activos(self):
        """Valida y normaliza el campo precios_escala_activos"""
        value = self._obtener_valor_post_booleano('precios_escala_activos')
        return value

    def clean_modo_oscuro_predeterminado(self):
        """Valida y normaliza el campo modo_oscuro_predeterminado"""
        value = self._obtener_valor_post_booleano('modo_oscuro_predeterminado')
        return value

    def clean_mostrar_alertas(self):
        """Valida y normaliza el campo mostrar_alertas"""
        value = self._obtener_valor_post_booleano('mostrar_alertas')
        return value

    def clean_acceso_admin_habilitado(self):
        """Valida y normaliza el campo acceso_admin_habilitado"""
        value = self._obtener_valor_post_booleano('acceso_admin_habilitado')
        return value

    def clean_monto_minimo_mayorista(self):
        """Valida el monto mínimo mayorista"""
        value = self.cleaned_data.get('monto_minimo_mayorista')
        if value is None:
            return 0
        if value < 0:
            raise forms.ValidationError("El monto mínimo no puede ser negativo")
        return value

    def clean_cantidad_minima_mayorista(self):
        """Valida la cantidad mínima mayorista"""
        value = self.cleaned_data.get('cantidad_minima_mayorista')
        if value is None:
            return 0
        if value < 0:
            raise forms.ValidationError("La cantidad mínima no puede ser negativa")
        return value

    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        
        # Asegurar que todos los campos booleanos estén normalizados
        boolean_fields = [
            'precios_escala_activos',
            'modo_oscuro_predeterminado',
            'mostrar_alertas',
            'acceso_admin_habilitado',
        ]
        
        for field_name in boolean_fields:
            if field_name in cleaned_data:
                cleaned_data[field_name] = self._normalizar_booleano(
                    field_name, 
                    cleaned_data[field_name]
                )
            else:
                # Si no está en cleaned_data, obtenerlo del POST
                cleaned_data[field_name] = self._obtener_valor_post_booleano(field_name)
        
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
