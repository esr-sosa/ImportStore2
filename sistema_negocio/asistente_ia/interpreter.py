import google.generativeai as genai
import json
from django.conf import settings
from django.db.models import Q, Count
from inventario.models import Producto, ProductoVariante, Precio, Categoria

# Compatibilidad: si DetalleIphone ya no existe en inventario.models,
# mantenemos una referencia nula para que el import no explote.
try:
    from inventario.models import DetalleIphone  # puede no existir luego de la 0005
except Exception:
    DetalleIphone = None

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

# asistente_ia/interpreter.py

def generate_query_json_from_question(question, user_name="Ema", chat_history=""):  # <-- Argumento nuevo
    """
    Convierte la PREGUNTA MÁS RECIENTE en un JSON, usando el historial como contexto.
    """
    if not question:
        return {"model": "None", "action": "chat", "filters": []}

    question_normalized = str(question).strip()

    if not question_normalized:
        return {"model": "None", "action": "chat", "filters": []}

    if question_normalized.lower() in SIMPLE_GREETINGS:
        return {"model": "None", "action": "chat", "filters": []}

    question = question_normalized

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Tu tarea es ser el motor de análisis de lenguaje para ISAC.
    El usuario es {user_name}, el dueño.

    **Contexto de la Conversación:**
    {chat_history}
    ---
    **Tarea:** Analiza el **último mensaje del cliente** ("{question}") y conviértelo en un JSON de consulta para el ORM de Django.
    Usa el contexto si es necesario (ej: si pregunta "y de 256gb?", se refiere al modelo que venían hablando).

    **REGLAS CRÍTICAS:**
    1.  **Devolvé ÚNICAMENTE un objeto JSON válido.**
    2.  **"model"**: Debe ser uno de: {', '.join(MODEL_MAP.keys())}.
    3.  **"action"**: "filter" (lista) o "count" (número).
    4.  **Si el último mensaje no es una consulta de datos** (ej: "gracias"), devolvé: `{{"model": "None", "action": "chat", "filters": []}}`

    **Esquema de la Base de Datos:**
    {DATABASE_SCHEMA}
    ---
    **JSON de la consulta para el último mensaje:**
    """
    try:
        # ... (el resto de la función no cambia) ...
        response = model.generate_content(prompt)
        json_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(json_text)
    except Exception as e:
        if "429" in str(e):
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
            # --- CÓDIGO CORREGIDO ---
            # Ahora la optimización de la consulta es específica para cada modelo.
            if model_name == 'Precio':
                queryset = queryset.select_related('variante__producto__categoria')
            elif model_name == 'DetalleIphone':
                queryset = queryset.select_related('variante__producto__categoria')
            elif model_name == 'ProductoVariante':
                queryset = queryset.select_related('producto__categoria')
            # --- FIN DE LA CORRECCIÓN ---
            results = list(queryset[:10])
        else:
            return f"Error: La acción '{action}' no es válida."
        return results
    except Exception as e:
        print(f"Error ejecutando consulta desde JSON: {e}")
        return f"Error al ejecutar la consulta: {type(e).__name__} - {e}"
# asistente_ia/interpreter.py

def generate_final_response(question, query_results, user_name="Ema", chat_history=""): # <-- Argumento nuevo
    # ... (la primera parte de la función no cambia) ...
    if isinstance(query_results, dict):
        if query_results.get("error") == "RATE_LIMIT_EXCEEDED":
            return (
                f"Disculpame, {user_name}. Llegamos al límite de consultas a la IA. "
                "Probá de nuevo en unos instantes."
            )
        # Otros errores inesperados se devuelven como mensaje legible.
        return (
            f"{user_name}, tuve un problema al interpretar la consulta: "
            f"{query_results.get('error', 'Error desconocido')}"
        )

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    results_str = ""
    # ... (la lógica para formatear results_str no cambia) ...
    if query_results is None:
        results_str = "Es una pregunta de chat, no una consulta de datos."
    elif isinstance(query_results, list):
        if not query_results:
            results_str = "La consulta no devolvió ningún resultado."
        else:
            # ... (código para formatear la lista de resultados) ...
            formatted_items = []
            for item in query_results:
                if isinstance(item, ProductoVariante):
                    formatted_items.append(
                        f"Producto: {item.producto.nombre}, Variante: {item.nombre_variante}"
                    )
                elif isinstance(item, Precio):
                    info = (
                        f"Producto: {item.variante.producto.nombre}, Variante: {item.variante.nombre_variante}"
                    )
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
    Sos ISAC, el asistente de IA de ImportStore. Tu tono es el de un colega proactivo y eficiente. Usá un lenguaje argentino y profesional.

    **Historial de la Conversación:**
    {chat_history}
    ---
    **Pregunta más reciente del cliente:** "{question}"
    **Resultados de tu consulta a la Base de Datos:** "{results_str}"
    ---
    **Tarea:** Formula la respuesta final para el cliente. La respuesta debe ser la continuación LÓGICA y COHERENTE del historial.

    **REGLAS DE RESPUESTA:**
    1.  **Si el cliente saluda**, respondé al saludo de forma natural.
    2.  **Si no hay resultados**, informalo amablemente. Ej: "Ema, busqué el iPhone 16 Pro Max pero no me figura stock disponible en este momento."
    3.  **Si hay resultados**, presentalos de forma clara y directa. Si antes preguntó por un modelo y ahora por colores, respondé sobre los colores de ESE modelo.
    4.  **Sé proactivo.** Si un cliente pregunta "¿Tienen iPhone 16?", y vos encontrás 3 variantes, una buena respuesta sería: "¡Hola! Sí, tenemos el iPhone 16. ¿Te interesa en alguna capacidad o color en particular? Así te paso el precio exacto."

    **Tu Respuesta Final (concisa, directa y en español de Argentina):**
    """
    try:
        # ... (el resto de la función no cambia) ...
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if "429" in str(e):
            return (
                f"Disculpame, {user_name}. Llegamos al límite de consultas a la IA. "
                "Probá de nuevo en unos instantes."
            )
        print(f"Error generando respuesta final: {e}")
        return (
            f"Disculpame, {user_name}. Tuve un problema para formular la respuesta final."
        )
