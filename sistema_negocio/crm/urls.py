# crm/urls.py
from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # --- Rutas de la Interfaz y API ---
    path('', views.panel_chat, name='panel_chat'),
    path('api/conversacion/<int:conv_id>/', views.get_conversacion_details, name='get_conversacion_details'),
    path('api/conversacion/<int:conv_id>/actualizar/', views.actualizar_conversacion, name='actualizar_conversacion'),
    path('api/enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    
    # --- ¡RUTAS DE IA CORREGIDAS Y FUNCIONALES! ---
    path('api/sugerir-respuesta/', views.sugerir_respuesta_ia, name='sugerir_respuesta_ia'),
    path('api/resumir-chat/', views.resumir_chat_ia, name='resumir_chat_ia'),
]