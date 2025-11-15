import json
from random import sample

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal

from . import interpreter
from core.db_inspector import table_exists
from .models import AssistantKnowledgeArticle, AssistantPlaybook, AssistantQuickReply, ConversationThread, ConversationMessage
from .product_matcher import extract_product_info_from_text, find_similar_products, format_similar_products_for_question
from inventario.models import ProductoVariante, Precio, Producto, Categoria
from historial.models import RegistroHistorial
from django.utils.text import slugify
from django.db import connection
from core.db_inspector import column_exists
from django.utils import timezone

@login_required
def chat_view(request):
    """Renderiza la experiencia completa del asistente."""

    quick_replies = AssistantQuickReply.objects.none()
    knowledge = AssistantKnowledgeArticle.objects.none()
    playbooks = AssistantPlaybook.objects.none()
    threads = ConversationThread.objects.none()
    missing_entities: list[str] = []

    if table_exists("asistente_ia_assistantquickreply"):
        quick_replies = (
            AssistantQuickReply.objects.filter(activo=True)
            .order_by("categoria", "orden", "titulo")
        )
    else:
        missing_entities.append("respuestas rápidas")

    if table_exists("asistente_ia_assistantknowledgearticle"):
        knowledge = AssistantKnowledgeArticle.objects.all()[:6]
    else:
        missing_entities.append("base de conocimiento")

    if table_exists("asistente_ia_assistantplaybook"):
        playbooks = AssistantPlaybook.objects.filter(es_template=True)[:6]
    else:
        missing_entities.append("playbooks")

    # Obtener threads del usuario
    if table_exists("asistente_ia_conversationthread"):
        threads = ConversationThread.objects.filter(
            usuario=request.user,
            activo=True
        ).order_by('-actualizado')[:20]

    if missing_entities:
        messages.info(
            request,
            f"Algunas funcionalidades no están disponibles: {', '.join(missing_entities)}. "
            "Ejecutá 'python manage.py create_sample_data' para crearlas."
        )

    context = {
        "quick_replies": quick_replies,
        "knowledge": knowledge,
        "playbooks": playbooks,
        "threads": threads,
    }

    # Obtener thread activo si hay thread_id en GET
    active_thread_id = request.GET.get("thread_id")
    active_thread = None
    messages_list_json = []
    
    if active_thread_id and table_exists("asistente_ia_conversationthread"):
        try:
            active_thread = ConversationThread.objects.get(
                id=active_thread_id,
                usuario=request.user,
                activo=True
            )
            # Obtener mensajes del thread
            if table_exists("asistente_ia_conversationmessage"):
                messages_list = active_thread.mensajes.all().order_by('creado')
                messages_list_json = [
                    {"role": msg.rol, "content": msg.contenido}
                    for msg in messages_list
                ]
        except ConversationThread.DoesNotExist:
            pass
    
    context["active_thread"] = active_thread
    context["messages_list_json"] = json.dumps(messages_list_json)

    return render(request, "asistente_ia/chat.html", context)

@login_required
def ask_question(request):
    """
    Recibe una pregunta, la pasa al intérprete para consultar la BD,
    y devuelve una respuesta final generada por la IA.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get("question", "").strip()
            quick_reply_id = data.get("quick_reply_id")
            extra_context = data.get("context", [])
            images_base64 = data.get("images", [])  # Imágenes en base64

            if not user_question and not images_base64:
                return JsonResponse({"error": "No se recibió ninguna pregunta ni imagen."}, status=400)

            # Obtener o crear thread
            thread_id = data.get("thread_id")
            thread = None
            
            if thread_id and table_exists("asistente_ia_conversationthread"):
                try:
                    thread = ConversationThread.objects.get(
                        id=thread_id,
                        usuario=request.user
                    )
                except ConversationThread.DoesNotExist:
                    pass
            
            if not thread and table_exists("asistente_ia_conversationthread"):
                # Crear nuevo thread con título basado en la primera pregunta
                titulo = (user_question[:50] + "..." if len(user_question) > 50 else user_question) or "Nueva conversación"
                thread = ConversationThread.objects.create(
                    usuario=request.user,
                    titulo=titulo
                )

            # Obtener historial del thread o usar sesión como fallback
            if thread and table_exists("asistente_ia_conversationmessage"):
                # Obtener los últimos 10 mensajes (no usar indexación negativa en queryset)
                total_messages = thread.mensajes.count()
                if total_messages > 10:
                    history_messages = list(thread.mensajes.all().order_by('creado')[total_messages-10:])
                else:
                    history_messages = list(thread.mensajes.all().order_by('creado'))
                history = [
                    {"role": msg.rol, "content": msg.contenido}
                    for msg in history_messages
                ]
            else:
                # Fallback a sesión si no hay threads
                session_history = request.session.get("assistant_history", [])
                if len(session_history) > 6:
                    history = session_history[-6:]
                else:
                    history = session_history
            
            if extra_context:
                for snippet in extra_context:
                    history.append({"role": "system", "content": str(snippet)[:400]})

            if user_question:
                history.append({"role": "user", "content": user_question})
                
                # Guardar mensaje del usuario en el thread
                if thread and table_exists("asistente_ia_conversationmessage"):
                    ConversationMessage.objects.create(
                        thread=thread,
                        rol='user',
                        contenido=user_question
                    )

            # Procesar imágenes si hay
            if images_base64:
                processed_text = interpreter.process_images_with_vision(images_base64, user_question)
                if processed_text:
                    user_question = f"{user_question}\n\n[Contenido extraído de imágenes/PDFs]:\n{processed_text}"

            # 1. Pregunta -> JSON de Consulta
            query_json = interpreter.generate_query_json_from_question(
                user_question,
                chat_history="\n".join(item["content"] for item in history if item["role"] == "user"),
            )

            if not query_json:
                # Si la IA no pudo generar un JSON, le pedimos que explique por qué.
                final_answer = interpreter.generate_final_response(
                    user_question,
                    "No se pudo generar una consulta válida para esta pregunta.",
                )
                return JsonResponse({"answer": final_answer, "history": history, "thread_id": thread.id if thread else None})

            # Verificar si hay productos pendientes y el usuario está respondiendo con un precio
            if 'productos_pendientes_proveedor' in request.session:
                import re
                # Buscar todos los números en la respuesta
                # El último número grande (>= 10) generalmente es el precio
                numeros = re.findall(r'(\d+(?:[.,]\d+)?)', user_question.replace(',', '.'))
                if numeros:
                    # Convertir a float y tomar el más grande (probablemente el precio)
                    precios_candidatos = [float(n) for n in numeros if float(n) >= 10]
                    if precios_candidatos:
                        precio = max(precios_candidatos)  # Tomar el más grande como precio
                        indice = request.session.get('indice_producto_actual', 0)
                        productos_pendientes = request.session.get('productos_pendientes_proveedor', [])
                        
                        if indice < len(productos_pendientes):
                            # Procesar el producto con el precio
                            return _procesar_producto_con_precio(request, thread, history, productos_pendientes, indice, precio, user_question)
            
            # Manejar procesamiento de listados de proveedores
            if query_json.get("action") == "procesar_listado_proveedor":
                return _procesar_listado_proveedor(request, query_json, user_question, thread, history)

            # 2. Ejecutar la consulta desde el JSON para obtener datos
            query_results = interpreter.run_query_from_json(query_json)

            # 3. Recopilar recursos disponibles para el contexto
            available_resources = {}
            if table_exists("asistente_ia_assistantplaybook"):
                playbooks = AssistantPlaybook.objects.filter(es_template=True)[:5]
                available_resources["playbooks"] = [{"titulo": p.titulo} for p in playbooks]
            if table_exists("asistente_ia_assistantknowledgearticle"):
                knowledge = AssistantKnowledgeArticle.objects.all()[:5]
                available_resources["knowledge"] = [{"titulo": k.titulo} for k in knowledge]
            if table_exists("asistente_ia_assistantquickreply"):
                quick_replies_count = AssistantQuickReply.objects.filter(activo=True).count()
                available_resources["quick_replies"] = quick_replies_count

            # 4. Datos -> Respuesta Final en lenguaje natural
            # Obtener últimos 6 mensajes del historial para el contexto
            if len(history) > 6:
                recent_history = history[-6:]
            else:
                recent_history = history
            
            final_answer = interpreter.generate_final_response(
                user_question,
                query_results,
                user_name=request.user.first_name or request.user.username,
                chat_history="\n".join(item["content"] for item in recent_history),
                available_resources=available_resources,
            )

            history.append({"role": "assistant", "content": final_answer})
            
            # Guardar respuesta del asistente en el thread
            if thread and table_exists("asistente_ia_conversationmessage"):
                ConversationMessage.objects.create(
                    thread=thread,
                    rol='assistant',
                    contenido=final_answer
                )
                # Actualizar título del thread si es el primer mensaje
                if thread.mensajes.count() == 2:  # user + assistant
                    titulo = user_question[:50] + "..." if len(user_question) > 50 else user_question
                    thread.titulo = titulo
                    thread.save()
            
            return JsonResponse({
                "answer": final_answer,
                "history": history,
                "thread_id": thread.id if thread else None
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Payload inválido"}, status=400)
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en la vista ask_question: {e}\n{traceback.format_exc()}")
            return JsonResponse({"error": f"Error en la vista ask_question: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


def _procesar_listado_proveedor(request, query_json, user_question, thread, history):
    """
    Procesa un listado de productos del proveedor automáticamente, uno por uno.
    Para cada producto, pregunta el precio de venta y luego lo procesa.
    """
    texto = query_json.get("texto", user_question)
    
    # Extraer información de productos del texto
    productos_extraidos = extract_product_info_from_text(texto)
    
    if not productos_extraidos:
        respuesta = "No pude identificar productos en el listado. Por favor, asegurate de incluir el nombre del producto, cantidad y costo. Ejemplo: 'cargador xiaomi 20w x3 5000'"
        
        if thread and table_exists("asistente_ia_conversationmessage"):
            ConversationMessage.objects.create(
                thread=thread,
                rol='assistant',
                contenido=respuesta
            )
        
        return JsonResponse({
            "answer": respuesta,
            "history": history + [{"role": "assistant", "content": respuesta}],
            "thread_id": thread.id if thread else None
        })
    
    # Guardar productos pendientes en la sesión para procesarlos uno por uno
    productos_pendientes = []
    
    for producto_info in productos_extraidos:
        nombre = producto_info.get('nombre', '')
        cantidad = producto_info.get('cantidad', 1)
        costo = producto_info.get('costo')
        
        # Buscar productos similares
        similares = find_similar_products(nombre, threshold=0.3)
        
        # Preparar información del producto para procesar
        producto_data = {
            'nombre': nombre,
            'cantidad': cantidad,
            'costo': float(costo) if costo else None,
            'similares': [{'id': s[0].id, 'nombre': s[0].producto.nombre, 'sku': s[0].sku, 'score': s[1]} for s in similares[:3]] if similares else []
        }
        productos_pendientes.append(producto_data)
    
    # Guardar en la sesión
    request.session['productos_pendientes_proveedor'] = productos_pendientes
    request.session['indice_producto_actual'] = 0
    
    # Procesar el primer producto
    return _preguntar_precio_producto(request, thread, history, productos_pendientes, 0)


def _preguntar_precio_producto(request, thread, history, productos_pendientes, indice):
    """
    Pregunta el precio de venta para un producto específico.
    """
    if indice >= len(productos_pendientes):
        # Ya se procesaron todos los productos
        respuesta = f"✅ **Procesamiento completado**\n\nHe procesado todos los productos del listado. Total: {len(productos_pendientes)} productos."
        
        # Limpiar sesión
        if 'productos_pendientes_proveedor' in request.session:
            del request.session['productos_pendientes_proveedor']
        if 'indice_producto_actual' in request.session:
            del request.session['indice_producto_actual']
        
        if thread and table_exists("asistente_ia_conversationmessage"):
            ConversationMessage.objects.create(
                thread=thread,
                rol='assistant',
                contenido=respuesta
            )
        
        return JsonResponse({
            "answer": respuesta,
            "history": history + [{"role": "assistant", "content": respuesta}],
            "thread_id": thread.id if thread else None
        })
    
    producto_actual = productos_pendientes[indice]
    nombre = producto_actual['nombre']
    cantidad = producto_actual['cantidad']
    costo = producto_actual['costo']
    similares = producto_actual.get('similares', [])
    
    # Construir mensaje para preguntar precio
    respuesta = f"**Producto {indice + 1} de {len(productos_pendientes)}**\n\n"
    respuesta += f"📦 **{nombre}**\n"
    respuesta += f"   Cantidad: {cantidad} unidades\n"
    if costo:
        respuesta += f"   Costo unitario: ${costo:.2f}\n"
    
    if similares:
        respuesta += f"\n🔍 **Productos similares encontrados:**\n"
        for idx, similar in enumerate(similares, 1):
            respuesta += f"   {idx}. {similar['nombre']} (SKU: {similar['sku']}) - Similitud: {similar['score']:.0%}\n"
        respuesta += f"\n💡 Si querés agregar stock a uno de estos productos, respondé con el número. Si querés crear uno nuevo, respondé 'nuevo'.\n"
    else:
        respuesta += f"\n⚠️ No encontré productos similares en el inventario. Se creará un producto nuevo.\n"
    
    respuesta += f"\n💰 **¿Cuál es el precio de venta minorista en ARS para este producto?**\n"
    respuesta += f"   (Respondé solo con el número, ej: 1500 o 2500.50)"
    
    if thread and table_exists("asistente_ia_conversationmessage"):
        ConversationMessage.objects.create(
            thread=thread,
            rol='assistant',
            contenido=respuesta
        )
    
    return JsonResponse({
        "answer": respuesta,
        "history": history + [{"role": "assistant", "content": respuesta}],
        "thread_id": thread.id if thread else None,
        "waiting_for_price": True,
        "product_index": indice
    })


def _procesar_producto_con_precio(request, thread, history, productos_pendientes, indice, precio_venta, user_response):
    """
    Procesa un producto con el precio de venta proporcionado.
    Puede agregar stock a un producto existente o crear uno nuevo.
    """
    producto_actual = productos_pendientes[indice]
    nombre = producto_actual['nombre']
    cantidad = producto_actual['cantidad']
    costo = producto_actual.get('costo')
    similares = producto_actual.get('similares', [])
    
    # Verificar si el usuario quiere usar un producto similar
    import re
    numero_match = re.search(r'\b(\d+)\b', user_response)
    variante_seleccionada = None
    
    if numero_match and similares:
        numero = int(numero_match.group(1))
        if 1 <= numero <= len(similares):
            variante_id = similares[numero - 1]['id']
            try:
                variante_seleccionada = ProductoVariante.objects.get(pk=variante_id)
            except ProductoVariante.DoesNotExist:
                pass
    
    respuesta = ""
    variante_procesada = None
    
    try:
        with transaction.atomic():
            if variante_seleccionada:
                # Agregar stock a producto existente
                stock_anterior = variante_seleccionada.stock_actual or 0
                nuevo_stock = stock_anterior + cantidad
                variante_seleccionada.stock_actual = nuevo_stock
                variante_seleccionada.save()
                variante_procesada = variante_seleccionada
                
                # Actualizar precio si es necesario
                precio_obj, created = Precio.objects.get_or_create(
                    variante=variante_seleccionada,
                    tipo=Precio.Tipo.MINORISTA,
                    moneda=Precio.Moneda.ARS,
                    defaults={'precio': Decimal(str(precio_venta)), 'activo': True}
                )
                if not created:
                    precio_obj.precio = Decimal(str(precio_venta))
                    precio_obj.activo = True
                    precio_obj.save()
                
                # Registrar en historial
                RegistroHistorial.objects.create(
                    usuario=request.user,
                    tipo_accion=RegistroHistorial.TipoAccion.MODIFICACION,
                    descripcion=f"Stock agregado desde proveedor: {variante_seleccionada.producto.nombre} ({variante_seleccionada.sku}) - {stock_anterior} → {nuevo_stock} (+{cantidad})"
                )
                
                respuesta = f"✅ **Stock actualizado**\n\n"
                respuesta += f"📦 {variante_seleccionada.producto.nombre} (SKU: {variante_seleccionada.sku})\n"
                respuesta += f"   Stock: {stock_anterior} → {nuevo_stock} (+{cantidad})\n"
                respuesta += f"   Precio minorista: ${precio_venta:.2f} ARS\n"
            else:
                # Crear producto nuevo
                # Detectar categoría automáticamente
                categoria = _detectar_categoria(nombre)
                
                # Crear producto
                producto = Producto.objects.create(
                    nombre=nombre,
                    categoria=categoria,
                    activo=True
                )
                
                # Generar SKU único
                sku = _generar_sku_unico(nombre)
                
                # Crear variante
                ahora = timezone.now()
                columnas = ["producto_id", "sku", "stock_actual", "activo", "creado", "actualizado"]
                valores = [producto.pk, sku, cantidad, 1, ahora, ahora]
                
                # Verificar campos adicionales
                if column_exists("inventario_productovariante", "peso"):
                    columnas.append("peso")
                    valores.append(0)
                if column_exists("inventario_productovariante", "costo") and costo:
                    columnas.append("costo")
                    valores.append(Decimal(str(costo)))
                
                with connection.cursor() as cursor:
                    placeholders = ", ".join(["%s"] * len(valores))
                    cursor.execute(
                        f"INSERT INTO inventario_productovariante ({', '.join(columnas)}) VALUES ({placeholders})",
                        valores
                    )
                    variante_id = cursor.lastrowid
                
                variante_procesada = ProductoVariante.objects.get(pk=variante_id)
                
                # Crear precio
                Precio.objects.create(
                    variante=variante_procesada,
                    tipo=Precio.Tipo.MINORISTA,
                    moneda=Precio.Moneda.ARS,
                    precio=Decimal(str(precio_venta)),
                    activo=True
                )
                
                # Registrar en historial
                RegistroHistorial.objects.create(
                    usuario=request.user,
                    tipo_accion=RegistroHistorial.TipoAccion.CREACION,
                    descripcion=f"Producto creado desde proveedor: {nombre} (SKU: {sku}) - Stock inicial: {cantidad}"
                )
                
                respuesta = f"✅ **Producto creado**\n\n"
                respuesta += f"📦 {nombre}\n"
                respuesta += f"   SKU: {sku}\n"
                respuesta += f"   Categoría: {categoria.nombre if categoria else 'Sin categoría'}\n"
                respuesta += f"   Stock inicial: {cantidad}\n"
                respuesta += f"   Precio minorista: ${precio_venta:.2f} ARS\n"
                if costo:
                    respuesta += f"   Costo: ${costo:.2f}\n"
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error procesando producto: {e}", exc_info=True)
        respuesta = f"❌ **Error al procesar el producto**\n\n{str(e)}"
    
    # Guardar respuesta
    if thread and table_exists("asistente_ia_conversationmessage"):
        ConversationMessage.objects.create(
            thread=thread,
            rol='assistant',
            contenido=respuesta
        )
    
    # Avanzar al siguiente producto
    siguiente_indice = indice + 1
    request.session['indice_producto_actual'] = siguiente_indice
    
    # Preguntar por el siguiente producto
    return _preguntar_precio_producto(request, thread, history + [{"role": "assistant", "content": respuesta}], productos_pendientes, siguiente_indice)


def _detectar_categoria(nombre_producto):
    """
    Detecta la categoría del producto basándose en palabras clave en el nombre.
    """
    nombre_lower = nombre_producto.lower()
    
    # Mapeo de palabras clave a categorías
    categorias_keywords = {
        'celulares': ['iphone', 'celular', 'smartphone', 'telefono'],
        'accesorios': ['cargador', 'cable', 'auricular', 'headphone', 'case', 'funda', 'protector'],
        'electrónica': ['tv', 'televisor', 'monitor', 'tablet', 'ipad'],
        'relojes': ['reloj', 'watch', 'smartwatch'],
        'memoria': ['memoria', 'usb', 'pendrive', 'sd card', 'microsd'],
    }
    
    for categoria_nombre, keywords in categorias_keywords.items():
        if any(keyword in nombre_lower for keyword in keywords):
            try:
                return Categoria.objects.filter(nombre__icontains=categoria_nombre).first()
            except:
                pass
    
    # Categoría por defecto o "Otros"
    return Categoria.objects.filter(nombre__icontains='otros').first() or None


def _generar_sku_unico(nombre: str, attr1: str = "", attr2: str = "") -> str:
    """
    Genera un SKU único basado en el nombre del producto.
    """
    sku_base = slugify(nombre).upper()[:30]  # Limitar longitud
    if not sku_base:
        sku_base = "PROD"
    
    sku_final = sku_base
    contador = 1
    while ProductoVariante.objects.filter(sku=sku_final).exists():
        sku_final = f"{sku_base}-{contador}"
        contador += 1
        if contador > 1000:
            from uuid import uuid4
            sku_final = f"{sku_base}-{str(uuid4())[:8].upper()}"
            break
    
    return sku_final


@login_required
@require_POST
def aplicar_stock_proveedor(request):
    """
    Aplica stock y costo a un producto después de la confirmación del usuario.
    """
    try:
        data = json.loads(request.body)
        variante_id = data.get('variante_id')
        cantidad = data.get('cantidad', 0)
        costo = data.get('costo')
        
        if not variante_id or cantidad <= 0:
            return JsonResponse({"error": "variante_id y cantidad son requeridos"}, status=400)
        
        variante = ProductoVariante.objects.get(pk=variante_id)
        stock_anterior = variante.stock_actual or 0
        nuevo_stock = stock_anterior + cantidad
        
        with transaction.atomic():
            variante.stock_actual = nuevo_stock
            variante.save()
            
            # Si hay costo, actualizar (esto requeriría un campo costo en ProductoVariante o en otro modelo)
            # Por ahora solo actualizamos stock
            
            # Registrar en historial
            RegistroHistorial.objects.create(
                usuario=request.user,
                tipo_accion=RegistroHistorial.TipoAccion.MODIFICACION,
                descripcion=f"Stock agregado desde proveedor: {variante.producto.nombre} ({variante.sku}) - {stock_anterior} → {nuevo_stock} (+{cantidad})"
            )
        
        return JsonResponse({
            "success": True,
            "message": f"Stock actualizado: {variante.producto.nombre} - {stock_anterior} → {nuevo_stock} (+{cantidad})",
            "stock": nuevo_stock
        })
    except ProductoVariante.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en aplicar_stock_proveedor: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_GET
def list_threads(request):
    """Devuelve la lista de threads en formato JSON."""
    if table_exists("asistente_ia_conversationthread"):
        threads = ConversationThread.objects.filter(
            usuario=request.user,
            activo=True
        ).order_by('-actualizado')[:20]
        
        threads_data = [{
            'id': thread.id,
            'titulo': thread.titulo,
            'actualizado': thread.actualizado.isoformat(),
            'creado': thread.creado.isoformat()
        } for thread in threads]
        
        return JsonResponse({'threads': threads_data})
    return JsonResponse({'threads': []})


@login_required
@require_POST
@csrf_exempt
def create_thread(request):
    """Crea un nuevo thread de conversación."""
    try:
        data = json.loads(request.body)
        titulo = data.get('titulo', 'Nueva conversación')
        
        if table_exists("asistente_ia_conversationthread"):
            thread = ConversationThread.objects.create(
                usuario=request.user,
                titulo=titulo
            )
            return JsonResponse({
                'id': thread.id,
                'titulo': thread.titulo,
                'creado': thread.creado.isoformat()
            })
        return JsonResponse({'error': 'Threads no disponibles'}, status=400)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en create_thread: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
@csrf_exempt
def delete_thread(request, thread_id):
    """Elimina (desactiva) un thread de conversación."""
    try:
        if table_exists("asistente_ia_conversationthread"):
            thread = ConversationThread.objects.get(
                id=thread_id,
                usuario=request.user
            )
            thread.activo = False
            thread.save()
            return JsonResponse({"status": "ok"})
        return JsonResponse({'error': 'Threads no disponibles'}, status=400)
    except ConversationThread.DoesNotExist:
        return JsonResponse({"error": "Thread no encontrado"}, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en delete_thread: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_GET
def quick_replies_catalogue(request):
    """Devuelve el catálogo de respuestas rápidas en formato JSON."""
    if table_exists("asistente_ia_assistantquickreply"):
        quick_replies = AssistantQuickReply.objects.filter(activo=True).order_by("categoria", "orden", "titulo")
        # Agrupar por categoría
        replies_by_category = {}
        for reply in quick_replies:
            categoria = reply.categoria or "General"
            if categoria not in replies_by_category:
                replies_by_category[categoria] = []
            replies_by_category[categoria].append({
                'id': reply.id,
                'titulo': reply.titulo,
                'prompt': reply.prompt,
                'orden': reply.orden
            })
        return JsonResponse({'quick_replies': replies_by_category})
    return JsonResponse({'quick_replies': {}})


@login_required
@require_GET
def playbook_detail(request, pk):
    """Devuelve los detalles de un playbook en formato JSON."""
    try:
        if table_exists("asistente_ia_assistantplaybook"):
            playbook = AssistantPlaybook.objects.get(pk=pk, es_template=True)
            pasos_data = []
            if playbook.pasos:
                for paso in playbook.pasos:
                    pasos_data.append({
                        'titulo': paso.get('titulo', ''),
                        'descripcion': paso.get('descripcion', '')
                    })
            
            return JsonResponse({
                'id': playbook.id,
                'titulo': playbook.titulo,
                'descripcion': playbook.descripcion,
                'pasos': pasos_data
            })
        return JsonResponse({'error': 'Playbooks no disponibles'}, status=400)
    except AssistantPlaybook.DoesNotExist:
        return JsonResponse({'error': 'Playbook no encontrado'}, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en playbook_detail: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_GET
def thread_messages(request, thread_id):
    """Devuelve los mensajes de un thread en formato JSON."""
    try:
        if table_exists("asistente_ia_conversationthread") and table_exists("asistente_ia_conversationmessage"):
            thread = ConversationThread.objects.get(
                id=thread_id,
                usuario=request.user,
                activo=True
            )
            messages_list = thread.mensajes.all().order_by('creado')
            messages_data = [
                {
                    'role': msg.rol,
                    'content': msg.contenido
                }
                for msg in messages_list
            ]
            
            return JsonResponse({
                'thread_id': thread.id,
                'titulo': thread.titulo,
                'messages': messages_data
            })
        return JsonResponse({'error': 'Threads no disponibles'}, status=400)
    except ConversationThread.DoesNotExist:
        return JsonResponse({'error': 'Thread no encontrado'}, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en thread_messages: {e}")
        return JsonResponse({'error': str(e)}, status=500)
