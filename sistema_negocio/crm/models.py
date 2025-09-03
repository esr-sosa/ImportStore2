# crm/models.py

from django.db import models
from django.contrib.auth.models import User # Para vincular conversaciones a los asesores (empleados)

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
    fecha_envio = models.DateTimeField(auto_now_add=True)
    enviado_por_ia = models.BooleanField(default=False, help_text="Marca si este mensaje fue enviado automáticamente por la IA.")
    
    def __str__(self):
        # Trunca el mensaje para una vista previa corta
        return f"Mensaje de {self.emisor}: {self.contenido[:50]}..."
        
    class Meta:
        ordering = ['fecha_envio'] # Ordena los mensajes por fecha
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"