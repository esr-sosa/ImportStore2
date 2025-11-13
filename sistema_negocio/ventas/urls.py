from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path("pos/", views.pos_view, name="pos"),
    path("pos-remoto/", views.pos_remoto_view, name="pos_remoto"),
    path("escaner-productos/", views.escaner_productos_view, name="escaner_productos"),
    path("listado/", views.listado_ventas, name="listado"),
    path("detalle/<str:venta_id>/", views.detalle_venta, name="detalle"),
    path("anular/<str:venta_id>/", views.anular_venta, name="anular"),
    path("actualizar-estado/<str:venta_id>/", views.actualizar_estado_venta, name="actualizar_estado"),
    path("voucher/<str:venta_id>/", views.generar_voucher_pdf, name="voucher"),
    path("api/buscar-productos/", views.buscar_productos_api, name="buscar_productos_api"),
    path("api/buscar-producto-codigo/", views.buscar_producto_por_codigo_api, name="buscar_producto_codigo_api"),
    path("api/actualizar-producto-rapido/", views.actualizar_producto_rapido_api, name="actualizar_producto_rapido_api"),
    path("api/agregar-carrito-remoto/", views.agregar_producto_carrito_remoto_api, name="agregar_carrito_remoto_api"),
    path("api/obtener-carrito-remoto/", views.obtener_carrito_remoto_api, name="obtener_carrito_remoto_api"),
    path("api/limpiar-carrito-remoto/", views.limpiar_carrito_remoto_api, name="limpiar_carrito_remoto_api"),
    path("api/buscar-clientes/", views.buscar_clientes_api, name="buscar_clientes_api"),
    path("api/crear/", views.crear_venta_api, name="crear_venta_api"),
    path("api/ultima-venta/", views.ultima_venta_api, name="ultima_venta_api"),
]
