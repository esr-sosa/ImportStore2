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
    """Renderiza un QR compacto y bien proporcionado en la terminal."""
    try:
        import qrcode
    except ImportError:
        print("--- Instalá 'qrcode[pil]' para ver el QR code en terminal ---")
        return

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(public_url)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        # Usar dos caracteres horizontales por celda para compensar el aspecto rectangular de los caracteres
        ascii_lines = ["".join("██" if cell else "  " for cell in row) for row in matrix]
        
        # Calcular ancho del QR (cada celda = 2 caracteres)
        qr_width = len(ascii_lines[0]) if ascii_lines else 0
        border_width = max(40, qr_width + 2)

        print("\n" + "=" * border_width)
        print(f" {title.center(border_width - 2)}")
        print("=" * border_width)
        print(f"URL: {public_url}\n")
        for line in ascii_lines:
            print(line)
        print("\n" + "=" * border_width + "\n")
    except Exception as exc:
        print(f"--- Error al generar QR: {exc} ---")


# 2. Bloque NGROK "Anti-Bloqueo"
# Solo ejecutamos si estamos en DEBUG, tenemos token y NO es el reloader automático
if DEBUG and os.getenv('NGROK_AUTHTOKEN') and os.environ.get('RUN_MAIN') is None:
    try:
        from pyngrok import ngrok, conf
        
        # Configuramos el token
        conf.get_default().auth_token = os.getenv("NGROK_AUTHTOKEN")
        
        # Intentamos obtener túneles existentes primero
        tunnels = ngrok.get_tunnels()
        public_url = None

        if tunnels:
            # Si ya hay uno abierto (quizás quedó de una sesión anterior), lo usamos
            public_url = tunnels[0].public_url
            print(f"--- NGROK (Existente detectado): {public_url} ---")
        else:
            # Si no hay, creamos uno nuevo
            try:
                # Matamos cualquier proceso ngrok zombie del sistema antes de arrancar
                ngrok.kill()
                
                http_tunnel = ngrok.connect(8000)
                public_url = http_tunnel.public_url
                print(f"--- NGROK (Nuevo túnel): {public_url} ---")
            except Exception as e:
                print(f"--- Error al crear túnel NGROK: {e} ---")

        # Actualizamos las listas de Django (esto es lo que te permite entrar)
        if public_url:
            ngrok_host = public_url.replace("https://", "").replace("http://", "")
            if ngrok_host not in ALLOWED_HOSTS:
                ALLOWED_HOSTS.append(ngrok_host)
            if public_url not in CSRF_TRUSTED_ORIGINS:
                CSRF_TRUSTED_ORIGINS.append(public_url)
                
            # Guardamos la URL en una variable de entorno para que el reloader la vea
            os.environ["DJANGO_NGROK_URL"] = public_url

            _print_terminal_qr(public_url)

    except ImportError:
        print("--- pyngrok no instalado. ---")
    except Exception as e:
        print(f"--- Error general NGROK: {e} ---")

# 3. Truco para el Reloader: Si el proceso principal ya consiguió URL, la usamos
if os.environ.get("DJANGO_NGROK_URL"):
    public_url = os.environ["DJANGO_NGROK_URL"]
    ngrok_host = public_url.replace("https://", "").replace("http://", "")
    if ngrok_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(ngrok_host)
    if public_url not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(public_url)
    print(f"--- NGROK (Heredado en Reloader): {public_url} ---")
    
    _print_terminal_qr(public_url)

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
            },
        }
    }
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
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
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

