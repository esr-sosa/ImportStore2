from django.urls import path

from . import views

app_name = "configuracion"

urlpatterns = [
    path("", views.panel_configuracion, name="panel"),
    path("toggle-tema/", views.toggle_modo_oscuro, name="toggle_tema"),
    path("locales/<int:pk>/eliminar/", views.eliminar_local, name="local_eliminar"),
    path("categorias/<int:categoria_id>/garantia/", views.actualizar_garantia_categoria, name="categoria_garantia"),
]
