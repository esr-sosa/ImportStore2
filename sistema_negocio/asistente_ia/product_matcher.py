"""
Módulo para matching de productos similares y procesamiento de listados de proveedores.
"""
import logging
import re
from decimal import Decimal, InvalidOperation
from typing import List, Dict, Optional, Tuple

from django.db.models import Q
from inventario.models import Producto, ProductoVariante

logger = logging.getLogger(__name__)


def extract_product_info_from_text(text: str) -> List[Dict]:
    """
    Extrae información de productos de un texto de proveedor.
    Formato esperado: "producto cantidad costo" o variaciones.
    
    Ejemplos:
    - "cargador xiaomi 20w x3 5000"
    - "cargador 20w xiaomi, cantidad: 3, costo: 5000"
    - "proveedor cargador xiaomi 20w x3 y el costo 5000"
    - Listados de pedidos con formato: "Producto × cantidad $precio"
    """
    products = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
        
        # Ignorar líneas que son encabezados o totales
        if any(skip in line.lower() for skip in ['producto', 'total', 'subtotal', 'descuento', 'envío', 'detalles', '---', '===']):
            if 'producto' in line.lower() and 'total' in line.lower():
                continue  # Es un encabezado de tabla
        
        # Patrón 1: "producto × cantidad $precio" (formato de pedido)
        match1 = re.search(r'(.+?)\s*×\s*(\d+)\s+\$?(\d+(?:[.,]\d+)?)', line, re.IGNORECASE)
        if match1:
            nombre = match1.group(1).strip()
            cantidad = int(match1.group(2))
            costo = _parse_decimal(match1.group(3))
            if costo and nombre:
                products.append({
                    'nombre': nombre,
                    'cantidad': cantidad,
                    'costo': costo
                })
                continue
        
        # Patrón 2: "producto x cantidad costo"
        match2 = re.search(r'(.+?)\s+x\s*(\d+)\s+(\d+(?:[.,]\d+)?)', line, re.IGNORECASE)
        if match2:
            nombre = match2.group(1).strip()
            cantidad = int(match2.group(2))
            costo = _parse_decimal(match2.group(3))
            if costo and nombre:
                products.append({
                    'nombre': nombre,
                    'cantidad': cantidad,
                    'costo': costo
                })
                continue
        
        # Patrón 3: "producto cantidad costo" (sin x)
        match3 = re.search(r'(.+?)\s+(\d+)\s+(\d+(?:[.,]\d+)?)', line, re.IGNORECASE)
        if match3:
            nombre = match3.group(1).strip()
            cantidad = int(match3.group(2))
            costo = _parse_decimal(match3.group(3))
            # Validar que no sea solo números (evitar falsos positivos)
            if costo and nombre and not re.match(r'^\d+$', nombre):
                products.append({
                    'nombre': nombre,
                    'cantidad': cantidad,
                    'costo': costo
                })
                continue
        
        # Patrón 4: "producto, cantidad: X, costo: Y"
        match4 = re.search(r'(.+?)(?:,|\s+)(?:cantidad|cant|qty|unidades?):\s*(\d+)(?:,|\s+)(?:costo|precio|price):\s*(\d+(?:[.,]\d+)?)', line, re.IGNORECASE)
        if match4:
            nombre = match4.group(1).strip()
            cantidad = int(match4.group(2))
            costo = _parse_decimal(match4.group(3))
            if costo and nombre:
                products.append({
                    'nombre': nombre,
                    'cantidad': cantidad,
                    'costo': costo
                })
                continue
        
        # Patrón 5: Solo nombre de producto (sin cantidad ni costo explícitos)
        # Solo si la línea parece un nombre de producto válido
        if len(line) > 10 and not re.match(r'^[\d\s\$.,]+$', line):
            # Verificar que tenga palabras significativas
            words = re.findall(r'\b\w{3,}\b', line.lower())
            if words and any(keyword in line.lower() for keyword in ['cargador', 'auricular', 'cable', 'iphone', 'producto', 'pack', 'kit', 'set', 'adaptador', 'reloj', 'smartwatch', 'memoria', 'cable', 'riñonera', 'estante', 'gorra', 'frasco', 'tv', 'box', 'tripode', 'soporte', 'toma']):
                products.append({
                    'nombre': line,
                    'cantidad': 1,  # Default
                    'costo': None
                })
    
    return products


def _parse_decimal(value: str) -> Optional[Decimal]:
    """Convierte un string a Decimal, manejando comas y puntos."""
    try:
        # Reemplazar coma por punto
        value = value.replace(',', '.')
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def find_similar_products(product_name: str, threshold: float = 0.3) -> List[Tuple[ProductoVariante, float]]:
    """
    Encuentra productos similares en el inventario usando búsqueda por palabras clave.
    
    Args:
        product_name: Nombre del producto a buscar
        threshold: Umbral mínimo de similitud (0-1)
    
    Returns:
        Lista de tuplas (ProductoVariante, score) ordenadas por relevancia
    """
    # Normalizar el nombre del producto
    search_terms = _extract_keywords(product_name)
    
    if not search_terms:
        return []
    
    # Buscar productos que contengan alguna de las palabras clave
    q_objects = Q()
    for term in search_terms:
        q_objects |= Q(producto__nombre__icontains=term)
        q_objects |= Q(sku__icontains=term)
        q_objects |= Q(atributo_1__icontains=term)
        q_objects |= Q(atributo_2__icontains=term)
    
    variantes = ProductoVariante.objects.filter(
        q_objects,
        producto__activo=True
    ).select_related('producto', 'producto__categoria')[:20]
    
    # Calcular score de similitud simple
    results = []
    for variante in variantes:
        score = _calculate_similarity(product_name, variante)
        if score >= threshold:
            results.append((variante, score))
    
    # Ordenar por score descendente
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results


def _extract_keywords(text: str) -> List[str]:
    """Extrae palabras clave relevantes del texto."""
    # Palabras comunes a ignorar
    stop_words = {'el', 'la', 'los', 'las', 'de', 'del', 'y', 'o', 'a', 'en', 'un', 'una', 'por', 'con', 'para', 'x', 'proveedor'}
    
    # Normalizar y dividir
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filtrar stop words y palabras muy cortas
    keywords = [w for w in words if len(w) > 2 and w not in stop_words]
    
    return keywords


def _calculate_similarity(search_name: str, variante: ProductoVariante) -> float:
    """
    Calcula un score de similitud simple entre el nombre buscado y la variante.
    """
    search_lower = search_name.lower()
    variante_text = f"{variante.producto.nombre} {variante.sku} {variante.atributo_1 or ''} {variante.atributo_2 or ''}".lower()
    
    # Contar palabras coincidentes
    search_words = set(_extract_keywords(search_name))
    variante_words = set(_extract_keywords(variante_text))
    
    if not search_words:
        return 0.0
    
    # Jaccard similarity
    intersection = search_words & variante_words
    union = search_words | variante_words
    
    if not union:
        return 0.0
    
    jaccard = len(intersection) / len(union)
    
    # Bonus si el nombre completo está contenido
    if search_lower in variante_text or variante_text in search_lower:
        jaccard += 0.3
    
    return min(jaccard, 1.0)


def format_similar_products_for_question(similar_products: List[Tuple[ProductoVariante, float]], max_items: int = 5) -> str:
    """
    Formatea productos similares para mostrar al usuario en una pregunta.
    """
    if not similar_products:
        return ""
    
    items = similar_products[:max_items]
    lines = []
    
    for idx, (variante, score) in enumerate(items, 1):
        categoria = variante.producto.categoria.nombre if variante.producto.categoria else "Sin categoría"
        atributos = f" - {variante.atributo_1}" if variante.atributo_1 else ""
        atributos += f" - {variante.atributo_2}" if variante.atributo_2 else ""
        stock = variante.stock_actual
        
        lines.append(
            f"{idx}. **{variante.producto.nombre}{atributos}** (SKU: {variante.sku}) - "
            f"Categoría: {categoria} - Stock actual: {stock} - Similitud: {score:.0%}"
        )
    
    return "\n".join(lines)

