# dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # La ruta vacía ('') es la página principal (ej: http://127.0.0.1:8000/)
    path('', views.dashboard_view, name='dashboard'),
]