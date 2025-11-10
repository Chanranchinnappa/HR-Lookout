"""
Serializers for Employee, Department, and Document models
"""
from rest_framework import serializers
from .models import Employee, Department, Document
from hr_core.apps.organizations.models import Organization


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    head_name = serializers.SerializerMethodField()
    employee_count = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = [
            'id',
            'organization',
            'organization_name',
            'name',
            'code',
            'description',
            'head',
            'head_name',
            'parent_department',
            'cost_center',
            'is_active',
            'employee_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'employee_count', 'code']

    def get_head_name(self, obj):
        """Get department head's full name"""
        if obj.head:
            return obj.head.get_full_name()
        return None


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee lists"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'job_title',
            'department',
            'department_name',
            'organization',
            'organization_name',
            'status',  # ✅ Changed from employment_status
            'hire_date',
        ]

    def get_full_name(self, obj):
        """Get employee's full name"""
        return obj.get_full_name()


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for employee detail view"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    manager_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'full_name',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'hire_date',
            'termination_date',
            'job_title',
            'department',
            'department_name',
            'organization',
            'organization_name',
            'manager',
            'manager_name',
            'status',  # ✅ Changed from employment_status
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'full_name', 'employee_id']

    def get_full_name(self, obj):
        """Get employee's full name"""
        return obj.get_full_name()

    def get_manager_name(self, obj):
        """Get manager's full name"""
        if obj.manager:
            return obj.manager.get_full_name()
        return None


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    employee_name = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id',
            'employee',
            'employee_name',
            'organization',
            'title',
            'document_type',
            'file_key',  # ✅ Changed from 'file'
            'file_name',  # ✅ Added
            'file_size',  # ✅ Added
            'mime_type',  # ✅ Added
            'uploaded_by',
            'uploaded_by_name',
            'is_archived',
            'uploaded_at',  # ✅ Changed from created_at
        ]
        read_only_fields = ['uploaded_at', 'file_size', 'mime_type', 'uploaded_by']

    def get_employee_name(self, obj):
        """Get employee's full name"""
        if obj.employee:
            return obj.employee.get_full_name()
        return None

    def get_uploaded_by_name(self, obj):
        """Get uploader's name"""
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name()
        return None
