from django.contrib import admin

from .models import DetalleVenta, Venta


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
