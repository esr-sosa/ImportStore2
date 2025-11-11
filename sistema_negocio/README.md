# ImportStore2 - Guía rápida

## Requisitos
- Python 3.11+
- Pip + venv
- (Opcional prod) Redis para Channels/WebSockets

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1) Crear archivo `.env` en `sistema_negocio/` (mismo nivel que `core/`) basado en:

```dotenv
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
REQUESTS_TIMEOUT_SECONDS=15
# REDIS_URL=redis://localhost:6379/0
# DB_ENGINE=mysql
# DB_NAME=sistema_negocio
# DB_USER=root
# DB_PASSWORD=
# DB_HOST=localhost
# DB_PORT=3306
# DB_CHARSET=utf8mb4
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=
GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-flash
LOG_LEVEL=INFO
```

2) Migraciones y superusuario:
```bash
python manage.py migrate
python manage.py ensure_superuser
```

3) Archivos estáticos (prod):
```bash
python manage.py collectstatic --noinput
```

## Ejecución
Dev (HTTP):
```bash
python manage.py runserver 0.0.0.0:8000
```
ASGI/Channels (recomendado en prod): usar un servidor como `daphne` o `uvicorn` con el app `core.asgi:application` y Redis si definís `REDIS_URL`.

## Notas de seguridad
- Con `DEBUG=false` se exige `DJANGO_SECRET_KEY` y `DJANGO_ALLOWED_HOSTS`.
- Activados HSTS, cookies seguras y redirección SSL (configurable) en producción.

## WhatsApp
Configurar `WHATSAPP_*` en `.env`. El servicio usa timeouts, reintentos y logging estructurado.

## Asistente IA (Gemini)
`GEMINI_API_KEY` requerido. La capa de interpretación valida modelos y campos permitidos para proteger la base.

## Importación de inventario
CSV/XLSX con validaciones por fila. Los errores indican el número de fila y el motivo.

## UI/Responsive
- Sidebar móvil con botón hamburguesa y backdrop.
- Modo oscuro estable mediante variables CSS.
