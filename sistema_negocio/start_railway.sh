#!/bin/bash
# Script de inicio para Railway
# Detecta automáticamente si usar settings_railway o settings normal

set -e

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
echo "📝 Verificando migraciones pendientes..."
python manage.py makemigrations --noinput 2>/dev/null || echo "⚠️  No se pudieron crear migraciones automáticamente"

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

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

