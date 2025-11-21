# dashboard/urls.py

from django.urls import path
from . import views
from . import views_solicitudes
from . import views_notificaciones

app_name = 'dashboard'

urlpatterns = [
    # La ruta vacía ('') es la página principal (ej: http://127.0.0.1:8000/)
    path('', views.dashboard_view, name='dashboard'),
    path('preview/', views.tienda_preview, name='tienda_preview'),
    
    # Solicitudes Mayoristas
    path('solicitudes-mayoristas/', views_solicitudes.solicitudes_mayoristas_list, name='solicitudes_mayoristas'),
    path('solicitudes-mayoristas/<int:solicitud_id>/aprobar/', views_solicitudes.aprobar_solicitud_mayorista, name='aprobar_solicitud_mayorista'),
    path('solicitudes-mayoristas/<int:solicitud_id>/rechazar/', views_solicitudes.rechazar_solicitud_mayorista, name='rechazar_solicitud_mayorista'),
    
    # Notificaciones
    path('notificaciones/', views_notificaciones.notificaciones_view, name='notificaciones'),
    path('notificaciones/<int:notificacion_id>/marcar-leida/', views_notificaciones.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones/marcar-todas-leidas/', views_notificaciones.marcar_todas_leidas, name='marcar_todas_leidas'),
]
