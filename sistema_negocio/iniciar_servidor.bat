@echo off
echo Iniciando servidor Django con Daphne (soporta WebSockets)...
echo.
cd /d %~dp0
daphne -b 0.0.0.0 -p 8000 core.asgi:application
pause

