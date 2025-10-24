"""
Organization serializers
"""

from rest_framework import serializers
from .models import Organization, Department


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for organization lists
    """
    employee_count = serializers.SerializerMethodField()
    department_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'legal_name', 'email', 'phone', 'website',
            'city', 'state', 'country', 'is_active',
            'employee_count', 'department_count'
        ]
    
    def get_employee_count(self, obj):
        return obj.employees.filter(employment_status='ACTIVE').count()
    
    def get_department_count(self, obj):
        return obj.departments.filter(is_active=True).count()


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """
    Detailed organization serializer
    """
    employee_count = serializers.SerializerMethodField()
    department_count = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        return obj.employees.filter(employment_status='ACTIVE').count()
    
    def get_department_count(self, obj):
        return obj.departments.filter(is_active=True).count()
    
    def get_departments(self, obj):
        departments = obj.departments.filter(is_active=True, parent_department__isnull=True)
        return DepartmentListSerializer(departments, many=True).data


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating organizations
    """
    
    class Meta:
        model = Organization
        fields = [
            'name', 'legal_name', 'email', 'phone', 'website',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'tax_id', 'registration_number',
            'fiscal_year_start', 'currency', 'timezone', 'is_active'
        ]
    
    def validate_tax_id(self, value):
        """Ensure tax_id is unique"""
        instance = self.instance
        if Organization.objects.filter(tax_id=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("This tax ID is already in use.")
        return value


class DepartmentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for department lists
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    head_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'description', 'organization_name',
            'head_name', 'employee_count', 'is_active'
        ]
    
    def get_head_name(self, obj):
        return obj.head.full_name if obj.head else None
    
    def get_employee_count(self, obj):
        return obj.employees.filter(employment_status='ACTIVE').count()


class DepartmentDetailSerializer(serializers.ModelSerializer):
    """
    Detailed department serializer
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    parent_department_name = serializers.CharField(source='parent_department.name', read_only=True)
    head_name = serializers.SerializerMethodField()
    sub_departments = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_head_name(self, obj):
        return obj.head.full_name if obj.head else None
    
    def get_sub_departments(self, obj):
        sub_depts = obj.sub_departments.filter(is_active=True)
        return DepartmentListSerializer(sub_depts, many=True).data
    
    def get_employee_count(self, obj):
        return obj.employees.filter(employment_status='ACTIVE').count()


class DepartmentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating departments
    """
    
    class Meta:
        model = Department
        fields = [
            'organization', 'name', 'code', 'description',
            'parent_department', 'head', 'cost_center', 'is_active'
        ]
    
    def validate(self, data):
        """Prevent circular parent relationships"""
        if data.get('parent_department'):
            parent = data['parent_department']
            current = parent
            # Check for circular reference
            while current:
                if current == self.instance:
                    raise serializers.ValidationError(
                        "A department cannot be its own ancestor."
                    )
                current = current.parent_department
        return data
