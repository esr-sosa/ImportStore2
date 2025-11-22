from types import SimpleNamespace


def configuracion_global(request):
    """Inyecta configuraciones globales y preferencias del usuario en cada plantilla."""

    configuracion_tienda = None
    configuracion_sistema = None
    preferencia_usuario = None
    modo_oscuro_usuario = None

    try:
        from .models import ConfiguracionTienda  # type: ignore

        configuracion_tienda = ConfiguracionTienda.obtener_unica()
    except Exception:
        configuracion_tienda = None

    try:
        from .models import ConfiguracionSistema, PreferenciaUsuario

        configuracion_sistema = ConfiguracionSistema.obtener_unica()

        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            preferencia_usuario = (
                PreferenciaUsuario.objects.only("usa_modo_oscuro")
                .filter(usuario=user)
                .first()
            )
            if preferencia_usuario is not None:
                modo_oscuro_usuario = preferencia_usuario.usa_modo_oscuro
    except Exception:
        configuracion_sistema = SimpleNamespace(
            nombre_comercial="ImportStore",
            lema="",
            logo=None,
            color_principal="#2563eb",
            modo_oscuro_predeterminado=False,
        )

    if configuracion_tienda is None:
        configuracion_tienda = SimpleNamespace(
            nombre_tienda=getattr(configuracion_sistema, "nombre_comercial", "ImportStore"),
            logo=getattr(configuracion_sistema, "logo", None),
            cuit="",
            direccion=getattr(configuracion_sistema, "domicilio_comercial", ""),
            email_contacto=getattr(configuracion_sistema, "contacto_email", ""),
            telefono_contacto="",
        )

    return {
        "configuracion_tienda": configuracion_tienda,
        "configuracion_sistema": configuracion_sistema,
        "preferencia_usuario": preferencia_usuario,
        "modo_oscuro_usuario": modo_oscuro_usuario,
        "modo_oscuro_predeterminado": getattr(
            configuracion_sistema, "modo_oscuro_predeterminado", False
        ),
    }
