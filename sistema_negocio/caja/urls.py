from django.urls import path

from . import views

app_name = "caja"

urlpatterns = [
    path("", views.vista_caja, name="caja"),  # Vista combinada
    path("apertura/", views.vista_apertura, name="apertura"),  # Legacy redirect
    path("cierre/", views.vista_cierre, name="cierre"),  # Legacy redirect
    path("cierre/<int:caja_id>/", views.vista_cierre, name="cierre_detalle"),  # Legacy redirect
    path("listado/", views.listado_cajas, name="listado"),
]

