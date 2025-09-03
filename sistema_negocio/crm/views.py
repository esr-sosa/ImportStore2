# crm/views.py
import requests # <--- AGREGA ESTA LÍNEA
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# crm/views.py
# ... (debajo de las otras importaciones)
from asistente_ia import interpreter
from django.conf import settings
import google.generativeai as genai

from .models import Conversacion, Mensaje, Cliente
# --- ¡NUEVO! Importamos nuestro servicio de WhatsApp ---
from .whatsapp_service import send_whatsapp_message

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

# crm/views.py

# ... (importaciones y otras vistas quedan igual) ...

# --- VISTA DE ENVIAR MENSAJE MODIFICADA ---
@csrf_exempt
def enviar_mensaje(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            contenido = data.get('contenido')
            
            conversacion = Conversacion.objects.select_related('cliente').get(id=conv_id)
            
            # 1. Guardar el mensaje en nuestra base de datos
            nuevo_mensaje = Mensaje.objects.create(conversacion=conversacion, emisor='Sistema', contenido=contenido)
            conversacion.save()
            
            # 2. ¡NUEVO! Enviar el mensaje por WhatsApp al cliente a través del servicio
            send_whatsapp_message(conversacion.cliente.telefono, contenido)

            return JsonResponse({'status': 'ok', 'mensaje_id': nuevo_mensaje.id, 'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M')})
        
        # --- ¡ESTA ES LA MODIFICACIÓN IMPORTANTE! ---
        except requests.exceptions.RequestException as e:
            # Si el error viene de la API de Meta, devolvemos el detalle exacto.
            error_detalle = "No se pudo obtener el detalle del error."
            if e.response:
                error_detalle = e.response.text
            return JsonResponse({'error': f"Error de Meta: {error_detalle}"}, status=400)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)

# ... (el resto de las vistas quedan igual) ...

# --- FUNCIÓN DE RESUMEN (Sin cambios) ---
@csrf_exempt
def resumir_chat_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial_chat = data.get('historial', '')
            if not historial_chat:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            prompt = f"""
                Tu tarea es actuar como un analista de ventas experto para 'ImportStore'.
                Leé la siguiente conversación y generá un informe DIRECTAMENTE en formato HTML.
                El informe debe tener la siguiente estructura:
                <h4>Puntos Clave</h4><ul><li>...resumen...</li></ul><hr class="my-3">
                <h4>Contexto Adicional</h4><p>...</p><hr class="my-3">
                <h4>Recomendaciones</h4><p>...</p>
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


# --- FUNCIÓN DE SUGERIR RESPUESTA (Sin cambios) ---
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
                1. Español de Argentina (Rioplatense Profesional).
                2. Continuidad y Coherencia.
                3. Adaptación al Cliente.
                4. Enfoque en la Solución.
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

# crm/views.py

# ... (otras vistas e importaciones) ...
# crm/views.py

# ... (importaciones y otras vistas) ...
# crm/views.py
# crm/views.py

@csrf_exempt
def whatsapp_webhook(request):
    # ... (la parte de verificación del webhook 'GET' no cambia) ...
    if request.method == 'GET':
        verify_token = settings.WHATSAPP_VERIFY_TOKEN
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode == 'subscribe' and token == verify_token:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('Error, token de verificación inválido', status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'object' in data and data['object'] == 'whatsapp_business_account':
                for entry in data.get('entry', []):
                    for change in entry.get('changes', []):
                        if 'messages' in change.get('value', {}):
                            for message in change['value']['messages']:
                                if message.get('type') == 'text':
                                    from_number = message['from']
                                    msg_body = message['text']['body']

                                    cliente, _ = Cliente.objects.get_or_create(telefono=from_number, defaults={'nombre': f"Cliente {from_number[-4:]}"})
                                    conversacion, _ = Conversacion.objects.get_or_create(cliente=cliente, fuente='WhatsApp', defaults={'estado': 'Abierta'})
                                    Mensaje.objects.create(conversacion=conversacion, emisor='Cliente', contenido=msg_body)
                                    print(f"Mensaje recibido de {from_number}: {msg_body}")

                                    # --- ¡NUEVA LÓGICA PARA CONSTRUIR EL HISTORIAL! ---
                                    ultimos_mensajes = conversacion.mensajes.order_by('-fecha_envio')[:6]
                                    historial_chat = "\n".join([f"{m.emisor}: {m.contenido}" for m in reversed(ultimos_mensajes)])

                                    # --- Llamamos a ISAC con el contexto ---
                                    query_json = interpreter.generate_query_json_from_question(msg_body, chat_history=historial_chat)
                                    if query_json and query_json.get("action") != "chat":
                                        query_results = interpreter.run_query_from_json(query_json)
                                        respuesta_cliente = interpreter.generate_final_response(msg_body, query_results, chat_history=historial_chat)

                                        if respuesta_cliente:
                                            send_whatsapp_message(from_number, respuesta_cliente)
                                            Mensaje.objects.create(
                                                conversacion=conversacion,
                                                emisor='Sistema',
                                                contenido=respuesta_cliente,
                                                enviado_por_ia=True
                                            )
                                            print(f"Respuesta de ISAC (con contexto) enviada: {respuesta_cliente}")

            return HttpResponse(status=200)
        except Exception as e:
            print(f"Error procesando webhook: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=405)