from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from crm.models import Cliente
from inventario.models import ProductoVariante


class Venta(models.Model):
    class MetodoPago(models.TextChoices):
        EFECTIVO_ARS = "EFECTIVO_ARS", "Efectivo ARS"
        EFECTIVO_USD = "EFECTIVO_USD", "Efectivo USD"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"
        TARJETA = "TARJETA", "Tarjeta"

    class Status(models.TextChoices):
        PENDIENTE_PAGO = "PENDIENTE_PAGO", "Pendiente de pago"
        PAGADO = "PAGADO", "Pagado"
        PENDIENTE_ENVIO = "PENDIENTE_ENVIO", "Pendiente de envío"
        COMPLETADO = "COMPLETADO", "Completado"
        CANCELADO = "CANCELADO", "Cancelado"

    id = models.CharField(
        primary_key=True,
        max_length=20,
        help_text="Identificador único de la venta / número de orden.",
    )
    fecha = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    cliente_nombre = models.CharField(max_length=120, blank=True)
    cliente_documento = models.CharField(max_length=40, blank=True)
    subtotal_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    descuento_total_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    impuestos_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDIENTE_PAGO)
    nota = models.TextField(blank=True)
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ventas_registradas",
    )
    comprobante_pdf = models.FileField(upload_to="comprobantes/", blank=True, null=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Campos para pago mixto
    es_pago_mixto = models.BooleanField(default=False, help_text="Indica si la venta tiene múltiples métodos de pago")
    metodo_pago_2 = models.CharField(max_length=20, choices=MetodoPago.choices, blank=True, null=True, help_text="Segundo método de pago si es pago mixto")
    monto_pago_1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Monto del primer método de pago")
    monto_pago_2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Monto del segundo método de pago (restante)")

    class Meta:
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"Venta {self.id}"

    @property
    def saldo_pendiente(self) -> Decimal:
        return Decimal("0") if self.status in {self.Status.PAGADO, self.Status.COMPLETADO} else self.total_ars


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles", on_delete=models.CASCADE)
    variante = models.ForeignKey(ProductoVariante, on_delete=models.SET_NULL, related_name="detalles_venta", null=True, blank=True, help_text="Null para productos varios o productos eliminados")
    sku = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    precio_unitario_ars_congelado = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal_ars = models.DecimalField(max_digits=12, decimal_places=2)
    # Campos para conversión USD -> ARS (solo para iPhones)
    precio_unitario_usd_original = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Precio original en USD si fue convertido")
    tipo_cambio_usado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Tipo de cambio usado para la conversión")

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

    def __str__(self) -> str:
        return f"{self.descripcion} x{self.cantidad}"


class CarritoRemoto(models.Model):
    """Carrito remoto compartido por usuario (para sincronización entre dispositivos)."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carrito_remoto"
    )
    items = models.JSONField(default=list, help_text="Lista de items en el carrito remoto")
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Carrito Remoto"
        verbose_name_plural = "Carritos Remotos"
    
    def __str__(self) -> str:
        total_items = sum(int(item.get("cantidad", 1)) for item in self.items if isinstance(item, dict))
        return f"Carrito de {self.usuario.username} ({total_items} items)"


class SolicitudImpresion(models.Model):
    """Cola de solicitudes de impresión remota (desde celular hacia PC)."""
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PROCESANDO = "PROCESANDO", "Procesando"
        COMPLETADA = "COMPLETADA", "Completada"
        ERROR = "ERROR", "Error"
    
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="solicitudes_impresion")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitudes_impresion"
    )
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    error = models.TextField(blank=True, help_text="Mensaje de error si falla la impresión")
    creado = models.DateTimeField(auto_now_add=True)
    procesado = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-creado"]
        verbose_name = "Solicitud de Impresión"
        verbose_name_plural = "Solicitudes de Impresión"
    
    def __str__(self) -> str:
        return f"Impresión {self.venta.id} - {self.get_estado_display()}"
