"""
Vistas para gestionar solicitudes mayoristas en el dashboard
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

from core.models import SolicitudMayorista, PerfilUsuario
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def solicitudes_mayoristas_list(request):
    """
    Lista todas las solicitudes mayoristas
    """
    estado_filter = request.GET.get('estado', '')
    
    solicitudes = SolicitudMayorista.objects.all().order_by('-creado')
    
    if estado_filter:
        solicitudes = solicitudes.filter(estado=estado_filter)
    
    # Estadísticas
    total_pendientes = SolicitudMayorista.objects.filter(estado='PENDIENTE').count()
    total_aprobadas = SolicitudMayorista.objects.filter(estado='APROBADA').count()
    total_rechazadas = SolicitudMayorista.objects.filter(estado='RECHAZADA').count()
    
    context = {
        'solicitudes': solicitudes,
        'total_pendientes': total_pendientes,
        'total_aprobadas': total_aprobadas,
        'total_rechazadas': total_rechazadas,
        'estado_filter': estado_filter,
    }
    
    return render(request, 'dashboard/solicitudes_mayoristas.html', context)


@login_required
def aprobar_solicitud_mayorista(request, solicitud_id):
    """
    Aprueba una solicitud mayorista y convierte al usuario en mayorista
    """
    solicitud = get_object_or_404(SolicitudMayorista, pk=solicitud_id)
    
    if solicitud.estado != 'PENDIENTE':
        messages.error(request, 'Esta solicitud ya fue procesada.')
        return redirect('dashboard:solicitudes_mayoristas')
    
    try:
        with transaction.atomic():
            # Buscar usuario por email
            usuario = None
            try:
                usuario = User.objects.get(email=solicitud.email)
            except User.DoesNotExist:
                # Si no existe usuario, crear uno nuevo
                username = solicitud.email.split('@')[0]
                # Asegurar que el username sea único
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                usuario = User.objects.create_user(
                    username=username,
                    email=solicitud.email,
                    first_name=solicitud.nombre,
                    last_name=solicitud.apellido,
                    is_active=True,
                )
                
                # Crear perfil
                PerfilUsuario.objects.create(
                    usuario=usuario,
                    tipo_usuario='MAYORISTA',
                    telefono=solicitud.telefono,
                    documento=solicitud.dni,
                )
            else:
                # Usuario existe, actualizar perfil
                perfil, created = PerfilUsuario.objects.get_or_create(
                    usuario=usuario,
                    defaults={
                        'tipo_usuario': 'MAYORISTA',
                        'telefono': solicitud.telefono,
                        'documento': solicitud.dni,
                    }
                )
                if not created:
                    perfil.tipo_usuario = 'MAYORISTA'
                    if not perfil.telefono:
                        perfil.telefono = solicitud.telefono
                    if not perfil.documento:
                        perfil.documento = solicitud.dni
                    perfil.save()
            
            # Actualizar solicitud
            solicitud.estado = 'APROBADA'
            solicitud.revisado_por = request.user
            solicitud.fecha_revision = timezone.now()
            solicitud.save()
        
        # Enviar email de notificación (si está configurado)
        try:
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                send_mail(
                    subject='Solicitud de cuenta mayorista aprobada',
                    message=f'Hola {solicitud.nombre},\n\nTu solicitud de cuenta mayorista ha sido aprobada. Ya puedes acceder con tu cuenta y ver los precios mayoristas.\n\nSaludos,\nEquipo de ImportStore',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[solicitud.email],
                    fail_silently=True,
                )
        except Exception:
            pass  # Si falla el email, continuar
        
        messages.success(request, f'Solicitud aprobada. Usuario {usuario.username} ahora es mayorista.')
    except Exception as e:
        messages.error(request, f'Error al aprobar solicitud: {str(e)}')
    
    return redirect('dashboard:solicitudes_mayoristas')


@login_required
def rechazar_solicitud_mayorista(request, solicitud_id):
    """
    Rechaza una solicitud mayorista
    """
    solicitud = get_object_or_404(SolicitudMayorista, pk=solicitud_id)
    
    if solicitud.estado != 'PENDIENTE':
        messages.error(request, 'Esta solicitud ya fue procesada.')
        return redirect('dashboard:solicitudes_mayoristas')
    
    if request.method == 'POST':
        notas = request.POST.get('notas', '').strip()
        
        solicitud.estado = 'RECHAZADA'
        solicitud.revisado_por = request.user
        solicitud.fecha_revision = timezone.now()
        solicitud.notas = notas
        solicitud.save()
        
        # Enviar email de notificación (si está configurado)
        try:
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                send_mail(
                    subject='Solicitud de cuenta mayorista',
                    message=f'Hola {solicitud.nombre},\n\nTu solicitud de cuenta mayorista ha sido revisada. Por el momento no podemos aprobar tu solicitud.\n\n{"Motivo: " + notas if notas else ""}\n\nSaludos,\nEquipo de ImportStore',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[solicitud.email],
                    fail_silently=True,
                )
        except Exception:
            pass
        
        messages.success(request, 'Solicitud rechazada.')
        return redirect('dashboard:solicitudes_mayoristas')
    
    # Mostrar formulario de rechazo
    return render(request, 'dashboard/rechazar_solicitud.html', {'solicitud': solicitud})

