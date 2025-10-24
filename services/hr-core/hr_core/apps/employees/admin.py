"""
Django admin for Employee app
"""

from django.contrib import admin
from .models import Employee, Document


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin interface for Employee"""
    
    list_display = [
        'employee_id', 'full_name', 'email', 'job_title',
        'employment_status', 'organization', 'hire_date'
    ]
    list_filter = ['employment_status', 'employment_type', 'organization', 'department']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Identity', {
            'fields': ('employee_id', 'keycloak_user_id')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'middle_name', 'preferred_name', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('email', 'personal_email', 'phone', 'mobile')
        }),
        ('Employment Details', {
            'fields': (
                'organization', 'department', 'job_title', 'employment_status',
                'employment_type', 'hire_date', 'termination_date', 'manager'
            )
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Profile', {
            'fields': ('profile_picture', 'bio'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin interface for Document"""
    
    list_display = ['title', 'employee', 'document_type', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['title', 'employee__first_name', 'employee__last_name']
    readonly_fields = ['uploaded_at', 'uploaded_by']
