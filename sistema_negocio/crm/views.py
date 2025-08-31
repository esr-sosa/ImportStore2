# crm/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# --- Nuevas importaciones ---
from django.conf import settings
import google.generativeai as genai
# --- Fin de nuevas importaciones ---

from .models import Conversacion, Mensaje

# --- Configuración de la API de Gemini ---
genai.configure(api_key=settings.GEMINI_API_KEY)
# --- Fin de la configuración ---


def panel_chat(request):
    """
    Vista principal del Centro de Mando.
    """
    conversaciones = Conversacion.objects.select_related('cliente').all().order_by('-ultima_actualizacion')
    context = {
        'conversaciones': conversaciones
    }
    return render(request, 'crm/panel_chat.html', context)


def get_conversacion_details(request, conv_id):
    """
    Proveedor de datos: Busca una conversación y devuelve sus detalles en JSON.
    """
    try:
        conversacion = Conversacion.objects.select_related('cliente').get(id=conv_id)
        mensajes = Mensaje.objects.filter(conversacion=conversacion).order_by('fecha_envio')

        cliente_data = {
            'nombre': conversacion.cliente.nombre,
            'telefono': conversacion.cliente.telefono,
            'tipo_cliente': conversacion.cliente.get_tipo_cliente_display(),
            'inicial': conversacion.cliente.nombre[0].upper() if conversacion.cliente.nombre else '?',
        }

        mensajes_data = [
            {
                'emisor': msg.emisor,
                'contenido': msg.contenido,
                'fecha_envio': msg.fecha_envio.strftime('%d de %b, %H:%M'),
            }
            for msg in mensajes
        ]
        
        response_data = {
            'cliente': cliente_data,
            'mensajes': mensajes_data,
            'fuente': conversacion.get_fuente_display(),
        }
        return JsonResponse(response_data)

    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversacion no encontrada'}, status=404)


@csrf_exempt
def enviar_mensaje(request):
    """
    Receptor de nuevos mensajes enviados por el asesor.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            contenido = data.get('contenido')

            if not conv_id or not contenido:
                return JsonResponse({'error': 'Faltan datos'}, status=400)

            conversacion = Conversacion.objects.get(id=conv_id)
            nuevo_mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                emisor='Sistema',
                contenido=contenido
            )
            conversacion.save()

            return JsonResponse({
                'status': 'ok', 
                'mensaje_id': nuevo_mensaje.id,
                'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M'),
            })

        except Conversacion.DoesNotExist:
            return JsonResponse({'error': 'La conversación no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)


@csrf_exempt
def resumir_chat_ia(request):
    """
    Recibe el historial de un chat, llama a la API de Gemini desde el backend
    y devuelve el resumen generado.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial_chat = data.get('historial', '')

            if not historial_chat:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)

            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            prompt = f"""
                Eres un asistente de ventas experto para una tienda de tecnología llamada 'ImportStore'.
                Tu tarea es leer la siguiente conversación y generar un resumen conciso en formato HTML.
                El resumen debe estar en una lista <ul> con puntos clave en <li>.
                Resalta en negrita con <strong> los productos mencionados, las intenciones de compra y las acciones recomendadas.

                Conversación:
                {historial_chat}
            """
            
            response = model.generate_content(prompt)
            resumen_generado = response.text

            return JsonResponse({'resumen': resumen_generado})

        except Exception as e:
            print(f"Error en la vista resumir_chat_ia: {e}")
            return JsonResponse({'error': 'Hubo un problema al contactar el servicio de IA.'}, status=500)

    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)


# --- ESTA ES LA FUNCIÓN QUE HEMOS MODIFICADO ---
@csrf_exempt
def sugerir_respuesta_ia(request):
    """
    Recibe el historial del chat, se enfoca en el último mensaje del cliente,
    y genera una sugerencia de respuesta para el asesor con un tono argentino y humano.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial_chat = data.get('historial', '')

            if not historial_chat:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)

            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            # --- PROMPT MEJORADO CON TUS INDICACIONES ---
            prompt = f"""
                **Misión:** Sos un asistente de ventas para 'ImportStore', una tienda de tecnología en Argentina. Tu objetivo es generar una respuesta para un asesor humano.

                **Personalidad y Tono:**
                1.  **Súper Humano y Cercano:** Hablá de forma natural, como lo haría una persona. Usá un lenguaje coloquial y amigable.
                2.  **100% Argentino:** Usá el "vos" en lugar del "tú". Evitá el español neutro a toda costa. Podés usar expresiones como "dale", "buenísimo", "no hay drama".
                3.  **Resolutivo y Profesional:** Mantené siempre un tono que inspire confianza y que busque ayudar al cliente a concretar su compra.
                4.  **No Menciones Productos Específicos:** En lugar de decir "celulares, accesorios o perfumes", usá frases más generales como "nuestra amplia gama de productos", "lo que necesites de tecnología" o similar.
                5.  **Evitá Frases Robóticas:** Nunca uses frases como "Disculpe las molestias anteriores. ¿En qué puedo ayudarle hoy...?". Sé directo y natural.

                **Tarea:**
                Leé el siguiente historial de chat, enfocándote en el último mensaje del cliente. Basado en eso, generá la respuesta perfecta que el asesor debería enviar.

                **Historial de la Conversación:**
                {historial_chat}

                **Formato de Salida:**
                Generá solo el texto de la respuesta, sin explicaciones ni saludos al asesor. Directamente lo que el cliente leería.
            """
            
            response = model.generate_content(prompt)
            sugerencia_generada = response.text.strip()
            # --- FIN DE LA MODIFICACIÓN ---

            return JsonResponse({'sugerencia': sugerencia_generada})

        except Exception as e:
            print(f"Error en la vista sugerir_respuesta_ia: {e}")
            return JsonResponse({'error': 'Hubo un problema al generar la sugerencia.'}, status=500)

    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)