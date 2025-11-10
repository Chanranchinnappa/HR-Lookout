"""
Django Admin configuration for employees app
"""
from django.contrib import admin
from .models import Employee, Department, Document


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'email', 'department', 'job_title', 'status', 'hire_date']
    list_filter = ['status', 'organization', 'department', 'hire_date']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'employee_id', 'get_full_name', 'is_active']
    date_hierarchy = 'hire_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'first_name', 'middle_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Employment Details', {
            'fields': ('organization', 'department', 'job_title', 'manager', 'hire_date', 'termination_date', 'status', 'employment_type')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        """Display full name in admin"""
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'organization', 'head', 'is_active', 'employee_count', 'created_at']
    list_filter = ['is_active', 'organization', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at', 'employee_count', 'code']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'organization')
        }),
        ('Hierarchy', {
            'fields': ('head', 'parent_department')
        }),
        ('Financial', {
            'fields': ('cost_center',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('employee_count',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'document_type', 'file_size', 'created_at']
    list_filter = ['document_type', 'created_at', 'organization']
    search_fields = ['title', 'employee__first_name', 'employee__last_name', 'employee__employee_id', 'file_name']
    readonly_fields = ['created_at', 'updated_at', 'file_key', 'version']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'document_type', 'file_name', 'file_size', 'mime_type', 'description')
        }),
        ('Related Information', {
            'fields': ('employee', 'organization', 'uploaded_by')
        }),
        ('Storage', {
            'fields': ('file_key', 'version', 'replaces'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_archived',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
