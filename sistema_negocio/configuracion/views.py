import json
from typing import Any, Dict, Iterable

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from decimal import Decimal, InvalidOperation

from core.db_inspector import column_exists, table_exists
from crm.models import Cliente
from historial.models import RegistroHistorial
from inventario.models import Categoria, Producto
from locales.forms import LocalForm
from locales.models import Local

from .forms import ConfiguracionSistemaForm, ConfiguracionTiendaForm, PreferenciaUsuarioForm
from .models import ConfiguracionSistema, ConfiguracionTienda, PreferenciaUsuario, EscalaPrecioMayorista


def _pendientes_migracion() -> list[str]:
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    plan = executor.migration_plan(targets)
    pendientes: list[str] = []
    for migration, backwards in plan:
        if not backwards:
            pendientes.append(f"{migration.app_label}.{migration.name}")
    return pendientes


def _columnas_faltantes() -> Dict[str, Iterable[str]]:
    columnas = {
        "inventario": [
            "inventario_productovariante.sku"
            if not column_exists("inventario_productovariante", "sku")
            else None,
            "inventario_precio.precio"
            if not column_exists("inventario_precio", "precio")
            else None,
        ],
        "ventas": [
            "inventario_productovariante.stock_actual"
            if not column_exists("inventario_productovariante", "stock_actual")
            else None,
        ],
    }
    return {
        app: [col for col in valores if col]
        for app, valores in columnas.items()
        if any(valores)
    }


def _salud_inventario() -> Dict[str, Any]:
    productos_activos = None
    if table_exists("inventario_producto"):
        try:
            productos_activos = Producto.objects.filter(activo=True).count()
        except Exception:
            productos_activos = None

    return {
        "productos": productos_activos,
        "tablas": {
            "inventario_producto": table_exists("inventario_producto"),
            "inventario_productovariante": table_exists("inventario_productovariante"),
            "inventario_precio": table_exists("inventario_precio"),
        },
    }


def _system_info(configuracion: ConfiguracionSistema, pendientes: int) -> Dict[str, Any]:
    db_settings = connection.settings_dict
    info = {
        "engine": connection.vendor,
        "database": db_settings.get("NAME", "—"),
        "host": db_settings.get("HOST", "local"),
        "usuarios": get_user_model().objects.count() if table_exists("auth_user") else None,
        "clientes": Cliente.objects.count() if table_exists("crm_cliente") else None,
        "pendientes": pendientes,
    }
    info["debug"] = settings.DEBUG
    return info


def _historial_reciente() -> Iterable[RegistroHistorial]:
    try:
        return RegistroHistorial.objects.select_related("usuario").order_by("-fecha")[:5]
    except Exception:
        return []


def _contexto_panel(
    configuracion,
    configuracion_tienda,
    form,
    pref_form,
    tienda_form,
    local_form,
) -> Dict[str, Any]:
    pendientes = _pendientes_migracion()
    return {
        "form": form,
        "pref_form": pref_form,
        "tienda_form": tienda_form,
        "local_form": local_form,
        "configuracion": configuracion,
        "configuracion_tienda": configuracion_tienda,
        "locales": Local.objects.order_by("nombre"),
        "categorias": Categoria.objects.order_by("nombre"),
        "pendientes": pendientes,
        "columnas_faltantes": _columnas_faltantes(),
        "salud_inventario": _salud_inventario(),
        "system_info": _system_info(configuracion, len(pendientes)),
        "historial_reciente": _historial_reciente(),
        "escalas_precio": EscalaPrecioMayorista.objects.filter(configuracion=configuracion).order_by('orden', 'cantidad_minima'),
    }


@login_required
def panel_configuracion(request):
    configuracion = ConfiguracionSistema.obtener_unica()
    configuracion_tienda = ConfiguracionTienda.obtener_unica()
    preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)

    form = ConfiguracionSistemaForm(instance=configuracion, prefix="sistema")
    pref_form = PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia")
    tienda_form = ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda")
    local_form = LocalForm(prefix="local")

    if request.method == "POST":
        target = request.POST.get("form-target", "sistema")

        if target == "tienda":
            tienda_form = ConfiguracionTiendaForm(request.POST, request.FILES, instance=configuracion_tienda, prefix="tienda")
            if tienda_form.is_valid():
                tienda = tienda_form.save()
                mensaje = "Datos de la tienda actualizados correctamente."

                if request.headers.get("HX-Request"):
                    form = ConfiguracionSistemaForm(instance=configuracion, prefix="sistema")
                    pref_form = PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia")
                    local_form = LocalForm(prefix="local")
                    contexto = _contexto_panel(
                        configuracion,
                        tienda,
                        form,
                        pref_form,
                        ConfiguracionTiendaForm(instance=tienda, prefix="tienda"),
                        local_form,
                    )
                    response = render(request, "configuracion/_panel_content.html", contexto)
                    logo_url = tienda.logo.url if tienda.logo else ""
                    response["HX-Trigger-After-Swap"] = json.dumps(
                        {
                            "configuracionTiendaActualizada": {
                                "nombre": tienda.nombre_tienda,
                                "cuit": tienda.cuit,
                                "direccion": tienda.direccion,
                                "email": tienda.email_contacto,
                                "telefono": tienda.telefono_contacto,
                                "logo": logo_url,
                            },
                            "showToast": {"message": mensaje, "level": "success"},
                        }
                    )
                    return response

                messages.success(request, mensaje)
                return redirect("configuracion:panel")

        elif target == "local":
            local_form = LocalForm(request.POST, prefix="local")
            if local_form.is_valid():
                local = local_form.save()
                mensaje = f"Se agregó el local “{local.nombre}”."

                if request.headers.get("HX-Request"):
                    form = ConfiguracionSistemaForm(instance=configuracion, prefix="sistema")
                    pref_form = PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia")
                    tienda_form = ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda")
                    local_form = LocalForm(prefix="local")
                    contexto = _contexto_panel(
                        configuracion,
                        configuracion_tienda,
                        form,
                        pref_form,
                        tienda_form,
                        local_form,
                    )
                    response = render(request, "configuracion/_panel_content.html", contexto)
                    response["HX-Trigger-After-Swap"] = json.dumps(
                        {
                            "localesActualizados": {
                                "total": Local.objects.count(),
                            },
                            "showToast": {"message": mensaje, "level": "success"},
                        }
                    )
                    return response

                messages.success(request, mensaje)
                return redirect("configuracion:panel")

        else:
            form = ConfiguracionSistemaForm(request.POST, request.FILES, instance=configuracion, prefix="sistema")
            pref_form = PreferenciaUsuarioForm(request.POST, instance=preferencias, prefix="preferencia")
            if form.is_valid() and pref_form.is_valid():
                instancia = form.save()
                pref_form.save()

                mensaje = "Configuración actualizada correctamente."
                if instancia.dolar_blue_manual:
                    mensaje += " Valor manual del dólar blue activo como respaldo."

                if request.headers.get("HX-Request"):
                    form = ConfiguracionSistemaForm(instance=instancia, prefix="sistema")
                    pref_form = PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia")
                    tienda_form = ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda")
                    local_form = LocalForm(prefix="local")
                    contexto = _contexto_panel(
                        instancia,
                        configuracion_tienda,
                        form,
                        pref_form,
                        tienda_form,
                        local_form,
                    )
                    response = render(request, "configuracion/_panel_content.html", contexto)
                    logo_url = instancia.logo.url if instancia.logo else ""
                    response["HX-Trigger-After-Swap"] = json.dumps(
                        {
                            "configuracionActualizada": {
                                "nombre": instancia.nombre_comercial,
                                "lema": instancia.lema,
                                "color": instancia.color_principal,
                                "logo": logo_url,
                            },
                            "showToast": {"message": mensaje, "level": "success"},
                        }
                    )
                    return response

                messages.success(request, mensaje)
                return redirect("configuracion:panel")

    contexto = _contexto_panel(
        configuracion,
        configuracion_tienda,
        form,
        pref_form,
        tienda_form,
        local_form,
    )
    template = "configuracion/_panel_content.html" if request.headers.get("HX-Request") else "configuracion/panel.html"
    return render(request, template, contexto)


@login_required
@require_POST
def actualizar_garantia_categoria(request, categoria_id):
    """Actualiza los días de garantía de una categoría."""
    from django.shortcuts import get_object_or_404
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    
    garantia_dias = request.POST.get("garantia_dias", "").strip()
    if garantia_dias:
        try:
            categoria.garantia_dias = int(garantia_dias)
        except ValueError:
            categoria.garantia_dias = None
    else:
        categoria.garantia_dias = None
    
    categoria.save()
    
    if request.headers.get("HX-Request"):
        configuracion = ConfiguracionSistema.obtener_unica()
        configuracion_tienda = ConfiguracionTienda.obtener_unica()
        preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
        form = ConfiguracionSistemaForm(instance=configuracion, prefix="sistema")
        pref_form = PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia")
        tienda_form = ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda")
        local_form = LocalForm(prefix="local")
        contexto = _contexto_panel(
            configuracion,
            configuracion_tienda,
            form,
            pref_form,
            tienda_form,
            local_form,
        )
        response = render(request, "configuracion/_panel_content.html", contexto)
        response["HX-Trigger-After-Swap"] = json.dumps({
            "showToast": {"message": f"Garantía de {categoria.nombre} actualizada correctamente.", "level": "success"},
        })
        return response
    
    messages.success(request, f"Garantía de {categoria.nombre} actualizada correctamente.")
    return redirect("configuracion:panel")


@login_required
@require_POST
def toggle_modo_oscuro(request):
    preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)

    theme_value = None
    if request.body:
        try:
            payload = json.loads(request.body.decode("utf-8"))
            theme_value = payload.get("theme")
        except (json.JSONDecodeError, UnicodeDecodeError):
            theme_value = None

    if theme_value is None:
        theme_value = request.POST.get("theme")

    if theme_value not in {"light", "dark"}:
        return HttpResponseBadRequest("Tema inválido")

    preferencias.usa_modo_oscuro = theme_value == "dark"
    preferencias.save(update_fields=["usa_modo_oscuro", "actualizado"])

    return JsonResponse(
        {
            "ok": True,
            "theme": theme_value,
            "modo_oscuro": preferencias.usa_modo_oscuro,
        }
    )


@login_required
@require_POST
def eliminar_local(request, pk: int):
    local = get_object_or_404(Local, pk=pk)
    nombre = local.nombre
    local.delete()
    mensaje = f"Se eliminó el local “{nombre}”."

    configuracion = ConfiguracionSistema.obtener_unica()
    configuracion_tienda = ConfiguracionTienda.obtener_unica()
    preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)

    if request.headers.get("HX-Request"):
        contexto = _contexto_panel(
            configuracion,
            configuracion_tienda,
            ConfiguracionSistemaForm(instance=configuracion, prefix="sistema"),
            PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia"),
            ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda"),
            LocalForm(prefix="local"),
        )
        response = render(request, "configuracion/_panel_content.html", contexto)
        response["HX-Trigger-After-Swap"] = json.dumps(
            {
                "localesActualizados": {
                    "total": Local.objects.count(),
                },
                "showToast": {"message": mensaje, "level": "info"},
            }
        )
        return response

    messages.success(request, mensaje)
    return redirect("configuracion:panel")


@login_required
@require_POST
def crear_escala_precio(request):
    """Crear una nueva escala de precio mayorista"""
    try:
        # Obtener datos del POST
        cantidad_minima = request.POST.get("cantidad_minima")
        cantidad_maxima = request.POST.get("cantidad_maxima", "").strip()
        porcentaje_descuento = request.POST.get("porcentaje_descuento")
        orden = request.POST.get("orden", "0")
        activo = request.POST.get("activo") == "on" or request.POST.get("activo") == "true"
        
        # Validaciones
        if not cantidad_minima:
            raise ValueError("La cantidad mínima es requerida")
        
        try:
            cantidad_minima = int(cantidad_minima)
            if cantidad_minima < 1:
                raise ValueError("La cantidad mínima debe ser mayor a 0")
        except ValueError:
            raise ValueError("La cantidad mínima debe ser un número entero válido")
        
        if cantidad_maxima:
            try:
                cantidad_maxima = int(cantidad_maxima)
                if cantidad_maxima < cantidad_minima:
                    raise ValueError("La cantidad máxima debe ser mayor o igual a la cantidad mínima")
            except ValueError:
                raise ValueError("La cantidad máxima debe ser un número entero válido")
        else:
            cantidad_maxima = None
        
        if not porcentaje_descuento:
            raise ValueError("El porcentaje de descuento es requerido")
        
        try:
            porcentaje_descuento = Decimal(str(porcentaje_descuento))
            if porcentaje_descuento < 0 or porcentaje_descuento > 100:
                raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
        except (ValueError, InvalidOperation):
            raise ValueError("El porcentaje de descuento debe ser un número válido")
        
        try:
            orden = int(orden)
        except ValueError:
            orden = 0
        
        configuracion = ConfiguracionSistema.obtener_unica()
        
        escala = EscalaPrecioMayorista.objects.create(
            configuracion=configuracion,
            cantidad_minima=cantidad_minima,
            cantidad_maxima=cantidad_maxima,
            porcentaje_descuento=porcentaje_descuento,
            activo=activo,
            orden=orden,
        )
        
        if request.headers.get("HX-Request"):
            configuracion = ConfiguracionSistema.obtener_unica()
            configuracion_tienda = ConfiguracionTienda.obtener_unica()
            preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
            contexto = _contexto_panel(
                configuracion,
                configuracion_tienda,
                ConfiguracionSistemaForm(instance=configuracion, prefix="sistema"),
                PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia"),
                ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda"),
                LocalForm(prefix="local"),
            )
            response = render(request, "configuracion/_panel_content.html", contexto)
            response["HX-Trigger-After-Swap"] = json.dumps({
                "showToast": {"message": f"Escala creada correctamente: {escala}", "level": "success"},
            })
            return response
        
        return JsonResponse({"success": True, "id": escala.id})
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error al crear escala: {e}", exc_info=True)
        if request.headers.get("HX-Request"):
            # Re-renderizar el panel completo con el error
            configuracion = ConfiguracionSistema.obtener_unica()
            configuracion_tienda = ConfiguracionTienda.obtener_unica()
            preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
            contexto = _contexto_panel(
                configuracion,
                configuracion_tienda,
                ConfiguracionSistemaForm(instance=configuracion, prefix="sistema"),
                PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia"),
                ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda"),
                LocalForm(prefix="local"),
            )
            response = render(request, "configuracion/_panel_content.html", contexto)
            response["HX-Trigger-After-Swap"] = json.dumps({
                "showToast": {"message": f"Error al crear escala: {str(e)}", "level": "error"},
            })
            return response
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_POST
def editar_escala_precio(request, escala_id):
    """Editar una escala de precio mayorista existente"""
    try:
        escala = get_object_or_404(EscalaPrecioMayorista, pk=escala_id)
        
        # Si solo viene el campo 'activo', es un toggle rápido
        post_keys = set(request.POST.keys()) - {'csrfmiddlewaretoken'}
        if "activo" in request.POST and len(post_keys) == 1:
            # Invertir el estado actual (toggle)
            escala.activo = not escala.activo
            escala.save()
        else:
            # Edición completa
            if "cantidad_minima" in request.POST:
                cantidad_minima = int(request.POST["cantidad_minima"])
                if cantidad_minima < 1:
                    raise ValueError("La cantidad mínima debe ser mayor a 0")
                escala.cantidad_minima = cantidad_minima
            
            if "cantidad_maxima" in request.POST:
                cantidad_maxima = request.POST.get("cantidad_maxima", "").strip()
                if cantidad_maxima:
                    cantidad_maxima = int(cantidad_maxima)
                    if escala.cantidad_minima and cantidad_maxima < escala.cantidad_minima:
                        raise ValueError("La cantidad máxima debe ser mayor o igual a la cantidad mínima")
                    escala.cantidad_maxima = cantidad_maxima
                else:
                    escala.cantidad_maxima = None
            
            if "porcentaje_descuento" in request.POST:
                porcentaje_descuento = Decimal(str(request.POST["porcentaje_descuento"]))
                if porcentaje_descuento < 0 or porcentaje_descuento > 100:
                    raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
                escala.porcentaje_descuento = porcentaje_descuento
            
            if "activo" in request.POST:
                escala.activo = request.POST.get("activo") == "on" or request.POST.get("activo") == "true"
            
            if "orden" in request.POST:
                escala.orden = int(request.POST.get("orden", 0))
            
            escala.save()
        
        if request.headers.get("HX-Request"):
            configuracion = ConfiguracionSistema.obtener_unica()
            configuracion_tienda = ConfiguracionTienda.obtener_unica()
            preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
            contexto = _contexto_panel(
                configuracion,
                configuracion_tienda,
                ConfiguracionSistemaForm(instance=configuracion, prefix="sistema"),
                PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia"),
                ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda"),
                LocalForm(prefix="local"),
            )
            response = render(request, "configuracion/_panel_content.html", contexto)
            response["HX-Trigger-After-Swap"] = json.dumps({
                "showToast": {"message": f"Escala actualizada correctamente: {escala}", "level": "success"},
            })
            return response
        
        return JsonResponse({"success": True})
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error al editar escala: {e}", exc_info=True)
        if request.headers.get("HX-Request"):
            # Re-renderizar el panel completo con el error
            configuracion = ConfiguracionSistema.obtener_unica()
            configuracion_tienda = ConfiguracionTienda.obtener_unica()
            preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
            contexto = _contexto_panel(
                configuracion,
                configuracion_tienda,
                ConfiguracionSistemaForm(instance=configuracion, prefix="sistema"),
                PreferenciaUsuarioForm(instance=preferencias, prefix="preferencia"),
                ConfiguracionTiendaForm(instance=configuracion_tienda, prefix="tienda"),
                LocalForm(prefix="local"),
            )
            response = render(request, "configuracion/_panel_content.html", contexto)
            response["HX-Trigger-After-Swap"] = json.dumps({
                "showToast": {"message": f"Error: {str(e)}", "level": "error"},
            })
            return response
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_POST
def eliminar_escala_precio(request, escala_id):
    """Eliminar una escala de precio mayorista"""
    escala = get_object_or_404(EscalaPrecioMayorista, pk=escala_id)
    descripcion = str(escala)
    escala.delete()
    
    if request.headers.get("HX-Request"):
        contexto = _contexto_panel(
            ConfiguracionSistema.obtener_unica(),
            ConfiguracionTienda.obtener_unica(),
            ConfiguracionSistemaForm(instance=ConfiguracionSistema.obtener_unica(), prefix="sistema"),
            PreferenciaUsuarioForm(instance=PreferenciaUsuario.objects.get_or_create(usuario=request.user)[0], prefix="preferencia"),
            ConfiguracionTiendaForm(instance=ConfiguracionTienda.obtener_unica(), prefix="tienda"),
            LocalForm(prefix="local"),
        )
        response = render(request, "configuracion/_panel_content.html", contexto)
        response["HX-Trigger-After-Swap"] = json.dumps({
            "showToast": {"message": f"Escala eliminada: {descripcion}", "level": "info"},
        })
        return response
    
    messages.success(request, f"Escala eliminada: {descripcion}")
    return redirect("configuracion:panel")
