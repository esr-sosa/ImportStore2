from django.contrib import admin
from .models import Cliente, Conversacion, Etiqueta, Mensaje

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

# Finalmente, con estas líneas, le damos la orden final a Django:
# "¡Registra el modelo Cliente en el panel de admin, usando la vista ClienteAdmin que diseñé!"
admin.site.register(Cliente, ClienteAdmin)
# "¡Y registra el modelo Conversacion, usando la vista ConversacionAdmin!"
admin.site.register(Conversacion, ConversacionAdmin)
admin.site.register(Etiqueta)
