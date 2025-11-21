"""
Settings específicos para Railway
Uso: DJANGO_SETTINGS_MODULE=core.settings_railway python manage.py ...
"""
import os
from pathlib import Path
import dj_database_url
from .settings_production import *

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================
# BASE DE DATOS (Railway PostgreSQL)
# ============================================
# Railway inyecta DATABASE_URL automáticamente
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Usar dj-database-url para parsear DATABASE_URL
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback a variables individuales
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'railway'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            },
            'CONN_MAX_AGE': 600,
        }
    }

# ============================================
# ALLOWED HOSTS (Railway)
# ============================================
RAILWAY_PUBLIC_DOMAIN = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
ALLOWED_HOSTS_ENV = os.getenv('DJANGO_ALLOWED_HOSTS', '')

if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',') if host.strip()]
else:
    # Defaults para Railway
    ALLOWED_HOSTS = ['*']  # Railway maneja el routing

if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

# ============================================
# CSRF TRUSTED ORIGINS
# ============================================
CSRF_TRUSTED_ORIGINS_ENV = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '')

if CSRF_TRUSTED_ORIGINS_ENV:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_ENV.split(',') if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []

if RAILWAY_PUBLIC_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_PUBLIC_DOMAIN}')

# ============================================
# STATIC FILES (Railway usa volúmenes efímeros)
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Usar WhiteNoise para servir archivos estáticos en Railway
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================
# MEDIA FILES (Bunny Storage)
# ============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Si está configurado Bunny Storage, usarlo como backend
USE_BUNNY_STORAGE = os.getenv('USE_BUNNY_STORAGE', 'false').lower() == 'true'

if USE_BUNNY_STORAGE:
    DEFAULT_FILE_STORAGE = 'core.storage.BunnyStorage'
    # Configurar Bunny Storage
    BUNNY_STORAGE_KEY = os.getenv('BUNNY_STORAGE_KEY')
    BUNNY_STORAGE_ZONE = os.getenv('BUNNY_STORAGE_ZONE')
    BUNNY_STORAGE_REGION = os.getenv('BUNNY_STORAGE_REGION', 'ny')
    BUNNY_STORAGE_URL = os.getenv('BUNNY_STORAGE_URL')

# ============================================
# LOGGING (Railway)
# ============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'importstore': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================
# SEGURIDAD
# ============================================
# Railway maneja SSL/TLS, así que confiamos en el proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway maneja esto
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

