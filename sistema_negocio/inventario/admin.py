from django.contrib import admin
from .models import (
    Categoria,
    DetalleIphone,
    PlanCanjeConfig,
    PlanCanjeTransaccion,
    Precio,
    Producto,
    ProductoImagen,
    ProductoVariante,
    Proveedor,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo_display", "parent", "descripcion", "garantia_dias")
    list_filter = ("parent", "garantia_dias")
    search_fields = ("nombre", "descripcion")
    ordering = ("parent__nombre", "nombre")
    list_select_related = ("parent",)
    
    def nombre_completo_display(self, obj):
        """Muestra el nombre completo con jerarquía."""
        nivel = obj.get_nivel()
        indent = "  " * nivel
        if obj.parent:
            return f"{indent}└─ {obj.nombre}"
        return obj.nombre
    nombre_completo_display.short_description = "Categoría"


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "email", "activo")
    search_fields = ("nombre", "telefono", "email")
    list_filter = ("activo",)
    list_editable = ("activo",)


class PrecioInline(admin.TabularInline):
    model = Precio
    extra = 0
    fields = ("tipo", "precio", "moneda", "activo")
    classes = ["collapse"]


class VarianteInline(admin.TabularInline):
    model = ProductoVariante
    extra = 0
    fields = ("sku", "atributo_1", "atributo_2", "stock_actual", "stock_minimo", "activo")
    classes = ["collapse"]


class DetalleIphoneInline(admin.StackedInline):
    model = DetalleIphone
    extra = 0
    classes = ["collapse"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "imei",
                    ("salud_bateria", "es_plan_canje"),
                    "costo_usd",
                    ("precio_venta_usd", "precio_oferta_usd"),
                    "notas",
                    "foto",
                )
            },
        ),
    )


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 0
    fields = ("imagen", "orden", "creado", "actualizado")
    readonly_fields = ("creado", "actualizado")
    classes = ["collapse"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "proveedor", "activo", "codigo_barras")
    list_filter = ("activo", "categoria", "proveedor")
    search_fields = ("nombre", "codigo_barras")
    list_editable = ("activo",)
    inlines = [ProductoImagenInline, VarianteInline]
    autocomplete_fields = ("categoria", "proveedor")


@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    list_display = ("sku", "producto", "atributo_1", "atributo_2", "stock_actual", "stock_minimo", "activo")
    list_filter = ("activo", "producto__categoria", "producto__proveedor")
    search_fields = ("sku", "producto__nombre", "producto__codigo_barras")
    list_editable = ("stock_actual", "stock_minimo", "activo")
    autocomplete_fields = ("producto",)
    inlines = [DetalleIphoneInline, PrecioInline]


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ("variante", "tipo", "precio", "moneda", "activo")
    list_filter = ("tipo", "moneda", "activo")
    search_fields = ("variante__sku", "variante__producto__nombre")
    list_editable = ("precio", "activo")
    autocomplete_fields = ("variante",)


@admin.register(PlanCanjeConfig)
class PlanCanjeConfigAdmin(admin.ModelAdmin):
    list_display = ("modelo_iphone", "capacidad", "valor_base_canje_usd", "activo", "actualizado")
    list_filter = ("activo", "modelo_iphone")
    search_fields = ("modelo_iphone", "capacidad")
    list_editable = ("activo", "valor_base_canje_usd")
    ordering = ("modelo_iphone", "capacidad")
    fieldsets = (
        ("Información Básica", {
            "fields": ("modelo_iphone", "capacidad", "valor_base_canje_usd", "activo")
        }),
        ("Descuentos", {
            "fields": ("descuentos_bateria", "descuentos_estado", "descuentos_accesorios"),
            "description": "Descuentos en formato JSON. Ej: {'<80': 0.15, '80-90': 0.10, '>90': 0.0}"
        }),
        ("Guías de Ayuda", {
            "fields": ("guia_estado_excelente", "guia_estado_bueno", "guia_estado_regular"),
            "description": "Guías que se mostrarán al admin para ayudar a evaluar el estado del iPhone"
        }),
    )


@admin.register(PlanCanjeTransaccion)
class PlanCanjeTransaccionAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "iphone_recibido_modelo", "iphone_entregado", "diferencia_ars", "vendedor")
    list_filter = ("fecha", "iphone_recibido_estado", "vendedor")
    search_fields = ("iphone_recibido_modelo", "iphone_recibido_imei", "cliente_nombre", "venta_asociada__id")
    readonly_fields = ("fecha", "creado", "actualizado")
    date_hierarchy = "fecha"
    ordering = ("-fecha",)
    