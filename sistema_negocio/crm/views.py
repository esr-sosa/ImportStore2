# crm/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.conf import settings
import google.generativeai as genai

from .models import Conversacion, Mensaje, Cliente

genai.configure(api_key=settings.GEMINI_API_KEY)


def panel_chat(request):
    conversaciones = Conversacion.objects.select_related('cliente').all().order_by('-ultima_actualizacion')
    context = {'conversaciones': conversaciones}
    return render(request, 'crm/panel_chat.html', context)


def get_conversacion_details(request, conv_id):
    try:
        conversacion = Conversacion.objects.select_related('cliente').get(id=conv_id)
        mensajes = Mensaje.objects.filter(conversacion=conversacion).order_by('fecha_envio')
        cliente_data = {
            'id': conversacion.cliente.id,
            'nombre': conversacion.cliente.nombre,
            'telefono': conversacion.cliente.telefono,
            'email': conversacion.cliente.email or "No especificado",
            'tipo_cliente': conversacion.cliente.get_tipo_cliente_display(),
            'instagram': conversacion.cliente.instagram_handle or "No especificado",
            'fecha_creacion': conversacion.cliente.fecha_creacion.strftime('%d/%m/%Y'),
            'inicial': conversacion.cliente.nombre[0].upper() if conversacion.cliente.nombre else '?',
        }
        mensajes_data = [{'emisor': msg.emisor, 'contenido': msg.contenido, 'fecha_envio': msg.fecha_envio.strftime('%d de %b, %H:%M')} for msg in mensajes]
        response_data = {'cliente': cliente_data, 'mensajes': mensajes_data, 'fuente': conversacion.get_fuente_display()}
        return JsonResponse(response_data)
    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversacion no encontrada'}, status=404)


@csrf_exempt
def enviar_mensaje(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            contenido = data.get('contenido')
            if not conv_id or not contenido:
                return JsonResponse({'error': 'Faltan datos'}, status=400)
            conversacion = Conversacion.objects.get(id=conv_id)
            nuevo_mensaje = Mensaje.objects.create(conversacion=conversacion, emisor='Sistema', contenido=contenido)
            conversacion.save()
            return JsonResponse({'status': 'ok', 'mensaje_id': nuevo_mensaje.id, 'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M')})
        except Conversacion.DoesNotExist:
            return JsonResponse({'error': 'La conversación no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)


# --- FUNCIÓN DE RESUMEN ACTUALIZADA ---
@csrf_exempt
def resumir_chat_ia(request):
    """
    Genera un resumen estructurado con puntos clave, contexto y recomendaciones.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial_chat = data.get('historial', '')
            if not historial_chat:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            # --- PROMPT MEJORADO Y ESTRUCTURADO ---
            prompt = f"""
                Tu tarea es actuar como un analista de ventas experto para 'ImportStore'.
                Leé la siguiente conversación y generá un informe DIRECTAMENTE en formato HTML.

                El informe debe tener la siguiente estructura:
                
                <h4>Puntos Clave</h4>
                <ul>
                    <li>...resumen en 3 o 4 puntos...</li>
                </ul>
                <hr class="my-3">
                <h4>Contexto Adicional</h4>
                <p>...un párrafo breve explicando la situación actual de la conversación...</p>
                <hr class="my-3">
                <h4>Recomendaciones</h4>
                <p>...un párrafo con acciones claras y específicas que el asesor debería tomar a continuación para avanzar la venta o resolver la consulta...</p>

                **Instrucciones Importantes:**
                - Sé conciso y andá al grano.
                - Usá la etiqueta <strong> para resaltar las palabras más importantes.
                - NO incluyas ` ```html ` ni nada fuera de la estructura HTML solicitada.

                **Conversación a Analizar:**
                {historial_chat}
            """
            response = model.generate_content(prompt)
            resumen_limpio = response.text.replace('```html', '').replace('```', '').strip()
            return JsonResponse({'resumen': resumen_limpio})
        except Exception as e:
            print(f"Error en la vista resumir_chat_ia: {e}")
            return JsonResponse({'error': 'Hubo un problema al contactar el servicio de IA.'}, status=500)
    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)


@csrf_exempt
def sugerir_respuesta_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial_chat = data.get('historial', '')
            cliente_data = data.get('cliente', {})
            if not historial_chat:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            prompt = f"""
                **Misión:** Sos un asistente de ventas de 'ImportStore', una tienda de tecnología en Argentina. Tu tarea es generar la respuesta ideal para que un asesor la envíe a un cliente.
                **Contexto del Cliente:**
                - Nombre: {cliente_data.get('nombre', 'N/A')}
                - Tipo de Cliente: {cliente_data.get('tipo_cliente', 'N/A')}
                **Reglas de Estilo y Tono:**
                1.  **Español de Argentina (Rioplatense Profesional):** Utilizá "vos" y conjugaciones verbales correspondientes (ej. 'tenés', 'querés', 'podés'). El tono debe ser profesional, servicial y humano. Evitá el "che" o jerga excesivamente informal.
                2.  **Continuidad y Coherencia:** Analizá el historial completo para entender en qué punto se encuentra la conversación. NO saludes con "Hola" si el diálogo ya comenzó. Tu respuesta debe ser la continuación lógica del último mensaje.
                3.  **Adaptación al Cliente:** Tené en cuenta si el cliente es 'Mayorista' o 'Minorista' para adaptar sutilmente la formalidad o el enfoque de la respuesta.
                4.  **Enfoque en la Solución:** Sé proactivo. El objetivo es siempre avanzar hacia la resolución o la venta.
                **Tarea Inmediata:**
                Basado en el siguiente historial y los datos del cliente, generá únicamente el texto de la respuesta que el asesor debe enviar.
                **Historial de la Conversación:**
                {historial_chat}
            """
            response = model.generate_content(prompt)
            sugerencia_generada = response.text.strip()
            return JsonResponse({'sugerencia': sugerencia_generada})
        except Exception as e:
            print(f"Error en la vista sugerir_respuesta_ia: {e}")
            return JsonResponse({'error': 'Hubo un problema al generar la sugerencia.'}, status=500)
    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)