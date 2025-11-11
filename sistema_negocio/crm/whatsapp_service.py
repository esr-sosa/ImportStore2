# crm/whatsapp_service.py

import json
import logging
import re
from typing import Any, Dict

import requests
from django.conf import settings
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
        "type": "text",
        "text": {"body": message_text, "preview_url": False},
    }

    logger.info("Enviando WhatsApp", extra={"to": to_normalized, "length": len(message_text or "")})

    try:
        response = session.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        response.raise_for_status()
        data = response.json()
        logger.info("WhatsApp enviado", extra={"to": to_normalized, "message_id": data.get("messages", [{}])[0].get("id")})
        return data
    except requests.exceptions.RequestException as exc:
        body = getattr(exc.response, "text", None) if getattr(exc, "response", None) is not None else None
        logger.error("Falla enviando WhatsApp", extra={"to": to_normalized, "error": str(exc), "meta_body": body})
        raise