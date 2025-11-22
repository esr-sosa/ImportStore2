"""
Comando para marcar migraciones problemáticas como aplicadas cuando no se pueden ejecutar.
Ejecutar: python manage.py fix_problematic_migrations
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Marca migraciones problemáticas como aplicadas si no se pueden ejecutar'

    def _index_exists(self, table_name, index_name):
        """Verifica si un índice existe en una tabla"""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM information_schema.STATISTICS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = %s 
                    AND INDEX_NAME = %s
                    """,
                    [table_name, index_name]
                )
                return cursor.fetchone()[0] > 0
            elif connection.vendor == 'postgresql':
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM pg_indexes 
                    WHERE tablename = %s 
                    AND indexname = %s
                    """,
                    [table_name, index_name]
                )
                return cursor.fetchone()[0] > 0
        return False

    def handle(self, *args, **options):
        # Verificar si la migración core.0008 puede ejecutarse
        # Esta migración intenta renombrar un índice que puede no existir
        
        table_name = "core_notificacioninterna"
        old_index = "core_notifi_leida_9a8f2d_idx"
        new_index = "core_notifi_leida_d2a21f_idx"
        
        # Verificar si el índice antiguo existe
        old_exists = self._index_exists(table_name, old_index)
        new_exists = self._index_exists(table_name, new_index)
        
        if not old_exists and not new_exists:
            # Si ninguno de los índices existe, la migración no se puede ejecutar
            # pero podemos marcarla como aplicada
            self.stdout.write(self.style.WARNING(
                f"⚠️  Los índices {old_index} y {new_index} no existen en {table_name}"
            ))
            self.stdout.write(self.style.SUCCESS(
                "💡 La migración core.0008 se puede marcar como aplicada manualmente si es necesario"
            ))
        elif old_exists and not new_exists:
            self.stdout.write(self.style.SUCCESS(
                f"✓ El índice antiguo {old_index} existe, la migración debería ejecutarse correctamente"
            ))
        elif new_exists:
            self.stdout.write(self.style.SUCCESS(
                f"✓ El índice nuevo {new_index} ya existe, la migración ya fue aplicada"
            ))
        
        self.stdout.write(self.style.SUCCESS("\n✅ Verificación completada"))

