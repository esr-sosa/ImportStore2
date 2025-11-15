#!/usr/bin/env python
"""Script para verificar la configuración del token de WhatsApp"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
env_path = Path('sistema_negocio') / '.env' if Path('sistema_negocio/.env').exists() else Path('.env')
load_dotenv(env_path)

token = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')

print("=" * 60)
print("VERIFICACIÓN DE CONFIGURACIÓN DE WHATSAPP")
print("=" * 60)
print(f"\nToken configurado: {'SÍ' if token else 'NO'}")
if token:
    print(f"  Longitud: {len(token)} caracteres")
    print(f"  Primeros 10 caracteres: {token[:10]}...")
    print(f"  Últimos 10 caracteres: ...{token[-10:]}")
else:
    print("  ⚠️  El token NO está configurado en .env")

print(f"\nPhone Number ID configurado: {'SÍ' if phone_id else 'NO'}")
if phone_id:
    print(f"  Valor: {phone_id}")
else:
    print("  ⚠️  El Phone Number ID NO está configurado en .env")

print("\n" + "=" * 60)
print("SOLUCIÓN AL ERROR 401:")
print("=" * 60)
print("""
El error 401 Unauthorized significa que el token de acceso no es válido.

Para solucionarlo:

1. Ve a Meta for Developers: https://developers.facebook.com/apps/
2. Seleccioná tu app de WhatsApp Business
3. Ve a "Configuración" > "Básica"
4. En "Token de acceso", generá un nuevo token con estos permisos:
   - whatsapp_business_messaging
   - whatsapp_business_management
5. Copiá el nuevo token y actualizalo en tu archivo .env:
   WHATSAPP_ACCESS_TOKEN=tu_nuevo_token_aqui
6. Reiniciá el servidor Django

NOTA: Los tokens temporales expiran. Si usás un token temporal, necesitás
generar uno permanente o renovarlo periódicamente.
""")

