"""
Script para probar que el webhook de WhatsApp esté funcionando correctamente
Ejecutar: python test_webhook.py
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from crm.models import Cliente, Conversacion, Mensaje

print("=" * 70)
print("PRUEBA DEL WEBHOOK DE WHATSAPP")
print("=" * 70)
print()

# Verificar configuración
print("1. Verificando configuración...")
print("-" * 70)

config_ok = True

if not settings.WHATSAPP_ACCESS_TOKEN:
    print("[ERROR] WHATSAPP_ACCESS_TOKEN no está configurado")
    config_ok = False
else:
    print(f"[OK] WHATSAPP_ACCESS_TOKEN: {settings.WHATSAPP_ACCESS_TOKEN[:20]}...")

if not settings.WHATSAPP_PHONE_NUMBER_ID:
    print("[ERROR] WHATSAPP_PHONE_NUMBER_ID no está configurado")
    config_ok = False
else:
    print(f"[OK] WHATSAPP_PHONE_NUMBER_ID: {settings.WHATSAPP_PHONE_NUMBER_ID}")

if not settings.WHATSAPP_VERIFY_TOKEN:
    print("[ERROR] WHATSAPP_VERIFY_TOKEN no está configurado")
    config_ok = False
else:
    print(f"[OK] WHATSAPP_VERIFY_TOKEN: {settings.WHATSAPP_VERIFY_TOKEN}")

print()

if not config_ok:
    print("[ERROR] Faltan variables de configuración. Revisa tu archivo .env")
    sys.exit(1)

# Verificar base de datos
print("2. Verificando base de datos...")
print("-" * 70)

try:
    total_clientes = Cliente.objects.count()
    total_conversaciones = Conversacion.objects.count()
    total_mensajes = Mensaje.objects.count()
    
    print(f"[OK] Clientes en la base de datos: {total_clientes}")
    print(f"[OK] Conversaciones en la base de datos: {total_conversaciones}")
    print(f"[OK] Mensajes en la base de datos: {total_mensajes}")
    
    # Mostrar conversaciones recientes de WhatsApp
    conversaciones_whatsapp = Conversacion.objects.filter(fuente='WhatsApp').order_by('-ultima_actualizacion')[:5]
    if conversaciones_whatsapp:
        print()
        print("Conversaciones recientes de WhatsApp:")
        for conv in conversaciones_whatsapp:
            mensajes_count = Mensaje.objects.filter(conversacion=conv).count()
            print(f"  - Cliente: {conv.cliente.nombre} ({conv.cliente.telefono}) - {mensajes_count} mensajes")
    else:
        print()
        print("[INFO] Aún no hay conversaciones de WhatsApp")
    
except Exception as e:
    print(f"[ERROR] Error al acceder a la base de datos: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("INSTRUCCIONES PARA PROBAR:")
print("=" * 70)
print()
print("1. Asegurate de que el servidor Django esté corriendo:")
print("   python manage.py runserver")
print()
print("2. Asegurate de que ngrok esté corriendo (si estás en local):")
print("   ngrok http 8000")
print()
print("3. En Meta for Developers, suscribite a estos campos del webhook:")
print("   - messages (obligatorio)")
print("   - message_status (opcional, para estados de entrega)")
print()
print("4. Enviá un mensaje de WhatsApp al número de prueba de Meta")
print()
print("5. Verificá los logs del servidor Django - deberías ver:")
print("   [WEBHOOK] Mensaje recibido de: +XXXXXXXXXXXX")
print()
print("6. Abrí el panel de CRM en tu navegador:")
print("   http://localhost:8000/crm/")
print()
print("7. Deberías ver la conversación con el cliente que envió el mensaje")
print()
print("=" * 70)

