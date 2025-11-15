# asistente_ia/urls.py

from django.urls import path
from . import views
from . import management_views

app_name = 'asistente_ia'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('ask/', views.ask_question, name='ask_question'),
    path('threads/', views.list_threads, name='list_threads'),
    path('threads/create/', views.create_thread, name='create_thread'),
    path('threads/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('quick-replies/', views.quick_replies_catalogue, name='quick_replies'),
    path('playbooks/<int:pk>/', views.playbook_detail, name='playbook_detail'),
    
    # Gestión de recursos
    path('manage/quick-replies/', management_views.manage_quick_replies, name='manage_quick_replies'),
    path('manage/quick-replies/create/', management_views.quick_reply_create, name='quick_reply_create'),
    path('manage/quick-replies/<int:pk>/update/', management_views.quick_reply_update, name='quick_reply_update'),
    path('manage/quick-replies/<int:pk>/delete/', management_views.quick_reply_delete, name='quick_reply_delete'),
    
    path('manage/playbooks/', management_views.manage_playbooks, name='manage_playbooks'),
    path('manage/playbooks/create/', management_views.playbook_create, name='playbook_create'),
    path('manage/playbooks/<int:pk>/update/', management_views.playbook_update, name='playbook_update'),
    path('manage/playbooks/<int:pk>/delete/', management_views.playbook_delete, name='playbook_delete'),
    
    path('manage/knowledge/', management_views.manage_knowledge, name='manage_knowledge'),
    path('manage/knowledge/create/', management_views.knowledge_create, name='knowledge_create'),
    path('manage/knowledge/<int:pk>/update/', management_views.knowledge_update, name='knowledge_update'),
    path('manage/knowledge/<int:pk>/delete/', management_views.knowledge_delete, name='knowledge_delete'),
    
    # Procesamiento de listados de proveedores
    path('aplicar-stock-proveedor/', views.aplicar_stock_proveedor, name='aplicar_stock_proveedor'),
    
    # Obtener mensajes de un thread
    path('threads/<int:thread_id>/messages/', views.thread_messages, name='thread_messages'),
]
