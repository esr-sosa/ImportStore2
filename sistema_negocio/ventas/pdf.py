from __future__ import annotations

import os
from decimal import Decimal
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image

try:
    import qrcode
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
except ImportError as exc:
    qrcode = A4 = mm = canvas = colors = None
    _reportlab_import_error = exc
else:
    _reportlab_import_error = None

from configuracion.models import ConfiguracionSistema, ConfiguracionTienda
from locales.models import Local
from ventas.models import Venta


def _generar_qr_whatsapp(venta, telefono: str) -> BytesIO:
    """Genera un QR code que abre WhatsApp con un mensaje sobre la compra."""
    if qrcode is None:
        return None
    
    from urllib.parse import quote
    from django.utils import timezone
    
    # Limpiar y normalizar el teléfono
    telefono_limpio = telefono.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Construir mensaje completo con fecha, hora y productos
    fecha_local = timezone.localtime(venta.fecha)
    fecha_str = fecha_local.strftime("%d/%m/%Y")
    hora_str = fecha_local.strftime("%H:%M")
    
    # Lista de productos
    productos_lista = []
    for detalle in venta.detalles.all():
        productos_lista.append(f"- {detalle.descripcion} x{detalle.cantidad}")
    
    productos_texto = "\n".join(productos_lista[:10])  # Máximo 10 productos para no exceder límite de URL
    
    # Mensaje completo
    mensaje = f"Tengo una consulta sobre el pedido {venta.id} comprado el día {fecha_str} a las {hora_str}.\n\nProductos:\n{productos_texto}"
    
    # Codificar correctamente la URL
    mensaje_codificado = quote(mensaje, safe='')
    url_whatsapp = f"https://wa.me/{telefono_limpio}?text={mensaje_codificado}"
    
    # Generar QR con mejor calidad
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url_whatsapp)
    qr.make(fit=True)
    
    img_qr = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img_qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generar_comprobante_pdf(venta) -> ContentFile:
    if canvas is None:
        raise ImproperlyConfigured(
            "Las librerías 'reportlab' y 'qrcode' son necesarias para generar comprobantes PDF. "
            "Instalálas ejecutando `pip install -r requirements.txt`."
        ) from _reportlab_import_error

    config_tienda = ConfiguracionTienda.obtener_unica()
    config_sistema = ConfiguracionSistema.carga()
    locales = list(Local.objects.order_by("nombre"))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    content_width = width - (2 * margin)

    # ========== HEADER ESTILO APPLE ==========
    y = height - margin
    
    # Logo (si existe) - MEJORADO
    logo_dibujado = False
    import logging
    logger = logging.getLogger(__name__)
    
    # Priorizar logo de tienda sobre sistema
    logo_fields = []
    if config_tienda and config_tienda.logo:
        logo_fields.append(('tienda', config_tienda.logo))
    if config_sistema and config_sistema.logo:
        logo_fields.append(('sistema', config_sistema.logo))
    
    logger.info(f"Intentando cargar logo. Campos encontrados: {len(logo_fields)}")
    
    for origen, logo_field in logo_fields:
        if not logo_field:
            logger.warning(f"Logo ({origen}) es None")
            continue
            
        logger.info(f"Procesando logo ({origen}), name: {getattr(logo_field, 'name', 'N/A')}")
            
        try:
            logo_img = None
            tmp_path = None
            
            # Método 1: Intentar con path directo (más confiable en desarrollo)
            try:
                if hasattr(logo_field, 'path'):
                    logo_path = logo_field.path
                    logger.info(f"Intentando path directo: {logo_path}")
                    if logo_path and os.path.exists(logo_path):
                        logo_img = Image.open(logo_path)
                        logger.info(f"✓ Logo ({origen}) cargado desde path: {logo_path}")
                    else:
                        logger.warning(f"Path no existe: {logo_path}")
            except Exception as e:
                logger.debug(f"Path no disponible: {e}")
            
            # Método 2: Intentar con MEDIA_ROOT + name
            if logo_img is None and hasattr(logo_field, 'name') and logo_field.name:
                try:
                    media_path = os.path.join(settings.MEDIA_ROOT, logo_field.name)
                    logger.info(f"Intentando MEDIA_ROOT: {media_path}")
                    if os.path.exists(media_path):
                        logo_img = Image.open(media_path)
                        logger.info(f"✓ Logo ({origen}) cargado desde MEDIA_ROOT: {media_path}")
                except Exception as e:
                    logger.debug(f"MEDIA_ROOT no disponible: {e}")
            
            # Método 3: Intentar con storage de Django
            if logo_img is None:
                try:
                    from django.core.files.storage import default_storage
                    if logo_field.name and default_storage.exists(logo_field.name):
                        logger.info(f"Intentando default_storage: {logo_field.name}")
                        with default_storage.open(logo_field.name, 'rb') as f:
                            logo_img = Image.open(f)
                            logo_img.load()  # Forzar carga completa
                            logger.info(f"✓ Logo ({origen}) cargado desde storage: {logo_field.name}")
                except Exception as e:
                    logger.debug(f"Storage no disponible: {e}")
            
            # Método 4: Intentar con file object
            if logo_img is None and hasattr(logo_field, 'file'):
                try:
                    logger.info("Intentando file object")
                    logo_field.file.seek(0)
                    logo_img = Image.open(logo_field.file)
                    logo_img.load()
                    logger.info(f"✓ Logo ({origen}) cargado desde file object")
                except Exception as e:
                    logger.debug(f"File object no disponible: {e}")
            
            if logo_img is None:
                logger.warning(f"✗ No se pudo cargar el logo ({origen}) desde ninguna fuente. name={getattr(logo_field, 'name', 'N/A')}")
                continue
            
            # Redimensionar logo manteniendo aspecto (máx 80x80)
            logo_img.thumbnail((80, 80), Image.Resampling.LANCZOS)
            
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if logo_img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', logo_img.size, (255, 255, 255))
                if logo_img.mode == 'P':
                    logo_img = logo_img.convert('RGBA')
                rgb_img.paste(logo_img, mask=logo_img.split()[-1] if logo_img.mode in ('RGBA', 'LA') else None)
                logo_img = rgb_img
            
            # Guardar a archivo temporal para ReportLab
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                logo_img.save(tmp_file.name, format="PNG", quality=95)
                tmp_path = tmp_file.name
            
            try:
                c.drawImage(tmp_path, margin, y - 80, width=80, height=80, mask='auto')
                logo_dibujado = True
                y -= 90
                logger.info(f"Logo ({origen}) dibujado exitosamente en el PDF")
            except Exception as e:
                logger.error(f"Error al dibujar logo: {e}")
            finally:
                # Limpiar archivo temporal
                if tmp_path:
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
            
            if logo_dibujado:
                break
        except Exception as e:
            logger.warning(f"Error general al procesar logo ({origen}): {e}")
            import traceback
            logger.debug(traceback.format_exc())
            continue
    
    # Nombre de la tienda (grande y elegante)
    c.setFont("Helvetica-Bold", 24)
    nombre_tienda = config_tienda.nombre_tienda or config_sistema.nombre_comercial or "ImportStore"
    c.drawString(margin, y, nombre_tienda)
    y -= 30

    # Información de contacto (pequeña y discreta)
    c.setFont("Helvetica", 9)
    contacto_lines = []
    if config_tienda.cuit:
        contacto_lines.append(f"CUIT: {config_tienda.cuit}")
    direccion = config_tienda.direccion or config_sistema.domicilio_comercial
    if direccion:
        contacto_lines.append(direccion)
    email = config_tienda.email_contacto or config_sistema.contacto_email
    if email:
        contacto_lines.append(f"Email: {email}")
    telefono = config_tienda.telefono_contacto or config_sistema.whatsapp_numero
    if telefono:
        contacto_lines.append(f"Tel: {telefono}")
    
    for line in contacto_lines:
        c.drawString(margin, y, line)
        y -= 12
    
    y -= 15

    # ========== INFORMACIÓN DE LA VENTA ==========
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, f"Comprobante #{venta.id}")
    y -= 20

    c.setFont("Helvetica", 10)
    # Usar zona horaria local (ya configurada en settings)
    fecha_local = timezone.localtime(venta.fecha)
    fecha_str = fecha_local.strftime("%d/%m/%Y %H:%M:%S")
    c.drawString(margin, y, f"Fecha y hora: {fecha_str}")
    y -= 14

    if venta.vendedor:
        vendedor_nombre = venta.vendedor.get_full_name() or venta.vendedor.username
        c.drawString(margin, y, f"Vendedor: {vendedor_nombre}")
        y -= 14

    if venta.cliente_nombre:
        c.drawString(margin, y, f"Cliente: {venta.cliente_nombre}")
        y -= 14
        if venta.cliente_documento:
            c.drawString(margin, y, f"Documento: {venta.cliente_documento}")
            y -= 14
    
    # Información del local (si está asociado a una caja)
    if hasattr(venta, 'movimientos_caja') and venta.movimientos_caja.exists():
        movimiento = venta.movimientos_caja.first()
        if movimiento and movimiento.caja_diaria:
            c.drawString(margin, y, f"Local: {movimiento.caja_diaria.local.nombre}")
            y -= 14
            if movimiento.caja_diaria.local.direccion:
                c.drawString(margin, y, f"Dirección: {movimiento.caja_diaria.local.direccion}")
                y -= 14
    
    # Nota de la venta (si existe)
    if venta.nota:
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        c.drawString(margin, y, f"Nota: {venta.nota[:100]}")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        y -= 14

    y -= 20

    # ========== TABLA DE PRODUCTOS (ESTILO APPLE) ==========
    # Encabezados
    c.setFont("Helvetica-Bold", 10)
    header_y = y
    c.drawString(margin, header_y, "Descripción")
    c.drawRightString(margin + content_width * 0.65, header_y, "Cant.")
    c.drawRightString(margin + content_width * 0.80, header_y, "P. Unit.")
    c.drawRightString(width - margin, header_y, "Total")
    
    # Línea separadora
    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.5)
    c.line(margin, header_y - 6, width - margin, header_y - 6)
    y = header_y - 20

    # Productos
    c.setFont("Helvetica", 9)
    detalles = list(venta.detalles.all())
    items_per_page = 25  # Ajustar según necesidad
    
    for idx, detalle in enumerate(detalles):
        # Nueva página si es necesario
        if y < 100 and idx < len(detalles) - 1:
            # Totales en la parte inferior antes de nueva página
            c.setFont("Helvetica-Bold", 10)
            c.setStrokeColor(colors.grey)
            c.line(margin, y - 10, width - margin, y - 10)
            y -= 20
            c.drawString(margin, y, "(Continúa en siguiente página...)")
            
            c.showPage()
            y = height - margin - 40
            c.setFont("Helvetica", 9)

        # Descripción (con wrap si es muy larga)
        desc = detalle.descripcion[:50] + "..." if len(detalle.descripcion) > 50 else detalle.descripcion
        c.drawString(margin, y, desc)
        
        # SKU pequeño debajo
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.grey)
        c.drawString(margin, y - 10, f"SKU: {detalle.sku}")
        
        # Calcular descuento si existe (comparando precio unitario * cantidad vs subtotal)
        precio_bruto = detalle.precio_unitario_ars_congelado * detalle.cantidad
        descuento_linea = precio_bruto - detalle.subtotal_ars
        tiene_descuento = descuento_linea > Decimal("0.01")
        
        # Si tiene conversión USD -> ARS, mostrar información
        if detalle.precio_unitario_usd_original and detalle.tipo_cambio_usado:
            conversion_text = f"US${detalle.precio_unitario_usd_original:.2f} × {detalle.tipo_cambio_usado:.2f} = ${detalle.precio_unitario_ars_congelado:.2f}"
            c.drawString(margin, y - 20, conversion_text)
            y -= 10
        
        # Mostrar descuento si existe
        if tiene_descuento:
            porcentaje_desc = (descuento_linea / precio_bruto) * 100 if precio_bruto > 0 else 0
            descuento_text = f"Descuento: -${descuento_linea:.2f} ({porcentaje_desc:.1f}%)"
            c.setFillColor(colors.darkgreen)
            c.drawString(margin, y - 20, descuento_text)
            y -= 10
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        
        # Cantidad, precio unitario y total (alineados a la derecha)
        c.drawRightString(margin + content_width * 0.65, y, str(detalle.cantidad))
        c.drawRightString(margin + content_width * 0.80, y, f"${detalle.precio_unitario_ars_congelado:.2f}")
        # Mostrar precio final después del descuento
        if tiene_descuento:
            c.setFillColor(colors.darkgreen)
            c.drawRightString(width - margin, y, f"${detalle.subtotal_ars:.2f}")
            c.setFillColor(colors.black)
        else:
            c.drawRightString(width - margin, y, f"${detalle.subtotal_ars:.2f}")
        
        # Ajustar espacio según si hay conversión o descuento
        espacio_extra = 0
        if detalle.precio_unitario_usd_original and detalle.tipo_cambio_usado:
            espacio_extra += 10
        if tiene_descuento:
            espacio_extra += 10
        y -= (22 + espacio_extra)

    # ========== TOTALES ==========
    y -= 10
    c.setStrokeColor(colors.grey)
    c.line(margin, y, width - margin, y)
    y -= 15

    c.setFont("Helvetica", 10)
    c.drawRightString(width - margin, y, f"Subtotal: ${venta.subtotal_ars:.2f}")
    y -= 14

    if venta.descuento_total_ars > 0:
        c.setFillColor(colors.darkgreen)
        c.drawRightString(width - margin, y, f"Descuentos: -${venta.descuento_total_ars:.2f}")
        c.setFillColor(colors.black)
        y -= 14

    if venta.impuestos_ars > 0:
        c.drawRightString(width - margin, y, f"Impuestos: ${venta.impuestos_ars:.2f}")
        y -= 14

    y -= 5
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.line(margin, y, width - margin, y)
    y -= 15

    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width - margin, y, f"TOTAL: ${venta.total_ars:.2f}")
    y -= 20

    # Método de pago
    c.setFont("Helvetica", 9)
    metodo_pago_display = dict(Venta.MetodoPago.choices).get(venta.metodo_pago, venta.metodo_pago)
    c.drawString(margin, y, f"Método de pago: {metodo_pago_display}")
    y -= 20

    # ========== QR CODE WHATSAPP ==========
    # Asegurar que tenemos un teléfono válido
    telefono_whatsapp = telefono or config_tienda.telefono_contacto or config_sistema.whatsapp_numero
    if telefono_whatsapp:
        try:
            qr_buffer = _generar_qr_whatsapp(venta, telefono_whatsapp)
            if qr_buffer:
                # Guardar QR a archivo temporal
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_qr_file:
                    qr_buffer.seek(0)
                    tmp_qr_file.write(qr_buffer.read())
                    tmp_qr_path = tmp_qr_file.name
                
                try:
                    qr_size = 80  # Más grande y visible
                    qr_x = width - margin - qr_size
                    qr_y = y - qr_size - 20
                    
                    # Fondo blanco para el QR (estilo Apple)
                    c.setFillColor(colors.white)
                    c.rect(qr_x - 5, qr_y - 5, qr_size + 10, qr_size + 10, fill=1, stroke=0)
                    c.setFillColor(colors.black)
                    
                    # Dibujar el QR
                    c.drawImage(tmp_qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
                    
                    # Borde alrededor del QR
                    c.setStrokeColor(colors.grey)
                    c.setLineWidth(0.5)
                    c.rect(qr_x - 5, qr_y - 5, qr_size + 10, qr_size + 10, fill=0, stroke=1)
                    
                    # Texto debajo del QR (mejorado)
                    c.setFont("Helvetica-Bold", 8)
                    c.setFillColor(colors.black)
                    texto_y = qr_y - 20
                    c.drawCentredString(qr_x + qr_size / 2, texto_y, "Tenga una consulta sobre este pedido")
                    c.setFont("Helvetica", 7)
                    c.setFillColor(colors.grey)
                    c.drawCentredString(qr_x + qr_size / 2, texto_y - 12, "WhatsApp")
                    c.setFillColor(colors.black)
                finally:
                    # Limpiar archivo temporal
                    try:
                        os.unlink(tmp_qr_path)
                    except:
                        pass
        except Exception as e:
            # Log del error pero no fallar el PDF
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error al generar QR: {e}")
            import traceback
            logger.warning(traceback.format_exc())

    # ========== LOCALES (si hay) ==========
    y -= 80
    if locales:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "Locales / Puntos de retiro:")
        y -= 15
        c.setFont("Helvetica", 8)
        for local in locales[:3]:  # Máximo 3 locales para no ocupar mucho espacio
            if y < 50:
                break
            direccion_local = local.direccion or "Dirección a confirmar"
            c.drawString(margin + 10, y, f"• {local.nombre}: {direccion_local}")
            y -= 12

    # ========== FOOTER ==========
    y = 40
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, y, f"{nombre_tienda} - Comprobante #{venta.id}")
    c.drawCentredString(width / 2, y - 10, "Gracias por su compra")

    c.showPage()
    c.save()
    buffer.seek(0)
    filename = f"comprobante_{venta.id}.pdf"
    return ContentFile(buffer.read(), name=filename)
