# asistente_ia/urls.py

from django.urls import path
from . import views

app_name = 'asistente_ia'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('ask/', views.ask_question, name='ask_question'),
]
