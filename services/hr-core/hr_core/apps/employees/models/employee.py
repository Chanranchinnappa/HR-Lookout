"""
Employee model with auto-generated unique IDs
"""
from django.db import models
from django.utils.crypto import get_random_string
from hr_core.apps.core.models import TenantAwareModel


class EmploymentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    ON_LEAVE = 'ON_LEAVE', 'On Leave'
    TERMINATED = 'TERMINATED', 'Terminated'


class Employee(TenantAwareModel):
    """
    Employee model - represents individual employees
    Unique ID format: EMP-{org_code}-{dept_code}-{random}
    """
    # Auto-generated unique employee ID
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        help_text="Auto-generated unique employee identifier (EMP-XXXX-DEPT-123456)"
    )
    
    # Personal information
    first_name = models.CharField(max_length=100, help_text="First name")
    middle_name = models.CharField(max_length=100, blank=True, help_text="Middle name")
    last_name = models.CharField(max_length=100, help_text="Last name")
    
    email = models.EmailField(unique=True, help_text="Work email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date of birth")
    
    # Employment details
    hire_date = models.DateField(help_text="Date of hire")
    termination_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of termination (if applicable)"
    )
    
    # Organizational relationships
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        help_text="Department"
    )
    
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_reports',
        help_text="Direct manager/supervisor"
    )
    
    # Job details
    job_title = models.CharField(max_length=200, help_text="Job title")
    employment_type = models.CharField(
        max_length=50,
        default='FULL_TIME',
        help_text="Employment type (FULL_TIME, PART_TIME, CONTRACT)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
        help_text="Employment status"
    )
    
    # Address
    address_line1 = models.CharField(max_length=255, blank=True, help_text="Address line 1")
    address_line2 = models.CharField(max_length=255, blank=True, help_text="Address line 2")
    city = models.CharField(max_length=100, blank=True, help_text="City")
    state = models.CharField(max_length=100, blank=True, help_text="State/Province")
    postal_code = models.CharField(max_length=20, blank=True, help_text="Postal code")
    country = models.CharField(max_length=100, blank=True, help_text="Country")
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['department', 'status']),
            models.Index(fields=['manager']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"
    
    def save(self, *args, **kwargs):
        # Generate unique employee ID on creation
        if not self.employee_id:
            org_code = self.organization.org_unique_id.split('-')[1][:4] if self.organization else 'NONE'
            dept_code = self.department.code if self.department else 'NODEPT'
            random_digits = get_random_string(6, '0123456789')
            self.employee_id = f"EMP-{org_code}-{dept_code}-{random_digits}"
        
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        """Get employee's full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self):
        """Check if employee is currently active"""
        return self.status == EmploymentStatus.ACTIVE
    
    @property
    def direct_reports_count(self):
        """Count of direct reports"""
        return self.direct_reports.filter(status=EmploymentStatus.ACTIVE).count()

