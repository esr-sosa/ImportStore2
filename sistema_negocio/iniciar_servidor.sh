#!/bin/bash
echo "Iniciando servidor Django con Daphne (soporta WebSockets)..."
echo ""
cd "$(dirname "$0")"
daphne -b 0.0.0.0 -p 8000 core.asgi:application

