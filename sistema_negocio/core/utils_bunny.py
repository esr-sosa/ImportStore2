"""
Utilidades para trabajar con Bunny Storage
"""
import os
import requests
import logging
from typing import Optional, BinaryIO
from io import BytesIO

logger = logging.getLogger(__name__)


class BunnyStorageClient:
    """
    Cliente para interactuar con Bunny Storage API
    
    Uso:
        client = BunnyStorageClient()
        url = client.upload_file(file_content, 'comprobantes/venta_123.pdf')
    """
    
    def __init__(self):
        self.storage_key = os.getenv('BUNNY_STORAGE_KEY')
        self.storage_zone = os.getenv('BUNNY_STORAGE_ZONE')
        self.storage_region = os.getenv('BUNNY_STORAGE_REGION', 'ny')
        self.storage_url = os.getenv('BUNNY_STORAGE_URL')
        
        if not all([self.storage_key, self.storage_zone, self.storage_url]):
            raise ValueError(
                "Bunny Storage no está configurado. "
                "Variables requeridas: BUNNY_STORAGE_KEY, BUNNY_STORAGE_ZONE, BUNNY_STORAGE_URL"
            )
        
        self.api_url = f"https://storage.bunnycdn.com/{self.storage_zone}"
    
    def _get_headers(self, content_type: str = 'application/octet-stream'):
        """Headers para las peticiones a Bunny API"""
        return {
            'AccessKey': self.storage_key,
            'Content-Type': content_type,
        }
    
    def upload_file(
        self,
        file_content: bytes | BinaryIO,
        remote_path: str,
        content_type: Optional[str] = None
    ) -> Optional[str]:
        """
        Sube un archivo a Bunny Storage
        
        Args:
            file_content: Contenido del archivo (bytes o file-like object)
            remote_path: Ruta donde guardar el archivo (ej: 'comprobantes/venta_123.pdf')
            content_type: Tipo MIME del archivo (se detecta automáticamente si no se proporciona)
        
        Returns:
            URL pública del archivo o None si falla
        """
        # Normalizar la ruta
        remote_path = remote_path.lstrip('/')
        
        # Leer el contenido si es un file-like object
        if hasattr(file_content, 'read'):
            content_bytes = file_content.read()
            if hasattr(file_content, 'seek'):
                file_content.seek(0)  # Resetear para posibles lecturas futuras
        else:
            content_bytes = file_content
        
        # Detectar content-type si no se proporciona
        if not content_type:
            if remote_path.endswith('.pdf'):
                content_type = 'application/pdf'
            elif remote_path.endswith(('.jpg', '.jpeg')):
                content_type = 'image/jpeg'
            elif remote_path.endswith('.png'):
                content_type = 'image/png'
            elif remote_path.endswith('.webp'):
                content_type = 'image/webp'
            else:
                content_type = 'application/octet-stream'
        
        url = f"{self.api_url}/{remote_path}"
        headers = self._get_headers(content_type)
        
        try:
            response = requests.put(url, data=content_bytes, headers=headers, timeout=60)
            response.raise_for_status()
            
            # Generar URL pública
            public_url = f"{self.storage_url.rstrip('/')}/{remote_path}"
            logger.info(f"Archivo subido exitosamente a Bunny: {remote_path} -> {public_url}")
            return public_url
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al subir archivo a Bunny: {e}")
            return None
    
    def delete_file(self, remote_path: str) -> bool:
        """
        Elimina un archivo de Bunny Storage
        
        Args:
            remote_path: Ruta del archivo a eliminar
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        remote_path = remote_path.lstrip('/')
        url = f"{self.api_url}/{remote_path}"
        
        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            logger.info(f"Archivo eliminado de Bunny: {remote_path}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al eliminar archivo de Bunny: {e}")
            return False
    
    def file_exists(self, remote_path: str) -> bool:
        """
        Verifica si un archivo existe en Bunny Storage
        
        Args:
            remote_path: Ruta del archivo a verificar
        
        Returns:
            True si existe, False en caso contrario
        """
        remote_path = remote_path.lstrip('/')
        url = f"{self.api_url}/{remote_path}"
        
        try:
            response = requests.head(url, headers=self._get_headers(), timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_file_url(self, remote_path: str) -> str:
        """
        Obtiene la URL pública de un archivo
        
        Args:
            remote_path: Ruta del archivo
        
        Returns:
            URL pública del archivo
        """
        remote_path = remote_path.lstrip('/')
        return f"{self.storage_url.rstrip('/')}/{remote_path}"


def upload_pdf_to_bunny(pdf_content: bytes | BinaryIO, filename: str) -> Optional[str]:
    """
    Función helper para subir un PDF a Bunny Storage
    
    Args:
        pdf_content: Contenido del PDF (bytes o file-like object)
        filename: Nombre del archivo (ej: 'comprobantes/venta_123.pdf')
    
    Returns:
        URL pública del PDF o None si falla
    """
    try:
        client = BunnyStorageClient()
        return client.upload_file(pdf_content, filename, content_type='application/pdf')
    except ValueError as e:
        logger.error(f"Error de configuración de Bunny: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al subir PDF a Bunny: {e}")
        return None


def upload_image_to_bunny(image_content: bytes | BinaryIO, filename: str) -> Optional[str]:
    """
    Función helper para subir una imagen a Bunny Storage
    
    Args:
        image_content: Contenido de la imagen (bytes o file-like object)
        filename: Nombre del archivo (ej: 'productos/producto_123.jpg')
    
    Returns:
        URL pública de la imagen o None si falla
    """
    try:
        client = BunnyStorageClient()
        # Detectar content-type por extensión
        content_type = 'image/jpeg'
        if filename.endswith('.png'):
            content_type = 'image/png'
        elif filename.endswith('.webp'):
            content_type = 'image/webp'
        
        return client.upload_file(image_content, filename, content_type=content_type)
    except ValueError as e:
        logger.error(f"Error de configuración de Bunny: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al subir imagen a Bunny: {e}")
        return None

