# Django 5.2.x – Migración “anti-fallas”
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def _create_indexes(apps, schema_editor):
    """Recrea los índices heredados únicamente cuando la base es MySQL."""

    connection = schema_editor.connection
    if connection.vendor != "mysql":
        return

    statements = (
        "CREATE INDEX IF NOT EXISTS idx_categoria_nombre  ON inventario_categoria (nombre);",
        "CREATE INDEX IF NOT EXISTS idx_precio_activo     ON inventario_precio (activo);",
        "CREATE INDEX IF NOT EXISTS idx_precio_var_tipo_mon ON inventario_precio (variante_id, tipo, moneda);",
        "CREATE INDEX IF NOT EXISTS idx_producto_activo   ON inventario_producto (activo);",
        "CREATE INDEX IF NOT EXISTS idx_producto_nombre   ON inventario_producto (nombre);",
        "CREATE INDEX IF NOT EXISTS idx_var_activo        ON inventario_productovariante (activo);",
        "CREATE INDEX IF NOT EXISTS idx_var_stock         ON inventario_productovariante (stock_actual);",
        "CREATE INDEX IF NOT EXISTS idx_proveedor_activo  ON inventario_proveedor (activo);",
        "CREATE INDEX IF NOT EXISTS idx_proveedor_nombre  ON inventario_proveedor (nombre);",
    )

    with connection.cursor() as cursor:
        for statement in statements:
            try:
                cursor.execute(statement)
            except Exception:
                # Si el índice ya existe o la versión no soporta IF NOT EXISTS,
                # simplemente continuamos sin interrumpir la migración.
                continue

class Migration(migrations.Migration):
    """
    Objetivo:
    - Reemplazar la migración conflictiva 0006_remove_detalleiphone_variante_and_more
      para que no intente eliminar/crear columnas que ya no cuadran con la DB real.
    - Ajustar SOLO el estado (ORM) a la estructura existente en MySQL.
    - Crear índices de forma segura (IF NOT EXISTS).
    """

    # Muy importante: esto hace que Django considere esta migración
    # como el reemplazo de la 0006 conflictiva, evitando que se ejecute.
    replaces = [
        ('inventario', '0006_remove_detalleiphone_variante_and_more'),
    ]

    # Colócala DESPUÉS de la 0006 que ya figura aplicada en tu tabla django_migrations
    # (según tu dump): 0006_remove_producto_activo_remove_producto_codigo_barras_and_more
    dependencies = [
        # Debe apuntar al mismo nodo que la migración reemplazada para que
        # Django pueda trazar correctamente el grafo de dependencias.
        ('inventario', '0005_remove_detalleiphone_fecha_compra_and_more'),
    ]

    operations = [

        # ------------------------------------------------------------
        # 1) DetalleIphone: sólo estado (no tocar la DB física)
        #    - Quitamos la relación y el modelo del estado para que el ORM no lo use.
        # ------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Si en tu models.py ya no existe DetalleIphone o su FK 'variante',
                # esto asegura el estado. (No ejecuta SQL.)
                migrations.RemoveField(
                    model_name='detalleiphone',
                    name='variante',
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='DetalleIphone'),
            ],
            database_operations=[],
        ),

        # ------------------------------------------------------------
        # 2) Opciones de modelos (solo estado)
        # ------------------------------------------------------------
        migrations.AlterModelOptions(
            name='categoria',
            options={'ordering': ['nombre'], 'verbose_name': 'Categoría', 'verbose_name_plural': 'Categorías'},
        ),
        migrations.AlterModelOptions(
            name='precio',
            options={'ordering': ['variante__sku', 'tipo', 'moneda'], 'verbose_name': 'Precio', 'verbose_name_plural': 'Precios'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['-actualizado', 'nombre']},
        ),
        migrations.AlterModelOptions(
            name='productovariante',
            options={'ordering': ['producto__nombre', 'sku'], 'verbose_name': 'Variante de Producto', 'verbose_name_plural': 'Variantes de Producto'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'ordering': ['nombre']},
        ),

        # ------------------------------------------------------------
        # 3) unique_together a vacío (solo estado)
        #    * En DB sigue tu UNIQUE viejo para no romper datos ahora mismo.
        # ------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterUniqueTogether(name='precio', unique_together=set()),
                migrations.AlterUniqueTogether(name='productovariante', unique_together=set()),
            ],
            database_operations=[],
        ),

        # ------------------------------------------------------------
        # 4) Eliminaciones problemáticas: SOLO ESTADO (evita "Can't DROP ...")
        #    Estas columnas NO existen en tu DB actual.
        # ------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name='producto', name='fecha_creacion'),
                migrations.RemoveField(model_name='producto', name='imagen'),
                migrations.RemoveField(model_name='proveedor', name='contacto'),
                migrations.RemoveField(model_name='proveedor', name='fecha_creacion'),
            ],
            database_operations=[],
        ),

        # ------------------------------------------------------------
        # 5) Campos que YA existen en tu DB: los re-declaramos SOLO EN ESTADO
        #    para alinear el ORM y evitar "Duplicate column name …"
        #    (ver dump: inventario_categoria.descripcion, inventario_precio.*, etc.)
        # ------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # inventario_categoria.descripcion (ya existe como LONGTEXT NOT NULL)
                migrations.AddField(
                    model_name='categoria',
                    name='descripcion',
                    field=models.TextField(blank=True, default=""),
                ),
                # precio: activo/actualizado/creado/precio/tipo/moneda ya están en tu DB
                migrations.AddField(model_name='precio', name='activo',      field=models.BooleanField(default=True)),
                migrations.AddField(model_name='precio', name='actualizado',  field=models.DateTimeField(auto_now=True)),
                migrations.AddField(model_name='precio', name='creado',       field=models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                migrations.AddField(model_name='precio', name='precio',       field=models.DecimalField(max_digits=12, decimal_places=2, default=0)),
                migrations.AddField(
                    model_name='precio',
                    name='tipo',
                    field=models.CharField(max_length=20, choices=[('MINORISTA', 'Minorista'), ('MAYORISTA', 'Mayorista')], default='MINORISTA'),
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # producto.creado ya existe en DB
                migrations.AddField(model_name='producto', name='creado', field=models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                # variante: estos campos existen en DB
                migrations.AddField(model_name='productovariante', name='activo',        field=models.BooleanField(default=True)),
                migrations.AddField(model_name='productovariante', name='actualizado',    field=models.DateTimeField(auto_now=True)),
                migrations.AddField(model_name='productovariante', name='atributo_1',     field=models.CharField(max_length=120, blank=True)),
                migrations.AddField(model_name='productovariante', name='atributo_2',     field=models.CharField(max_length=120, blank=True)),
                migrations.AddField(model_name='productovariante', name='creado',         field=models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                # sku: en DB existe y es UNIQUE pero permite NULL; mantenemos null/blank para no romper datos existentes.
                migrations.AddField(
                    model_name='productovariante',
                    name='sku',
                    field=models.CharField(max_length=100, unique=True, null=True, blank=True),
                ),
                migrations.AddField(model_name='productovariante', name='stock_actual',   field=models.IntegerField(default=0)),
                migrations.AddField(model_name='productovariante', name='stock_minimo',   field=models.IntegerField(default=0)),
                # proveedor.activo ya existe en DB
                migrations.AddField(model_name='proveedor', name='activo', field=models.BooleanField(default=True)),
            ],
            database_operations=[],
        ),

        # ------------------------------------------------------------
        # 6) Alteraciones de campos: SOLO ESTADO (no tocar DB)
        # ------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(model_name='categoria', name='nombre', field=models.CharField(max_length=120, unique=True)),
                migrations.AlterField(model_name='precio',    name='moneda', field=models.CharField(max_length=10, choices=[('ARS', 'ARS'), ('USD', 'USD')], default='USD')),
                migrations.AlterField(model_name='producto',  name='activo', field=models.BooleanField(default=True)),
                migrations.AlterField(
                    model_name='producto',
                    name='categoria',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='inventario.categoria'),
                ),
                migrations.AlterField(model_name='producto',  name='codigo_barras',        field=models.CharField(max_length=64, blank=True, null=True)),
                migrations.AlterField(model_name='producto',  name='descripcion',          field=models.TextField(default='', blank=True)),
                migrations.AlterField(model_name='producto',  name='imagen_codigo_barras', field=models.CharField(max_length=255, blank=True, null=True)),
                migrations.AlterField(model_name='producto',  name='nombre',               field=models.CharField(max_length=180)),
                migrations.AlterField(
                    model_name='producto',
                    name='proveedor',
                    field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='inventario.proveedor'),
                ),
                migrations.AlterField(model_name='proveedor', name='email',    field=models.EmailField(max_length=254, blank=True, default='')),
                migrations.AlterField(model_name='proveedor', name='nombre',   field=models.CharField(max_length=150, unique=True)),
                migrations.AlterField(model_name='proveedor', name='telefono', field=models.CharField(max_length=50, blank=True, default='')),
            ],
            database_operations=[],
        ),

        # ------------------------------------------------------------
        # 7) Índices: crear solo si NO existen (seguro en MySQL 8.0+)
        # ------------------------------------------------------------
        migrations.RunPython(_create_indexes, migrations.RunPython.noop),

        # ------------------------------------------------------------
        # 8) Quitar del ESTADO campos viejos que en tu DB aún existen
        #    (no los dropeamos ahora para no generar errores ni perder datos)
        # ------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name='precio', name='costo'),
                migrations.RemoveField(model_name='precio', name='precio_venta_descuento'),
                migrations.RemoveField(model_name='precio', name='precio_venta_minimo'),
                migrations.RemoveField(model_name='precio', name='precio_venta_normal'),
                migrations.RemoveField(model_name='precio', name='tipo_precio'),
                migrations.RemoveField(model_name='productovariante', name='nombre_variante'),
                migrations.RemoveField(model_name='productovariante', name='stock'),
            ],
            database_operations=[],
        ),
    ]
