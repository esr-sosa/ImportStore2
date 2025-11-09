# core/utils.py

import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


_DOLAR_CACHE = {"valor": None, "timestamp": None}


def _cache_expirado(ttl_minutos: int) -> bool:
    marca = _DOLAR_CACHE["timestamp"]
    if not marca:
        return True
    return datetime.utcnow() - marca > timedelta(minutes=ttl_minutos)


def obtener_valor_dolar_blue(force: bool = False) -> float | None:
    """Devuelve la cotización de dolarhoy con caché y fallback configurable."""

    ttl_minutos = int(os.getenv("DOLAR_BLUE_CACHE_MINUTES", "15"))
    fallback_valor = os.getenv("DOLAR_BLUE_FALLBACK")

    if not force and not _cache_expirado(ttl_minutos):
        return _DOLAR_CACHE["valor"]

    try:
        url = "https://www.dolarhoy.com/cotizaciondolarblue"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        valor_venta_div = soup.find("div", class_="value")

        if valor_venta_div:
            valor_str = valor_venta_div.text.strip().replace("$", "").replace(",", ".")
            _DOLAR_CACHE["valor"] = float(valor_str)
            _DOLAR_CACHE["timestamp"] = datetime.utcnow()
            return _DOLAR_CACHE["valor"]
    except Exception:
        # Silenciamos errores de red/parsing y pasamos al fallback.
        pass

    manual_config = None
    try:
        from configuracion.models import ConfiguracionSistema  # type: ignore

        manual_config = ConfiguracionSistema.carga().dolar_blue_manual
    except Exception:
        manual_config = None

    if manual_config is not None:
        valor = float(manual_config)
        _DOLAR_CACHE["valor"] = valor
        _DOLAR_CACHE["timestamp"] = datetime.utcnow()
        return valor

    if fallback_valor is not None:
        try:
            valor = float(fallback_valor)
            _DOLAR_CACHE["valor"] = valor
            _DOLAR_CACHE["timestamp"] = datetime.utcnow()
            return valor
        except ValueError:
            pass

    return _DOLAR_CACHE["valor"]
