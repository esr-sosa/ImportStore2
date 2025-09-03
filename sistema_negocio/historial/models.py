from django.db import models
from django.conf import settings

class RegistroHistorial(models.Model):
    class TipoAccion(models.TextChoices):
        CREACION = 'CREACION', 'Creación'
        MODIFICACION = 'MODIFICACION', 'Modificación'
        ELIMINACION = 'ELIMINACION', 'Eliminación'
        CAMBIO_ESTADO = 'ESTADO', 'Cambio de Estado'
        VENTA = 'VENTA', 'Venta'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="Usuario que realizó la acción."
    )
    tipo_accion = models.CharField(
        max_length=20, 
        choices=TipoAccion.choices,
        help_text="El tipo de acción realizada."
    )
    descripcion = models.TextField(
        help_text="Descripción detallada de la acción."
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que ocurrió la acción."
    )

    def __str__(self):
        return f"[{self.fecha.strftime('%d/%m/%Y %H:%M')}] {self.tipo_accion} por {self.usuario or 'Sistema'}"

    class Meta:
        verbose_name = "Registro de Historial"
        verbose_name_plural = "Registros de Historial"
        ordering = ['-fecha']
