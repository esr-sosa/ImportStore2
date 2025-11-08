"""Checks y utilidades de verificación para la app core."""

from __future__ import annotations

from typing import Dict, List, Tuple

from django.core.checks import Error, Warning, register, Tags
from django.db import connections
from django.db.migrations.exceptions import InconsistentMigrationHistory, MigrationSchemaMissing
from django.db.migrations.executor import MigrationExecutor
from django.db.utils import OperationalError


def databases_with_pending_migrations() -> Tuple[List[str], Dict[str, Exception]]:
    """Devuelve las bases de datos con migraciones pendientes y errores detectados."""

    pending: List[str] = []
    errors: Dict[str, Exception] = {}

    for alias in connections:
        connection = connections[alias]
        engine = connection.settings_dict.get("ENGINE", "")
        if engine.endswith("dummy"):
            # Se ignoran las conexiones dummy utilizadas para pruebas.
            continue

        try:
            executor = MigrationExecutor(connection)
        except OperationalError as exc:
            errors[alias] = exc
            continue

        try:
            targets = executor.loader.graph.leaf_nodes()
            plan = executor.migration_plan(targets)
        except (MigrationSchemaMissing, InconsistentMigrationHistory) as exc:
            # Si falta la tabla de migraciones o hay inconsistencia, se considera pendiente.
            pending.append(alias)
            errors.setdefault(alias, exc)
            continue

        if plan:
            pending.append(alias)

    return pending, errors


@register(Tags.database)
def check_pending_migrations(app_configs=None, **kwargs):  # type: ignore[override]
    """Sistema de checks para avisar migraciones pendientes en cualquier base."""

    pending, errors = databases_with_pending_migrations()
    messages = []

    for alias, exc in errors.items():
        messages.append(
            Warning(
                f"No se pudo validar completamente la base de datos '{alias}': {exc}",
                hint="Verifica la conexión y vuelve a ejecutar el chequeo.",
                id="core.W001",
            )
        )

    if pending:
        aliases = ", ".join(sorted(set(pending)))
        messages.append(
            Error(
                f"Existen migraciones pendientes en las bases de datos: {aliases}.",
                hint="Ejecuta `python manage.py migrate` para aplicar los cambios.",
                id="core.E001",
            )
        )

    return messages


__all__ = ["databases_with_pending_migrations", "check_pending_migrations"]
