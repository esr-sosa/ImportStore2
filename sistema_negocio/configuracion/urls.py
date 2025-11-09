from django.urls import path

from . import views

app_name = "configuracion"

urlpatterns = [
    path("", views.panel_configuracion, name="panel"),
    path("toggle-tema/", views.toggle_modo_oscuro, name="toggle_tema"),
]
