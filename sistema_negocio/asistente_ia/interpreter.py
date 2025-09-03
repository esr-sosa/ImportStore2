import google.generativeai as genai
import json
from django.conf import settings
from django.db.models import Q, Count
from inventario.models import Producto, ProductoVariante, DetalleIphone, Precio, Categoria
from historial.models import RegistroHistorial

# Configurar la API de Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# --- ¡NUEVO! LISTA DE SALUDOS COMUNES ---
# Esto evita llamadas innecesarias a la IA para conversaciones simples
SIMPLE_GREETINGS = [
    "hola", "holis", "buenas", "que tal", "todo bien",
    "como estas", "cómo estás", "como va", "cómo va",
    "gracias", "muchas gracias", "joya", "dale"
]

# SECURITY: Mapeo de nombres de modelos a las clases reales.
MODEL_MAP = {
    'Producto': Producto,
    'ProductoVariante': ProductoVariante,
    'DetalleIphone': DetalleIphone,
    'Precio': Precio,
    'RegistroHistorial': RegistroHistorial,
    'Categoria': Categoria,
}

# Esquema de la DB para que la IA entienda la estructura.
DATABASE_SCHEMA = """
# Modelos de la base de datos de Django para ImportStore
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, ...)
    activo = models.BooleanField(default=True)

class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, ...)
    nombre_variante = models.CharField(max_length=150) # Ej: "256GB / Titanio Natural"

class DetalleIphone(models.Model):
    variante = models.OneToOneField(ProductoVariante, ...)
    imei = models.CharField(max_length=15, ...)
    salud_bateria = models.PositiveIntegerField(...)
    
class Precio(models.Model):
    variante = models.ForeignKey(ProductoVariante, ...)
    moneda = models.CharField(max_length=3, default='USD')
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta_normal = models.DecimalField(max_digits=10, decimal_places=2)
"""

def generate_query_json_from_question(question, user_name="Ema"):
    """
    Convierte una pregunta en un JSON que describe la consulta a la base de datos.
    """
    # --- ¡NUEVO! FILTRO DE SENTIDO COMÚN ---
    if question.lower().strip() in SIMPLE_GREETINGS:
        return {"model": "None", "action": "chat", "filters": []}

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Tu tarea es ser el motor de análisis de lenguaje para ISAC, un asistente de IA.
    El usuario que te habla es {user_name}, el dueño del negocio.
    Convierte su pregunta en una estructura JSON para una consulta al ORM de Django.

    **REGLAS CRÍTICAS:**
    1.  **Devolvé ÚNICAMENTE un objeto JSON válido.** Sin explicaciones ni markdown.
    2.  El JSON debe tener "model", "action", y "filters".
    3.  **"model"**: Debe ser uno de: {', '.join(MODEL_MAP.keys())}.
    4.  **"action"**: Puede ser "filter" (lista) o "count" (número).
    5.  **"filters"**: Una lista de diccionarios con "field" y "value".
    6.  **Usa `__icontains` para búsquedas de texto flexibles.**
    7.  **SIEMPRE que se pregunte por "iPhones", agrega un filtro para la categoría "Celulares"**: `{{"field": "producto__categoria__nombre__iexact", "value": "Celulares"}}`
    8.  **Para preguntas de cantidad ("cuántos", "stock de"), la acción debe ser "count" y el modelo `ProductoVariante`.**
    9.  **Para preguntas de precio o costo ("cuánto vale", "precio de", "costo"), el modelo debe ser `Precio` y la acción `filter`.**
    10. Si la pregunta es un saludo o no parece una consulta (ej: "quien sos"), devolvé: `{{"model": "None", "action": "chat", "filters": []}}`

    **Esquema de la Base de Datos:**
    {DATABASE_SCHEMA}
    ---
    **Pregunta del usuario:** "{question}"
    **JSON de la consulta:**
    """
    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(json_text)
    except Exception as e:
        if "429" in str(e):
            print("Se alcanzó el límite de la API de Gemini.")
            return {"error": "RATE_LIMIT_EXCEEDED"}
        print(f"Error generando JSON de consulta: {e}")
        return None

def run_query_from_json(query_json):
    if not query_json or query_json.get("model") == "None":
        return None
    if "error" in query_json:
        return query_json

    try:
        model_name = query_json.get("model")
        action = query_json.get("action")
        filters_list = query_json.get("filters", [])

        if model_name not in MODEL_MAP:
            return f"Error de seguridad: El modelo '{model_name}' no está permitido."
        
        Model = MODEL_MAP[model_name]
        q_objects = Q()
        for f in filters_list:
            if "field" in f and "value" in f:
                q_objects &= Q(**{f['field']: f['value']})

        queryset = Model.objects.filter(q_objects)

        if action == "count":
            results = queryset.count()
        elif action == "filter":
            if model_name in ['ProductoVariante', 'DetalleIphone', 'Precio']:
                queryset = queryset.select_related('variante__producto', 'producto__categoria')
            results = list(queryset[:10])
        else:
            return f"Error: La acción '{action}' no es válida."
        
        return results
    except Exception as e:
        print(f"Error ejecutando consulta desde JSON: {e}")
        return f"Error al ejecutar la consulta: {type(e).__name__} - {e}"

def generate_final_response(question, query_results, user_name="Ema"):
    if isinstance(query_results, dict) and query_results.get("error") == "RATE_LIMIT_EXCEEDED":
        return f"Disculpame, {user_name}. Parece que hemos hecho muchas consultas a la inteligencia artificial por hoy y alcanzamos el límite de la capa gratuita. Podemos seguir mañana cuando se reinicie la cuota."

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    results_str = ""
    if query_results is None:
        results_str = "Es una pregunta de chat, no una consulta de datos."
    elif isinstance(query_results, list):
        if not query_results:
            results_str = "La consulta no devolvió ningún resultado."
        else:
            formatted_items = []
            for item in query_results:
                if isinstance(item, ProductoVariante):
                    formatted_items.append(f"Producto: {item.producto.nombre}, Variante: {item.nombre_variante}")
                elif isinstance(item, Precio):
                    info = f"Producto: {item.variante.producto.nombre}, Variante: {item.variante.nombre_variante}"
                    if hasattr(item, 'precio_venta_normal'):
                        info += f", Precio de Venta: USD {item.precio_venta_normal}"
                    if hasattr(item, 'costo'):
                        info += f", Costo: USD {item.costo}"
                    formatted_items.append(info)
                else:
                    formatted_items.append(str(item))
            results_str = "\n".join(formatted_items)
    else:
        results_str = str(query_results)

    prompt = f"""
    Sos ISAC, el asistente de IA de ImportStore. Tu interlocutor es {user_name}, el dueño del negocio.
    Tu tono es el de un colega proactivo y eficiente, pero siempre servicial. Usá un lenguaje argentino y profesional.

    El usuario te hizo una pregunta y vos obtuviste un resultado de la base de datos (o no, si era un saludo). Tu tarea es formular la respuesta final.

    **REGLAS DE PERSONALIDAD Y RESPUESTA:**
    1.  **Si es una pregunta de chat** (resultado: "Es una pregunta de chat..."), respondé de forma natural y directa. No repitas "Hola Ema" si él ya saludó. Si te pregunta "como estas", respondé brevemente y devolvé la pregunta o ponete a disposición. Ej: "Todo bien por acá, Ema. ¿En qué te puedo ayudar?".
    2.  **Si es un error técnico**, informá que hubo un problema al consultar la base de datos, de forma concisa.
    3.  **Si no se encontraron resultados**, informalo claramente. Ej: "Ema, estuve buscando pero no encontré ningún iPhone que coincida con esa descripción en la base de datos."
    4.  **Si hay resultados**, presentalos de forma clara y directa. No inventes contexto, solo presentá los datos.
    5.  **NUNCA INVENTES INFORMACIÓN.** Es tu regla más importante.

    **Pregunta Original de {user_name}:** "{question}"

    **Resultados de la Base de Datos (en crudo):**
    {results_str}

    **Tu Respuesta Final (concisa y directa para {user_name}):**
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if "429" in str(e):
             return f"Disculpame, {user_name}. Parece que hemos hecho muchas consultas a la inteligencia artificial por hoy y alcanzamos el límite de la capa gratuita. Podemos seguir mañana cuando se reinicie la cuota."
        print(f"Error generando respuesta final: {e}")
        return "Disculpame, Ema. Tuve un problema para formular la respuesta final."

