from django.contrib import admin

from .models import CajaDiaria, MovimientoCaja


@admin.register(CajaDiaria)
class CajaDiariaAdmin(admin.ModelAdmin):
    list_display = ["local", "fecha_apertura", "usuario_apertura", "monto_inicial_ars", "estado", "fecha_cierre"]
    list_filter = ["estado", "local", "fecha_apertura"]
    search_fields = ["local__nombre", "usuario_apertura__username"]
    readonly_fields = ["fecha_apertura", "fecha_cierre"]


@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):
    list_display = ["caja_diaria", "tipo", "metodo_pago", "monto_ars", "usuario", "fecha"]
    list_filter = ["tipo", "metodo_pago", "fecha"]
    search_fields = ["descripcion", "caja_diaria__local__nombre"]
    readonly_fields = ["fecha"]
