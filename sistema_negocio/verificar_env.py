"""
Script para verificar que el .env se esté leyendo correctamente
Ejecutar: python verificar_env.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener el directorio base (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

print("=" * 60)
print("VERIFICACION DEL ARCHIVO .env")
print("=" * 60)
print()
print(f"Buscando .env en: {env_path}")
print(f"Existe el archivo: {env_path.exists()}")
print()

if env_path.exists():
    print("Leyendo variables del .env...")
    load_dotenv(env_path)
    
    # Verificar las variables de WhatsApp
    variables = {
        'WHATSAPP_ACCESS_TOKEN': os.getenv('WHATSAPP_ACCESS_TOKEN'),
        'WHATSAPP_PHONE_NUMBER_ID': os.getenv('WHATSAPP_PHONE_NUMBER_ID'),
        'WHATSAPP_VERIFY_TOKEN': os.getenv('WHATSAPP_VERIFY_TOKEN'),
    }
    
    print()
    print("Variables encontradas:")
    print("-" * 60)
    for var_name, var_value in variables.items():
        if var_value:
            if 'TOKEN' in var_name:
                display = var_value[:20] + "..." if len(var_value) > 20 else var_value
            else:
                display = var_value
            print(f"[OK] {var_name}: {display}")
        else:
            print(f"[FALTA] {var_name}: NO CONFIGURADO")
    
    print()
    print("=" * 60)
    
    # Verificar específicamente el verify token
    verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
    if not verify_token:
        print()
        print("ERROR: WHATSAPP_VERIFY_TOKEN no está configurado!")
        print()
        print("Agrega esta linea a tu archivo .env:")
        print("WHATSAPP_VERIFY_TOKEN=importstore_token_secreto_123")
        print()
        print("IMPORTANTE:")
        print("- No dejes espacios antes o después del =")
        print("- No uses comillas")
        print("- El archivo debe estar en: sistema_negocio/.env")
    else:
        print()
        print(f"Token de verificacion encontrado: {verify_token}")
        print("El token deberia ser: importstore_token_secreto_123")
        if verify_token == "importstore_token_secreto_123":
            print("[OK] El token coincide correctamente!")
        else:
            print("[ERROR] El token NO coincide!")
            print(f"Esperado: importstore_token_secreto_123")
            print(f"Encontrado: {verify_token}")
else:
    print()
    print("ERROR: El archivo .env NO existe!")
    print()
    print("Crea el archivo .env en: sistema_negocio/.env")
    print()
    print("Con este contenido minimo:")
    print("-" * 60)
    print("WHATSAPP_ACCESS_TOKEN=tu_access_token_aqui")
    print("WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui")
    print("WHATSAPP_VERIFY_TOKEN=importstore_token_secreto_123")
    print("-" * 60)

print()
print("=" * 60)

