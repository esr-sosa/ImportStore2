from decimal import Decimal
from django.conf import settings
from django.db import models


class ConfiguracionTienda(models.Model):
    nombre_tienda = models.CharField(max_length=150, default="ImportStore")
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    cuit = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    email_contacto = models.EmailField(blank=True)
    telefono_contacto = models.CharField(max_length=40, blank=True)
    garantia_dias_general = models.PositiveIntegerField(default=45, help_text="Días de garantía por defecto para todos los productos")
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración de tienda"
        verbose_name_plural = "Configuración de tienda"

    def __str__(self) -> str:
        return self.nombre_tienda or "Configuración de tienda"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def obtener_unica(cls) -> "ConfiguracionTienda":
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"nombre_tienda": "ImportStore"})
        return obj


class EscalaPrecioMayorista(models.Model):
    """
    Define rangos de cantidad y porcentajes de descuento para precios mayoristas
    """
    configuracion = models.ForeignKey(
        'ConfiguracionSistema',
        on_delete=models.CASCADE,
        related_name='escalas_precio',
        null=True,
        blank=True
    )
    cantidad_minima = models.IntegerField(
        verbose_name="Cantidad Mínima",
        help_text="Cantidad mínima de unidades para este rango"
    )
    cantidad_maxima = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Cantidad Máxima",
        help_text="Cantidad máxima de unidades para este rango (null = sin límite)"
    )
    porcentaje_descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Porcentaje de Descuento",
        help_text="Porcentaje de descuento a aplicar sobre el precio mayorista base (ej: 5.00 = 5%)"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aplicación (menor = primero)"
    )
    
    class Meta:
        verbose_name = "Escala de Precio Mayorista"
        verbose_name_plural = "Escalas de Precio Mayorista"
        ordering = ['orden', 'cantidad_minima']
    
    def __str__(self):
        if self.cantidad_maxima:
            return f"{self.cantidad_minima}-{self.cantidad_maxima} unidades: {self.porcentaje_descuento}% desc."
        return f"{self.cantidad_minima}+ unidades: {self.porcentaje_descuento}% desc."
    
    def aplicar_descuento(self, precio_base: Decimal, cantidad: int) -> Decimal:
        """
        Aplica el descuento de esta escala al precio base si la cantidad está en el rango
        """
        if not self.activo:
            return precio_base
        
        if cantidad < self.cantidad_minima:
            return precio_base
        
        if self.cantidad_maxima and cantidad > self.cantidad_maxima:
            return precio_base
        
        descuento = (precio_base * self.porcentaje_descuento) / Decimal('100')
        return precio_base - descuento


class ConfiguracionSistema(models.Model):
    nombre_comercial = models.CharField(
        max_length=120,
        default="ImportStore",
        help_text="Nombre visible en cabecera, comprobantes y correos.",
    )
    lema = models.CharField(
        max_length=180,
        blank=True,
        help_text="Subtítulo o frase corta que acompaña al nombre.",
    )
    logo = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Logotipo que se muestra en dashboards y documentos.",
    )
    color_principal = models.CharField(
        max_length=7,
        default="#2563eb",
        help_text="Color primario en formato HEX (#RRGGBB).",
    )
    modo_oscuro_predeterminado = models.BooleanField(
        default=False,
        help_text="Habilita el modo oscuro como opción por defecto.",
    )
    mostrar_alertas = models.BooleanField(
        default=True,
        help_text="Muestra alertas de sistema (migraciones pendientes, integraciones).",
    )
    whatsapp_numero = models.CharField(
        max_length=30,
        blank=True,
        help_text="Número de WhatsApp corporativo que se muestra en la web.",
    )
    acceso_admin_habilitado = models.BooleanField(
        default=True,
        help_text="Mostrar acceso directo al panel de administración de Django.",
    )
    contacto_email = models.EmailField(
        blank=True,
        help_text="Correo de contacto o soporte.",
    )
    domicilio_comercial = models.CharField(
        max_length=200,
        blank=True,
        help_text="Dirección fiscal o comercial impresa en comprobantes.",
    )
    notas_sistema = models.TextField(
        blank=True,
        help_text="Notas internas, checklist o recordatorios de mantenimiento.",
    )
    dolar_blue_manual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Valor de dólar blue manual cuando no se pueda consultar online.",
    )
    
    # --- NUEVOS CAMPOS PARA IA CRM ---
    # Datos del local extendidos
    nombre_local = models.CharField(
        max_length=200,
        blank=True,
        help_text="Nombre del local físico (puede diferir del nombre comercial).",
    )
    ubicacion_mapa = models.CharField(
        max_length=255,
        blank=True,
        help_text="URL de Google Maps o coordenadas del local.",
    )
    horarios_apertura = models.CharField(
        max_length=100,
        blank=True,
        help_text="Horarios de atención (ej: 'Lun-Vie 9-18hs').",
    )
    instagram_personal = models.CharField(
        max_length=100,
        blank=True,
        help_text="Usuario de Instagram personal (sin @).",
    )
    instagram_secundario = models.CharField(
        max_length=100,
        blank=True,
        help_text="Usuario de Instagram secundario (sin @).",
    )
    instagram_empresa = models.CharField(
        max_length=100,
        blank=True,
        help_text="Usuario de Instagram de la empresa (sin @).",
    )
    tiktok = models.CharField(
        max_length=100,
        blank=True,
        help_text="Usuario de TikTok (sin @).",
    )
    facebook = models.URLField(
        blank=True,
        help_text="URL de la página de Facebook.",
    )
    whatsapp_alternativo = models.CharField(
        max_length=40,
        blank=True,
        help_text="Número de WhatsApp alternativo para mostrar.",
    )
    
    # Métodos de pago
    pago_efectivo_local = models.BooleanField(
        default=True,
        help_text="Acepta pago en efectivo en el local.",
    )
    pago_efectivo_retiro = models.BooleanField(
        default=True,
        help_text="Acepta pago en efectivo al retirar.",
    )
    pago_transferencia = models.BooleanField(
        default=True,
        help_text="Acepta transferencia bancaria.",
    )
    transferencia_alias = models.CharField(
        max_length=50,
        blank=True,
        help_text="Alias de transferencia bancaria.",
    )
    transferencia_cbu = models.CharField(
        max_length=22,
        blank=True,
        help_text="CBU para transferencias.",
    )
    pago_tarjeta = models.BooleanField(
        default=True,
        help_text="Acepta tarjetas de crédito y débito.",
    )
    pago_online = models.BooleanField(
        default=False,
        help_text="Acepta pago online.",
    )
    pago_online_link = models.URLField(
        blank=True,
        help_text="Link o QR para pago online.",
    )
    descuento_efectivo_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        blank=True,
        help_text="Porcentaje de descuento por pago en efectivo o transferencia.",
    )
    
    # Envíos
    envios_disponibles = models.BooleanField(
        default=True,
        help_text="Realiza envíos.",
    )
    envios_locales = models.CharField(
        max_length=200,
        blank=True,
        help_text="Zonas de envío local (barrios, ciudades).",
    )
    envios_nacionales = models.BooleanField(
        default=False,
        help_text="Realiza envíos a todo el país.",
    )
    costo_envio_local = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Costo de envío local (opcional).",
    )
    costo_envio_nacional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Costo de envío nacional (opcional).",
    )
    
    # Configuración de precios mayoristas por escala
    precios_escala_activos = models.BooleanField(
        default=False,
        verbose_name="Activar Precios por Escala",
        help_text="Si está activado, se aplicarán descuentos por cantidad a los precios mayoristas"
    )
    
    # Configuración de compra mínima mayorista
    monto_minimo_mayorista = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name="Monto Mínimo Mayorista",
        help_text="Monto mínimo de compra para usuarios mayoristas"
    )
    cantidad_minima_mayorista = models.IntegerField(
        default=0,
        verbose_name="Cantidad Mínima Mayorista",
        help_text="Cantidad mínima de unidades para usuarios mayoristas"
    )

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuración del Sistema"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def obtener_unica(cls) -> "ConfiguracionSistema":
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"nombre_comercial": "ImportStore"})
        return obj
    
    def obtener_precio_con_escala(self, precio_base: Decimal, cantidad: int) -> Decimal:
        """
        Calcula el precio aplicando las escalas de descuento si están activas
        """
        if not self.precios_escala_activos:
            return precio_base
        
        escalas = self.escalas_precio.filter(activo=True).order_by('orden', 'cantidad_minima')
        
        for escala in escalas:
            if cantidad >= escala.cantidad_minima:
                if escala.cantidad_maxima is None or cantidad <= escala.cantidad_maxima:
                    return escala.aplicar_descuento(precio_base, cantidad)
        
        return precio_base


class PreferenciaUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    usa_modo_oscuro = models.BooleanField(default=False)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Preferencias de {self.usuario}" if self.usuario_id else "Preferencias"
