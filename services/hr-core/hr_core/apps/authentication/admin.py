"""
Django admin for authentication models
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Role, UserProfile


# Inline for UserProfile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('organization', 'role', 'employee', 'is_super_admin', 'phone', 'avatar', 'is_2fa_enabled')


# Extend default User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_organization')
    list_select_related = ('profile',)
    
    def get_organization(self, obj):
        try:
            return obj.profile.organization.name if obj.profile.organization else 'No Organization'
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_organization.short_description = 'Organization'


# Unregister default User admin and register extended version
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'organization', 'is_active', 'created_at']
    list_filter = ['level', 'is_active', 'organization']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Role Information', {
            'fields': ('name', 'level', 'description', 'is_active')
        }),
        ('Organization', {
            'fields': ('organization',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'is_super_admin', 'phone', 'created_at']
    list_filter = ['is_super_admin', 'role', 'organization', 'is_2fa_enabled']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user', 'employee']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Organization & Role', {
            'fields': ('organization', 'role', 'employee')
        }),
        ('Permissions', {
            'fields': ('is_super_admin', 'is_2fa_enabled')
        }),
        ('Contact', {
            'fields': ('phone', 'avatar')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
