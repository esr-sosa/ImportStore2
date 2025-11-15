import json
import logging
import re

import google.generativeai as genai
from django.conf import settings
from django.db.models import Q, Count, Sum
from inventario.models import (
    Categoria,
    DetalleIphone,
    Precio,
    Producto,
    ProductoVariante,
)

from historial.models import RegistroHistorial
from ventas.models import Venta, DetalleVenta
from django.utils import timezone
from datetime import datetime, timedelta
from .product_matcher import extract_product_info_from_text, find_similar_products, format_similar_products_for_question

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

    # Usar modelos Gemini 2.x que están disponibles actualmente
    preferred = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash") or "gemini-2.5-flash"
    candidates = [
        preferred,
        "gemini-2.5-flash",      # Modelo más reciente y rápido
        "gemini-2.0-flash",      # Fallback estable
        "gemini-2.5-pro",        # Modelo más potente
        "gemini-flash-latest",   # Alias al último flash
        "gemini-pro-latest"      # Alias al último pro
    ]
    
    # Eliminar duplicados manteniendo el orden
    seen = set()
    unique_candidates = []
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            unique_candidates.append(candidate)

    last_error: Exception | None = None
    for model_name in unique_candidates:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt)
        except Exception as exc:  # pragma: no cover - SDK externo
            last_error = exc
            message = str(exc)
            if "404" in message or "not found" in message.lower() or "not supported" in message.lower():
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
    'Venta': Venta,
    'DetalleVenta': DetalleVenta,
}

# Whitelist de campos permitidos por modelo (para evitar consultas peligrosas)
ALLOWED_FIELDS: dict[str, set[str]] = {
    'Producto': {'nombre', 'categoria__nombre', 'activo'},
    'ProductoVariante': {'producto__nombre', 'producto__categoria__nombre', 'sku', 'atributo_1', 'atributo_2', 'stock_actual', 'stock_minimo'},
    'DetalleIphone': {'variante__sku', 'imei', 'salud_bateria', 'costo_usd', 'precio_venta_usd', 'precio_oferta_usd'},
    'Precio': {'variante__sku', 'variante__producto__nombre', 'tipo', 'moneda', 'precio'},
    'RegistroHistorial': {'accion', 'usuario__username', 'modelo', 'obj_id'},
    'Categoria': {'nombre'},
    'Venta': {'id', 'fecha', 'fecha__gte', 'fecha__lte', 'fecha__date', 'cliente__nombre', 'cliente_nombre', 'status', 'metodo_pago', 'total_ars', 'vendedor__username'},
    'DetalleVenta': {'venta__id', 'venta__fecha', 'descripcion', 'sku', 'cantidad', 'variante__producto__nombre', 'variante__producto__categoria__nombre'},
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

class Venta(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    fecha = models.DateTimeField()
    cliente_nombre = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=[("PAGADO", "Pagado"), ("COMPLETADO", "Completado"), ...])
    metodo_pago = models.CharField(max_length=20)
    total_ars = models.DecimalField(max_digits=12, decimal_places=2)
    vendedor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles", on_delete=models.CASCADE)
    variante = models.ForeignKey(ProductoVariante, null=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=200)
    sku = models.CharField(max_length=60)
    cantidad = models.PositiveIntegerField()
    precio_unitario_ars_congelado = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal_ars = models.DecimalField(max_digits=12, decimal_places=2)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
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
    
    # Detectar si es un listado de productos del proveedor
    question_lower = question.lower()
    if any(keyword in question_lower for keyword in ['proveedor', 'listado', 'cargar', 'agregar stock', 'actualizar stock', 'agregar al stock', 'añadir al stock', 'sumar stock', 'recibir mercadería', 'recepción']):
        # Verificar si hay información de productos (cantidad, costo, etc.) o si el mensaje anterior tenía productos
        if any(keyword in question_lower for keyword in ['x', '×', 'cantidad', 'costo', 'precio', 'unidades']) or len(question) > 100:
            return {"model": "None", "action": "procesar_listado_proveedor", "texto": question, "filters": []}
    
    # Detectar acciones especiales
    if any(keyword in question_lower for keyword in ['comprobante', 'pdf', 'voucher', 'recibo']):
        # Buscar ID de venta en la pregunta
        venta_id_match = re.search(r'venta\s*[#:]?\s*([A-Z0-9-]+)', question_lower)
        if venta_id_match:
            venta_id = venta_id_match.group(1).upper()
            return {"model": "Venta", "action": "generar_comprobante", "venta_id": venta_id, "filters": []}
    
    # Detectar consultas de ventas por fecha
    fecha_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', question)
    if fecha_match and any(keyword in question_lower for keyword in ['venta', 'ventas', 'vendido', 'facturado']):
        dia, mes, anio = fecha_match.groups()
        if len(anio) == 2:
            anio = '20' + anio
        try:
            fecha_obj = datetime(int(anio), int(mes), int(dia))
            fecha_desde = fecha_obj.replace(hour=0, minute=0, second=0)
            fecha_hasta = fecha_obj.replace(hour=23, minute=59, second=59)
            return {
                "model": "Venta",
                "action": "filter",
                "filters": [
                    {"field": "fecha__gte", "value": fecha_desde.isoformat()},
                    {"field": "fecha__lte", "value": fecha_hasta.isoformat()}
                ]
            }
        except:
            pass
    
    # Detectar "hoy"
    if 'hoy' in question_lower and any(keyword in question_lower for keyword in ['venta', 'ventas', 'vendido']):
        hoy = timezone.now().date()
        fecha_desde = timezone.make_aware(datetime.combine(hoy, datetime.min.time()))
        fecha_hasta = timezone.make_aware(datetime.combine(hoy, datetime.max.time()))
        return {
            "model": "Venta",
            "action": "filter",
            "filters": [
                {"field": "fecha__gte", "value": fecha_desde.isoformat()},
                {"field": "fecha__lte", "value": fecha_hasta.isoformat()}
            ]
        }
    
    prompt = f"""
    Tu tarea es ser el motor de análisis de lenguaje para ISAC.
    El usuario es {user_name}, un asesor/empleado de ImportStore (empresa de venta de productos tecnológicos).

    **Contexto de la Conversación:**
    {chat_history}
    ---
    **Tarea:** Analiza el **último mensaje del empleado** ("{question}") y conviértelo en un JSON de consulta para el ORM de Django.
    Usa el contexto si es necesario (ej: si pregunta "y de 256gb?", se refiere al modelo que venían hablando).

    **IMPORTANTE - BÚSQUEDAS INTELIGENTES:**
    - Si el usuario pregunta por un producto genérico (ej: "cargadores", "auriculares", "cables", "iphone"), busca en el NOMBRE del producto usando "producto__nombre__icontains"
    - Si pregunta por una categoría (ej: "celulares"), busca en "producto__categoria__nombre__icontains"
    - Para productos como "iphone", busca TANTO en el nombre del producto COMO en la categoría (usa múltiples filtros)
    - Si pregunta por stock, usa "ProductoVariante" y filtra por "stock_actual"
    - Si pregunta por precios, usa "Precio" y filtra por tipo y moneda
    - Si pregunta por ventas, usa "Venta" o "DetalleVenta"
    - SIEMPRE usa búsquedas parciales (icontains) para nombres de productos, no exactas
    - Para contar stock total, usa "action": "count" y suma el stock_actual de todas las variantes

    **REGLAS CRÍTICAS:**
    1.  **Devolvé ÚNICAMENTE un objeto JSON válido.**
    2.  **"model"**: Debe ser uno de: {', '.join(MODEL_MAP.keys())}.
    3.  **"action"**: "filter" (lista) o "count" (número).
    4.  **Si el último mensaje no es una consulta de datos** (ej: "gracias"), devolvé: `{{"model": "None", "action": "chat", "filters": []}}`
    5.  **Para búsquedas de productos por nombre**, usa "producto__nombre__icontains" o "nombre__icontains"
    6.  **Para búsquedas por categoría**, usa "producto__categoria__nombre__icontains" o "categoria__nombre__icontains"

    **Esquema de la Base de Datos:**
    {DATABASE_SCHEMA}
    
    **Ejemplos de consultas:**
    - "cuantos cargadores hay" → {{"model": "ProductoVariante", "action": "count", "filters": [{{"field": "producto__nombre__icontains", "value": "cargador"}}]}}
    - "cuantos iphone hay" → {{"model": "ProductoVariante", "action": "filter", "filters": [{{"field": "producto__nombre__icontains", "value": "iphone"}}, {{"field": "producto__categoria__nombre__icontains", "value": "celulares"}}]}}
    - "stock de iphone 15" → {{"model": "ProductoVariante", "action": "filter", "filters": [{{"field": "producto__nombre__icontains", "value": "iphone 15"}}]}}
    - "ventas de hoy" → {{"model": "Venta", "action": "filter", "filters": [{{"field": "fecha__date", "value": "hoy"}}]}}
    
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

        # Manejar acciones especiales
        if action == "generar_comprobante":
            venta_id = query_json.get("venta_id")
            if not venta_id:
                return {"error": "No se especificó el ID de la venta"}
            try:
                venta = Venta.objects.get(id=venta_id)
                return {"action": "generar_comprobante", "venta_id": venta_id, "venta": venta}
            except Venta.DoesNotExist:
                return {"error": f"No se encontró la venta {venta_id}"}

        if model_name not in MODEL_MAP:
            return f"Error de seguridad: El modelo '{model_name}' no está permitido."
        
        Model = MODEL_MAP[model_name]
        q_objects = Q()
        valid_filters = 0
        
        # Agrupar filtros icontains con el mismo valor para hacer OR
        icontains_groups = {}
        other_filters = []
        
        for f in filters_list:
            field = f.get("field")
            value = f.get("value")
            if not field or value is None:
                continue
            
            # Manejar fechas en formato ISO
            if field.endswith("__gte") or field.endswith("__lte") or field.endswith("__date"):
                try:
                    if isinstance(value, str) and 'T' in value:
                        # Es un datetime ISO string
                        value = timezone.datetime.fromisoformat(value.replace('Z', '+00:00'))
                    elif isinstance(value, str) and value == "hoy":
                        # Manejar "hoy"
                        hoy = timezone.now().date()
                        if field.endswith("__date"):
                            value = hoy
                        elif field.endswith("__gte"):
                            value = timezone.make_aware(datetime.combine(hoy, datetime.min.time()))
                        elif field.endswith("__lte"):
                            value = timezone.make_aware(datetime.combine(hoy, datetime.max.time()))
                except Exception as ex:
                    logger.warning("Error parseando fecha", extra={"field": field, "value": value, "error": str(ex)})
                    continue
            
            if not _is_allowed_field(model_name, field):
                logger.warning("Filtro rechazado por whitelist", extra={"model": model_name, "field": field})
                continue
            
            # Agrupar filtros icontains con el mismo valor para hacer OR
            if field.endswith("__icontains") and isinstance(value, str):
                key = value.lower().strip()
                if key not in icontains_groups:
                    icontains_groups[key] = []
                icontains_groups[key].append((field, value))
            else:
                other_filters.append((field, value))
        
        # Construir Q objects: OR para filtros icontains con mismo valor, AND para el resto
        for value_key, fields_list in icontains_groups.items():
            if len(fields_list) > 1:
                # Múltiples campos con mismo valor -> OR
                q_or = Q()
                for field, value in fields_list:
                    q_or |= Q(**{field: value})
                q_objects &= q_or
                valid_filters += 1
            else:
                # Un solo campo -> AND normal
                try:
                    field, value = fields_list[0]
                    q_objects &= Q(**{field: value})
                    valid_filters += 1
                except Exception as ex:
                    logger.warning("Filtro inválido descartado", extra={"field": field, "error": str(ex)})
        
        # Agregar otros filtros con AND
        for field, value in other_filters:
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
            # Optimización de consultas por modelo
            if model_name == 'Precio':
                queryset = queryset.select_related('variante__producto', 'variante__producto__categoria')
            elif model_name == 'DetalleIphone':
                queryset = queryset.select_related('variante__producto', 'variante__producto__categoria')
            elif model_name == 'ProductoVariante':
                queryset = queryset.select_related('producto', 'producto__categoria')
            elif model_name == 'Venta':
                queryset = queryset.select_related('vendedor', 'cliente').prefetch_related('detalles')
            elif model_name == 'DetalleVenta':
                queryset = queryset.select_related('venta', 'variante__producto', 'variante__producto__categoria')
            elif model_name == 'Producto':
                queryset = queryset.select_related('categoria')
            
            # Limitar resultados pero permitir más para ventas
            limit = 50 if model_name == 'Venta' else 10
            results = list(queryset[:limit])
        else:
            return f"Error: La acción '{action}' no es válida."
        return results
    except Exception as e:
        logger.exception("Error ejecutando consulta desde JSON: %s", e)
        return f"Error al ejecutar la consulta: {type(e).__name__} - {e}"


def generate_final_response(question, query_results, user_name="Ema", chat_history="", available_resources=None):
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
    special_action = None
    
    if query_results is None:
        results_str = "Es una pregunta de chat, no una consulta de datos."
    elif isinstance(query_results, dict):
        # Manejar acciones especiales o errores
        if query_results.get("action") == "generar_comprobante":
            special_action = "generar_comprobante"
            venta = query_results.get("venta")
            if venta:
                results_str = f"Venta {venta.id} encontrada. Total: ${venta.total_ars:.2f} ARS. Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}"
            else:
                results_str = f"Venta {query_results.get('venta_id')} encontrada."
        elif query_results.get("error"):
            results_str = f"Error: {query_results.get('error')}"
        else:
            results_str = str(query_results)
    elif isinstance(query_results, (int, float)):
        # Es un count
        results_str = f"Total encontrado: {query_results}"
    elif isinstance(query_results, list):
        if not query_results:
            results_str = "La consulta no devolvió ningún resultado."
        else:
            formatted_items = []
            total_stock = 0
            for item in query_results:
                if isinstance(item, ProductoVariante):
                    detalles = item.atributos_display or "Variante estándar"
                    categoria = item.producto.categoria.nombre if item.producto.categoria else "Sin categoría"
                    stock = item.stock_actual
                    total_stock += stock
                    formatted_items.append(
                        f"Producto: {item.producto.nombre}, SKU {item.sku} ({detalles}) — Stock: {stock} — Categoría: {categoria}"
                    )
            
            # Procesar otros tipos de items que no sean ProductoVariante
            for item in query_results:
                if isinstance(item, ProductoVariante):
                    continue  # Ya procesado arriba
                elif isinstance(item, Precio):
                    info = f"Producto: {item.variante.producto.nombre}, SKU {item.variante.sku}"
                    info += f", {item.get_tipo_display()} ${item.precio:.2f} {item.moneda}"
                    formatted_items.append(info)
                elif isinstance(item, DetalleIphone):
                    estado = "Plan canje" if getattr(item, "es_plan_canje", False) else "Venta directa"
                    formatted_items.append(
                        f"IMEI {item.imei or 'sin registrar'} — {estado} — Salud batería: {item.salud_bateria or 'N/D'}%"
                    )
                elif isinstance(item, Venta):
                    cliente = item.cliente_nombre or (item.cliente.nombre if item.cliente else "Consumidor Final")
                    formatted_items.append(
                        f"Venta {item.id} — {item.fecha.strftime('%d/%m/%Y %H:%M')} — Cliente: {cliente} — Total: ${item.total_ars:.2f} ARS — {item.get_status_display()}"
                    )
                elif isinstance(item, DetalleVenta):
                    producto_info = item.variante.producto.nombre if item.variante and item.variante.producto else item.descripcion
                    formatted_items.append(
                        f"{producto_info} x{item.cantidad} — ${item.subtotal_ars:.2f} ARS (Venta {item.venta.id})"
                    )
                elif isinstance(item, Producto):
                    categoria = item.categoria.nombre if item.categoria else "Sin categoría"
                    formatted_items.append(
                        f"Producto: {item.nombre} — Categoría: {categoria}"
                    )
                else:
                    formatted_items.append(str(item))
            
            # Si hay múltiples variantes, agregar total
            if total_stock > 0 and any(isinstance(item, ProductoVariante) for item in query_results):
                if len([item for item in query_results if isinstance(item, ProductoVariante)]) > 1:
                    results_str = f"**Total de stock: {total_stock} unidades**\n\n" + "\n".join(formatted_items)
                else:
                    results_str = "\n".join(formatted_items)
            else:
                results_str = "\n".join(formatted_items)
    else:
        results_str = str(query_results)


    # Construir información de recursos disponibles
    resources_info = ""
    if available_resources:
        if available_resources.get("playbooks"):
            playbooks_list = [p.get('titulo', '') for p in available_resources['playbooks'][:5]]
            if playbooks_list:
                resources_info += f"\n**Playbooks disponibles:** {', '.join(playbooks_list)}\n"
        if available_resources.get("knowledge"):
            knowledge_list = [k.get('titulo', '') for k in available_resources['knowledge'][:5]]
            if knowledge_list:
                resources_info += f"\n**Artículos de conocimiento:** {', '.join(knowledge_list)}\n"
        if available_resources.get("quick_replies"):
            count = available_resources['quick_replies']
            if count:
                resources_info += f"\n**Respuestas rápidas disponibles:** {count} atajos configurados para consultas frecuentes\n"

    prompt = f"""
    Sos ISAC, el asistente de IA inteligente de ImportStore. 

    **CONTEXTO CRÍTICO - LEE CON ATENCIÓN:**
    - Estás trabajando para ImportStore, una EMPRESA de venta de productos tecnológicos (principalmente iPhones y accesorios)
    - Los usuarios que te consultan son ASESORES, VENDEDORES o EMPLEADOS INTERNOS de la empresa
    - NO son clientes externos. Son tus COLEGAS de trabajo
    - Tu función es ayudarlos a gestionar el negocio: consultar inventario, analizar ventas, generar reportes, responder preguntas operativas

    **RECURSOS DISPONIBLES EN EL SISTEMA:**
    {resources_info if resources_info else "El sistema tiene playbooks, artículos de conocimiento y respuestas rápidas configuradas que pueden ayudar a los empleados."}

    **HISTORIAL DE LA CONVERSACIÓN:**
    {chat_history if chat_history else "Esta es la primera interacción de la sesión."}
    
    ---
    **PREGUNTA DEL ASESOR/EMPLEADO:** "{question}"
    **RESULTADOS DE LA CONSULTA A LA BASE DE DATOS:** "{results_str}"
    ---

    **TAREA:** Formula una respuesta profesional, útil y contextualizada para el asesor/empleado. La respuesta debe ser la continuación LÓGICA y COHERENTE del historial.

    **REGLAS DE RESPUESTA (CRÍTICAS):**
    1. **CONTEXTO EMPRESARIAL:** Recordá SIEMPRE que estás hablando con un COLEGA/EMPLEADO de la empresa, NO con un cliente externo. Usá un tono profesional pero cercano, como entre compañeros de trabajo que se ayudan mutuamente.
    
    2. **Si el empleado saluda**, respondé de forma natural y ofrecé ayuda específica: "Hola {user_name}! ¿En qué te puedo ayudar hoy? Puedo consultarte stock, precios, generar reportes, o ayudarte con cualquier consulta del negocio."
    
    3. **Si no hay resultados**, informalo claramente y sugerí alternativas: "{user_name}, busqué en la base de datos pero no encontré resultados para esa consulta. ¿Querés que revise con otros criterios o te ayudo con algo más?"
    
    4. **Si hay resultados**, presentalos de forma clara, estructurada y profesional. Usá formato markdown:
       - Listas con bullets (*) para múltiples items
       - **Negrita** para destacar información crítica (stock bajo, precios, SKUs)
       - Separá secciones con saltos de línea
       - Incluí TODA la información relevante: nombre, SKU, stock, precios
    
    5. **Sé proactivo y útil:** Si un empleado pregunta "¿Qué iPhone 16 tenemos?", y encontrás 3 variantes, una respuesta profesional sería:
       "Tenemos estas opciones de iPhone 16 en stock:
       
       * **iPhone 16 - 128GB** - SKU: IPHONE-16-128GB-XXX - Stock: 5 unidades
       * **iPhone 16 - 256GB** - SKU: IPHONE-16-256GB-XXX - Stock: 3 unidades  
       * **iPhone 16 - 512GB** - SKU: IPHONE-16-512GB-XXX - Stock: 2 unidades
       
       ¿Necesitás que te muestre los precios o alguna otra información específica?"
    
    6. **RECURSOS DEL SISTEMA:** Si el empleado pregunta sobre procesos, procedimientos o necesita ayuda operativa, mencioná que pueden consultar los Playbooks o el Centro de Conocimiento disponibles en el panel lateral del sistema.
    
    7. **Formato de datos:** Cuando muestres productos, SIEMPRE incluye:
       - Nombre completo del producto
       - SKU (importante para identificación interna)
       - Stock actual
       - Precios (si están disponibles)
       - Cualquier información relevante para la gestión del negocio
    
    8. **Para ventas:** Cuando muestres ventas, incluye: ID de venta, fecha, cliente, total, método de pago, estado. Si el empleado pregunta por un comprobante, indicá que puede generarlo desde el sistema.
    
    9. **Sé conciso pero completo:** No te extiendas innecesariamente, pero proporcioná TODA la información relevante que el empleado necesita para hacer su trabajo eficientemente.
    
    10. **Lenguaje:** Usá español argentino, profesional pero natural. Evitá formalidades excesivas, pero mantené un tono de trabajo profesional entre colegas.
    
    11. **NUNCA uses la palabra "original"** cuando describas productos. Siempre mencioná la garantía y el servicio post-venta profesional.

    **Tu Respuesta Final (en español argentino, profesional, con formato markdown cuando sea útil):**
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


def process_images_with_vision(images_base64: list, user_question: str = "") -> str:
    """
    Procesa imágenes/PDFs usando Gemini Vision para extraer texto de listados de proveedores.
    """
    if not images_base64:
        return ""
    
    try:
        # Usar modelo con visión
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""
        Analizá esta imagen/PDF que contiene un listado de productos de un proveedor.
        
        Extraé la siguiente información de cada producto:
        - Nombre del producto
        - Cantidad/unidades
        - Costo/precio (si está disponible)
        
        Si hay texto, extraelo tal cual. Si es una imagen de un listado, describí los productos en formato:
        "producto nombre x cantidad costo"
        
        {f"Pregunta del usuario: {user_question}" if user_question else ""}
        
        Respondé SOLO con el listado de productos extraído, sin explicaciones adicionales.
        """
        
        # Procesar imágenes
        image_parts = []
        for img_base64 in images_base64[:3]:  # Máximo 3 imágenes
            try:
                # Remover prefijo data:image/...;base64, si existe
                if ',' in img_base64:
                    img_base64 = img_base64.split(',')[1]
                
                import base64
                from PIL import Image
                import io
                
                img_data = base64.b64decode(img_base64)
                img = Image.open(io.BytesIO(img_data))
                image_parts.append(img)
            except Exception as e:
                logger.warning(f"Error procesando imagen: {e}")
                continue
        
        if not image_parts:
            return ""
        
        # Generar contenido con imágenes
        response = model.generate_content([prompt] + image_parts)
        
        return response.text.strip() if response.text else ""
    
    except Exception as e:
        logger.error(f"Error procesando imágenes con visión: {e}")
        return ""
