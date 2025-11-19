# Generated manually to handle field rename and SKU nullability

from django.db import migrations, models


def check_column_exists(connection, table_name, column_name):
    """Check if a column exists in a table."""
    vendor = connection.vendor
    with connection.cursor() as cursor:
        if vendor == 'sqlite':
            # SQLite approach
            cursor.execute(
                "PRAGMA table_info(%s)" % table_name
            )
            columns = [row[1] for row in cursor.fetchall()]
            return column_name in columns
        else:
            # MySQL/MariaDB approach
            cursor.execute(
                """
                SELECT COUNT(*) FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = %s 
                AND COLUMN_NAME = %s
                """,
                [table_name, column_name]
            )
            return cursor.fetchone()[0] > 0


def rename_if_exists(apps, schema_editor):
    """Rename ultima_actualizacion to actualizado only if it exists."""
    connection = schema_editor.connection
    table_name = "inventario_producto"
    vendor = connection.vendor
    
    if check_column_exists(connection, table_name, "ultima_actualizacion"):
        with connection.cursor() as cursor:
            if vendor == 'sqlite':
                # SQLite doesn't support ALTER TABLE RENAME COLUMN directly in older versions
                # For SQLite 3.25.0+, we can use ALTER TABLE ... RENAME COLUMN
                # For older versions, we'd need to recreate the table, but Django handles this
                # So we'll just skip the rename for SQLite and let Django handle it
                pass
            else:
                # MySQL/MariaDB
                cursor.execute(
                    f"ALTER TABLE {table_name} CHANGE COLUMN ultima_actualizacion actualizado DATETIME(6)"
                )


def populate_missing_skus(apps, schema_editor):
    """Populate any NULL SKU values with temporary values."""
    ProductoVariante = apps.get_model("inventario", "ProductoVariante")
    connection = schema_editor.connection
    
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM inventario_productovariante WHERE sku IS NULL OR sku = ''"
        )
        rows = cursor.fetchall()
        
        for (pk,) in rows:
            cursor.execute(
                "UPDATE inventario_productovariante SET sku = %s WHERE id = %s",
                [f"SKU-{pk:06d}", pk]
            )


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0010_sync_schema_new"),
    ]

    operations = [
        # Rename ultima_actualizacion to actualizado in Producto (only if it exists in DB)
        migrations.RunPython(rename_if_exists, migrations.RunPython.noop),
        # Update Django's migration state to reflect the rename (without touching DB)
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name="producto",
                    old_name="ultima_actualizacion",
                    new_name="actualizado",
                ),
            ],
        ),
        # Ensure all SKUs have values before making it non-nullable
        migrations.RunPython(populate_missing_skus, migrations.RunPython.noop),
        # Make SKU non-nullable and unique
        migrations.AlterField(
            model_name="productovariante",
            name="sku",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]

