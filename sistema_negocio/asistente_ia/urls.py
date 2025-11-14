# asistente_ia/urls.py

from django.urls import path
from . import views

app_name = 'asistente_ia'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('ask/', views.ask_question, name='ask_question'),
    path('quick-replies/', views.quick_replies_catalogue, name='quick_replies'),
    path('playbooks/<int:pk>/', views.playbook_detail, name='playbook_detail'),
]
