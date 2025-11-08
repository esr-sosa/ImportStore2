from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        # Importa los checks para que se registren cuando la app se carga.
        from . import checks  # noqa: F401


__all__ = ["CoreConfig"]
