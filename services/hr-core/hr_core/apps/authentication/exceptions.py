"""
Custom exceptions for authentication and RBAC
"""

from django.core.exceptions import PermissionDenied


class AuthenticationException(Exception):
    """Base exception for authentication errors"""
    pass


class RBACPermissionDenied(PermissionDenied):
    """
    Custom exception for RBAC permission denied
    Raised when user lacks required permissions
    """
    def __init__(self, permission, message=None):
        self.permission = permission
        if message is None:
            message = f"Permission denied: {permission} required"
        super().__init__(message)


class InvalidRoleException(Exception):
    """
    Exception raised when invalid role is specified or assigned
    """
    def __init__(self, role, message=None):
        self.role = role
        if message is None:
            message = f"Invalid role: {role}"
        super().__init__(message)


class InsufficientPermissionsException(Exception):
    """
    Exception raised when user has insufficient permissions for an action
    """
    def __init__(self, required_permissions, message=None):
        self.required_permissions = required_permissions
        if message is None:
            message = f"Insufficient permissions. Required: {', '.join(required_permissions)}"
        super().__init__(message)


class TenantIsolationViolation(PermissionDenied):
    """
    Exception raised when user attempts to access data from another organization
    """
    def __init__(self, message="Cannot access data from other organizations"):
        super().__init__(message)


class InvalidTokenException(AuthenticationException):
    """
    Exception raised when authentication token is invalid or expired
    """
    def __init__(self, message="Invalid or expired authentication token"):
        super().__init__(message)


class UserInactiveException(AuthenticationException):
    """
    Exception raised when user account is inactive
    """
    def __init__(self, message="User account is inactive"):
        super().__init__(message)


class PasswordValidationException(Exception):
    """
    Exception raised when password does not meet validation requirements
    """
    def __init__(self, errors, message="Password validation failed"):
        self.errors = errors
        super().__init__(message)
