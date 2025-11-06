"""
Authentication and health check views
"""

from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import redis
from pymongo import MongoClient


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Get current authenticated user information
    
    Returns user details from Keycloak token including roles and permissions.
    """
    user = request.user
    
    # Convert KeycloakUser to dictionary
    if hasattr(user, 'to_dict'):
        user_data = user.to_dict()
    else:
        # Fallback for regular Django users
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    
    return Response({
        'user': user_data,
        'authenticated': True,
    })


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

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


# ============================================================================
# INTERNAL HEALTH CHECK HELPERS
# ============================================================================

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
