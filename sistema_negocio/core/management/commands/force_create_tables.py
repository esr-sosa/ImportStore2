"""
Comando para crear tablas faltantes directamente usando SQL.
Este comando es más agresivo y crea las tablas directamente sin depender de migraciones.
Ejecutar: python manage.py force_create_tables
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management.sql import sql_create_index, sql_create_table
from django.apps import apps


class Command(BaseCommand):
    help = 'Crea tablas faltantes directamente usando SQL si las migraciones fallan'

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

    def _create_table_from_model(self, model_class):
        """Crea una tabla directamente desde un modelo usando SQL"""
        table_name = model_class._meta.db_table
        if self._table_exists(table_name):
            self.stdout.write(f"   ✓ Tabla {table_name} ya existe")
            return True

        try:
            # Obtener el SQL para crear la tabla
            sql_statements = sql_create_table(model_class._meta, connection)
            
            with connection.cursor() as cursor:
                for statement in sql_statements:
                    try:
                        cursor.execute(statement)
                        self.stdout.write(self.style.SUCCESS(f"   ✓ Tabla {table_name} creada"))
                        return True
                    except Exception as e:
                        # Si falla, intentar con una versión simplificada
                        error_msg = str(e)
                        if "already exists" in error_msg.lower() or "duplicate" in error_msg.lower():
                            self.stdout.write(f"   ✓ Tabla {table_name} ya existe (detectado por error)")
                            return True
                        self.stdout.write(self.style.WARNING(
                            f"   ⚠️  Error al crear {table_name}: {error_msg[:100]}"
                        ))
                        return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"   ✗ Error al generar SQL para {table_name}: {str(e)[:100]}"
            ))
            return False

    def handle(self, *args, **options):
        # Modelos críticos que deben existir
        critical_models = [
            ('inventario', 'Producto'),
            ('inventario', 'ProductoVariante'),
            ('inventario', 'Precio'),
            ('ventas', 'Venta'),
            ('ventas', 'DetalleVenta'),
        ]

        missing_tables = []
        for app_label, model_name in critical_models:
            try:
                model = apps.get_model(app_label, model_name)
                table_name = model._meta.db_table
                if not self._table_exists(table_name):
                    missing_tables.append((app_label, model_name, model))
            except LookupError:
                self.stdout.write(self.style.WARNING(
                    f"⚠️  No se pudo encontrar el modelo {app_label}.{model_name}"
                ))

        if not missing_tables:
            self.stdout.write(self.style.SUCCESS("✅ Todas las tablas críticas existen"))
            return

        self.stdout.write(self.style.WARNING(
            f"⚠️  Faltan {len(missing_tables)} tablas críticas"
        ))

        # Agrupar por app
        apps_to_fix = {}
        for app_label, model_name, model in missing_tables:
            if app_label not in apps_to_fix:
                apps_to_fix[app_label] = []
            apps_to_fix[app_label].append((model_name, model))

        # Intentar crear tablas usando --fake-initial primero
        self.stdout.write("\n🔧 Intentando crear tablas usando --fake-initial...")
        from django.core.management import call_command
        
        for app_label in apps_to_fix.keys():
            try:
                self.stdout.write(f"\n📦 Procesando {app_label} con --fake-initial...")
                call_command('migrate', app_label, '--fake-initial', '--noinput', verbosity=1)
                # Verificar si se crearon
                still_missing = []
                for model_name, model in apps_to_fix[app_label]:
                    if not self._table_exists(model._meta.db_table):
                        still_missing.append((model_name, model))
                if not still_missing:
                    self.stdout.write(self.style.SUCCESS(f"   ✓ Todas las tablas de {app_label} fueron creadas"))
                    apps_to_fix[app_label] = []
                else:
                    apps_to_fix[app_label] = still_missing
            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f"   ⚠️  Error con --fake-initial en {app_label}: {str(e)[:100]}"
                ))

        # Si aún faltan tablas, crearlas directamente desde los modelos
        remaining_missing = []
        for app_label, models_list in apps_to_fix.items():
            if models_list:
                remaining_missing.extend([(app_label, model_name, model) for model_name, model in models_list])

        if remaining_missing:
            self.stdout.write("\n🔧 Creando tablas faltantes directamente desde modelos...")
            for app_label, model_name, model in remaining_missing:
                self.stdout.write(f"\n📦 Creando {app_label}.{model_name}...")
                success = self._create_table_from_model(model)
                if not success:
                    self.stdout.write(self.style.ERROR(
                        f"   ❌ No se pudo crear la tabla {model._meta.db_table}"
                    ))

        # Verificación final
        still_missing = []
        for app_label, model_name in critical_models:
            try:
                model = apps.get_model(app_label, model_name)
                table_name = model._meta.db_table
                if not self._table_exists(table_name):
                    still_missing.append(table_name)
            except LookupError:
                pass

        if still_missing:
            self.stdout.write(self.style.ERROR(
                f"\n❌ Aún faltan {len(still_missing)} tablas: {', '.join(still_missing)}"
            ))
            self.stdout.write(self.style.WARNING(
                "💡 Puede que necesites ejecutar las migraciones manualmente o verificar los logs"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                "\n✅ Todas las tablas críticas fueron creadas exitosamente"
            ))

