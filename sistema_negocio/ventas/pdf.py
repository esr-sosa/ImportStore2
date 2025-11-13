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
    
    import logging
    logger = logging.getLogger(__name__)
    
    # ========== HEADER ESTILO APPLE ==========
    # Empezar más arriba para el logo (30px más arriba)
    y = height - margin - 30
    
    # Logo (si existe) - MEJORADO
    logo_dibujado = False
    
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
                    else:
                        # Intentar sin el prefijo branding/ si existe
                        if logo_field.name.startswith('branding/'):
                            alt_path = os.path.join(settings.MEDIA_ROOT, logo_field.name.replace('branding/', ''))
                            logger.info(f"Intentando MEDIA_ROOT alternativo: {alt_path}")
                            if os.path.exists(alt_path):
                                logo_img = Image.open(alt_path)
                                logger.info(f"✓ Logo ({origen}) cargado desde MEDIA_ROOT alternativo: {alt_path}")
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
            
            # Método 5: Intentar con URL (si está disponible)
            if logo_img is None and hasattr(logo_field, 'url'):
                try:
                    import requests
                    logo_url = logo_field.url
                    if logo_url.startswith('/'):
                        # URL relativa, construir URL completa usando MEDIA_URL
                        from django.conf import settings
                        if hasattr(settings, 'MEDIA_URL'):
                            # Si MEDIA_URL es absoluto, usarlo directamente
                            if settings.MEDIA_URL.startswith('http'):
                                logo_url = f"{settings.MEDIA_URL.rstrip('/')}/{logo_field.name}"
                            else:
                                # Construir URL local
                                protocol = 'https' if not settings.DEBUG else 'http'
                                logo_url = f"{protocol}://127.0.0.1:8000{settings.MEDIA_URL.rstrip('/')}/{logo_field.name}"
                    logger.info(f"Intentando URL: {logo_url}")
                    response = requests.get(logo_url, timeout=5, verify=False)
                    if response.status_code == 200:
                        logo_img = Image.open(BytesIO(response.content))
                        logger.info(f"✓ Logo ({origen}) cargado desde URL: {logo_url}")
                except Exception as e:
                    logger.debug(f"URL no disponible: {e}")
            
            # Método 6: Intentar buscar en todos los archivos de branding/
            if logo_img is None and hasattr(logo_field, 'name') and logo_field.name:
                try:
                    import glob
                    branding_dir = os.path.join(settings.MEDIA_ROOT, 'branding')
                    if os.path.exists(branding_dir):
                        # Buscar cualquier imagen en branding/
                        pattern = os.path.join(branding_dir, '*')
                        for file_path in glob.glob(pattern):
                            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                                try:
                                    logo_img = Image.open(file_path)
                                    logger.info(f"✓ Logo ({origen}) cargado desde branding/: {file_path}")
                                    break
                                except:
                                    continue
                except Exception as e:
                    logger.debug(f"Búsqueda en branding/ no disponible: {e}")
            
            if logo_img is None:
                logger.warning(f"✗ No se pudo cargar el logo ({origen}) desde ninguna fuente. name={getattr(logo_field, 'name', 'N/A')}, url={getattr(logo_field, 'url', 'N/A')}")
                continue
            
            # Redimensionar logo manteniendo aspecto (máx 300x300 para mejor calidad)
            # Usar LANCZOS para mejor calidad de redimensionamiento
            original_size = logo_img.size
            # No redimensionar si es menor a 300px, mantener calidad original
            max_size = 300
            if original_size[0] > max_size or original_size[1] > max_size:
                logo_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if logo_img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', logo_img.size, (255, 255, 255))
                if logo_img.mode == 'P':
                    logo_img = logo_img.convert('RGBA')
                rgb_img.paste(logo_img, mask=logo_img.split()[-1] if logo_img.mode in ('RGBA', 'LA') else None)
                logo_img = rgb_img
            
            # Guardar a archivo temporal para ReportLab con máxima calidad
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                # Guardar con máxima calidad (sin compresión)
                logo_img.save(tmp_file.name, format="PNG", optimize=False, compress_level=0)
                tmp_path = tmp_file.name
            
            try:
                # Obtener dimensiones reales del logo
                logo_width, logo_height = logo_img.size
                # Dibujar logo un poco más grande y centrado (hasta 140x140)
                max_logo_size = 140
                if logo_width > max_logo_size or logo_height > max_logo_size:
                    # Mantener proporción
                    ratio = min(max_logo_size / logo_width, max_logo_size / logo_height)
                    logo_width = int(logo_width * ratio)
                    logo_height = int(logo_height * ratio)
                
                # Centrar el logo horizontalmente
                logo_x = (width - logo_width) / 2
                
                # Mover el logo un poco más arriba (reducir el espacio superior)
                y_logo = y - logo_height - 5  # 5px menos de espacio arriba
                
                # Dibujar con preserveAspectRatio para mantener calidad
                c.drawImage(tmp_path, logo_x, y_logo, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
                logo_dibujado = True
                y = y_logo - 10  # Ajustar y para el siguiente elemento
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
    
    # Nombre de la tienda (solo si no hay logo)
    nombre_tienda = config_tienda.nombre_tienda or config_sistema.nombre_comercial or "ImportStore"
    if not logo_dibujado:
        c.setFont("Helvetica-Bold", 24)
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
    
    # Nota interna se mostrará más abajo, después del método de pago
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
        # Si es producto varios, mostrar el nombre que el usuario ingresó
        if not detalle.variante:
            # Producto varios - la descripción ya tiene el nombre que el usuario ingresó
            desc = detalle.descripcion or "Producto varios"
            if len(desc) > 50:
                desc = desc[:50] + "..."
            # Mostrar solo el nombre ingresado, sin agregar "(Producto varios)"
            desc_display = desc
        else:
            desc = detalle.descripcion[:50] + "..." if len(detalle.descripcion) > 50 else detalle.descripcion
            desc_display = desc
        c.drawString(margin, y, desc_display)
        
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
            # Calcular el precio convertido correctamente
            precio_convertido = detalle.precio_unitario_usd_original * detalle.tipo_cambio_usado
            conversion_text = f"US${detalle.precio_unitario_usd_original:.2f} × {detalle.tipo_cambio_usado:.2f} = ${precio_convertido:,.2f}"
            c.setFont("Helvetica", 7)
            c.setFillColor(colors.grey)
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
        
        # Mostrar precio unitario: USD si tiene conversión, ARS si no
        if detalle.precio_unitario_usd_original and detalle.tipo_cambio_usado:
            precio_unitario_text = f"US${detalle.precio_unitario_usd_original:.2f}"
        else:
            precio_unitario_text = f"${detalle.precio_unitario_ars_congelado:,.2f}"
        c.drawRightString(margin + content_width * 0.80, y, precio_unitario_text)
        # Mostrar precio final después del descuento (siempre en ARS)
        if tiene_descuento:
            c.setFillColor(colors.darkgreen)
            c.drawRightString(width - margin, y, f"${detalle.subtotal_ars:,.2f}")
            c.setFillColor(colors.black)
        else:
            c.drawRightString(width - margin, y, f"${detalle.subtotal_ars:,.2f}")
        
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
    c.drawRightString(width - margin, y, f"Subtotal: ${venta.subtotal_ars:,.2f}")
    y -= 14

    if venta.descuento_total_ars > 0:
        c.setFillColor(colors.darkgreen)
        c.drawRightString(width - margin, y, f"Descuentos: -${venta.descuento_total_ars:,.2f}")
        c.setFillColor(colors.black)
        y -= 14

    if venta.impuestos_ars > 0:
        c.drawRightString(width - margin, y, f"Impuestos: ${venta.impuestos_ars:,.2f}")
        y -= 14

    y -= 5
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.line(margin, y, width - margin, y)
    y -= 15

    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width - margin, y, f"TOTAL: ${venta.total_ars:,.2f}")
    y -= 20

    # Método de pago (simple o mixto)
    c.setFont("Helvetica", 9)
    if venta.es_pago_mixto and venta.metodo_pago_2:
        # Pago mixto
        metodo_pago_1_display = dict(Venta.MetodoPago.choices).get(venta.metodo_pago, venta.metodo_pago)
        metodo_pago_2_display = dict(Venta.MetodoPago.choices).get(venta.metodo_pago_2, venta.metodo_pago_2)
        c.drawString(margin, y, f"Pago mixto:")
        y -= 14
        c.drawString(margin + 10, y, f"• {metodo_pago_1_display}: ${venta.monto_pago_1:,.2f}")
        y -= 14
        c.drawString(margin + 10, y, f"• {metodo_pago_2_display}: ${venta.monto_pago_2:,.2f}")
        y -= 14
        c.drawString(margin + 10, y, f"Total: ${venta.total_ars:,.2f}")
    else:
        # Pago simple
        metodo_pago_display = dict(Venta.MetodoPago.choices).get(venta.metodo_pago, venta.metodo_pago)
        c.drawString(margin, y, f"Método de pago: {metodo_pago_display}")
    y -= 20
    
    # Nota interna (si existe)
    if venta.nota:
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        # Dividir la nota en líneas si es muy larga
        nota_lines = []
        words = venta.nota.split()
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if c.stringWidth(test_line, "Helvetica-Oblique", 9) < content_width - 20:
                current_line = test_line
            else:
                if current_line:
                    nota_lines.append(current_line)
                current_line = word
        if current_line:
            nota_lines.append(current_line)
        
        c.drawString(margin, y, "Nota interna:")
        y -= 12
        for line in nota_lines[:5]:  # Máximo 5 líneas
            c.drawString(margin + 10, y, line)
            y -= 12
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        y -= 10

    # ========== LOCALES / PUNTOS DE RETIRO ==========
    if locales:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "Locales / Puntos de retiro:")
        y -= 15
        c.setFont("Helvetica", 9)
        for local in locales[:5]:  # Máximo 5 locales
            if y < 100:
                c.showPage()
                y = height - margin - 40
                c.setFont("Helvetica", 9)
            
            local_text = f"• {local.nombre}"
            if local.direccion:
                local_text += f": {local.direccion}"
            c.drawString(margin + 10, y, local_text)
            y -= 14
        y -= 10
    else:
        # Si no hay locales configurados, mostrar información de la tienda
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "Punto de retiro:")
        y -= 15
        c.setFont("Helvetica", 9)
        punto_retiro = nombre_tienda
        if direccion:
            punto_retiro += f": {direccion}"
        c.drawString(margin + 10, y, f"• {punto_retiro}")
        y -= 20

    # Guardar la posición Y después de los locales
    y_despues_locales = y

    # ========== GARANTÍAS POR PRODUCTO ==========
    # Calcular posición dinámica para la garantía basándose en el contenido anterior
    # Asegurar un mínimo de espacio desde los locales (mínimo 30 puntos)
    # Pero también asegurar que no esté demasiado abajo (mínimo 200 puntos desde el fondo)
    y_garantia_minima = 200  # Mínimo desde el fondo de la página
    y_garantia_calculada = min(y_despues_locales - 30, height - margin - y_garantia_minima)
    
    # Si la posición calculada es muy baja, crear una nueva página
    if y_garantia_calculada < 150:
        c.showPage()
        y = height - margin - 40
        y_garantia_calculada = y - 30
    
    y = y_garantia_calculada
    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.5)
    c.line(margin, y, width - margin, y)
    y -= 20
    
    # Guardar posición Y inicial para garantía
    garantia_y_start = y
    
    # Calcular garantías para cada producto
    garantias_productos = []
    fecha_venta = timezone.localtime(venta.fecha).date()
    garantia_general = config_tienda.garantia_dias_general if config_tienda else 45
    
    for detalle in detalles:
        if not detalle.variante:
            # Producto varios - usar garantía general
            dias_garantia = garantia_general
            nombre_producto = detalle.descripcion
        else:
            # Producto del catálogo - verificar garantía de categoría
            categoria = detalle.variante.producto.categoria
            if categoria and categoria.garantia_dias:
                dias_garantia = categoria.garantia_dias
            else:
                dias_garantia = garantia_general
            nombre_producto = detalle.descripcion
        
        from datetime import timedelta
        fecha_vencimiento = fecha_venta + timedelta(days=dias_garantia)
        garantias_productos.append({
            'nombre': nombre_producto,
            'dias': dias_garantia,
            'fecha_vencimiento': fecha_vencimiento
        })
    
    # Verificar si todos tienen la misma garantía
    garantias_unicas = set(g['dias'] for g in garantias_productos)
    todas_iguales = len(garantias_unicas) == 1
    
    # Texto de garantía a la izquierda
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.black)
    garantia_y = garantia_y_start
    
    if todas_iguales:
        # Todos tienen la misma garantía - mostrar texto general
        dias = garantias_productos[0]['dias']
        fecha_venc = garantias_productos[0]['fecha_vencimiento']
        garantia_text = f"GARANTÍA: Estos productos tienen {dias} días de garantía. Válida hasta el {fecha_venc.strftime('%d/%m/%Y')}. Para hacer uso de la garantía, traiga este comprobante."
    else:
        # Diferentes garantías - mostrar texto general primero
        garantia_text = f"GARANTÍA: Los productos tienen diferentes períodos de garantía según se detalla a continuación. Para hacer uso de la garantía, traiga este comprobante."
    
    # Dividir en líneas si es muy largo
    garantia_lines = []
    words = garantia_text.split()
    current_line = ""
    max_width = content_width * 0.6  # 60% del ancho para dejar espacio al QR
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if c.stringWidth(test_line, "Helvetica-Bold", 9) < max_width:
            current_line = test_line
        else:
            if current_line:
                garantia_lines.append(current_line)
            current_line = word
    if current_line:
        garantia_lines.append(current_line)
    
    # Calcular altura total del texto de garantía ANTES de dibujarlo
    altura_total_garantia = len(garantia_lines) * 11  # 11 puntos por línea
    
    # Si hay diferentes garantías, calcular altura adicional
    if not todas_iguales:
        altura_total_garantia += 5  # Espacio antes de los detalles
        for garantia in garantias_productos:
            garantia_detalle = f"• {garantia['nombre'][:40]}: {garantia['dias']} días (válida hasta {garantia['fecha_vencimiento'].strftime('%d/%m/%Y')})"
            if c.stringWidth(garantia_detalle, "Helvetica", 8) > max_width:
                altura_total_garantia += 18  # 2 líneas
            else:
                altura_total_garantia += 10  # 1 línea
    
    # Calcular altura del subtítulo
    garantia_subtext = "En caso de tener algún problema, escanee el código QR al final de este comprobante."
    sub_lines = []
    current_sub = ""
    for word in garantia_subtext.split():
        test_sub = current_sub + (" " if current_sub else "") + word
        if c.stringWidth(test_sub, "Helvetica", 8) < max_width:
            current_sub = test_sub
        else:
            if current_sub:
                sub_lines.append(current_sub)
            current_sub = word
    if current_sub:
        sub_lines.append(current_sub)
    
    altura_total_garantia += 5  # Espacio antes del subtítulo
    altura_total_garantia += len(sub_lines) * 10  # 10 puntos por línea del subtítulo
    
    # Ahora dibujar el texto de garantía
    for line in garantia_lines:
        c.drawString(margin, garantia_y, line)
        garantia_y -= 11
    
    # Si hay diferentes garantías, mostrar detalle por producto
    if not todas_iguales:
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        garantia_y -= 5
        for garantia in garantias_productos:
            garantia_detalle = f"• {garantia['nombre'][:40]}: {garantia['dias']} días (válida hasta {garantia['fecha_vencimiento'].strftime('%d/%m/%Y')})"
            # Dividir si es muy largo
            if c.stringWidth(garantia_detalle, "Helvetica", 8) > max_width:
                partes = garantia_detalle.split(':')
                if len(partes) == 2:
                    c.drawString(margin + 5, garantia_y, partes[0] + ':')
                    garantia_y -= 9
                    c.drawString(margin + 10, garantia_y, partes[1])
                else:
                    c.drawString(margin + 5, garantia_y, garantia_detalle)
            else:
                c.drawString(margin + 5, garantia_y, garantia_detalle)
            garantia_y -= 10
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    garantia_y -= 5
    for line in sub_lines:
        c.drawString(margin, garantia_y, line)
        garantia_y -= 10
    
    # Guardar la posición Y final del texto de garantía
    garantia_y_final = garantia_y
    
    # QR a la derecha
    telefono_whatsapp = telefono or config_tienda.telefono_contacto or config_sistema.whatsapp_numero
    qr_y = None
    qr_size = 80
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
                    qr_size = 80  # Tamaño más pequeño para que quepa a la derecha
                    qr_x = width - margin - qr_size  # A la derecha
                    
                    # Calcular la posición Y del QR
                    # Intentar alinearlo con el inicio de la sección de garantía
                    qr_y = garantia_y_start - qr_size - 10
                    
                    # Verificar si el QR se superpone con el texto de garantía
                    # El texto de garantía va desde garantia_y_start (más alto) hasta garantia_y_final (más bajo)
                    # El QR ocupa desde qr_y (más alto) hasta qr_y + qr_size (más bajo)
                    # Hay superposición si: qr_y < garantia_y_start Y qr_y + qr_size > garantia_y_final
                    # O si el QR está completamente dentro del área del texto
                    qr_top = qr_y
                    qr_bottom = qr_y + qr_size
                    texto_top = garantia_y_start
                    texto_bottom = garantia_y_final
                    
                    # Verificar superposición: si el QR se cruza con el área del texto
                    if not (qr_bottom < texto_bottom or qr_top > texto_top):
                        # Hay superposición, mover el QR más arriba (por encima del texto)
                        # Dejar un margen de 20 puntos entre el QR y el texto
                        qr_y = texto_top - qr_size - 20
                    
                    # Asegurar que el QR no esté demasiado abajo (mínimo 50 puntos desde el fondo)
                    if qr_y < 50:
                        # Si el QR está muy abajo, moverlo más arriba
                        qr_y = max(50, garantia_y_start - qr_size - 10)
                    
                    # Fondo blanco para el QR
                    c.setFillColor(colors.white)
                    c.rect(qr_x - 5, qr_y - 5, qr_size + 10, qr_size + 10, fill=1, stroke=0)
                    c.setFillColor(colors.black)
                    
                    # Dibujar el QR
                    c.drawImage(tmp_qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
                    
                    # Borde alrededor del QR
                    c.setStrokeColor(colors.grey)
                    c.setLineWidth(0.5)
                    c.rect(qr_x - 5, qr_y - 5, qr_size + 10, qr_size + 10, fill=0, stroke=1)
                    
                    # Texto debajo del QR
                    c.setFont("Helvetica-Bold", 7)
                    c.setFillColor(colors.black)
                    texto_y = qr_y - 12
                    c.drawCentredString(qr_x + qr_size / 2, texto_y, "Tenga una consulta")
                    c.setFont("Helvetica", 6)
                    c.setFillColor(colors.grey)
                    c.drawCentredString(qr_x + qr_size / 2, texto_y - 9, "sobre este pedido")
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
    
    # Ajustar Y para asegurar que no se superponga con el footer
    if qr_y is not None:
        y = min(garantia_y, qr_y - qr_size - 30)
    else:
        y = garantia_y
    
    # ========== FOOTER ==========
    # Footer al final de la página
    footer_y = 40
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, footer_y, f"{nombre_tienda} - Comprobante #{venta.id}")
    c.drawCentredString(width / 2, footer_y - 10, "Gracias por su compra")

    # ========== CERTIFICADOS DE GARANTÍA PARA IPHONES ==========
    # Detectar iPhones vendidos y generar certificados de garantía
    from inventario.models import DetalleIphone
    from datetime import timedelta
    
    detalles_iphones = []
    for detalle in venta.detalles.all():
        if detalle.variante:
            # Verificar si es iPhone (categoría Celulares) - más flexible en la comparación
            categoria = detalle.variante.producto.categoria
            if categoria:
                categoria_nombre_lower = categoria.nombre.lower().strip()
                # Detectar si es iPhone (categoría "celulares" o nombre del producto contiene "iphone")
                es_iphone = (
                    categoria_nombre_lower == "celulares" or 
                    "iphone" in detalle.variante.producto.nombre.lower()
                )
                
                if es_iphone:
                    # Intentar obtener el DetalleIphone usando getattr para evitar excepciones
                    detalle_iphone = getattr(detalle.variante, 'detalle_iphone', None)
                    imei = None
                    if detalle_iphone:
                        imei = detalle_iphone.imei
                    
                    # Obtener garantía (categoría o general)
                    if categoria.garantia_dias:
                        dias_garantia = categoria.garantia_dias
                    else:
                        dias_garantia = config_tienda.garantia_dias_general if config_tienda else 45
                    
                    # Agregar el iPhone incluso si no tiene IMEI (se mostrará "No registrado")
                    detalles_iphones.append({
                        'detalle_venta': detalle,
                        'detalle_iphone': detalle_iphone,
                        'modelo': detalle.variante.producto.nombre,
                        'imei': imei or "No registrado",
                        'dias_garantia': dias_garantia,
                    })
    
    # Generar certificado de garantía para cada iPhone
    for iphone_data in detalles_iphones:
        c.showPage()
        y = height - margin - 40
        
        # Título del certificado
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.black)
        c.drawCentredString(width / 2, y, "CERTIFICADO DE GARANTÍA LIMITADA")
        y -= 40
        
        # Texto de garantía
        c.setFont("Helvetica", 10)
        fecha_compra = timezone.localtime(venta.fecha).date()
        fecha_vencimiento = fecha_compra + timedelta(days=iphone_data['dias_garantia'])
        
        texto_garantia = f"""
{nombre_tienda}, en adelante 'el Vendedor', otorga la presente garantía limitada por el término de {iphone_data['dias_garantia']} días corridos a partir de la fecha de adquisición del equipo detallado a continuación. La misma cubre exclusivamente fallas de hardware no imputables al uso indebido, maltrato, humedad, caídas, intervención de terceros o factores externos.

El equipo deberá conservar intacto su número de IMEI, coincidiendo los últimos seis (6) dígitos con los aquí consignados. Quedan expresamente excluidos de esta garantía los bloqueos por iCloud, contraseñas, cuentas Apple, problemas derivados de configuraciones de usuario, actualizaciones de software, aplicaciones de terceros, o cualquier manipulación posterior a la entrega.

Ante cualquier reclamo, el comprador deberá presentar este documento original junto con el equipo en cuestión, sin excepción. La falta de coincidencia del IMEI o la omisión de esta documentación anularán automáticamente el derecho a reclamo.

La presente garantía no implica derecho a reposición, reembolso ni sustitución automática del producto. Cualquier resolución estará sujeta a revisión técnica por parte del Vendedor.
        """.strip()
        
        # Dividir el texto en líneas y dibujarlo
        lines = []
        for paragraph in texto_garantia.split('\n\n'):
            words = paragraph.split()
            current_line = ""
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if c.stringWidth(test_line, "Helvetica", 10) < content_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            lines.append("")  # Espacio entre párrafos
        
        for line in lines:
            if y < 200:
                c.showPage()
                y = height - margin - 40
            c.drawString(margin, y, line)
            y -= 12
        
        y -= 20
        
        # Datos del producto
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "Datos del Producto:")
        y -= 30
        
        c.setFont("Helvetica", 10)
        # Modelo
        modelo_text = "Modelo:"
        c.drawString(margin, y, modelo_text)
        # Alinear el valor a la derecha con más espacio
        c.drawRightString(width - margin - 100, y, iphone_data['modelo'])
        y -= 25
        
        # IMEI (últimos 6 dígitos)
        imei_completo = iphone_data['imei']
        if imei_completo and imei_completo != "No registrado":
            ultimos_6_digitos = imei_completo[-6:] if len(imei_completo) >= 6 else imei_completo
        else:
            ultimos_6_digitos = "No registrado"
        imei_text = "Últimos 6 dígitos IMEI:"
        c.drawString(margin, y, imei_text)
        c.drawRightString(width - margin - 100, y, ultimos_6_digitos)
        y -= 25
        
        # Fecha de compra
        fecha_compra_text = "Fecha de compra:"
        c.drawString(margin, y, fecha_compra_text)
        c.drawRightString(width - margin - 100, y, fecha_compra.strftime("%d/%m/%Y"))
        y -= 25
        
        # Cliente
        cliente_text = "Cliente:"
        c.drawString(margin, y, cliente_text)
        cliente_nombre = venta.cliente_nombre or (venta.cliente.nombre if venta.cliente else "Consumidor Final")
        c.drawRightString(width - margin - 100, y, cliente_nombre)
        y -= 25
        
        # Fecha de vencimiento de garantía
        fecha_venc_text = "Garantía válida hasta:"
        c.drawString(margin, y, fecha_venc_text)
        c.drawRightString(width - margin - 100, y, fecha_vencimiento.strftime("%d/%m/%Y"))
        y -= 50
        
        # Línea separadora
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(margin, y, width - margin, y)
        y -= 30
        
        # Firma y DNI del cliente
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, "Fecha: " + fecha_compra.strftime("%d/%m/%Y"))
        y -= 25
        c.drawString(margin, y, "Firma y DNI:")
        y -= 30
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.line(margin, y, margin + 200, y)
        y -= 40
        
        # Firma del gerente
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, f"{nombre_tienda} – Gerente")
        y -= 15
        # Por ahora usar un valor por defecto, se puede agregar a ConfiguracionTienda después
        gerente_nombre = "RAUL EMANUEL SOSA"  # TODO: Agregar campo gerente_nombre a ConfiguracionTienda
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, gerente_nombre)
        y -= 20
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.line(margin, y, margin + 200, y)

    c.save()
    buffer.seek(0)
    filename = f"comprobante_{venta.id}.pdf"
    return ContentFile(buffer.read(), name=filename)
