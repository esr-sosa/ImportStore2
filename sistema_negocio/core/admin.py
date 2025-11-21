"""
Admin para modelos de core
"""
from django.contrib import admin
from .models import PerfilUsuario, DireccionEnvio, Favorito, SolicitudMayorista, NotificacionInterna


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_usuario', 'telefono', 'ciudad', 'creado')
    list_filter = ('tipo_usuario', 'creado')
    search_fields = ('usuario__username', 'usuario__email', 'telefono', 'documento')
    readonly_fields = ('creado', 'actualizado')


@admin.register(DireccionEnvio)
class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'ciudad', 'es_principal', 'creado')
    list_filter = ('es_principal', 'ciudad', 'pais', 'creado')
    search_fields = ('nombre', 'usuario__username', 'direccion', 'ciudad')
    readonly_fields = ('creado', 'actualizado')


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'variante', 'creado')
    list_filter = ('creado',)
    search_fields = ('usuario__username', 'variante__producto__nombre', 'variante__sku')
    readonly_fields = ('creado',)


@admin.register(SolicitudMayorista)
class SolicitudMayoristaAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercio', 'nombre', 'apellido', 'email', 'rubro', 'estado', 'creado')
    list_filter = ('estado', 'rubro', 'creado', 'fecha_revision')
    search_fields = ('nombre', 'apellido', 'nombre_comercio', 'email', 'dni', 'telefono')
    readonly_fields = ('creado', 'actualizado')
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'dni', 'email', 'telefono')
        }),
        ('Información del Comercio', {
            'fields': ('nombre_comercio', 'rubro', 'mensaje')
        }),
        ('Estado de la Solicitud', {
            'fields': ('estado', 'revisado_por', 'fecha_revision', 'notas')
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'estado' in form.changed_data:
            if obj.estado != 'PENDIENTE' and not obj.revisado_por:
                obj.revisado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(NotificacionInterna)
class NotificacionInternaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'titulo', 'prioridad', 'leida', 'creada', 'leida_por')
    list_filter = ('tipo', 'prioridad', 'leida', 'creada')
    search_fields = ('titulo', 'mensaje')
    readonly_fields = ('creada', 'fecha_lectura', 'leida_por')
    fieldsets = (
        ('Información', {
            'fields': ('tipo', 'prioridad', 'titulo', 'mensaje', 'url_relacionada')
        }),
        ('Estado', {
            'fields': ('leida', 'leida_por', 'fecha_lectura')
        }),
        ('Datos Adicionales', {
            'fields': ('datos_adicionales',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('creada',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('leida_por')

