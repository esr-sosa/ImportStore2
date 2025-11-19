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

