from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='cliente_documento',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='venta',
            name='cliente_nombre',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='venta',
            name='comprobante_pdf',
            field=models.FileField(blank=True, null=True, upload_to='comprobantes/'),
        ),
        migrations.AddField(
            model_name='venta',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('cobrada', 'Cobrada'), ('anulada', 'Anulada')], default='cobrada', max_length=20),
        ),
        migrations.AddField(
            model_name='venta',
            name='vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas_realizadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
