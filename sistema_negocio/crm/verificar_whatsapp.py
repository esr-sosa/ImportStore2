"""
Script para verificar la configuración de WhatsApp API
Ejecutar: python manage.py shell < crm/verificar_whatsapp.py
O mejor: python -c "import os, sys, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); django.setup(); exec(open('crm/verificar_whatsapp.py').read())"
"""

import os
from django.conf import settings

print("=" * 60)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE WHATSAPP API")
print("=" * 60)
print()

# Verificar variables del .env
variables_requeridas = {
    'WHATSAPP_ACCESS_TOKEN': settings.WHATSAPP_ACCESS_TOKEN,
    'WHATSAPP_PHONE_NUMBER_ID': settings.WHATSAPP_PHONE_NUMBER_ID,
    'WHATSAPP_VERIFY_TOKEN': settings.WHATSAPP_VERIFY_TOKEN,
}

print("📋 Variables de configuración:")
print("-" * 60)

todo_ok = True
for var_name, var_value in variables_requeridas.items():
    if var_value:
        # Ocultar el token completo por seguridad
        if 'TOKEN' in var_name:
            display_value = var_value[:20] + "..." if len(var_value) > 20 else var_value
        else:
            display_value = var_value
        print(f"✅ {var_name}: {display_value}")
    else:
        print(f"❌ {var_name}: NO CONFIGURADO")
        todo_ok = False

print()
print("=" * 60)

if todo_ok:
    print("✅ Todas las variables están configuradas correctamente!")
    print()
    print("📝 Próximos pasos:")
    print("1. Verificá que la URL del webhook en Meta sea:")
    print("   https://b68590d879ef.ngrok-free.app/webhook/")
    print("   (IMPORTANTE: debe terminar en /webhook/)")
    print()
    print("2. Verificá que el Token de verificación en Meta sea igual a:")
    print(f"   {settings.WHATSAPP_VERIFY_TOKEN}")
    print()
    print("3. Verificá que 'messages' esté suscrito en Meta")
    print()
    print("4. Probá enviando un mensaje desde WhatsApp al número de prueba")
else:
    print("❌ Faltan variables de configuración en el .env")
    print()
    print("Agregá estas líneas a tu archivo .env:")
    print("-" * 60)
    for var_name in variables_requeridas.keys():
        if not variables_requeridas[var_name]:
            print(f"{var_name}=")
    print("-" * 60)

print("=" * 60)

