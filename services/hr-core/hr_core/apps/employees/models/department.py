"""
Department model with hierarchical code generation
"""
from django.db import models
from django.core.exceptions import ValidationError
from hr_core.apps.core.models import TenantAwareModel


class Department(TenantAwareModel):
    """
    Department model - organizational units within a company
    Code format: HR03 (parent), HR032 (child), HR0321 (grandchild)
    """
    name = models.CharField(max_length=100, help_text="Department name")
    
    # Auto-generated hierarchical code
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Auto-generated unique department code (e.g., HR03, HR032)"
    )
    
    description = models.TextField(blank=True, help_text="Department description")
    
    # Department head
    head = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_department',
        help_text="Department head/manager"
    )
    
    # Hierarchical structure
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments',
        help_text="Parent department (for hierarchy)"
    )
    
    # Accounting details
    cost_center = models.CharField(
        max_length=50,
        blank=True,
        help_text="Cost center code for accounting"
    )
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Is department active")
    
    class Meta:
        db_table = 'departments'
        ordering = ['code']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['organization', 'is_active']),
            models.Index(fields=['parent_department']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def save(self, *args, **kwargs):
        # Auto-generate hierarchical department code
        if not self.pk and not self.code:
            if self.parent_department:
                # Child department: append number to parent code
                parent_code = self.parent_department.code
                sibling_count = Department.objects.filter(
                    organization=self.organization,
                    parent_department=self.parent_department
                ).count()
                self.code = f"{parent_code}{sibling_count + 1}"
            else:
                # Root department: use abbreviated name + count
                root_count = Department.objects.filter(
                    organization=self.organization,
                    parent_department__isnull=True
                ).count()
                abbrev = ''.join([c for c in self.name.upper() if c.isalpha()])[:3]
                self.code = f"{abbrev}{root_count + 1:02d}"
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate department hierarchy"""
        if self.parent_department:
            # Prevent circular references
            if self.parent_department == self:
                raise ValidationError("Department cannot be its own parent")
            
            # Ensure parent is in same organization
            if self.parent_department.organization != self.organization:
                raise ValidationError("Parent department must be in same organization")
    
    @property
    def level(self):
        """Get department hierarchy level (0 = root)"""
        if not self.parent_department:
            return 0
        return self.parent_department.level + 1
    
    @property
    def employee_count(self):
        """Get total employee count (including sub-departments)"""
        from .employee import Employee, EmploymentStatus
        count = self.employees.filter(status=EmploymentStatus.ACTIVE).count()
        
        # Add employees from sub-departments
        for sub_dept in self.sub_departments.filter(is_active=True):
            count += sub_dept.employee_count
        
        return count
    
    @property
    def full_path(self):
        """Get full department path (e.g., 'Engineering > Backend > API Team')"""
        if not self.parent_department:
            return self.name
        return f"{self.parent_department.full_path} > {self.name}"
