"""
Organization model - multi-tenant root entity
"""
import uuid
from django.db import models


class Organization(models.Model):
    """
    Organization model - represents companies/entities using the system
    This is the top-level tenant model for multi-tenancy
    Each client gets their own organization
    """
    # Unique system-generated ID (visible only to super admin)
    org_unique_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        help_text='System-generated unique org ID (ORG-XXXXXXXX)'
    )
    
    # Basic info
    name = models.CharField(max_length=200, help_text="Organization name")
    legal_name = models.CharField(max_length=200, help_text="Legal/registered name")
    
    email = models.EmailField(unique=True, help_text="Organization contact email")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    website = models.URLField(blank=True, help_text="Website URL")
    
    # Address fields
    address_line1 = models.CharField(max_length=255, help_text="Address line 1")
    address_line2 = models.CharField(max_length=255, blank=True, help_text="Address line 2")
    city = models.CharField(max_length=100, help_text="City")
    state = models.CharField(max_length=100, help_text="State/Province")
    postal_code = models.CharField(max_length=20, help_text="Postal/ZIP code")
    country = models.CharField(max_length=100, default='United States', help_text="Country")
    
    # Registration details
    tax_id = models.CharField(max_length=50, unique=True, help_text="Tax ID/EIN")
    registration_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Business registration number"
    )
    
    # Operational details
    fiscal_year_start = models.DateField(help_text="Fiscal year start date")
    currency = models.CharField(max_length=3, default='USD', help_text="Currency code (USD, EUR, INR, etc.)")
    timezone = models.CharField(max_length=50, default='UTC', help_text="Timezone")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Is organization active")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['name']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        indexes = [
            models.Index(fields=['org_unique_id']),
            models.Index(fields=['is_active', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.org_unique_id})"
    
    def save(self, *args, **kwargs):
        # Generate unique org ID on creation
        if not self.org_unique_id:
            self.org_unique_id = f"ORG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def employee_count(self):
        """Get total number of employees in this organization"""
        return self.employee_set.count()
    
    @property
    def department_count(self):
        """Get total number of departments in this organization"""
        return self.department_set.count()
    
    @property
    def active_employee_count(self):
        """Get count of active employees"""
        return self.employee_set.filter(status='ACTIVE').count()
