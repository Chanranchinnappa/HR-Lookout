"""
Organization and Department models
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    """
    Organization/Company entity
    """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    legal_name = models.CharField(max_length=255)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    
    # Tax & Legal
    tax_id = models.CharField(max_length=50, unique=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Settings
    fiscal_year_start = models.DateField()
    currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Logo
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Department(models.Model):
    """
    Department within an organization
    """
    
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    # Hierarchy
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments'
    )
    
    # Head of Department
    head = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    
    # Cost Center
    cost_center = models.CharField(max_length=50, blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'departments'
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"
