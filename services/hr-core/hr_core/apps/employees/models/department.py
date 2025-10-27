from django.db import models
from django.core.exceptions import ValidationError
from hr_core.apps.core.models import TenantAwareModel


class Department(TenantAwareModel):
    """
    Department model - organizational units within a company
    """
    name = models.CharField(max_length=100, help_text="Department name")
    code = models.CharField(max_length=20, unique=True, help_text="Unique department code")
    description = models.TextField(blank=True, help_text="Department description")
    
    head = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_department',
        help_text="Department head/manager"
    )
    
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments',
        help_text="Parent department (for hierarchy)"
    )
    
    cost_center = models.CharField(
        max_length=50,
        blank=True,
        help_text="Cost center code for accounting"
    )
    
    is_active = models.BooleanField(default=True, help_text="Is department active")
    
    class Meta:
        db_table = 'departments'
        ordering = ['name']
        unique_together = [['organization', 'code']]
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def employee_count(self):
        """Get number of active employees in this department"""
        return self.employees.filter(employment_status='ACTIVE').count()
    
    def can_delete(self, user):
        """
        Check if department can be deleted based on user role
        Returns: (can_delete: bool, reason: str)
        """
        employee_count = self.employee_count
        
        # Super admin can always delete with confirmation
        if hasattr(user, 'is_super_admin') and user.is_super_admin:
            if employee_count > 0:
                return (True, f"Warning: {employee_count} employees will be affected")
            return (True, "")
        
        # Org admin must reassign employees first
        if hasattr(user, 'is_org_admin') and user.is_org_admin:
            if employee_count > 0:
                return (False, f"Cannot delete: {employee_count} employees are assigned. Reassign them first.")
            return (True, "")
        
        return (False, "Insufficient permissions to delete department")
    
    def delete(self, using=None, keep_parents=False, user=None):
        """Override delete method with role-based validation"""
        if user:
            can_delete, reason = self.can_delete(user)
            if not can_delete:
                raise ValidationError(reason)
        
        return super().delete(using=using, keep_parents=keep_parents)
