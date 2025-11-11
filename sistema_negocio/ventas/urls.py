from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path("pos/", views.pos_view, name="pos"),
    path("listado/", views.listado_ventas, name="listado"),
    path("api/buscar-productos/", views.buscar_productos_api, name="buscar_productos_api"),
    path("api/crear", views.crear_venta_api, name="crear_venta_api"),
]
