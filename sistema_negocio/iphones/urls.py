# iphones/urls.py

from django.urls import path
from . import views

app_name = 'iphones'

urlpatterns = [
    path('', views.iphone_dashboard, name='dashboard'),
]
