from django.db import models
from hr_core.apps.core.models import TenantAwareModel


class EmploymentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    ON_LEAVE = 'ON_LEAVE', 'On Leave'
    TERMINATED = 'TERMINATED', 'Terminated'


class Employee(TenantAwareModel):
    """
    Employee model - represents individual employees
    """
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique employee identifier"
    )
    
    first_name = models.CharField(max_length=100, help_text="First name")
    middle_name = models.CharField(max_length=100, blank=True, help_text="Middle name")
    last_name = models.CharField(max_length=100, help_text="Last name")
    
    email = models.EmailField(unique=True, help_text="Work email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date of birth")
    
    hire_date = models.DateField(help_text="Date of hire")
    termination_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of termination (if applicable)"
    )
    
    job_title = models.CharField(max_length=100, help_text="Current job title")
    
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        help_text="Department this employee belongs to"
    )
    
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_reports',
        help_text="Direct manager/supervisor"
    )
    
    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
        help_text="Current employment status"
    )
    
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Current salary"
    )
    
    address_line1 = models.CharField(max_length=255, blank=True, help_text="Address line 1")
    address_line2 = models.CharField(max_length=255, blank=True, help_text="Address line 2")
    city = models.CharField(max_length=100, blank=True, help_text="City")
    state = models.CharField(max_length=100, blank=True, help_text="State/Province")
    postal_code = models.CharField(max_length=20, blank=True, help_text="Postal/ZIP code")
    country = models.CharField(max_length=100, default='India', help_text="Country")
    
    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Emergency contact name"
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Emergency contact phone"
    )
    emergency_contact_relationship = models.CharField(
        max_length=50,
        blank=True,
        help_text="Relationship to emergency contact"
    )
    
    class Meta:
        db_table = 'employees'
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
            models.Index(fields=['employment_status']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
    
    @property
    def full_name(self):
        """Get employee's full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self):
        """Check if employee is currently active"""
        return self.employment_status == EmploymentStatus.ACTIVE
