# iphones/urls.py

from django.urls import path
from . import views

app_name = 'iphones'

urlpatterns = [
    path('', views.iphone_dashboard, name='dashboard'),
    path('agregar/', views.agregar_iphone, name='agregar_iphone'),
    path('editar/<int:variante_id>/', views.editar_iphone, name='editar_iphone'),
    
    # --- ¡NUEVAS RUTAS DE ACCIÓN! ---
    path('eliminar/<int:variante_id>/', views.eliminar_iphone, name='eliminar_iphone'),
    path('toggle-status/<int:variante_id>/', views.toggle_iphone_status, name='toggle_iphone_status'),
    path('historial/', views.iphone_historial, name='historial'),
    path('etiqueta/<int:detalle_id>/', views.descargar_etiqueta_iphone, name='descargar_etiqueta_iphone'),
    
    # Plan Canje
    path('plan-canje/', views.plan_canje_calculadora, name='plan_canje_calculadora'),
    path('plan-canje/calcular/', views.plan_canje_calcular_api, name='plan_canje_calcular_api'),
    path('plan-canje/aplicar/', views.plan_canje_aplicar_api, name='plan_canje_aplicar_api'),
    path('plan-canje/config/', views.plan_canje_config, name='plan_canje_config'),
    path('plan-canje/config/guardar/', views.plan_canje_config_guardar_api, name='plan_canje_config_guardar_api'),
    path('plan-canje/config/<int:config_id>/', views.plan_canje_config_obtener_api, name='plan_canje_config_obtener_api'),
    path('plan-canje/config/<int:config_id>/eliminar/', views.plan_canje_config_eliminar_api, name='plan_canje_config_eliminar_api'),
    path('plan-canje/config/precargar/', views.plan_canje_precargar_modelos_api, name='plan_canje_precargar_modelos_api'),
    path('plan-canje/historial/', views.plan_canje_historial, name='plan_canje_historial'),
]