from __future__ import annotations

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from core.checks import databases_with_pending_migrations


class MigrationChecksTests(TestCase):
    databases = {"default"}

    def test_databases_without_pending_migrations(self) -> None:
        pending, errors = databases_with_pending_migrations()
        self.assertFalse(pending, "No deberían existir migraciones pendientes durante las pruebas.")
        self.assertFalse(errors, "No deberían registrarse errores al verificar migraciones.")

    def test_management_command_reports_success(self) -> None:
        stdout = StringIO()
        call_command("check_pending_migrations", stdout=stdout)
        self.assertIn("No hay migraciones pendientes.", stdout.getvalue())
