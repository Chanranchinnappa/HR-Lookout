"""
Django Authentication Middleware with Tenant/Organization isolation
Handles token authentication and request context
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)


class TokenAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate requests using Django REST Framework tokens
    Also sets tenant/organization context from authenticated user
    """

    def process_request(self, request):
        """
        Process incoming request and attach authenticated user + tenant context
        """
        # Skip authentication for specific paths
        if self._should_skip_auth(request.path):
            return None

        # Extract token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            
            try:
                # Validate token and get user
                token = Token.objects.select_related('user').get(key=token_key)
                user = token.user

                # Check if user is active
                if not user.is_active:
                    return JsonResponse(
                        {'error': 'User account is disabled'},
                        status=403
                    )

                # Attach user to request
                request.user = user

                # Attach user profile to request for easy access
                try:
                    request.user_profile = user.userprofile
                    
                    # Set organization context for tenant isolation
                    if hasattr(request.user_profile, 'organization'):
                        request.organization = request.user_profile.organization
                        request.organization_id = request.user_profile.organization.id if request.user_profile.organization else None
                    else:
                        request.organization = None
                        request.organization_id = None

                    logger.debug(f"Authenticated user: {user.username}, org: {request.organization_id}")

                except Exception as e:
                    logger.error(f"Error loading user profile: {str(e)}")
                    request.user_profile = None
                    request.organization = None
                    request.organization_id = None

            except Token.DoesNotExist:
                logger.warning(f"Invalid token attempted: {token_key[:10]}...")
                request.user = AnonymousUser()
                request.organization = None
                request.organization_id = None

        else:
            # No token provided
            request.user = AnonymousUser()
            request.organization = None
            request.organization_id = None

        return None

    def _should_skip_auth(self, path):
        """
        Check if authentication should be skipped for this path
        """
        skip_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/api/v1/auth/login/',
            '/api/v1/auth/register/',
            '/api/v1/auth/health/',
            '/health/',
        ]
        
        return any(path.startswith(skip_path) for skip_path in skip_paths)


class TenantIsolationMiddleware(MiddlewareMixin):
    """
    Middleware to enforce tenant/organization isolation
    Ensures users can only access data from their organization
    """

    def process_request(self, request):
        """
        Validate that user has access to requested organization data
        """
        # Skip for non-authenticated requests
        if not hasattr(request, 'user') or request.user.is_anonymous:
            return None

        # Skip for superadmins
        if hasattr(request, 'user_profile') and request.user_profile:
            if request.user_profile.is_super_admin or request.user.is_superuser:
                return None

        # Check if request includes organization_id parameter
        org_id_from_request = request.GET.get('organization_id') or request.POST.get('organization_id')
        
        if org_id_from_request:
            # Ensure user can only access their own organization
            if hasattr(request, 'organization_id') and request.organization_id:
                if str(org_id_from_request) != str(request.organization_id):
                    logger.warning(
                        f"Tenant isolation violation: User {request.user.username} "
                        f"attempted to access org {org_id_from_request} "
                        f"but belongs to org {request.organization_id}"
                    )
                    return JsonResponse(
                        {'error': 'Access denied: Cannot access other organization data'},
                        status=403
                    )

        return None


class RolePermissionMiddleware(MiddlewareMixin):
    """
    Middleware to check role-based permissions on views
    Can be used to enforce permissions at middleware level
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check if user has required role/permission for view
        """
        # Skip for anonymous users (handled by permission classes)
        if not hasattr(request, 'user') or request.user.is_anonymous:
            return None

        # Check if view has required_permission attribute
        required_permission = getattr(view_func, 'required_permission', None)
        
        if required_permission:
            # Check if user has the required permission
            if hasattr(request, 'user_profile') and request.user_profile:
                if not request.user_profile.has_permission(required_permission):
                    logger.warning(
                        f"Permission denied: User {request.user.username} "
                        f"lacks permission {required_permission}"
                    )
                    return JsonResponse(
                        {'error': f'Permission denied: {required_permission} required'},
                        status=403
                    )

        # Check if view has required_role attribute
        required_role = view_kwargs.get('required_role')
        
        if required_role:
            if hasattr(request, 'user_profile') and request.user_profile:
                user_role = request.user_profile.role
                if not user_role or user_role.name != required_role:
                    logger.warning(
                        f"Role denied: User {request.user.username} "
                        f"lacks role {required_role}"
                    )
                    return JsonResponse(
                        {'error': f'Access denied: {required_role} role required'},
                        status=403
                    )

        return None


class AuditLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all API requests for audit trail
    """

    def process_request(self, request):
        """
        Log incoming request details
        """
        # Only log API requests
        if request.path.startswith('/api/'):
            user_info = 'anonymous'
            org_info = 'none'

            if hasattr(request, 'user') and request.user.is_authenticated:
                user_info = f"{request.user.username} (ID: {request.user.id})"
                
                if hasattr(request, 'organization_id') and request.organization_id:
                    org_info = str(request.organization_id)

            logger.info(
                f"API Request: {request.method} {request.path} | "
                f"User: {user_info} | Org: {org_info} | "
                f"IP: {self._get_client_ip(request)}"
            )

        return None

    def _get_client_ip(self, request):
        """
        Get client IP address from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
