from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from django.db import transaction
from django.utils.text import slugify

from .models import Categoria, Precio, Producto, ProductoVariante, Proveedor


HEADER_ALIASES = {
    "nombre": {"nombre", "name", "titulo", "producto", "nombre del producto"},
    "descripcion": {"descripcion", "description", "detalle", "descripción"},
    "sku": {"sku", "codigo", "codigo sku", "sku principal", "sku (obligatorio)", "sku obligatorio"},
    "stock": {"stock", "stock_actual", "inventario"},
    "stock_minimo": {"stock_minimo", "stock minimo", "minimo"},
    "costo": {"costo", "costo_usd", "costo unitario"},
    "precio_minorista_ars": {"precio", "precio_minorista_ars", "precio ars", "precio venta", "precio minorista"},
    "precio_minorista_usd": {"precio_minorista_usd", "precio usd"},
    "precio_mayorista_ars": {"precio_mayorista_ars", "mayorista ars"},
    "precio_mayorista_usd": {"precio_mayorista_usd", "mayorista usd"},
    "precio_oferta_ars": {"oferta", "precio oferta", "precio promocional"},
    "categoria": {"categoria", "category", "categorias", "categorías > subcategorías > … > subcategorías", "categorías > subcategorías > … > subcategorías"},
    "proveedor": {"proveedor", "supplier", "proveedores", "vendor", "fabricante", "marca"},
    "codigo_barras": {"codigo barras", "barcode", "codigo_de_barras"},
    "atributo_1": {"opcion 1 valor", "opcion1", "atributo1", "color", "opción de variante #1", "opción variante 1", "opción de variante #1", "nombre de variante #1"},
    "atributo_2": {"opcion 2 valor", "opcion2", "atributo2", "talle", "capacidad", "opción de variante #2", "opción variante 2", "opción de variante #2", "nombre de variante #2"},
    "atributo_3": {"opcion 3 valor", "opcion3", "atributo3", "opción de variante #3", "opción variante 3", "nombre de variante #3"},
    "visibilidad": {"visibilidad", "visibilidad (visible o oculto)", "estado", "publicación", "visibilidad visible o oculto"},
}


@dataclass
class ImportResult:
    creados: int = 0
    actualizados: int = 0
    errores: list[str] = None

    def __post_init__(self):
        if self.errores is None:
            self.errores = []


def _normalizar_header(header: str) -> str:
    normal = re.sub(r"\s+", " ", header.strip().lower())
    for canonical, aliases in HEADER_ALIASES.items():
        if normal in aliases:
            return canonical
    return normal


def _leer_csv(contenido: bytes) -> Iterable[dict[str, str]]:
    buffer = io.StringIO(contenido.decode("utf-8-sig"))
    reader = csv.DictReader(buffer)
    headers = reader.fieldnames or []
    mapping = {original: _normalizar_header(original) for original in headers}

    for row in reader:
        data: dict[str, str] = {}
        for original, value in row.items():
            if not original:
                continue
            canonical = mapping.get(original)
            if not canonical:
                continue
            if isinstance(value, str):
                value = value.strip()
            data[canonical] = value
        yield data


def _leer_xlsx(contenido: bytes) -> Iterable[dict[str, str]]:
    try:
        from openpyxl import load_workbook
    except ImportError as exc:  # pragma: no cover - dependencia opcional
        raise RuntimeError("openpyxl es requerido para importar archivos XLSX") from exc

    buffer = io.BytesIO(contenido)
    wb = load_workbook(buffer, read_only=True)
    sheet = wb.active
    rows = sheet.iter_rows(values_only=True)
    headers = [str(h or "").strip() for h in next(rows)]
    headers_normalizados = [_normalizar_header(h) for h in headers]

    for row in rows:
        data = {}
        for header, value in zip(headers_normalizados, row):
            if header:
                data[header] = str(value).strip() if value is not None else ""
        yield data


def _parse_decimal(value: str) -> Decimal | None:
    if value is None:
        return None
    value = value.replace("$", "").replace(",", ".").strip()
    if not value:
        return None
    try:
        return Decimal(value)
    except Exception:
        return None


def _obtener_categoria(nombre: str | None) -> Categoria | None:
    if not nombre:
        return None
    return Categoria.objects.get_or_create(nombre=nombre.strip())[0]


def _obtener_proveedor(nombre: str | None) -> Proveedor | None:
    if not nombre:
        return None
    return Proveedor.objects.get_or_create(nombre=nombre.strip())[0]


@transaction.atomic
def importar_catalogo_desde_archivo(archivo, actualizar: bool = True) -> ImportResult:
    nombre = archivo.name.lower()
    contenido = archivo.read()

    if nombre.endswith(".csv"):
        filas = list(_leer_csv(contenido))
    elif nombre.endswith((".xlsx", ".xls")):
        filas = list(_leer_xlsx(contenido))
    else:
        raise ValueError("Formato no soportado. Usá CSV o XLSX.")

    resultado = ImportResult()

    for idx, fila in enumerate(filas, start=2):  # encabezado es la fila 1
        data = {k: fila.get(k, "") for k in HEADER_ALIASES}
        # Para MercadoLibre: SKU es obligatorio, si no está, generamos desde nombre + variantes
        sku = data.get("sku") or ""
        if not sku:
            nombre = data.get("nombre", "")
            attr1 = data.get("atributo_1", "")
            attr2 = data.get("atributo_2", "")
            attr3 = data.get("atributo_3", "")
            sku = slugify(f"{nombre}-{attr1}-{attr2}-{attr3}".strip("-"))
        if not sku:
            resultado.errores.append(f"Fila {idx}: sin SKU ni nombre.")
            continue

        # Validaciones básicas de stock
        try:
            stock_val = int(data.get("stock") or 0)
            stock_min_val = int(data.get("stock_minimo") or 0)
            if stock_val < 0 or stock_min_val < 0:
                resultado.errores.append(f"Fila {idx}: stock o stock mínimo negativo.")
                continue
        except Exception:
            resultado.errores.append(f"Fila {idx}: stock inválido.")
            continue

        visibilidad = (data.get("visibilidad") or "").strip().lower()
        is_visible = True
        if visibilidad:
            if any(term in visibilidad for term in ["ocult", "hidden", "no", "desactiv", "draft", "inactivo", "0"]):
                is_visible = False

        producto_defaults = {
            "descripcion": data.get("descripcion", ""),
            "categoria": _obtener_categoria(data.get("categoria")),
            "proveedor": _obtener_proveedor(data.get("proveedor")),
            "codigo_barras": data.get("codigo_barras", ""),
            "activo": is_visible,
        }

        producto, _ = Producto.objects.get_or_create(nombre=data.get("nombre") or sku, defaults=producto_defaults)
        for campo, valor in producto_defaults.items():
            if actualizar and valor and getattr(producto, campo) != valor:
                setattr(producto, campo, valor)
        if actualizar:
            producto.save()

        defaults_variante = {
            "atributo_1": data.get("atributo_1", ""),
            "atributo_2": data.get("atributo_2", ""),
            "stock_actual": stock_val,
            "stock_minimo": stock_min_val,
            "activo": is_visible,
        }
        # Si hay atributo_3, lo agregamos a atributo_2 o creamos un campo combinado
        if data.get("atributo_3"):
            if defaults_variante["atributo_2"]:
                defaults_variante["atributo_2"] = f"{defaults_variante['atributo_2']} / {data.get('atributo_3')}"
            else:
                defaults_variante["atributo_2"] = data.get("atributo_3", "")

        variante, creada = ProductoVariante.objects.get_or_create(sku=sku, defaults={"producto": producto, **defaults_variante})
        if creada:
            resultado.creados += 1
        else:
            if actualizar:
                for campo, valor in defaults_variante.items():
                    setattr(variante, campo, valor)
                if variante.producto_id != producto.id:
                    resultado.errores.append(f"Fila {idx}: el SKU {sku} ya está asociado a otro producto.")
                    continue
                variante.save()
                resultado.actualizados += 1
            else:
                resultado.errores.append(f"Fila {idx}: el SKU {sku} ya existe y no se actualizó.")
                continue

        precio_minorista = _parse_decimal(data.get("precio_minorista_ars"))
        if precio_minorista is None:
            precio_minorista = _parse_decimal(data.get("precio_oferta_ars"))

        precios = {
            (Precio.Tipo.MINORISTA, Precio.Moneda.ARS): precio_minorista,
            (Precio.Tipo.MINORISTA, Precio.Moneda.USD): _parse_decimal(data.get("precio_minorista_usd")),
            (Precio.Tipo.MAYORISTA, Precio.Moneda.ARS): _parse_decimal(data.get("precio_mayorista_ars")),
            (Precio.Tipo.MAYORISTA, Precio.Moneda.USD): _parse_decimal(data.get("precio_mayorista_usd")),
        }

        for (tipo, moneda), valor in precios.items():
            if valor is None:
                continue
            Precio.objects.update_or_create(
                variante=variante,
                tipo=tipo,
                moneda=moneda,
                defaults={"precio": valor, "activo": True},
            )

    return resultado


def exportar_catalogo_a_excel() -> io.BytesIO:
    """Exporta el catálogo en formato Excel compatible con MercadoLibre."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
    except ImportError:
        raise RuntimeError("openpyxl es requerido para exportar a Excel")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Catálogo"
    
    # Headers estilo MercadoLibre
    headers = [
        "SKU (OBLIGATORIO)",
        "Nombre del producto",
        "Precio",
        "Oferta",
        "Stock",
        "Visibilidad (Visible o Oculto)",
        "Descripción",
        "Peso en KG",
        "Alto en CM",
        "Ancho en CM",
        "Profundidad en CM",
        "Nombre de variante #1",
        "Opción de variante #1",
        "Nombre de variante #2",
        "Opción de variante #2",
        "Nombre de variante #3",
        "Opción de variante #3",
        "Categorías > Subcategorías > … > Subcategorías",
    ]
    
    # Estilo de headers
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    variantes = ProductoVariante.objects.select_related("producto", "producto__categoria", "producto__proveedor").prefetch_related("precios")
    
    row = 2
    for variante in variantes:
        def precio(tipo, moneda):
            registro = variante.precios.filter(tipo=tipo, moneda=moneda, activo=True).order_by("-actualizado").first()
            return registro.precio if registro else ""
        precio_minorista_ars = precio(Precio.Tipo.MINORISTA, Precio.Moneda.ARS)
        precio_oferta = precio(Precio.Tipo.MINORISTA, Precio.Moneda.ARS)  # Puedes ajustar esto
        visibilidad = "Visible" if variante.activo and variante.producto.activo else "Oculto"
        categoria = variante.producto.categoria.nombre if variante.producto.categoria else ""
        
        ws.cell(row=row, column=1, value=variante.sku)
        ws.cell(row=row, column=2, value=variante.producto.nombre)
        ws.cell(row=row, column=3, value=precio_minorista_ars)
        ws.cell(row=row, column=4, value=precio_oferta)
        ws.cell(row=row, column=5, value=variante.stock_actual)
        ws.cell(row=row, column=6, value=visibilidad)
        ws.cell(row=row, column=7, value=variante.producto.descripcion or "")
        ws.cell(row=row, column=12, value=variante.atributo_1 or "")
        ws.cell(row=row, column=13, value=variante.atributo_1 or "")
        ws.cell(row=row, column=14, value=variante.atributo_2 or "")
        ws.cell(row=row, column=15, value=variante.atributo_2 or "")
        ws.cell(row=row, column=18, value=categoria)
        row += 1
    
    # Ajustar ancho de columnas
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[col_letter].width = adjusted_width
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


def exportar_catalogo_a_csv() -> io.BytesIO:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "SKU (OBLIGATORIO)",
            "Nombre del producto",
            "Precio",
            "Oferta",
            "Stock",
            "Visibilidad (Visible o Oculto)",
            "Descripción",
            "Peso en KG",
            "Alto en CM",
            "Ancho en CM",
            "Profundidad en CM",
            "Nombre de variante #1",
            "Opción de variante #1",
            "Nombre de variante #2",
            "Opción de variante #2",
            "Nombre de variante #3",
            "Opción de variante #3",
            "Categorías > Subcategorías > … > Subcategorías",
        ]
    )

    variantes = ProductoVariante.objects.select_related("producto", "producto__categoria", "producto__proveedor").prefetch_related("precios")
    for variante in variantes:
        def precio(tipo, moneda):
            registro = variante.precios.filter(tipo=tipo, moneda=moneda, activo=True).order_by("-actualizado").first()
            return registro.precio if registro else ""

        precio_minorista_ars = precio(Precio.Tipo.MINORISTA, Precio.Moneda.ARS)
        precio_oferta = precio(Precio.Tipo.MINORISTA, Precio.Moneda.ARS)  # Ajustar según necesidad
        visibilidad = "Visible" if variante.activo and variante.producto.activo else "Oculto"
        categoria = variante.producto.categoria.nombre if variante.producto.categoria else ""
        
        writer.writerow(
            [
                variante.sku,
                variante.producto.nombre,
                precio_minorista_ars,
                precio_oferta,
                variante.stock_actual,
                visibilidad,
                variante.producto.descripcion or "",
                "",  # Peso en KG
                "",  # Alto en CM
                "",  # Ancho en CM
                "",  # Profundidad en CM
                variante.atributo_1 or "",
                variante.atributo_1 or "",
                variante.atributo_2 or "",
                variante.atributo_2 or "",
                "",  # Variante #3
                "",  # Opción variante #3
                categoria,
            ]
        )

    byte_buffer = io.BytesIO()
    byte_buffer.write(buffer.getvalue().encode("utf-8"))
    byte_buffer.seek(0)
    return byte_buffer
