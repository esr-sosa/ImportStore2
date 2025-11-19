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
from ventas.models import CarritoRemoto, Venta, DetalleVenta
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


def _formatear_variante_publica(variante, request, tipo_precio="MINORISTA"):
    """Formatea una variante para la API pública"""
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
    
    if tipo_precio == "MAYORISTA":
        if precio_mayorista_ars:
            precio_final_ars = float(precio_mayorista_ars.precio)
        elif precio_mayorista_usd and dolar_blue:
            precio_original_usd = float(precio_mayorista_usd.precio)
            precio_final_ars = precio_original_usd * float(dolar_blue)
            precio_final_usd = precio_original_usd
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
        config = ConfiguracionSistema.carga()
        tienda = ConfiguracionTienda.obtener_unica()
        
        base_url = _get_base_url(request)
        
        return JsonResponse({
            "nombre_comercial": config.nombre_comercial,
            "lema": config.lema or "",
            "logo": _formatear_imagen(config.logo, request) if config.logo else None,
            "color_principal": config.color_principal,
            "whatsapp": config.telefono_whatsapp or config.whatsapp_numero or "",
            "email": config.correo_contacto or config.contacto_email or "",
            "telefono": config.telefono_local or "",
            "direccion": config.domicilio_comercial or tienda.direccion or "",
            "horarios": {
                "lunes_viernes": config.horario_lunes_a_viernes or "",
                "sabados": config.horario_sabados or "",
                "domingos": config.horario_domingos or "",
            },
            "redes_sociales": {
                "instagram": config.instagram_principal or "",
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
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
        return JsonResponse({"error": str(e)}, status=500)


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
            
            # Obtener precio
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
            precio_ars_valor = None
            
            if precio_ars:
                precio_ars_valor = float(precio_ars.precio)
            elif precio_usd and dolar_blue:
                precio_ars_valor = float(precio_usd.precio) * float(dolar_blue)
            
            if precio_ars_valor is None:
                return JsonResponse({"error": "Producto sin precio"}, status=400)
            
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
            else:
                carrito.append({
                    "variante_id": variante_id,
                    "sku": variante.sku,
                    "nombre": variante.producto.nombre,
                    "descripcion": f"{variante.producto.nombre} {variante.atributos_display}".strip(),
                    "cantidad": cantidad,
                    "precio_unitario_ars": precio_ars_valor,
                    "stock_actual": variante.stock_actual or 0,
                })
            
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
        
        # Crear venta
        from django.utils import timezone
        venta_id = f"WEB-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        venta = Venta.objects.create(
            id=venta_id,
            cliente_nombre=cliente_nombre,
            cliente_documento=cliente_documento,
            metodo_pago=metodo_pago,
            status=Venta.Status.PENDIENTE_PAGO,
            nota=nota,
            vendedor=request.user,
            origen=Venta.Origen.WEB,  # Marcar como venta web
        )
        
        # Crear registro inicial en historial
        from ventas.models import HistorialEstadoVenta
        HistorialEstadoVenta.objects.create(
            venta=venta,
            estado_nuevo=Venta.Status.PENDIENTE_PAGO,
            usuario=request.user,
            nota="Pedido creado desde la web"
        )
        
        # Crear detalles
        total_ars = Decimal("0")
        for item in carrito:
            if not isinstance(item, dict):
                continue
            
            variante_id = item.get("variante_id")
            cantidad = int(item.get("cantidad", 1))
            precio_unitario = Decimal(str(item.get("precio_unitario_ars", 0)))
            subtotal = precio_unitario * cantidad
            
            try:
                variante = ProductoVariante.objects.get(pk=variante_id)
                DetalleVenta.objects.create(
                    venta=venta,
                    variante=variante,
                    sku=variante.sku,
                    descripcion=item.get("descripcion", variante.producto.nombre),
                    cantidad=cantidad,
                    precio_unitario_ars_congelado=precio_unitario,
                    subtotal_ars=subtotal,
                )
                total_ars += subtotal
            except ProductoVariante.DoesNotExist:
                continue
        
        venta.subtotal_ars = total_ars
        venta.total_ars = total_ars
        venta.save()
        
        # Limpiar carrito
        carrito_obj.items = []
        carrito_obj.save()
        
        return JsonResponse({
            "success": True,
            "venta_id": venta_id,
            "total": float(total_ars),
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

