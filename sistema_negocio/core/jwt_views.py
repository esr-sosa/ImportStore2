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
    Registro de nuevos usuarios (mayoristas y minoristas)
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
        }
    })


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_actualizar_perfil(request):
    """
    Actualizar perfil de usuario
    """
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
    
    # Actualizar perfil
    if 'tipo_usuario' in data:
        tipo = data['tipo_usuario'].upper()
        if tipo in ['MINORISTA', 'MAYORISTA']:
            perfil.tipo_usuario = tipo
    if 'telefono' in data:
        perfil.telefono = data['telefono']
    if 'direccion' in data:
        perfil.direccion = data['direccion']
    if 'ciudad' in data:
        perfil.ciudad = data['ciudad']
    if 'codigo_postal' in data:
        perfil.codigo_postal = data['codigo_postal']
    if 'documento' in data:
        perfil.documento = data['documento']
    if 'fecha_nacimiento' in data:
        perfil.fecha_nacimiento = data['fecha_nacimiento']
    
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
            'telefono': perfil.telefono or '',
            'direccion': perfil.direccion or '',
            'ciudad': perfil.ciudad or '',
        }
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_direcciones(request):
    """
    Listar o crear direcciones de envío
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
        data = request.data
        direccion = DireccionEnvio.objects.create(
            usuario=request.user,
            nombre=data.get('nombre', ''),
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', ''),
            ciudad=data.get('ciudad', ''),
            codigo_postal=data.get('codigo_postal', ''),
            provincia=data.get('provincia', ''),
            pais=data.get('pais', 'Argentina'),
            es_principal=data.get('es_principal', False),
        )
        
        return Response({
            'success': True,
            'direccion': {
                'id': direccion.id,
                'nombre': direccion.nombre,
                'telefono': direccion.telefono,
                'direccion': direccion.direccion,
                'ciudad': direccion.ciudad,
                'es_principal': direccion.es_principal,
            }
        }, status=201)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_favoritos(request, producto_id=None):
    """
    Gestionar favoritos
    """
    from inventario.models import ProductoVariante
    
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
    
    elif request.method == 'POST':
        if not producto_id:
            return Response({'error': 'producto_id requerido'}, status=400)
        
        try:
            variante = ProductoVariante.objects.get(pk=producto_id)
        except ProductoVariante.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
        
        favorito, created = Favorito.objects.get_or_create(
            usuario=request.user,
            variante=variante
        )
        
        return Response({
            'success': True,
            'message': 'Agregado a favoritos' if created else 'Ya está en favoritos',
            'favorito_id': favorito.id,
        }, status=201 if created else 200)
    
    elif request.method == 'DELETE':
        if not producto_id:
            return Response({'error': 'producto_id requerido'}, status=400)
        
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
    Historial de pedidos del usuario
    """
    from ventas.models import Venta
    
    ventas = Venta.objects.filter(
        vendedor=request.user
    ).prefetch_related('detalles').order_by('-fecha')[:50]
    
    return Response({
        'pedidos': [
            {
                'id': v.id,
                'fecha': v.fecha.isoformat(),
                'cliente_nombre': v.cliente_nombre,
                'total_ars': float(v.total_ars),
                'status': v.status,
                'metodo_pago': v.metodo_pago,
                'items_count': v.detalles.count(),
            }
            for v in ventas
        ]
    })

