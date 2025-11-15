# crm/models.py

from django.db import models
from django.contrib.auth.models import User  # Para vincular conversaciones a los asesores (empleados)


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7,
        default="#6366f1",
        help_text="Color HEX utilizado para renderizar la etiqueta",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return self.nombre

# Modelo para los Clientes
class Cliente(models.Model):
    # Opciones para la clasificación automática requerida
    TIPO_CLIENTE_CHOICES = [
        ('Minorista', 'Minorista'),
        ('Mayorista', 'Mayorista'),
        ('Potencial', 'Potencial'),
        ('No Potencial', 'No Potencial'),
    ]

    nombre = models.CharField(max_length=150, help_text="Nombre y Apellido del cliente")
    telefono = models.CharField(max_length=20, unique=True, help_text="Número de WhatsApp. Debe ser único.")
    email = models.EmailField(max_length=254, blank=True, null=True, help_text="Email del cliente (opcional)")
    tipo_cliente = models.CharField(
        max_length=20,
        choices=TIPO_CLIENTE_CHOICES,
        default='Potencial',
        help_text="Clasificación del cliente"
    )
    instagram_handle = models.CharField(max_length=100, blank=True, null=True, help_text="Usuario de Instagram (opcional)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

# Modelo para las Conversaciones
class Conversacion(models.Model):
    # Opciones para identificar el origen de la conversación
    FUENTE_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Instagram', 'Instagram'),
    ]
    
    ESTADO_CHOICES = [
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('Pendiente', 'Pendiente'),
        ('En seguimiento', 'En seguimiento'),
    ]

    PRIORIDAD_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="conversaciones")
    asesor_asignado = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Si se elimina un asesor, la conversación no se borra
        null=True, # Permite que sea nulo
        blank=True, # Permite que el campo esté vacío en los formularios
        help_text="Asesor humano asignado. Si es Nulo, está siendo manejado por la IA."
    )
    fuente = models.CharField(max_length=20, choices=FUENTE_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierta')
    resumen = models.TextField(blank=True, help_text="Resumen de la conversación generado por la IA.")
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='medium')
    sla_vencimiento = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha estimada para volver a contactar al cliente",
    )
    etiquetas = models.ManyToManyField(
        Etiqueta,
        blank=True,
        related_name="conversaciones",
        help_text="Etiquetas utilizadas para segmentar la conversación",
    )
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversación con {self.cliente.nombre} de {self.fuente} ({self.id})"

    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"

# Modelo para cada Mensaje dentro de una Conversación
class Mensaje(models.Model):
    # Opciones para saber quién envió el mensaje
    EMISOR_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Sistema', 'Sistema'), # Usado para IA y Asesores
        ('IA_Nota', 'Nota de IA'), # <---
    ]

    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    emisor = models.CharField(max_length=10, choices=EMISOR_CHOICES)
    contenido = models.TextField()
    archivo = models.FileField(upload_to='archivos_chat/', blank=True, null=True)
    tipo_mensaje = models.CharField(max_length=20, default='texto') # texto, imagen, audio
    # --- FIN DEL NUEVO CAMPO --
    fecha_envio = models.DateTimeField(auto_now_add=True)
    enviado_por_ia = models.BooleanField(default=False, help_text="Marca si este mensaje fue enviado automáticamente por la IA.")
    metadata = models.JSONField(blank=True, null=True, help_text="Datos extra como IDs de mensaje o status de envío")
    
    def __str__(self):
        # Trunca el mensaje para una vista previa corta
        return f"Mensaje de {self.emisor}: {self.contenido[:50]}..."
        
    class Meta:
        ordering = ['fecha_envio'] # Ordena los mensajes por fecha
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"


class ClienteContexto(models.Model):
    """
    Guarda el contexto y preferencias del cliente para personalizar respuestas.
    Se actualiza automáticamente con cada interacción.
    """
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='contexto')
    
    # Preferencias detectadas
    productos_interes = models.JSONField(
        default=list,
        help_text="Lista de productos que el cliente ha consultado o mostrado interés"
    )
    categorias_preferidas = models.JSONField(
        default=list,
        help_text="Categorías de productos que más consulta"
    )
    tipo_consulta_comun = models.CharField(
        max_length=50,
        blank=True,
        help_text="Tipo de consulta más común (compra, stock, precio, etc.)"
    )
    
    # Información de comportamiento
    ultima_interaccion = models.DateTimeField(auto_now=True)
    total_interacciones = models.IntegerField(default=0)
    promedio_respuesta_segundos = models.FloatField(
        null=True,
        blank=True,
        help_text="Tiempo promedio que tarda en responder (si aplica)"
    )
    
    # Notas y observaciones
    notas_internas = models.TextField(
        blank=True,
        help_text="Notas internas sobre el cliente (no se muestran al cliente)"
    )
    tags_comportamiento = models.JSONField(
        default=list,
        help_text="Tags automáticos sobre el comportamiento (ej: 'comprador frecuente', 'consulta precios')"
    )
    
    # Metadata adicional
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos adicionales en formato JSON"
    )
    
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contexto del Cliente"
        verbose_name_plural = "Contextos de Clientes"
    
    def __str__(self):
        return f"Contexto de {self.cliente.nombre}"
    
    def actualizar_producto_interes(self, producto_nombre: str):
        """Agrega un producto a la lista de intereses"""
        if producto_nombre not in self.productos_interes:
            self.productos_interes.append(producto_nombre)
            # Mantener solo los últimos 10
            if len(self.productos_interes) > 10:
                self.productos_interes = self.productos_interes[-10:]
            self.save(update_fields=['productos_interes', 'actualizado'])
    
    def actualizar_categoria_preferida(self, categoria_nombre: str):
        """Agrega una categoría a las preferidas"""
        if categoria_nombre not in self.categorias_preferidas:
            self.categorias_preferidas.append(categoria_nombre)
            if len(self.categorias_preferidas) > 5:
                self.categorias_preferidas = self.categorias_preferidas[-5:]
            self.save(update_fields=['categorias_preferidas', 'actualizado'])


class Cotizacion(models.Model):
    """
    Cotización generada desde una conversación del CRM.
    Permite crear cotizaciones rápidas y enviarlas al cliente.
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Enviada', 'Enviada'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('Expirada', 'Expirada'),
    ]
    
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='cotizaciones')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cotizaciones')
    productos = models.JSONField(
        help_text="Lista de productos con precios: [{'sku': '...', 'nombre': '...', 'cantidad': 1, 'precio': 1000}]"
    )
    total = models.DecimalField(max_digits=12, decimal_places=2)
    valido_hasta = models.DateTimeField(
        help_text="Fecha de expiración de la cotización"
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    venta_relacionada = models.ForeignKey(
        'ventas.Venta',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Venta creada a partir de esta cotización"
    )
    notas = models.TextField(blank=True, help_text="Notas internas sobre la cotización")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-creado']
    
    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente.nombre} - ${self.total}"
    
    @property
    def esta_expirada(self):
        """Verifica si la cotización está expirada"""
        from django.utils import timezone
        return timezone.now() > self.valido_hasta