from django.urls import path
from .views import inventario_dashboard

app_name = "inventario"

urlpatterns = [
    path("", inventario_dashboard, name="dashboard"),
]
