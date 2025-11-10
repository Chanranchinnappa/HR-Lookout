"""
Django Token Authentication + Tenant-aware Middleware
Replaces Keycloak with Django-native authentication
"""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


class TokenAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate requests using Django REST Framework tokens
    Also sets tenant context from authenticated user
    """

    def process_request(self, request):
        """
        Process incoming request and attach authenticated user + tenant
        """
        # Skip authentication for specific paths
        if self._should_skip_auth(request.path):
            return None

        # Extract token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            
            try:
                # Validate token (no select_related - User doesn't have organization)
                token = Token.objects.select_related('user').get(key=token_key)
                request.user = token.user
                request.auth = token
                
                # Try to get UserProfile for tenant context
                try:
                    profile = token.user.userprofile
                    request.current_tenant = profile.organization
                    request.is_super_admin = profile.is_super_admin
                except Exception:
                    request.current_tenant = None
                    request.is_super_admin = False
                    
            except Token.DoesNotExist:
                # Invalid token
                request.user = AnonymousUser()
                request.current_tenant = None
                request.is_super_admin = False
        else:
            # No token provided
            request.user = AnonymousUser()
            request.current_tenant = None
            request.is_super_admin = False

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
            '/api/v1/auth/login/',
            '/api/v1/auth/register/',
        ]
        return any(path.startswith(skip_path) for skip_path in skip_paths)


class TenantMiddleware(MiddlewareMixin):
    """
    Additional tenant context middleware
    Ensures tenant is set even for session-based auth
    """

    def process_request(self, request):
        """Extract tenant from authenticated user (for non-token auth)"""
        if not hasattr(request, 'current_tenant') and hasattr(request, 'user') and request.user.is_authenticated:
            # Try to get UserProfile
            try:
                profile = request.user.userprofile
                request.current_tenant = profile.organization
                request.is_super_admin = profile.is_super_admin
            except Exception:
                request.current_tenant = None
                request.is_super_admin = False
        elif not hasattr(request, 'current_tenant'):
            request.current_tenant = None
            request.is_super_admin = False

        return None
