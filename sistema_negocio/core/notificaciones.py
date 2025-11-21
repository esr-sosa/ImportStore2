"""
Funciones helper para crear notificaciones internas automáticamente
"""
from django.utils import timezone
from django.urls import reverse
from .models import NotificacionInterna
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def crear_notificacion_interna(
    tipo: NotificacionInterna.Tipo,
    prioridad: NotificacionInterna.Prioridad,
    titulo: str,
    mensaje: str,
    url_relacionada: str = None,
    leida_por: User = None,
    datos_adicionales: dict = None
):
    """
    Crea una nueva notificación interna en el sistema.
    """
    try:
        NotificacionInterna.objects.create(
            tipo=tipo,
            prioridad=prioridad,
            titulo=titulo,
            mensaje=mensaje,
            url_relacionada=url_relacionada,
            leida_por=leida_por,
            fecha_lectura=timezone.now() if leida_por else None,
            datos_adicionales=datos_adicionales or {}
        )
        logger.info(f"Notificación interna creada: {titulo} ({tipo})")
    except Exception as e:
        logger.error(f"Error al crear notificación interna '{titulo}': {e}", exc_info=True)


def crear_notificacion(
    tipo: str,
    titulo: str,
    mensaje: str,
    prioridad: str = NotificacionInterna.Prioridad.MEDIA,
    url_relacionada: str = None,
    datos_adicionales: dict = None
) -> NotificacionInterna:
    """
    Crea una notificación interna
    
    Args:
        tipo: Tipo de notificación (usar NotificacionInterna.Tipo)
        titulo: Título de la notificación
        mensaje: Mensaje de la notificación
        prioridad: Prioridad (usar NotificacionInterna.Prioridad)
        url_relacionada: URL relacionada (opcional)
        datos_adicionales: Datos adicionales en formato dict (opcional)
    
    Returns:
        NotificacionInterna: La notificación creada
    """
    return NotificacionInterna.objects.create(
        tipo=tipo,
        titulo=titulo,
        mensaje=mensaje,
        prioridad=prioridad,
        url_relacionada=url_relacionada,
        datos_adicionales=datos_adicionales or {}
    )


def notificar_venta_web(venta_id: str, cliente_nombre: str, total: float):
    """Crea una notificación cuando se recibe una nueva venta web"""
    return crear_notificacion(
        tipo=NotificacionInterna.Tipo.VENTA_WEB,
        titulo=f"Nueva Venta Web: {venta_id}",
        mensaje=f"Se recibió una nueva venta web de {cliente_nombre} por ${total:,.2f}",
        prioridad=NotificacionInterna.Prioridad.ALTA,
        url_relacionada=f"/ventas/listado/?q={venta_id}",
        datos_adicionales={
            "venta_id": venta_id,
            "cliente_nombre": cliente_nombre,
            "total": total
        }
    )


def notificar_solicitud_mayorista(solicitud_id: int, nombre: str, email: str):
    """Crea una notificación cuando se recibe una nueva solicitud mayorista"""
    return crear_notificacion(
        tipo=NotificacionInterna.Tipo.SOLICITUD_MAYORISTA,
        titulo=f"Nueva Solicitud Mayorista: {nombre}",
        mensaje=f"Se recibió una nueva solicitud de cuenta mayorista de {nombre} ({email})",
        prioridad=NotificacionInterna.Prioridad.MEDIA,
        url_relacionada=f"/solicitudes-mayoristas/",
        datos_adicionales={
            "solicitud_id": solicitud_id,
            "nombre": nombre,
            "email": email
        }
    )


def notificar_error_pago(venta_id: str, error: str):
    """Crea una notificación cuando hay un error de pago"""
    return crear_notificacion(
        tipo=NotificacionInterna.Tipo.ERROR_PAGO,
        titulo=f"Error de Pago: {venta_id}",
        mensaje=f"Error al procesar el pago de la venta {venta_id}: {error}",
        prioridad=NotificacionInterna.Prioridad.URGENTE,
        url_relacionada=f"/ventas/listado/?q={venta_id}",
        datos_adicionales={
            "venta_id": venta_id,
            "error": error
        }
    )


def notificar_stock_bajo(variante_id: int, sku: str, stock_actual: int, stock_minimo: int):
    """Crea una notificación cuando el stock está bajo"""
    return crear_notificacion(
        tipo=NotificacionInterna.Tipo.STOCK_BAJO,
        titulo=f"Stock Bajo: {sku}",
        mensaje=f"El producto {sku} tiene stock bajo: {stock_actual} unidades (mínimo: {stock_minimo})",
        prioridad=NotificacionInterna.Prioridad.MEDIA,
        url_relacionada=f"/inventario/productos/{variante_id}/",
        datos_adicionales={
            "variante_id": variante_id,
            "sku": sku,
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo
        }
    )


def notificar_stock_reposicion(variante_id: int, sku: str, stock_anterior: int, stock_actual: int):
    """Crea una notificación cuando se repone stock"""
    return crear_notificacion(
        tipo=NotificacionInterna.Tipo.STOCK_REPOSICION,
        titulo=f"Stock Repuesto: {sku}",
        mensaje=f"El producto {sku} fue repuesto: {stock_anterior} → {stock_actual} unidades",
        prioridad=NotificacionInterna.Prioridad.BAJA,
        url_relacionada=f"/inventario/productos/{variante_id}/",
        datos_adicionales={
            "variante_id": variante_id,
            "sku": sku,
            "stock_anterior": stock_anterior,
            "stock_actual": stock_actual
        }
    )


def notificar_pedido_pendiente(venta_id: str, cliente_nombre: str, dias_pendiente: int):
    """Crea una notificación cuando un pedido está pendiente de pago por mucho tiempo"""
    return crear_notificacion(
        tipo=NotificacionInterna.Tipo.PEDIDO_PENDIENTE,
        titulo=f"Pedido Pendiente: {venta_id}",
        mensaje=f"El pedido {venta_id} de {cliente_nombre} lleva {dias_pendiente} días pendiente de pago",
        prioridad=NotificacionInterna.Prioridad.ALTA,
        url_relacionada=f"/ventas/listado/?q={venta_id}",
        datos_adicionales={
            "venta_id": venta_id,
            "cliente_nombre": cliente_nombre,
            "dias_pendiente": dias_pendiente
        }
    )

