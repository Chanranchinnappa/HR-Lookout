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
        read_only_fields = ['created_at', 'updated_at', 'employee_count']
    
    def get_head_name(self, obj):
        """Get department head's full name"""
        if obj.head:
            return obj.head.full_name
        return None
    
    def validate_code(self, value):
        """Ensure department code is uppercase"""
        return value.upper()


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee lists"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    full_name = serializers.ReadOnlyField()
    
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
            'employment_status',
            'hire_date',
        ]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for employee detail view"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    manager_name = serializers.SerializerMethodField()
    full_name = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
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
            'employment_status',
            'is_active',
            'salary',
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
        read_only_fields = ['created_at', 'updated_at', 'full_name', 'is_active']
        extra_kwargs = {
            'salary': {'write_only': True},  # Don't expose salary in API responses by default
        }
    
    def get_manager_name(self, obj):
        """Get manager's full name"""
        if obj.manager:
            return obj.manager.full_name
        return None


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()
    verified_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'employee',
            'employee_name',
            'organization',
            'title',
            'document_type',
            'file',
            'description',
            'uploaded_by',
            'uploaded_by_name',
            'is_verified',
            'verified_by',
            'verified_by_name',
            'verified_at',
            'expiry_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'uploaded_by', 'verified_at']
    
    def get_uploaded_by_name(self, obj):
        """Get uploader's name"""
        if obj.uploaded_by:
            return obj.uploaded_by.full_name
        return None
    
    def get_verified_by_name(self, obj):
        """Get verifier's name"""
        if obj.verified_by:
            return obj.verified_by.full_name
        return None
