"""
Storage backend para Bunny.net
Permite subir y leer archivos desde Bunny Storage
"""
import os
import requests
import logging
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible

logger = logging.getLogger(__name__)


@deconstructible
class BunnyStorage(Storage):
    """
    Storage backend para Bunny.net
    
    Requiere estas variables de entorno:
    - BUNNY_STORAGE_KEY: API key de Bunny Storage
    - BUNNY_STORAGE_ZONE: Nombre de la zona de almacenamiento
    - BUNNY_STORAGE_REGION: Región (ej: 'ny', 'la', 'sg')
    - BUNNY_STORAGE_URL: URL base del CDN (ej: 'https://tu-zona.b-cdn.net')
    """
    
    def __init__(self, location=None, base_url=None):
        self.storage_key = os.getenv('BUNNY_STORAGE_KEY')
        self.storage_zone = os.getenv('BUNNY_STORAGE_ZONE')
        self.storage_region = os.getenv('BUNNY_STORAGE_REGION', 'ny')
        self.storage_url = os.getenv('BUNNY_STORAGE_URL')
        
        if not all([self.storage_key, self.storage_zone, self.storage_url]):
            logger.warning(
                "Bunny Storage no configurado completamente. "
                "Variables requeridas: BUNNY_STORAGE_KEY, BUNNY_STORAGE_ZONE, BUNNY_STORAGE_URL"
            )
        
        self.base_url = base_url or self.storage_url
        self.api_url = f"https://storage.bunnycdn.com/{self.storage_zone}"
    
    def _get_full_path(self, name):
        """Obtiene la ruta completa del archivo en Bunny"""
        return name.lstrip('/')
    
    def _get_public_url(self, name):
        """Genera la URL pública del archivo"""
        if not self.base_url:
            return None
        path = self._get_full_path(name)
        return f"{self.base_url.rstrip('/')}/{path}"
    
    def _get_headers(self):
        """Headers para las peticiones a Bunny API"""
        return {
            'AccessKey': self.storage_key,
            'Content-Type': 'application/octet-stream',
        }
    
    def _open(self, name, mode='rb'):
        """Abre un archivo desde Bunny Storage"""
        if mode != 'rb':
            raise ValueError("BunnyStorage solo soporta modo lectura binaria")
        
        path = self._get_full_path(name)
        url = f"{self.api_url}/{path}"
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            return ContentFile(response.content, name=name)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al leer archivo desde Bunny: {e}")
            raise IOError(f"No se pudo leer el archivo desde Bunny: {e}")
    
    def _save(self, name, content):
        """Guarda un archivo en Bunny Storage"""
        if not all([self.storage_key, self.storage_zone]):
            raise ValueError("Bunny Storage no está configurado correctamente")
        
        path = self._get_full_path(name)
        url = f"{self.api_url}/{path}"
        
        # Leer el contenido del archivo
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content
        
        # Determinar Content-Type
        content_type = 'application/octet-stream'
        if hasattr(content, 'content_type'):
            content_type = content.content_type
        elif name.endswith('.pdf'):
            content_type = 'application/pdf'
        elif name.endswith(('.jpg', '.jpeg')):
            content_type = 'image/jpeg'
        elif name.endswith('.png'):
            content_type = 'image/png'
        elif name.endswith('.webp'):
            content_type = 'image/webp'
        
        headers = {
            'AccessKey': self.storage_key,
            'Content-Type': content_type,
        }
        
        try:
            response = requests.put(url, data=file_content, headers=headers, timeout=60)
            response.raise_for_status()
            logger.info(f"Archivo subido exitosamente a Bunny: {path}")
            return name
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al subir archivo a Bunny: {e}")
            raise IOError(f"No se pudo subir el archivo a Bunny: {e}")
    
    def delete(self, name):
        """Elimina un archivo de Bunny Storage"""
        if not all([self.storage_key, self.storage_zone]):
            return False
        
        path = self._get_full_path(name)
        url = f"{self.api_url}/{path}"
        
        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            logger.info(f"Archivo eliminado de Bunny: {path}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al eliminar archivo de Bunny: {e}")
            return False
    
    def exists(self, name):
        """Verifica si un archivo existe en Bunny Storage"""
        if not all([self.storage_key, self.storage_zone]):
            return False
        
        path = self._get_full_path(name)
        url = f"{self.api_url}/{path}"
        
        try:
            response = requests.head(url, headers=self._get_headers(), timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def url(self, name):
        """Retorna la URL pública del archivo"""
        return self._get_public_url(name)
    
    def size(self, name):
        """Obtiene el tamaño del archivo"""
        if not all([self.storage_key, self.storage_zone]):
            return None
        
        path = self._get_full_path(name)
        url = f"{self.api_url}/{path}"
        
        try:
            response = requests.head(url, headers=self._get_headers(), timeout=10)
            if response.status_code == 200:
                return int(response.headers.get('Content-Length', 0))
        except requests.exceptions.RequestException:
            pass
        
        return None

