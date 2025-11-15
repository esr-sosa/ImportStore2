"""
Servicio de IA para CRM - Genera respuestas humanas y mantiene contexto del cliente
"""
import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from decimal import Decimal

import google.generativeai as genai
from django.conf import settings
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta

from inventario.models import Producto, ProductoVariante, Precio, Categoria
from ventas.models import Venta, DetalleVenta
from crm.models import Cliente, Conversacion, Mensaje
from configuracion.models import ConfiguracionSistema

logger = logging.getLogger(__name__)

# Configurar Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


def _invoke_gemini(prompt: str, model_name: str = None):
    """Invoca Gemini con fallback de modelos"""
    model_candidates = [
        model_name,
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-2.5-pro',
        'gemini-flash-latest',
        'gemini-pro-latest',
    ] if model_name else [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-2.5-pro',
        'gemini-flash-latest',
        'gemini-pro-latest',
    ]
    
    unique_candidates = []
    for m in model_candidates:
        if m and m not in unique_candidates:
            unique_candidates.append(m)
    
    last_error = None
    for model_name in unique_candidates:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt)
        except Exception as exc:
            last_error = exc
            message = str(exc)
            if "404" in message or "not found" in message.lower():
                logger.warning(f"Modelo {model_name} no disponible, intentando siguiente...")
                continue
            raise
    
    if last_error:
        raise last_error


def obtener_contexto_cliente(cliente: Cliente, conversacion: Conversacion) -> Dict:
    """
    Obtiene todo el contexto relevante del cliente para generar respuestas personalizadas.
    Incluye información persistente guardada en ClienteContexto.
    """
    from crm.models import ClienteContexto
    
    contexto = {
        'cliente': {
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'tipo': cliente.tipo_cliente,
            'email': cliente.email,
            'instagram': cliente.instagram_handle,
        },
        'historial_compras': [],
        'productos_interes': [],
        'conversaciones_anteriores': [],
        'preferencias': {},
        'contexto_persistente': {},
    }
    
    # Obtener contexto persistente si existe
    try:
        contexto_obj = ClienteContexto.objects.get(cliente=cliente)
        contexto['contexto_persistente'] = {
            'productos_interes': contexto_obj.productos_interes,
            'categorias_preferidas': contexto_obj.categorias_preferidas,
            'tipo_consulta_comun': contexto_obj.tipo_consulta_comun,
            'total_interacciones': contexto_obj.total_interacciones,
            'tags_comportamiento': contexto_obj.tags_comportamiento,
        }
        # Usar productos de interés del contexto persistente
        contexto['productos_interes'] = contexto_obj.productos_interes
    except ClienteContexto.DoesNotExist:
        pass
    
    # Historial de compras
    try:
        compras = Venta.objects.filter(
            cliente_nombre__icontains=cliente.nombre
        ).order_by('-fecha')[:5]
        
        for venta in compras:
            detalles = venta.detalles.all()[:3]
            productos_comprados = [d.descripcion for d in detalles]
            contexto['historial_compras'].append({
                'fecha': venta.fecha.strftime('%d/%m/%Y'),
                'total': float(venta.total_ars),
                'productos': productos_comprados,
            })
    except Exception as e:
        logger.warning(f"Error obteniendo historial de compras: {e}")
    
    # Productos mencionados en conversaciones anteriores (solo si no hay contexto persistente)
    if not contexto.get('productos_interes'):
        try:
            mensajes_anteriores = Mensaje.objects.filter(
                conversacion__cliente=cliente
            ).exclude(conversacion=conversacion).order_by('-fecha_envio')[:20]
            
            productos_mencionados = set()
            for msg in mensajes_anteriores:
                # Buscar nombres de productos en mensajes
                productos = Producto.objects.filter(
                    Q(nombre__icontains=msg.contenido[:50]) | 
                    Q(variantes__sku__icontains=msg.contenido[:20])
                )[:3]
                for prod in productos:
                    productos_mencionados.add(prod.nombre)
            
            contexto['productos_interes'] = list(productos_mencionados)[:5]
        except Exception as e:
            logger.warning(f"Error obteniendo productos de interés: {e}")
    
    # Resúmenes de conversaciones anteriores
    try:
        otras_conversaciones = Conversacion.objects.filter(
            cliente=cliente
        ).exclude(id=conversacion.id).order_by('-ultima_actualizacion')[:3]
        
        for conv in otras_conversaciones:
            if conv.resumen:
                contexto['conversaciones_anteriores'].append({
                    'fecha': conv.ultima_actualizacion.strftime('%d/%m/%Y'),
                    'resumen': conv.resumen[:200],
                })
    except Exception as e:
        logger.warning(f"Error obteniendo conversaciones anteriores: {e}")
    
    return contexto


def buscar_productos_en_mensaje(mensaje: str, limite: int = 5) -> List[ProductoVariante]:
    """
    Busca productos mencionados en el mensaje del cliente.
    """
    mensaje_lower = mensaje.lower()
    
    # Palabras clave comunes de productos
    keywords = re.findall(r'\b\w{3,}\b', mensaje_lower)
    
    # Buscar productos que contengan alguna palabra clave
    q_objects = Q()
    for keyword in keywords:
        if len(keyword) > 3:  # Ignorar palabras muy cortas
            q_objects |= Q(producto__nombre__icontains=keyword)
            q_objects |= Q(sku__icontains=keyword)
            q_objects |= Q(atributo_1__icontains=keyword)
            q_objects |= Q(atributo_2__icontains=keyword)
            q_objects |= Q(producto__categoria__nombre__icontains=keyword)
    
    productos = ProductoVariante.objects.filter(
        q_objects,
        producto__activo=True,
        activo=True
    ).select_related('producto', 'producto__categoria').distinct()[:limite]
    
    return list(productos)


def obtener_configuracion_sistema() -> Dict:
    """
    Obtiene la configuración del sistema para usar en las respuestas de IA.
    """
    try:
        config = ConfiguracionSistema.carga()
        return {
            'nombre_local': config.nombre_local or config.nombre_comercial or 'ImportStore',
            'direccion': config.domicilio_comercial or '',
            'ubicacion_mapa': config.ubicacion_mapa or '',
            'google_maps_url': config.google_maps_url or '',
            'cuit': getattr(config, 'cuit', '') or '',
            'telefono_local': config.telefono_local or config.whatsapp_numero or '',
            'telefono_whatsapp': config.telefono_whatsapp or config.whatsapp_numero or '',
            'correo_contacto': config.correo_contacto or config.contacto_email or '',
            'horario_lunes_a_viernes': config.horario_lunes_a_viernes or '',
            'horario_sabados': config.horario_sabados or '',
            'horario_domingos': config.horario_domingos or '',
            'instagram_principal': config.instagram_principal or '',
            'instagram_secundario': config.instagram_secundario or '',
            'instagram_empresa': config.instagram_empresa or '',
            'tiktok': config.tiktok or '',
            'facebook': config.facebook or '',
            'whatsapp_alternativo': config.whatsapp_alternativo or '',
            'pago_efectivo_local': config.pago_efectivo_local,
            'pago_efectivo_retiro': config.pago_efectivo_retiro,
            'pago_transferencia': config.pago_transferencia,
            'transferencia_alias': config.transferencia_alias or '',
            'transferencia_cbu': config.transferencia_cbu or '',
            'pago_tarjeta': config.pago_tarjeta,
            'pago_online': config.pago_online,
            'pago_online_link': config.pago_online_link or '',
            'descuento_efectivo_porcentaje': float(config.descuento_efectivo_porcentaje) if config.descuento_efectivo_porcentaje else 0,
            'envios_disponibles': config.envios_disponibles,
            'envios_locales': config.envios_locales or '',
            'envios_nacionales': config.envios_nacionales or '',
            'costo_envio_local': float(config.costo_envio_local) if config.costo_envio_local else None,
            'costo_envio_nacional': float(config.costo_envio_nacional) if config.costo_envio_nacional else None,
            'politica_envio': config.politica_envio or '',
        }
    except Exception as e:
        logger.warning(f"Error obteniendo configuración del sistema: {e}")
        return {}


def es_cliente_nuevo(cliente: Cliente, conversacion: Conversacion = None) -> bool:
    """
    Determina si es un cliente nuevo (sin nombre o primera interacción en esta conversación).
    """
    # Si no tiene nombre o tiene uno genérico, es nuevo
    if not cliente.nombre or cliente.nombre.startswith('Cliente ') or cliente.nombre.lower() in ['hola', 'holi', 'hi']:
        return True
    
    # Si se proporciona la conversación, verificar si es el primer mensaje del cliente en esta conversación
    if conversacion:
        mensajes_cliente = conversacion.mensajes.filter(emisor='Cliente').count()
        return mensajes_cliente <= 1
    
    # Si no hay conversación, verificar conversaciones previas
    conversaciones_previas = Conversacion.objects.filter(cliente=cliente).exclude(mensajes__isnull=True).count()
    return conversaciones_previas <= 1


def extraer_y_guardar_nombre(mensaje: str, cliente: Cliente) -> Optional[str]:
    """
    Extrae el nombre del cliente del mensaje y lo guarda si es válido.
    Retorna el nombre extraído o None.
    """
    mensaje_original = mensaje.strip()
    mensaje_lower = mensaje_original.lower()
    
    # Palabras a excluir que no son nombres
    palabras_excluidas = ['hola', 'holi', 'hi', 'hey', 'gracias', 'quiero', 'precio', 'cuanto', 'cuánto', 
                          'tengo', 'tiene', 'hay', 'disponible', 'stock', 'venden', 'venden', 'me', 'te', 
                          'le', 'nos', 'les', 'mi', 'tu', 'su', 'nuestro', 'vuestro', 'su', 'el', 'la', 
                          'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'en', 'con', 'por', 
                          'para', 'a', 'al', 'es', 'son', 'está', 'están', 'soy', 'eres', 'es', 'somos', 
                          'son', 'fue', 'fueron', 'será', 'serán', 'si', 'sí', 'no', 'también', 'tampoco']
    
    # Patrones mejorados para detectar nombre (incluyendo nombres con apellido)
    patrones = [
        r'me llamo\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
        r'soy\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
        r'mi nombre es\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
        r'me dicen\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
        r'^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)$',  # Solo el nombre
        # Patrón más flexible para "me llamo emanuel sosa"
        r'(?:me\s+llamo|soy|mi\s+nombre\s+es|me\s+dicen)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
    ]
    
    nombre_extraido = None
    for patron in patrones:
        match = re.search(patron, mensaje_original, re.IGNORECASE)
        if match:
            nombre_candidato = match.group(1).strip()
            # Capitalizar correctamente (primera letra de cada palabra)
            palabras_nombre = nombre_candidato.split()
            nombre_formateado = ' '.join([palabra.capitalize() for palabra in palabras_nombre])
            
            # Validar que no sea muy corto ni muy largo
            if 2 <= len(nombre_formateado) <= 50:
                # Verificar que no sea una palabra excluida
                palabras_nombre_lower = [p.lower() for p in palabras_nombre]
                if not any(palabra in palabras_excluidas for palabra in palabras_nombre_lower):
                    nombre_extraido = nombre_formateado
                    break
    
    # Si encontramos un nombre válido y el cliente no tiene nombre o tiene uno genérico/inválido
    if nombre_extraido:
        nombre_actual = cliente.nombre or ''
        nombre_actual_lower = nombre_actual.lower()
        
        # Solo actualizar si no tiene nombre o tiene uno genérico/inválido
        if (not nombre_actual or 
            nombre_actual.startswith('Cliente ') or 
            nombre_actual_lower in ['hola', 'holi', 'hi', 'hey'] or
            len(nombre_actual) < 3):
            cliente.nombre = nombre_extraido
            cliente.save()
            logger.info(f"Nombre guardado para cliente {cliente.telefono}: {nombre_extraido}")
            print(f"[CRM] Nombre guardado: {nombre_extraido} para cliente {cliente.telefono}")
            return nombre_extraido
    
    return None


def obtener_precios_producto(variante: ProductoVariante) -> Dict:
    """
    Obtiene los precios de un producto (minorista y mayorista).
    """
    precios = Precio.objects.filter(
        variante=variante,
        activo=True
    ).select_related('variante')
    
    precios_dict = {
        'minorista_ars': None,
        'mayorista_ars': None,
    }
    
    for precio in precios:
        if precio.tipo == Precio.Tipo.MINORISTA and precio.moneda == Precio.Moneda.ARS:
            precios_dict['minorista_ars'] = float(precio.precio)
        elif precio.tipo == Precio.Tipo.MAYORISTA and precio.moneda == Precio.Moneda.ARS:
            precios_dict['mayorista_ars'] = float(precio.precio)
    
    return precios_dict


def generar_respuesta_humana(
    mensaje_cliente: str,
    cliente: Cliente,
    conversacion: Conversacion,
    historial_mensajes: List[Mensaje],
    productos_encontrados: List[ProductoVariante] = None
) -> Tuple[str, Dict]:
    """
    Genera una respuesta humana y natural usando IA, considerando:
    - Contexto del cliente
    - Historial de la conversación
    - Productos encontrados
    - Preferencias y compras anteriores
    
    Returns:
        (respuesta_texto, metadata) donde metadata contiene información adicional
    """
    
    # Obtener contexto completo del cliente
    contexto_cliente = obtener_contexto_cliente(cliente, conversacion)
    
    # Buscar productos si no se proporcionaron
    if productos_encontrados is None:
        productos_encontrados = buscar_productos_en_mensaje(mensaje_cliente)
    
    # Construir información de productos encontrados
    productos_info = []
    for variante in productos_encontrados:
        precios = obtener_precios_producto(variante)
        categoria = variante.producto.categoria.nombre if variante.producto.categoria else "Sin categoría"
        atributos = f" - {variante.atributo_1}" if variante.atributo_1 else ""
        atributos += f" - {variante.atributo_2}" if variante.atributo_2 else ""
        
        productos_info.append({
            'nombre': variante.producto.nombre,
            'sku': variante.sku,
            'atributos': atributos.strip(),
            'categoria': categoria,
            'stock': variante.stock_actual,
            'precio_minorista': precios['minorista_ars'],
            'precio_mayorista': precios['mayorista_ars'],
        })
    
    # Obtener configuración del sistema
    config_sistema = obtener_configuracion_sistema()
    
    # Verificar si es cliente nuevo (pasar la conversación para verificar si es el primer mensaje)
    cliente_nuevo = es_cliente_nuevo(cliente, conversacion)
    
    # Construir historial de la conversación
    historial_texto = "\n".join([
        f"{'Cliente' if m.emisor == 'Cliente' else 'Vendedor'}: {m.contenido}"
        for m in historial_mensajes[-6:]  # Últimos 6 mensajes
    ])
    
    # Verificar si ya se mencionó garantía/servicio post-venta en esta conversación
    ya_menciono_garantia = any(
        'garantía' in m.contenido.lower() or 'garantia' in m.contenido.lower() or 
        'servicio post-venta' in m.contenido.lower() or 'post-venta' in m.contenido.lower()
        for m in historial_mensajes
        if m.emisor != 'Cliente'  # Solo verificar mensajes del sistema/vendedor
    )
    
    # Detectar si el cliente está preguntando por nombre
    mensaje_lower = mensaje_cliente.lower()
    pregunta_nombre = any(palabra in mensaje_lower for palabra in ['me llamo', 'soy', 'mi nombre es', 'me dicen'])
    
    # Construir información de configuración para el prompt
    config_texto = f"""
**CONFIGURACIÓN DEL NEGOCIO (USAR SIEMPRE ESTOS DATOS):**
- Nombre del local: {config_sistema.get('nombre_local', 'ImportStore')}
- Dirección: {config_sistema.get('direccion', 'No configurado')}
- Ubicación: {config_sistema.get('ubicacion_mapa', '')}
- Google Maps: {config_sistema.get('google_maps_url', '')}
- CUIT: {config_sistema.get('cuit', 'No configurado')}
- Teléfono local: {config_sistema.get('telefono_local', '')}
- WhatsApp: {config_sistema.get('telefono_whatsapp', '')}
- Email: {config_sistema.get('correo_contacto', '')}
- Horarios L-V: {config_sistema.get('horario_lunes_a_viernes', 'No configurado')}
- Horarios Sábados: {config_sistema.get('horario_sabados', 'No configurado')}
- Horarios Domingos: {config_sistema.get('horario_domingos', 'No configurado')}
- Instagram principal: {config_sistema.get('instagram_principal', '')}
- Instagram secundario: {config_sistema.get('instagram_secundario', '')}
- TikTok: {config_sistema.get('tiktok', '')}
- Facebook: {config_sistema.get('facebook', '')}
- Métodos de pago: Efectivo local: {config_sistema.get('pago_efectivo_local', False)}, Efectivo retiro: {config_sistema.get('pago_efectivo_retiro', False)}, Transferencia: {config_sistema.get('pago_transferencia', False)}, Tarjeta: {config_sistema.get('pago_tarjeta', False)}, Online: {config_sistema.get('pago_online', False)}
- Transferencia Alias: {config_sistema.get('transferencia_alias', '')}
- Transferencia CBU: {config_sistema.get('transferencia_cbu', '')}
- Descuento efectivo/transferencia: {config_sistema.get('descuento_efectivo_porcentaje', 0)}%
- Envíos disponibles: {config_sistema.get('envios_disponibles', False)}
- Envíos locales: {config_sistema.get('envios_locales', '')}
- Envíos nacionales: {config_sistema.get('envios_nacionales', '')}
- Costo envío local: ${config_sistema.get('costo_envio_local', 0) if config_sistema.get('costo_envio_local') else 'Consultar'}
- Política de envío: {config_sistema.get('politica_envio', '')}
"""
    
    # Construir prompt para la IA con las nuevas reglas
    prompt = f"""Tu nombre es ISAC (ImportStore Asistente de Atención y Conversión). Sos un asistente virtual humano, cálido, profesional, vendedor y confiable. Nada robótico. Frases cortas, claras, naturales y con energía positiva.

**CONTEXTO DEL CLIENTE:**
- Nombre: {contexto_cliente['cliente']['nombre']}
- Es cliente nuevo: {cliente_nuevo}
- Tipo de cliente: {contexto_cliente['cliente']['tipo']}
- Compras anteriores: {len(contexto_cliente['historial_compras'])} compras registradas
- Productos de interés: {', '.join(contexto_cliente['productos_interes'][:3]) if contexto_cliente['productos_interes'] else 'Ninguno aún'}
- Total de interacciones: {contexto_cliente.get('contexto_persistente', {}).get('total_interacciones', 0)}

{config_texto}

**HISTORIAL DE LA CONVERSACIÓN:**
{historial_texto if historial_texto else 'Esta es la primera interacción'}

**CONTEXTO IMPORTANTE:**
- ¿Ya se mencionó garantía/servicio post-venta en esta conversación? {('SÍ, ya se mencionó. NO lo repitas.' if ya_menciono_garantia else 'NO, aún no se mencionó. Podés mencionarlo si es relevante.')}

**ÚLTIMO MENSAJE DEL CLIENTE:**
"{mensaje_cliente}"

**PRODUCTOS ENCONTRADOS EN EL INVENTARIO:**
{json.dumps(productos_info, indent=2, ensure_ascii=False) if productos_info else 'No se encontraron productos específicos'}

**REGLAS CRÍTICAS (SEGUIR SIEMPRE):**

1. **IDENTIDAD**: Tu nombre es ISAC (una sola A, no Isaac). Presentate como asistente virtual de {config_sistema.get('nombre_local', 'ImportStore')}.

2. **CLIENTE NUEVO Y SALUDOS**: 
   - **SOLO saludar si es la PRIMERA VEZ que el cliente escribe en esta conversación** (no saludar en cada mensaje)
   - Si es cliente nuevo Y es el primer mensaje: "¡Hola! ¿Cómo estás? Soy ISAC, asistente virtual de {config_sistema.get('nombre_local', 'ImportStore')}."
   - Si no tiene nombre guardado Y es el primer mensaje: "¿Cuál es tu nombre? Así te atiendo bien personalizado 😊"
   - Cuando diga su nombre, confirmalo: "Un gusto, [NOMBRE] 😄 ¿En qué te puedo ayudar hoy?"
   - **Si ya tiene nombre guardado Y NO es el primer mensaje, NO saludar de nuevo**, solo responder directamente a su pregunta
   - **IMPORTANTE: NO repetir saludos en cada mensaje. Solo saludar en el primer mensaje de la conversación.**

3. **PRODUCTOS**: Cuando pregunten por un producto:
   - Buscar y mostrar el producto encontrado
   - SI HAY STOCK: Mostrar foto automáticamente (mencionar que se envía), mostrar precios así:
     * Precio Normal: $X
     * Precio Oferta: $Y (SIEMPRE destacarlo como beneficio)
     * Precio Mayorista: $Z (si existe y es mayorista)
   - SIEMPRE ofrecer la oferta: "Mirá {contexto_cliente['cliente']['nombre']}, el precio normal es $X, pero hoy te lo puedo dejar a $Y 😁🔥"
   - SI NO HAY STOCK: "Ese modelo puntual no lo tengo ahora, {contexto_cliente['cliente']['nombre']}, pero mirá estas opciones similares 👇🔥" y sugerir 3 alternativas relacionadas

4. **CONFIGURACIONES**: Cuando pregunten por dirección, horarios, nombre del local, ubicación, CUIT, medios de pago, envíos, redes sociales:
   - SIEMPRE usar SOLO los datos de CONFIGURACIÓN proporcionados arriba
   - NUNCA inventar nada
   - Si algo existe en configuración, usarlo sí o sí
   - Ejemplos:
     * "¿Dónde están?" → Usar dirección y Google Maps URL de configuración
     * "¿Qué horarios tienen?" → Usar horarios de configuración
     * "¿Aceptan tarjeta?" → Usar datos de métodos de pago de configuración
     * "¿Hacen envíos?" → Usar datos de envíos de configuración
     * "¿Tienen Instagram?" → Listar las redes sociales de configuración

5. **MÉTODOS DE PAGO**: Siempre mencionar:
   - "Podés pagar en efectivo en el local, en efectivo al retirar, por transferencia bancaria, o con tarjeta."
   - Si hay descuento por efectivo/transferencia: "Si pagás en efectivo o transferencia tenés un descuento exclusivo del {config_sistema.get('descuento_efectivo_porcentaje', 0)}% 😉🔥"
   - Si hay alias/CBU configurado, mencionarlo cuando pregunten por transferencia

6. **PRESUPUESTOS**: Si piden presupuesto:
   - Preguntar: "Perfecto {contexto_cliente['cliente']['nombre']} 😄 ¿A nombre de quién preparo el presupuesto?"
   - Luego mencionar que se preparará un PDF profesional con todos los detalles

7. **CIERRE DE VENTA**: Siempre intentar cerrar:
   - "¿Querés que te lo reserve, {contexto_cliente['cliente']['nombre']}? Hoy te queda a $[PRECIO_OFERTA] y lo podés retirar cuando quieras 😉"

8. **FALTA DE RESPUESTA**: Si pasan más de 3 horas sin responder:
   - "¿Seguís ahí {contexto_cliente['cliente']['nombre']}? 😊 Si querés te ayudo a elegir algo según tu presupuesto."
   - Si pasan 24 horas: "¡Hola {contexto_cliente['cliente']['nombre']}! ¿Te quedó alguna duda? Estoy para ayudarte 😄"

9. **TONO**: 
   - Natural, cálido, argentino, profesional
   - Sin tecnicismos, sin lenguaje robótico
   - Emojis moderados (2-3 máximo por mensaje, no abusar)
   - Frases cortas
   - Persuasivo pero amable

10. **OFERTAS AUTOMÁTICAS**: Cuando pregunten por precio, SIEMPRE ofrecer:
    - "Normalmente vale $[PRECIO_NORMAL], pero te lo puedo dejar ahora a $[PRECIO_OFERTA]. ¿Querés que te lo reserve?"

**IMPORTANTE:**
- La respuesta debe ser en español argentino
- Máximo 150 palabras (respuestas cortas y directas)
- Usa saltos de línea (ENTER) para separar ideas y hacer el mensaje más legible
- Estructura tu respuesta así:
  * Primera línea: Saludo breve y respuesta directa
  * Línea en blanco
  * Si hay productos: Lista breve con nombre y precio (una línea por producto)
  * Línea en blanco
  * Cierre: Pregunta o llamado a la acción
- NO uses formato markdown (sin asteriscos, sin guiones bajos, sin comillas dobles)
- NO uses ""texto"" para negrita, solo escribe el texto normal
- Escribe todo en texto plano, usa ENTER para separar párrafos
- Si hay múltiples productos, mencioná SOLO el más relevante (no más de 1-2)
- NUNCA uses la palabra "original" al describir productos
- **GARANTÍA Y SERVICIO POST-VENTA**: Solo mencioná esto UNA VEZ por conversación, cuando sea relevante (al cerrar una venta o cuando el cliente pregunte). Si ya lo mencionaste antes en esta conversación, NO lo repitas.
- Formatea los precios así: $1.560.000 (con puntos de miles)

Generá una respuesta natural y humana siguiendo TODAS estas reglas:"""

    try:
        response = _invoke_gemini(prompt)
        respuesta_texto = response.text.strip()
        
        # Limpiar la respuesta de posibles prefijos de la IA
        respuesta_texto = re.sub(r'^(Respuesta|Mensaje|Vendedor):\s*', '', respuesta_texto, flags=re.IGNORECASE)
        respuesta_texto = respuesta_texto.strip()
        
        # Limpiar formato markdown incorrecto (asteriscos dobles ""texto"" -> texto)
        respuesta_texto = re.sub(r'""([^"]+)""', r'\1', respuesta_texto)  # ""texto"" -> texto
        respuesta_texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', respuesta_texto)  # **texto** -> texto (negrita)
        respuesta_texto = re.sub(r'\*([^*]+)\*', r'\1', respuesta_texto)  # *texto* -> texto (cursiva)
        respuesta_texto = re.sub(r'__([^_]+)__', r'\1', respuesta_texto)  # __texto__ -> texto
        respuesta_texto = re.sub(r'_([^_]+)_', r'\1', respuesta_texto)  # _texto_ -> texto
        
        # Formatear precios: convertir números grandes a formato con puntos (ej: 1560000 -> 1.560.000)
        def formatear_precio(match):
            numero = match.group(1)
            try:
                num = float(numero.replace('.', '').replace(',', '.'))
                if num >= 1000:
                    return f"${num:,.0f}".replace(',', '.')
                else:
                    return f"${num:,.2f}".replace(',', '.')
            except:
                return match.group(0)
        
        # Buscar patrones de precios como $1560000 o $1560000.0
        respuesta_texto = re.sub(r'\$(\d+(?:[.,]\d+)?)', formatear_precio, respuesta_texto)
        
        # Limpiar espacios múltiples pero preservar saltos de línea
        respuesta_texto = re.sub(r'[ \t]+', ' ', respuesta_texto)  # Múltiples espacios a uno
        respuesta_texto = re.sub(r' *\n *', '\n', respuesta_texto)  # Limpiar espacios alrededor de saltos de línea
        respuesta_texto = re.sub(r'\n{3,}', '\n\n', respuesta_texto)  # Máximo 2 saltos de línea seguidos
        respuesta_texto = respuesta_texto.strip()
        
        # Metadata para guardar
        metadata = {
            'productos_mencionados': [p['sku'] for p in productos_info],
            'productos_info': productos_info,  # Incluir información completa de productos
            'intencion_detectada': _detectar_intencion(mensaje_cliente),
            'requiere_asesor': _requiere_intervencion_humana(mensaje_cliente, productos_info),
            'contexto_usado': {
                'tiene_historial': len(contexto_cliente['historial_compras']) > 0,
                'productos_interes': len(contexto_cliente['productos_interes']) > 0,
            }
        }
        
        # Actualizar contexto del cliente
        actualizar_contexto_cliente(
            cliente=cliente,
            mensaje=mensaje_cliente,
            productos_mencionados=metadata['productos_mencionados'],
            metadata=metadata
        )
        
        return respuesta_texto, metadata
        
    except Exception as e:
        logger.error(f"Error generando respuesta con IA: {e}", exc_info=True)
        # Respuesta de fallback
        return _respuesta_fallback(mensaje_cliente, productos_info), {}


def obtener_imagen_producto_url(variante: 'ProductoVariante', request=None) -> Optional[str]:
    """
    Obtiene la URL pública de la primera imagen de un producto.
    Retorna None si no hay imagen disponible.
    """
    try:
        producto = variante.producto
        primera_imagen = producto.imagenes.first()
        
        if primera_imagen and primera_imagen.imagen:
            # Construir URL pública
            from django.conf import settings
            
            # Si hay request, usar el dominio del request
            if request:
                protocol = 'https' if request.is_secure() else 'http'
                host = request.get_host()
                return f"{protocol}://{host}{primera_imagen.imagen.url}"
            
            # Si no hay request, construir URL con MEDIA_URL
            # NOTA: Para producción, necesitarás configurar una URL pública (ej: ngrok, dominio propio)
            if settings.DEBUG:
                # En desarrollo, usar localhost
                return f"http://127.0.0.1:8000{primera_imagen.imagen.url}"
            else:
                # En producción, necesitas configurar ALLOWED_HOSTS y usar tu dominio
                from django.contrib.sites.models import Site
                try:
                    site = Site.objects.get_current()
                    protocol = 'https'
                    return f"{protocol}://{site.domain}{primera_imagen.imagen.url}"
                except:
                    # Fallback
                    return primera_imagen.imagen.url
        
        return None
    except Exception as e:
        logger.warning(f"Error obteniendo URL de imagen del producto: {e}")
        return None


def generar_botones_producto(producto_info: Dict, config_sistema: Dict) -> List[Dict[str, str]]:
    """
    Genera botones nativos de WhatsApp para un producto.
    """
    botones = []
    
    # Botón "Comprar ahora" si hay stock
    if producto_info.get('stock', 0) > 0:
        botones.append({
            "id": f"comprar_{producto_info['sku']}",
            "title": "Comprar ahora"
        })
    
    # Botón "Ver más modelos" (siempre disponible)
    botones.append({
        "id": "ver_mas_modelos",
        "title": "Ver más modelos"
    })
    
    # Botón "Ver ubicación" si hay Google Maps configurado
    if config_sistema.get('google_maps_url'):
        botones.append({
            "id": "ver_ubicacion",
            "title": "Ver ubicación"
        })
    # O "Hablar con asesor" si no hay ubicación
    elif len(botones) < 3:
        botones.append({
            "id": "hablar_asesor",
            "title": "Hablar asesor"
        })
    
    return botones[:3]  # WhatsApp permite máximo 3 botones


def _detectar_intencion(mensaje: str) -> str:
    """Detecta la intención del mensaje del cliente"""
    mensaje_lower = mensaje.lower()
    
    if any(palabra in mensaje_lower for palabra in ['comprar', 'quiero', 'me interesa', 'cuanto sale', 'precio']):
        return 'compra'
    elif any(palabra in mensaje_lower for palabra in ['tenes', 'hay', 'disponible', 'stock']):
        return 'consulta_stock'
    elif any(palabra in mensaje_lower for palabra in ['problema', 'error', 'no funciona', 'reclamo']):
        return 'problema'
    elif any(palabra in mensaje_lower for palabra in ['hola', 'buenas', 'buenos dias']):
        return 'saludo'
    else:
        return 'consulta_general'


def _requiere_intervencion_humana(mensaje: str, productos_info: List) -> bool:
    """Determina si la conversación requiere intervención de un asesor humano"""
    mensaje_lower = mensaje.lower()
    
    # Palabras clave que indican necesidad de asesor
    palabras_asesor = [
        'problema', 'error', 'reclamo', 'no funciona', 'defectuoso',
        'devolver', 'reembolso', 'cancelar', 'queja'
    ]
    
    if any(palabra in mensaje_lower for palabra in palabras_asesor):
        return True
    
    # Si no hay productos y el cliente pregunta algo específico
    if not productos_info and len(mensaje) > 20:
        return False  # La IA puede ayudar a buscar
    
    return False


def _respuesta_fallback(mensaje: str, productos_info: List) -> str:
    """Respuesta de fallback si la IA falla"""
    if productos_info:
        producto = productos_info[0]
        return f"¡Hola! Sí, tenemos {producto['nombre']} disponible. Stock: {producto['stock']} unidades. ¿Te interesa?"
    else:
        return "¡Hola! Gracias por contactarnos. ¿En qué puedo ayudarte hoy? Podés consultarme sobre productos, precios o stock disponible."


def actualizar_contexto_cliente(cliente: Cliente, mensaje: str, productos_mencionados: List[str], metadata: Dict = None):
    """
    Actualiza el contexto y preferencias del cliente basándose en la interacción.
    Guarda información persistente para mejorar futuras respuestas.
    """
    from crm.models import ClienteContexto
    
    try:
        # Obtener o crear contexto del cliente
        contexto, created = ClienteContexto.objects.get_or_create(cliente=cliente)
        
        # Actualizar contador de interacciones
        contexto.total_interacciones += 1
        contexto.ultima_interaccion = timezone.now()
        
        # Actualizar productos de interés
        if productos_mencionados:
            for sku in productos_mencionados:
                try:
                    variante = ProductoVariante.objects.get(sku=sku)
                    contexto.actualizar_producto_interes(variante.producto.nombre)
                    
                    # Actualizar categoría preferida
                    if variante.producto.categoria:
                        contexto.actualizar_categoria_preferida(variante.producto.categoria.nombre)
                except ProductoVariante.DoesNotExist:
                    pass
        
        # Actualizar tipo de consulta común
        if metadata and metadata.get('intencion_detectada'):
            intencion = metadata['intencion_detectada']
            # Guardar en metadata para análisis posterior
            if 'intenciones' not in contexto.metadata:
                contexto.metadata['intenciones'] = {}
            contexto.metadata['intenciones'][intencion] = contexto.metadata['intenciones'].get(intencion, 0) + 1
            
            # Determinar tipo de consulta más común
            if contexto.metadata.get('intenciones'):
                tipo_mas_comun = max(contexto.metadata['intenciones'].items(), key=lambda x: x[1])[0]
                contexto.tipo_consulta_comun = tipo_mas_comun
        
        # Actualizar tags de comportamiento
        tags = []
        if contexto.total_interacciones > 5:
            tags.append('cliente_frecuente')
        if metadata and metadata.get('intencion_detectada') == 'compra':
            tags.append('interesado_en_comprar')
        if contexto.productos_interes:
            tags.append('consulta_productos')
        
        contexto.tags_comportamiento = list(set(tags))  # Eliminar duplicados
        
        contexto.save()
        
    except Exception as e:
        logger.warning(f"Error actualizando contexto del cliente: {e}")


def analizar_intencion_compra(cliente: Cliente, conversacion: Conversacion, historial_mensajes: List[Mensaje]) -> Dict:
    """
    Analiza la intención de compra del cliente basándose en el historial de mensajes.
    Retorna un score de 0-100 y análisis detallado.
    """
    try:
        # Construir contexto para la IA
        mensajes_texto = "\n".join([
            f"{'Cliente' if m.emisor == 'Cliente' else 'Vendedor'}: {m.contenido}"
            for m in historial_mensajes[-10:]
        ])
        
        contexto_cliente = obtener_contexto_cliente(cliente, conversacion)
        
        prompt = f"""Analizá la siguiente conversación y determiná la intención de compra del cliente.

CONVERSACIÓN:
{mensajes_texto}

CONTEXTO DEL CLIENTE:
- Tipo: {contexto_cliente['cliente']['tipo']}
- Productos de interés: {', '.join(contexto_cliente.get('productos_interes', [])[:5])}
- Compras anteriores: {len(contexto_cliente.get('historial_compras', []))} compras

Analizá:
1. ¿El cliente muestra intención de comprar? (0-100)
2. ¿Qué está buscando específicamente?
3. ¿Qué factores podrían influir en su decisión?
4. ¿Qué sugerencias podrías dar para cerrar la venta?

Respondé SOLO con un JSON válido en este formato:
{{
    "score_intencion": 75,
    "nivel": "alto|medio|bajo",
    "que_busca": "Descripción breve de lo que el cliente busca",
    "factores_influyentes": ["factor1", "factor2"],
    "sugerencias": ["sugerencia1", "sugerencia2", "sugerencia3"],
    "productos_recomendados": ["producto1", "producto2"]
}}"""

        response = _invoke_gemini(prompt)
        texto = response.text.strip()
        
        # Extraer JSON
        import json as json_lib
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0].strip()
        
        resultado = json_lib.loads(texto)
        
        return {
            'score': int(resultado.get('score_intencion', 50)),
            'nivel': resultado.get('nivel', 'medio'),
            'que_busca': resultado.get('que_busca', 'No determinado'),
            'factores_influyentes': resultado.get('factores_influyentes', []),
            'sugerencias': resultado.get('sugerencias', []),
            'productos_recomendados': resultado.get('productos_recomendados', []),
        }
        
    except Exception as e:
        logger.error(f"Error analizando intención de compra: {e}", exc_info=True)
        return {
            'score': 50,
            'nivel': 'medio',
            'que_busca': 'No determinado',
            'factores_influyentes': [],
            'sugerencias': [],
            'productos_recomendados': [],
        }


def generar_resumen_cliente_ia(cliente: Cliente, conversacion: Conversacion, historial_mensajes: List[Mensaje]) -> Dict:
    """
    Genera un resumen completo del cliente usando IA:
    - Qué preguntó
    - Qué quiere
    - Resumen de la conversación
    """
    try:
        mensajes_texto = "\n".join([
            f"{'Cliente' if m.emisor == 'Cliente' else 'Vendedor'}: {m.contenido}"
            for m in historial_mensajes
        ])
        
        contexto_cliente = obtener_contexto_cliente(cliente, conversacion)
        
        prompt = f"""Analizá esta conversación y generá un resumen completo del cliente.

CONVERSACIÓN:
{mensajes_texto}

CONTEXTO:
- Cliente: {cliente.nombre}
- Tipo: {contexto_cliente['cliente']['tipo']}
- Productos de interés previos: {', '.join(contexto_cliente.get('productos_interes', [])[:5]) or 'Ninguno'}

Generá un resumen en formato JSON:
{{
    "resumen_conversacion": "Resumen breve de toda la conversación (2-3 oraciones)",
    "que_pregunto": ["pregunta1", "pregunta2", "pregunta3"],
    "que_quiere": "Descripción de lo que el cliente realmente quiere o necesita",
    "puntos_clave": ["punto1", "punto2", "punto3"],
    "siguiente_paso": "Qué debería hacer el vendedor a continuación"
}}"""

        response = _invoke_gemini(prompt)
        texto = response.text.strip()
        
        # Extraer JSON
        import json as json_lib
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0].strip()
        
        resultado = json_lib.loads(texto)
        
        return {
            'resumen_conversacion': resultado.get('resumen_conversacion', 'Sin resumen disponible'),
            'que_pregunto': resultado.get('que_pregunto', []),
            'que_quiere': resultado.get('que_quiere', 'No determinado'),
            'puntos_clave': resultado.get('puntos_clave', []),
            'siguiente_paso': resultado.get('siguiente_paso', 'Continuar la conversación'),
        }
        
    except Exception as e:
        logger.error(f"Error generando resumen del cliente: {e}", exc_info=True)
        return {
            'resumen_conversacion': 'Error al generar resumen',
            'que_pregunto': [],
            'que_quiere': 'No determinado',
            'puntos_clave': [],
            'siguiente_paso': 'Continuar la conversación',
        }

