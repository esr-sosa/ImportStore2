# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Conecta las URLs de cada una de nuestras apps
    path('chat/', include('crm.urls')),
    path('ventas/', include('ventas.urls')),
    path('inventario/', include('inventario.urls')),
    path('iphones/', include('iphones.urls')), # <--- AÑADIR ESTA LÍNEA
    path('', include('dashboard.urls')),
]

# Configuración para servir archivos de imágenes en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
