from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from crm.models import Cliente
from inventario.models import ProductoVariante


class Cupon(models.Model):
    """
    Modelo para cupones de descuento
    """
    TIPO_DESCUENTO_CHOICES = [
        ('PORCENTAJE', 'Porcentaje'),
        ('MONTO_FIJO', 'Monto Fijo'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código del Cupón')
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripción')
    tipo_descuento = models.CharField(
        max_length=20,
        choices=TIPO_DESCUENTO_CHOICES,
        default='PORCENTAJE',
        verbose_name='Tipo de Descuento'
    )
    valor_descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor del Descuento',
        help_text='Porcentaje (0-100) o monto fijo según el tipo'
    )
    monto_minimo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Monto Mínimo',
        help_text='Monto mínimo de compra para aplicar el cupón'
    )
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateTimeField(verbose_name='Fecha de Fin')
    usos_maximos = models.IntegerField(
        default=0,
        verbose_name='Usos Máximos',
        help_text='0 = ilimitado'
    )
    usos_actuales = models.IntegerField(default=0, verbose_name='Usos Actuales')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    solo_mayoristas = models.BooleanField(
        default=False,
        verbose_name='Solo Mayoristas',
        help_text='Si está marcado, solo usuarios mayoristas pueden usar este cupón'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
        ordering = ['-creado']
    
    def __str__(self):
        return f"{self.codigo} - {self.get_tipo_descuento_display()}"
    
    def es_valido(self, monto_total, usuario=None):
        """
        Verifica si el cupón es válido para el monto y usuario dados
        """
        from django.utils import timezone
        
        # Verificar si está activo
        if not self.activo:
            return False, 'El cupón no está activo'
        
        # Verificar fechas
        ahora = timezone.now()
        if ahora < self.fecha_inicio:
            return False, 'El cupón aún no está vigente'
        if ahora > self.fecha_fin:
            return False, 'El cupón ha expirado'
        
        # Verificar monto mínimo
        if monto_total < self.monto_minimo:
            return False, f'El monto mínimo es ${self.monto_minimo}'
        
        # Verificar usos máximos
        if self.usos_maximos > 0 and self.usos_actuales >= self.usos_maximos:
            return False, 'El cupón ha alcanzado su límite de usos'
        
        # Verificar si es solo para mayoristas
        if self.solo_mayoristas:
            if not usuario or not hasattr(usuario, 'perfil'):
                return False, 'Este cupón es solo para usuarios mayoristas'
            if usuario.perfil.tipo_usuario != 'MAYORISTA':
                return False, 'Este cupón es solo para usuarios mayoristas'
        
        return True, 'Válido'
    
    def calcular_descuento(self, monto_total):
        """
        Calcula el descuento a aplicar según el tipo
        """
        if self.tipo_descuento == 'PORCENTAJE':
            descuento = (monto_total * self.valor_descuento) / Decimal('100')
            # Limitar el descuento al monto total
            return min(descuento, monto_total)
        else:  # MONTO_FIJO
            return min(self.valor_descuento, monto_total)


class Venta(models.Model):
    class MetodoPago(models.TextChoices):
        # Nuevos valores normalizados
        EFECTIVO = "efectivo", "Efectivo"
        TRANSFERENCIA = "transferencia", "Transferencia"
        MERCADOPAGO_LINK = "mercadopago_link", "MercadoPago Link"
        TARJETA = "tarjeta", "Tarjeta"
        # Mantener valores antiguos para compatibilidad con datos existentes
        EFECTIVO_ARS = "EFECTIVO_ARS", "Efectivo ARS"
        EFECTIVO_USD = "EFECTIVO_USD", "Efectivo USD"

    class Status(models.TextChoices):
        PENDIENTE_PAGO = "PENDIENTE_PAGO", "Pendiente de pago"
        PAGADO = "PAGADO", "Pagado"
        PENDIENTE_ARMADO = "PENDIENTE_ARMADO", "Pendiente de armado"
        LISTO_RETIRAR = "LISTO_RETIRAR", "Listo para retirar"
        EN_CAMINO = "EN_CAMINO", "En camino / Enviado"
        COMPLETADO = "COMPLETADO", "Completado"
        CANCELADO = "CANCELADO", "Cancelado"
        DEVUELTO = "DEVUELTO", "Devuelto"
        # Mantener compatibilidad con estados antiguos
        PENDIENTE_ENVIO = "PENDIENTE_ENVIO", "Pendiente de envío"  # Deprecated, usar PENDIENTE_ARMADO
    
    class Origen(models.TextChoices):
        WEB = "web", "Web"
        LOCAL = "local", "Local"
        MAYORISTA = "mayorista", "Mayorista"
        # Mantener compatibilidad con valores antiguos (POS se mapea a LOCAL en la migración)
        POS = "POS", "POS"  # Mantener para compatibilidad con datos existentes
    
    class EstadoPago(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PAGADO = "pagado", "Pagado"
        ERROR = "error", "Error"
        CANCELADO = "cancelado", "Cancelado"
    
    class EstadoEntrega(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PREPARANDO = "preparando", "Preparando"
        ENVIADO = "enviado", "Enviado"
        ENTREGADO = "entregado", "Entregado"
        RETIRADO = "retirado", "Retirado"

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
    descuento_metodo_pago_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    impuestos_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_ars = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDIENTE_PAGO)
    origen = models.CharField(max_length=10, choices=Origen.choices, default=Origen.POS)
    motivo_cancelacion = models.TextField(blank=True, null=True, verbose_name='Motivo de Cancelación/Devolución')
    
    estado_pago = models.CharField(max_length=20, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE, verbose_name='Estado de Pago')
    estado_entrega = models.CharField(max_length=20, choices=EstadoEntrega.choices, default=EstadoEntrega.PENDIENTE, verbose_name='Estado de Entrega')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    # Cupón aplicado
    cupon = models.ForeignKey(
        'Cupon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas',
        verbose_name='Cupón Aplicado'
    )
    descuento_cupon_ars = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name='Descuento por Cupón'
    )
    
    nota = models.TextField(blank=True)
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas_realizadas",
    )

    # Campos para pago mixto
    es_pago_mixto = models.BooleanField(default=False, verbose_name="Es Pago Mixto")
    metodo_pago_2 = models.CharField(
        max_length=20,
        choices=MetodoPago.choices,
        blank=True,
        null=True,
        verbose_name="Método de Pago 2",
    )
    monto_pago_1 = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto Pagado con Método 1",
    )
    monto_pago_2 = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto Pagado con Método 2",
    )
    
    # URL del comprobante PDF en Bunny Storage
    comprobante_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="URL del Comprobante PDF",
        help_text="URL del PDF del comprobante almacenado en Bunny Storage"
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo al crear una nueva venta
            if self.origen == self.Origen.WEB:
                self.estado_pago = self.EstadoPago.PENDIENTE
                self.estado_entrega = self.EstadoEntrega.PENDIENTE
            elif self.origen == self.Origen.POS:
                self.estado_pago = self.EstadoPago.PAGADO
                self.estado_entrega = self.EstadoEntrega.RETIRADO
            elif self.origen == self.Origen.MAYORISTA:
                self.estado_pago = self.EstadoPago.PENDIENTE
                self.estado_entrega = self.EstadoEntrega.PENDIENTE
        super().save(*args, **kwargs)

    @property
    def cliente_id(self) -> int | None:
        return self.cliente.id if self.cliente else None

    @property
    def monto_total(self) -> Decimal:
        return self.total_ars

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.id} - {self.cliente_nombre or 'Sin cliente'} - ${self.total_ars}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    variante = models.ForeignKey(
        ProductoVariante, on_delete=models.SET_NULL, null=True, blank=True
    )
    descripcion = models.CharField(max_length=200)
    sku = models.CharField(max_length=60)
    cantidad = models.PositiveIntegerField()
    precio_unitario_ars_congelado = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    subtotal_ars = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"{self.venta.id} - {self.descripcion} x{self.cantidad}"


class HistorialEstadoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='historial_estados')
    estado_anterior = models.CharField(max_length=30, choices=Venta.Status.choices, null=True, blank=True)
    estado_nuevo = models.CharField(max_length=30, choices=Venta.Status.choices)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Historial de Estado de Venta'
        verbose_name_plural = 'Historiales de Estado de Venta'
        ordering = ['-creado']
        indexes = [
            models.Index(fields=['venta', '-creado'], name='ventas_hist_venta_i_65b196_idx'),
        ]
    
    def __str__(self):
        return f"{self.venta.id} - {self.estado_anterior} → {self.estado_nuevo}"


class CarritoRemoto(models.Model):
    """
    Carrito remoto compartido entre dispositivos para el POS
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrito_remoto'
    )
    items = models.JSONField(
        default=list,
        help_text='Lista de items en el carrito remoto'
    )
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carrito Remoto'
        verbose_name_plural = 'Carritos Remotos'
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class SolicitudImpresion(models.Model):
    """
    Solicitudes de impresión remota de comprobantes
    """
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PROCESANDO = 'PROCESANDO', 'Procesando'
        COMPLETADA = 'COMPLETADA', 'Completada'
        ERROR = 'ERROR', 'Error'
    
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='solicitudes_impresion'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_impresion'
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    error = models.TextField(
        blank=True,
        help_text='Mensaje de error si falla la impresión'
    )
    creado = models.DateTimeField(auto_now_add=True)
    procesado = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Solicitud de Impresión'
        verbose_name_plural = 'Solicitudes de Impresión'
        ordering = ['-creado']
    
    def __str__(self):
        return f"Solicitud {self.id} - {self.venta.id} - {self.get_estado_display()}"
