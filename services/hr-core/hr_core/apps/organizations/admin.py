"""
Django admin for Organization app
"""

from django.contrib import admin
from .models import Organization, Department


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for Organization"""
    
    list_display = ['name', 'legal_name', 'city', 'country', 'is_active']
    list_filter = ['is_active', 'country']
    search_fields = ['name', 'legal_name', 'tax_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'legal_name', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Legal & Tax', {
            'fields': ('tax_id', 'registration_number')
        }),
        ('Settings', {
            'fields': ('fiscal_year_start', 'currency', 'timezone', 'logo_url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department"""
    
    list_display = ['name', 'code', 'organization', 'head', 'is_active']
    list_filter = ['is_active', 'organization']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('organization', 'name', 'code', 'description', 'is_active')
        }),
        ('Hierarchy', {
            'fields': ('parent_department', 'head')
        }),
        ('Financial', {
            'fields': ('cost_center',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
