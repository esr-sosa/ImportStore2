from django.contrib import admin

from .models import CarritoRemoto, DetalleVenta, Venta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = (
        "variante",
        "sku",
        "descripcion",
        "cantidad",
        "precio_unitario_ars_congelado",
        "subtotal_ars",
    )


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "status", "metodo_pago", "total_ars", "vendedor")
    list_filter = ("status", "metodo_pago", "fecha")
    search_fields = ("id", "cliente_nombre", "cliente_documento")
    date_hierarchy = "fecha"
    inlines = [DetalleVentaInline]


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("venta", "sku", "descripcion", "cantidad", "precio_unitario_ars_congelado")
    search_fields = ("venta__id", "sku", "descripcion")
    list_filter = ("venta__metodo_pago",)


@admin.register(CarritoRemoto)
class CarritoRemotoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "total_items", "actualizado")
    search_fields = ("usuario__username", "usuario__email")
    readonly_fields = ("actualizado",)
    
    def total_items(self, obj):
        if isinstance(obj.items, list):
            return sum(int(item.get("cantidad", 1)) for item in obj.items if isinstance(item, dict))
        return 0
    total_items.short_description = "Total Items"
