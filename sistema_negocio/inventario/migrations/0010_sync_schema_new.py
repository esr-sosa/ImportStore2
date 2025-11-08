"""Ensure fresh installations align with the expected ORM schema."""

from __future__ import annotations

import django.utils.timezone
from django.db import migrations, models
from django.db.models import Count, Q


def _get_columns(connection, table_name: str) -> set[str]:
    introspection = connection.introspection
    with connection.cursor() as cursor:
        try:
            description = introspection.get_table_description(cursor, table_name)
        except Exception:
            return set()
    return {column.name.lower() for column in description}


def _add_field_if_missing(apps, schema_editor, model_name: str, field_name: str, field: models.Field) -> bool:
    """Add *field_name* to *model_name* only when it doesn't exist."""

    model = apps.get_model("inventario", model_name)
    table_name = model._meta.db_table
    existing_columns = _get_columns(schema_editor.connection, table_name)

    working_field = field.clone()
    # ``set_attributes_from_name`` normaliza ``attname`` y ``column`` cuando
    # todavía no fueron definidos en el ``Field`` clonado.
    working_field.set_attributes_from_name(field_name)
    _, resolved_column = working_field.get_attname_column()
    column_name = (resolved_column or field_name).lower()

    if column_name in existing_columns:
        return False

    schema_editor.add_field(model, working_field)
    return True


def _finalize_field(schema_editor, model, field_name: str, new_field: models.Field) -> None:
    """Alter an existing field so the database matches the ORM definition."""

    old_field = model._meta.get_field(field_name)
    desired = new_field.clone()
    desired.set_attributes_from_name(field_name)
    schema_editor.alter_field(model, old_field, desired)


def _ensure_index(schema_editor, model, index: models.Index | models.UniqueConstraint) -> None:
    connection = schema_editor.connection
    introspection = connection.introspection
    table_name = model._meta.db_table

    with connection.cursor() as cursor:
        constraints = introspection.get_constraints(cursor, table_name)

    if index.name in constraints:
        return

    try:
        if isinstance(index, models.UniqueConstraint):
            schema_editor.add_constraint(model, index)
        else:
            schema_editor.add_index(model, index)
    except Exception:
        # Different engines may expose pre-existing objects with other names.
        # If creation fails we assume it's already there and continue.
        pass


def _populate_missing_skus(apps, schema_editor) -> None:
    ProductoVariante = apps.get_model("inventario", "ProductoVariante")
    table_name = ProductoVariante._meta.db_table
    columns = _get_columns(schema_editor.connection, table_name)

    if "sku" not in columns:
        return

    missing_ids = list(
        ProductoVariante.objects.filter(Q(sku__isnull=True) | Q(sku=""))
        .values_list("pk", flat=True)
    )

    if not missing_ids:
        return

    for pk in missing_ids:
        ProductoVariante.objects.filter(pk=pk).update(sku=f"SKU-{pk:06d}")


def _ensure_unique_sku(schema_editor, apps) -> None:
    ProductoVariante = apps.get_model("inventario", "ProductoVariante")
    if ProductoVariante.objects.values("sku").filter(Q(sku__isnull=True) | Q(sku="")).exists():
        return
    if ProductoVariante.objects.values("sku").annotate(total=Count("id")).filter(total__gt=1).exists():
        return

    constraint = models.UniqueConstraint(fields=["sku"], name="uniq_variante_sku")
    _ensure_index(schema_editor, ProductoVariante, constraint)


def sync_schema(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        tables = set(connection.introspection.table_names(cursor))

    required_tables = {
        apps.get_model("inventario", name)._meta.db_table
        for name in ("Categoria", "Proveedor", "Producto", "ProductoVariante", "Precio")
    }
    if not required_tables.issubset(tables):
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

    sku_added = _add_field_if_missing(
        apps,
        schema_editor,
        "ProductoVariante",
        "sku",
        models.CharField(max_length=64, blank=True, null=True),
    )

    columns = _get_columns(
        schema_editor.connection, apps.get_model("inventario", "ProductoVariante")._meta.db_table
    )
    if "sku" in columns:
        _populate_missing_skus(apps, schema_editor)

    if sku_added:
        ProductoVariante = apps.get_model("inventario", "ProductoVariante")
        _finalize_field(
            schema_editor,
            ProductoVariante,
            "sku",
            models.CharField(max_length=64, unique=True),
        )
        _ensure_unique_sku(schema_editor, apps)
    elif "sku" in columns:
        _ensure_unique_sku(schema_editor, apps)

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

    Categoria = apps.get_model("inventario", "Categoria")
    Proveedor = apps.get_model("inventario", "Proveedor")
    Producto = apps.get_model("inventario", "Producto")
    ProductoVariante = apps.get_model("inventario", "ProductoVariante")
    Precio = apps.get_model("inventario", "Precio")

    _ensure_index(schema_editor, Categoria, models.Index(fields=["nombre"], name="idx_categoria_nombre"))
    _ensure_index(schema_editor, Proveedor, models.Index(fields=["activo"], name="idx_proveedor_activo"))
    _ensure_index(schema_editor, Proveedor, models.Index(fields=["nombre"], name="idx_proveedor_nombre"))
    _ensure_index(schema_editor, Producto, models.Index(fields=["activo"], name="idx_producto_activo"))
    _ensure_index(schema_editor, Producto, models.Index(fields=["nombre"], name="idx_producto_nombre"))
    _ensure_index(schema_editor, Producto, models.Index(fields=["codigo_barras"], name="idx_producto_cod_barras"))
    _ensure_index(schema_editor, ProductoVariante, models.Index(fields=["sku"], name="idx_var_sku"))
    _ensure_index(schema_editor, ProductoVariante, models.Index(fields=["activo"], name="idx_var_activo"))
    _ensure_index(schema_editor, ProductoVariante, models.Index(fields=["stock_actual"], name="idx_var_stock"))
    _ensure_index(schema_editor, Precio, models.Index(fields=["activo"], name="idx_precio_activo"))
    _ensure_index(
        schema_editor,
        Precio,
        models.Index(fields=["variante", "tipo", "moneda"], name="idx_precio_var_tipo_mon"),
    )


def _reset_inspector_cache(apps, schema_editor) -> None:
    try:
        from core.db_inspector import reset_caches
    except Exception:
        return

    reset_caches()


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0009_detalleiphone_variante_bridge"),
    ]

    operations = [
        migrations.RunPython(sync_schema, migrations.RunPython.noop),
        migrations.RunPython(_reset_inspector_cache, migrations.RunPython.noop),
    ]

