"""
Comando para verificar y crear tablas básicas si no existen.
Ejecutar: python manage.py ensure_tables_exist
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Verifica que las tablas básicas existan y las crea si faltan'

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
        # Tablas críticas que deben existir
        required_tables = {
            'inventario': [
                'inventario_categoria',
                'inventario_proveedor',
                'inventario_producto',
                'inventario_productovariante',
                'inventario_precio',
            ],
            'ventas': [
                'ventas_venta',
                'ventas_detalleventa',
            ],
            'core': [
                'core_perfilusuario',
                'core_direccionenvio',
                'core_favorito',
                'core_solicitudmayorista',
                'core_notificacioninterna',
            ],
        }

        missing_tables = []
        for app, tables in required_tables.items():
            for table in tables:
                if not self._table_exists(table):
                    missing_tables.append((app, table))

        if not missing_tables:
            self.stdout.write(self.style.SUCCESS("✅ Todas las tablas críticas existen"))
            return

        self.stdout.write(self.style.WARNING(
            f"⚠️  Faltan {len(missing_tables)} tablas críticas"
        ))

        # Agrupar por app
        apps_to_fix = {}
        for app, table in missing_tables:
            if app not in apps_to_fix:
                apps_to_fix[app] = []
            apps_to_fix[app].append(table)

        # Intentar crear las tablas faltantes
        for app, tables in apps_to_fix.items():
            self.stdout.write(f"\n🔧 Creando tablas faltantes para {app}...")
            self.stdout.write(f"   Tablas faltantes: {', '.join(tables)}")
            
            # PRIMERO: Intentar ejecutar migraciones normalmente
            try:
                self.stdout.write(f"   💡 Intentando ejecutar migraciones de {app}...")
                call_command('migrate', app, '--noinput', verbosity=1)
                self.stdout.write(self.style.SUCCESS(f"   ✓ Migraciones de {app} ejecutadas"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"   ⚠️  Error en migraciones de {app}: {e}"))
                
                # SEGUNDO: Si falla, usar --run-syncdb para crear tablas básicas
                try:
                    self.stdout.write(f"   💡 Intentando crear tablas con --run-syncdb...")
                    call_command('migrate', app, '--run-syncdb', '--noinput', verbosity=1)
                    self.stdout.write(self.style.SUCCESS(f"   ✓ Tablas de {app} creadas con --run-syncdb"))
                except Exception as e2:
                    self.stdout.write(self.style.ERROR(f"   ✗ Error al crear tablas de {app}: {e2}"))
                    
                    # TERCERO: Intentar ejecutar migraciones nuevamente después de --run-syncdb
                    try:
                        self.stdout.write(f"   💡 Intentando ejecutar migraciones nuevamente...")
                        call_command('migrate', app, '--noinput', verbosity=1)
                        self.stdout.write(self.style.SUCCESS(f"   ✓ Migraciones de {app} ejecutadas después de --run-syncdb"))
                    except Exception as e3:
                        self.stdout.write(self.style.ERROR(f"   ✗ Error final en {app}: {e3}"))

        # Verificar nuevamente
        still_missing = []
        for app, tables in required_tables.items():
            for table in tables:
                if not self._table_exists(table):
                    still_missing.append((app, table))

        if still_missing:
            self.stdout.write(self.style.ERROR(
                f"\n❌ Aún faltan {len(still_missing)} tablas:"
            ))
            for app, table in still_missing:
                self.stdout.write(f"   - {table} ({app})")
        else:
            self.stdout.write(self.style.SUCCESS(
                "\n✅ Todas las tablas críticas fueron creadas exitosamente"
            ))

