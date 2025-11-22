#!/bin/bash
# Script de inicio para Railway
# Detecta automáticamente si usar settings_railway o settings normal

# No usar set -e para permitir manejo de errores en migraciones
set -o pipefail

cd /app/sistema_negocio

# Si DATABASE_URL o MYSQL_URL está presente, usar settings_railway
if [ -n "$DATABASE_URL" ] || [ -n "$MYSQL_URL" ] || [ -n "$MYSQL_PUBLIC_URL" ]; then
    export DJANGO_SETTINGS_MODULE=core.settings_railway
    if [ -n "$MYSQL_URL" ] || [ -n "$MYSQL_PUBLIC_URL" ]; then
        echo "✅ Usando settings_railway (MySQL detectado)"
    else
        echo "✅ Usando settings_railway (PostgreSQL detectado)"
    fi
else
    export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-core.settings}
    echo "ℹ️  Usando ${DJANGO_SETTINGS_MODULE}"
fi

# Recopilar archivos estáticos
echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear tabla django_migrations si no existe
echo "🔧 Verificando tabla django_migrations..."
python manage.py create_django_migrations_table 2>/dev/null || true

# Crear migraciones pendientes (si hay cambios en modelos)
echo "📝 Verificando y creando migraciones pendientes..."
MAKE_OUTPUT=$(python manage.py makemigrations --noinput 2>&1) || {
    echo "⚠️  No se pudieron crear migraciones automáticamente"
    echo "$MAKE_OUTPUT" | head -20
}
if [ -n "$MAKE_OUTPUT" ]; then
    echo "$MAKE_OUTPUT" | head -30
fi

# PRIMERO: Ejecutar migraciones de apps críticas (inventario y ventas) ANTES de core
# Esto asegura que las tablas se creen incluso si core.0008 falla
echo "🔄 Ejecutando migraciones de apps críticas primero..."
python manage.py migrate inventario --noinput 2>&1 | tail -20 || echo "⚠️  Error en inventario (continuando...)"
python manage.py migrate ventas --noinput 2>&1 | tail -20 || echo "⚠️  Error en ventas (continuando...)"

# SEGUNDO: Ejecutar migraciones de otras apps (sin core)
echo "🔄 Ejecutando migraciones de otras apps..."
python manage.py migrate crm --noinput 2>&1 | tail -10 || echo "⚠️  Error en crm (continuando...)"
python manage.py migrate configuracion --noinput 2>&1 | tail -10 || echo "⚠️  Error en configuracion (continuando...)"
python manage.py migrate caja --noinput 2>&1 | tail -10 || echo "⚠️  Error en caja (continuando...)"
python manage.py migrate locales --noinput 2>&1 | tail -10 || echo "⚠️  Error en locales (continuando...)"
python manage.py migrate historial --noinput 2>&1 | tail -10 || echo "⚠️  Error en historial (continuando...)"

# TERCERO: Intentar ejecutar todas las migraciones (incluyendo core)
echo "🔄 Ejecutando todas las migraciones (incluyendo core)..."
python manage.py migrate --noinput 2>&1 | tail -30 || {
    echo "⚠️  Algunas migraciones fallaron, intentando marcar core.0008 como aplicada..."
    # Intentar marcar la migración problemática como aplicada
    python manage.py migrate core 0008_rename_core_notifi_leida_9a8f2d_idx_core_notifi_leida_d2a21f_idx_and_more --fake --noinput 2>&1 | tail -5 || {
        echo "⚠️  No se pudo marcar core.0008 como aplicada, continuando..."
    }
    # Intentar core nuevamente después de marcar como aplicada
    python manage.py migrate core --noinput 2>&1 | tail -10 || echo "⚠️  Core aún falla, pero las otras apps están OK"
}

# Asegurar que la migración de sincronización de inventario se ejecute
echo "🔧 Verificando migración de sincronización de inventario..."
python manage.py migrate inventario 0010 --noinput 2>&1 | tail -10 || {
    echo "⚠️  No se pudo ejecutar la migración de sincronización específica (puede que ya esté aplicada)"
}

# Ejecutar todas las migraciones nuevamente para asegurar que todo esté aplicado
echo "🔄 Ejecutando migraciones finales..."
python manage.py migrate --noinput 2>&1 | tail -15

# Verificar estado de migraciones pendientes
echo "📊 Verificando estado de migraciones..."
PENDIENTES=$(python manage.py showmigrations --plan 2>&1 | grep -c "\[ \]" || echo "0")
if [ "$PENDIENTES" -gt 0 ]; then
    echo "⚠️  Hay $PENDIENTES migraciones pendientes:"
    python manage.py showmigrations --plan 2>&1 | grep "\[ \]" | head -15
    echo ""
    echo "💡 Intentando aplicar migraciones pendientes nuevamente..."
    python manage.py migrate --noinput 2>&1 | tail -20
else
    echo "✅ Todas las migraciones están aplicadas"
fi

# Forzar creación de columnas faltantes en inventario (por si las migraciones no las crearon)
echo "🔧 Verificando y creando columnas faltantes en inventario..."
python manage.py fix_inventario_schema 2>&1 | tail -20 || {
    echo "⚠️  No se pudo ejecutar fix_inventario_schema, continuando..."
}

# Iniciar Gunicorn
PORT=${PORT:-8000}
echo "🚀 Iniciando servidor en puerto ${PORT}..."
exec gunicorn \
    --bind 0.0.0.0:${PORT} \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    core.wsgi:application

