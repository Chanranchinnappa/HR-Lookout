"""
Authentication models - Django User + Profile pattern
Uses Django's built-in User model with separate UserProfile
No more custom User model = No circular dependencies
"""
from django.db import models
from django.contrib.auth.models import User
from hr_core.apps.core.models import BaseModel


class RoleLevel(models.TextChoices):
    """Hierarchical role levels"""
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    ORG_ADMIN = 'ORG_ADMIN', 'Organization Admin'
    DEPT_ADMIN = 'DEPT_ADMIN', 'Department Admin'
    MANAGER = 'MANAGER', 'Manager'
    EMPLOYEE = 'EMPLOYEE', 'Employee'


class Role(BaseModel):
    """
    User roles with hierarchical permissions
    Can be organization-specific or system-wide
    """
    name = models.CharField(max_length=100, help_text="Role name")
    level = models.CharField(
        max_length=20,
        choices=RoleLevel.choices,
        default=RoleLevel.EMPLOYEE,
        help_text="Role hierarchy level"
    )
    description = models.TextField(blank=True, help_text="Role description")
    is_active = models.BooleanField(default=True, help_text="Is role active")
    
    # Tenant isolation
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='roles',
        help_text="Organization (null for system-wide roles)"
    )
    
    class Meta:
        db_table = 'roles'
        ordering = ['name']
        unique_together = [['name', 'organization']]
        indexes = [
            models.Index(fields=['level', 'is_active']),
            models.Index(fields=['organization', 'is_active']),
        ]
    
    def __str__(self):
        org_suffix = f" ({self.organization.name})" if self.organization else " (System-wide)"
        return f"{self.name}{org_suffix}"


class UserProfile(BaseModel):
    """
    Extended user profile linked to Django's built-in User
    Contains organization, role, and HR-specific fields
    
    This pattern avoids custom User model circular dependency issues
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Django User"
    )
    
    # Organization & Role
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profiles',
        help_text="User's organization"
    )
    
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profiles',
        help_text="User's role"
    )
    
    # Employee link
    employee = models.OneToOneField(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profile',
        help_text="Linked employee record"
    )
    
    # Additional fields
    is_super_admin = models.BooleanField(
        default=False,
        help_text="System-wide superadmin (can manage all orgs)"
    )
    
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    
    is_2fa_enabled = models.BooleanField(
        default=False,
        help_text="Two-factor authentication enabled"
    )
    
    class Meta:
        db_table = 'user_profiles'
        ordering = ['user__username']
        indexes = [
            models.Index(fields=['organization', 'role']),
            models.Index(fields=['is_super_admin']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    @property
    def is_org_admin(self):
        """Check if user is an org admin"""
        return self.role and self.role.level == RoleLevel.ORG_ADMIN
    
    @property
    def is_dept_admin(self):
        """Check if user is a dept admin"""
        return self.role and self.role.level == RoleLevel.DEPT_ADMIN
    
    @property
    def can_manage_organization(self):
        """Check if user can manage their organization"""
        return self.is_super_admin or self.is_org_admin
    
    @property
    def can_manage_department(self):
        """Check if user can manage department"""
        return self.is_super_admin or self.is_org_admin or self.is_dept_admin
