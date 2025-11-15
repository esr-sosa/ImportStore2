from django.urls import path
from .views import (
    inventario_dashboard,
    inventario_exportar,
    inventario_importar,
    maestros,
    categoria_eliminar,
    proveedor_toggle_activo,
    producto_crear,
    remove_background_api,
    variante_editar,
    variante_toggle_activo,
    descargar_etiqueta,
    descargar_etiquetas_multiples,
    descargar_etiquetas_categoria,
    generar_descripcion_ia_api,
    actualizar_stock_rapido_api,
    actualizar_precio_rapido_api,
)

app_name = "inventario"

urlpatterns = [
    path("", inventario_dashboard, name="dashboard"),
    path("nuevo/", producto_crear, name="producto_crear"),
    path("variantes/<int:pk>/editar/", variante_editar, name="variante_editar"),
    path("variantes/<int:pk>/toggle/", variante_toggle_activo, name="variante_toggle_activo"),
    path("importar/", inventario_importar, name="importar"),
    path("exportar/", inventario_exportar, name="exportar"),
    path("maestros/", maestros, name="maestros"),
    path("categorias/<int:pk>/eliminar/", categoria_eliminar, name="categoria_eliminar"),
    path("proveedores/<int:pk>/toggle/", proveedor_toggle_activo, name="proveedor_toggle"),
    path("etiquetas/<int:variante_id>/", descargar_etiqueta, name="descargar_etiqueta"),
    path("etiquetas/multiples/", descargar_etiquetas_multiples, name="descargar_etiquetas_multiples"),
    path("etiquetas/categoria/<int:categoria_id>/", descargar_etiquetas_categoria, name="descargar_etiquetas_categoria"),
    path("api/remove-background/", remove_background_api, name="remove_background_api"),
    path("api/generar-descripcion-ia/", generar_descripcion_ia_api, name="generar_descripcion_ia_api"),
    path("api/actualizar-stock/", actualizar_stock_rapido_api, name="actualizar_stock_rapido_api"),
    path("api/actualizar-precio/", actualizar_precio_rapido_api, name="actualizar_precio_rapido_api"),
]
