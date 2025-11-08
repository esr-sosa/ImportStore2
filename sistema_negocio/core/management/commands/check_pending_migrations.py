from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand, CommandError

from core.checks import databases_with_pending_migrations


class Command(BaseCommand):
    """Verifica si existen migraciones pendientes y falla si encuentra alguna."""

    help = "Verifica si existen migraciones pendientes en las bases de datos configuradas."

    def handle(self, *args: Any, **options: Any) -> None:
        pending, errors = databases_with_pending_migrations()

        for alias, exc in errors.items():
            self.stderr.write(
                self.style.WARNING(
                    f"No se pudo validar completamente la base de datos '{alias}': {exc}"
                )
            )

        if pending:
            aliases = ", ".join(sorted(set(pending)))
            raise CommandError(
                f"Existen migraciones pendientes en las bases de datos: {aliases}. Ejecuta 'python manage.py migrate'."
            )

        self.stdout.write(self.style.SUCCESS("No hay migraciones pendientes."))
