# crm/views.py

import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from django.core.paginator import Paginator
from django.db.models import Count, Q, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

# --- Importaciones Clave para Tiempo Real e IA ---
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asistente_ia import interpreter
from core.db_inspector import column_exists
# --- Fin de Importaciones ---

from .forms import ClienteForm
from .models import Cliente, Conversacion, Etiqueta, Mensaje
from .whatsapp_service import send_whatsapp_message

genai.configure(api_key=settings.GEMINI_API_KEY)


@login_required
def panel_chat(request):
    conversaciones = (
        Conversacion.objects.select_related('cliente', 'asesor_asignado')
        .prefetch_related('etiquetas')
        .annotate(total_mensajes=Count('mensajes'))
        .order_by('-ultima_actualizacion')
    )

    ahora = timezone.now()
    sla_ready = column_exists("crm_conversacion", "sla_vencimiento")
    if sla_ready:
        sla_vencidos = conversaciones.filter(
            sla_vencimiento__lt=ahora, estado__in=['Pendiente', 'En seguimiento']
        ).count()
    else:
        sla_vencidos = 0
        messages.warning(
            request,
            "Debés ejecutar `python manage.py migrate` para habilitar el seguimiento de SLA en el CRM.",
        )

    stats = {
        'total': conversaciones.count(),
        'abiertas': conversaciones.filter(estado='Abierta').count(),
        'pendientes': conversaciones.filter(estado='Pendiente').count(),
        'seguimiento': conversaciones.filter(estado='En seguimiento').count(),
        'sla_vencidos': sla_vencidos,
    }

    top_etiquetas = (
        Etiqueta.objects.annotate(total=Count('conversaciones')).order_by('-total', 'nombre')[:8]
    )

    context = {
        'conversaciones': conversaciones,
        'stats': stats,
        'etiquetas': top_etiquetas,
        'asesores': Conversacion.objects.exclude(asesor_asignado__isnull=True)
        .values('asesor_asignado__id', 'asesor_asignado__first_name', 'asesor_asignado__last_name')
        .distinct(),
        'sla_ready': sla_ready,
    }
    return render(request, 'crm/panel_chat.html', context)


def _clientes_context(request, form: ClienteForm):
    filtros = {
        "q": request.GET.get("q", "").strip(),
        "tipo": request.GET.get("tipo", ""),
        "page": request.GET.get("page", "1"),
    }

    clientes_qs = Cliente.objects.all().annotate(
        ultima_actividad=Max("conversaciones__ultima_actualizacion")
    )
    if filtros["q"]:
        clientes_qs = clientes_qs.filter(
            Q(nombre__icontains=filtros["q"]) | Q(telefono__icontains=filtros["q"]) | Q(email__icontains=filtros["q"])
        )
    if filtros["tipo"]:
        clientes_qs = clientes_qs.filter(tipo_cliente=filtros["tipo"])

    clientes_qs = clientes_qs.order_by("-fecha_creacion")
    paginator = Paginator(clientes_qs, 12)
    page_obj = paginator.get_page(filtros["page"])

    stats_tipo = (
        Cliente.objects.values("tipo_cliente").annotate(total=Count("id")).order_by("-total", "tipo_cliente")
    )
    nuevos_semana = Cliente.objects.filter(
        fecha_creacion__gte=timezone.now() - timedelta(days=7)
    ).count()

    try:
        conversaciones_prioritarias = (
            Conversacion.objects.select_related("cliente")
            .annotate(total_mensajes=Count("mensajes"))
            .order_by("-total_mensajes", "-ultima_actualizacion")[:5]
        )
    except Exception:
        conversaciones_prioritarias = []

    contexto = {
        "form": form,
        "page_obj": page_obj,
        "clientes": page_obj.object_list,
        "filtros": filtros,
        "stats_tipo": stats_tipo,
        "total_clientes": Cliente.objects.count(),
        "nuevos_semana": nuevos_semana,
        "conversaciones_prioritarias": conversaciones_prioritarias,
    }
    return contexto


@login_required
def clientes_panel(request):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")
        if cliente_id:  # Editar cliente existente
            cliente = get_object_or_404(Cliente, pk=cliente_id)
            form = ClienteForm(request.POST, instance=cliente)
            accion = "actualizado"
        else:  # Crear nuevo cliente
            form = ClienteForm(request.POST)
            accion = "agregado"
        
        if form.is_valid():
            cliente = form.save()
            if request.headers.get("HX-Request"):
                form = ClienteForm()
                contexto = _clientes_context(request, form)
                response = render(request, "crm/clientes/_panel_content.html", contexto)
                response["HX-Trigger"] = json.dumps(
                    {
                        "clientesActualizados": {
                            "id": cliente.id,
                            "toast": {
                                "message": f"Cliente {cliente.nombre} {accion} correctamente.",
                                "level": "success",
                            },
                        }
                    }
                )
                return response

            messages.success(request, f"Cliente {cliente.nombre} {accion} correctamente.")
            return redirect("crm:clientes")
    else:
        form = ClienteForm()

    contexto = _clientes_context(request, form)

    template = "crm/clientes/_panel_content.html" if request.headers.get("HX-Request") else "crm/clientes/panel.html"
    return render(request, template, contexto)

@login_required
def cliente_eliminar(request, cliente_id):
    """Eliminar un cliente"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    # Verificar si tiene conversaciones asociadas
    if cliente.conversaciones.exists():
        return JsonResponse({
            "error": f"No se puede eliminar el cliente {cliente.nombre} porque tiene conversaciones asociadas."
        }, status=400)
    
    nombre = cliente.nombre
    cliente.delete()
    
    messages.success(request, f"Cliente {nombre} eliminado correctamente.")
    return JsonResponse({"success": True})

@login_required
def get_conversacion_details(request, conv_id):
    # ... tu código existente ...
    try:
        conversacion = Conversacion.objects.select_related('cliente', 'asesor_asignado').prefetch_related('etiquetas').get(id=conv_id)
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
        mensajes_data = [
            {
                'emisor': msg.emisor,
                'contenido': msg.contenido,
                'fecha_envio': msg.fecha_envio.strftime('%d de %b, %H:%M'),
                'tipo': msg.tipo_mensaje,
                'enviado_por_ia': msg.enviado_por_ia,
            }
            for msg in mensajes
        ]
        response_data = {
            'cliente': cliente_data,
            'mensajes': mensajes_data,
            'fuente': conversacion.get_fuente_display(),
            'estado': conversacion.estado,
            'prioridad': conversacion.prioridad,
            'sla': conversacion.sla_vencimiento.isoformat() if conversacion.sla_vencimiento else None,
            'etiquetas': [{'id': tag.id, 'nombre': tag.nombre, 'color': tag.color} for tag in conversacion.etiquetas.all()],
            'asesor': conversacion.asesor_asignado.get_full_name() if conversacion.asesor_asignado else None,
            'resumen': conversacion.resumen,
        }
        return JsonResponse(response_data)
    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversacion no encontrada'}, status=404)

@login_required
@csrf_exempt
def enviar_mensaje(request):
    # ... tu código existente ...
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            contenido = data.get('contenido')
            metadata = data.get('metadata') or {}

            conversacion = Conversacion.objects.get(id=conv_id)

            # 1. Guardar mensaje en la DB
            nuevo_mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                emisor='Sistema',
                contenido=contenido,
                enviado_por_ia=metadata.get('enviado_por_ia', False),
                metadata=metadata or None,
            )

            # 2. Notificar al WebSocket para que se actualice la UI en tiempo real
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{conv_id}',
                {
                    'type': 'chat.message',
                    'message': {
                        'emisor': 'Sistema',
                        'contenido': nuevo_mensaje.contenido,
                        'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M'),
                        'tipo_mensaje': nuevo_mensaje.tipo_mensaje,
                    }
                }
            )
            
            # 3. Enviar por WhatsApp
            send_whatsapp_message(conversacion.cliente.telefono, contenido)

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Solo POST'}, status=405)


@login_required
@csrf_exempt
def actualizar_conversacion(request, conv_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo POST'}, status=405)

    try:
        conversacion = Conversacion.objects.get(pk=conv_id)
    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversación no encontrada'}, status=404)

    data = json.loads(request.body or '{}')

    nuevo_estado = data.get('estado')
    prioridad = data.get('prioridad')
    sla = data.get('sla')
    etiquetas_ids = data.get('etiquetas', [])
    resumen = data.get('resumen')

    if nuevo_estado and nuevo_estado in dict(Conversacion.ESTADO_CHOICES):
        conversacion.estado = nuevo_estado
    if prioridad and prioridad in dict(Conversacion.PRIORIDAD_CHOICES):
        conversacion.prioridad = prioridad
    if sla:
        try:
            parsed = timezone.datetime.fromisoformat(sla)
            if timezone.is_naive(parsed):
                parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
            conversacion.sla_vencimiento = parsed
        except ValueError:
            pass
    if resumen is not None:
        conversacion.resumen = resumen
    if etiquetas_ids:
        conversacion.etiquetas.set(Etiqueta.objects.filter(id__in=etiquetas_ids))

    conversacion.save()

    return JsonResponse({'status': 'ok'})


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
