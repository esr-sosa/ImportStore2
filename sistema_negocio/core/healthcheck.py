"""
Healthcheck endpoint para Railway y monitoreo
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def healthcheck(request):
    """
    Endpoint de healthcheck para Railway y monitoreo
    
    Returns:
        - 200 OK: Si todo está funcionando
        - 503 Service Unavailable: Si hay problemas
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    overall_healthy = True
    
    # Check de base de datos
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['checks']['database'] = 'healthy'
    except Exception as e:
        logger.error(f"Database healthcheck failed: {e}")
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        overall_healthy = False
    
    # Check de Bunny Storage (si está configurado)
    use_bunny = __import__('os').getenv('USE_BUNNY_STORAGE', 'false').lower() == 'true'
    if use_bunny:
        try:
            from core.utils_bunny import BunnyStorageClient
            client = BunnyStorageClient()
            # Intentar verificar conexión (verificar que existe una zona)
            if client.storage_zone:
                health_status['checks']['bunny_storage'] = 'healthy'
            else:
                health_status['checks']['bunny_storage'] = 'unhealthy: not configured'
                overall_healthy = False
        except Exception as e:
            logger.error(f"Bunny Storage healthcheck failed: {e}")
            health_status['checks']['bunny_storage'] = f'unhealthy: {str(e)}'
            overall_healthy = False
    
    if not overall_healthy:
        health_status['status'] = 'unhealthy'
        return JsonResponse(health_status, status=503)
    
    return JsonResponse(health_status, status=200)

