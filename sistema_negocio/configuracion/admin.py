from django.contrib import admin

from .models import ConfiguracionSistema, ConfiguracionTienda, PreferenciaUsuario, EscalaPrecioMayorista


@admin.register(ConfiguracionTienda)
class ConfiguracionTiendaAdmin(admin.ModelAdmin):
    list_display = ("nombre_tienda", "cuit", "actualizado")
    readonly_fields = ("actualizado",)

    def has_add_permission(self, request):
        return not ConfiguracionTienda.objects.exists()


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ("nombre_comercial", "precios_escala_activos", "monto_minimo_mayorista", "cantidad_minima_mayorista")
    readonly_fields = ()

    def has_add_permission(self, request):
        return not ConfiguracionSistema.objects.exists()


@admin.register(PreferenciaUsuario)
class PreferenciaUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "usa_modo_oscuro", "actualizado")
    search_fields = ("usuario__username", "usuario__email")
    list_filter = ("usa_modo_oscuro",)


@admin.register(EscalaPrecioMayorista)
class EscalaPrecioMayoristaAdmin(admin.ModelAdmin):
    list_display = ("cantidad_minima", "cantidad_maxima", "porcentaje_descuento", "activo", "orden")
    list_filter = ("activo",)
    ordering = ("orden", "cantidad_minima")
    fieldsets = (
        ("Rango de Cantidad", {
            "fields": ("cantidad_minima", "cantidad_maxima", "orden")
        }),
        ("Descuento", {
            "fields": ("porcentaje_descuento", "activo")
        }),
        ("Configuración", {
            "fields": ("configuracion",)
        }),
    )
