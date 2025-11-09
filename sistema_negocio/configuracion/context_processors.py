def configuracion_global(request):
    """Inyecta la configuración global y preferencias visuales en cada plantilla."""

    from types import SimpleNamespace

    configuracion = None
    preferencia_usuario = None
    modo_oscuro_usuario = None

    try:
        from .models import ConfiguracionSistema, PreferenciaUsuario

        configuracion = ConfiguracionSistema.carga()

        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            try:
                preferencia_usuario = (
                    PreferenciaUsuario.objects.select_related(None)
                    .only("usa_modo_oscuro")
                    .filter(usuario=user)
                    .first()
                )
                if preferencia_usuario is not None:
                    modo_oscuro_usuario = preferencia_usuario.usa_modo_oscuro
            except Exception:
                preferencia_usuario = None
                modo_oscuro_usuario = None
    except Exception:
        configuracion = SimpleNamespace(
            nombre_comercial="ImportStore",
            lema="",
            logo=None,
            color_principal="#2563eb",
            modo_oscuro_predeterminado=False,
        )

    return {
        "configuracion_sistema": configuracion,
        "preferencia_usuario": preferencia_usuario,
        "modo_oscuro_usuario": modo_oscuro_usuario,
        "modo_oscuro_predeterminado": getattr(
            configuracion, "modo_oscuro_predeterminado", False
        ),
    }
