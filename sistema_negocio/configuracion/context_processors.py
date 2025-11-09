def configuracion_global(request):
    """Inyecta la configuración global del sistema en cada plantilla."""
    from types import SimpleNamespace

    try:
        from .models import ConfiguracionSistema

        configuracion = ConfiguracionSistema.carga()
    except Exception:
        configuracion = SimpleNamespace(
            nombre_comercial="ImportStore",
            lema="",
            logo=None,
            color_principal="#2563eb",
        )
    return {
        "configuracion_sistema": configuracion,
    }
