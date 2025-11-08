from __future__ import annotations

import getpass
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea o actualiza un superusuario usando argumentos o variables de entorno."

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--username", dest="username", help="Nombre de usuario del superusuario.")
        parser.add_argument("--email", dest="email", help="Correo electrónico del superusuario.")
        parser.add_argument(
            "--password",
            dest="password",
            help="Contraseña a asignar. Si no se proporciona, se solicitará de forma interactiva.",
        )
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Evita cualquier prompt interactivo. Requiere que password se proporcione por argumento o variable de entorno.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        user_model = get_user_model()

        username = options.get("username") or getattr(settings, "DJANGO_SUPERUSER_USERNAME", None)
        email = options.get("email") or getattr(settings, "DJANGO_SUPERUSER_EMAIL", None)
        password = options.get("password") or getattr(settings, "DJANGO_SUPERUSER_PASSWORD", None)
        noinput = bool(options.get("noinput"))

        missing_fields = [
            name
            for name, value in (("username", username), ("email", email))
            if not value
        ]
        if missing_fields:
            raise CommandError(
                "Faltan los siguientes datos del superusuario: {}."
                " Proporciónalos mediante argumentos o variables de entorno.".format(
                    ", ".join(missing_fields)
                )
            )

        if not password:
            if noinput:
                raise CommandError(
                    "No se recibió contraseña. Usa --password o DJANGO_SUPERUSER_PASSWORD cuando se ejecuta con --noinput."
                )
            password = getpass.getpass("Contraseña para '{}': ".format(username))
            confirmation = getpass.getpass("Confirmar contraseña: ")
            if password != confirmation:
                raise CommandError("Las contraseñas no coinciden. Vuelve a ejecutar el comando.")

        user, created = user_model.objects.update_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.set_password(password)
        user.full_clean(exclude={"password"})
        user.save(update_fields=["password", "email", "is_staff", "is_superuser"])

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado correctamente."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Datos de acceso de '{username}' actualizados correctamente."))
