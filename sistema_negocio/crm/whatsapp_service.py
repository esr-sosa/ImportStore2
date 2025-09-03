# crm/whatsapp_service.py

import requests
import json
from django.conf import settings
import re # <--- Importamos la librería para limpiar el texto

def send_whatsapp_message(to_number, message_text):
    """
    Envía un mensaje de texto a un número de WhatsApp usando la API de Meta.
    """
    try:
        # --- ¡ESTA ES LA LÍNEA DE CORRECCIÓN CLAVE! ---
        # Nos aseguramos de que el número contenga solo dígitos.
        clean_number = re.sub(r'\D', '', to_number)

        access_token = settings.WHATSAPP_ACCESS_TOKEN
        phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        
        url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_number, # <-- Usamos el número limpio
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        response_data = response.json()
        print(f"Mensaje enviado a {clean_number}: {response_data}")
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje de WhatsApp: {e}")
        if e.response:
            print(f"Detalle del error: {e.response.text}")
        raise e