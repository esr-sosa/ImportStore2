# crm/whatsapp_service.py

import requests
import json
from django.conf import settings

def send_whatsapp_message(to_number, message_text):
    """
    Envía un mensaje de texto a un número de WhatsApp usando la API de Meta.
    """
    try:
        access_token = settings.WHATSAPP_ACCESS_TOKEN
        phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        
        url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Lanza un error si la respuesta no es 2xx

        response_data = response.json()
        print(f"Mensaje enviado a {to_number}: {response_data}")
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje de WhatsApp: {e}")
        if e.response:
            print(f"Detalle del error: {e.response.text}")
        return None