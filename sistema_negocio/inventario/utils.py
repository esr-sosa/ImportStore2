from __future__ import annotations

from functools import lru_cache

from core.db_inspector import column_exists


@lru_cache(maxsize=1)
def is_detalleiphone_variante_ready() -> bool:
    """Return True when the DetalleIphone.variante column exists in the DB."""
    return column_exists("inventario_detalleiphone", "variante_id")


def reset_detalleiphone_ready_cache() -> None:
    """Clear the cached result after running migrations."""
    is_detalleiphone_variante_ready.cache_clear()
