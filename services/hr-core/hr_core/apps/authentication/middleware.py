"""
Keycloak Authentication Middleware
"""

from django.utils.deprecation import MiddlewareMixin
from .backends import KeycloakAuthentication


class KeycloakAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate requests using Keycloak
    """
    
    def process_request(self, request):
        """
        Process incoming request and attach Keycloak user if authenticated
        """
        # Skip authentication for specific paths
        if self._should_skip_auth(request.path):
            return None
        
        # Attempt Keycloak authentication
        authenticator = KeycloakAuthentication()
        try:
            auth_result = authenticator.authenticate(request)
            if auth_result:
                request.user, request.auth = auth_result
        except Exception:
            # Authentication failed, user remains anonymous
            pass
        
        return None
    
    def _should_skip_auth(self, path):
        """
        Determine if authentication should be skipped for this path
        """
        skip_paths = [
            '/admin/',
            '/health/',
            '/static/',
            '/media/',
        ]
        return any(path.startswith(skip_path) for skip_path in skip_paths)
