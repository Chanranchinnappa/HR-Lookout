"""
Audit Middleware - Automatically log API requests
"""

from django.utils.deprecation import MiddlewareMixin
from .logger import get_audit_logger
import json


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware to automatically audit API requests
    """
    
    def process_response(self, request, response):
        """
        Log audit trail after request is processed
        """
        # Only audit API requests
        if not request.path.startswith('/api/'):
            return response
        
        # Only audit mutating operations
        if request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return response
        
        # Only audit successful requests
        if response.status_code >= 400:
            return response
        
        # Skip if user is not authenticated
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return response
        
        try:
            audit_logger = get_audit_logger()
            
            action = self._map_method_to_action(request.method)
            resource_type = self._extract_resource_type(request.path)
            
            audit_logger.log(
                action=action,
                user_id=request.user.id,
                resource_type=resource_type,
                metadata={
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                },
                request=request,
            )
        except Exception:
            # Fail silently - don't break the request
            pass
        
        return response
    
    def _map_method_to_action(self, method):
        """Map HTTP method to audit action"""
        mapping = {
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE',
        }
        return mapping.get(method, 'UNKNOWN')
    
    def _extract_resource_type(self, path):
        """Extract resource type from API path"""
        # Example: /api/v1/employees/ -> Employee
        parts = path.strip('/').split('/')
        if len(parts) >= 3 and parts[0] == 'api':
            resource = parts[2].rstrip('s').capitalize()
            return resource
        return 'Unknown'
