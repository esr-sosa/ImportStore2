# crm/whatsapp_service.py

import requests
import json
import re
from django.conf import settings

def send_whatsapp_message(to_number, message_text):
    """
    Envía un mensaje de texto a un número de WhatsApp usando la API de Meta.
    """
    try:
        # 1. Limpiamos caracteres no numéricos
        clean_number = re.sub(r'\D', '', to_number)

        # 2. --- ¡ESTA ES LA CORRECCIÓN CLAVE PARA ARGENTINA! ---
        # Si el número empieza con 549 y tiene 13 dígitos, le quitamos el 9.
        if clean_number.startswith('549') and len(clean_number) == 13:
            clean_number = '54' + clean_number[3:]
            print(f"Número argentino detectado. Corrigiendo a: {clean_number}")

        access_token = settings.WHATSAPP_ACCESS_TOKEN
        phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        
        url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_number, # <-- Usamos el número corregido
            "type": "text",
            "text": { "body": message_text, "preview_url": False }
        }
        
        print(f"--- Intentando enviar a WhatsApp ---")
        print(f"Payload final: {json.dumps(payload)}")
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        response_data = response.json()
        print(f"--- Éxito --- Mensaje enviado a {clean_number}: {response_data}")
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"--- ¡ERROR! --- Falla en la solicitud a la API de WhatsApp.")
        print(f"Error: {e}")
        if e.response is not None:
            print(f"Detalle del error de Meta: {e.response.text}")
        raise e