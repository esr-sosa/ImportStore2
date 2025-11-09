from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.shortcuts import redirect, render

from core.db_inspector import column_exists, table_exists
from inventario.models import Producto

from .forms import ConfiguracionSistemaForm, PreferenciaUsuarioForm
from .models import ConfiguracionSistema, PreferenciaUsuario


def _pendientes_migracion() -> list[str]:
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    plan = executor.migration_plan(targets)
    pendientes = []
    for migration, backwards in plan:
        if not backwards:
            pendientes.append(f"{migration.app_label}.{migration.name}")
    return pendientes


@login_required
def panel_configuracion(request):
    configuracion = ConfiguracionSistema.carga()
    preferencias, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form = ConfiguracionSistemaForm(request.POST, request.FILES, instance=configuracion)
        pref_form = PreferenciaUsuarioForm(request.POST, instance=preferencias)
        if form.is_valid() and pref_form.is_valid():
            instancia = form.save()
            pref_form.save()
            messages.success(request, "Configuración actualizada correctamente.")
            if instancia.dolar_blue_manual:
                messages.info(
                    request,
                    "El valor manual del dólar blue se utilizará como fallback cuando no haya conexión.",
                )
            return redirect("configuracion:panel")
    else:
        form = ConfiguracionSistemaForm(instance=configuracion)
        pref_form = PreferenciaUsuarioForm(instance=preferencias)

    pendientes = _pendientes_migracion()
    columnas_faltantes = {
        "inventario": [
            "inventario_productovariante.sku" if not column_exists("inventario_productovariante", "sku") else None,
            "inventario_precio.precio" if not column_exists("inventario_precio", "precio") else None,
        ],
        "ventas": [
            "inventario_productovariante.stock_actual" if not column_exists("inventario_productovariante", "stock_actual") else None,
        ],
    }

    columnas_faltantes = {
        app: [col for col in cols if col]
        for app, cols in columnas_faltantes.items()
        if any(cols)
    }

    productos_activos = None
    if table_exists("inventario_producto"):
        try:
            productos_activos = Producto.objects.filter(activo=True).count()
        except Exception:
            productos_activos = None

    salud_inventario = {
        "productos": productos_activos,
        "tablas": {
            "inventario_producto": table_exists("inventario_producto"),
            "inventario_productovariante": table_exists("inventario_productovariante"),
            "inventario_precio": table_exists("inventario_precio"),
        },
    }

    return render(
        request,
        "configuracion/panel.html",
        {
            "form": form,
            "pref_form": pref_form,
            "configuracion": configuracion,
            "pendientes": pendientes,
            "columnas_faltantes": columnas_faltantes,
            "salud_inventario": salud_inventario,
        },
    )
