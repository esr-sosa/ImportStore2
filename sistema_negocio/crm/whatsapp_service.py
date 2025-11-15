# crm/whatsapp_service.py

import json
import logging
import re
import base64
from typing import Any, Dict, List, Optional
from pathlib import Path

import requests
from django.conf import settings
from django.core.files.storage import default_storage
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def _build_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["POST"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_maxsize=10)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _normalize_argentina_number(number: str) -> str:
    clean_number = re.sub(r"\D", "", number or "")
    if clean_number.startswith("549") and len(clean_number) == 13:
        # Corrige formato AR removiendo el '9' intermedio (celulares)
        return "54" + clean_number[3:]
    return clean_number


def send_whatsapp_message(to_number: str, message_text: str) -> Dict[str, Any]:
    """
    Envía un mensaje de texto a WhatsApp usando la API de Meta con timeouts/reintentos y logging.
    """
    access_token = settings.WHATSAPP_ACCESS_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    if not access_token or not phone_number_id:
        error_msg = "Configuración de WhatsApp faltante: verifique el .env"
        print(f"[WHATSAPP ERROR] {error_msg}")
        print(f"[WHATSAPP ERROR] ACCESS_TOKEN configurado: {bool(access_token)}")
        print(f"[WHATSAPP ERROR] PHONE_NUMBER_ID configurado: {bool(phone_number_id)}")
        raise RuntimeError(error_msg)

    timeout = getattr(settings, "REQUESTS_TIMEOUT_SECONDS", 15)
    session = _build_session()

    to_normalized = _normalize_argentina_number(to_number)
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_normalized,
        "type": "text",
        "text": {"body": message_text, "preview_url": False},
    }

    logger.info("Enviando WhatsApp", extra={"to": to_normalized, "length": len(message_text or "")})
    print(f"[WHATSAPP] Enviando a {to_normalized} usando Phone ID: {phone_number_id}")

    try:
        response = session.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        
        # Log detallado de la respuesta
        print(f"[WHATSAPP] Status code: {response.status_code}")
        
        if response.status_code == 401:
            error_detail = response.text
            print(f"[WHATSAPP ERROR] 401 Unauthorized - Token inválido o expirado")
            print(f"[WHATSAPP ERROR] Detalle: {error_detail}")
            print(f"[WHATSAPP ERROR] Verificá:")
            print(f"[WHATSAPP ERROR] 1. Que el WHATSAPP_ACCESS_TOKEN en .env sea válido")
            print(f"[WHATSAPP ERROR] 2. Que el token no haya expirado (los tokens temporales expiran)")
            print(f"[WHATSAPP ERROR] 3. Que tengas permisos de 'whatsapp_business_messaging' y 'whatsapp_business_management'")
            print(f"[WHATSAPP ERROR] 4. Que el PHONE_NUMBER_ID sea correcto")
            raise RuntimeError(f"Token de WhatsApp inválido o expirado (401). Verificá tu configuración en Meta for Developers.")
        
        response.raise_for_status()
        data = response.json()
        logger.info("WhatsApp enviado", extra={"to": to_normalized, "message_id": data.get("messages", [{}])[0].get("id")})
        print(f"[WHATSAPP] Mensaje enviado exitosamente")
        return data
    except requests.exceptions.HTTPError as exc:
        if exc.response and exc.response.status_code == 401:
            error_detail = exc.response.text if exc.response else "No hay detalles"
            print(f"[WHATSAPP ERROR] 401 Unauthorized - Token inválido o expirado")
            print(f"[WHATSAPP ERROR] Detalle completo: {error_detail}")
            logger.error("Falla enviando WhatsApp - Token inválido", extra={
                "to": to_normalized, 
                "error": str(exc), 
                "status": exc.response.status_code if exc.response else None,
                "meta_body": error_detail
            })
            raise RuntimeError(f"Token de WhatsApp inválido o expirado (401). Necesitás regenerar el token en Meta for Developers.")
        body = getattr(exc.response, "text", None) if getattr(exc, "response", None) is not None else None
        logger.error("Falla enviando WhatsApp", extra={"to": to_normalized, "error": str(exc), "meta_body": body})
        print(f"[WHATSAPP ERROR] Error HTTP: {exc}")
        raise
    except requests.exceptions.RequestException as exc:
        body = getattr(exc.response, "text", None) if getattr(exc, "response", None) is not None else None
        logger.error("Falla enviando WhatsApp", extra={"to": to_normalized, "error": str(exc), "meta_body": body})
        print(f"[WHATSAPP ERROR] Error de conexión: {exc}")
        raise


def send_whatsapp_image(to_number: str, image_url: str, caption: str = "") -> Dict[str, Any]:
    """
    Envía una imagen a WhatsApp usando la API de Meta.
    
    Args:
        to_number: Número de teléfono del destinatario
        image_url: URL pública de la imagen (debe ser accesible desde internet)
        caption: Texto opcional que acompaña la imagen (máximo 1024 caracteres)
    """
    access_token = settings.WHATSAPP_ACCESS_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    if not access_token or not phone_number_id:
        raise RuntimeError("Configuración de WhatsApp faltante: verifique el .env")
    
    timeout = getattr(settings, "REQUESTS_TIMEOUT_SECONDS", 15)
    session = _build_session()
    
    to_normalized = _normalize_argentina_number(to_number)
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_normalized,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption[:1024] if caption else ""  # WhatsApp limita a 1024 caracteres
        }
    }
    
    logger.info("Enviando imagen por WhatsApp", extra={"to": to_normalized, "image_url": image_url})
    print(f"[WHATSAPP] Enviando imagen a {to_normalized}")
    
    try:
        response = session.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        response.raise_for_status()
        data = response.json()
        logger.info("Imagen enviada por WhatsApp", extra={"to": to_normalized, "message_id": data.get("messages", [{}])[0].get("id")})
        print(f"[WHATSAPP] Imagen enviada exitosamente")
        return data
    except requests.exceptions.RequestException as exc:
        logger.error("Falla enviando imagen por WhatsApp", extra={"to": to_normalized, "error": str(exc)})
        print(f"[WHATSAPP ERROR] Error enviando imagen: {exc}")
        raise


def send_whatsapp_buttons(
    to_number: str, 
    message_text: str, 
    buttons: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Envía un mensaje con botones interactivos nativos de WhatsApp.
    
    Args:
        to_number: Número de teléfono del destinatario
        message_text: Texto del mensaje (máximo 1024 caracteres)
        buttons: Lista de botones. Cada botón es un dict con:
            - "id": ID único del botón (máximo 256 caracteres)
            - "title": Texto del botón (máximo 20 caracteres)
    
    Ejemplo:
        buttons = [
            {"id": "comprar_ahora", "title": "Comprar ahora"},
            {"id": "ver_mas", "title": "Ver más modelos"},
            {"id": "ver_ubicacion", "title": "Ver ubicación"}
        ]
    """
    access_token = settings.WHATSAPP_ACCESS_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    if not access_token or not phone_number_id:
        raise RuntimeError("Configuración de WhatsApp faltante: verifique el .env")
    
    if len(buttons) > 3:
        raise ValueError("WhatsApp permite máximo 3 botones por mensaje")
    
    timeout = getattr(settings, "REQUESTS_TIMEOUT_SECONDS", 15)
    session = _build_session()
    
    to_normalized = _normalize_argentina_number(to_number)
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    # Formatear botones según la API de WhatsApp
    formatted_buttons = []
    for btn in buttons:
        formatted_buttons.append({
            "type": "reply",
            "reply": {
                "id": btn["id"][:256],  # Limitar longitud
                "title": btn["title"][:20]  # Limitar longitud
            }
        })
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_normalized,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": message_text[:1024]  # Limitar longitud
            },
            "action": {
                "buttons": formatted_buttons
            }
        }
    }
    
    logger.info("Enviando mensaje con botones por WhatsApp", extra={"to": to_normalized, "buttons_count": len(buttons)})
    print(f"[WHATSAPP] Enviando mensaje con {len(buttons)} botones a {to_normalized}")
    
    try:
        response = session.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        response.raise_for_status()
        data = response.json()
        logger.info("Mensaje con botones enviado por WhatsApp", extra={"to": to_normalized, "message_id": data.get("messages", [{}])[0].get("id")})
        print(f"[WHATSAPP] Mensaje con botones enviado exitosamente")
        return data
    except requests.exceptions.RequestException as exc:
        logger.error("Falla enviando mensaje con botones por WhatsApp", extra={"to": to_normalized, "error": str(exc)})
        print(f"[WHATSAPP ERROR] Error enviando mensaje con botones: {exc}")
        raise


def send_whatsapp_typing_indicator(to_number: str, typing: bool = True) -> Dict[str, Any]:
    """
    Intenta enviar el indicador de "escribiendo..." a WhatsApp.
    
    NOTA: La API oficial de Meta/WhatsApp Business puede no soportar esto directamente,
    pero algunos proveedores (como Twilio) sí lo ofrecen. Esta función intenta
    diferentes endpoints y formatos para ver si funciona con tu configuración.
    
    Si no funciona, no afecta el funcionamiento del sistema.
    """
    access_token = settings.WHATSAPP_ACCESS_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    if not access_token or not phone_number_id:
        return {}  # No lanzar error, es opcional
    
    timeout = getattr(settings, "REQUESTS_TIMEOUT_SECONDS", 5)  # Timeout corto
    session = _build_session()
    
    to_normalized = _normalize_argentina_number(to_number)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    # Intentar diferentes formatos de endpoint
    endpoints_to_try = [
        # Formato 1: Endpoint de mensajes con tipo "typing"
        {
            "url": f"https://graph.facebook.com/v19.0/{phone_number_id}/messages",
            "payload": {
                "messaging_product": "whatsapp",
                "to": to_normalized,
                "type": "typing",
                "typing": typing
            }
        },
        # Formato 2: Endpoint específico de typing (si existe)
        {
            "url": f"https://graph.facebook.com/v19.0/{phone_number_id}/typing",
            "payload": {
                "to": to_normalized,
                "typing": typing
            }
        },
        # Formato 3: Usando el formato de Messenger (puede funcionar en algunos casos)
        {
            "url": f"https://graph.facebook.com/v19.0/{phone_number_id}/messages",
            "payload": {
                "recipient": {"id": to_normalized},
                "sender_action": "typing_on" if typing else "typing_off"
            }
        },
    ]
    
    for attempt, endpoint_config in enumerate(endpoints_to_try, 1):
        try:
            url = endpoint_config["url"]
            payload = endpoint_config["payload"]
            
            response = session.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Indicador de typing enviado exitosamente (método {attempt})", extra={"to": to_normalized, "typing": typing})
                print(f"[WHATSAPP] ✓ Indicador de 'escribiendo...' enviado al cliente (método {attempt})")
                return data
            elif response.status_code == 400:
                # Error de formato, probar siguiente método
                error_data = response.json() if response.text else {}
                logger.debug(f"Método {attempt} no funcionó: {error_data.get('error', {}).get('message', 'Unknown error')}")
                continue
            else:
                # Otro error, loguear pero continuar
                logger.debug(f"Método {attempt} falló con status {response.status_code}")
                continue
                
        except Exception as exc:
            logger.debug(f"Error en método {attempt}: {exc}")
            continue
    
    # Si ningún método funcionó, no es crítico
    logger.debug("Ningún método de typing indicator funcionó (puede ser normal)")
    print(f"[WHATSAPP] ⚠ No se pudo enviar indicador de 'escribiendo...' (la API puede no soportarlo)")
    return {}