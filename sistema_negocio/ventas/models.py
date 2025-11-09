from decimal import Decimal

from django.conf import settings
from django.db import models

from inventario.models import ProductoVariante


class Venta(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        COBRADA = "cobrada", "Cobrada"
        ANULADA = "anulada", "Anulada"

    class MetodoPago(models.TextChoices):
        EFECTIVO = "efectivo", "Efectivo"
        TARJETA = "tarjeta", "Tarjeta"
        TRANSFERENCIA = "transferencia", "Transferencia"
        MIXTO = "mixto", "Mixto"

    numero = models.CharField(max_length=40, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_items = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    descuento_general = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, default=MetodoPago.EFECTIVO)
    nota = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.COBRADA)
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ventas_realizadas",
    )
    cliente_nombre = models.CharField(max_length=120, blank=True)
    cliente_documento = models.CharField(max_length=40, blank=True)
    comprobante_pdf = models.FileField(upload_to="comprobantes/", blank=True, null=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self) -> str:  # pragma: no cover - presentación simple
        return f"Venta {self.numero}"


class LineaVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="lineas", on_delete=models.CASCADE)
    variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_linea = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Línea de venta"
        verbose_name_plural = "Líneas de venta"

    def __str__(self) -> str:  # pragma: no cover - presentación simple
        return f"{self.descripcion} x{self.cantidad}"
