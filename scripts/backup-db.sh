#!/bin/bash

# Script de backup de base de datos
# Uso: ./scripts/backup-db.sh

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"

echo "🔄 Creando backup de la base de datos..."

# Cargar variables de entorno
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Hacer backup
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U ${DB_USER:-importstore_user} ${DB_NAME:-importstore} > "$BACKUP_FILE"

# Comprimir backup
gzip "$BACKUP_FILE"
BACKUP_FILE="${BACKUP_FILE}.gz"

echo "✅ Backup creado: $BACKUP_FILE"

# Mantener solo los últimos 7 backups
ls -t "$BACKUP_DIR"/backup_*.sql.gz | tail -n +8 | xargs -r rm

echo "📦 Backups antiguos eliminados (manteniendo últimos 7)"

