from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0009_detalleiphone_variante_bridge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=40, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('descuento_items', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento_general', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('impuestos', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('metodo_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), ('mixto', 'Mixto')], default='efectivo', max_length=20)),
                ('nota', models.TextField(blank=True)),
            ],
            options={'ordering': ['-fecha']},
        ),
        migrations.CreateModel(
            name='LineaVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_linea', models.DecimalField(decimal_places=2, max_digits=12)),
                ('variante', models.ForeignKey(on_delete=models.deletion.PROTECT, to='inventario.productovariante')),
                ('venta', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='lineas', to='ventas.venta')),
            ],
            options={'verbose_name': 'Línea de venta', 'verbose_name_plural': 'Líneas de venta'},
        ),
    ]
