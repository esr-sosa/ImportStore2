"""
Comando para marcar migraciones como aplicadas sin usar RETURNING
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Marca la migración 0001_initial de core como aplicada'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Verificar si ya existe
            cursor.execute(
                "SELECT COUNT(*) FROM django_migrations WHERE app='core' AND name='0001_initial'"
            )
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insertar sin usar RETURNING (compatible con MariaDB 10.4)
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())",
                    ['core', '0001_initial']
                )
                self.stdout.write(
                    self.style.SUCCESS('✅ Migración core.0001_initial marcada como aplicada')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️  La migración ya estaba registrada')
                )

