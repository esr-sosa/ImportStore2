#!/usr/bin/env python
"""
Script de prueba para Bunny Storage
Uso: python scripts/test_bunny.py
"""
import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'sistema_negocio'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from core.utils_bunny import BunnyStorageClient, upload_pdf_to_bunny, upload_image_to_bunny
from io import BytesIO


def test_bunny_connection():
    """Test de conexión a Bunny Storage"""
    print("🔍 Test de conexión a Bunny Storage...")
    
    try:
        client = BunnyStorageClient()
        print("✅ Cliente Bunny Storage inicializado correctamente")
        print(f"   Zona: {client.storage_zone}")
        print(f"   Región: {client.storage_region}")
        print(f"   URL: {client.storage_url}")
        return True
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("   Verificá que las variables de entorno estén configuradas:")
        print("   - BUNNY_STORAGE_KEY")
        print("   - BUNNY_STORAGE_ZONE")
        print("   - BUNNY_STORAGE_URL")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def test_upload_file():
    """Test de subida de archivo"""
    print("\n📤 Test de subida de archivo...")
    
    try:
        client = BunnyStorageClient()
        
        # Crear un archivo de prueba
        test_content = b"Este es un archivo de prueba para Bunny Storage"
        test_path = "test/test_file.txt"
        
        url = client.upload_file(test_content, test_path, content_type='text/plain')
        
        if url:
            print(f"✅ Archivo subido exitosamente")
            print(f"   URL: {url}")
            
            # Verificar que existe
            if client.file_exists(test_path):
                print("✅ Archivo verificado en Bunny Storage")
            else:
                print("⚠️  Archivo no encontrado después de subir")
            
            # Limpiar
            if client.delete_file(test_path):
                print("✅ Archivo de prueba eliminado")
            
            return True
        else:
            print("❌ No se pudo subir el archivo")
            return False
    except Exception as e:
        print(f"❌ Error al subir archivo: {e}")
        return False


def test_upload_pdf():
    """Test de subida de PDF"""
    print("\n📄 Test de subida de PDF...")
    
    try:
        # Crear un PDF de prueba simple
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"
        test_path = "test/test_comprobante.pdf"
        
        url = upload_pdf_to_bunny(BytesIO(pdf_content), test_path)
        
        if url:
            print(f"✅ PDF subido exitosamente")
            print(f"   URL: {url}")
            
            # Limpiar
            client = BunnyStorageClient()
            if client.delete_file(test_path):
                print("✅ PDF de prueba eliminado")
            
            return True
        else:
            print("❌ No se pudo subir el PDF")
            return False
    except Exception as e:
        print(f"❌ Error al subir PDF: {e}")
        return False


def test_upload_image():
    """Test de subida de imagen"""
    print("\n🖼️  Test de subida de imagen...")
    
    try:
        # Crear una imagen de prueba simple (1x1 PNG)
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        test_path = "test/test_image.png"
        
        url = upload_image_to_bunny(BytesIO(png_content), test_path)
        
        if url:
            print(f"✅ Imagen subida exitosamente")
            print(f"   URL: {url}")
            
            # Limpiar
            client = BunnyStorageClient()
            if client.delete_file(test_path):
                print("✅ Imagen de prueba eliminada")
            
            return True
        else:
            print("❌ No se pudo subir la imagen")
            return False
    except Exception as e:
        print(f"❌ Error al subir imagen: {e}")
        return False


def main():
    """Ejecutar todos los tests"""
    print("=" * 60)
    print("🧪 TESTS DE BUNNY STORAGE")
    print("=" * 60)
    
    results = []
    
    results.append(("Conexión", test_bunny_connection()))
    results.append(("Subida de archivo", test_upload_file()))
    results.append(("Subida de PDF", test_upload_pdf()))
    results.append(("Subida de imagen", test_upload_image()))
    
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

