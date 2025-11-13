from django.urls import path
from .views import (
    inventario_dashboard,
    inventario_exportar,
    inventario_importar,
    maestros,
    proveedor_toggle_activo,
    producto_crear,
    variante_editar,
    descargar_etiqueta,
    descargar_etiquetas_multiples,
    descargar_etiquetas_categoria,
)

app_name = "inventario"

urlpatterns = [
    path("", inventario_dashboard, name="dashboard"),
    path("nuevo/", producto_crear, name="producto_crear"),
    path("variantes/<int:pk>/editar/", variante_editar, name="variante_editar"),
    path("importar/", inventario_importar, name="importar"),
    path("exportar/", inventario_exportar, name="exportar"),
    path("maestros/", maestros, name="maestros"),
    path("proveedores/<int:pk>/toggle/", proveedor_toggle_activo, name="proveedor_toggle"),
    path("etiquetas/<int:variante_id>/", descargar_etiqueta, name="descargar_etiqueta"),
    path("etiquetas/multiples/", descargar_etiquetas_multiples, name="descargar_etiquetas_multiples"),
    path("etiquetas/categoria/<int:categoria_id>/", descargar_etiquetas_categoria, name="descargar_etiquetas_categoria"),
]
