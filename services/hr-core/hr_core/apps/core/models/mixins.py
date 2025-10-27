from django.db import models


class TenantAwareManager(models.Manager):
    """
    Custom manager that can filter by organization based on user context
    Provides a for_user() method to automatically scope queries
    """
    def get_queryset(self):
        return super().get_queryset()
    
    def for_user(self, user):
        """
        Filter queryset based on user's role and organization
        - Super admins see everything
        - Others see only their organization's data
        """
        queryset = self.get_queryset()
        
        # If user has is_super_admin attribute and it's True
        if hasattr(user, 'is_super_admin') and user.is_super_admin:
            return queryset
        
        # If user has organization_id, filter by it
        if hasattr(user, 'organization_id') and user.organization_id:
            return queryset.filter(organization_id=user.organization_id)
        
        # No organization = no data (safety measure)
        return queryset.none()


class TenantAwareModelMixin(models.Model):
    """
    Mixin that adds tenant-aware manager to models
    Use this with TenantAwareModel for complete multi-tenancy
    """
    objects = TenantAwareManager()
    
    class Meta:
        abstract = True
