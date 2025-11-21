"""
Vistas JWT para autenticación y registro
"""
import json
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import PerfilUsuario, DireccionEnvio, Favorito, SolicitudMayorista

User = get_user_model()
logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Genera tokens JWT para un usuario"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@csrf_exempt
@require_http_methods(["POST"])
@permission_classes([AllowAny])
def api_registro(request):
    """
    Registro de nuevos usuarios (SIEMPRE minorista)
    """
    try:
        data = json.loads(request.body)
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        password_confirm = data.get('password_confirm', '')
        tipo_usuario = 'MINORISTA'  # SIEMPRE minorista en registro normal
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        telefono = data.get('telefono', '').strip()
        dni = data.get('dni', '').strip()  # DNI obligatorio
        
        # Validaciones
        if not email:
            return JsonResponse({'error': 'El email es requerido'}, status=400)
        
        if not dni:
            return JsonResponse({'error': 'El DNI es obligatorio'}, status=400)
        
        if not password:
            return JsonResponse({'error': 'La contraseña es requerida'}, status=400)
        
        if password != password_confirm:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)
        
        # Validar contraseña
        try:
            validate_password(password)
        except ValidationError as e:
            return JsonResponse({'error': '; '.join(e.messages)}, status=400)
        
        # Verificar si el email ya está en uso
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El email ya está registrado'}, status=400)
        
        # Generar username desde el email (usar email como username, generar único si ya existe)
        username = email
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email}_{counter}"
            counter += 1
        
        # Crear usuario
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            
            # Crear perfil con DNI
            PerfilUsuario.objects.create(
                usuario=user,
                tipo_usuario=tipo_usuario,
                telefono=telefono or None,
                documento=dni,  # Guardar DNI en documento
            )
        
        # Generar tokens
        tokens = get_tokens_for_user(user)
        
        # Obtener perfil para incluir DNI
        perfil = PerfilUsuario.objects.filter(usuario=user).first()
        
        return JsonResponse({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'tokens': tokens,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'tipo_usuario': tipo_usuario,
                'documento': perfil.documento if perfil else None,
                'telefono': perfil.telefono if perfil else None,
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Payload inválido'}, status=400)
    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en registro: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({'error': f'Error al registrar usuario: {str(e)}'}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login_jwt(request):
    """
    Login con JWT
    """
    try:
        data = request.data
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return Response(
                {'error': 'Usuario y contraseña requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Autenticar usuario
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        
        if user is None or not user.is_active:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generar tokens
        tokens = get_tokens_for_user(user)
        
        # Obtener perfil
        perfil = getattr(user, 'perfil', None)
        tipo_usuario = perfil.tipo_usuario if perfil else 'MINORISTA'
        
        return Response({
            'success': True,
            'tokens': tokens,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email or '',
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'tipo_usuario': tipo_usuario,
                'is_staff': user.is_staff,
                'documento': perfil.documento if perfil else None,
                'telefono': perfil.telefono if perfil else None,
                'direccion': perfil.direccion if perfil else None,
                'ciudad': perfil.ciudad if perfil else None,
            }
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_usuario_actual_jwt(request):
    """
    Obtener información del usuario actual (JWT)
    """
    user = request.user
    perfil = getattr(user, 'perfil', None)
    tipo_usuario = perfil.tipo_usuario if perfil else 'MINORISTA'
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email or '',
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'tipo_usuario': tipo_usuario,
            'is_staff': user.is_staff,
            'documento': perfil.documento if perfil else None,
            'telefono': perfil.telefono if perfil else None,
            'direccion': perfil.direccion if perfil else None,
            'ciudad': perfil.ciudad if perfil else None,
        }
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_actualizar_perfil(request):
    """
    Actualizar perfil del usuario
    """
    try:
        user = request.user
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
        
        data = request.data
        
        # Actualizar campos del usuario
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        if 'email' in data:
            nuevo_email = data['email'].strip().lower()
            # Verificar que el email no esté en uso por otro usuario
            if User.objects.filter(email=nuevo_email).exclude(pk=user.pk).exists():
                return Response({
                    'error': 'Este email ya está en uso por otra cuenta'
                }, status=status.HTTP_400_BAD_REQUEST)
            user.email = nuevo_email
        user.save()
        
        # Actualizar campos del perfil
        if 'telefono' in data:
            perfil.telefono = data['telefono'].strip() if data['telefono'] else ''
        if 'documento' in data:
            perfil.documento = data['documento'].strip() if data['documento'] else ''
        if 'direccion' in data:
            perfil.direccion = data['direccion'].strip() if data['direccion'] else ''
        if 'ciudad' in data:
            perfil.ciudad = data['ciudad'].strip() if data['ciudad'] else ''
        perfil.save()
        
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email or '',
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'tipo_usuario': perfil.tipo_usuario,
                'documento': perfil.documento or '',
                'telefono': perfil.telefono or '',
                'direccion': perfil.direccion or '',
                'ciudad': perfil.ciudad or '',
            }
        })
    except Exception as e:
        logger.error(f"Error al actualizar perfil: {e}", exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_cambiar_contraseña(request):
    """
    Cambiar contraseña del usuario
    """
    try:
        user = request.user
        data = request.data
        
        contraseña_actual = data.get('contraseña_actual', '')
        nueva_contraseña = data.get('nueva_contraseña', '')
        confirmar_contraseña = data.get('confirmar_contraseña', '')
        
        # Validar campos requeridos
        if not contraseña_actual or not nueva_contraseña or not confirmar_contraseña:
            return Response({
                'error': 'Todos los campos son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar contraseña actual
        if not user.check_password(contraseña_actual):
            return Response({
                'error': 'La contraseña actual es incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que las nuevas contraseñas coincidan
        if nueva_contraseña != confirmar_contraseña:
            return Response({
                'error': 'Las nuevas contraseñas no coinciden'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar nueva contraseña
        try:
            validate_password(nueva_contraseña, user)
        except ValidationError as e:
            return Response({
                'error': '; '.join(e.messages)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cambiar contraseña
        user.set_password(nueva_contraseña)
        user.save()
        
        logger.info(f"Contraseña cambiada para usuario {user.username}")
        
        return Response({
            'success': True,
            'message': 'Contraseña actualizada correctamente'
        })
    except Exception as e:
        logger.error(f"Error al cambiar contraseña: {e}", exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_direcciones(request):
    """
    Obtener o crear direcciones de envío
    """
    if request.method == 'GET':
        direcciones = DireccionEnvio.objects.filter(usuario=request.user)
        return Response({
            'direcciones': [
                {
                    'id': d.id,
                    'nombre': d.nombre,
                    'telefono': d.telefono,
                    'direccion': d.direccion,
                    'ciudad': d.ciudad,
                    'codigo_postal': d.codigo_postal,
                    'provincia': d.provincia,
                    'pais': d.pais,
                    'es_principal': d.es_principal,
                }
                for d in direcciones
            ]
        })
    elif request.method == 'POST':
        direccion = DireccionEnvio.objects.create(
            usuario=request.user,
            nombre=request.data.get('nombre'),
            telefono=request.data.get('telefono'),
            direccion=request.data.get('direccion'),
            ciudad=request.data.get('ciudad'),
            codigo_postal=request.data.get('codigo_postal', ''),
            provincia=request.data.get('provincia', ''),
            pais=request.data.get('pais', 'Argentina'),
            es_principal=request.data.get('es_principal', False),
        )
        return Response({
            'direccion': {
                'id': direccion.id,
                'nombre': direccion.nombre,
                'telefono': direccion.telefono,
                'direccion': direccion.direccion,
                'ciudad': direccion.ciudad,
                'codigo_postal': direccion.codigo_postal,
                'provincia': direccion.provincia,
                'pais': direccion.pais,
                'es_principal': direccion.es_principal,
            }
        }, status=201)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_direcciones_detail(request, direccion_id):
    """
    Actualizar o eliminar una dirección
    """
    try:
        direccion = DireccionEnvio.objects.get(id=direccion_id, usuario=request.user)
        
        if request.method == 'PUT':
            direccion.nombre = request.data.get('nombre', direccion.nombre)
            direccion.telefono = request.data.get('telefono', direccion.telefono)
            direccion.direccion = request.data.get('direccion', direccion.direccion)
            direccion.ciudad = request.data.get('ciudad', direccion.ciudad)
            direccion.codigo_postal = request.data.get('codigo_postal', direccion.codigo_postal)
            direccion.provincia = request.data.get('provincia', direccion.provincia)
            direccion.es_principal = request.data.get('es_principal', direccion.es_principal)
            direccion.save()
            
            return Response({
                'direccion': {
                    'id': direccion.id,
                    'nombre': direccion.nombre,
                    'telefono': direccion.telefono,
                    'direccion': direccion.direccion,
                    'ciudad': direccion.ciudad,
                    'codigo_postal': direccion.codigo_postal,
                    'provincia': direccion.provincia,
                    'pais': direccion.pais,
                    'es_principal': direccion.es_principal,
                }
            })
        elif request.method == 'DELETE':
            direccion.delete()
            return Response({'success': True})
    except DireccionEnvio.DoesNotExist:
        return Response({'error': 'Dirección no encontrada'}, status=404)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_favoritos(request, producto_id=None):
    """
    Obtener, agregar o eliminar favoritos
    """
    if request.method == 'GET':
        favoritos = Favorito.objects.filter(usuario=request.user).select_related('variante', 'variante__producto')
        return Response({
            'favoritos': [
                {
                    'id': f.id,
                    'variante_id': f.variante.id,
                    'producto_nombre': f.variante.producto.nombre,
                    'sku': f.variante.sku,
                    'creado': f.creado.isoformat(),
                }
                for f in favoritos
            ]
        })
    elif request.method == 'POST' and producto_id:
        from inventario.models import ProductoVariante
        try:
            variante = ProductoVariante.objects.get(pk=producto_id)
            favorito, created = Favorito.objects.get_or_create(
                usuario=request.user,
                variante=variante
            )
            if created:
                return Response({'success': True, 'message': 'Agregado a favoritos'})
            else:
                return Response({'success': True, 'message': 'Ya está en favoritos'})
        except ProductoVariante.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
    elif request.method == 'DELETE' and producto_id:
        try:
            favorito = Favorito.objects.get(usuario=request.user, variante_id=producto_id)
            favorito.delete()
            return Response({'success': True, 'message': 'Eliminado de favoritos'})
        except Favorito.DoesNotExist:
            return Response({'error': 'Favorito no encontrado'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def api_solicitar_mayorista(request):
    """
    Endpoint para crear una solicitud de cuenta mayorista
    """
    try:
        data = json.loads(request.body)
        
        nombre = data.get('nombre', '').strip()
        apellido = data.get('apellido', '').strip()
        dni = data.get('dni', '').strip()
        cuit_cuil = data.get('cuit_cuil', '').strip()
        nombre_comercio = data.get('nombre_comercio', '').strip()
        rubro = data.get('rubro', '').strip()
        email = data.get('email', '').strip()
        telefono = data.get('telefono', '').strip()
        mensaje = data.get('mensaje', '').strip()
        
        # Validaciones
        if not all([nombre, apellido, dni, nombre_comercio, rubro, email, telefono]):
            return JsonResponse({'error': 'Todos los campos requeridos deben ser completados'}, status=400)
        
        # Crear solicitud
        solicitud = SolicitudMayorista.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            cuit_cuil=cuit_cuil or None,
            nombre_comercio=nombre_comercio,
            rubro=rubro,
            email=email,
            telefono=telefono,
            mensaje=mensaje or None,
            estado='PENDIENTE',
        )
        
        # Crear notificación de nueva solicitud mayorista
        try:
            from core.notificaciones import crear_notificacion_interna
            from core.models import NotificacionInterna
            from django.urls import reverse
            
            crear_notificacion_interna(
                tipo=NotificacionInterna.Tipo.SOLICITUD_MAYORISTA,
                prioridad=NotificacionInterna.Prioridad.MEDIA,
                titulo=f"Nueva Solicitud Mayorista: {nombre_comercio}",
                mensaje=f"El usuario {nombre} {apellido} ha solicitado una cuenta mayorista.",
                url_relacionada=reverse('dashboard:solicitudes_mayoristas'),
                datos_adicionales={'solicitud_id': solicitud.id, 'email': email}
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"No se pudo crear notificación de solicitud mayorista: {e}")
        
        return JsonResponse({
            'success': True,
            'message': 'Solicitud enviada correctamente. Será revisada a la brevedad.',
            'id': solicitud.id,
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Payload inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_historial_pedidos(request):
    """
    Historial de pedidos del usuario (POS y Web)
    Vincula por DNI o email
    """
    from ventas.models import Venta
    from django.db.models import Q
    
    user = request.user
    perfil = getattr(user, 'perfil', None)
    
    # Buscar ventas por vendedor (si es vendedor) o por DNI/email del cliente
    ventas_qs = Venta.objects.none()
    
    # Si el usuario tiene perfil con DNI, buscar por DNI
    if perfil and perfil.documento:
        ventas_qs = Venta.objects.filter(
            Q(vendedor=user) | 
            Q(cliente_documento=perfil.documento) |
            Q(cliente_nombre__icontains=user.get_full_name() or user.username)
        )
    else:
        # Buscar por email o vendedor
        ventas_qs = Venta.objects.filter(
            Q(vendedor=user) |
            Q(cliente_nombre__icontains=user.get_full_name() or user.username)
        )
    
    # Si tiene email, también buscar por email (si hay campo cliente_email en el futuro)
    if user.email:
        ventas_qs = ventas_qs | Venta.objects.filter(
            cliente_nombre__icontains=user.email.split('@')[0]
        )
    
    ventas = ventas_qs.distinct().prefetch_related('detalles', 'historial_estados').order_by('-fecha')[:50]
    
    return Response({
        'pedidos': [
            {
                'id': v.id,
                'fecha': v.fecha.isoformat(),
                'cliente_nombre': v.cliente_nombre,
                'total_ars': float(v.total_ars),
                'status': v.status,
                'status_display': v.get_status_display(),
                'estado_pago': v.estado_pago,
                'estado_pago_display': v.get_estado_pago_display(),
                'estado_entrega': v.estado_entrega,
                'estado_entrega_display': v.get_estado_entrega_display(),
                'metodo_pago': v.metodo_pago,
                'metodo_pago_display': v.get_metodo_pago_display(),
                'items_count': v.detalles.count(),
                'origen': v.origen,
                'origen_display': v.get_origen_display(),
                'motivo_cancelacion': v.motivo_cancelacion,
            }
            for v in ventas
        ]
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_pedido_detalle(request, pedido_id):
    """
    Detalle de un pedido con historial de estados
    """
    from ventas.models import Venta, HistorialEstadoVenta
    from django.db.models import Q
    
    user = request.user
    perfil = getattr(user, 'perfil', None)
    
    # Buscar venta que pertenezca al usuario
    try:
        if perfil and perfil.documento:
            venta = Venta.objects.filter(
                Q(id=pedido_id) & (
                    Q(vendedor=user) | 
                    Q(cliente_documento=perfil.documento) |
                    Q(cliente_nombre__icontains=user.get_full_name() or user.username)
                )
            ).prefetch_related('detalles', 'historial_estados').first()
        else:
            venta = Venta.objects.filter(
                Q(id=pedido_id) & (
                    Q(vendedor=user) |
                    Q(cliente_nombre__icontains=user.get_full_name() or user.username)
                )
            ).prefetch_related('detalles', 'historial_estados').first()
        
        if not venta:
            return Response({'error': 'Pedido no encontrado'}, status=404)
        
        # Obtener historial de estados
        historial = venta.historial_estados.all().order_by('creado')
        
        return Response({
            'pedido': {
                'id': venta.id,
                'fecha': venta.fecha.isoformat(),
                'cliente_nombre': venta.cliente_nombre or '',
                'cliente_documento': venta.cliente_documento or '',
                'total_ars': float(venta.total_ars),
                'subtotal_ars': float(venta.subtotal_ars),
                'descuento_total_ars': float(venta.descuento_total_ars),
                'impuestos_ars': float(venta.impuestos_ars),
                'status': venta.status,
                'status_display': venta.get_status_display(),
                'estado_pago': venta.estado_pago,
                'estado_pago_display': venta.get_estado_pago_display(),
                'estado_entrega': venta.estado_entrega,
                'estado_entrega_display': venta.get_estado_entrega_display(),
                'metodo_pago': venta.metodo_pago,
                'metodo_pago_display': venta.get_metodo_pago_display(),
                'origen': venta.origen,
                'origen_display': venta.get_origen_display(),
                'motivo_cancelacion': venta.motivo_cancelacion or '',
                'nota': venta.nota or '',
                'items': [
                    {
                        'sku': d.sku,
                        'descripcion': d.descripcion,
                        'cantidad': d.cantidad,
                        'precio_unitario_ars': float(d.precio_unitario_ars_congelado),
                        'subtotal_ars': float(d.subtotal_ars),
                    }
                    for d in venta.detalles.all()
                ],
                'historial': [
                    {
                        'estado_anterior': h.estado_anterior,
                        'estado_anterior_display': h.get_estado_anterior_display() if h.estado_anterior else None,
                        'estado_nuevo': h.estado_nuevo,
                        'estado_nuevo_display': h.get_estado_nuevo_display(),
                        'usuario': h.usuario.username if h.usuario else 'Sistema',
                        'nota': h.nota or '',
                        'fecha': h.creado.isoformat(),
                    }
                    for h in historial
                ],
            }
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_pedido_pdf(request, pedido_id):
    """
    Generar y descargar PDF del comprobante de un pedido
    """
    from ventas.models import Venta
    from ventas.pdf import generar_comprobante_pdf
    from django.db.models import Q
    from django.http import FileResponse
    
    user = request.user
    perfil = getattr(user, 'perfil', None)
    
    # Buscar venta que pertenezca al usuario
    try:
        if perfil and perfil.documento:
            venta = Venta.objects.filter(
                Q(id=pedido_id) & (
                    Q(vendedor=user) | 
                    Q(cliente_documento=perfil.documento) |
                    Q(cliente_nombre__icontains=user.get_full_name() or user.username)
                )
            ).first()
        else:
            venta = Venta.objects.filter(
                Q(id=pedido_id) & (
                    Q(vendedor=user) |
                    Q(cliente_nombre__icontains=user.get_full_name() or user.username)
                )
            ).first()
        
        if not venta:
            return Response({'error': 'Pedido no encontrado'}, status=404)
        
        # Generar PDF usando la función existente
        try:
            pdf_file = generar_comprobante_pdf(venta)
            filename = f"comprobante_{venta.id}.pdf"
            
            # Devolver el PDF directamente sin guardarlo
            from django.http import HttpResponse
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as pdf_error:
            logger.error(f"Error al generar PDF: {pdf_error}", exc_info=True)
            return Response({'error': 'No se pudo generar el comprobante'}, status=500)
        
    except Exception as e:
        logger.error(f"Error al generar PDF del pedido: {e}", exc_info=True)
        return Response({'error': 'Error al generar el comprobante'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_chat_cliente(request):
    """
    Endpoint público para chat IA con clientes.
    Responde consultas sobre productos, precios, stock, etc.
    Si el usuario está autenticado, incluye su contexto personal.
    """
    try:
        data = json.loads(request.body)
        mensaje = data.get('mensaje', '').strip()
        historial = data.get('historial', [])  # Lista de mensajes anteriores
        
        if not mensaje:
            return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)
        
        # Verificar si el usuario está autenticado (opcional)
        user = None
        perfil = None
        contexto_usuario = ""
        nombre_usuario = None
        
        try:
            from rest_framework_simplejwt.authentication import JWTAuthentication
            jwt_auth = JWTAuthentication()
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                user, token = auth_result
                perfil = getattr(user, 'perfil', None)
                
                # Obtener nombre del usuario
                nombre_completo = user.get_full_name()
                if nombre_completo:
                    nombre_usuario = nombre_completo.split()[0]  # Primer nombre
                elif user.first_name:
                    nombre_usuario = user.first_name
                elif user.username:
                    nombre_usuario = user.username.split('@')[0] if '@' in user.username else user.username
                
                # Construir contexto del usuario
                contexto_usuario = f"\n=== INFORMACIÓN DEL CLIENTE ===\n"
                contexto_usuario += f"Nombre: {nombre_completo or user.username}\n"
                contexto_usuario += f"Email: {user.email or 'No proporcionado'}\n"
                
                if perfil:
                    contexto_usuario += f"Tipo de cuenta: {perfil.get_tipo_usuario_display()}\n"
                    if perfil.documento:
                        contexto_usuario += f"DNI: {perfil.documento}\n"
                    if perfil.telefono:
                        contexto_usuario += f"Teléfono: {perfil.telefono}\n"
                    if perfil.direccion:
                        contexto_usuario += f"Dirección: {perfil.direccion}\n"
                
                # Obtener historial de pedidos
                from ventas.models import Venta
                from django.db.models import Q
                
                ventas_qs = Venta.objects.none()
                if perfil and perfil.documento:
                    ventas_qs = Venta.objects.filter(
                        Q(vendedor=user) | 
                        Q(cliente_documento=perfil.documento) |
                        Q(cliente_nombre__icontains=nombre_completo or user.username)
                    ).order_by('-fecha')[:10]
                else:
                    ventas_qs = Venta.objects.filter(
                        Q(vendedor=user) |
                        Q(cliente_nombre__icontains=nombre_completo or user.username)
                    ).order_by('-fecha')[:10]
                
                if ventas_qs.exists():
                    contexto_usuario += f"\nHistorial de pedidos ({ventas_qs.count()} pedidos):\n"
                    for venta in ventas_qs:
                        estado_pago = venta.get_estado_pago_display() if hasattr(venta, 'estado_pago') else 'N/A'
                        estado_entrega = venta.get_estado_entrega_display() if hasattr(venta, 'estado_entrega') else 'N/A'
                        origen = venta.get_origen_display() if hasattr(venta, 'origen') else 'N/A'
                        contexto_usuario += f"  • Pedido #{venta.id} - {venta.fecha.strftime('%d/%m/%Y')} - ${venta.monto_total:,.2f} - {origen} - Pago: {estado_pago} - Entrega: {estado_entrega}\n"
                        # Incluir algunos productos del pedido
                        detalles = venta.detalles.select_related('variante', 'variante__producto').all()[:3]
                        if detalles:
                            productos_lista = []
                            for d in detalles:
                                if d.variante and d.variante.producto:
                                    nombre_producto = d.variante.producto.nombre
                                else:
                                    nombre_producto = d.descripcion
                                productos_lista.append(f"{nombre_producto} (x{d.cantidad})")
                            if productos_lista:
                                contexto_usuario += f"    Productos: {', '.join(productos_lista)}\n"
                else:
                    contexto_usuario += "\nNo tiene pedidos previos.\n"
        except Exception as e:
            # Si falla la autenticación, continuar sin contexto de usuario
            logger.debug(f"Usuario no autenticado o error en autenticación: {e}")
        
        # Obtener información del catálogo para contexto
        from inventario.models import ProductoVariante, Precio, Categoria
        from configuracion.models import ConfiguracionSistema
        from django.db.models import Q
        import google.generativeai as genai
        from django.conf import settings
        
        # Configurar Gemini
        genai.configure(api_key=getattr(settings, 'GEMINI_API_KEY', None))
        
        # Buscar productos relacionados con la consulta del usuario
        productos_encontrados = []
        if mensaje:
            # Buscar productos que coincidan con el mensaje
            busqueda_terminos = mensaje.lower().split()
            query_productos = Q()
            for termino in busqueda_terminos:
                if len(termino) > 2:  # Ignorar palabras muy cortas
                    query_productos |= (
                        Q(producto__nombre__icontains=termino) |
                        Q(sku__icontains=termino) |
                        Q(atributo_1__icontains=termino) |
                        Q(atributo_2__icontains=termino) |
                        Q(producto__categoria__nombre__icontains=termino)
                    )
            
            if query_productos:
                productos_encontrados = ProductoVariante.objects.filter(
                    query_productos,
                    producto__activo=True,
                    activo=True
                ).select_related('producto', 'producto__categoria').prefetch_related('precios')[:5]
        
        # Obtener productos destacados si no se encontraron productos específicos
        if not productos_encontrados:
            productos_activos = ProductoVariante.objects.filter(
                producto__activo=True,
                activo=True
            ).select_related('producto', 'producto__categoria')[:10]
        else:
            productos_activos = productos_encontrados
        
        # Obtener categorías que tienen productos activos
        categorias = Categoria.objects.filter(
            productos__activo=True,
            productos__variantes__activo=True
        ).distinct()[:10]
        
        # Construir contexto del catálogo
        contexto_catalogo = "Catálogo disponible:\n"
        contexto_catalogo += f"- Categorías: {', '.join([c.nombre for c in categorias])}\n"
        
        # Si se encontraron productos específicos, incluirlos con más detalle
        if productos_encontrados:
            contexto_catalogo += f"\nProductos encontrados relacionados con tu consulta:\n"
            for prod in productos_encontrados:
                precio_minorista = prod.precios.filter(
                    tipo=Precio.Tipo.MINORISTA,
                    moneda=Precio.Moneda.ARS,
                    activo=True
                ).first()
                precio_usd = prod.precios.filter(
                    tipo=Precio.Tipo.MINORISTA,
                    moneda=Precio.Moneda.USD,
                    activo=True
                ).first()
                
                precio_texto = ""
                if precio_minorista:
                    precio_texto = f" - ${precio_minorista.precio:,.0f} ARS"
                elif precio_usd:
                    precio_texto = f" - US${precio_usd.precio:,.2f}"
                
                stock_texto = f" (Stock: {prod.stock_actual})" if prod.stock_actual > 0 else " (Sin stock)"
                contexto_catalogo += f"  • {prod.producto.nombre} {prod.atributos_display}{precio_texto}{stock_texto}\n"
        else:
            contexto_catalogo += "- Productos destacados:\n"
            for prod in productos_activos:
                contexto_catalogo += f"  • {prod.producto.nombre} ({prod.sku})\n"
        
        # Construir historial de conversación
        historial_texto = ""
        if historial:
            historial_texto = "\n".join([
                f"{'Cliente' if msg.get('tipo') == 'usuario' else 'Asistente'}: {msg.get('mensaje', '')}"
                for msg in historial[-6:]  # Últimos 6 mensajes
            ])
        
        # Obtener nombre comercial
        config = ConfiguracionSistema.objects.first()
        nombre_tienda = config.nombre_comercial if config else 'ImportStore'
        
        # Construir saludo personalizado
        saludo_personalizado = ""
        if nombre_usuario:
            saludo_personalizado = f"\nIMPORTANTE: El cliente está autenticado y se llama {nombre_usuario}. Debes saludarlo usando su nombre cuando sea apropiado (por ejemplo, al inicio de la conversación o cuando sea natural)."
        
        # Prompt para el asistente
        prompt = f"""Eres un asistente virtual de {nombre_tienda}, una tienda de productos tecnológicos.

Tu función es ayudar a los clientes con:
- Consultas sobre productos disponibles
- Información sobre precios
- Consultas de stock
- Recomendaciones de productos
- Información general sobre la tienda
- Consultas sobre pedidos anteriores (si el cliente está autenticado)

{contexto_usuario}

{contexto_catalogo}

Historial de conversación:
{historial_texto}

{saludo_personalizado}

Cliente: {mensaje}

Responde de forma amigable, profesional y concisa. 

IMPORTANTE:
- Si el cliente está autenticado y tiene nombre, úsalo de forma natural (ej: "Hola {nombre_usuario or 'cliente'}" al inicio si es el primer mensaje, o cuando sea apropiado).
- Si el cliente tiene pedidos previos, puedes hacer referencia a ellos cuando sea relevante (ej: "Veo que anteriormente compraste...").
- Si se encontraron productos relacionados con la consulta, menciona los productos encontrados con sus precios y stock.
- Si el cliente pregunta por un producto específico que no aparece en los resultados, sugiere que puede buscarlo en el catálogo de la web o contactarnos para más información.
- Para productos como iPhones o celulares, menciona que están disponibles en la categoría "Celulares".
- No inventes precios ni información que no tengas.
- Si hay productos encontrados, destácalos y proporciona información útil sobre ellos.
- Si el cliente pregunta sobre sus pedidos, usa la información del historial proporcionada.

Asistente:"""
        
        # Generar respuesta con Gemini (con fallback de modelos)
        respuesta = None
        modelos_candidatos = [
            "gemini-2.5-flash",      # Modelo más reciente y rápido
            "gemini-2.0-flash",      # Fallback estable
            "gemini-2.5-pro",        # Modelo más potente
            "gemini-flash-latest",   # Alias al último flash
            "gemini-pro-latest"      # Alias al último pro
        ]
        
        for model_name in modelos_candidatos:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                respuesta = response.text.strip()
                break
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                    logger.warning(f"Modelo Gemini '{model_name}' no disponible. Intentando siguiente...")
                    continue
                else:
                    logger.error(f"Error al generar respuesta con Gemini ({model_name}): {e}", exc_info=True)
                    break
        
        if not respuesta:
            # Respuesta de fallback si todos los modelos fallan
            respuesta = "Lo siento, no puedo procesar tu consulta en este momento. Por favor, contacta con nuestro equipo de atención al cliente o busca productos en nuestro catálogo."
        
        return JsonResponse({
            'success': True,
            'respuesta': respuesta,
            'mensaje': mensaje
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Payload inválido'}, status=400)
    except Exception as e:
        logger.error(f"Error en api_chat_cliente: {e}", exc_info=True)
        return JsonResponse({'error': 'Error al procesar la consulta'}, status=500)
