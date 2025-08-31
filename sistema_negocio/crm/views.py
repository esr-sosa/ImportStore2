from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Conversacion, Mensaje

# Create your views here.

def panel_chat(request):
    """
    Vista principal del Centro de Mando.
    Obtiene todas las conversaciones y las pasa al template.
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
    Recibe el historial de un chat y devuelve un resumen (simulado por ahora).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            historial_chat = data.get('historial', '')

            if not historial_chat:
                return JsonResponse({'error': 'No se proporcionó historial'}, status=400)

            # --- AQUÍ IRÍA LA LLAMADA REAL A LA API DE GEMINI ---
            nombre_cliente = "Cliente"
            # Simple heurística para encontrar un nombre en el historial
            if "Emanuel Sosa" in historial_chat:
                nombre_cliente = "Emanuel Sosa"

            resumen_simulado = f"""
                <ul class="list-disc pl-5 space-y-1">
                    <li>El cliente, <strong>{nombre_cliente}</strong>, inició la conversación.</li>
                    <li>Ha mostrado interés en los productos y ha hecho varias preguntas.</li>
                    <li>La conversación está activa y pendiente de una respuesta del asesor.</li>
                    <li><strong>Acción recomendada:</strong> Revisar la última pregunta del cliente y ofrecer una solución.</li>
                </ul>
            """
            # --- FIN DE LA SIMULACIÓN ---

            return JsonResponse({'resumen': resumen_simulado})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Solo se aceptan peticiones POST'}, status=405)

