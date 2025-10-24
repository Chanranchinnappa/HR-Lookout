"""
Authentication and health check views
"""

from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import redis
from pymongo import MongoClient


def health_check(request):
    """
    Overall health check endpoint
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'hr-core',
        'version': settings.SERVICE_VERSION if hasattr(settings, 'SERVICE_VERSION') else '1.0.0',
    })


def readiness_check(request):
    """
    Readiness check - verifies all dependencies are available
    """
    checks = {
        'postgres': _check_postgres(),
        'redis': _check_redis(),
        'mongodb': _check_mongodb(),
    }
    
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    
    return JsonResponse({
        'ready': all_ready,
        'checks': checks,
    }, status=status_code)


def liveness_check(request):
    """
    Liveness check - verifies the service is alive
    """
    return JsonResponse({
        'alive': True,
    })


def _check_postgres():
    """Check PostgreSQL connection"""
    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False


def _check_redis():
    """Check Redis connection"""
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            socket_connect_timeout=2,
        )
        redis_client.ping()
        return True
    except Exception:
        return False


def _check_mongodb():
    """Check MongoDB connection"""
    try:
        mongo_settings = settings.MONGODB_SETTINGS
        client = MongoClient(
            host=mongo_settings['host'],
            port=mongo_settings['port'],
            username=mongo_settings['username'],
            password=mongo_settings['password'],
            serverSelectionTimeoutMS=2000,
        )
        client.server_info()
        return True
    except Exception:
        return False
