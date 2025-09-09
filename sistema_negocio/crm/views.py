# crm/views.py

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from django.conf import settings
import google.generativeai as genai

# --- Importaciones Clave para Tiempo Real e IA ---
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asistente_ia import interpreter
# --- Fin de Importaciones ---

from .models import Conversacion, Mensaje, Cliente
from .whatsapp_service import send_whatsapp_message

genai.configure(api_key=settings.GEMINI_API_KEY)


# ... (las otras vistas como panel_chat, get_conversacion_details, etc., no cambian) ...
def panel_chat(request):
    # ... tu código existente ...
    conversaciones = Conversacion.objects.select_related('cliente').all().order_by('-ultima_actualizacion')
    context = {'conversaciones': conversaciones}
    return render(request, 'crm/panel_chat.html', context)

def get_conversacion_details(request, conv_id):
    # ... tu código existente ...
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
    # ... tu código existente ...
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            contenido = data.get('contenido')
            
            conversacion = Conversacion.objects.get(id=conv_id)
            
            # 1. Guardar mensaje en la DB
            nuevo_mensaje = Mensaje.objects.create(conversacion=conversacion, emisor='Sistema', contenido=contenido)
            
            # 2. Notificar al WebSocket para que se actualice la UI en tiempo real
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{conv_id}',
                {
                    'type': 'chat.message',
                    'message': {
                        'emisor': 'Sistema',
                        'contenido': nuevo_mensaje.contenido,
                        'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M')
                    }
                }
            )
            
            # 3. Enviar por WhatsApp
            send_whatsapp_message(conversacion.cliente.telefono, contenido)

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Solo POST'}, status=405)


# --- ¡FUNCIÓN COMPLETAMENTE ACTUALIZADA! ---
@csrf_exempt
def whatsapp_webhook(request):
    # Verificación del Webhook (se usa una sola vez al configurar en Meta)
    if request.method == 'GET':
        verify_token = settings.WHATSAPP_VERIFY_TOKEN
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == verify_token:
            print("Webhook verificado con éxito!")
            return HttpResponse(challenge, status=200)
        else:
            print("Falló la verificación del Webhook.")
            return HttpResponse('Error, token de verificación inválido', status=403)

    # Procesar mensajes entrantes de clientes
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'object' in data and data.get('object') == 'whatsapp_business_account':
                for entry in data.get('entry', []):
                    for change in entry.get('changes', []):
                        if 'messages' in change.get('value', {}):
                            for message in change['value']['messages']:
                                from_number = message['from']
                                
                                cliente, _ = Cliente.objects.get_or_create(telefono=from_number, defaults={'nombre': f"Cliente {from_number[-4:]}"})
                                conversacion, _ = Conversacion.objects.get_or_create(cliente=cliente, fuente='WhatsApp', defaults={'estado': 'Abierta'})
                                
                                msg_type = message.get('type')
                                msg_body_for_ia = ""
                                nuevo_mensaje = None

                                # 1. GUARDAR EL MENSAJE ENTRANTE Y NOTIFICAR AL FRONTEND
                                if msg_type == 'text':
                                    msg_body_for_ia = message['text']['body']
                                    nuevo_mensaje = Mensaje.objects.create(conversacion=conversacion, emisor='Cliente', contenido=msg_body_for_ia, tipo_mensaje='texto')
                                
                                elif msg_type in ['image', 'audio', 'document', 'video']:
                                    # Por ahora, solo registramos que llegó un archivo. La descarga es un paso futuro.
                                    msg_body_for_ia = f"[{msg_type.capitalize()} recibido por el cliente]"
                                    nuevo_mensaje = Mensaje.objects.create(conversacion=conversacion, emisor='Cliente', contenido=msg_body_for_ia, tipo_mensaje=msg_type)

                                if nuevo_mensaje:
                                    print(f"Mensaje guardado de {from_number}: {nuevo_mensaje.contenido}")
                                    # Notificamos al frontend via WebSocket que llegó un nuevo mensaje
                                    channel_layer = get_channel_layer()
                                    async_to_sync(channel_layer.group_send)(
                                        f'chat_{conversacion.id}',
                                        {
                                            'type': 'chat.message',
                                            'message': {
                                                'emisor': nuevo_mensaje.emisor,
                                                'contenido': nuevo_mensaje.contenido,
                                                'tipo_mensaje': nuevo_mensaje.tipo_mensaje,
                                                'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M')
                                            }
                                        }
                                    )

                                # 2. ACTIVAR A ISAC PARA QUE ANALICE Y RESPONDA
                                # Construimos el historial de la conversación para darle contexto a la IA
                                ultimos_mensajes = conversacion.mensajes.order_by('-fecha_envio')[:6]
                                historial_chat = "\n".join([f"{m.emisor}: {m.contenido}" for m in reversed(ultimos_mensajes)])
                                
                                query_json = interpreter.generate_query_json_from_question(msg_body_for_ia, chat_history=historial_chat)
                                
                                # Si la IA determina que es una pregunta que requiere acción (y no un simple saludo)
                                if query_json and query_json.get("action") != "chat":
                                    query_results = interpreter.run_query_from_json(query_json)
                                    respuesta_cliente = interpreter.generate_final_response(msg_body_for_ia, query_results, chat_history=historial_chat)
                                    
                                    if respuesta_cliente:
                                        # Enviamos la respuesta de la IA por WhatsApp
                                        send_whatsapp_message(from_number, respuesta_cliente)
                                        
                                        # Guardamos la respuesta de la IA en nuestra base de datos
                                        mensaje_ia = Mensaje.objects.create(
                                            conversacion=conversacion,
                                            emisor='Sistema',
                                            contenido=respuesta_cliente,
                                            enviado_por_ia=True,
                                            tipo_mensaje='texto'
                                        )
                                        print(f"Respuesta de ISAC enviada a {from_number}: {respuesta_cliente}")

                                        # Notificamos al frontend sobre la respuesta de la IA
                                        async_to_sync(channel_layer.group_send)(
                                            f'chat_{conversacion.id}',
                                            {
                                                'type': 'chat.message',
                                                'message': {
                                                    'emisor': mensaje_ia.emisor,
                                                    'contenido': mensaje_ia.contenido,
                                                    'tipo_mensaje': mensaje_ia.tipo_mensaje,
                                                    'fecha_envio': mensaje_ia.fecha_envio.strftime('%d de %b, %H:%M')
                                                }
                                            }
                                        )

            return HttpResponse(status=200)
        except Exception as e:
            print(f"Error procesando el webhook: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=405)

@csrf_exempt
def resumir_chat_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial = data.get('historial', '')

            if not historial:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)

            # Usamos una función del intérprete específica para resúmenes (debemos crearla)
            # Por ahora, vamos a simularla para que no falle.
            # En un futuro, llamaríamos a algo como:
            # resumen = interpreter.generate_summary_from_history(historial)
            
            # SIMULACIÓN TEMPORAL:
            resumen = "Este es un resumen de la conversación generado por IA. El cliente parece interesado en los iPhones y preguntó por los precios. Se le proporcionó la información solicitada."

            return JsonResponse({'resumen': resumen})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def sugerir_respuesta_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial = data.get('historial', '')
            cliente_info = data.get('cliente', {}) # Obtenemos info del cliente
            
            if not historial:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)

            # Extraemos la última pregunta del historial para darle más contexto a la IA
            ultima_pregunta = historial.strip().split('\n')[-1]

            # Llamamos a la función que ya tenemos en nuestro intérprete
            sugerencia = interpreter.generate_final_response(
                question=ultima_pregunta,
                query_results="Basado en el historial, necesito sugerir una buena respuesta.", # Le damos un contexto a la IA
                chat_history=historial
            )

            return JsonResponse({'sugerencia': sugerencia})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
