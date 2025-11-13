"""
Django Admin configuration for authentication models
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Role, Permission


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'
    fields = (
        'organization', 'role', 'employee', 'is_super_admin',
        'phone', 'avatar', 'is_2fa_enabled'
    )


class CustomUserAdmin(BaseUserAdmin):
    """Extended User admin with UserProfile inline"""
    inlines = (UserProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'get_organization', 'get_role'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active',
        'userprofile__is_super_admin', 'userprofile__organization'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    def get_organization(self, obj):
        """Get user's organization"""
        try:
            return obj.userprofile.organization.name if obj.userprofile.organization else '-'
        except:
            return '-'
    get_organization.short_description = 'Organization'

    def get_role(self, obj):
        """Get user's role"""
        try:
            return obj.userprofile.role.name if obj.userprofile.role else '-'
        except:
            return '-'
    get_role.short_description = 'Role'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin interface for Permission model"""
    list_display = (
        'code', 'name', 'resource', 'action',
        'is_active', 'created_at'
    )
    list_filter = ('resource', 'action', 'is_active', 'created_at')
    search_fields = ('code', 'name', 'resource', 'action', 'description')
    ordering = ('resource', 'action')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description')
        }),
        ('Permission Details', {
            'fields': ('resource', 'action', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin interface for Role model"""
    list_display = (
        'name', 'level', 'organization', 'is_active',
        'get_permission_count', 'created_at'
    )
    list_filter = ('level', 'is_active', 'organization', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('level', 'name')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('permissions',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'level', 'description')
        }),
        ('Organization', {
            'fields': ('organization',)
        }),
        ('Permissions', {
            'fields': ('permissions',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_permission_count(self, obj):
        """Get count of permissions for this role"""
        return obj.permissions.count()
    get_permission_count.short_description = 'Permissions'


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
