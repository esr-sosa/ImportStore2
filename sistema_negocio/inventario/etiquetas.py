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
    """Dibuja el contenido de una etiqueta individual mejorada estilo referencia."""
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
    
    # Fondo blanco
    canvas_obj.setFillColor(colors.white)
    canvas_obj.rect(x, y, width, height, fill=1, stroke=0)
    
    # Calcular división: ~40% izquierda (QR), 60% derecha (info)
    division_x = x + (width * 0.40)
    
    # Línea vertical divisoria roja (estilo referencia)
    canvas_obj.setStrokeColor(colors.HexColor("#dc2626"))  # Rojo
    canvas_obj.setLineWidth(2)
    canvas_obj.line(division_x, y, division_x, y + height)
    
    # ========== SECCIÓN IZQUIERDA (QR) ==========
    left_width = division_x - x
    left_center_x = x + (left_width / 2)
    
    # Texto pequeño arriba (como "Gran Bretaña" en la referencia)
    if variante.producto.categoria:
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.setFillColor(colors.black)
        categoria_text = variante.producto.categoria.nombre[:20]  # Limitar longitud
        categoria_width = canvas_obj.stringWidth(categoria_text, "Helvetica", 6)
        canvas_obj.drawCentredString(left_center_x, y + height - 10, categoria_text)
    
    # QR Code (centrado en la sección izquierda) - MÁS GRANDE
    qr_size = min(left_width * 0.82, height * 0.72, 78)  # Mayor presencia visual
    qr_x = left_center_x - (qr_size / 2)
    qr_y = y + (height / 2) - (qr_size / 2) + 4  # Centrado vertical con pequeño offset
    
    # Generar QR code
    qr_data = variante.sku
    try:
        qr = qrcode.QRCode(version=2, box_size=4, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert("RGB")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            qr_img.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            canvas_obj.drawImage(tmp_path, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=True)
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        logger.error(f"Error al generar QR para {variante.sku}: {e}")
    
    # SKU o código de barras abajo (como "1234567890" en la referencia)
    identificador = variante.codigo_barras if variante.codigo_barras else variante.sku
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.setFillColor(colors.black)
    id_text = str(identificador)[:15]  # Limitar longitud
    id_width = canvas_obj.stringWidth(id_text, "Helvetica", 6)
    canvas_obj.drawCentredString(left_center_x, y + 8, id_text)
    
    # ========== SECCIÓN DERECHA (INFO DEL PRODUCTO) ==========
    right_x = division_x + 5  # Pequeño margen después de la línea
    right_width = width - (right_x - x)
    right_y_start = y + height - 8
    
    # Nombre del producto (grande y destacado)
    nombre = variante.producto.nombre
    if variante.nombre_variante and variante.nombre_variante.strip() and variante.nombre_variante.lower() != "único":
        nombre = f"{nombre} {variante.nombre_variante}"
    
    # Atributos como descripción
    descripcion = variante.atributos_display if variante.atributos_display else ""
    
    # Nombre del producto (fuente grande, negrita)
    canvas_obj.setFont("Helvetica-Bold", 11)
    canvas_obj.setFillColor(colors.black)
    
    # Dividir nombre en líneas si es necesario
    max_nombre_width = right_width - 10
    nombre_lines = []
    words = nombre.split()
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}" if current_line else word
        if canvas_obj.stringWidth(test_line, "Helvetica-Bold", 11) < max_nombre_width:
            current_line = test_line
        else:
            if current_line:
                nombre_lines.append(current_line)
            current_line = word
    if current_line:
        nombre_lines.append(current_line)
    
    # Dibujar nombre (máximo 2 líneas)
    nombre_y = right_y_start
    for i, line in enumerate(nombre_lines[:2]):
        canvas_obj.drawString(right_x, nombre_y - (i * 13), line)
    
    # Cursor vertical para ir ubicando elementos
    info_cursor = nombre_y - (len(nombre_lines[:2]) * 13) - 6

    # Descripción (atributos) inmediatamente debajo del nombre
    if descripcion:
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.black)
        desc_y = info_cursor - 6
        # Truncar descripción si es muy larga
        max_desc_width = right_width - 10
        if canvas_obj.stringWidth(descripcion, "Helvetica", 8) > max_desc_width:
            # Truncar con ellipsis
            while canvas_obj.stringWidth(descripcion + "...", "Helvetica", 8) > max_desc_width and len(descripcion) > 0:
                descripcion = descripcion[:-1]
            descripcion = descripcion + "..."
        canvas_obj.drawString(right_x, desc_y, descripcion)
        info_cursor = desc_y - 14
    else:
        info_cursor -= 12
    
    # Precio - posicionarlo más abajo para evitar superposición
    precio_y = max(info_cursor - 12, y + 22)
    
    precio_x = right_x
    precio_font_size = min(22, int(height * 0.30))

    if precio_minorista_ars:
        # Formatear precio: separar parte entera y decimal
        precio_valor = float(precio_minorista_ars.precio)
        precio_formateado = f"${precio_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Etiqueta de precio más prominente con diseño profesional
        precio_tag_padding_x = 8
        precio_tag_padding_y = 5
        canvas_obj.setFont("Helvetica-Bold", precio_font_size)
        precio_text_width = canvas_obj.stringWidth(precio_formateado, "Helvetica-Bold", precio_font_size)
        
        # Calcular ancho máximo disponible para el recuadro del precio
        # Espacio desde right_x hasta el borde derecho de la etiqueta (x + width)
        espacio_disponible = (x + width) - right_x - 8  # 8px de margen del borde
        
        # Limitar el ancho del recuadro al espacio disponible
        tag_width = min(precio_text_width + (precio_tag_padding_x * 2), espacio_disponible)
        tag_height = precio_font_size + (precio_tag_padding_y * 2)
        tag_x = right_x
        tag_y = precio_y - precio_tag_padding_y
        
        # Sombra suave
        canvas_obj.setFillColor(colors.HexColor("#94a3b8"))
        canvas_obj.setStrokeColor(colors.HexColor("#94a3b8"))
        canvas_obj.setLineWidth(0.3)
        canvas_obj.roundRect(tag_x + 1, tag_y - 1, tag_width + 2, tag_height + 2, 6, fill=1, stroke=0)
        
        # Contenedor principal con gradiente
        canvas_obj.setFillColor(colors.HexColor("#f8fafc"))
        canvas_obj.setStrokeColor(colors.HexColor("#cbd5e1"))
        canvas_obj.setLineWidth(1.5)
        canvas_obj.roundRect(tag_x, tag_y, tag_width + 2, tag_height + 2, 6, fill=1, stroke=1)
        
        # Texto del precio (centrado o ajustado si es muy largo)
        texto_x = tag_x + precio_tag_padding_x
        # Si el texto es más ancho que el espacio, reducir el tamaño de fuente
        if precio_text_width > (tag_width - precio_tag_padding_x * 2):
            precio_font_size_ajustado = int(precio_font_size * 0.85)
            canvas_obj.setFont("Helvetica-Bold", precio_font_size_ajustado)
            texto_x = tag_x + 4
        
        canvas_obj.setFillColor(colors.HexColor("#0f172a"))
        canvas_obj.drawString(texto_x, precio_y + (precio_font_size * 0.10), precio_formateado)
        
        # Precio USD si existe (debajo, más pequeño)
        if precio_minorista_usd:
            precio_usd_valor = float(precio_minorista_usd.precio)
            precio_texto_usd = f"USD ${precio_usd_valor:,.2f}"
            canvas_obj.setFont("Helvetica-Bold", 7)
            canvas_obj.setFillColor(colors.HexColor("#475569"))
            usd_y = tag_y - 10
            canvas_obj.drawString(tag_x + 2, usd_y, precio_texto_usd)
    else:
        # Sin precio
        canvas_obj.setFont("Helvetica-Bold", 14)
        canvas_obj.setFillColor(colors.HexColor("#ef4444"))
        canvas_obj.drawString(right_x, precio_y, "Sin precio")
        precio_font_size = 14
    
    # Garantía (abajo del precio) - más visible y profesional
    from configuracion.models import ConfiguracionTienda
    config_tienda = ConfiguracionTienda.obtener_unica()
    garantia_general = config_tienda.garantia_dias_general if config_tienda else 45
    
    # Verificar garantía de categoría
    dias_garantia = garantia_general
    if variante.producto.categoria and variante.producto.categoria.garantia_dias:
        dias_garantia = variante.producto.categoria.garantia_dias
    
    garantia_text = f"✓ Garantía {dias_garantia} días"
    canvas_obj.setFont("Helvetica-Bold", 7)
    canvas_obj.setFillColor(colors.HexColor("#10b981"))
    garantia_y = y + 14
    # Dibujar fondo para la garantía
    garantia_width = canvas_obj.stringWidth(garantia_text, "Helvetica-Bold", 7)
    # Limitar el ancho al espacio disponible
    garantia_width_max = (x + width) - right_x - 8
    garantia_width = min(garantia_width, garantia_width_max)
    canvas_obj.setFillColor(colors.HexColor("#d1fae5"))
    canvas_obj.roundRect(right_x, garantia_y - 2, garantia_width + 4, 10, 4, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor("#047857"))
    canvas_obj.drawString(right_x + 2, garantia_y, garantia_text)


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
    page_width = 50 * mm
    page_height = 30 * mm
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # Fondo
    c.setFillColor(colors.white)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    variante = detalle_iphone.variante
    producto = variante.producto if variante else None

    modelo = producto.nombre if producto else "iPhone"
    capacidad = variante.atributo_1 or ""
    header_text = f"{modelo} - {capacidad}".strip(" -")
    color_text = variante.atributo_2 if variante and variante.atributo_2 else "Sin especificar"
    bateria = detalle_iphone.salud_bateria
    bateria_text = f"{int(bateria)}%" if bateria is not None else "—"
    imei = detalle_iphone.imei or "SIN IMEI"
    sku = variante.sku if variante and variante.sku else "SKU"

    def mm_to_pt(value_mm: float) -> float:
        return value_mm * 72 / 25.4

    def svg_x(x_mm: float) -> float:
        return mm_to_pt(x_mm)

    def svg_y(y_mm: float) -> float:
        return page_height - mm_to_pt(y_mm)

    # Encabezado (tamaño base 3.8 mm, ajustar si excede anchura)
    font_size_header_mm = 3.8
    font_size_header = mm_to_pt(font_size_header_mm)
    c.setFont("Helvetica-Bold", font_size_header)
    max_header_width = svg_x(48) - svg_x(2)
    header_width = c.stringWidth(header_text, "Helvetica-Bold", font_size_header)
    if header_width > max_header_width:
        scale = max_header_width / header_width
        font_size_header *= scale
        c.setFont("Helvetica-Bold", font_size_header)
    c.setFillColor(colors.black)
    c.drawString(svg_x(2), svg_y(6), header_text)

    # Línea separadora
    c.setStrokeColor(colors.black)
    c.setLineWidth(mm_to_pt(0.3))
    c.line(svg_x(2), svg_y(8), svg_x(48), svg_y(8))

    # Color
    c.setFont("Helvetica", mm_to_pt(2.8))
    c.setFillColor(colors.black)
    c.drawString(svg_x(2), svg_y(13), f"Color: {color_text}")

    # Batería
    c.setFont("Helvetica-Bold", mm_to_pt(2.8))
    c.drawString(svg_x(2), svg_y(17), f"Bat: {bateria_text}")

    # Marco QR (dashed)
    qr_frame_size = 17
    qr_frame_x = 31
    qr_frame_y = 9
    c.setStrokeColor(colors.black)
    c.setLineWidth(mm_to_pt(0.2))
    c.setDash(mm_to_pt(1), mm_to_pt(1))
    c.rect(svg_x(qr_frame_x), svg_y(qr_frame_y + qr_frame_size), mm_to_pt(qr_frame_size), mm_to_pt(qr_frame_size), stroke=1, fill=0)
    c.setDash()

    # QR interno (14 mm)
    qr_inner_size = 14
    qr_inner_x = 32.5
    qr_inner_y = 10.5
    try:
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=3,
            border=0,
        )
        qr.add_data(sku)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_reader = ImageReader(qr_buffer)
        c.drawImage(
            qr_reader,
            svg_x(qr_inner_x),
            svg_y(qr_inner_y + qr_inner_size),
            width=mm_to_pt(qr_inner_size),
            height=mm_to_pt(qr_inner_size),
            preserveAspectRatio=True,
            anchor='sw',
        )
    except Exception as exc:  # pragma: no cover
        logger.error("Error generando QR: %s", exc)
        c.setStrokeColor(colors.black)
        c.rect(
            svg_x(qr_inner_x),
            svg_y(qr_inner_y + qr_inner_size),
            mm_to_pt(qr_inner_size),
            mm_to_pt(qr_inner_size),
            stroke=1,
            fill=0,
        )

    # IMEI (abajo izquierda, Courier)
    c.setFont("Courier", mm_to_pt(2.2))
    c.setFillColor(colors.black)
    c.drawString(svg_x(2), svg_y(28.5), f"IMEI: {imei}")

    # SKU (abajo derecha, pequeño)
    c.setFont("Helvetica", mm_to_pt(2.0))
    c.setFillColor(colors.HexColor("#555555"))
    c.drawRightString(svg_x(48), svg_y(28.5), f"SKU: {sku}")

    c.showPage()
    c.save()
    buffer.seek(0)