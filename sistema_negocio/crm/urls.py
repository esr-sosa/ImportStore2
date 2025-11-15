# crm/urls.py
from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # --- Rutas de la Interfaz y API ---
    path('', views.panel_chat, name='panel_chat'),
    path('clientes/', views.clientes_panel, name='clientes'),
    path('clientes/<int:cliente_id>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),
    path('api/conversacion/<int:conv_id>/', views.get_conversacion_details, name='get_conversacion_details'),
    path('api/conversacion/<int:conv_id>/actualizar/', views.actualizar_conversacion, name='actualizar_conversacion'),
    path('api/enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    
    # --- ¡RUTAS DE IA CORREGIDAS Y FUNCIONALES! ---
    path('api/sugerir-respuesta/', views.sugerir_respuesta_ia, name='sugerir_respuesta_ia'),
    path('api/resumir-chat/', views.resumir_chat_ia, name='resumir_chat_ia'),
    
    # --- Acciones rápidas ---
    path('api/buscar-productos/', views.buscar_productos_api, name='buscar_productos_api'),
    path('api/enviar-producto/', views.enviar_producto_chat, name='enviar_producto_chat'),
    path('api/crear-cotizacion/', views.crear_cotizacion_api, name='crear_cotizacion_api'),
    path('api/conversacion/<int:conv_id>/contexto/', views.obtener_contexto_cliente_api, name='obtener_contexto_cliente_api'),
    path('api/conversacion/<int:conv_id>/reiniciar/', views.reiniciar_conversacion_api, name='reiniciar_conversacion_api'),
]