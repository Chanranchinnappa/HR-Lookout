from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models
    Adds created_at and updated_at timestamps automatically
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class TenantAwareModel(BaseModel):
    """
    Abstract model that adds organization-level multi-tenancy
    All models inheriting this will be automatically filtered by organization
    """
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        help_text='Organization this record belongs to'
    )
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['organization']),
        ]
