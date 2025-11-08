"""Ensure fresh installations get the same schema expected by the ORM."""

from django.db import migrations, models
import django.utils.timezone


def _get_columns(connection, table_name):
    introspection = connection.introspection
    with connection.cursor() as cursor:
        try:
            description = introspection.get_table_description(cursor, table_name)
        except Exception:
            return set()
    return {col.name for col in description}


def _add_field_if_missing(apps, schema_editor, model_name, field_name, field):
    model = apps.get_model("inventario", model_name)
    table_name = model._meta.db_table
    columns = _get_columns(schema_editor.connection, table_name)
    column_name = field.db_column or field_name
    if column_name in columns:
        return
    field.set_attributes_from_name(field_name)
    schema_editor.add_field(model, field)


def _ensure_index(schema_editor, model, index):
    connection = schema_editor.connection
    introspection = connection.introspection
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        constraints = introspection.get_constraints(cursor, table_name)
    if index.name in constraints:
        return
    try:
        schema_editor.add_index(model, index)
    except Exception:
        # Different databases may expose existing indexes with custom names.
        # If we cannot create it (because it already exists), we safely ignore it.
        pass


def sync_schema(apps, schema_editor):
    # Ensure tables exist before touching them (fresh databases use all apps).
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        tables = set(connection.introspection.table_names(cursor))

    inventario_tables = {
        apps.get_model("inventario", "Categoria")._meta.db_table,
        apps.get_model("inventario", "Proveedor")._meta.db_table,
        apps.get_model("inventario", "Producto")._meta.db_table,
        apps.get_model("inventario", "ProductoVariante")._meta.db_table,
        apps.get_model("inventario", "Precio")._meta.db_table,
    }

    if not inventario_tables.issubset(tables):
        # The base tables are not ready yet; nothing to do.
        return

    timezone_now = django.utils.timezone.now

    _add_field_if_missing(
        apps,
        schema_editor,
        "Categoria",
        "descripcion",
        models.TextField(blank=True, default=""),
    )

    _add_field_if_missing(
        apps,
        schema_editor,
        "Proveedor",
        "activo",
        models.BooleanField(default=True),
    )

    _add_field_if_missing(
        apps,
        schema_editor,
        "Producto",
        "creado",
        models.DateTimeField(default=timezone_now, editable=False),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "Producto",
        "actualizado",
        models.DateTimeField(auto_now=True, default=timezone_now),
    )

    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "sku",
        models.CharField(max_length=64, unique=True, default=""),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "atributo_1",
        models.CharField(max_length=120, blank=True, default=""),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "atributo_2",
        models.CharField(max_length=120, blank=True, default=""),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "stock_actual",
        models.IntegerField(default=0),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "stock_minimo",
        models.IntegerField(default=0),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "activo",
        models.BooleanField(default=True),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "creado",
        models.DateTimeField(default=timezone_now, editable=False),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "actualizado",
        models.DateTimeField(auto_now=True, default=timezone_now),
    )

    _add_field_if_missing(
        apps,
        schema_editor,
        "Precio",
        "tipo",
        models.CharField(
            max_length=20,
            choices=[("MINORISTA", "Minorista"), ("MAYORISTA", "Mayorista")],
            default="MINORISTA",
        ),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "Precio",
        "precio",
        models.DecimalField(max_digits=12, decimal_places=2, default=0),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "Precio",
        "moneda",
        models.CharField(
            max_length=10,
            choices=[("ARS", "ARS"), ("USD", "USD")],
            default="USD",
        ),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "Precio",
        "activo",
        models.BooleanField(default=True),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "Precio",
        "creado",
        models.DateTimeField(default=timezone_now, editable=False),
    )
    _add_field_if_missing(
        apps,
        schema_editor,
        "Precio",
        "actualizado",
        models.DateTimeField(auto_now=True, default=timezone_now),
    )

    # Ensure the key indexes exist so ORM queries match expectations.
    Categoria = apps.get_model("inventario", "Categoria")
    Proveedor = apps.get_model("inventario", "Proveedor")
    Producto = apps.get_model("inventario", "Producto")
    ProductoVariante = apps.get_model("inventario", "ProductoVariante")
    Precio = apps.get_model("inventario", "Precio")

    _ensure_index(
        schema_editor,
        Categoria,
        models.Index(fields=["nombre"], name="idx_categoria_nombre"),
    )
    _ensure_index(
        schema_editor,
        Proveedor,
        models.Index(fields=["activo"], name="idx_proveedor_activo"),
    )
    _ensure_index(
        schema_editor,
        Proveedor,
        models.Index(fields=["nombre"], name="idx_proveedor_nombre"),
    )
    _ensure_index(
        schema_editor,
        Producto,
        models.Index(fields=["activo"], name="idx_producto_activo"),
    )
    _ensure_index(
        schema_editor,
        Producto,
        models.Index(fields=["nombre"], name="idx_producto_nombre"),
    )
    _ensure_index(
        schema_editor,
        Producto,
        models.Index(fields=["codigo_barras"], name="idx_producto_cod_barras"),
    )
    _ensure_index(
        schema_editor,
        ProductoVariante,
        models.Index(fields=["sku"], name="idx_var_sku"),
    )
    _ensure_index(
        schema_editor,
        ProductoVariante,
        models.Index(fields=["activo"], name="idx_var_activo"),
    )
    _ensure_index(
        schema_editor,
        ProductoVariante,
        models.Index(fields=["stock_actual"], name="idx_var_stock"),
    )
    _ensure_index(
        schema_editor,
        Precio,
        models.Index(fields=["activo"], name="idx_precio_activo"),
    )
    _ensure_index(
        schema_editor,
        Precio,
        models.Index(fields=["variante", "tipo", "moneda"], name="idx_precio_var_tipo_mon"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0009_detalleiphone_variante_bridge"),
    ]

    operations = [
        migrations.RunPython(sync_schema, migrations.RunPython.noop),
    ]
