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
    qr_size = min(left_width * 0.75, height * 0.65, 60)  # Más grande: 75% del ancho o 65% de altura, máximo 60
    qr_x = left_center_x - (qr_size / 2)
    qr_y = y + (height / 2) - (qr_size / 2) + 3  # Centrado vertical con pequeño offset
    
    # Generar QR code
    qr_data = variante.sku
    try:
        qr = qrcode.QRCode(version=1, box_size=2, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
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
    if variante.nombre_variante:
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
    
    # Descripción (atributos) debajo del nombre
    if descripcion:
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.black)
        desc_y = nombre_y - (len(nombre_lines[:2]) * 13) - 8
        # Truncar descripción si es muy larga
        max_desc_width = right_width - 10
        if canvas_obj.stringWidth(descripcion, "Helvetica", 8) > max_desc_width:
            # Truncar con ellipsis
            while canvas_obj.stringWidth(descripcion + "...", "Helvetica", 8) > max_desc_width and len(descripcion) > 0:
                descripcion = descripcion[:-1]
            descripcion = descripcion + "..."
        canvas_obj.drawString(right_x, desc_y, descripcion)
    
    # Precio (más chico, con símbolo de peso)
    # Calcular posición del precio basado en el espacio disponible
    precio_y = y + 35  # Abajo en la sección derecha
    
    if precio_minorista_ars:
        # Formatear precio: separar parte entera y decimal
        precio_valor = float(precio_minorista_ars.precio)
        parte_entera = int(precio_valor)
        parte_decimal = int((precio_valor - parte_entera) * 100)
        
        # Precio principal (parte entera) - MÁS CHICO
        precio_font_size = min(24, int(height * 0.35))  # Más chico: hasta 24pt, o 35% de la altura
        precio_texto_principal = f"${parte_entera:,}".replace(",", ".")  # Con símbolo $ y formato con puntos para miles
        canvas_obj.setFont("Helvetica-Bold", precio_font_size)
        canvas_obj.setFillColor(colors.black)
        precio_width = canvas_obj.stringWidth(precio_texto_principal, "Helvetica-Bold", precio_font_size)
        precio_x = right_x
        canvas_obj.drawString(precio_x, precio_y, precio_texto_principal)
        
        # Parte decimal (superíndice, más pequeño)
        if parte_decimal > 0:
            decimal_texto = f"{parte_decimal:02d}"
            decimal_font_size = int(precio_font_size * 0.55)  # 55% del tamaño principal
            canvas_obj.setFont("Helvetica-Bold", decimal_font_size)
            canvas_obj.setFillColor(colors.black)
            decimal_x = precio_x + precio_width + 2
            decimal_y = precio_y + (precio_font_size * 0.2)  # Ligeramente arriba
            canvas_obj.drawString(decimal_x, decimal_y, decimal_texto)
        
        # Precio USD si existe (más pequeño, debajo)
        if precio_minorista_usd:
            precio_usd_valor = float(precio_minorista_usd.precio)
            precio_texto_usd = f"USD ${precio_usd_valor:,.2f}"
            canvas_obj.setFont("Helvetica", 7)
            canvas_obj.setFillColor(colors.HexColor("#64748b"))
            canvas_obj.drawString(precio_x, precio_y - (precio_font_size * 0.6), precio_texto_usd)
    else:
        # Sin precio
        canvas_obj.setFont("Helvetica-Bold", 12)
        canvas_obj.setFillColor(colors.HexColor("#ef4444"))
        canvas_obj.drawString(right_x, precio_y, "Sin precio")
    
    # Garantía (abajo del precio)
    from configuracion.models import ConfiguracionTienda
    config_tienda = ConfiguracionTienda.obtener_unica()
    garantia_general = config_tienda.garantia_dias_general if config_tienda else 45
    
    # Verificar garantía de categoría
    dias_garantia = garantia_general
    if variante.producto.categoria and variante.producto.categoria.garantia_dias:
        dias_garantia = variante.producto.categoria.garantia_dias
    
    garantia_text = f"Garantía de {dias_garantia} días"
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.setFillColor(colors.HexColor("#475569"))
    garantia_y = precio_y - (precio_font_size * 0.8) - 12
    if precio_minorista_usd:
        garantia_y -= 8  # Ajustar si hay precio USD
    canvas_obj.drawString(precio_x, garantia_y, garantia_text)


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
    
    # Dibujar borde de la etiqueta (opcional, para referencia)
    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.5)
    c.rect(x, y, etiqueta_width, etiqueta_height, stroke=1, fill=0)
    
    # Dibujar contenido de la etiqueta
    _dibujar_etiqueta(c, variante, x, y, etiqueta_width, etiqueta_height)
    
    c.save()
    buffer.seek(0)
    return ContentFile(buffer.read(), name="etiqueta.pdf")

