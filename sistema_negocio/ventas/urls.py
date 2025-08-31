# ventas/urls.py

from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('pos/', views.pos_view, name='pos'),
     # --- ¡NUEVA RUTA AÑADIDA AQUÍ! ---
    path('api/buscar-productos/', views.buscar_productos_api, name='buscar_productos_api'),
]