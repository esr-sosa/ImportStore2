from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # --- Rutas existentes ---
    path('', views.panel_chat, name='panel_chat'),
    path('api/conversacion/<int:conv_id>/', views.get_conversacion_details, name='get_conversacion_details'),
    path('api/enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    
    # --- ¡NUEVA RUTA DE IA AÑADIDA AQUÍ! ---
    # Esta es la dirección que usará el botón de "Resumir"
    path('api/resumir_chat/', views.resumir_chat_ia, name='resumir_chat_ia'),
]

