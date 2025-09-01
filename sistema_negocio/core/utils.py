# core/utils.py

import requests
from bs4 import BeautifulSoup

def obtener_valor_dolar_blue():
    """
    Esta función se conecta a dolarhoy.com y extrae el valor de venta del Dólar Blue.
    """
    try:
        # Hacemos la petición a la página
        url = 'https://www.dolarhoy.com/cotizaciondolarblue'
        response = requests.get(url)
        response.raise_for_status() # Lanza un error si la página no cargó bien

        # Analizamos el HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscamos el div que contiene el valor de venta.
        # Esta clase puede cambiar si la página se actualiza, es el riesgo del scraping.
        valor_venta_div = soup.find('div', class_='value')

        if valor_venta_div:
            # Limpiamos el texto para quedarnos solo con el número
            valor_str = valor_venta_div.text.strip().replace('$', '')
            return float(valor_str)
        else:
            # Si no encontramos el div, devolvemos un valor por defecto o un error
            return None
    except Exception as e:
        # Si algo falla (sin internet, la página cambió, etc.), lo dejamos registrado
        print(f"Error al obtener el valor del dólar: {e}")
        return None
