# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('crm.urls')),
    path('ventas/', include('ventas.urls')),
    path('inventario/', include('inventario.urls')),
    path('iphones/', include('iphones.urls')),
    path('historial/', include('historial.urls')),
    path('asistente_ia/', include('asistente_ia.urls')),
    path('configuracion/', include('configuracion.urls')),
    path('caja/', include('caja.urls')),
    path('', include('dashboard.urls')),
    path('webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
