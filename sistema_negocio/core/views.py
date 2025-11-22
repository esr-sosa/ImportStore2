from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from configuracion.models import ConfiguracionSistema, ConfiguracionTienda


class IosLoginView(LoginView):
    """
    Pantalla de acceso con estética iOS 16/17, utilizando las credenciales
    estándar de Django (usuario/contraseña).
    """

    template_name = "auth/login.html"
    redirect_authenticated_user = True
    extra_context = {"page_title": "Ingresá a ImportStore"}

    def get_success_url(self):
        # Respetar el parámetro ?next= si existe, de lo contrario el dashboard.
        return self.get_redirect_url() or reverse_lazy("dashboard:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tienda = ConfiguracionTienda.obtener_unica()
        sistema = ConfiguracionSistema.obtener_unica()

        # Obtener logo de forma segura
        store_logo = None
        if tienda.logo:
            try:
                store_logo = tienda.logo.url
            except (ValueError, AttributeError):
                pass
        if not store_logo and sistema.logo:
            try:
                store_logo = sistema.logo.url
            except (ValueError, AttributeError):
                pass

        context.update(
            {
                "store_name": tienda.nombre_tienda or sistema.nombre_comercial or "ImportStore",
                "store_tagline": sistema.lema or "Panel táctil para ventas inteligentes",
                "store_logo": store_logo,
            }
        )
        return context

    def form_valid(self, form):
        """
        Permitir "Recordarme": si se marca, la sesión dura 30 días; si no,
        se cierra al salir del navegador.
        """
        remember = self.request.POST.get("remember") == "on"
        response = super().form_valid(form)
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # 30 días
        else:
            self.request.session.set_expiry(0)
        return response


@require_POST
@login_required
def set_precio_modo(request):
    """Establece el modo de precio (Minorista/Mayorista) en la sesión del usuario."""
    modo = request.POST.get("modo", "MINORISTA").upper()
    
    # Validar que el modo sea válido
    if modo not in ["MINORISTA", "MAYORISTA"]:
        return JsonResponse({"error": "Modo inválido"}, status=400)
    
    # Guardar en la sesión
    request.session["modo_precio"] = modo
    
    return JsonResponse({"status": "ok", "modo": modo})

