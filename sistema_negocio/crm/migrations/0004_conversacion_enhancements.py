from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_mensaje_archivo_mensaje_tipo_mensaje'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('color', models.CharField(default='#6366f1', help_text='Color HEX utilizado para renderizar la etiqueta', max_length=7)),
            ],
            options={
                'verbose_name': 'Etiqueta',
                'verbose_name_plural': 'Etiquetas',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='conversacion',
            name='prioridad',
            field=models.CharField(choices=[('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta'), ('urgent', 'Urgente')], default='medium', max_length=10),
        ),
        migrations.AddField(
            model_name='conversacion',
            name='sla_vencimiento',
            field=models.DateTimeField(blank=True, help_text='Fecha estimada para volver a contactar al cliente', null=True),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='metadata',
            field=models.JSONField(blank=True, help_text='Datos extra como IDs de mensaje o status de envío', null=True),
        ),
        migrations.AddField(
            model_name='conversacion',
            name='etiquetas',
            field=models.ManyToManyField(blank=True, help_text='Etiquetas utilizadas para segmentar la conversación', related_name='conversaciones', to='crm.etiqueta'),
        ),
        migrations.AlterField(
            model_name='conversacion',
            name='estado',
            field=models.CharField(choices=[('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'), ('Pendiente', 'Pendiente'), ('En seguimiento', 'En seguimiento')], default='Abierta', max_length=20),
        ),
    ]
