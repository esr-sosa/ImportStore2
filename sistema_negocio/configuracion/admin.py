from django.contrib import admin

from .models import ConfiguracionSistema, PreferenciaUsuario


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ("nombre_comercial", "ultima_actualizacion")
    readonly_fields = ("ultima_actualizacion",)

    def has_add_permission(self, request):
        return not ConfiguracionSistema.objects.exists()


@admin.register(PreferenciaUsuario)
class PreferenciaUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "usa_modo_oscuro", "actualizado")
    search_fields = ("usuario__username", "usuario__email")
    list_filter = ("usa_modo_oscuro",)
