from decimal import Decimal

from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    garantia_dias = models.PositiveIntegerField(null=True, blank=True, help_text="Días de garantía específicos para esta categoría. Si está vacío, se usa la garantía general.")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=["nombre"], name="idx_categoria_nombre"),
        ]

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=["activo"], name="idx_proveedor_activo"),
            models.Index(fields=["nombre"], name="idx_proveedor_nombre"),
        ]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=180)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos"
    )
    descripcion = models.TextField(blank=True)

    # Campos que ya estás usando en tu DB:
    activo = models.BooleanField(default=True)
    estado = models.CharField(max_length=20, default="ACTIVO", blank=True, help_text="Estado del producto en la base de datos")
    codigo_barras = models.CharField(max_length=64, blank=True, null=True)
    # Guardás un path/ruta (VARCHAR en DB). Lo dejo CharField para compatibilidad.
    imagen_codigo_barras = models.CharField(max_length=255, blank=True, null=True)

    creado = models.DateTimeField(default=timezone.now, editable=False)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-actualizado", "nombre"]
        indexes = [
            models.Index(fields=["activo"], name="idx_producto_activo"),
            models.Index(fields=["nombre"], name="idx_producto_nombre"),
            models.Index(fields=["codigo_barras"], name="idx_producto_cod_barras"),
        ]

    def __str__(self):
        return self.nombre


class ProductoVariante(models.Model):
    """
    Variante de un producto (por ejemplo: color, capacidad, tamaño).
    """
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="variantes"
    )
    sku = models.CharField(max_length=64, unique=True)
    nombre_variante = models.CharField(max_length=200, blank=True, default="", help_text="Nombre descriptivo de la variante")
    codigo_barras = models.CharField(max_length=64, blank=True, null=True, help_text="Código de barras EAN/UPC")
    qr_code = models.CharField(max_length=255, blank=True, null=True, help_text="Código QR (URL o texto)")
    atributo_1 = models.CharField(max_length=120, blank=True)  # ej: color
    atributo_2 = models.CharField(max_length=120, blank=True)  # ej: capacidad/tamaño
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(default=timezone.now, editable=False)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Producto"
        ordering = ["producto__nombre", "sku"]
        indexes = [
            models.Index(fields=["sku"], name="idx_var_sku"),
            models.Index(fields=["activo"], name="idx_var_activo"),
            models.Index(fields=["stock_actual"], name="idx_var_stock"),
        ]

    def __str__(self):
        etiqueta = self.producto.nombre if self.producto_id else "Producto"
        detalles = " / ".join([x for x in [self.atributo_1, self.atributo_2] if x])
        return f"{etiqueta} [{self.sku}]" + (f" — {detalles}" if detalles else "")

    @property
    def bajo_stock(self):
        return self.stock_minimo and self.stock_actual <= self.stock_minimo

    @property
    def atributos_display(self):
        partes = [parte for parte in [self.atributo_1, self.atributo_2] if parte]
        return " / ".join(partes) if partes else "Sin especificar"

    def precio_activo(self, tipo: str, moneda: str):
        return (
            self.precios.filter(tipo=tipo, moneda=moneda, activo=True)
            .order_by("-actualizado")
            .first()
        )

    def valor_estimado(self, tipo: str, moneda: str) -> Decimal:
        precio = self.precio_activo(tipo=tipo, moneda=moneda)
        if not precio:
            return Decimal("0")
        return Decimal(precio.precio) * Decimal(self.stock_actual or 0)


class Precio(models.Model):
    """
    Precio asociado a una variante.
    - tipo: MINORISTA / MAYORISTA (podés agregar otros)
    - moneda: ARS / USD (extensible)
    """
    class Tipo(models.TextChoices):
        MINORISTA = "MINORISTA", "Minorista"
        MAYORISTA = "MAYORISTA", "Mayorista"

    class Moneda(models.TextChoices):
        ARS = "ARS", "ARS"
        USD = "USD", "USD"

    variante = models.ForeignKey(
        ProductoVariante, on_delete=models.CASCADE, related_name="precios"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.MINORISTA)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=10, choices=Moneda.choices, default=Moneda.USD)
    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(default=timezone.now, editable=False)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"
        ordering = ["variante__sku", "tipo", "moneda"]
        indexes = [
            models.Index(fields=["activo"], name="idx_precio_activo"),
            models.Index(fields=["variante", "tipo", "moneda"], name="idx_precio_var_tipo_mon"),
        ]
        # ⚠️ Antes de activar este UniqueConstraint en una migración, verificá duplicados.
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["variante", "tipo", "moneda"],
        #         name="uniq_precio_var_tipo_moneda",
        #     )
        # ]

    def __str__(self):
        return f"{self.variante.sku} — {self.tipo} {self.precio} {self.moneda}"


class DetalleIphone(models.Model):
    variante = models.OneToOneField(
        ProductoVariante,
        on_delete=models.CASCADE,
        related_name="detalle_iphone",
        blank=True,
        null=True,
        help_text="Variante asociada al equipo dentro del inventario",
    )
    imei = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        help_text="IMEI único del equipo",
    )
    salud_bateria = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Porcentaje de salud de la batería (1-100)",
    )
    fallas_detectadas = models.TextField(
        blank=True,
        help_text="Observaciones o detalles a tener en cuenta",
    )
    es_plan_canje = models.BooleanField(
        default=False,
        help_text="Indica si fue recibido como parte de un plan canje",
    )
    costo_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Costo de adquisición en USD",
    )
    precio_venta_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio minorista en USD",
    )
    precio_oferta_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Precio promocional en USD",
    )
    notas = models.TextField(
        blank=True,
        help_text="Notas internas adicionales",
    )
    foto = models.ImageField(
        upload_to="iphones/",
        blank=True,
        null=True,
        help_text="Fotografía principal del equipo",
    )
    creado = models.DateTimeField(default=timezone.now, editable=False)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Detalle de iPhone"
        verbose_name_plural = "Detalles de iPhone"
        ordering = ["-actualizado"]

    def __str__(self):
        nombre = self.variante.producto.nombre if self.variante_id else "iPhone"
        atributos = self.variante.atributos_display if self.variante_id else ""
        return f"{nombre} {atributos}".strip()
