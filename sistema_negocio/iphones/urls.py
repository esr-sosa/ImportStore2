# iphones/urls.py

from django.urls import path
from . import views

app_name = 'iphones'

urlpatterns = [
    path('', views.iphone_dashboard, name='dashboard'),
    path('agregar/', views.agregar_iphone, name='agregar_iphone'),
    path('editar/<int:variante_id>/', views.editar_iphone, name='editar_iphone'),
    
    # --- ¡NUEVAS RUTAS DE ACCIÓN! ---
    path('eliminar/<int:variante_id>/', views.eliminar_iphone, name='eliminar_iphone'),
    path('toggle-status/<int:producto_id>/', views.toggle_iphone_status, name='toggle_iphone_status'),
]