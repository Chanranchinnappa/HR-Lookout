from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'legal_name', 'email', 'city', 'country', 'is_active', 'employee_count', 'department_count']
    list_filter = ['is_active', 'country', 'currency']
    search_fields = ['name', 'legal_name', 'email', 'tax_id']
    readonly_fields = ['created_at', 'updated_at', 'employee_count', 'department_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'legal_name', 'email', 'phone', 'website')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Registration', {
            'fields': ('tax_id', 'registration_number')
        }),
        ('Operational', {
            'fields': ('fiscal_year_start', 'currency', 'timezone', 'is_active')
        }),
        ('Statistics', {
            'fields': ('employee_count', 'department_count'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
