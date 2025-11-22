"""
Comando para generar SQL que crea las tablas faltantes.
Ejecutar: python manage.py generate_create_tables_sql
Luego copiar el SQL y ejecutarlo en MySQL Workbench.
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.core.management.sql import sql_create_table
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class Command(BaseCommand):
    help = 'Genera SQL para crear tablas faltantes que puedes ejecutar manualmente en MySQL Workbench'

    def _table_exists(self, table_name):
        """Verifica si una tabla existe"""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM information_schema.TABLES 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = %s
                    """,
                    [table_name]
                )
                return cursor.fetchone()[0] > 0
            elif connection.vendor == 'postgresql':
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_name = %s
                    """,
                    [table_name]
                )
                return cursor.fetchone()[0] > 0
        return False

    def handle(self, *args, **options):
        # Modelos críticos que deben existir
        critical_models = [
            ('inventario', 'Categoria'),
            ('inventario', 'Proveedor'),
            ('inventario', 'Producto'),
            ('inventario', 'ProductoVariante'),
            ('inventario', 'Precio'),
            ('ventas', 'Cupon'),
            ('ventas', 'Venta'),
            ('ventas', 'DetalleVenta'),
        ]

        missing_tables = []
        for app_label, model_name in critical_models:
            try:
                model = apps.get_model(app_label, model_name)
                table_name = model._meta.db_table
                if not self._table_exists(table_name):
                    missing_tables.append((app_label, model_name, model, table_name))
            except LookupError:
                self.stdout.write(self.style.WARNING(
                    f"⚠️  No se pudo encontrar el modelo {app_label}.{model_name}"
                ))

        if not missing_tables:
            self.stdout.write(self.style.SUCCESS("✅ Todas las tablas críticas existen"))
            return

        self.stdout.write(self.style.WARNING(
            f"\n⚠️  Faltan {len(missing_tables)} tablas críticas\n"
        ))
        self.stdout.write("=" * 80)
        self.stdout.write("SQL PARA EJECUTAR EN MYSQL WORKBENCH:")
        self.stdout.write("=" * 80)
        self.stdout.write("\n-- Copia y pega este SQL en MySQL Workbench\n")
        self.stdout.write("-- Asegúrate de estar conectado a la base de datos 'railway'\n\n")

        # Generar SQL para cada tabla faltante
        sql_statements = []
        for app_label, model_name, model, table_name in missing_tables:
            self.stdout.write(f"-- Creando tabla: {table_name} ({app_label}.{model_name})")
            
            try:
                # Obtener el SQL para crear la tabla
                with connection.schema_editor() as schema_editor:
                    # Obtener la definición SQL de la tabla
                    sql = schema_editor.sql_create_table(model._meta)
                    sql_statements.append(sql)
                    self.stdout.write(f"-- SQL generado para {table_name}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"-- ❌ Error al generar SQL para {table_name}: {str(e)[:100]}"
                ))
                # Intentar método alternativo
                try:
                    from django.db import models
                    from django.core.management.sql import sql_create_table
                    sql = sql_create_table(model._meta, connection)
                    if sql:
                        sql_statements.extend(sql)
                        self.stdout.write(f"-- ✓ SQL generado alternativamente para {table_name}")
                except Exception as e2:
                    self.stdout.write(self.style.ERROR(
                        f"-- ❌ Error alternativo para {table_name}: {str(e2)[:100]}"
                    ))

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("INSTRUCCIONES:")
        self.stdout.write("=" * 80)
        self.stdout.write("""
1. Abre MySQL Workbench
2. Conéctate a tu base de datos Railway
3. Selecciona la base de datos 'railway'
4. Abre una nueva pestaña de SQL
5. Copia y pega el SQL generado arriba
6. Ejecuta el SQL (Ctrl+Enter o botón Execute)

O mejor aún, ejecuta este comando localmente para obtener el SQL:
    python manage.py sqlmigrate inventario 0001
    python manage.py sqlmigrate ventas 0001

Luego ejecuta ese SQL en MySQL Workbench.
""")

        # Intentar obtener SQL de las migraciones iniciales
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SQL DE MIGRACIONES INICIALES (RECOMENDADO):")
        self.stdout.write("=" * 80)
        self.stdout.write("\n-- Ejecuta estos comandos localmente para obtener el SQL:\n")
        self.stdout.write("python manage.py sqlmigrate inventario 0001\n")
        self.stdout.write("python manage.py sqlmigrate ventas 0001\n")
        self.stdout.write("\nLuego copia y pega el SQL en MySQL Workbench.\n")

