from django.urls import path

from . import views

app_name = "caja"

urlpatterns = [
    path("apertura/", views.vista_apertura, name="apertura"),
    path("cierre/", views.vista_cierre, name="cierre"),
    path("cierre/<int:caja_id>/", views.vista_cierre, name="cierre_detalle"),
    path("listado/", views.listado_cajas, name="listado"),
]

