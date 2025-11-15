from django.contrib import admin
from .models import Cliente, Conversacion, Etiqueta, Mensaje, ClienteContexto, Cotizacion

# Primero le decimos a este archivo que "importe" o "traiga" los modelos que creamos.

# --- Vistas personalizadas para que el panel sea más útil ---

# Esta es una "vista personalizada" para el modelo Cliente.
# Le decimos a Django cómo queremos ver la lista de clientes.
class ClienteAdmin(admin.ModelAdmin):
    # Muestra estas columnas en la lista de clientes
    list_display = ('nombre', 'telefono', 'tipo_cliente', 'fecha_creacion')
    # Añade un filtro a la derecha para poder filtrar por tipo de cliente
    list_filter = ('tipo_cliente',)
    # Añade una barra de búsqueda que buscará en estos campos
    search_fields = ('nombre', 'telefono', 'email')
    
# Esta es la parte más potente: le decimos que, cuando vea una conversación,
# muestre los mensajes de esa conversación ADENTRO de la misma página.
class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0  # No muestra formularios extra para añadir mensajes nuevos
    readonly_fields = ('emisor', 'contenido', 'fecha_envio', 'enviado_por_ia', 'metadata')  # Campos que no se pueden editar

# Y aquí, la vista personalizada para las Conversaciones.
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fuente', 'estado', 'prioridad', 'asesor_asignado', 'sla_vencimiento')
    list_filter = ('fuente', 'estado', 'prioridad', 'asesor_asignado', 'etiquetas')
    search_fields = ('cliente__nombre', 'cliente__telefono', 'resumen')
    autocomplete_fields = ('cliente', 'asesor_asignado', 'etiquetas')
    date_hierarchy = 'fecha_inicio'
    inlines = [MensajeInline]  # Aquí conectamos los mensajes con la conversación

# --- El registro final ---


class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "color")
    search_fields = ("nombre",)


class ClienteContextoInline(admin.StackedInline):
    model = ClienteContexto
    can_delete = False
    verbose_name_plural = "Contexto del Cliente"
    readonly_fields = ('total_interacciones', 'ultima_interaccion', 'creado', 'actualizado')
    fieldsets = (
        ('Preferencias', {
            'fields': ('productos_interes', 'categorias_preferidas', 'tipo_consulta_comun')
        }),
        ('Comportamiento', {
            'fields': ('total_interacciones', 'ultima_interaccion', 'tags_comportamiento')
        }),
        ('Notas', {
            'fields': ('notas_internas',)
        }),
    )


class ClienteContextoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'total_interacciones', 'tipo_consulta_comun', 'ultima_interaccion')
    list_filter = ('tipo_consulta_comun', 'tags_comportamiento')
    search_fields = ('cliente__nombre', 'cliente__telefono')
    readonly_fields = ('creado', 'actualizado')


# Actualizar ClienteAdmin para incluir el inline
ClienteAdmin.inlines = [ClienteContextoInline]


# Finalmente, con estas líneas, le damos la orden final a Django:
# "¡Registra el modelo Cliente en el panel de admin, usando la vista ClienteAdmin que diseñé!"
admin.site.register(Cliente, ClienteAdmin)
# "¡Y registra el modelo Conversacion, usando la vista ConversacionAdmin!"
admin.site.register(Conversacion, ConversacionAdmin)
admin.site.register(Etiqueta, EtiquetaAdmin)
admin.site.register(ClienteContexto, ClienteContextoAdmin)


class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'estado', 'valido_hasta', 'creado')
    list_filter = ('estado', 'creado', 'valido_hasta')
    search_fields = ('cliente__nombre', 'cliente__telefono', 'id')
    readonly_fields = ('creado', 'actualizado')
    date_hierarchy = 'creado'


admin.site.register(Cotizacion, CotizacionAdmin)
