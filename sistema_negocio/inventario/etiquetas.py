"""Generador de etiquetas PDF para productos."""

import logging
import os
import tempfile
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import qrcode
from reportlab.graphics.barcode import qr as reportlab_qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader

logger = logging.getLogger(__name__)


def generar_etiqueta_pdf(variantes, etiquetas_por_fila=3, etiquetas_por_columna=8):
    """
    Genera un PDF con etiquetas de productos.
    
    Args:
        variantes: Lista de ProductoVariante
        etiquetas_por_fila: Número de etiquetas por fila (default: 3)
        etiquetas_por_columna: Número de etiquetas por columna (default: 8)
    
    Returns:
        ContentFile con el PDF generado
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Dimensiones de cada etiqueta (3x8 en A4)
    etiqueta_width = width / etiquetas_por_fila
    etiqueta_height = height / etiquetas_por_columna
    
    # Margen interno de cada etiqueta (más pequeño para aprovechar mejor el espacio)
    margin = 2 * mm
    
    variante_index = 0
    total_variantes = len(variantes)
    
    # Generar múltiples páginas si es necesario
    while variante_index < total_variantes:
        # Nueva página
        if variante_index > 0:
            c.showPage()
        
        # Dibujar etiquetas en esta página
        for row in range(etiquetas_por_columna):
            for col in range(etiquetas_por_fila):
                if variante_index >= total_variantes:
                    break
                
                variante = variantes[variante_index]
                
                # Calcular posición de la etiqueta
                x = col * etiqueta_width + margin
                y = height - (row + 1) * etiqueta_height + margin
                
                # Dibujar borde de la etiqueta
                c.setStrokeColor(colors.grey)
                c.setLineWidth(0.5)
                c.rect(
                    col * etiqueta_width,
                    height - (row + 1) * etiqueta_height,
                    etiqueta_width,
                    etiqueta_height,
                    stroke=1,
                    fill=0
                )
                
                # Dibujar contenido de la etiqueta
                _dibujar_etiqueta(c, variante, x, y, etiqueta_width - 2 * margin, etiqueta_height - 2 * margin)
                
                variante_index += 1
            
            if variante_index >= total_variantes:
                break
        
        if variante_index >= total_variantes:
            break
    
    c.save()
    buffer.seek(0)
    return ContentFile(buffer.read(), name="etiquetas.pdf")


def _dibujar_etiqueta(canvas_obj, variante, x, y, width, height):
    """Dibuja el contenido de una etiqueta individual estilo Apple - minimalista y profesional."""
    from inventario.models import Precio
    
    # Obtener precios
    precio_minorista_ars = variante.precios.filter(
        tipo=Precio.Tipo.MINORISTA,
        moneda=Precio.Moneda.ARS,
        activo=True
    ).first()
    
    precio_minorista_usd = variante.precios.filter(
        tipo=Precio.Tipo.MINORISTA,
        moneda=Precio.Moneda.USD,
        activo=True
    ).first()
    
    # Fondo blanco puro (estilo Apple)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.rect(x, y, width, height, fill=1, stroke=0)
    
    # Margen general
    margin = 4
    content_x = x + margin
    content_y = y + margin
    content_width = width - (margin * 2)
    content_height = height - (margin * 2)
    
    # ========== SECCIÓN SUPERIOR: NOMBRE DEL PRODUCTO ==========
    nombre = variante.producto.nombre
    if variante.nombre_variante and variante.nombre_variante.strip() and variante.nombre_variante.lower() != "único":
        nombre = f"{nombre} {variante.nombre_variante}"
    
    # Nombre del producto - tipografía grande, negrita, estilo Apple
    nombre_font_size = 12
    canvas_obj.setFont("Helvetica-Bold", nombre_font_size)
    canvas_obj.setFillColor(colors.HexColor("#1d1d1f"))  # Negro suave estilo Apple
    
    # Dividir nombre en líneas si es necesario
    max_nombre_width = content_width - 8
    nombre_lines = []
    words = nombre.split()
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}" if current_line else word
        if canvas_obj.stringWidth(test_line, "Helvetica-Bold", nombre_font_size) < max_nombre_width:
            current_line = test_line
        else:
            if current_line:
                nombre_lines.append(current_line)
            current_line = word
    if current_line:
        nombre_lines.append(current_line)
    
    # Dibujar nombre (máximo 2 líneas)
    nombre_y = content_y + content_height - 6
    for i, line in enumerate(nombre_lines[:2]):
        canvas_obj.drawString(content_x, nombre_y - (i * 14), line)
    
    # ========== SECCIÓN MEDIA: ATRIBUTOS Y DESCRIPCIÓN ==========
    descripcion = variante.atributos_display if variante.atributos_display else ""
    info_y = nombre_y - (len(nombre_lines[:2]) * 14) - 8
    
    if descripcion:
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.setFillColor(colors.HexColor("#6e6e73"))  # Gris suave estilo Apple
        # Truncar descripción si es muy larga
        max_desc_width = content_width - 8
        if canvas_obj.stringWidth(descripcion, "Helvetica", 7) > max_desc_width:
            while canvas_obj.stringWidth(descripcion + "...", "Helvetica", 7) > max_desc_width and len(descripcion) > 0:
                descripcion = descripcion[:-1]
            descripcion = descripcion + "..."
        canvas_obj.drawString(content_x, info_y, descripcion)
        info_y -= 10
    else:
        info_y -= 6
    
    # ========== SECCIÓN PRECIO: DISEÑO MINIMALISTA ESTILO APPLE ==========
    precio_y = info_y - 4
    
    if precio_minorista_ars:
        precio_valor = float(precio_minorista_ars.precio)
        # Formatear precio estilo Apple (sin decimales si es entero, con decimales si no)
        if precio_valor == int(precio_valor):
            precio_formateado = f"${int(precio_valor):,}".replace(",", ".")
        else:
            precio_formateado = f"${precio_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Precio principal - tipografía grande, negrita, color negro
        precio_font_size = 18
        canvas_obj.setFont("Helvetica-Bold", precio_font_size)
        canvas_obj.setFillColor(colors.HexColor("#1d1d1f"))
        
        # Ajustar tamaño si es muy largo (dejar espacio para QR a la derecha)
        precio_text_width = canvas_obj.stringWidth(precio_formateado, "Helvetica-Bold", precio_font_size)
        max_precio_width = content_width - 70  # Dejar espacio para QR (65px + margen)
        if precio_text_width > max_precio_width:
            precio_font_size = int(precio_font_size * (max_precio_width / precio_text_width))
            canvas_obj.setFont("Helvetica-Bold", precio_font_size)
        
        canvas_obj.drawString(content_x, precio_y, precio_formateado)
    else:
        # Sin precio - texto discreto
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(colors.HexColor("#86868b"))
        canvas_obj.drawString(content_x, precio_y, "Sin precio")
    
    # ========== SECCIÓN INFERIOR DERECHA: QR CODE Y SKU ==========
    # QR Code - posición inferior derecha, tamaño más grande para fácil escaneo
    qr_size = min(65, content_width * 0.45)  # Más grande, máximo 65px
    qr_size = max(qr_size, 50)  # Mínimo 50px para asegurar escaneo fácil
    
    # Posicionar QR a la derecha
    qr_x = (x + width) - margin - qr_size
    qr_y = content_y + 4
    
    # Generar QR code - asegurar que siempre se genere
    qr_data = variante.sku or variante.codigo_barras or str(variante.id)
    if not qr_data:
        # Si no hay SKU ni código de barras, usar el ID de la variante
        qr_data = f"VAR-{variante.id}"
    
    try:
        # Aumentar box_size para mejor calidad de escaneo
        qr = qrcode.QRCode(version=2, box_size=4, border=2)
        qr.add_data(str(qr_data))
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#1d1d1f", back_color="white").convert("RGB")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            qr_img.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            canvas_obj.drawImage(tmp_path, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=True)
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        logger.error(f"Error al generar QR para {variante.sku}: {e}")
        # Si falla, intentar generar un QR básico con el ID
        try:
            qr_data_fallback = f"VAR-{variante.id}"
            qr = qrcode.QRCode(version=1, box_size=4, border=2)
            qr.add_data(qr_data_fallback)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#1d1d1f", back_color="white").convert("RGB")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                qr_img.save(tmp_file.name)
                tmp_path = tmp_file.name
            canvas_obj.drawImage(tmp_path, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=True)
            os.unlink(tmp_path)
        except Exception as e2:
            logger.error(f"Error al generar QR de respaldo: {e2}")
    
    # SKU debajo del QR - tipografía pequeña, monospace, gris, centrado
    identificador = variante.codigo_barras if variante.codigo_barras else (variante.sku or f"VAR-{variante.id}")
    canvas_obj.setFont("Courier", 5)
    canvas_obj.setFillColor(colors.HexColor("#86868b"))
    id_text = str(identificador)[:18]  # Limitar longitud
    id_text_width = canvas_obj.stringWidth(id_text, "Courier", 5)
    id_x = qr_x + (qr_size / 2) - (id_text_width / 2)  # Centrar debajo del QR
    canvas_obj.drawString(id_x, qr_y - 8, id_text)
    
    # ========== GARANTÍA: ESTILO DISCRETO (IZQUIERDA) ==========
    from configuracion.models import ConfiguracionTienda
    config_tienda = ConfiguracionTienda.obtener_unica()
    garantia_general = config_tienda.garantia_dias_general if config_tienda else 45
    
    dias_garantia = garantia_general
    if variante.producto.categoria and variante.producto.categoria.garantia_dias:
        dias_garantia = variante.producto.categoria.garantia_dias
    
    garantia_text = f"{dias_garantia} días de garantía"
    canvas_obj.setFont("Helvetica", 5.5)
    canvas_obj.setFillColor(colors.HexColor("#86868b"))
    garantia_y = content_y + 2
    garantia_x = content_x  # A la izquierda, no compite con el QR
    canvas_obj.drawString(garantia_x, garantia_y, garantia_text)
    
    # ========== LÍNEA DIVISORIA SUTIL (OPCIONAL) ==========
    # Línea horizontal muy sutil separando secciones (estilo Apple)
    line_y = precio_y - 12
    if line_y > content_y + 10:
        canvas_obj.setStrokeColor(colors.HexColor("#d2d2d7"))  # Gris muy claro
        canvas_obj.setLineWidth(0.3)
        canvas_obj.line(content_x, line_y, x + width - margin, line_y)


def generar_etiqueta_individual_pdf(variante):
    """Genera un PDF con una sola etiqueta (más grande, tamaño estándar de etiqueta)."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Para etiqueta individual, usar un tamaño razonable (ej: 10cm x 6cm)
    # pero centrado en la página A4
    etiqueta_width = 100 * mm  # 10cm
    etiqueta_height = 60 * mm  # 6cm
    
    # Centrar en la página
    x = (width - etiqueta_width) / 2
    y = (height - etiqueta_height) / 2
    
    # Dibujar borde de la etiqueta más sutil
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.setLineWidth(1)
    c.setDash([3, 2])  # Línea punteada
    c.rect(x, y, etiqueta_width, etiqueta_height, stroke=1, fill=0)
    c.setDash([])  # Volver a línea sólida
    
    # Dibujar contenido de la etiqueta
    _dibujar_etiqueta(c, variante, x, y, etiqueta_width, etiqueta_height)
    
    c.save()
    buffer.seek(0)
    return buffer  # Retornar BytesIO directamente


def generar_etiqueta(buffer, detalle_iphone):
    """
    Genera una etiqueta térmica profesional (50mm x 30mm) para un iPhone específico.
    
    Args:
        buffer (BytesIO): Buffer sobre el que se escribirá el PDF.
        detalle_iphone (DetalleIphone): Instancia con información del iPhone.
    """
    page_width_mm = 50
    page_height_mm = 30
    page_width = page_width_mm * mm
    page_height = page_height_mm * mm
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    def mm_to_pt(value_mm: float) -> float:
        return value_mm * 72 / 25.4

    def y_from_bottom(y_mm: float) -> float:
        return mm_to_pt(y_mm)

    # Fondo blanco
    c.setFillColor(colors.white)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    from configuracion.models import ConfiguracionTienda

    variante = detalle_iphone.variante
    producto = variante.producto if variante else None

    modelo = (producto.nombre if producto else "iPhone").strip()
    capacidad = (variante.atributo_1 or "").strip()
    color = (variante.atributo_2 or "").strip()
    color_text = color.title() if color else ""
    bateria = detalle_iphone.salud_bateria
    bateria_text = f"{int(bateria)}%" if bateria is not None else "—"
    imei = (detalle_iphone.imei or "SIN IMEI").strip()
    sku = (variante.sku or "SKU").strip()
    sku_for_qr = sku.replace(" ", "")

    # Configuración de columnas y medidas
    left_x_mm = 2
    right_margin_mm = 2
    gap_mm = 1.2
    qr_size_mm = 17
    qr_x_mm = 32
    qr_y_mm = 6
    left_width_mm = qr_x_mm - gap_mm - left_x_mm
    left_x_pt = mm_to_pt(left_x_mm)
    left_width_pt = mm_to_pt(left_width_mm)

    # Header shrink-to-fit
    header_font_name = "Helvetica-Bold"
    header_font_size = 14  # pt
    max_header_width_pt = mm_to_pt(left_width_mm)
    while header_font_size > 6 and c.stringWidth(modelo, header_font_name, header_font_size) > max_header_width_pt:
        header_font_size -= 0.5
    c.setFont(header_font_name, header_font_size)
    c.setFillColor(colors.black)
    c.drawString(left_x_pt, y_from_bottom(24), modelo)

    # Subheader (GB - Color) with wrapping if needed
    subtitle = " - ".join(part for part in [capacidad, color_text] if part)
    if subtitle:
        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.HexColor("#333333"))
        text_obj = c.beginText()
        text_obj.setTextOrigin(left_x_pt, y_from_bottom(19))
        text_obj.setLeading(mm_to_pt(3.4))
        available_width = max_header_width_pt
        words = subtitle.split()
        line = ""
        for word in words:
            candidate = word if not line else f"{line} {word}"
            if c.stringWidth(candidate, "Helvetica", 8.5) <= available_width:
                line = candidate
            else:
                text_obj.textLine(line)
                line = word
        if line:
            text_obj.textLine(line)
        c.drawText(text_obj)

    # Batería
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.black)
    c.drawString(left_x_pt, y_from_bottom(12), f"Bat: {bateria_text}")

    # IMEI
    c.setFont("Helvetica", 5)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(left_x_pt, y_from_bottom(7.5), "IMEI:")
    imei_text = c.beginText()
    imei_text.setTextOrigin(left_x_pt, y_from_bottom(4.5))
    imei_text.setFont("Courier-Bold", 7)
    imei_text.setCharSpace(-0.2)
    imei_text.textLine(imei)
    c.drawText(imei_text)

    # QR utilizando QrCodeWidget
    qr_widget = reportlab_qr.QrCodeWidget(sku_for_qr)
    bounds = qr_widget.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    qr_size_pt = mm_to_pt(qr_size_mm)
    drawing = Drawing(qr_size_pt, qr_size_pt, transform=[qr_size_pt / qr_width, 0, 0, qr_size_pt / qr_height, 0, 0])
    drawing.add(qr_widget)
    renderPDF.draw(drawing, c, mm_to_pt(qr_x_mm), y_from_bottom(qr_y_mm))

    # Logo sobre el QR
    logo_reader = None
    logo_max_height_mm = 5
    config_tienda = ConfiguracionTienda.obtener_unica()
    if config_tienda and getattr(config_tienda, "logo", None):
        try:
            logo_data = None
            if hasattr(config_tienda.logo, "path") and config_tienda.logo.path and os.path.exists(config_tienda.logo.path):
                with open(config_tienda.logo.path, "rb") as logo_file:
                    logo_data = logo_file.read()
            else:
                with config_tienda.logo.open("rb") as logo_file:
                    logo_data = logo_file.read()
            if logo_data:
                logo_reader = ImageReader(BytesIO(logo_data))
        except Exception:
            logger.exception("No se pudo cargar el logo para la etiqueta del iPhone")
            logo_reader = None

    if logo_reader:
        logo_w_pt, logo_h_pt = logo_reader.getSize()
        target_w_pt = mm_to_pt(qr_size_mm)
        target_h_pt = mm_to_pt(logo_max_height_mm)
        scale = min(target_w_pt / logo_w_pt, target_h_pt / logo_h_pt)
        draw_w = logo_w_pt * scale
        draw_h = logo_h_pt * scale
        logo_x = mm_to_pt(qr_x_mm) + (target_w_pt - draw_w) / 2
        logo_y = y_from_bottom(qr_y_mm + qr_size_mm + 1)
        top_limit = page_height - mm_to_pt(1)
        if logo_y + draw_h > top_limit:
            logo_y = top_limit - draw_h
        c.drawImage(logo_reader, logo_x, logo_y, width=draw_w, height=draw_h, mask="auto")

    # SKU en el pie (centrado, 4 pt aprox)
    sku_display = sku
    if sku_display.upper().startswith("IPHONE-"):
        sku_display = sku_display[7:]
    sku_font = "Helvetica"
    sku_font_size = 4  # pt
    max_width_pt = page_width - mm_to_pt(4)
    while c.stringWidth(sku_display, sku_font, sku_font_size) > max_width_pt and sku_font_size > 3:
        sku_font_size -= 0.2
    if c.stringWidth(sku_display, sku_font, sku_font_size) > max_width_pt:
        # Recortar desde el inicio manteniendo sufijo distintivo
        while c.stringWidth(sku_display, sku_font, sku_font_size) > max_width_pt and len(sku_display) > 6:
            sku_display = sku_display[1:]
    c.setFont(sku_font, sku_font_size)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(page_width / 2, y_from_bottom(1.5), f"SKU: {sku_display}")

    c.showPage()
    c.save()
    buffer.seek(0)