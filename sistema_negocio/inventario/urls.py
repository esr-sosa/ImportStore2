# inventario/urls.py

from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Ruta para el listado principal del inventario
    path('', views.inventario_dashboard, name='dashboard'),
    
    # --- ¡ESTA ES LA RUTA QUE FALTABA! ---
    # Ruta para la página de agregar un nuevo producto
    path('producto/nuevo/', views.agregar_producto, name='agregar_producto'),
]