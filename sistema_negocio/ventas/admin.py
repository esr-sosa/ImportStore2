from django.contrib import admin

from .models import LineaVenta, Venta


class LineaVentaInline(admin.TabularInline):
    model = LineaVenta
    extra = 0
    readonly_fields = ("descripcion", "cantidad", "precio_unitario", "descuento", "total_linea")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha", "estado", "metodo_pago", "subtotal", "total", "vendedor")
    list_filter = ("estado", "metodo_pago", "fecha")
    search_fields = ("numero", "nota", "cliente_nombre")
    date_hierarchy = "fecha"
    inlines = [LineaVentaInline]
