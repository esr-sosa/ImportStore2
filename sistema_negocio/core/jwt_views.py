"""
Vistas JWT para autenticación y registro
"""
import json
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
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        password_confirm = data.get('password_confirm', '')
        tipo_usuario = 'MINORISTA'  # SIEMPRE minorista en registro normal
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        telefono = data.get('telefono', '').strip()
        dni = data.get('dni', '').strip()  # DNI obligatorio
        
        # Validaciones
        if not username:
            return JsonResponse({'error': 'El nombre de usuario es requerido'}, status=400)
        
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
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El email ya está en uso'}, status=400)
        
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
        return JsonResponse({'error': str(e)}, status=500)


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
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        user.save()
        
        # Actualizar campos del perfil
        if 'telefono' in data:
            perfil.telefono = data['telefono']
        if 'documento' in data:
            perfil.documento = data['documento']
        if 'direccion' in data:
            perfil.direccion = data['direccion']
        if 'ciudad' in data:
            perfil.ciudad = data['ciudad']
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
                'documento': perfil.documento,
                'telefono': perfil.telefono,
                'direccion': perfil.direccion,
                'ciudad': perfil.ciudad,
            }
        })
    except Exception as e:
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
            nombre_comercio=nombre_comercio,
            rubro=rubro,
            email=email,
            telefono=telefono,
            mensaje=mensaje or None,
            estado='PENDIENTE',
        )
        
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
        
        historial = venta.historial_estados.all().order_by('-creado')
        
        return Response({
            'pedido': {
                'id': venta.id,
                'fecha': venta.fecha.isoformat(),
                'cliente_nombre': venta.cliente_nombre,
                'cliente_documento': venta.cliente_documento,
                'total_ars': float(venta.total_ars),
                'subtotal_ars': float(venta.subtotal_ars),
                'descuento_total_ars': float(venta.descuento_total_ars),
                'impuestos_ars': float(venta.impuestos_ars),
                'status': venta.status,
                'status_display': venta.get_status_display(),
                'metodo_pago': venta.metodo_pago,
                'metodo_pago_display': venta.get_metodo_pago_display(),
                'origen': venta.origen,
                'origen_display': venta.get_origen_display(),
                'motivo_cancelacion': venta.motivo_cancelacion,
                'nota': venta.nota,
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
                        'nota': h.nota,
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
    from ventas.views import generar_voucher_pdf
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
        
        # Usar la función existente de generar PDF
        return generar_voucher_pdf(request, pedido_id)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
