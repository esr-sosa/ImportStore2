import pymysql

pymysql.install_as_MySQLdb()

# Parche para deshabilitar RETURNING en MariaDB 10.4 (no soportado)
# Django 5.2 intenta usar RETURNING que no está disponible en MariaDB 10.4

def _apply_returning_patches():
    """Aplica parches para evitar el uso de RETURNING en MariaDB 10.4."""
    try:
        from django.db.backends.utils import CursorWrapper
        
        # Parche 1: Interceptar queries SQL y remover RETURNING
        if hasattr(CursorWrapper, 'execute'):
            original_execute = CursorWrapper.execute
            
            def patched_execute(self, sql, params=None):
                # Remover RETURNING de las queries SQL si existe
                if sql:
                    sql_str = sql
                    if isinstance(sql, bytes):
                        sql_str = sql.decode('utf-8', errors='ignore')
                    elif not isinstance(sql, str):
                        sql_str = str(sql)
                    
                    # Parche especial para INSERT en django_migrations: MySQL estricto requiere id explícito
                    if 'INSERT INTO' in sql_str.upper() and 'django_migrations' in sql_str:
                        # Verificar si el INSERT no incluye id
                        if '(`id`' not in sql_str and '(id' not in sql_str and '`id`' not in sql_str:
                            # Modificar el SQL para incluir id con NULL (que activará AUTO_INCREMENT)
                            import re
                            # Patrón: INSERT INTO django_migrations (app, name, applied) VALUES ...
                            pattern = r'INSERT INTO\s+(?:`)?django_migrations(?:`)?\s*\(([^)]+)\)\s*VALUES'
                            match = re.search(pattern, sql_str, re.IGNORECASE)
                            if match:
                                columns = match.group(1)
                                # Agregar id al principio de las columnas
                                new_columns = f"id, {columns}"
                                sql_str = re.sub(
                                    pattern,
                                    lambda m: f"INSERT INTO django_migrations ({new_columns}) VALUES",
                                    sql_str,
                                    flags=re.IGNORECASE
                                )
                                # Agregar NULL para id en los valores
                                # Buscar VALUES (?, ?, ?) o VALUES (%s, %s, %s)
                                values_pattern = r'VALUES\s*\(([^)]+)\)'
                                values_match = re.search(values_pattern, sql_str, re.IGNORECASE)
                                if values_match:
                                    values = values_match.group(1)
                                    # Contar cuántos placeholders hay
                                    placeholder_count = values.count('?') + values.count('%s')
                                    if placeholder_count > 0:
                                        # Agregar NULL al principio
                                        sql_str = re.sub(
                                            values_pattern,
                                            lambda m: f"VALUES (NULL, {m.group(1)})",
                                            sql_str,
                                            flags=re.IGNORECASE
                                        )
                    
                    if 'RETURNING' in sql_str.upper():
                        # Encontrar la posición de RETURNING (case-insensitive)
                        sql_upper = sql_str.upper()
                        returning_pos = sql_upper.find('RETURNING')
                        if returning_pos != -1:
                            # Tomar solo la parte antes de RETURNING
                            sql_str = sql_str[:returning_pos].rstrip()
                            # Remover punto y coma final si existe
                            if sql_str.endswith(';'):
                                sql_str = sql_str[:-1]
                            # Mantener el tipo original (str o bytes)
                            if isinstance(sql, bytes):
                                sql = sql_str.encode('utf-8')
                            else:
                                sql = sql_str
                    
                    # Actualizar sql si fue modificado
                    if isinstance(sql, bytes) and not isinstance(sql_str, bytes):
                        sql = sql_str.encode('utf-8') if isinstance(sql_str, str) else sql_str
                    elif not isinstance(sql, bytes) and sql_str != sql:
                        sql = sql_str
                
                return original_execute(self, sql, params)
            
            CursorWrapper.execute = patched_execute
        
        # Parche 2: Parchear _save_table para manejar cuando results es None
        from django.db.models.base import Model
        
        if hasattr(Model, '_save_table'):
            original_save_table = Model._save_table
            
            def patched_save_table(self, *args, **kwargs):
                """Versión parcheada de _save_table que maneja RETURNING cuando results es None."""
                from django.db import connection
                
                # SIEMPRE deshabilitar RETURNING antes de guardar para MariaDB 10.4
                original_can_return = None
                if hasattr(connection, 'features') and hasattr(connection.features, 'can_return_columns_from_insert'):
                    original_can_return = connection.features.can_return_columns_from_insert
                    connection.features.can_return_columns_from_insert = False
                
                try:
                    result = original_save_table(self, *args, **kwargs)
                    return result
                except TypeError as e:
                    # Si el error es "'NoneType' object is not iterable" relacionado con RETURNING
                    error_str = str(e)
                    if "'NoneType' object is not iterable" in error_str or "returning_fields" in error_str or "results[0]" in error_str:
                        # Django intentó usar RETURNING pero MariaDB devolvió None
                        # Forzar que no use RETURNING y reintentar
                        if hasattr(connection, 'features') and hasattr(connection.features, 'can_return_columns_from_insert'):
                            connection.features.can_return_columns_from_insert = False
                        # Reintentar el guardado sin RETURNING
                        try:
                            return original_save_table(self, *args, **kwargs)
                        except Exception as retry_error:
                            # Si aún falla, lanzar el error original con más contexto
                            raise TypeError(f"Error al guardar modelo (RETURNING no soportado en MariaDB 10.4): {error_str}") from retry_error
                    else:
                        raise
                finally:
                    # Restaurar el valor original si existe
                    if original_can_return is not None and hasattr(connection, 'features'):
                        connection.features.can_return_columns_from_insert = original_can_return
            
            Model._save_table = patched_save_table
        
        # Parche 3: Deshabilitar RETURNING en el backend MySQL/MariaDB a nivel de clase
        try:
            from django.db.backends.mysql.features import DatabaseFeatures
            # Deshabilitar completamente RETURNING para todas las instancias
            DatabaseFeatures.can_return_columns_from_insert = False
        except:
            pass
        
        # Parche 4: También deshabilitar en la conexión activa si existe
        try:
            from django.db import connections
            for conn in connections.all():
                if hasattr(conn, 'features') and hasattr(conn.features, 'can_return_columns_from_insert'):
                    conn.features.can_return_columns_from_insert = False
        except:
            pass
        
        return True
    except Exception as e:
        # Silenciar errores durante la inicialización
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"No se pudo aplicar parche RETURNING completo: {e}")
        return False

# Aplicar el parche de forma lazy - se ejecutará cuando se importen los módulos
try:
    _apply_returning_patches()
except:
    pass

# -*- coding: utf-8 -*-