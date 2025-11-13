"""
Authentication models - Django User + Profile pattern with RBAC
Uses Django's built-in User model with separate UserProfile
Includes comprehensive role-based access control
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from hr_core.apps.core.models import BaseModel


class RoleLevel(models.TextChoices):
    """Hierarchical role levels for RBAC"""
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    ORG_ADMIN = 'ORG_ADMIN', 'Organization Admin'
    DEPT_ADMIN = 'DEPT_ADMIN', 'Department Admin'
    MANAGER = 'MANAGER', 'Manager'
    EMPLOYEE = 'EMPLOYEE', 'Employee'


class Permission(BaseModel):
    """
    Granular permissions for RBAC
    Can be assigned to roles for fine-grained access control
    """
    code = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Unique permission code (e.g., 'employee.create')"
    )
    name = models.CharField(max_length=200, help_text="Human-readable permission name")
    description = models.TextField(blank=True, help_text="Permission description")
    resource = models.CharField(
        max_length=100,
        help_text="Resource this permission applies to (e.g., 'employee', 'department')"
    )
    action = models.CharField(
        max_length=50,
        help_text="Action this permission allows (e.g., 'create', 'read', 'update', 'delete')"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'permissions'
        ordering = ['resource', 'action']
        indexes = [
            models.Index(fields=['resource', 'action']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


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
    
    # Permissions
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='roles',
        help_text="Permissions assigned to this role"
    )
    
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

    def has_permission(self, permission_code):
        """Check if this role has a specific permission"""
        return self.permissions.filter(code=permission_code, is_active=True).exists()


class UserProfile(BaseModel):
    """
    Extended user profile linked to Django's built-in User
    Contains organization, role, and HR-specific fields
    This pattern avoids custom User model circular dependency issues
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile',
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
    
    # Session and security
    last_password_change = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)

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

    def has_permission(self, permission_code):
        """Check if user has a specific permission through their role"""
        if self.is_super_admin:
            return True
        return self.role and self.role.has_permission(permission_code)

    def get_all_permissions(self):
        """Get all permissions for this user"""
        if self.is_super_admin:
            return Permission.objects.filter(is_active=True)
        if self.role:
            return self.role.permissions.filter(is_active=True)
        return Permission.objects.none()

    def to_dict(self):
        """Convert user profile to dictionary for API responses"""
        return {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_super_admin': self.is_super_admin,
            'is_org_admin': self.is_org_admin,
            'is_dept_admin': self.is_dept_admin,
            'organization_id': self.organization_id,
            'role': {
                'id': self.role.id,
                'name': self.role.name,
                'level': self.role.level
            } if self.role else None,
            'permissions': [p.code for p in self.get_all_permissions()]
        }


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
