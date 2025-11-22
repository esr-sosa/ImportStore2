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

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

# Iniciar Gunicorn
echo "🚀 Iniciando servidor..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    core.wsgi:application

