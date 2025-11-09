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
    "nombre": {"nombre", "name", "titulo", "producto"},
    "descripcion": {"descripcion", "description", "detalle"},
    "sku": {"sku", "codigo", "codigo sku", "sku principal"},
    "stock": {"stock", "stock_actual", "inventario"},
    "stock_minimo": {"stock_minimo", "stock minimo", "minimo"},
    "costo": {"costo", "costo_usd", "costo unitario"},
    "precio_minorista_ars": {"precio", "precio_minorista_ars", "precio ars", "precio venta", "precio minorista"},
    "precio_minorista_usd": {"precio_minorista_usd", "precio usd"},
    "precio_mayorista_ars": {"precio_mayorista_ars", "mayorista ars"},
    "precio_mayorista_usd": {"precio_mayorista_usd", "mayorista usd"},
    "categoria": {"categoria", "category"},
    "proveedor": {"proveedor", "supplier"},
    "codigo_barras": {"codigo barras", "barcode", "codigo_de_barras"},
    "atributo_1": {"opcion 1 valor", "opcion1", "atributo1", "color"},
    "atributo_2": {"opcion 2 valor", "opcion2", "atributo2", "talle", "capacidad"},
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

    for fila in filas:
        data = {k: fila.get(k, "") for k in HEADER_ALIASES}
        sku = data.get("sku") or slugify(f"{data.get('nombre')}-{data.get('atributo_1')}-{data.get('atributo_2')}")
        if not sku:
            resultado.errores.append("Fila ignorada por no contar con SKU ni nombre.")
            continue

        producto_defaults = {
            "descripcion": data.get("descripcion", ""),
            "categoria": _obtener_categoria(data.get("categoria")),
            "proveedor": _obtener_proveedor(data.get("proveedor")),
            "codigo_barras": data.get("codigo_barras", ""),
            "activo": True,
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
            "stock_actual": int(data.get("stock") or 0),
            "stock_minimo": int(data.get("stock_minimo") or 0),
            "activo": True,
        }

        variante, creada = ProductoVariante.objects.get_or_create(sku=sku, defaults={"producto": producto, **defaults_variante})
        if creada:
            resultado.creados += 1
        else:
            if actualizar:
                for campo, valor in defaults_variante.items():
                    setattr(variante, campo, valor)
                if variante.producto_id != producto.id:
                    resultado.errores.append(f"El SKU {sku} ya está asociado a otro producto.")
                    continue
                variante.save()
                resultado.actualizados += 1
            else:
                resultado.errores.append(f"El SKU {sku} ya existe y no se actualizó.")
                continue

        precios = {
            (Precio.Tipo.MINORISTA, Precio.Moneda.ARS): _parse_decimal(data.get("precio_minorista_ars")),
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


def exportar_catalogo_a_csv() -> io.BytesIO:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "Nombre",
            "Descripción",
            "SKU",
            "Atributo 1",
            "Atributo 2",
            "Stock",
            "Stock mínimo",
            "Precio minorista ARS",
            "Precio minorista USD",
            "Precio mayorista ARS",
            "Precio mayorista USD",
            "Categoría",
            "Proveedor",
            "Código de barras",
        ]
    )

    variantes = ProductoVariante.objects.select_related("producto", "producto__categoria", "producto__proveedor").prefetch_related("precios")
    for variante in variantes:
        def precio(tipo, moneda):
            registro = variante.precios.filter(tipo=tipo, moneda=moneda, activo=True).order_by("-actualizado").first()
            return registro.precio if registro else ""

        writer.writerow(
            [
                variante.producto.nombre,
                variante.producto.descripcion,
                variante.sku,
                variante.atributo_1,
                variante.atributo_2,
                variante.stock_actual,
                variante.stock_minimo,
                precio(Precio.Tipo.MINORISTA, Precio.Moneda.ARS),
                precio(Precio.Tipo.MINORISTA, Precio.Moneda.USD),
                precio(Precio.Tipo.MAYORISTA, Precio.Moneda.ARS),
                precio(Precio.Tipo.MAYORISTA, Precio.Moneda.USD),
                variante.producto.categoria.nombre if variante.producto.categoria else "",
                variante.producto.proveedor.nombre if variante.producto.proveedor else "",
                variante.producto.codigo_barras or "",
            ]
        )

    byte_buffer = io.BytesIO()
    byte_buffer.write(buffer.getvalue().encode("utf-8"))
    byte_buffer.seek(0)
    return byte_buffer
