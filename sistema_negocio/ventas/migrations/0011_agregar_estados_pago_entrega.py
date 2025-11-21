# Generated manually for new estado_pago and estado_entrega fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0010_agregar_estados_y_origen'),
    ]

    operations = [
        # Actualizar campo origen para incluir mayorista
        migrations.AlterField(
            model_name='venta',
            name='origen',
            field=models.CharField(
                choices=[
                    ('web', 'Web'),
                    ('local', 'Local'),
                    ('mayorista', 'Mayorista'),
                ],
                default='local',
                help_text='Origen de la venta: web, local o mayorista',
                max_length=20
            ),
        ),
        # Agregar campo estado_pago
        migrations.AddField(
            model_name='venta',
            name='estado_pago',
            field=models.CharField(
                choices=[
                    ('pendiente', 'Pendiente'),
                    ('pagado', 'Pagado'),
                    ('error', 'Error'),
                    ('cancelado', 'Cancelado'),
                ],
                default='pendiente',
                help_text='Estado del pago de la venta',
                max_length=20,
                verbose_name='Estado de Pago'
            ),
        ),
        # Agregar campo estado_entrega
        migrations.AddField(
            model_name='venta',
            name='estado_entrega',
            field=models.CharField(
                choices=[
                    ('pendiente', 'Pendiente'),
                    ('preparando', 'Preparando'),
                    ('enviado', 'Enviado'),
                    ('entregado', 'Entregado'),
                    ('retirado', 'Retirado'),
                ],
                default='pendiente',
                help_text='Estado de entrega/preparación de la venta',
                max_length=20,
                verbose_name='Estado de Entrega'
            ),
        ),
        # Agregar campo observaciones
        migrations.AddField(
            model_name='venta',
            name='observaciones',
            field=models.TextField(
                blank=True,
                help_text='Observaciones adicionales sobre la venta',
                null=True
            ),
        ),
        # Actualizar método de pago para incluir nuevos valores
        migrations.AlterField(
            model_name='venta',
            name='metodo_pago',
            field=models.CharField(
                choices=[
                    ('efectivo', 'Efectivo'),
                    ('transferencia', 'Transferencia'),
                    ('mercadopago_link', 'MercadoPago Link'),
                    ('tarjeta', 'Tarjeta'),
                ],
                max_length=20
            ),
        ),
    ]

