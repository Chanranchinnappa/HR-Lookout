"""
Keycloak Authentication Backend for Django REST Framework
"""

import jwt
from jwt import PyJWKClient
from rest_framework import authentication, exceptions
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from keycloak import KeycloakOpenID


class KeycloakUser:
    """
    Custom user object to represent Keycloak user
    """
    
    def __init__(self, token_payload):
        self.id = token_payload.get('sub')
        self.username = token_payload.get('preferred_username', '')
        self.email = token_payload.get('email', '')
        self.first_name = token_payload.get('given_name', '')
        self.last_name = token_payload.get('family_name', '')
        self.roles = token_payload.get('realm_access', {}).get('roles', [])
        self.groups = token_payload.get('groups', [])
        self.is_authenticated = True
        self.is_anonymous = False
        self.token_payload = token_payload
        
        # Extract organization_id from custom attributes if present
        self._organization_id = token_payload.get('organization_id')
    
    def __str__(self):
        return self.username or self.email
    
    def has_role(self, role):
        """Check if user has a specific role"""
        return role in self.roles
    
    def has_any_role(self, roles):
        """Check if user has any of the specified roles"""
        return any(role in self.roles for role in roles)
    
    def has_all_roles(self, roles):
        """Check if user has all of the specified roles"""
        return all(role in self.roles for role in roles)
    
    @property
    def is_admin(self):
        """Generic admin check (for backward compatibility)"""
        return self.has_role('hr_admin')
    
    @property
    def is_manager(self):
        """Check if user is manager or admin"""
        return self.has_any_role(['hr_admin', 'hr_manager'])
    
    # NEW: Properties for permission classes compatibility
    @property
    def is_super_admin(self):
        """Check if user is super admin (cross-tenant access)"""
        return self.has_role('super_admin')
    
    @property
    def is_org_admin(self):
        """Check if user is organization admin"""
        return self.has_any_role(['hr_admin', 'org_admin'])
    
    @property
    def organization_id(self):
        """Get user's organization ID from token claims"""
        return self._organization_id
    
    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'roles': self.roles,
            'groups': self.groups,
            'is_super_admin': self.is_super_admin,
            'is_org_admin': self.is_org_admin,
            'organization_id': self.organization_id,
        }


class KeycloakAuthentication(authentication.BaseAuthentication):
    """
    Keycloak JWT Authentication for DRF
    """
    
    def __init__(self):
        self.keycloak_config = settings.KEYCLOAK_CONFIG
        self.keycloak_openid = KeycloakOpenID(
            server_url=self.keycloak_config['server_url'],
            realm_name=self.keycloak_config['realm'],
            client_id=self.keycloak_config['client_id'],
            client_secret_key=self.keycloak_config['client_secret'],
        )
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        try:
            # Extract token from "Bearer <token>"
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                return None
            
            # Validate and decode token
            token_payload = self._validate_token(token)
            
            # Create Keycloak user object
            user = KeycloakUser(token_payload)
            
            return (user, token)
        
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid authorization header format')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')
    
    def _validate_token(self, token):
        """
        Validate JWT token with Keycloak
        """
        try:
            # Get public key from Keycloak
            public_key = f"-----BEGIN PUBLIC KEY-----\n{self.keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"
            
            # Decode and validate token
            options = {
                'verify_signature': True,
                'verify_aud': False,
                'verify_exp': True,
            }
            
            token_payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options=options,
            )
            
            return token_payload
        
        except Exception as e:
            raise jwt.InvalidTokenError(f'Token validation failed: {str(e)}')
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the WWW-Authenticate
        header in a 401 Unauthenticated response.
        """
        return 'Bearer realm="hr-lookout"'
