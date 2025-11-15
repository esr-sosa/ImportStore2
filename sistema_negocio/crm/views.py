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
from .models import Cliente, Conversacion, Etiqueta, Mensaje, Cotizacion, ClienteContexto
from .whatsapp_service import send_whatsapp_message
from inventario.models import ProductoVariante, Precio
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

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
            try:
                channel_layer = get_channel_layer()
                if channel_layer:
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
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"No se pudo enviar notificación WebSocket: {e}")
            
            # 3. Enviar por WhatsApp (no fallar si hay error, solo loguear)
            try:
                send_whatsapp_message(conversacion.cliente.telefono, contenido)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error enviando mensaje por WhatsApp: {e}", exc_info=True)
                # No fallar la request, solo loguear el error

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

        # Debug logging
        print(f"[WEBHOOK DEBUG] Mode: {mode}")
        print(f"[WEBHOOK DEBUG] Token recibido: {token}")
        print(f"[WEBHOOK DEBUG] Token esperado: {verify_token}")
        print(f"[WEBHOOK DEBUG] Challenge: {challenge}")

        if not verify_token:
            print("[WEBHOOK ERROR] WHATSAPP_VERIFY_TOKEN no está configurado en .env")
            return HttpResponse('Error: Token de verificación no configurado', status=500)

        if mode == 'subscribe' and token == verify_token:
            print("[WEBHOOK] ¡Webhook verificado con éxito!")
            return HttpResponse(challenge, status=200)
        else:
            print(f"[WEBHOOK ERROR] Falló la verificación. Mode={mode}, Token coincide={token == verify_token if verify_token else False}")
            return HttpResponse('Error, token de verificación inválido', status=403)

    # Procesar mensajes entrantes de clientes
    if request.method == 'POST':
        try:
            print(f"[WEBHOOK] POST recibido - Content-Type: {request.content_type}")
            print(f"[WEBHOOK] Body length: {len(request.body)} bytes")
            
            # Obtener channel_layer al inicio para usarlo en todo el scope
            try:
                channel_layer = get_channel_layer()
            except Exception as e:
                print(f"[WARNING] No se pudo obtener channel_layer (Redis puede no estar disponible): {e}")
                channel_layer = None
            
            data = json.loads(request.body)
            print(f"[WEBHOOK] Datos parseados - object: {data.get('object')}")
            
            if 'object' in data and data.get('object') == 'whatsapp_business_account':
                print("[WEBHOOK] Procesando mensaje de WhatsApp Business Account")
                for entry in data.get('entry', []):
                    print(f"[WEBHOOK] Procesando entry: {entry.get('id')}")
                    for change in entry.get('changes', []):
                        print(f"[WEBHOOK] Procesando change: {change.get('field')}")
                        if 'messages' in change.get('value', {}):
                            messages_list = change['value']['messages']
                            print(f"[WEBHOOK] Mensajes encontrados: {len(messages_list)}")
                            for message in messages_list:
                                from_number = message.get('from')
                                print(f"[WEBHOOK] Procesando mensaje de {from_number}, tipo: {message.get('type')}")
                                
                                cliente, _ = Cliente.objects.get_or_create(telefono=from_number, defaults={'nombre': f"Cliente {from_number[-4:]}"})
                                conversacion, _ = Conversacion.objects.get_or_create(cliente=cliente, fuente='WhatsApp', defaults={'estado': 'Abierta'})
                                
                                msg_type = message.get('type')
                                msg_body_for_ia = ""
                                nuevo_mensaje = None

                                # 1. GUARDAR EL MENSAJE ENTRANTE Y NOTIFICAR AL FRONTEND
                                if msg_type == 'text':
                                    msg_body_for_ia = message['text']['body']
                                    msg_id_whatsapp = message.get('id')
                                    
                                    # Verificar si el mensaje ya existe (evitar duplicados)
                                    mensaje_existente = None
                                    if msg_id_whatsapp:
                                        mensaje_existente = Mensaje.objects.filter(
                                            conversacion=conversacion,
                                            metadata__whatsapp_id=msg_id_whatsapp
                                        ).first()
                                    
                                    if not mensaje_existente:
                                        # Verificar también por contenido y tiempo (últimos 30 segundos)
                                        from datetime import timedelta
                                        from django.utils import timezone
                                        mensaje_reciente = Mensaje.objects.filter(
                                            conversacion=conversacion,
                                            emisor='Cliente',
                                            contenido=msg_body_for_ia,
                                            fecha_envio__gte=timezone.now() - timedelta(seconds=30)
                                        ).first()
                                        
                                        if not mensaje_reciente:
                                            nuevo_mensaje = Mensaje.objects.create(
                                                conversacion=conversacion, 
                                                emisor='Cliente', 
                                                contenido=msg_body_for_ia, 
                                                tipo_mensaje='texto',
                                                metadata={'whatsapp_id': msg_id_whatsapp} if msg_id_whatsapp else {}
                                            )
                                        else:
                                            print(f"[WEBHOOK] Mensaje duplicado detectado (contenido reciente), ignorando")
                                            nuevo_mensaje = None
                                    else:
                                        print(f"[WEBHOOK] Mensaje duplicado detectado (whatsapp_id existente), ignorando")
                                        nuevo_mensaje = None
                                
                                elif msg_type in ['image', 'audio', 'document', 'video']:
                                    # Por ahora, solo registramos que llegó un archivo. La descarga es un paso futuro.
                                    msg_body_for_ia = f"[{msg_type.capitalize()} recibido por el cliente]"
                                    nuevo_mensaje = Mensaje.objects.create(conversacion=conversacion, emisor='Cliente', contenido=msg_body_for_ia, tipo_mensaje=msg_type)

                                if nuevo_mensaje:
                                    print(f"[WEBHOOK] Mensaje guardado de {from_number}: {nuevo_mensaje.contenido}")
                                    # Notificamos al frontend via WebSocket que llegó un nuevo mensaje
                                    if channel_layer:
                                        try:
                                            async_to_sync(channel_layer.group_send)(
                                                f'chat_{conversacion.id}',
                                                {
                                                    'type': 'chat.message',
                                                    'message': {
                                                        'emisor': nuevo_mensaje.emisor,
                                                        'contenido': nuevo_mensaje.contenido,
                                                        'tipo_mensaje': nuevo_mensaje.tipo_mensaje,
                                                        'fecha_envio': nuevo_mensaje.fecha_envio.strftime('%d de %b, %H:%M'),
                                                        'enviado_por_ia': getattr(nuevo_mensaje, 'enviado_por_ia', False)
                                                    }
                                                }
                                            )
                                            print(f"[WEBHOOK] Notificación WebSocket enviada para mensaje del cliente")
                                        except Exception as e:
                                            print(f"[WARNING] No se pudo enviar notificación WebSocket: {e}")
                                            import traceback
                                            traceback.print_exc()

                                # 2. EXTRAER Y GUARDAR NOMBRE SI ES CLIENTE NUEVO (solo si hay mensaje nuevo)
                                if nuevo_mensaje and msg_body_for_ia:
                                    from crm.services.ai_crm_service import extraer_y_guardar_nombre, es_cliente_nuevo
                                    # Verificar si es cliente nuevo antes de extraer nombre
                                    if es_cliente_nuevo(cliente, conversacion):
                                        nombre_extraido = extraer_y_guardar_nombre(msg_body_for_ia, cliente)
                                        if nombre_extraido:
                                            # Actualizar el objeto cliente en memoria
                                            cliente.refresh_from_db()
                                            print(f"[WEBHOOK] Nombre extraído y guardado: {nombre_extraido}")
                                
                                # 3. ACTIVAR A ISAC PARA QUE ANALICE Y RESPONDA CON CONTEXTO DEL CLIENTE (solo si hay mensaje nuevo)
                                if nuevo_mensaje and msg_body_for_ia:
                                    from crm.services.ai_crm_service import generar_respuesta_humana
                                    
                                    # Refrescar cliente para obtener nombre actualizado
                                    cliente.refresh_from_db()
                                    
                                    # Obtener historial de mensajes para contexto
                                    total_mensajes = conversacion.mensajes.count()
                                    if total_mensajes > 10:
                                        ultimos_mensajes = list(conversacion.mensajes.order_by('fecha_envio')[total_mensajes-10:])
                                    else:
                                        ultimos_mensajes = list(conversacion.mensajes.order_by('fecha_envio'))
                                    
                                    # Generar respuesta humana con contexto completo
                                    try:
                                        # Notificar que ISAC está escribiendo (en el panel administrativo)
                                        if channel_layer:
                                            try:
                                                async_to_sync(channel_layer.group_send)(
                                                    f'chat_{conversacion.id}',
                                                    {
                                                        'type': 'chat.typing',
                                                        'typing': True
                                                    }
                                                )
                                            except Exception as e:
                                                print(f"[WARNING] No se pudo enviar notificación de typing: {e}")
                                        
                                        # Enviar indicador de "escribiendo..." al cliente en WhatsApp
                                        try:
                                            from crm.whatsapp_service import send_whatsapp_typing_indicator
                                            send_whatsapp_typing_indicator(from_number, typing=True)
                                            print(f"[WEBHOOK] Indicador de 'escribiendo...' enviado a WhatsApp")
                                        except Exception as e:
                                            print(f"[WARNING] No se pudo enviar indicador de typing a WhatsApp: {e}")
                                        
                                        print(f"[WEBHOOK] Generando respuesta para mensaje: {msg_body_for_ia[:50]}...")
                                        respuesta_cliente, metadata = generar_respuesta_humana(
                                            mensaje_cliente=msg_body_for_ia,
                                            cliente=cliente,
                                            conversacion=conversacion,
                                            historial_mensajes=ultimos_mensajes
                                        )
                                        
                                        # Ocultar indicador de "escribiendo" cuando termine (en el panel administrativo)
                                        if channel_layer:
                                            try:
                                                async_to_sync(channel_layer.group_send)(
                                                    f'chat_{conversacion.id}',
                                                    {
                                                        'type': 'chat.typing',
                                                        'typing': False
                                                    }
                                                )
                                            except Exception as e:
                                                print(f"[WARNING] No se pudo enviar notificación de typing: {e}")
                                        
                                        # Ocultar indicador de "escribiendo..." en WhatsApp
                                        try:
                                            from crm.whatsapp_service import send_whatsapp_typing_indicator
                                            send_whatsapp_typing_indicator(from_number, typing=False)
                                            print(f"[WEBHOOK] Indicador de 'escribiendo...' ocultado en WhatsApp")
                                        except Exception as e:
                                            print(f"[WARNING] No se pudo ocultar indicador de typing en WhatsApp: {e}")
                                    
                                        print(f"[WEBHOOK] Respuesta generada: {respuesta_cliente[:100] if respuesta_cliente else 'VACÍA'}...")
                                        
                                        if respuesta_cliente and respuesta_cliente.strip():
                                            # Obtener productos mencionados para enviar imágenes y botones
                                            productos_mencionados = metadata.get('productos_mencionados', [])
                                            productos_info = metadata.get('productos_info', [])
                                            
                                            # Enviamos la respuesta de la IA por WhatsApp
                                            try:
                                                print(f"[WEBHOOK] Enviando respuesta por WhatsApp a {from_number}...")
                                                send_whatsapp_message(from_number, respuesta_cliente)
                                                print(f"[WEBHOOK] Respuesta enviada exitosamente")
                                            except RuntimeError as e:
                                                # Si el error es por token expirado, loguear pero continuar
                                                if "401" in str(e) or "expirado" in str(e).lower() or "expired" in str(e).lower():
                                                    print(f"[WEBHOOK WARNING] Token de WhatsApp expirado. El mensaje se guardó en la DB pero no se pudo enviar por WhatsApp.")
                                                    print(f"[WEBHOOK WARNING] Necesitás renovar el token en Meta for Developers.")
                                                    # Continuar para guardar el mensaje en la DB y notificar al frontend
                                                else:
                                                    raise  # Re-lanzar otros errores
                                            
                                            # Si hay productos mencionados, enviar imágenes y botones (solo si el mensaje se envió exitosamente)
                                            if productos_info and len(productos_info) > 0:
                                                from crm.services.ai_crm_service import obtener_imagen_producto_url, generar_botones_producto, obtener_configuracion_sistema
                                                from crm.whatsapp_service import send_whatsapp_image, send_whatsapp_buttons
                                                from inventario.models import ProductoVariante
                                                
                                                config_sistema = obtener_configuracion_sistema()
                                                
                                                # Enviar imagen del primer producto mencionado
                                                primer_producto = productos_info[0]
                                                try:
                                                    variante = ProductoVariante.objects.get(sku=primer_producto.get('sku'))
                                                    imagen_url = obtener_imagen_producto_url(variante, request)
                                                    
                                                    if imagen_url:
                                                        print(f"[WEBHOOK] Enviando imagen del producto {primer_producto.get('nombre')}...")
                                                        try:
                                                            send_whatsapp_image(
                                                                to_number=from_number,
                                                                image_url=imagen_url,
                                                                caption=f"{primer_producto.get('nombre', 'Producto')} - Stock: {primer_producto.get('stock', 0)}"
                                                            )
                                                            print(f"[WEBHOOK] Imagen enviada exitosamente")
                                                        except Exception as e:
                                                            print(f"[WEBHOOK WARNING] No se pudo enviar imagen: {e}")
                                                except ProductoVariante.DoesNotExist:
                                                    print(f"[WEBHOOK WARNING] Variante no encontrada para SKU: {primer_producto.get('sku')}")
                                                except Exception as e:
                                                    print(f"[WEBHOOK WARNING] Error obteniendo imagen: {e}")
                                                
                                                # Enviar botones interactivos
                                                try:
                                                    botones = generar_botones_producto(primer_producto, config_sistema)
                                                    if botones:
                                                        print(f"[WEBHOOK] Enviando mensaje con {len(botones)} botones...")
                                                        mensaje_botones = f"¿Qué te gustaría hacer con {primer_producto.get('nombre', 'este producto')}?"
                                                        send_whatsapp_buttons(
                                                            to_number=from_number,
                                                            message_text=mensaje_botones,
                                                            buttons=botones
                                                        )
                                                        print(f"[WEBHOOK] Botones enviados exitosamente")
                                                except Exception as e:
                                                    print(f"[WEBHOOK WARNING] No se pudieron enviar botones: {e}")
                                            
                                            # Guardamos la respuesta de la IA en nuestra base de datos con metadata
                                            mensaje_ia = Mensaje.objects.create(
                                                conversacion=conversacion,
                                                emisor='Sistema',
                                                contenido=respuesta_cliente,
                                                enviado_por_ia=True,
                                                tipo_mensaje='texto',
                                                metadata=metadata
                                            )
                                            print(f"[WEBHOOK] Mensaje de IA guardado en DB con ID: {mensaje_ia.id}")
                                            
                                            # Notificamos al frontend sobre la respuesta de la IA
                                            if channel_layer:
                                                try:
                                                    async_to_sync(channel_layer.group_send)(
                                                        f'chat_{conversacion.id}',
                                                        {
                                                            'type': 'chat.message',
                                                            'message': {
                                                                'emisor': mensaje_ia.emisor,
                                                                'contenido': mensaje_ia.contenido,
                                                                'tipo_mensaje': mensaje_ia.tipo_mensaje,
                                                                'fecha_envio': mensaje_ia.fecha_envio.strftime('%d de %b, %H:%M'),
                                                                'enviado_por_ia': True
                                                            }
                                                        }
                                                    )
                                                    print(f"[WEBHOOK] Notificación WebSocket enviada para respuesta de IA")
                                                except Exception as e:
                                                    print(f"[WARNING] No se pudo enviar notificación WebSocket: {e}")
                                                    import traceback
                                                    traceback.print_exc()
                                        else:
                                            print(f"[WEBHOOK WARNING] La respuesta de la IA está vacía o es None")
                                            # Enviar respuesta de fallback
                                            respuesta_fallback = "¡Hola! Gracias por tu mensaje. Estoy procesando tu consulta, por favor esperá un momento."
                                            try:
                                                send_whatsapp_message(from_number, respuesta_fallback)
                                                Mensaje.objects.create(
                                                    conversacion=conversacion,
                                                    emisor='Sistema',
                                                    contenido=respuesta_fallback,
                                                    enviado_por_ia=True,
                                                    tipo_mensaje='texto'
                                                )
                                            except Exception as e:
                                                print(f"[WEBHOOK ERROR] Error enviando respuesta de fallback: {e}")
                                    
                                    except Exception as e:
                                        print(f"[WEBHOOK ERROR] Error generando respuesta: {e}")
                                        import traceback
                                        traceback.print_exc()
                                        # Enviar respuesta de error al cliente
                                        try:
                                            respuesta_error = "Disculpá, tuve un problema procesando tu mensaje. Por favor intentá nuevamente en un momento."
                                            send_whatsapp_message(from_number, respuesta_error)
                                            Mensaje.objects.create(
                                                conversacion=conversacion,
                                                emisor='Sistema',
                                                contenido=respuesta_error,
                                                enviado_por_ia=False,
                                                tipo_mensaje='texto'
                                            )
                                        except Exception as e2:
                                            print(f"[WEBHOOK ERROR] Error enviando mensaje de error: {e2}")
                                        
                                        # Actualizar prioridad y estado según metadata (solo si hay metadata)
                                        if 'metadata' in locals() and metadata and metadata.get('requiere_asesor'):
                                            conversacion.prioridad = 'high'
                                            conversacion.estado = 'Pendiente'
                                            conversacion.save()

            return HttpResponse(status=200)
        except Exception as e:
            print(f"Error procesando el webhook: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=405)

@login_required
@csrf_exempt
def resumir_chat_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            
            if not conv_id:
                return JsonResponse({'error': 'No se proporcionó conversacion_id'}, status=400)
            
            conversacion = Conversacion.objects.get(id=conv_id)
            cliente = conversacion.cliente
            historial_mensajes = list(conversacion.mensajes.order_by('fecha_envio'))
            
            from crm.services.ai_crm_service import generar_resumen_cliente_ia
            resumen_data = generar_resumen_cliente_ia(cliente, conversacion, historial_mensajes)
            
            # Actualizar el resumen en la conversación
            if resumen_data.get('resumen_conversacion'):
                conversacion.resumen = resumen_data['resumen_conversacion']
                conversacion.save()

            return JsonResponse(resumen_data)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error resumiendo chat: {e}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
@csrf_exempt
def sugerir_respuesta_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conv_id = data.get('conversacion_id')
            
            if not conv_id:
                return JsonResponse({'error': 'No se proporcionó conversacion_id'}, status=400)
            
            conversacion = Conversacion.objects.get(id=conv_id)
            cliente = conversacion.cliente
            historial_mensajes = list(conversacion.mensajes.order_by('fecha_envio'))
            
            if not historial_mensajes:
                return JsonResponse({'error': 'No hay mensajes en la conversación'}, status=400)
            
            # Obtener último mensaje del cliente
            ultimo_mensaje_cliente = None
            for msg in reversed(historial_mensajes):
                if msg.emisor == 'Cliente':
                    ultimo_mensaje_cliente = msg.contenido
                    break
            
            if not ultimo_mensaje_cliente:
                return JsonResponse({'error': 'No hay mensajes del cliente'}, status=400)
            
            # Generar sugerencia usando el servicio de IA
            from crm.services.ai_crm_service import generar_respuesta_humana
            sugerencia, metadata = generar_respuesta_humana(
                mensaje_cliente=ultimo_mensaje_cliente,
                cliente=cliente,
                conversacion=conversacion,
                historial_mensajes=historial_mensajes
            )

            return JsonResponse({'sugerencia': sugerencia, 'metadata': metadata})
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error sugiriendo respuesta: {e}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
@csrf_exempt
def buscar_productos_api(request):
    """API para buscar productos desde el panel de chat"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Solo GET'}, status=405)
    
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'productos': []})
    
    # Buscar productos
    productos = ProductoVariante.objects.filter(
        Q(producto__nombre__icontains=query) |
        Q(sku__icontains=query) |
        Q(atributo_1__icontains=query) |
        Q(atributo_2__icontains=query) |
        Q(producto__categoria__nombre__icontains=query),
        producto__activo=True,
        activo=True
    ).select_related('producto', 'producto__categoria')[:10]
    
    resultados = []
    for variante in productos:
        # Obtener precios
        precio_minorista = Precio.objects.filter(
            variante=variante,
            tipo=Precio.Tipo.MINORISTA,
            moneda=Precio.Moneda.ARS,
            activo=True
        ).first()
        
        precio_mayorista = Precio.objects.filter(
            variante=variante,
            tipo=Precio.Tipo.MAYORISTA,
            moneda=Precio.Moneda.ARS,
            activo=True
        ).first()
        
        resultados.append({
            'id': variante.id,
            'sku': variante.sku,
            'nombre': variante.producto.nombre,
            'atributo_1': variante.atributo_1 or '',
            'atributo_2': variante.atributo_2 or '',
            'categoria': variante.producto.categoria.nombre if variante.producto.categoria else '',
            'stock': variante.stock_actual,
            'precio_minorista': float(precio_minorista.precio) if precio_minorista else None,
            'precio_mayorista': float(precio_mayorista.precio) if precio_mayorista else None,
        })
    
    return JsonResponse({'productos': resultados})


@login_required
@csrf_exempt
def enviar_producto_chat(request):
    """Envía información de un producto al chat"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo POST'}, status=405)
    
    try:
        data = json.loads(request.body)
        conv_id = data.get('conversacion_id')
        variante_id = data.get('variante_id')
        
        if not conv_id or not variante_id:
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)
        
        conversacion = Conversacion.objects.get(id=conv_id)
        variante = ProductoVariante.objects.get(id=variante_id)
        
        # Obtener precios
        precio_minorista = Precio.objects.filter(
            variante=variante,
            tipo=Precio.Tipo.MINORISTA,
            moneda=Precio.Moneda.ARS,
            activo=True
        ).first()
        
        precio_mayorista = Precio.objects.filter(
            variante=variante,
            tipo=Precio.Tipo.MAYORISTA,
            moneda=Precio.Moneda.ARS,
            activo=True
        ).first()
        
        # Determinar qué precio mostrar según tipo de cliente
        tipo_cliente = conversacion.cliente.tipo_cliente
        precio_mostrar = precio_mayorista if tipo_cliente == 'Mayorista' else precio_minorista
        
        # Construir mensaje
        atributos = []
        if variante.atributo_1:
            atributos.append(variante.atributo_1)
        if variante.atributo_2:
            atributos.append(variante.atributo_2)
        atributos_str = f" ({', '.join(atributos)})" if atributos else ""
        
        mensaje = f"*{variante.producto.nombre}{atributos_str}*\n\n"
        mensaje += f"SKU: {variante.sku}\n"
        mensaje += f"Stock disponible: {variante.stock_actual} unidades\n"
        
        if precio_mostrar:
            mensaje += f"Precio: ${precio_mostrar.precio:,.2f} ARS\n"
        else:
            mensaje += "Precio: Consultar\n"
        
        if variante.producto.categoria:
            mensaje += f"Categoría: {variante.producto.categoria.nombre}\n"
        
        mensaje += "\n¿Te interesa? Podemos crear una cotización para vos."
        
        # Enviar mensaje
        send_whatsapp_message(conversacion.cliente.telefono, mensaje)
        
        # Guardar en la conversación
        Mensaje.objects.create(
            conversacion=conversacion,
            emisor='Sistema',
            contenido=mensaje,
            enviado_por_ia=False,
            tipo_mensaje='texto',
            metadata={'tipo': 'producto_enviado', 'variante_id': variante_id}
        )
        
        # Notificar WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{conv_id}',
            {
                'type': 'chat.message',
                'message': {
                    'emisor': 'Sistema',
                    'contenido': mensaje,
                    'fecha_envio': timezone.now().strftime('%d de %b, %H:%M'),
                    'tipo_mensaje': 'texto',
                }
            }
        )
        
        return JsonResponse({'status': 'ok', 'mensaje': mensaje})
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error enviando producto al chat: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
def crear_cotizacion_api(request):
    """Crea una cotización desde el chat"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo POST'}, status=405)
    
    try:
        data = json.loads(request.body)
        conv_id = data.get('conversacion_id')
        productos = data.get('productos', [])  # Lista de {variante_id, cantidad}
        dias_validez = data.get('dias_validez', 7)
        
        if not conv_id or not productos:
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)
        
        conversacion = Conversacion.objects.get(id=conv_id)
        cliente = conversacion.cliente
        
        # Determinar tipo de precio según cliente
        tipo_precio = Precio.Tipo.MAYORISTA if cliente.tipo_cliente == 'Mayorista' else Precio.Tipo.MINORISTA
        
        productos_cotizacion = []
        total = Decimal('0')
        
        for item in productos:
            variante_id = item.get('variante_id')
            cantidad = int(item.get('cantidad', 1))
            
            if not variante_id:
                continue
            
            variante = ProductoVariante.objects.get(id=variante_id)
            precio_obj = Precio.objects.filter(
                variante=variante,
                tipo=tipo_precio,
                moneda=Precio.Moneda.ARS,
                activo=True
            ).first()
            
            if not precio_obj:
                continue
            
            precio_unitario = precio_obj.precio
            subtotal = precio_unitario * cantidad
            
            atributos = []
            if variante.atributo_1:
                atributos.append(variante.atributo_1)
            if variante.atributo_2:
                atributos.append(variante.atributo_2)
            nombre_completo = f"{variante.producto.nombre}"
            if atributos:
                nombre_completo += f" ({', '.join(atributos)})"
            
            productos_cotizacion.append({
                'sku': variante.sku,
                'nombre': nombre_completo,
                'cantidad': cantidad,
                'precio': float(precio_unitario),
                'subtotal': float(subtotal),
            })
            
            total += subtotal
        
        if not productos_cotizacion:
            return JsonResponse({'error': 'No se pudo crear la cotización'}, status=400)
        
        # Crear cotización
        valido_hasta = timezone.now() + timedelta(days=dias_validez)
        cotizacion = Cotizacion.objects.create(
            conversacion=conversacion,
            cliente=cliente,
            productos=productos_cotizacion,
            total=total,
            valido_hasta=valido_hasta,
            estado='Pendiente'
        )
        
        # Construir mensaje de cotización
        mensaje = f"📋 *Cotización #{cotizacion.id}*\n\n"
        mensaje += f"Cliente: {cliente.nombre}\n"
        mensaje += f"Válida hasta: {valido_hasta.strftime('%d/%m/%Y')}\n\n"
        mensaje += "*Productos:*\n"
        
        for prod in productos_cotizacion:
            mensaje += f"• {prod['nombre']}\n"
            mensaje += f"  Cantidad: {prod['cantidad']} x ${prod['precio']:,.2f} = ${prod['subtotal']:,.2f}\n\n"
        
        mensaje += f"*Total: ${total:,.2f} ARS*\n\n"
        mensaje += "¿Te interesa? Podemos proceder con la compra."
        
        # Enviar mensaje
        send_whatsapp_message(cliente.telefono, mensaje)
        
        # Guardar en la conversación
        Mensaje.objects.create(
            conversacion=conversacion,
            emisor='Sistema',
            contenido=mensaje,
            enviado_por_ia=False,
            tipo_mensaje='texto',
            metadata={'tipo': 'cotizacion_creada', 'cotizacion_id': cotizacion.id}
        )
        
        # Notificar WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{conv_id}',
            {
                'type': 'chat.message',
                'message': {
                    'emisor': 'Sistema',
                    'contenido': mensaje,
                    'fecha_envio': timezone.now().strftime('%d de %b, %H:%M'),
                    'tipo_mensaje': 'texto',
                }
            }
        )
        
        return JsonResponse({
            'status': 'ok',
            'cotizacion_id': cotizacion.id,
            'total': float(total),
            'mensaje': mensaje
        })
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error creando cotización: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
def reiniciar_conversacion_api(request, conv_id):
    """
    Reinicia una conversación borrando todos los mensajes y el contexto del cliente.
    Útil para pruebas.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo POST'}, status=405)
    
    try:
        conversacion = Conversacion.objects.get(id=conv_id)
        cliente = conversacion.cliente
        
        # Borrar todos los mensajes de la conversación
        mensajes_borrados = conversacion.mensajes.all().delete()
        print(f"[REINICIAR] Borrados {mensajes_borrados[0]} mensajes de la conversación {conv_id}")
        
        # Borrar el contexto persistente del cliente
        ClienteContexto.objects.filter(cliente=cliente).delete()
        print(f"[REINICIAR] Borrado contexto del cliente {cliente.telefono}")
        
        # Limpiar el resumen de la conversación (usar cadena vacía en lugar de None)
        conversacion.resumen = ""
        conversacion.save()
        
        # Notificar al frontend vía WebSocket
        try:
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f'chat_{conversacion.id}',
                    {
                        'type': 'chat.reload',
                        'message': 'Conversación reiniciada'
                    }
                )
        except Exception as e:
            print(f"[WARNING] No se pudo enviar notificación WebSocket: {e}")
        
        return JsonResponse({
            'success': True,
            'message': 'Conversación reiniciada exitosamente',
            'mensajes_borrados': mensajes_borrados[0]
        })
        
    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversación no encontrada'}, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error reiniciando conversación: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def obtener_contexto_cliente_api(request, conv_id):
    """Obtiene el contexto completo del cliente para mostrar en el panel, incluyendo análisis de IA"""
    try:
        conversacion = Conversacion.objects.get(id=conv_id)
        cliente = conversacion.cliente
        historial_mensajes = list(conversacion.mensajes.order_by('fecha_envio'))
        
        # Obtener contexto persistente
        try:
            contexto_obj = ClienteContexto.objects.get(cliente=cliente)
            contexto_persistente = {
                'productos_interes': contexto_obj.productos_interes,
                'categorias_preferidas': contexto_obj.categorias_preferidas,
                'tipo_consulta_comun': contexto_obj.tipo_consulta_comun,
                'total_interacciones': contexto_obj.total_interacciones,
                'tags_comportamiento': contexto_obj.tags_comportamiento,
            }
        except ClienteContexto.DoesNotExist:
            contexto_persistente = {}
        
        # Obtener compras anteriores
        compras = []
        try:
            ventas = Venta.objects.filter(
                cliente_nombre__icontains=cliente.nombre
            ).order_by('-fecha')[:5]
            
            for venta in ventas:
                compras.append({
                    'id': venta.id,
                    'fecha': venta.fecha.strftime('%d/%m/%Y'),
                    'total': float(venta.total_ars),
                    'status': venta.status,
                })
        except:
            pass
        
        # Obtener cotizaciones activas
        cotizaciones = []
        try:
            cotizaciones_activas = Cotizacion.objects.filter(
                cliente=cliente,
                estado__in=['Pendiente', 'Enviada']
            ).order_by('-creado')[:5]
            
            for cot in cotizaciones_activas:
                cotizaciones.append({
                    'id': cot.id,
                    'total': float(cot.total),
                    'estado': cot.estado,
                    'creado': cot.creado.strftime('%d/%m/%Y'),
                })
        except:
            pass
        
        # Generar análisis de IA (resumen, intención de compra, sugerencias)
        analisis_ia = {}
        if historial_mensajes:
            try:
                from crm.services.ai_crm_service import (
                    generar_resumen_cliente_ia,
                    analizar_intencion_compra
                )
                
                # Resumen del cliente
                resumen_data = generar_resumen_cliente_ia(cliente, conversacion, historial_mensajes)
                
                # Análisis de intención de compra
                intencion_data = analizar_intencion_compra(cliente, conversacion, historial_mensajes)
                
                analisis_ia = {
                    'resumen': resumen_data,
                    'intencion_compra': intencion_data,
                }
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error generando análisis de IA: {e}", exc_info=True)
        
        return JsonResponse({
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'telefono': cliente.telefono,
                'email': cliente.email or '',
                'tipo': cliente.get_tipo_cliente_display(),
                'inicial': cliente.nombre[0].upper() if cliente.nombre else '?',
            },
            'compras_anteriores': compras,
            'cotizaciones_activas': cotizaciones,
            'contexto_persistente': contexto_persistente,
            'analisis_ia': analisis_ia,
        })
    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversación no encontrada'}, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error obteniendo contexto del cliente: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
