from django.urls import path

from . import views

app_name = "configuracion"

urlpatterns = [
    path("", views.panel_configuracion, name="panel"),
]
