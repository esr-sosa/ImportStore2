from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from locales.models import Local
from ventas.models import Venta

User = get_user_model()


class CajaDiaria(models.Model):
    class Estado(models.TextChoices):
        ABIERTA = "ABIERTA", "Abierta"
        CERRADA = "CERRADA", "Cerrada"

    local = models.ForeignKey(Local, on_delete=models.PROTECT, related_name="cajas")
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    monto_inicial_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    usuario_apertura = models.ForeignKey(User, on_delete=models.PROTECT, related_name="cajas_aperturadas")
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre_real_ars = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, help_text="Conteo físico de efectivo"
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ABIERTA)

    class Meta:
        verbose_name = "Caja Diaria"
        verbose_name_plural = "Cajas Diarias"
        ordering = ["-fecha_apertura"]
        indexes = [
            models.Index(fields=["local", "estado"], name="idx_caja_local_estado"),
            models.Index(fields=["fecha_apertura"], name="idx_caja_fecha"),
        ]

    def __str__(self):
        return f"Caja {self.local.nombre} - {self.fecha_apertura.strftime('%d/%m/%Y')} ({self.estado})"

    @property
    def total_esperado_ars(self) -> Decimal:
        """Calcula el total esperado sumando movimientos."""
        return self.movimientos.aggregate(
            total=models.Sum("monto_ars")
        )["total"] or Decimal("0.00")

    @property
    def diferencia_ars(self) -> Decimal:
        """Diferencia entre el conteo físico y el esperado."""
        if self.monto_cierre_real_ars is None:
            return Decimal("0.00")
        return self.monto_cierre_real_ars - self.total_esperado_ars


class MovimientoCaja(models.Model):
    class Tipo(models.TextChoices):
        APERTURA = "APERTURA", "Apertura"
        VENTA = "VENTA", "Venta"
        RETIRO = "RETIRO", "Retiro"
        INGRESO_EXTRA = "INGRESO_EXTRA", "Ingreso Extra"

    class MetodoPago(models.TextChoices):
        EFECTIVO_ARS = "EFECTIVO_ARS", "Efectivo ARS"
        EFECTIVO_USD = "EFECTIVO_USD", "Efectivo USD"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"
        TARJETA = "TARJETA", "Tarjeta"

    caja_diaria = models.ForeignKey(CajaDiaria, on_delete=models.CASCADE, related_name="movimientos")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    monto_ars = models.DecimalField(max_digits=12, decimal_places=2, help_text="Negativo para retiros")
    descripcion = models.TextField(blank=True)
    venta_asociada = models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos_caja")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="movimientos_caja")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimiento de Caja"
        verbose_name_plural = "Movimientos de Caja"
        ordering = ["-fecha"]
        indexes = [
            models.Index(fields=["caja_diaria", "tipo"], name="idx_mov_caja_tipo"),
            models.Index(fields=["venta_asociada"], name="idx_mov_venta"),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - ${self.monto_ars} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
