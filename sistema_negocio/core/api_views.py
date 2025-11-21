"""
API REST endpoints para el frontend e-commerce
"""
import json
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch, Subquery, OuterRef
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from configuracion.models import ConfiguracionSistema, ConfiguracionTienda
from inventario.models import Categoria, Producto, ProductoImagen, ProductoVariante, Precio
from ventas.models import CarritoRemoto, Venta, DetalleVenta, Cupon
from crm.models import Cliente
from core.utils import obtener_valor_dolar_blue


def _get_base_url(request):
    """Obtiene la URL base para las imágenes"""
    return request.build_absolute_uri('/')[:-1]


def _formatear_imagen(imagen, request):
    """Formatea la URL de una imagen"""
    if not imagen:
        return None
    base_url = _get_base_url(request)
    return f"{base_url}{imagen.url}"


def _formatear_variante_publica(variante, request, tipo_precio="MINORISTA", cantidad=1):
    """Formatea una variante para la API pública
    
    Args:
        variante: ProductoVariante
        request: HttpRequest
        tipo_precio: "MINORISTA" o "MAYORISTA"
        cantidad: Cantidad del producto (para aplicar escalas de descuento)
    """
    from configuracion.models import ConfiguracionSistema
    from decimal import Decimal
    
    precios_activos = variante.precios.filter(activo=True)
    
    # Obtener precios según tipo
    precio_minorista_ars = precios_activos.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.ARS).first()
    precio_minorista_usd = precios_activos.filter(tipo=Precio.Tipo.MINORISTA, moneda=Precio.Moneda.USD).first()
    precio_mayorista_ars = precios_activos.filter(tipo=Precio.Tipo.MAYORISTA, moneda=Precio.Moneda.ARS).first()
    precio_mayorista_usd = precios_activos.filter(tipo=Precio.Tipo.MAYORISTA, moneda=Precio.Moneda.USD).first()
    
    # Convertir USD a ARS si es necesario
    dolar_blue = obtener_valor_dolar_blue()
    
    precio_final_ars = None
    precio_final_usd = None
    precio_original_usd = None
    precio_base_mayorista = None
    descuento_aplicado = None
    porcentaje_descuento = None
    
    if tipo_precio == "MAYORISTA":
        if precio_mayorista_ars:
            precio_base_mayorista = Decimal(str(precio_mayorista_ars.precio))
            precio_final_ars = float(precio_base_mayorista)
        elif precio_mayorista_usd and dolar_blue:
            precio_original_usd = float(precio_mayorista_usd.precio)
            precio_base_mayorista = Decimal(str(precio_original_usd)) * Decimal(str(dolar_blue))
            precio_final_ars = float(precio_base_mayorista)
            precio_final_usd = precio_original_usd
        
        # Aplicar escalas de descuento si están activas
        if precio_base_mayorista is not None:
            try:
                config = ConfiguracionSistema.obtener_unica()
                categoria_id = variante.producto.categoria.id if variante.producto.categoria else None
                precio_con_escala = config.obtener_precio_con_escala(precio_base_mayorista, cantidad, categoria_id)
                precio_final_ars = float(precio_con_escala)
                
                # Calcular descuento aplicado
                if precio_con_escala < precio_base_mayorista:
                    descuento_aplicado = float(precio_base_mayorista - precio_con_escala)
                    porcentaje_descuento = float((descuento_aplicado / float(precio_base_mayorista)) * 100)
            except:
                pass  # Si hay error, usar precio sin escala
    else:  # MINORISTA
        if precio_minorista_ars:
            precio_final_ars = float(precio_minorista_ars.precio)
        elif precio_minorista_usd and dolar_blue:
            precio_original_usd = float(precio_minorista_usd.precio)
            precio_final_ars = precio_original_usd * float(dolar_blue)
            precio_final_usd = precio_original_usd
    
    # Obtener imágenes del producto
    imagenes = []
    for img in variante.producto.imagenes.all().order_by('orden')[:5]:
        imagenes.append(_formatear_imagen(img.imagen, request))
    
    return {
        "id": variante.id,
        "sku": variante.sku,
        "nombre": variante.producto.nombre,
        "nombre_variante": variante.nombre_variante or "",
        "descripcion": variante.producto.descripcion or "",
        "categoria": {
            "id": variante.producto.categoria.id if variante.producto.categoria else None,
            "nombre": variante.producto.categoria.nombre if variante.producto.categoria else None,
        },
        "atributos": {
            "atributo_1": variante.atributo_1 or "",
            "atributo_2": variante.atributo_2 or "",
            "display": variante.atributos_display,
        },
        "stock": {
            "actual": variante.stock_actual or 0,
            "minimo": variante.stock_minimo or 0,
            "disponible": (variante.stock_actual or 0) > 0,
        },
        "precios": {
            "minorista": {
                "ars": float(precio_minorista_ars.precio) if precio_minorista_ars else None,
                "usd": float(precio_minorista_usd.precio) if precio_minorista_usd else None,
            },
            "mayorista": {
                "ars": float(precio_mayorista_ars.precio) if precio_mayorista_ars else None,
                "usd": float(precio_mayorista_usd.precio) if precio_mayorista_usd else None,
            },
            "final": {
                "ars": precio_final_ars,
                "usd": precio_final_usd,
                "tipo": tipo_precio.lower(),
            },
            "descuento": {
                "aplicado": descuento_aplicado,
                "porcentaje": porcentaje_descuento,
                "precio_base": float(precio_base_mayorista) if precio_base_mayorista else None,
            } if descuento_aplicado else None,
        },
        "imagenes": imagenes,
        "codigo_barras": variante.codigo_barras or "",
        "qr_code": variante.qr_code or "",
        "activo": variante.activo and variante.producto.activo,
    }


@csrf_exempt
@require_http_methods(["GET"])
def api_configuraciones(request):
    """API para obtener configuraciones de la tienda"""
    try:
        config = ConfiguracionSistema.obtener_unica()
        tienda = ConfiguracionTienda.obtener_unica()
        
        base_url = _get_base_url(request)
        
        return JsonResponse({
            "nombre_comercial": config.nombre_comercial,
            "lema": config.lema or "",
            "logo": _formatear_imagen(config.logo, request) if config.logo else None,
            "color_principal": config.color_principal,
            "whatsapp": config.whatsapp_numero or config.whatsapp_alternativo or "",
            "email": config.contacto_email or "",
            "telefono": config.whatsapp_numero or "",
            "direccion": config.domicilio_comercial or tienda.direccion or "",
            "horarios": {
                "lunes_viernes": config.horarios_apertura or "",
                "sabados": config.horarios_apertura or "",
                "domingos": config.horarios_apertura or "",
            },
            "redes_sociales": {
                "instagram": config.instagram_empresa or config.instagram_personal or "",
                "facebook": config.facebook or "",
            },
            "envios": {
                "disponibles": config.envios_disponibles,
                "costo_local": float(config.costo_envio_local) if config.costo_envio_local else None,
                "costo_nacional": float(config.costo_envio_nacional) if config.costo_envio_nacional else None,
            },
            "metodos_pago": {
                "efectivo": config.pago_efectivo_local,
                "transferencia": config.pago_transferencia,
                "tarjeta": config.pago_tarjeta,
            },
            "mayorista": {
                "precios_escala_activos": config.precios_escala_activos,
                "monto_minimo": float(config.monto_minimo_mayorista) if config.monto_minimo_mayorista else 0,
                "cantidad_minima": config.cantidad_minima_mayorista or 0,
                "escalas": [
                    {
                        "cantidad_minima": escala.cantidad_minima,
                        "cantidad_maxima": escala.cantidad_maxima,
                        "porcentaje_descuento": float(escala.porcentaje_descuento),
                        "activo": escala.activo,
                    }
                    for escala in config.escalas_precio.filter(activo=True).order_by('orden', 'cantidad_minima')
                ] if config.precios_escala_activos else [],
            },
        })
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error en api_configuraciones: {error_detail}")
        return JsonResponse({"error": str(e), "detail": error_detail}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_categorias(request):
    """API para obtener todas las categorías"""
    try:
        categorias = Categoria.objects.filter(
            productos__activo=True,
            productos__variantes__activo=True
        ).distinct().order_by('nombre')
        
        resultado = []
        for cat in categorias:
            # Contar productos activos
            productos_count = Producto.objects.filter(
                categoria=cat,
                activo=True,
                variantes__activo=True
            ).distinct().count()
            
            if productos_count > 0:
                resultado.append({
                    "id": cat.id,
                    "nombre": cat.nombre,
                    "descripcion": cat.descripcion or "",
                    "productos_count": productos_count,
                    "parent": cat.parent.id if cat.parent else None,
                })
        
        return JsonResponse({"categorias": resultado})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_proveedores(request):
    """API para obtener proveedores (marcas)"""
    try:
        from inventario.models import Proveedor
        
        proveedores = Proveedor.objects.filter(
            productos__activo=True,
            productos__variantes__activo=True
        ).distinct().order_by('nombre')
        
        resultado = []
        for prov in proveedores:
            productos_count = Producto.objects.filter(
                proveedor=prov,
                activo=True,
                variantes__activo=True
            ).distinct().count()
            
            if productos_count > 0:
                resultado.append({
                    "id": prov.id,
                    "nombre": prov.nombre,
                    "productos_count": productos_count,
                })
        
        return JsonResponse({"proveedores": resultado})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_atributos(request):
    """API para obtener valores únicos de atributos (para filtros)"""
    try:
        atributos_1 = ProductoVariante.objects.filter(
            producto__activo=True,
            activo=True,
            atributo_1__isnull=False
        ).exclude(atributo_1='').values_list('atributo_1', flat=True).distinct().order_by('atributo_1')
        
        atributos_2 = ProductoVariante.objects.filter(
            producto__activo=True,
            activo=True,
            atributo_2__isnull=False
        ).exclude(atributo_2='').values_list('atributo_2', flat=True).distinct().order_by('atributo_2')
        
        return JsonResponse({
            "atributos_1": list(atributos_1),
            "atributos_2": list(atributos_2),
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_productos(request):
    """API para obtener productos con filtros y paginación"""
    try:
        from inventario.models import Proveedor
        
        # Parámetros de consulta
        categoria_id = request.GET.get('categoria')
        proveedor_id = request.GET.get('proveedor')  # Marca
        atributo_1 = request.GET.get('atributo_1')  # Tipo
        atributo_2 = request.GET.get('atributo_2')  # Compatibilidad
        busqueda = request.GET.get('q', '').strip()
        tipo_precio = request.GET.get('tipo_precio', 'MINORISTA').upper()
        min_precio = request.GET.get('min_precio')
        max_precio = request.GET.get('max_precio')
        solo_disponibles = request.GET.get('solo_disponibles', 'true').lower() == 'true'
        ordenar = request.GET.get('ordenar', 'recientes')  # recientes, precio_asc, precio_desc, nombre
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # Query base
        variantes = ProductoVariante.objects.filter(
            producto__activo=True,
            activo=True
        ).select_related('producto', 'producto__categoria', 'producto__proveedor').prefetch_related(
            'precios',
            Prefetch('producto__imagenes', queryset=ProductoImagen.objects.order_by('orden'))
        )
        
        # Filtros
        if categoria_id:
            variantes = variantes.filter(producto__categoria_id=categoria_id)
        
        if proveedor_id:
            variantes = variantes.filter(producto__proveedor_id=proveedor_id)
        
        if atributo_1:
            variantes = variantes.filter(atributo_1__icontains=atributo_1)
        
        if atributo_2:
            variantes = variantes.filter(atributo_2__icontains=atributo_2)
        
        if busqueda:
            variantes = variantes.filter(
                Q(producto__nombre__icontains=busqueda) |
                Q(sku__icontains=busqueda) |
                Q(atributo_1__icontains=busqueda) |
                Q(atributo_2__icontains=busqueda) |
                Q(producto__descripcion__icontains=busqueda)
            )
        
        # Filtrar por stock disponible (solo si se solicita)
        if solo_disponibles:
            variantes = variantes.filter(stock_actual__gt=0)
        
        # Ordenar
        if ordenar == 'nombre':
            variantes = variantes.order_by('producto__nombre', 'sku')
        else:  # recientes (default)
            variantes = variantes.order_by('-actualizado', 'producto__nombre')
        
        # Paginación
        paginator = Paginator(variantes, page_size)
        page_obj = paginator.get_page(page)
        
        # Formatear resultados
        productos = []
        for variante in page_obj:
            producto_data = _formatear_variante_publica(variante, request, tipo_precio)
            
            # Filtrar por rango de precio si se especifica
            if min_precio or max_precio:
                precio_ars = producto_data.get('precios', {}).get('final', {}).get('ars')
                if precio_ars is not None:
                    if min_precio and precio_ars < float(min_precio):
                        continue
                    if max_precio and precio_ars > float(max_precio):
                        continue
            
            productos.append(producto_data)
        
        # Ordenar por precio después de formatear (si es necesario)
        if ordenar == 'precio_asc':
            productos.sort(key=lambda p: p.get('precios', {}).get('final', {}).get('ars') or float('inf'))
        elif ordenar == 'precio_desc':
            productos.sort(key=lambda p: p.get('precios', {}).get('final', {}).get('ars') or 0, reverse=True)
        
        return JsonResponse({
            "productos": productos,
            "paginacion": {
                "page": page,
                "page_size": page_size,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        })
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error en api_productos: {error_detail}")
        return JsonResponse({"error": str(e), "detail": error_detail}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_producto_detalle(request, producto_id):
    """API para obtener detalles de un producto específico"""
    try:
        variante = ProductoVariante.objects.select_related(
            'producto', 'producto__categoria'
        ).prefetch_related(
            'precios',
            Prefetch('producto__imagenes', queryset=ProductoImagen.objects.order_by('orden'))
        ).get(pk=producto_id, producto__activo=True, activo=True)
        
        tipo_precio = request.GET.get('tipo_precio', 'MINORISTA').upper()
        producto_data = _formatear_variante_publica(variante, request, tipo_precio)
        
        # Productos relacionados (misma categoría)
        relacionados = ProductoVariante.objects.filter(
            producto__categoria=variante.producto.categoria,
            producto__activo=True,
            activo=True,
            stock_actual__gt=0
        ).exclude(pk=variante.id).select_related('producto').prefetch_related('precios')[:6]
        
        producto_data["relacionados"] = [
            _formatear_variante_publica(rel, request, tipo_precio) 
            for rel in relacionados
        ]
        
        return JsonResponse(producto_data)
    except ProductoVariante.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_productos_destacados(request):
    """API para obtener productos destacados (puedes personalizar la lógica)"""
    try:
        tipo_precio = request.GET.get('tipo_precio', 'MINORISTA').upper()
        
        # Por ahora, productos con stock y ordenados por actualización
        variantes = ProductoVariante.objects.filter(
            producto__activo=True,
            activo=True,
            stock_actual__gt=0
        ).select_related('producto', 'producto__categoria').prefetch_related(
            'precios',
            Prefetch('producto__imagenes', queryset=ProductoImagen.objects.order_by('orden'))
        ).order_by('-actualizado')[:12]
        
        productos = [_formatear_variante_publica(v, request, tipo_precio) for v in variantes]
        
        return JsonResponse({"productos": productos})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """API para iniciar sesión"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({"error": "Usuario y contraseña requeridos"}, status=400)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email or "",
                    "first_name": user.first_name or "",
                    "last_name": user.last_name or "",
                    "is_staff": user.is_staff,
                }
            })
        else:
            return JsonResponse({"error": "Credenciales inválidas"}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_usuario_actual(request):
    """API para obtener el usuario actual"""
    if not request.user.is_authenticated:
        return JsonResponse({"user": None})
    
    return JsonResponse({
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email or "",
            "first_name": request.user.first_name or "",
            "last_name": request.user.last_name or "",
            "is_staff": request.user.is_staff,
        }
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_carrito(request):
    """API para obtener o modificar el carrito"""
    # Soporta tanto autenticación por sesión como JWT
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    
    # Intentar autenticación JWT primero
    jwt_auth = JWTAuthentication()
    try:
        user, token = jwt_auth.authenticate(request)
        if user:
            request.user = user
    except (AuthenticationFailed, TypeError, AttributeError):
        # Si falla JWT, usar autenticación por sesión
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Autenticación requerida"}, status=401)
    
    if request.method == "GET":
        try:
            carrito_obj, _ = CarritoRemoto.objects.get_or_create(
                usuario=request.user,
                defaults={"items": []}
            )
            carrito = carrito_obj.items if isinstance(carrito_obj.items, list) else []
            
            # Calcular totales
            total_items = sum(int(item.get("cantidad", 1)) for item in carrito if isinstance(item, dict))
            total_ars = sum(
                float(item.get("precio_unitario_ars", 0)) * int(item.get("cantidad", 1))
                for item in carrito if isinstance(item, dict)
            )
            
            return JsonResponse({
                "items": carrito,
                "total_items": total_items,
                "total_ars": total_ars,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == "POST":
        # Agregar producto al carrito
        try:
            data = json.loads(request.body)
            variante_id = data.get("variante_id")
            cantidad = int(data.get("cantidad", 1))
            tipo_precio = data.get("tipo_precio", "MINORISTA").upper()
            
            if not variante_id:
                return JsonResponse({"error": "variante_id requerido"}, status=400)
            
            variante = ProductoVariante.objects.select_related('producto').prefetch_related('precios').get(
                pk=variante_id,
                producto__activo=True,
                activo=True
            )
            
            # Verificar stock
            if (variante.stock_actual or 0) < cantidad:
                return JsonResponse({
                    "error": f"Stock insuficiente. Disponible: {variante.stock_actual}"
                }, status=400)
            
            # Obtener precio base
            precio_ars = variante.precios.filter(
                tipo=tipo_precio,
                moneda=Precio.Moneda.ARS,
                activo=True
            ).first()
            
            precio_usd = variante.precios.filter(
                tipo=tipo_precio,
                moneda=Precio.Moneda.USD,
                activo=True
            ).first()
            
            dolar_blue = obtener_valor_dolar_blue()
            precio_base_ars = None
            precio_ars_valor = None
            descuento_aplicado = None
            porcentaje_descuento = None
            
            if precio_ars:
                precio_base_ars = Decimal(str(precio_ars.precio))
                precio_ars_valor = float(precio_base_ars)
            elif precio_usd and dolar_blue:
                precio_base_ars = Decimal(str(precio_usd.precio)) * Decimal(str(dolar_blue))
                precio_ars_valor = float(precio_base_ars)
            
            if precio_ars_valor is None:
                return JsonResponse({"error": "Producto sin precio"}, status=400)
            
            # Aplicar descuentos por escala si es mayorista
            if tipo_precio == "MAYORISTA" and precio_base_ars:
                try:
                    config = ConfiguracionSistema.obtener_unica()
                    categoria_id = variante.producto.categoria.id if variante.producto.categoria else None
                    precio_con_escala = config.obtener_precio_con_escala(precio_base_ars, cantidad, categoria_id)
                    precio_ars_valor = float(precio_con_escala)
                    
                    if precio_con_escala < precio_base_ars:
                        descuento_aplicado = float(precio_base_ars - precio_con_escala)
                        porcentaje_descuento = float((descuento_aplicado / float(precio_base_ars)) * 100)
                except:
                    pass
            
            # Obtener o crear carrito
            carrito_obj, _ = CarritoRemoto.objects.get_or_create(
                usuario=request.user,
                defaults={"items": []}
            )
            carrito = carrito_obj.items if isinstance(carrito_obj.items, list) else []
            
            # Buscar si ya existe
            item_existente = None
            for item in carrito:
                if isinstance(item, dict) and item.get("variante_id") == variante_id:
                    item_existente = item
                    break
            
            if item_existente:
                nueva_cantidad = item_existente.get("cantidad", 1) + cantidad
                if (variante.stock_actual or 0) < nueva_cantidad:
                    return JsonResponse({
                        "error": f"Stock insuficiente. Disponible: {variante.stock_actual}"
                    }, status=400)
                item_existente["cantidad"] = nueva_cantidad
                
                # Recalcular descuento con nueva cantidad
                if tipo_precio == "MAYORISTA" and precio_base_ars:
                    try:
                        config = ConfiguracionSistema.obtener_unica()
                        categoria_id = variante.producto.categoria.id if variante.producto.categoria else None
                        precio_con_escala = config.obtener_precio_con_escala(precio_base_ars, nueva_cantidad, categoria_id)
                        nuevo_precio = float(precio_con_escala)
                        item_existente["precio_unitario_ars"] = nuevo_precio
                        
                        if precio_con_escala < precio_base_ars:
                            item_existente["descuento_aplicado"] = float(precio_base_ars - precio_con_escala)
                            item_existente["porcentaje_descuento"] = float((item_existente["descuento_aplicado"] / float(precio_base_ars)) * 100)
                            item_existente["precio_base"] = float(precio_base_ars)
                        else:
                            item_existente.pop("descuento_aplicado", None)
                            item_existente.pop("porcentaje_descuento", None)
                            item_existente.pop("precio_base", None)
                    except:
                        pass
            else:
                item_nuevo = {
                    "variante_id": variante_id,
                    "sku": variante.sku,
                    "nombre": variante.producto.nombre,
                    "descripcion": f"{variante.producto.nombre} {variante.atributos_display}".strip(),
                    "cantidad": cantidad,
                    "precio_unitario_ars": precio_ars_valor,
                    "stock_actual": variante.stock_actual or 0,
                }
                if descuento_aplicado:
                    item_nuevo["descuento_aplicado"] = descuento_aplicado
                    item_nuevo["porcentaje_descuento"] = porcentaje_descuento
                    item_nuevo["precio_base"] = float(precio_base_ars)
                carrito.append(item_nuevo)
            
            carrito_obj.items = carrito
            carrito_obj.save(update_fields=["items", "actualizado"])
            
            total_items = sum(int(item.get("cantidad", 1)) for item in carrito if isinstance(item, dict))
            total_ars = sum(
                float(item.get("precio_unitario_ars", 0)) * int(item.get("cantidad", 1))
                for item in carrito if isinstance(item, dict)
            )
            
            return JsonResponse({
                "success": True,
                "items": carrito,
                "total_items": total_items,
                "total_ars": total_ars,
            })
        except ProductoVariante.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_carrito_item(request, item_index):
    """API para eliminar un item del carrito"""
    # Soporta tanto autenticación por sesión como JWT
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    
    jwt_auth = JWTAuthentication()
    try:
        user, token = jwt_auth.authenticate(request)
        if user:
            request.user = user
    except (AuthenticationFailed, TypeError, AttributeError):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Autenticación requerida"}, status=401)
    
    try:
        carrito_obj = CarritoRemoto.objects.get(usuario=request.user)
        carrito = carrito_obj.items if isinstance(carrito_obj.items, list) else []
        
        item_index = int(item_index)
        if 0 <= item_index < len(carrito):
            carrito.pop(item_index)
            carrito_obj.items = carrito
            carrito_obj.save(update_fields=["items", "actualizado"])
            
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Índice inválido"}, status=400)
    except CarritoRemoto.DoesNotExist:
        return JsonResponse({"error": "Carrito no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_carrito_limpiar(request):
    """API para limpiar el carrito"""
    # Soporta tanto autenticación por sesión como JWT
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    
    jwt_auth = JWTAuthentication()
    try:
        user, token = jwt_auth.authenticate(request)
        if user:
            request.user = user
    except (AuthenticationFailed, TypeError, AttributeError):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Autenticación requerida"}, status=401)
    
    try:
        CarritoRemoto.objects.update_or_create(
            usuario=request.user,
            defaults={"items": []}
        )
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_pedido_crear(request):
    """API para crear un pedido desde el carrito"""
    # Soporta tanto autenticación por sesión como JWT
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    
    jwt_auth = JWTAuthentication()
    try:
        user, token = jwt_auth.authenticate(request)
        if user:
            request.user = user
    except (AuthenticationFailed, TypeError, AttributeError):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Autenticación requerida"}, status=401)
    
    try:
        data = json.loads(request.body)
        
        # Obtener carrito
        carrito_obj = CarritoRemoto.objects.get(usuario=request.user)
        carrito = carrito_obj.items if isinstance(carrito_obj.items, list) else []
        
        if not carrito:
            return JsonResponse({"error": "El carrito está vacío"}, status=400)
        
        # Datos del cliente
        cliente_nombre = data.get("cliente_nombre", "")
        cliente_documento = data.get("cliente_documento", "")
        metodo_pago = data.get("metodo_pago", "EFECTIVO_ARS")
        nota = data.get("nota", "")
        codigo_cupon = data.get("codigo_cupon", "").strip().upper() if data.get("codigo_cupon") else None
        
        # Si el usuario tiene documento en su perfil, usarlo si no se proporciona
        if not cliente_documento:
            try:
                perfil = request.user.perfilusuario
                if perfil and perfil.documento:
                    cliente_documento = perfil.documento
            except:
                pass
        
        # Buscar o crear cliente automáticamente
        cliente_obj = None
        if cliente_documento:
            try:
                cliente_obj = Cliente.objects.get(documento=cliente_documento)
            except Cliente.DoesNotExist:
                # Crear cliente si no existe
                cliente_obj = Cliente.objects.create(
                    nombre=cliente_nombre or "Cliente Web",
                    documento=cliente_documento,
                    email=request.user.email if request.user.is_authenticated else "",
                )
        elif request.user.is_authenticated:
            # Intentar obtener cliente del perfil del usuario
            try:
                from core.models import PerfilUsuario
                perfil = getattr(request.user, 'perfil', None)
                if not perfil:
                    try:
                        perfil = PerfilUsuario.objects.get(usuario=request.user)
                    except PerfilUsuario.DoesNotExist:
                        perfil = None
                if perfil and perfil.documento:
                    try:
                        cliente_obj = Cliente.objects.get(documento=perfil.documento)
                    except Cliente.DoesNotExist:
                        cliente_obj = Cliente.objects.create(
                            nombre=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                            documento=perfil.documento,
                            email=request.user.email or "",
                        )
            except:
                pass
        
        # Verificar stock de todos los items ANTES de crear la venta
        items_validos = []
        for item in carrito:
            if not isinstance(item, dict):
                continue
            
            variante_id = item.get("variante_id")
            cantidad = int(item.get("cantidad", 1))
            
            try:
                variante = ProductoVariante.objects.get(pk=variante_id)
                stock_disponible = variante.stock_actual or 0
                
                if stock_disponible < cantidad:
                    return JsonResponse({
                        "error": f"Stock insuficiente para {variante.producto.nombre} ({variante.sku}). Disponible: {stock_disponible}, Solicitado: {cantidad}"
                    }, status=400)
                
                items_validos.append(item)
            except ProductoVariante.DoesNotExist:
                return JsonResponse({
                    "error": f"Producto no encontrado (ID: {variante_id})"
                }, status=400)
        
        if not items_validos:
            return JsonResponse({"error": "No hay items válidos en el carrito"}, status=400)
        
        # Validar compra mínima mayorista si el usuario es mayorista
        try:
            from core.models import PerfilUsuario
            from configuracion.models import ConfiguracionSistema
            from decimal import Decimal
            
            perfil = getattr(request.user, 'perfil', None)
            if not perfil:
                try:
                    perfil = PerfilUsuario.objects.get(usuario=request.user)
                except PerfilUsuario.DoesNotExist:
                    perfil = None
            
            if perfil and perfil.tipo_usuario == 'MAYORISTA':
                config = ConfiguracionSistema.obtener_unica()
                
                # Calcular totales del carrito
                total_cantidad = sum(int(item.get("cantidad", 1)) for item in items_validos)
                total_monto = Decimal("0")
                
                for item in items_validos:
                    cantidad = int(item.get("cantidad", 1))
                    precio_ars = Decimal(str(item.get("precio_unitario_ars", 0)))
                    total_monto += precio_ars * Decimal(str(cantidad))
                
                # Validar monto mínimo
                if config.monto_minimo_mayorista and config.monto_minimo_mayorista > 0:
                    if total_monto < config.monto_minimo_mayorista:
                        return JsonResponse({
                            "error": f"Compra mínima mayorista: ${config.monto_minimo_mayorista:,.2f}. Tu carrito: ${total_monto:,.2f}"
                        }, status=400)
                
                # Validar cantidad mínima
                if config.cantidad_minima_mayorista and config.cantidad_minima_mayorista > 0:
                    if total_cantidad < config.cantidad_minima_mayorista:
                        return JsonResponse({
                            "error": f"Cantidad mínima mayorista: {config.cantidad_minima_mayorista} unidades. Tu carrito: {total_cantidad} unidades"
                        }, status=400)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error validando compra mínima mayorista: {e}")
            # Continuar sin validación si hay error
        
        # Crear venta con los nuevos campos (dentro de transacción)
        from django.utils import timezone
        from django.db import transaction
        import random
        import logging
        logger = logging.getLogger(__name__)
        
        # Generar ID corto para venta web (máximo 20 caracteres)
        # Formato: WEB-YYMMDDHHMMSS-XXX (ej: WEB-251121130030-123)
        timestamp = timezone.now().strftime('%y%m%d%H%M%S')  # Año de 2 dígitos
        random_suffix = random.randint(100, 999)  # 3 dígitos en lugar de 4
        venta_id = f"WEB-{timestamp}-{random_suffix}"
        
        # Normalizar método de pago
        metodo_pago_normalizado = metodo_pago.lower()
        if metodo_pago_normalizado not in [choice[0] for choice in Venta.MetodoPago.choices]:
            # Si viene un valor antiguo, normalizarlo
            if "EFECTIVO" in metodo_pago.upper():
                metodo_pago_normalizado = "efectivo"
            elif "TRANSFERENCIA" in metodo_pago.upper():
                metodo_pago_normalizado = "transferencia"
            elif "MERCADOPAGO" in metodo_pago.upper() or "MP" in metodo_pago.upper():
                metodo_pago_normalizado = "mercadopago_link"
            else:
                metodo_pago_normalizado = "transferencia"  # Default
        
        # Crear venta y detalles dentro de una transacción atómica
        with transaction.atomic():
            venta = Venta.objects.create(
                id=venta_id,
                cliente=cliente_obj,
                cliente_nombre=cliente_nombre or (cliente_obj.nombre if cliente_obj else ""),
                cliente_documento=cliente_documento or (cliente_obj.documento if cliente_obj else ""),
                metodo_pago=metodo_pago_normalizado,
                origen=Venta.Origen.WEB,
                estado_pago=Venta.EstadoPago.PENDIENTE,
                estado_entrega=Venta.EstadoEntrega.PENDIENTE,
                nota=nota,
                observaciones=nota,  # Usar nota también como observaciones
                vendedor=request.user if request.user.is_authenticated else None,
                fecha=timezone.now(),  # Hora exacta
            )
            
            # Crear registro inicial en historial
            from ventas.models import HistorialEstadoVenta
            historial = HistorialEstadoVenta(
                venta=venta,
                estado_nuevo=Venta.Status.PENDIENTE_PAGO,  # Mantener compatibilidad con status antiguo
                usuario=request.user if request.user.is_authenticated else None,
                nota="Pedido creado desde la web"
            )
            historial.save()
            
            # Crear detalles y descontar stock (con select_for_update para evitar condiciones de carrera)
            total_ars = Decimal("0")
            for item in items_validos:
                variante_id = item.get("variante_id")
                cantidad = int(item.get("cantidad", 1))
                precio_unitario = Decimal(str(item.get("precio_unitario_ars", 0)))
                subtotal = precio_unitario * cantidad
                
                # Bloquear la variante para actualización (evita condiciones de carrera)
                variante = ProductoVariante.objects.select_for_update().get(pk=variante_id)
                
                # Verificar stock nuevamente (por si cambió entre la verificación inicial y ahora)
                stock_disponible = variante.stock_actual or 0
                if stock_disponible < cantidad:
                    raise ValueError(f"Stock insuficiente para {variante.sku}: disponible={stock_disponible}, solicitado={cantidad}")
                
                # Crear detalle de venta
                DetalleVenta.objects.create(
                    venta=venta,
                    variante=variante,
                    sku=variante.sku,
                    descripcion=item.get("descripcion", variante.producto.nombre),
                    cantidad=cantidad,
                    precio_unitario_ars_congelado=precio_unitario,
                    subtotal_ars=subtotal,
                )
                
                # Descontar stock
                variante.stock_actual = max(0, stock_disponible - cantidad)
                variante.save(update_fields=['stock_actual', 'actualizado'])
                
                total_ars += subtotal
                logger.info(f"Stock descontado: {variante.sku} - {cantidad} unidades (nuevo stock: {variante.stock_actual})")
        
        # Aplicar cupón si existe
        descuento_cupon = Decimal("0")
        cupon_obj = None
        if codigo_cupon:
            try:
                cupon_obj = Cupon.objects.get(codigo=codigo_cupon)
                es_valido, mensaje = cupon_obj.es_valido(total_ars, request.user if request.user.is_authenticated else None)
                if es_valido:
                    descuento_cupon = cupon_obj.calcular_descuento(total_ars)
                    # Incrementar usos del cupón
                    cupon_obj.usos_actuales += 1
                    cupon_obj.save(update_fields=['usos_actuales'])
                else:
                    # Si el cupón no es válido, no aplicarlo pero continuar con la venta
                    cupon_obj = None
            except Cupon.DoesNotExist:
                pass  # Si el cupón no existe, continuar sin descuento
        
        venta.subtotal_ars = total_ars
        venta.descuento_cupon_ars = descuento_cupon
        venta.total_ars = total_ars - descuento_cupon
        if cupon_obj:
            venta.cupon = cupon_obj
        venta.save()
        
        # Crear notificación de nueva venta web
        try:
            from core.notificaciones import notificar_venta_web
            notificar_venta_web(
                venta_id=venta_id,
                cliente_nombre=cliente_nombre or (cliente_obj.nombre if cliente_obj else "Cliente"),
                total=float(total_ars - descuento_cupon)
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"No se pudo crear notificación de venta web: {e}")
        
        # Limpiar carrito
        carrito_obj.items = []
        carrito_obj.save()
        
        return JsonResponse({
            "success": True,
            "venta_id": venta_id,
            "total": float(total_ars - descuento_cupon),
            "descuento_cupon": float(descuento_cupon),
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_validar_cupon(request):
    """API para validar un cupón de descuento"""
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    
    jwt_auth = JWTAuthentication()
    try:
        user, token = jwt_auth.authenticate(request)
        if user:
            request.user = user
    except (AuthenticationFailed, TypeError, AttributeError):
        if not request.user.is_authenticated:
            request.user = None  # Permitir validación sin autenticación
    
    try:
        data = json.loads(request.body)
        codigo_cupon = data.get("codigo", "").strip().upper()
        monto_total = Decimal(str(data.get("monto_total", 0)))
        
        if not codigo_cupon:
            return JsonResponse({"error": "Código de cupón requerido"}, status=400)
        
        try:
            cupon = Cupon.objects.get(codigo=codigo_cupon)
        except Cupon.DoesNotExist:
            return JsonResponse({"error": "Cupón no encontrado"}, status=404)
        
        # Validar cupón
        es_valido, mensaje = cupon.es_valido(monto_total, request.user if request.user.is_authenticated else None)
        
        if not es_valido:
            return JsonResponse({"error": mensaje}, status=400)
        
        # Calcular descuento
        descuento = cupon.calcular_descuento(monto_total)
        monto_final = monto_total - descuento
        
        return JsonResponse({
            "success": True,
            "cupon": {
                "id": cupon.id,
                "codigo": cupon.codigo,
                "descripcion": cupon.descripcion,
                "tipo_descuento": cupon.tipo_descuento,
                "valor_descuento": float(cupon.valor_descuento),
            },
            "descuento": float(descuento),
            "monto_original": float(monto_total),
            "monto_final": float(monto_final),
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Cupon.DoesNotExist:
        return JsonResponse({"error": "Cupón no encontrado"}, status=404)
    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error al validar cupón: {e}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

