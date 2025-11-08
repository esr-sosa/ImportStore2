from __future__ import annotations

from functools import lru_cache

from django.db import connection


@lru_cache(maxsize=1)
def is_detalleiphone_variante_ready() -> bool:
    """Return True when the DetalleIphone.variante column exists in the DB."""
    table = "inventario_detalleiphone"

    with connection.cursor() as cursor:
        tables = connection.introspection.table_names(cursor)
    if table not in tables:
        return False

    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, table)

    for column in description:
        if column.name == "variante_id":
            return True
    return False


def reset_detalleiphone_ready_cache() -> None:
    """Clear the cached result after running migrations."""
    is_detalleiphone_variante_ready.cache_clear()
