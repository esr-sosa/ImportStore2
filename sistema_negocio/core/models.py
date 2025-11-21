"""
Modelos extendidos para el sistema
"""
from django.contrib.auth.models import User
from django.db import models


class PerfilUsuario(models.Model):
    """
    Perfil extendido de usuario para e-commerce
    """
    TIPO_USUARIO_CHOICES = [
        ('MINORISTA', 'Minorista'),
        ('MAYORISTA', 'Mayorista'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario'
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='MINORISTA',
        verbose_name='Tipo de Usuario',
        help_text='Define si el usuario ve precios minoristas o mayoristas'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    ciudad = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ciudad'
    )
    codigo_postal = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Código Postal'
    )
    fecha_nacimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Nacimiento'
    )
    documento = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Documento',
        help_text='DNI o documento de identidad'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
        ordering = ['-creado']

    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_tipo_usuario_display()})"


class DireccionEnvio(models.Model):
    """
    Direcciones de envío de los usuarios
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='direcciones_envio',
        verbose_name='Usuario'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre completo'
    )
    telefono = models.CharField(
        max_length=20,
        verbose_name='Teléfono'
    )
    direccion = models.TextField(verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    codigo_postal = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Código Postal'
    )
    provincia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Provincia'
    )
    pais = models.CharField(
        max_length=100,
        default='Argentina',
        verbose_name='País'
    )
    es_principal = models.BooleanField(
        default=False,
        verbose_name='Dirección Principal',
        help_text='Marcar como dirección principal'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dirección de Envío'
        verbose_name_plural = 'Direcciones de Envío'
        ordering = ['-es_principal', '-creado']

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

    def save(self, *args, **kwargs):
        # Si se marca como principal, desmarcar las demás
        if self.es_principal:
            DireccionEnvio.objects.filter(
                usuario=self.usuario,
                es_principal=True
            ).exclude(pk=self.pk).update(es_principal=False)
        super().save(*args, **kwargs)


class Favorito(models.Model):
    """
    Productos favoritos de los usuarios
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoritos',
        verbose_name='Usuario'
    )
    variante = models.ForeignKey(
        'inventario.ProductoVariante',
        on_delete=models.CASCADE,
        related_name='favoritos',
        verbose_name='Producto'
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ['usuario', 'variante']
        ordering = ['-creado']

    def __str__(self):
        return f"{self.usuario.username} - {self.variante.producto.nombre}"


class SolicitudMayorista(models.Model):
    """
    Solicitudes de cuenta mayorista pendientes de aprobación
    """
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    dni = models.CharField(max_length=20, verbose_name='DNI')
    cuit_cuil = models.CharField(max_length=20, blank=True, null=True, verbose_name='CUIT/CUIL')
    nombre_comercio = models.CharField(max_length=200, verbose_name='Nombre del Comercio')
    rubro = models.CharField(max_length=100, verbose_name='Rubro')
    email = models.EmailField(verbose_name='Email')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    mensaje = models.TextField(blank=True, null=True, verbose_name='Mensaje')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name='Estado'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    revisado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitudes_revisadas',
        verbose_name='Revisado por'
    )
    fecha_revision = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Revisión')
    notas = models.TextField(blank=True, null=True, verbose_name='Notas de Revisión')

    class Meta:
        verbose_name = 'Solicitud Mayorista'
        verbose_name_plural = 'Solicitudes Mayoristas'
        ordering = ['-creado']

    def __str__(self):
        return f"{self.nombre_comercio} - {self.get_estado_display()}"


class NotificacionInterna(models.Model):
    """
    Sistema de notificaciones internas para alertas del sistema
    """
    class Tipo(models.TextChoices):
        VENTA_WEB = "VENTA_WEB", "Nueva Venta Web"
        SOLICITUD_MAYORISTA = "SOLICITUD_MAYORISTA", "Nueva Solicitud Mayorista"
        ERROR_PAGO = "ERROR_PAGO", "Error de Pago"
        STOCK_BAJO = "STOCK_BAJO", "Stock Bajo"
        STOCK_REPOSICION = "STOCK_REPOSICION", "Stock Repuesto"
        PEDIDO_PENDIENTE = "PEDIDO_PENDIENTE", "Pedido Pendiente de Pago"
        OTRO = "OTRO", "Otro"
    
    class Prioridad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        URGENTE = "URGENTE", "Urgente"
    
    tipo = models.CharField(max_length=30, choices=Tipo.choices, verbose_name="Tipo")
    prioridad = models.CharField(max_length=20, choices=Prioridad.choices, default=Prioridad.MEDIA, verbose_name="Prioridad")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    url_relacionada = models.CharField(max_length=500, blank=True, null=True, verbose_name="URL Relacionada")
    leida = models.BooleanField(default=False, verbose_name="Leída")
    creada = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    leida_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notificaciones_leidas',
        verbose_name="Leída por"
    )
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Lectura")
    
    # Datos adicionales en JSON para flexibilidad
    datos_adicionales = models.JSONField(default=dict, blank=True, verbose_name="Datos Adicionales")
    
    class Meta:
        verbose_name = "Notificación Interna"
        verbose_name_plural = "Notificaciones Internas"
        ordering = ['-creada']
        indexes = [
            models.Index(fields=['leida', '-creada']),
            models.Index(fields=['tipo', '-creada']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo}"
    
    def marcar_como_leida(self, usuario):
        """Marca la notificación como leída"""
        from django.utils import timezone
        self.leida = True
        self.leida_por = usuario
        self.fecha_lectura = timezone.now()
        self.save(update_fields=['leida', 'leida_por', 'fecha_lectura'])

