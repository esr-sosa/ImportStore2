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

# Ejecutar migraciones para todas las apps
echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput || {
    echo "❌ Error al ejecutar migraciones, intentando continuar..."
    python manage.py migrate --noinput --run-syncdb 2>&1 | head -20 || true
}

# Asegurar que la migración de sincronización de inventario se ejecute
echo "🔧 Verificando migración de sincronización de inventario..."
python manage.py migrate inventario 0010 --noinput 2>&1 | tail -10 || {
    echo "⚠️  No se pudo ejecutar la migración de sincronización específica"
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

