import pymysql

pymysql.install_as_MySQLdb()

# Parche para deshabilitar RETURNING en MariaDB 10.4 (no soportado)
# Django 5.2 intenta usar RETURNING que no está disponible en MariaDB 10.4
try:
    from django.db.backends.mysql.operations import DatabaseOperations
    
    # Parchear el método que genera SQL con RETURNING
    if hasattr(DatabaseOperations, 'sql_insert'):
        original_sql_insert = DatabaseOperations.sql_insert
        
        def patched_sql_insert(self, table, fields, placeholder_rows, returning_fields=None):
            # Forzar returning_fields a None para MariaDB 10.4
            return original_sql_insert(self, table, fields, placeholder_rows, returning_fields=None)
        
        DatabaseOperations.sql_insert = patched_sql_insert
    
    # Parchear también el método que inserta en django_migrations
    from django.db.backends.base.operations import BaseDatabaseOperations
    if hasattr(BaseDatabaseOperations, 'execute_sql'):
        original_execute_sql = BaseDatabaseOperations.execute_sql
        
        def patched_execute_sql(self, sql, params=None):
            # Remover RETURNING de las queries SQL
            if sql and 'RETURNING' in sql.upper():
                sql = sql.split('RETURNING')[0].rstrip()
            return original_execute_sql(self, sql, params)
        
        # No parchear directamente, mejor usar otro enfoque
except (ImportError, AttributeError):
    pass
# -*- coding: utf-8 -*-