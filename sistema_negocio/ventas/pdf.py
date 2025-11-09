from __future__ import annotations

from io import BytesIO
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.utils import timezone

try:  # pragma: no cover - simple availability guard
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
except ImportError as exc:  # pragma: no cover - executed when dependency missing
    A4 = mm = canvas = None  # type: ignore
    _reportlab_import_error = exc
else:
    _reportlab_import_error = None

from configuracion.models import ConfiguracionSistema


def generar_comprobante_pdf(venta) -> ContentFile:
    if canvas is None:  # pragma: no cover - defensive branch
        raise ImproperlyConfigured(
            "La librería 'reportlab' es necesaria para generar comprobantes PDF. "
            "Instalála ejecutando `pip install -r requirements.txt`."
        ) from _reportlab_import_error

    config = ConfiguracionSistema.carga()
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 20 * mm
    y = height - margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, config.nombre_comercial or "ImportStore")
    if config.domicilio_comercial:
        c.setFont("Helvetica", 9)
        c.drawString(margin, y - 16, config.domicilio_comercial)
    if config.contacto_email:
        c.drawString(margin, y - 28, f"Email: {config.contacto_email}")
    if config.whatsapp_numero:
        c.drawString(margin, y - 40, f"WhatsApp: {config.whatsapp_numero}")

    y -= 60
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, f"Comprobante #{venta.numero}")
    c.setFont("Helvetica", 10)
    c.drawString(margin, y - 14, f"Fecha: {timezone.localtime(venta.fecha).strftime('%d/%m/%Y %H:%M')}" )
    if venta.vendedor:
        c.drawString(margin, y - 26, f"Vendedor: {venta.vendedor.get_full_name() or venta.vendedor.username}")
    if venta.cliente_nombre:
        c.drawString(margin, y - 38, f"Cliente: {venta.cliente_nombre}")
    if venta.cliente_documento:
        c.drawString(margin, y - 50, f"Documento: {venta.cliente_documento}")

    y -= 80
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "Descripción")
    c.drawString(width - 120, y, "Cantidad")
    c.drawString(width - 80, y, "Precio")
    c.drawString(width - 40, y, "Total")
    c.line(margin, y - 4, width - margin, y - 4)
    y -= 18

    c.setFont("Helvetica", 9)
    for linea in venta.lineas.all():
        if y < 80:
            c.showPage()
            y = height - margin - 20
        c.drawString(margin, y, linea.descripcion)
        c.drawRightString(width - 110, y, str(linea.cantidad))
        c.drawRightString(width - 60, y, f"{linea.precio_unitario:.2f}")
        c.drawRightString(width - margin, y, f"{linea.total_linea:.2f}")
        y -= 16

    y -= 10
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - margin, y, f"Subtotal: {venta.subtotal:.2f}")
    y -= 14
    c.setFont("Helvetica", 10)
    c.drawRightString(width - margin, y, f"Descuentos: -{venta.descuento_items + venta.descuento_general:.2f}")
    y -= 14
    c.drawRightString(width - margin, y, f"Impuestos: {venta.impuestos:.2f}")
    y -= 18
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - margin, y, f"Total: {venta.total:.2f}")

    c.showPage()
    c.save()
    buffer.seek(0)
    filename = f"comprobante_{venta.numero}.pdf"
    return ContentFile(buffer.read(), name=filename)
