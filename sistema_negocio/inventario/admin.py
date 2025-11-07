from django.contrib import admin
from .models import Categoria, Proveedor, Producto, ProductoVariante, Precio


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)


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


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "proveedor", "activo", "codigo_barras")
    list_filter = ("activo", "categoria", "proveedor")
    search_fields = ("nombre", "codigo_barras")
    list_editable = ("activo",)
    inlines = [VarianteInline]
    autocomplete_fields = ("categoria", "proveedor")


@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    list_display = ("sku", "producto", "atributo_1", "atributo_2", "stock_actual", "stock_minimo", "activo")
    list_filter = ("activo", "producto__categoria", "producto__proveedor")
    search_fields = ("sku", "producto__nombre", "producto__codigo_barras")
    list_editable = ("stock_actual", "stock_minimo", "activo")
    autocomplete_fields = ("producto",)
    inlines = [PrecioInline]


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ("variante", "tipo", "precio", "moneda", "activo")
    list_filter = ("tipo", "moneda", "activo")
    search_fields = ("variante__sku", "variante__producto__nombre")
    list_editable = ("precio", "activo")
    autocomplete_fields = ("variante",)
    