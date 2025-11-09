from __future__ import annotations

import getpass
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email


class Command(BaseCommand):
    """Create or update a superuser pulling defaults from the environment."""

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
            help=(
                "Evita cualquier prompt interactivo. Requiere que la contraseña se "
                "proporcione por argumento o variable de entorno."
            ),
        )

    def handle(self, *args: Any, **options: Any) -> None:
        user_model = get_user_model()

        username = options.get("username") or getattr(settings, "DJANGO_SUPERUSER_USERNAME", None)
        email = options.get("email") or getattr(settings, "DJANGO_SUPERUSER_EMAIL", None)
        password = options.get("password") or getattr(settings, "DJANGO_SUPERUSER_PASSWORD", None)
        noinput = bool(options.get("noinput"))

        missing_fields = [name for name, value in (("username", username), ("email", email)) if not value]
        if missing_fields:
            raise CommandError(
                "Faltan los siguientes datos del superusuario: {}. Proporcionalos "
                "mediante argumentos o variables de entorno.".format(
                    ", ".join(missing_fields)
                )
            )

        # Valida el correo electrónico y, si es posible, permite corregirlo en modo interactivo.
        while True:
            try:
                validate_email(email)
                break
            except ValidationError:
                if noinput:
                    raise CommandError(
                        "El correo electrónico proporcionado ('{}') no es válido. Proporciona uno válido "
                        "mediante --email o DJANGO_SUPERUSER_EMAIL.".format(email)
                    )
                email = input("Correo electrónico válido para '{}': ").strip()
                if not email:
                    self.stdout.write(self.style.WARNING("El correo no puede quedar vacío."))
                    continue

        if not password:
            if noinput:
                raise CommandError(
                    "No se recibió contraseña. Usa --password o DJANGO_SUPERUSER_PASSWORD cuando se ejecuta con --noinput."
                )
            password = getpass.getpass(f"Contraseña para '{username}': ")
            confirmation = getpass.getpass("Confirmar contraseña: ")
            if password != confirmation:
                raise CommandError("Las contraseñas no coinciden. Vuelve a ejecutar el comando.")

        user, created = user_model.objects.update_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        user.set_password(password)
        user.full_clean(exclude={"password"})
        user.save(update_fields=["password", "email", "is_staff", "is_superuser", "is_active"])

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado correctamente."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Datos de acceso de '{username}' actualizados correctamente."))
