# core/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import crm.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Importante: get_asgi_application() debe llamarse antes de importar el enrutado
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            crm.routing.websocket_urlpatterns
        )
    ),
})