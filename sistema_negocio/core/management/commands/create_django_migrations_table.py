"""
Comando para crear la tabla django_migrations si no existe
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Crea la tabla django_migrations si no existe'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Verificar si la tabla existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'django_migrations'
            """)
            table_exists = cursor.fetchone()[0] > 0
            
            if not table_exists:
                # Crear la tabla django_migrations
                # Asegurar que AUTO_INCREMENT esté configurado correctamente
                cursor.execute("""
                    CREATE TABLE django_migrations (
                        id BIGINT NOT NULL AUTO_INCREMENT,
                        app VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        applied DATETIME(6) NOT NULL,
                        PRIMARY KEY (id),
                        UNIQUE KEY django_migrations_app_name_uc (app, name)
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4
                """)
                self.stdout.write(
                    self.style.SUCCESS('✅ Tabla django_migrations creada')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('ℹ️  La tabla django_migrations ya existe')
                )

