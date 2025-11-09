from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ConfiguracionSistema",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre_comercial", models.CharField(default="ImportStore", help_text="Nombre visible en cabecera, comprobantes y correos.", max_length=120)),
                ("lema", models.CharField(blank=True, help_text="Subtítulo o frase corta que acompaña al nombre.", max_length=180)),
                ("logo", models.ImageField(blank=True, help_text="Logotipo que se muestra en dashboards y documentos.", null=True, upload_to="branding/")),
                ("color_principal", models.CharField(default="#2563eb", help_text="Color primario en formato HEX (#RRGGBB).", max_length=7)),
                ("modo_oscuro_predeterminado", models.BooleanField(default=False, help_text="Habilita el modo oscuro como opción por defecto.")),
                ("mostrar_alertas", models.BooleanField(default=True, help_text="Muestra alertas de sistema (migraciones pendientes, integraciones).")),
                ("whatsapp_numero", models.CharField(blank=True, help_text="Número de WhatsApp corporativo que se muestra en la web.", max_length=30)),
                ("acceso_admin_habilitado", models.BooleanField(default=True, help_text="Mostrar acceso directo al panel de administración de Django.")),
                ("contacto_email", models.EmailField(blank=True, help_text="Correo de contacto o soporte.", max_length=254)),
                ("domicilio_comercial", models.CharField(blank=True, help_text="Dirección fiscal o comercial impresa en comprobantes.", max_length=200)),
                ("notas_sistema", models.TextField(blank=True, help_text="Notas internas, checklist o recordatorios de mantenimiento.")),
                ("dolar_blue_manual", models.DecimalField(blank=True, decimal_places=2, help_text="Valor de dólar blue manual cuando no se pueda consultar online.", max_digits=10, null=True)),
                ("ultima_actualizacion", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Configuración del sistema",
                "verbose_name_plural": "Configuración del sistema",
            },
        ),
        migrations.CreateModel(
            name="PreferenciaUsuario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("usa_modo_oscuro", models.BooleanField(default=False)),
                ("actualizado", models.DateTimeField(auto_now=True)),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
