import json
import logging

import google.generativeai as genai
from django.conf import settings
from django.db.models import Q, Count
from inventario.models import (
    Categoria,
    DetalleIphone,
    Precio,
    Producto,
    ProductoVariante,
)

from historial.models import RegistroHistorial

logger = logging.getLogger(__name__)

# Configurar la API de Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


def _extract_json_block(text: str) -> str:
    """
    Extrae el primer bloque JSON válido de un texto potencialmente envuelto en ```json ... ```.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    # Fallback simple: si no empieza con { intenta encontrar el primer { y último }
    if not cleaned.startswith("{"):
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start : end + 1]
    return cleaned


def _invoke_gemini(prompt: str):
    """Ejecuta una generación en Gemini con fallback de modelo."""

    preferred = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash") or "gemini-1.5-flash"
    candidates = [preferred]
    if "gemini-1.5-flash" not in candidates:
        candidates.append("gemini-1.5-flash")

    last_error: Exception | None = None
    for model_name in candidates:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt)
        except Exception as exc:  # pragma: no cover - SDK externo
            last_error = exc
            message = str(exc)
            if "404" in message or "not found" in message.lower():
                logger.warning(
                    "Modelo Gemini '%s' no disponible (%s). Intentando fallback...",
                    model_name,
                    message,
                )
                continue
            raise

    if last_error is not None:
        raise last_error

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

# Whitelist de campos permitidos por modelo (para evitar consultas peligrosas)
ALLOWED_FIELDS: dict[str, set[str]] = {
    'Producto': {'nombre', 'categoria__nombre', 'activo'},
    'ProductoVariante': {'producto__nombre', 'producto__categoria__nombre', 'sku', 'atributo_1', 'atributo_2', 'stock_actual', 'stock_minimo'},
    'DetalleIphone': {'variante__sku', 'imei', 'salud_bateria', 'costo_usd', 'precio_venta_usd', 'precio_oferta_usd'},
    'Precio': {'variante__sku', 'variante__producto__nombre', 'tipo', 'moneda', 'precio'},
    'RegistroHistorial': {'accion', 'usuario__username', 'modelo', 'obj_id'},
    'Categoria': {'nombre'},
}

ALLOWED_LOOKUPS = {'exact', 'iexact', 'contains', 'icontains', 'gte', 'lte', 'gt', 'lt', 'in', 'startswith', 'istartswith', 'endswith', 'iendswith'}


def _is_allowed_field(model_name: str, field_lookup: str) -> bool:
    """
    Verifica que el lookup esté permitido. Permite sufijos de lookup (campo__icontains).
    """
    parts = field_lookup.split("__")
    if len(parts) > 1 and parts[-1] in ALLOWED_LOOKUPS:
        base = "__".join(parts[:-1])
    else:
        base = field_lookup
    return base in ALLOWED_FIELDS.get(model_name, set())


# Esquema de la DB para que la IA entienda la estructura.
DATABASE_SCHEMA = """
# Modelos de la base de datos de Django para ImportStore
class Producto(models.Model):
    nombre = models.CharField(max_length=180)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    activo = models.BooleanField(default=True)

class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sku = models.CharField(max_length=64, unique=True)
    atributo_1 = models.CharField(max_length=120, blank=True)
    atributo_2 = models.CharField(max_length=120, blank=True)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)

class DetalleIphone(models.Model):
    variante = models.OneToOneField(ProductoVariante, on_delete=models.CASCADE)
    imei = models.CharField(max_length=15, unique=True, null=True, blank=True)
    salud_bateria = models.PositiveIntegerField(null=True, blank=True)
    costo_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_venta_usd = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Precio(models.Model):
    variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=[("MINORISTA", "Minorista"), ("MAYORISTA", "Mayorista")])
    moneda = models.CharField(max_length=3, choices=[("USD", "USD"), ("ARS", "ARS")])
    precio = models.DecimalField(max_digits=12, decimal_places=2)
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
        response = _invoke_gemini(prompt)
        json_text = _extract_json_block(response.text or "")
        data = json.loads(json_text)
        # Validación mínima del esquema
        if not isinstance(data, dict):
            return {"model": "None", "action": "chat", "filters": []}
        model_name = data.get("model")
        action = data.get("action")
        filters = data.get("filters", [])
        if model_name not in MODEL_MAP and model_name != "None":
            data["model"] = "None"
        if action not in {"filter", "count"}:
            data["action"] = "chat"
        if not isinstance(filters, list):
            data["filters"] = []
        return data
    except Exception as e:
        if "429" in str(e):
            return {"error": "RATE_LIMIT_EXCEEDED"}
        logger.exception("Error generando JSON de consulta: %s", e)
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
        valid_filters = 0
        for f in filters_list:
            field = f.get("field")
            value = f.get("value")
            if not field or value is None:
                continue
            if not _is_allowed_field(model_name, field):
                logger.warning("Filtro rechazado por whitelist", extra={"model": model_name, "field": field})
                continue
            try:
                q_objects &= Q(**{field: value})
                valid_filters += 1
            except Exception as ex:
                logger.warning("Filtro inválido descartado", extra={"field": field, "error": str(ex)})
                continue

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
        logger.exception("Error ejecutando consulta desde JSON: %s", e)
        return f"Error al ejecutar la consulta: {type(e).__name__} - {e}"


def generate_final_response(question, query_results, user_name="Ema", chat_history=""):
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
                    detalles = item.atributos_display or "Variante estándar"
                    formatted_items.append(
                        f"Producto: {item.producto.nombre}, SKU {item.sku} ({detalles}) — Stock: {item.stock_actual}"
                    )
                elif isinstance(item, Precio):
                    info = f"Producto: {item.variante.producto.nombre}, SKU {item.variante.sku}"
                    info += f", {item.get_tipo_display()} {item.precio} {item.moneda}"
                    formatted_items.append(info)
                elif isinstance(item, DetalleIphone):
                    estado = "Plan canje" if getattr(item, "es_plan_canje", False) else "Venta directa"
                    formatted_items.append(
                        f"IMEI {item.imei or 'sin registrar'} — {estado} — Salud batería: {item.salud_bateria or 'N/D'}%"
                    )
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
        response = _invoke_gemini(prompt)
        return response.text.strip()
    except Exception as e:
        if "429" in str(e):
            return (
                f"Disculpame, {user_name}. Llegamos al límite de consultas a la IA. "
                "Probá de nuevo en unos instantes."
            )
        logger.exception("Error generando respuesta final: %s", e)
        return (
            f"Disculpame, {user_name}. Tuve un problema para formular la respuesta final."
        )
