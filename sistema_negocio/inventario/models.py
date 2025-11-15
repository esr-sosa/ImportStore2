import os
from uuid import uuid4
from decimal import Decimal

from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=120)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategorias",
        verbose_name="Categoría padre",
        help_text="Seleccioná la categoría padre si esta es una subcategoría"
    )
    descripcion = models.TextField(blank=True)
    garantia_dias = models.PositiveIntegerField(null=True, blank=True, help_text="Días de garantía específicos para esta categoría. Si está vacío, se usa la garantía general.")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["parent__nombre", "nombre"]
        indexes = [
            models.Index(fields=["nombre"], name="idx_categoria_nombre"),
            models.Index(fields=["parent"], name="idx_categoria_parent"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["nombre", "parent"], name="unique_categoria_nombre_parent"),
        ]

    def __str__(self):
        if self.parent:
            return f"{self.parent.nombre} > {self.nombre}"
        return self.nombre
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo con la jerarquía completa."""
        if self.parent:
            return f"{self.parent.nombre_completo} > {self.nombre}"
        return self.nombre
    
    @property
    def es_subcategoria(self):
        """Retorna True si esta categoría es una subcategoría."""
        return self.parent is not None
    
    def get_nivel(self):
        """Retorna el nivel de profundidad en la jerarquía (0 = categoría principal)."""
        nivel = 0
        categoria = self.parent
        while categoria:
            nivel += 1
            categoria = categoria.parent
        return nivel


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


def _producto_imagen_upload_to(instance, filename: str) -> str:
    base, ext = os.path.splitext(filename or "")
    ext = ext or ".png"
    unique = uuid4().hex
    return os.path.join("productos", str(instance.producto_id or "tmp"), f"{unique}{ext}")


class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=_producto_imagen_upload_to)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de producto"

    def __str__(self) -> str:
        return f"Imagen {self.pk} de {self.producto.nombre}"


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
        return " / ".join(partes) if partes else ""

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
        # NOTA: Antes de activar este UniqueConstraint en una migración, verificá duplicados.
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


class PlanCanjeConfig(models.Model):
    """Configuración de valores base para el Plan Canje por modelo y capacidad de iPhone."""
    
    class EstadoFisico(models.TextChoices):
        EXCELENTE = "excelente", "Excelente"
        BUENO = "bueno", "Bueno"
        REGULAR = "regular", "Regular"
    
    modelo_iphone = models.CharField(
        max_length=100,
        help_text="Modelo del iPhone (ej: iPhone 11, iPhone 13 Pro Max)"
    )
    capacidad = models.CharField(
        max_length=20,
        help_text="Capacidad de almacenamiento (ej: 128GB, 256GB, 512GB, 1TB)"
    )
    valor_base_canje_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Valor base del canje en USD para este modelo y capacidad"
    )
    
    # Descuentos por batería (JSON: {"<80": 0.15, "80-90": 0.10, ">90": 0.0})
    descuentos_bateria = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por salud de batería. Ej: {"<80": 0.15, "80-90": 0.10, ">90": 0.0}'
    )
    
    # Descuentos por estado físico (JSON: {"excelente": 0.0, "bueno": 0.05, "regular": 0.15})
    descuentos_estado = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por estado físico. Ej: {"excelente": 0.0, "bueno": 0.05, "regular": 0.15}'
    )
    
    # Descuentos por accesorios faltantes (JSON: {"sin_caja": 0.02})
    descuentos_accesorios = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por accesorios faltantes. Ej: {"sin_caja": 0.02}'
    )
    
    # Descuentos adicionales por estado de componentes
    descuentos_pantalla = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por estado de pantalla. Ej: {"perfecta": 0.0, "rayas_menores": 0.03, "rayas_visibles": 0.08, "grieta": 0.15}'
    )
    descuentos_marco = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por estado del marco. Ej: {"perfecto": 0.0, "arañazos": 0.02, "golpes": 0.05, "deformado": 0.10}'
    )
    descuentos_botones = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por estado de botones. Ej: {"todos_funcionan": 0.0, "alguno_no_funciona": 0.05, "varios_no_funcionan": 0.10}'
    )
    descuentos_camara = models.JSONField(
        default=dict,
        blank=True,
        help_text='Descuentos por estado de cámara. Ej: {"perfecta": 0.0, "rayas_menores": 0.02, "rayas_visibles": 0.05, "rota": 0.15}'
    )
    
    # Guías de ayuda para el admin
    guia_estado_excelente = models.TextField(
        blank=True,
        help_text="Guía: ¿Cuándo considerar 'Excelente'? (ej: Sin rayas, sin golpes visibles, pantalla perfecta, todos los botones funcionan)"
    )
    guia_estado_bueno = models.TextField(
        blank=True,
        help_text="Guía: ¿Cuándo considerar 'Bueno'? (ej: 1-2 rayitas menores, pequeños arañazos en marco, pantalla con rayas menores)"
    )
    guia_estado_regular = models.TextField(
        blank=True,
        help_text="Guía: ¿Cuándo considerar 'Regular'? (ej: Múltiples rayas, golpes visibles, pantalla con daños menores, algún botón no funciona)"
    )
    
    activo = models.BooleanField(
        default=True,
        help_text="Si está inactivo, no aparecerá en las opciones de canje"
    )
    creado = models.DateTimeField(default=timezone.now, editable=False)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración Plan Canje"
        verbose_name_plural = "Configuraciones Plan Canje"
        ordering = ["modelo_iphone", "capacidad"]
        unique_together = [["modelo_iphone", "capacidad"]]
        indexes = [
            models.Index(fields=["modelo_iphone", "capacidad"], name="idx_plan_canje_modelo_cap"),
            models.Index(fields=["activo"], name="idx_plan_canje_activo"),
        ]
    
    def __str__(self):
        return f"{self.modelo_iphone} {self.capacidad} - ${self.valor_base_canje_usd} USD"


class PlanCanjeTransaccion(models.Model):
    """Registro de transacciones de Plan Canje realizadas."""
    
    class EstadoFisico(models.TextChoices):
        EXCELENTE = "excelente", "Excelente"
        BUENO = "bueno", "Bueno"
        REGULAR = "regular", "Regular"
    
    fecha = models.DateTimeField(default=timezone.now)
    
    # Cliente (opcional)
    cliente = models.ForeignKey(
        'crm.Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="canjes_realizados"
    )
    cliente_nombre = models.CharField(max_length=200, blank=True)
    cliente_documento = models.CharField(max_length=40, blank=True)
    
    # iPhone recibido (el usado que trae el cliente)
    iphone_recibido_modelo = models.CharField(max_length=100)
    iphone_recibido_capacidad = models.CharField(max_length=20)
    iphone_recibido_color = models.CharField(max_length=50, blank=True)
    iphone_recibido_imei = models.CharField(max_length=15, blank=True)
    iphone_recibido_bateria = models.PositiveIntegerField(help_text="Salud de batería (1-100)")
    iphone_recibido_estado = models.CharField(max_length=20, choices=EstadoFisico.choices)
    iphone_recibido_accesorios = models.JSONField(
        default=dict,
        blank=True,
        help_text="Accesorios incluidos. Ej: {'caja': True}"
    )
    iphone_recibido_estado_pantalla = models.CharField(max_length=50, blank=True, help_text="Estado de la pantalla (perfecta, rayas_menores, rayas_visibles, grieta)")
    iphone_recibido_estado_marco = models.CharField(max_length=50, blank=True, help_text="Estado del marco (perfecto, arañazos, golpes, deformado)")
    iphone_recibido_estado_botones = models.CharField(max_length=50, blank=True, help_text="Estado de botones (todos_funcionan, alguno_no_funciona, varios_no_funcionan)")
    iphone_recibido_estado_camara = models.CharField(max_length=50, blank=True, help_text="Estado de cámara (perfecta, rayas_menores, rayas_visibles, rota)")
    iphone_recibido_observaciones = models.TextField(blank=True)
    
    # Valores calculados
    valor_base_usd = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_bateria_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_estado_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_accesorios_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_pantalla_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_marco_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_botones_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_camara_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_calculado_usd = models.DecimalField(max_digits=10, decimal_places=2)
    valor_calculado_ars = models.DecimalField(max_digits=12, decimal_places=2)
    ajuste_manual_ars = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Ajuste manual aplicado por el admin (puede ser positivo o negativo)"
    )
    
    # iPhone entregado (el nuevo que se vende)
    iphone_entregado = models.ForeignKey(
        ProductoVariante,
        on_delete=models.SET_NULL,
        null=True,
        related_name="canjes_entregados"
    )
    valor_iphone_entregado_ars = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Diferencia final
    diferencia_ars = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Diferencia que debe pagar el cliente (precio nuevo - valor usado + ajuste)"
    )
    
    # Relaciones
    venta_asociada = models.ForeignKey(
        'ventas.Venta',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="canje_asociado"
    )
    detalle_iphone_recibido = models.ForeignKey(
        DetalleIphone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transaccion_canje"
    )
    
    # Usuario que realizó el canje
    vendedor = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="canjes_registrados"
    )
    
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(default=timezone.now, editable=False)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Transacción Plan Canje"
        verbose_name_plural = "Transacciones Plan Canje"
        ordering = ["-fecha"]
        indexes = [
            models.Index(fields=["fecha"], name="idx_canje_fecha"),
            models.Index(fields=["cliente"], name="idx_canje_cliente"),
        ]
    
    def __str__(self):
        return f"Canje {self.id} - {self.iphone_recibido_modelo} por {self.iphone_entregado.producto.nombre if self.iphone_entregado else 'N/A'} - {self.fecha.strftime('%d/%m/%Y')}"