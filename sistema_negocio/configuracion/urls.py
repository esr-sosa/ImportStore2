from django.urls import path

from . import views

app_name = "configuracion"

urlpatterns = [
    path("", views.panel_configuracion, name="panel"),
    path("toggle-tema/", views.toggle_modo_oscuro, name="toggle_tema"),
    path("locales/<int:pk>/eliminar/", views.eliminar_local, name="local_eliminar"),
    path("categorias/<int:categoria_id>/garantia/", views.actualizar_garantia_categoria, name="categoria_garantia"),
    path("escalas/crear/", views.crear_escala_precio, name="escala_crear"),
    path("escalas/<int:escala_id>/editar/", views.editar_escala_precio, name="escala_editar"),
    path("escalas/<int:escala_id>/eliminar/", views.eliminar_escala_precio, name="escala_eliminar"),
]
