"""Utilidades de introspección de la base de datos."""

from __future__ import annotations

from functools import lru_cache

from django.db import connection


@lru_cache(maxsize=None)
def table_exists(table_name: str) -> bool:
    """Devuelve True si la tabla existe en la base de datos actual."""
    table_name = table_name.lower()
    with connection.cursor() as cursor:
        tables = {name.lower() for name in connection.introspection.table_names(cursor)}
    return table_name in tables


@lru_cache(maxsize=None)
def column_exists(table_name: str, column_name: str) -> bool:
    """Indica si una columna está presente en la tabla dada."""
    if not table_exists(table_name):
        return False

    column_name = column_name.lower()
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, table_name)

    for column in description:
        if column.name.lower() == column_name:
            return True
    return False


def reset_caches() -> None:
    """Limpia el caché tras ejecutar migraciones."""
    table_exists.cache_clear()
    column_exists.cache_clear()
