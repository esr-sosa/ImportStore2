# core/utils.py

import requests
from bs4 import BeautifulSoup

def obtener_valor_dolar_blue():
    """
    Se conecta a dolarhoy.com y extrae el valor de venta del Dólar Blue.
    """
    try:
        url = 'https://www.dolarhoy.com/cotizaciondolarblue'
        # Agregamos un User-Agent para simular ser un navegador y evitar bloqueos
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # Lanza un error si la página no cargó bien

        soup = BeautifulSoup(response.text, 'html.parser')
        
        valor_venta_div = soup.find('div', class_='value')

        if valor_venta_div:
            valor_str = valor_venta_div.text.strip().replace('$', '')
            # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
            # Reemplazamos la coma decimal argentina por un punto que Python entiende.
            valor_str_con_punto = valor_str.replace(',', '.')
            return float(valor_str_con_punto)
        return None
    except Exception as e:
        print(f"Error al obtener el valor del dólar: {e}")
        return None
