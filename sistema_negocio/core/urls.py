# core/urls.py

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from crm import views
from core.views import IosLoginView, set_precio_modo
from core import api_views
from core import jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('acceso/', IosLoginView.as_view(), name='login'),
    path('salir/', LogoutView.as_view(next_page='login'), name='logout'),
    path('set-precio-modo/', set_precio_modo, name='set_precio_modo'),
    path('admin/', admin.site.urls),
    path('chat/', include('crm.urls')),
    path('ventas/', include('ventas.urls')),
    path('inventario/', include('inventario.urls')),
    path('iphones/', include('iphones.urls')),
    path('historial/', include('historial.urls')),
    path('asistente_ia/', include('asistente_ia.urls')),
    path('configuracion/', include('configuracion.urls')),
    path('caja/', include('caja.urls')),
    path('', include('dashboard.urls')),
    path('webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
    
    # API REST para frontend e-commerce (mantener compatibilidad)
    path('api/configuraciones/', api_views.api_configuraciones, name='api_configuraciones'),
    path('api/categorias/', api_views.api_categorias, name='api_categorias'),
    path('api/proveedores/', api_views.api_proveedores, name='api_proveedores'),
    path('api/atributos/', api_views.api_atributos, name='api_atributos'),
    path('api/productos/', api_views.api_productos, name='api_productos'),
    path('api/productos/destacados/', api_views.api_productos_destacados, name='api_productos_destacados'),
    path('api/productos/<int:producto_id>/', api_views.api_producto_detalle, name='api_producto_detalle'),
    
    # JWT Authentication
    path('api/auth/login/', jwt_views.api_login_jwt, name='api_login_jwt'),
    path('api/auth/registro/', jwt_views.api_registro, name='api_registro'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/usuario/', jwt_views.api_usuario_actual_jwt, name='api_usuario_actual_jwt'),
    path('api/auth/perfil/', jwt_views.api_actualizar_perfil, name='api_actualizar_perfil'),
    
    # Carrito (actualizado para JWT)
    path('api/carrito/', api_views.api_carrito, name='api_carrito'),
    path('api/carrito/item/<int:item_index>/', api_views.api_carrito_item, name='api_carrito_item'),
    path('api/carrito/limpiar/', api_views.api_carrito_limpiar, name='api_carrito_limpiar'),
    path('api/pedido/', api_views.api_pedido_crear, name='api_pedido_crear'),
    
    # Nuevas funcionalidades
    path('api/direcciones/', jwt_views.api_direcciones, name='api_direcciones'),
    path('api/favoritos/', jwt_views.api_favoritos, name='api_favoritos'),
    path('api/favoritos/<int:producto_id>/', jwt_views.api_favoritos, name='api_favoritos_detail'),
    path('api/historial/', jwt_views.api_historial_pedidos, name='api_historial_pedidos'),
    path('api/solicitar-mayorista/', jwt_views.api_solicitar_mayorista, name='api_solicitar_mayorista'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
