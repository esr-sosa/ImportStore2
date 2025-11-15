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
        help_text="Descripción breve de la ubicación para mostrar en mapas.",
    )
    google_maps_url = models.URLField(
        blank=True,
        help_text="URL completa de Google Maps al local.",
    )
    telefono_local = models.CharField(
        max_length=40,
        blank=True,
        help_text="Teléfono fijo del local.",
    )
    telefono_whatsapp = models.CharField(
        max_length=40,
        blank=True,
        help_text="Número de WhatsApp alternativo (si difiere del principal).",
    )
    correo_contacto = models.EmailField(
        blank=True,
        help_text="Correo de contacto principal.",
    )
    
    # Horarios
    horario_lunes_a_viernes = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ej: 9:00 - 18:00",
    )
    horario_sabados = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ej: 9:00 - 13:00",
    )
    horario_domingos = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ej: Cerrado o 10:00 - 14:00",
    )
    
    # Redes sociales
    instagram_principal = models.CharField(
        max_length=100,
        blank=True,
        help_text="Usuario de Instagram principal (sin @).",
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
        help_text="Ej: moto, cadetería, mensajería",
    )
    envios_nacionales = models.CharField(
        max_length=200,
        blank=True,
        help_text="Ej: correo, expreso",
    )
    costo_envio_local = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Costo de envío local.",
    )
    costo_envio_nacional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Costo de envío nacional base.",
    )
    politica_envio = models.TextField(
        blank=True,
        help_text="Política de envíos (texto breve).",
    )
    
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración del sistema"
        verbose_name_plural = "Configuración del sistema"

    def __str__(self) -> str:
        return "Configuración"

    def save(self, *args, **kwargs):
        self.pk = 1  # forzamos singleton
        super().save(*args, **kwargs)

    @classmethod
    def carga(cls) -> "ConfiguracionSistema":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def color(cls) -> str:
        return cls.carga().color_principal


class PreferenciaUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    usa_modo_oscuro = models.BooleanField(default=False)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover - presentación
        return f"Preferencias de {self.usuario}" if self.usuario_id else "Preferencias"
