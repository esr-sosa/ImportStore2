import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-y1r-da*d4kgxhe-u@z4l7bd*=&i84@w=c&ybdp^w14d0=(zpv+")

DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"

# core/settings.py

# ... (Tus imports y variables SECRET_KEY, DEBUG, etc. quedan igual)
# core/settings.py

# ... imports y definiciones previas ...

# 1. Definimos las listas base (Leyendo del .env)
ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()
]

def _print_terminal_qr(public_url: str, title: str = "📱 QR CODE PARA ESCANEAR") -> None:
    """Renderiza un QR grande y bien visible en la terminal."""
    try:
        import qrcode
    except ImportError:
        print("--- Instalá 'qrcode[pil]' para ver el QR code en terminal ---")
        return

    try:
        # Configurar QR con tamaño más grande para mejor legibilidad
        qr = qrcode.QRCode(
            version=None,  # Auto-detect version
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # Mejor corrección de errores
            box_size=2,  # Cajas más grandes
            border=2,  # Borde más visible
        )
        qr.add_data(public_url)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        
        # Usar caracteres Unicode más visibles y compatibles
        # ██ para celdas negras, espacios para blancas
        # Con box_size=2, cada celda se renderiza con 2 caracteres de ancho
        ascii_lines = []
        for row in matrix:
            line = ""
            for cell in row:
                line += "██" if cell else "  "
            ascii_lines.append(line)
        
        # Calcular ancho del QR
        qr_width = len(ascii_lines[0]) if ascii_lines else 0
        border_width = max(60, qr_width + 4)

        # Imprimir con formato mejorado
        print("\n" + "═" * border_width)
        print(" " + title.center(border_width - 2) + " ")
        print("═" * border_width)
        print(f"\n🔗 URL: {public_url}\n")
        
        # Espacio antes del QR
        print(" " * ((border_width - qr_width) // 2) + "┌" + "─" * qr_width + "┐")
        
        # Imprimir cada línea del QR con bordes
        for line in ascii_lines:
            print(" " * ((border_width - qr_width) // 2) + "│" + line + "│")
        
        # Espacio después del QR
        print(" " * ((border_width - qr_width) // 2) + "└" + "─" * qr_width + "┘")
        
        print("\n" + "═" * border_width)
        print("💡 Escaneá el código QR con tu celular para acceder\n")
        print("═" * border_width + "\n")
    except Exception as exc:
        print(f"--- Error al generar QR: {exc} ---")
        print(f"URL directa: {public_url}")


# 2. Bloque NGROK "Anti-Bloqueo"
# Solo ejecutamos si estamos en DEBUG, tenemos token y NO es el reloader automático
if DEBUG and os.getenv('NGROK_AUTHTOKEN') and os.environ.get('RUN_MAIN') is None:
    try:
        import ssl
        # Configurar SSL para evitar problemas de certificados
        ssl._create_default_https_context = ssl._create_unverified_context
        
        from pyngrok import ngrok, conf
        
        # Configuramos el token
        conf.get_default().auth_token = os.getenv("NGROK_AUTHTOKEN")
        
        # Intentamos obtener túneles existentes primero
        tunnels = ngrok.get_tunnels()
        backend_url = None
        frontend_url = None

        # Buscar túneles existentes por puerto
        for tunnel in tunnels:
            addr = str(tunnel.config.get('addr', ''))
            if '8000' in addr or tunnel.public_url and '8000' in str(tunnel.config):
                backend_url = tunnel.public_url
            elif '3000' in addr or tunnel.public_url and '3000' in str(tunnel.config):
                frontend_url = tunnel.public_url

        # Si no hay túneles, crear nuevos
        try:
            # Matamos cualquier proceso ngrok zombie del sistema antes de arrancar
            if not backend_url and not frontend_url:
                try:
                    ngrok.kill()
                except:
                    pass  # Ignorar si no hay procesos ngrok para matar
            
            # Crear túnel para backend (puerto 8000) - SIEMPRE necesario
            if not backend_url:
                try:
                    backend_tunnel = ngrok.connect(8000)
                    backend_url = backend_tunnel.public_url
                    print(f"--- NGROK Backend (Nuevo túnel): {backend_url} ---")
                except Exception as backend_error:
                    error_msg = str(backend_error)
                    if "limited to" in error_msg or "simultaneous" in error_msg.lower():
                        print("--- NGROK: Ya hay una sesión activa. El servidor funcionará sin ngrok. ---")
                        print("--- Si necesitás ngrok, cerrá otras sesiones o usá 'ngrok start --all' ---")
                    else:
                        print(f"--- Error al crear túnel NGROK Backend: {backend_error} ---")
                    backend_url = None
            else:
                print(f"--- NGROK Backend (Existente): {backend_url} ---")
            
            # Crear túnel para frontend (puerto 3000) - Opcional si el frontend está corriendo
            if not frontend_url:
                try:
                    frontend_tunnel = ngrok.connect(3000)
                    frontend_url = frontend_tunnel.public_url
                    print(f"--- NGROK Frontend (Nuevo túnel): {frontend_url} ---")
                except Exception as frontend_error:
                    error_msg = str(frontend_error)
                    if "limited to" not in error_msg and "simultaneous" not in error_msg.lower():
                        print(f"--- NGROK Frontend: No se pudo crear túnel (¿Frontend corriendo en puerto 3000?): {frontend_error} ---")
                        print("--- Iniciá el frontend con 'npm run dev' y reiniciá Django para crear el túnel ---")
            else:
                print(f"--- NGROK Frontend (Existente): {frontend_url} ---")
        except Exception as e:
            error_msg = str(e)
            if "limited to" in error_msg or "simultaneous" in error_msg.lower():
                print("--- NGROK: Ya hay una sesión activa. El servidor funcionará sin ngrok. ---")
                print("--- Si necesitás ngrok, cerrá otras sesiones o usá 'ngrok start --all' ---")
            else:
                print(f"--- Error al crear túnel NGROK: {e} ---")

        # Actualizamos las listas de Django (esto es lo que te permite entrar)
        if backend_url:
            ngrok_host = backend_url.replace("https://", "").replace("http://", "")
            if ngrok_host not in ALLOWED_HOSTS:
                ALLOWED_HOSTS.append(ngrok_host)
            if backend_url not in CSRF_TRUSTED_ORIGINS:
                CSRF_TRUSTED_ORIGINS.append(backend_url)
                
            # Guardamos la URL en una variable de entorno para que el reloader la vea
            os.environ["DJANGO_NGROK_URL"] = backend_url
            os.environ["FRONTEND_NGROK_URL"] = frontend_url or ""

            # Mostrar QR para backend
            print("\n" + "=" * 60)
            print("🔧 BACKEND (Django)")
            print("=" * 60)
            _print_terminal_qr(backend_url, "📱 BACKEND QR")
            
            # Mostrar QR para frontend si existe
            if frontend_url:
                print("\n" + "=" * 60)
                print("🌐 FRONTEND (Next.js)")
                print("=" * 60)
                _print_terminal_qr(frontend_url, "📱 FRONTEND QR")
                print(f"\n💡 Actualizá tu .env.local del frontend con:")
                print(f"   NEXT_PUBLIC_API_URL={backend_url}")

    except ImportError:
        print("--- pyngrok no instalado. Instalá con: pip install pyngrok ---")
    except Exception as e:
        print(f"--- Error general NGROK: {e} ---")

# 3. Truco para el Reloader: Si el proceso principal ya consiguió URL, la usamos
if os.environ.get("DJANGO_NGROK_URL"):
    backend_url = os.environ["DJANGO_NGROK_URL"]
    frontend_url = os.environ.get("FRONTEND_NGROK_URL", "")
    ngrok_host = backend_url.replace("https://", "").replace("http://", "")
    if ngrok_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(ngrok_host)
    if backend_url not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(backend_url)
    print(f"--- NGROK Backend (Heredado en Reloader): {backend_url} ---")
    if frontend_url:
        print(f"--- NGROK Frontend (Heredado en Reloader): {frontend_url} ---")

# ... resto de tu settings.py ...


# ... (El resto de tu archivo sigue igual: Fallback inseguro, INSTALLED_APPS, etc.)


# Fallback inseguro sólo permitido en desarrollo
if not DEBUG:
    if not os.getenv("DJANGO_SECRET_KEY"):
        raise RuntimeError("DJANGO_SECRET_KEY es requerido con DEBUG=False")
    if not ALLOWED_HOSTS:
        raise RuntimeError("DJANGO_ALLOWED_HOSTS no puede estar vacío con DEBUG=False")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',  # Para CORS en APIs
    'rest_framework',  # Django REST Framework
    'rest_framework_simplejwt',  # JWT authentication
    'core',
    'crm',
    'inventario',
    'ventas',
    'dashboard',
    'iphones',
    'historial',
    'asistente_ia',
    'configuracion',
    'locales',
    'caja',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS debe ir antes de CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'configuracion.context_processors.configuracion_global',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'sistema_negocio'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
    # Deshabilitar validación de versión de MariaDB para desarrollo local
    import django.db.backends.mysql.base
    original_check_database_version_supported = django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported
    def patched_check_database_version_supported(self):
        try:
            return original_check_database_version_supported(self)
        except Exception:
            # Permitir versiones anteriores en desarrollo
            if DEBUG:
                return
            raise
    django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported = patched_check_database_version_supported
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / os.getenv('SQLITE_NAME', 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = True

USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Directorio opcional para assets compilados (ej: Tailwind build)
STATICFILES_DIRS = [p for p in [BASE_DIR / 'static'] if p.exists()]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGOUT_REDIRECT_URL = 'login'

ASGI_APPLICATION = 'core.asgi.application'

# Channels: Redis si REDIS_URL está disponible; caso contrario, memoria (dev)
REDIS_URL = os.getenv("REDIS_URL", "").strip()
if REDIS_URL:
    # Intentar usar Redis, pero si falla, usar memoria
    try:
        import channels_redis
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    'hosts': [REDIS_URL],
                },
            },
        }
    except ImportError:
        print("[WARNING] channels-redis no está instalado. Usando backend en memoria.")
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer',
            },
        }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

# Seguridad en producción
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "true").lower() == "true"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"

# Timeout por defecto para requests externas
REQUESTS_TIMEOUT_SECONDS = int(os.getenv("REQUESTS_TIMEOUT_SECONDS", "15"))

# CORS settings para frontend e-commerce
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

# Permitir credenciales (cookies, sesiones)
CORS_ALLOW_CREDENTIALS = True

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Para mantener compatibilidad con admin
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Por defecto permitir acceso, luego proteger endpoints específicos
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# Logging unificado
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s'
        },
        'json': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'crm': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'asistente_ia': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'inventario': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}

