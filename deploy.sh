#!/bin/bash

# Script de deploy para ImportStore
# Uso: ./deploy.sh [production|development]

set -e  # Salir si hay algún error

ENVIRONMENT=${1:-production}

echo "🚀 Iniciando deploy de ImportStore en modo: $ENVIRONMENT"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que existe .env
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: No se encontró el archivo .env${NC}"
    echo "💡 Copiá .env.example a .env y completá los valores"
    exit 1
fi

# Cargar variables de entorno
export $(cat .env | grep -v '^#' | xargs)

# Verificar variables críticas
if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo -e "${RED}❌ Error: DJANGO_SECRET_KEY no está configurado${NC}"
    exit 1
fi

if [ "$ENVIRONMENT" = "production" ]; then
    if [ "$DJANGO_DEBUG" = "True" ] || [ "$DJANGO_DEBUG" = "true" ]; then
        echo -e "${YELLOW}⚠️  Advertencia: DEBUG está en True en producción${NC}"
    fi
fi

echo -e "${GREEN}✅ Variables de entorno cargadas${NC}"

# Construir imágenes
echo -e "${YELLOW}📦 Construyendo imágenes Docker...${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.prod.yml build --no-cache
else
    docker-compose build --no-cache
fi

echo -e "${GREEN}✅ Imágenes construidas${NC}"

# Detener contenedores existentes
echo -e "${YELLOW}🛑 Deteniendo contenedores existentes...${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.prod.yml down
else
    docker-compose down
fi

# Iniciar servicios
echo -e "${YELLOW}🚀 Iniciando servicios...${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.prod.yml up -d
else
    docker-compose up -d
fi

# Esperar a que la base de datos esté lista
echo -e "${YELLOW}⏳ Esperando a que la base de datos esté lista...${NC}"
sleep 10

# Ejecutar migraciones
echo -e "${YELLOW}🔄 Ejecutando migraciones...${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
    docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
else
    docker-compose exec backend python manage.py migrate
    docker-compose exec backend python manage.py collectstatic --noinput
fi

# Crear superusuario si no existe (solo en desarrollo)
if [ "$ENVIRONMENT" != "production" ]; then
    echo -e "${YELLOW}👤 ¿Crear superusuario? (s/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
        docker-compose exec backend python manage.py createsuperuser
    fi
fi

echo -e "${GREEN}✅ Deploy completado exitosamente!${NC}"
echo ""
echo -e "${GREEN}📊 Estado de los contenedores:${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.prod.yml ps
else
    docker-compose ps
fi

echo ""
echo -e "${GREEN}🌐 URLs:${NC}"
echo "   Frontend: http://localhost:${FRONTEND_PORT:-3000}"
echo "   Backend:  http://localhost:${BACKEND_PORT:-8000}"
echo "   Admin:    http://localhost:${BACKEND_PORT:-8000}/admin/"

