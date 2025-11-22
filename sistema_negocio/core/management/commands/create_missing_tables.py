"""
Comando para crear tablas faltantes directamente usando SQL.
Ejecutar: python manage.py create_missing_tables
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command


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

    def handle(self, *args, **options):
        # Tablas críticas que deben existir
        critical_tables = [
            'inventario_producto',
            'inventario_productovariante',
            'inventario_precio',
            'ventas_venta',
            'ventas_detalleventa',
        ]

        missing_tables = [table for table in critical_tables if not self._table_exists(table)]

        if not missing_tables:
            self.stdout.write(self.style.SUCCESS("✅ Todas las tablas críticas existen"))
            return

        self.stdout.write(self.style.WARNING(
            f"⚠️  Faltan {len(missing_tables)} tablas críticas: {', '.join(missing_tables)}"
        ))

        # Intentar crear las tablas usando --run-syncdb forzado
        self.stdout.write("\n🔧 Intentando crear tablas faltantes...")
        
        # Agrupar por app
        apps_to_fix = {}
        for table in missing_tables:
            app = table.split('_')[0]
            if app not in apps_to_fix:
                apps_to_fix[app] = []
            apps_to_fix[app].append(table)

        for app, tables in apps_to_fix.items():
            self.stdout.write(f"\n📦 Procesando {app}...")
            self.stdout.write(f"   Tablas faltantes: {', '.join(tables)}")
            
            # Intentar múltiples estrategias en orden de efectividad
            strategies = [
                ("migrate --fake-initial", lambda a=app: call_command('migrate', a, '--fake-initial', '--noinput', verbosity=1)),
                ("migrate --run-syncdb", lambda a=app: call_command('migrate', a, '--run-syncdb', '--noinput', verbosity=1)),
                ("migrate normal", lambda a=app: call_command('migrate', a, '--noinput', verbosity=1)),
            ]
            
            success = False
            for strategy_name, strategy_func in strategies:
                try:
                    self.stdout.write(f"   💡 Intentando: {strategy_name}...")
                    strategy_func()
                    # Verificar si se crearon las tablas
                    still_missing = [t for t in tables if not self._table_exists(t)]
                    if not still_missing:
                        self.stdout.write(self.style.SUCCESS(f"   ✓ Todas las tablas de {app} fueron creadas"))
                        success = True
                        break
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"   ⚠️  Aún faltan: {', '.join(still_missing)}"
                        ))
                except Exception as e:
                    error_msg = str(e)
                    # No mostrar errores completos si son muy largos
                    if len(error_msg) > 200:
                        error_msg = error_msg[:200] + "..."
                    self.stdout.write(self.style.ERROR(f"   ✗ Error con {strategy_name}: {error_msg}"))
            
            if not success:
                self.stdout.write(self.style.ERROR(
                    f"   ❌ No se pudieron crear todas las tablas de {app}"
                ))
                self.stdout.write(self.style.WARNING(
                    f"   💡 Las tablas {', '.join(tables)} aún no existen. "
                    "Puede que necesites ejecutar las migraciones manualmente."
                ))

        # Verificación final
        still_missing = [table for table in critical_tables if not self._table_exists(table)]
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

