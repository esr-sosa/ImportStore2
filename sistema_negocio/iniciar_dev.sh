#!/bin/bash
# Script para iniciar el servidor de desarrollo de Django

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Activar el entorno virtual
source venv/bin/activate

# Verificar que estamos en el directorio correcto
echo "Directorio actual: $(pwd)"
echo "Python usado: $(which python)"
echo ""

# Iniciar el servidor de desarrollo
python manage.py runserver

