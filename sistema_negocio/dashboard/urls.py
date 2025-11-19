# dashboard/urls.py

from django.urls import path
from . import views
from . import views_solicitudes

app_name = 'dashboard'

urlpatterns = [
    # La ruta vacía ('') es la página principal (ej: http://127.0.0.1:8000/)
    path('', views.dashboard_view, name='dashboard'),
    path('preview/', views.tienda_preview, name='tienda_preview'),
    
    # Solicitudes Mayoristas
    path('solicitudes-mayoristas/', views_solicitudes.solicitudes_mayoristas_list, name='solicitudes_mayoristas'),
    path('solicitudes-mayoristas/<int:solicitud_id>/aprobar/', views_solicitudes.aprobar_solicitud_mayorista, name='aprobar_solicitud_mayorista'),
    path('solicitudes-mayoristas/<int:solicitud_id>/rechazar/', views_solicitudes.rechazar_solicitud_mayorista, name='rechazar_solicitud_mayorista'),
]
