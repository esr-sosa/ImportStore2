#!/usr/bin/env python
"""
Script de prueba para Railway
Uso: python scripts/test_railway.py
"""
import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'sistema_negocio'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_railway')
import django
django.setup()

from django.db import connection
from django.conf import settings


def test_database_connection():
    """Test de conexión a la base de datos"""
    print("🔍 Test de conexión a la base de datos...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"   Versión: {version}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("   Verificá que DATABASE_URL esté configurado correctamente")
        return False


def test_settings():
    """Test de configuración de Django"""
    print("\n⚙️  Test de configuración...")
    
    checks = []
    
    # Check SECRET_KEY
    if settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-y1r-da*d4kgxhe-u@z4l7bd*=&i84@w=c&ybdp^w14d0=(zpv+':
        print("✅ SECRET_KEY configurado")
        checks.append(True)
    else:
        print("⚠️  SECRET_KEY no configurado o usando valor por defecto")
        checks.append(False)
    
    # Check DEBUG
    if not settings.DEBUG:
        print("✅ DEBUG=False (producción)")
        checks.append(True)
    else:
        print("⚠️  DEBUG=True (desarrollo)")
        checks.append(False)
    
    # Check ALLOWED_HOSTS
    if settings.ALLOWED_HOSTS:
        print(f"✅ ALLOWED_HOSTS configurado: {settings.ALLOWED_HOSTS}")
        checks.append(True)
    else:
        print("⚠️  ALLOWED_HOSTS vacío")
        checks.append(False)
    
    # Check DATABASE
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        print("✅ Base de datos PostgreSQL configurada")
        checks.append(True)
    else:
        print("⚠️  Base de datos no es PostgreSQL")
        checks.append(False)
    
    return all(checks)


def test_bunny_config():
    """Test de configuración de Bunny Storage"""
    print("\n🟧 Test de configuración de Bunny Storage...")
    
    use_bunny = os.getenv('USE_BUNNY_STORAGE', 'false').lower() == 'true'
    
    if use_bunny:
        required_vars = [
            'BUNNY_STORAGE_KEY',
            'BUNNY_STORAGE_ZONE',
            'BUNNY_STORAGE_URL'
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if not missing:
            print("✅ Bunny Storage configurado correctamente")
            return True
        else:
            print(f"⚠️  Variables faltantes: {', '.join(missing)}")
            return False
    else:
        print("ℹ️  Bunny Storage no está habilitado (USE_BUNNY_STORAGE=false)")
        return True


def test_healthcheck():
    """Test del endpoint de healthcheck"""
    print("\n🏥 Test de healthcheck...")
    
    try:
        from core.healthcheck import healthcheck
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/health/')
        response = healthcheck(request)
        
        if response.status_code == 200:
            print("✅ Healthcheck funcionando")
            return True
        else:
            print(f"⚠️  Healthcheck retornó código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en healthcheck: {e}")
        return False


def main():
    """Ejecutar todos los tests"""
    print("=" * 60)
    print("🧪 TESTS DE RAILWAY")
    print("=" * 60)
    
    results = []
    
    results.append(("Base de datos", test_database_connection()))
    results.append(("Configuración", test_settings()))
    results.append(("Bunny Storage", test_bunny_config()))
    results.append(("Healthcheck", test_healthcheck()))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    print(f"\nTotal: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
        return 1


if __name__ == '__main__':
    sys.exit(main())

