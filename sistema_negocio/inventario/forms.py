from django import forms
from django.utils.text import slugify

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


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "garantia_dias"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Nombre de la categoría",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Descripción (opcional)",
                }
            ),
            "garantia_dias": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Días de garantía (opcional)",
                    "min": "0",
                }
            ),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "telefono", "email", "activo"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "Nombre del proveedor",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "+54 11 0000 0000",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200/60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100",
                    "placeholder": "proveedor@correo.com",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 rounded border-slate-300 text-slate-700 focus:ring-slate-400 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200",
                }
            ),
        }


class ProductoForm(forms.ModelForm):
    generar_codigo_barras = forms.BooleanField(
        required=False,
        initial=False,
        label="Generar código de barras automáticamente",
        widget=forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300"}),
    )
    generar_qr = forms.BooleanField(
        required=False,
        initial=False,
        label="Generar QR code",
        widget=forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].required = False
        self.fields["proveedor"].required = False
        self.fields["codigo_barras"].required = False
        self.fields["codigo_barras"].widget.attrs.update({
            "id": "codigo-barras-input",
            "readonly": True,
        })

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
            "nombre": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "id": "producto-nombre",
                "placeholder": "Nombre del producto",
            }),
            "categoria": forms.Select(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            }),
            "proveedor": forms.Select(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "placeholder": "Descripción del producto",
            }),
            "codigo_barras": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "placeholder": "Escaneá o generá código de barras",
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 rounded border-white/30 bg-white/5 text-slate-100 focus:ring-white/20",
            }),
        }


class ProductoVarianteForm(forms.ModelForm):
    # SKU automático
    sku_auto = forms.BooleanField(
        required=False,
        initial=True,
        label="SKU automático",
        widget=forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-white/30", "id": "sku-auto-toggle"}),
    )
    # Generar código de barras
    generar_codigo_barras = forms.BooleanField(
        required=False,
        initial=False,
        label="Generar código de barras",
        widget=forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-white/30"}),
    )
    # Generar QR
    generar_qr = forms.BooleanField(
        required=False,
        initial=False,
        label="Generar QR code",
        widget=forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-white/30"}),
    )

    # Moneda base para conversión
    moneda_base = forms.ChoiceField(
        choices=[("USD", "USD"), ("ARS", "ARS")],
        initial="ARS",
        label="Moneda base",
        widget=forms.Select(attrs={
            "class": "glass-input rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "moneda-base-select",
        }),
    )

    # Costo
    costo_usd = forms.DecimalField(
        required=False,
        label="Costo USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "costo-usd",
            "step": "0.01",
        }),
    )
    costo_ars = forms.DecimalField(
        required=False,
        label="Costo ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "costo-ars",
            "step": "0.01",
        }),
    )

    # Precio venta (minorista)
    precio_venta_usd = forms.DecimalField(
        required=False,
        label="Precio venta USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-venta-usd",
            "step": "0.01",
        }),
    )
    precio_venta_ars = forms.DecimalField(
        required=False,
        label="Precio venta ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-venta-ars",
            "step": "0.01",
        }),
    )

    # Precio mínimo
    precio_minimo_usd = forms.DecimalField(
        required=False,
        label="Precio mínimo USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-minimo-usd",
            "step": "0.01",
        }),
    )
    precio_minimo_ars = forms.DecimalField(
        required=False,
        label="Precio mínimo ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-minimo-ars",
            "step": "0.01",
        }),
    )

    # Precio minorista
    precio_minorista_usd = forms.DecimalField(
        required=False,
        label="P. minorista USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-minorista-usd",
            "step": "0.01",
        }),
    )
    precio_minorista_ars = forms.DecimalField(
        required=False,
        label="P. minorista ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-minorista-ars",
            "step": "0.01",
        }),
    )

    # Precio mayorista
    precio_mayorista_usd = forms.DecimalField(
        required=False,
        label="P. mayorista USD",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-mayorista-usd",
            "step": "0.01",
        }),
    )
    precio_mayorista_ars = forms.DecimalField(
        required=False,
        label="P. mayorista ARS",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
            "id": "precio-mayorista-ars",
            "step": "0.01",
        }),
    )

    class Meta:
        model = ProductoVariante
        fields = [
            "sku",
            "codigo_barras",
            "qr_code",
            "atributo_1",
            "atributo_2",
            "stock_actual",
            "stock_minimo",
            "activo",
        ]
        widgets = {
            "sku": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "id": "sku-input",
                "placeholder": "SKU (se genera automáticamente)",
            }),
            "atributo_1": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "placeholder": "Ej: Color, Talle",
            }),
            "atributo_2": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "placeholder": "Ej: Capacidad, Material",
            }),
            "stock_actual": forms.NumberInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "min": "0",
            }),
            "stock_minimo": forms.NumberInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "min": "0",
            }),
            "codigo_barras": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "placeholder": "Código de barras (EAN/UPC)",
            }),
            "qr_code": forms.TextInput(attrs={
                "class": "glass-input w-full rounded-2xl border border-white/20 bg-white/5 px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:border-white/40 focus:outline-none focus:ring-2 focus:ring-white/20",
                "placeholder": "QR code (URL o texto)",
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 rounded border-white/30 bg-white/5 text-slate-100 focus:ring-white/20",
            }),
        }

    def inicializar_precios(self, variante: ProductoVariante) -> None:
        # Inicializar precios desde la base de datos
        for tipo, moneda, campo in [
            (Precio.Tipo.MINORISTA, Precio.Moneda.USD, "precio_minorista_usd"),
            (Precio.Tipo.MINORISTA, Precio.Moneda.ARS, "precio_minorista_ars"),
            (Precio.Tipo.MAYORISTA, Precio.Moneda.USD, "precio_mayorista_usd"),
            (Precio.Tipo.MAYORISTA, Precio.Moneda.ARS, "precio_mayorista_ars"),
        ]:
            precio = variante.precios.filter(tipo=tipo, moneda=moneda, activo=True).order_by("-actualizado").first()
            if precio:
                self.fields[campo].initial = precio.precio
        
        # Precio venta = minorista si no hay precio_venta específico
        precio_venta_ars = variante.precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.ARS, activo=True).order_by("-actualizado").first()
        if precio_venta_ars:
            self.fields["precio_venta_ars"].initial = precio_venta_ars.precio
        
        # Precio mínimo (si existe en el modelo, sino usar precio_venta)
        precio_minimo_ars = variante.precios.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.ARS, activo=True).order_by("-actualizado").first()
        if precio_minimo_ars:
            self.fields["precio_minimo_ars"].initial = precio_minimo_ars.precio
