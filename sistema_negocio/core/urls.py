from django.contrib import admin
# ¡Añadimos 'include' para poder conectar las URLs de nuestra app!
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- ¡ESTA ES LA LÍNEA MÁGICA! ---
    # Le decimos a Django: "Cualquier dirección que empiece con 'chat/', 
    # envíala al mapa de calles que definimos en nuestra app 'crm'".
    path('chat/', include('crm.urls')),
]

