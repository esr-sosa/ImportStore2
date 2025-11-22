"""
Comando para forzar la creación de columnas faltantes en inventario.
Ejecutar: python manage.py fix_inventario_schema
"""
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db import models
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fuerza la creación de columnas faltantes en el esquema de inventario'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué columnas se crearían sin hacer cambios',
        )

    def _column_exists(self, table_name, column_name):
        """Verifica si una columna existe en una tabla"""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
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
            elif connection.vendor == 'postgresql':
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM information_schema.columns 
                    WHERE table_name = %s 
                    AND column_name = %s
                    """,
                    [table_name, column_name]
                )
                return cursor.fetchone()[0] > 0
        return False

    def _add_column(self, table_name, column_name, column_type, default_value=None, nullable=True):
        """Agrega una columna a una tabla"""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                null_clause = "NULL" if nullable else "NOT NULL"
                if default_value is not None:
                    default_clause = f"DEFAULT {default_value}"
                else:
                    default_clause = ""
                sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {column_type} {null_clause} {default_clause}".strip()
            elif connection.vendor == 'postgresql':
                null_clause = "" if nullable else "NOT NULL"
                if default_value is not None:
                    default_clause = f"DEFAULT {default_value}"
                else:
                    default_clause = ""
                sql = f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_type} {null_clause} {default_clause}'.strip()
            else:
                self.stdout.write(self.style.ERROR(f"Base de datos no soportada: {connection.vendor}"))
                return False
            
            try:
                cursor.execute(sql)
                return True
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error al agregar columna {table_name}.{column_name}: {e}"))
                return False

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
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING("MODO DRY-RUN: No se harán cambios reales\n"))

        # Verificar que las tablas existan primero
        required_tables = [
            "inventario_productovariante",
            "inventario_producto",
            "inventario_precio"
        ]
        
        missing_tables = [table for table in required_tables if not self._table_exists(table)]
        
        if missing_tables:
            self.stdout.write(self.style.ERROR(
                f"❌ Las siguientes tablas no existen: {', '.join(missing_tables)}\n"
            ))
            self.stdout.write(self.style.WARNING(
                "💡 Ejecutá primero: python manage.py migrate --run-syncdb\n"
            ))
            return

        # Definir las columnas que necesitamos crear
        columns_to_create = [
            # ProductoVariante
            ("inventario_productovariante", "sku", "VARCHAR(64)", None, True),
            ("inventario_productovariante", "nombre_variante", "VARCHAR(200)", "''", False),
            ("inventario_productovariante", "qr_code", "VARCHAR(255)", None, True),
            ("inventario_productovariante", "stock_actual", "INTEGER", "0", False),
            ("inventario_productovariante", "stock_minimo", "INTEGER", "0", False),
            ("inventario_productovariante", "activo", "BOOLEAN", "1", False),
            
            # Producto
            ("inventario_producto", "activo", "BOOLEAN", "1", False),
            
            # Precio
            ("inventario_precio", "precio", "DECIMAL(12,2)", "0", False),
        ]

        # Ajustar tipos según la base de datos
        if connection.vendor == 'mysql':
            # MySQL usa TINYINT(1) para booleanos
            columns_to_create = [
                (table, col, 
                 "TINYINT(1)" if col_type == "BOOLEAN" else col_type,
                 default, nullable)
                for table, col, col_type, default, nullable in columns_to_create
            ]
        elif connection.vendor == 'postgresql':
            # PostgreSQL usa BOOLEAN directamente
            columns_to_create = [
                (table, col,
                 "BOOLEAN" if col_type == "BOOLEAN" else col_type,
                 "TRUE" if col_type == "BOOLEAN" and default == "1" else default,
                 nullable)
                for table, col, col_type, default, nullable in columns_to_create
            ]

        created_count = 0
        skipped_count = 0
        error_count = 0

        self.stdout.write(self.style.SUCCESS("Verificando columnas faltantes...\n"))

        for table_name, column_name, column_type, default_value, nullable in columns_to_create:
            if self._column_exists(table_name, column_name):
                self.stdout.write(f"✓ {table_name}.{column_name} ya existe")
                skipped_count += 1
            else:
                if dry_run:
                    self.stdout.write(self.style.WARNING(
                        f"→ Se crearía: {table_name}.{column_name} ({column_type})"
                    ))
                    created_count += 1
                else:
                    self.stdout.write(f"Creando {table_name}.{column_name}...")
                    if self._add_column(table_name, column_name, column_type, default_value, nullable):
                        self.stdout.write(self.style.SUCCESS(
                            f"✓ {table_name}.{column_name} creada exitosamente"
                        ))
                        created_count += 1
                    else:
                        error_count += 1

        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f"DRY-RUN: {created_count} columnas se crearían, {skipped_count} ya existen"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"✓ {created_count} columnas creadas, {skipped_count} ya existían"
            ))
            if error_count > 0:
                self.stdout.write(self.style.ERROR(f"✗ {error_count} errores"))
            
            # Limpiar caché del inspector
            try:
                from core.db_inspector import reset_caches
                reset_caches()
                self.stdout.write(self.style.SUCCESS("✓ Caché del inspector limpiado"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠ No se pudo limpiar caché: {e}"))

