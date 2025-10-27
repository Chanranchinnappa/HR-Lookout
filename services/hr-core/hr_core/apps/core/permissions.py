from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Permission class: Only Super Admins can access
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'is_super_admin') and
            request.user.is_super_admin
        )


class IsOrgAdmin(permissions.BasePermission):
    """
    Permission class: Organization Admins can access their own organization data
    Super Admins can access everything
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Super admin has access
        if hasattr(request.user, 'is_super_admin') and request.user.is_super_admin:
            return True
        
        # Org admin has access
        if hasattr(request.user, 'is_org_admin') and request.user.is_org_admin:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Super admin can access everything
        if hasattr(request.user, 'is_super_admin') and request.user.is_super_admin:
            return True
        
        # Check if object belongs to user's organization
        if hasattr(obj, 'organization_id') and hasattr(request.user, 'organization_id'):
            return obj.organization_id == request.user.organization_id
        
        # For Organization objects themselves
        if obj.__class__.__name__ == 'Organization':
            return obj.id == request.user.organization_id
        
        return False


class TenantPermission(permissions.BasePermission):
    """
    Multi-tenant aware permission
    - Super Admin: Full access to all organizations
    - Org Admin: Full access to their organization
    - Manager/Employee: Read-only access to their organization
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Super admin bypass - can do anything
        if hasattr(user, 'is_super_admin') and user.is_super_admin:
            return True
        
        # Get organization from object
        org_id = None
        if hasattr(obj, 'organization_id'):
            org_id = obj.organization_id
        elif obj.__class__.__name__ == 'Organization':
            org_id = obj.id
        
        # Check user belongs to same organization
        if not hasattr(user, 'organization_id') or org_id != user.organization_id:
            return False
        
        # Write permissions only for org admin
        if request.method not in permissions.SAFE_METHODS:
            return hasattr(user, 'is_org_admin') and user.is_org_admin
        
        # Read access for everyone in the organization
        return True
