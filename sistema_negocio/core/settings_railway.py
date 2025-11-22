"""
Settings específicos para Railway
Uso: DJANGO_SETTINGS_MODULE=core.settings_railway python manage.py ...
"""
import os
from pathlib import Path
import dj_database_url
from .settings import *

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================
# BASE DE DATOS (Railway MySQL o PostgreSQL)
# ============================================
# Railway inyecta MYSQL_URL o DATABASE_URL automáticamente
MYSQL_URL = os.getenv('MYSQL_URL')
MYSQL_PUBLIC_URL = os.getenv('MYSQL_PUBLIC_URL')
DATABASE_URL = os.getenv('DATABASE_URL')

if MYSQL_URL or MYSQL_PUBLIC_URL or (DATABASE_URL and DATABASE_URL.startswith('mysql://')):
    # Railway MySQL - parsear URL de MySQL
    mysql_url = MYSQL_URL or MYSQL_PUBLIC_URL or DATABASE_URL
    from urllib.parse import urlparse
    db_url = urlparse(mysql_url)
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_url.path[1:] if db_url.path else os.getenv('MYSQLDATABASE', 'railway'),
            'USER': db_url.username or os.getenv('MYSQLUSER', 'root'),
            'PASSWORD': db_url.password or os.getenv('MYSQLPASSWORD', ''),
            'HOST': db_url.hostname or os.getenv('MYSQLHOST', 'localhost'),
            'PORT': db_url.port or os.getenv('MYSQLPORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode=''",
            },
        }
    }
    # Deshabilitar validación de versión de MariaDB para Railway
    import django.db.backends.mysql.base
    original_check_database_version_supported = django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported
    def patched_check_database_version_supported(self):
        try:
            return original_check_database_version_supported(self)
        except Exception:
            # Permitir versiones anteriores en Railway
            return
    django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported = patched_check_database_version_supported
elif DATABASE_URL:
    # Railway PostgreSQL - usar dj-database-url para parsear DATABASE_URL
    try:
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
    except Exception:
        # Fallback a parseo manual
        from urllib.parse import urlparse
        db_url = urlparse(DATABASE_URL)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_url.path[1:],
                'USER': db_url.username,
                'PASSWORD': db_url.password,
                'HOST': db_url.hostname,
                'PORT': db_url.port or '5432',
                'OPTIONS': {
                    'connect_timeout': 10,
                },
                'CONN_MAX_AGE': 600,
            }
        }
else:
    # Fallback a variables individuales de MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQLDATABASE', os.getenv('DB_NAME', 'railway')),
            'USER': os.getenv('MYSQLUSER', os.getenv('DB_USER', 'root')),
            'PASSWORD': os.getenv('MYSQLPASSWORD', os.getenv('DB_PASSWORD', '')),
            'HOST': os.getenv('MYSQLHOST', os.getenv('DB_HOST', 'localhost')),
            'PORT': os.getenv('MYSQLPORT', os.getenv('DB_PORT', '3306')),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode=''",
            },
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

