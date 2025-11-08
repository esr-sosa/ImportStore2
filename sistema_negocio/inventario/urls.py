from django.urls import path
from .views import inventario_dashboard, producto_crear, variante_editar

app_name = "inventario"

urlpatterns = [
    path("", inventario_dashboard, name="dashboard"),
    path("nuevo/", producto_crear, name="producto_crear"),
    path("variantes/<int:pk>/editar/", variante_editar, name="variante_editar"),
]
