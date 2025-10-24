"""
Employee models for PostgreSQL
"""

from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    """
    Core employee information stored in PostgreSQL
    """
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ON_LEAVE', 'On Leave'),
        ('TERMINATED', 'Terminated'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full-Time'),
        ('PART_TIME', 'Part-Time'),
        ('CONTRACT', 'Contract'),
        ('INTERN', 'Intern'),
    ]
    
    # Identity
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    keycloak_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact Information
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    personal_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    
    # Employment Details
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='employees'
    )
    department = models.ForeignKey(
        'organizations.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    job_title = models.CharField(max_length=200)
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='ACTIVE'
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='FULL_TIME'
    )
    
    # Dates
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    
    # Reporting Structure (stored in Neo4j as well)
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_reports'
    )
    
    # Address
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default='United States')
    
    # Profile
    profile_picture = models.CharField(max_length=500, blank=True, null=True)  # S3/MinIO URL
    bio = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
            models.Index(fields=['employment_status']),
            models.Index(fields=['organization', 'department']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
    
    @property
    def full_name(self):
        """Return full name"""
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{middle} {self.last_name}"
    
    @property
    def is_active(self):
        """Check if employee is active"""
        return self.employment_status == 'ACTIVE'


class Document(models.Model):
    """
    Employee documents (stored metadata in PostgreSQL, files in MinIO/S3)
    """
    
    DOCUMENT_TYPE_CHOICES = [
        ('CONTRACT', 'Employment Contract'),
        ('ID_PROOF', 'ID Proof'),
        ('RESUME', 'Resume/CV'),
        ('CERTIFICATE', 'Certificate'),
        ('POLICY', 'Policy Document'),
        ('OTHER', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # File information
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # in bytes
    file_type = models.CharField(max_length=50)  # MIME type
    file_url = models.CharField(max_length=500)  # S3/MinIO URL
    
    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'employee_documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} ({self.employee.full_name})"
