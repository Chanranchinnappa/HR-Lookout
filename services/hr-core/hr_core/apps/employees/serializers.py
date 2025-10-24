"""
Employee serializers for REST API
"""

from rest_framework import serializers
from .models import Employee, Document


class EmployeeListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for employee lists
    """
    full_name = serializers.ReadOnlyField()
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name', 'first_name', 'last_name',
            'email', 'phone', 'job_title', 'employment_status',
            'employment_type', 'organization_name', 'department_name',
            'manager_name', 'profile_picture', 'hire_date'
        ]
    
    def get_manager_name(self, obj):
        return obj.manager.full_name if obj.manager else None


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual employee
    """
    full_name = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    manager_name = serializers.SerializerMethodField()
    direct_reports = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    def get_manager_name(self, obj):
        return obj.manager.full_name if obj.manager else None
    
    def get_direct_reports(self, obj):
        """Get list of direct reports"""
        reports = obj.direct_reports.filter(employment_status='ACTIVE')
        return EmployeeListSerializer(reports, many=True).data


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating employees
    """
    
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'middle_name',
            'preferred_name', 'email', 'personal_email', 'phone', 'mobile',
            'organization', 'department', 'job_title', 'employment_status',
            'employment_type', 'date_of_birth', 'hire_date', 'manager',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'bio'
        ]
    
    def validate_email(self, value):
        """Ensure email is unique"""
        instance = self.instance
        if Employee.objects.filter(email=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate_employee_id(self, value):
        """Ensure employee_id is unique"""
        instance = self.instance
        if Employee.objects.filter(employee_id=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("This employee ID is already in use.")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        if data.get('termination_date') and not data.get('employment_status') == 'TERMINATED':
            raise serializers.ValidationError(
                "Termination date can only be set when employment status is 'TERMINATED'."
            )
        
        if data.get('employment_status') == 'TERMINATED' and not data.get('termination_date'):
            raise serializers.ValidationError(
                "Termination date is required when employment status is 'TERMINATED'."
            )
        
        return data


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for employee documents
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['uploaded_at', 'uploaded_by']
