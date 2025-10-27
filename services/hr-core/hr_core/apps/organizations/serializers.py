from rest_framework import serializers
from .models import Organization


class OrganizationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for organization lists"""
    employee_count = serializers.ReadOnlyField()
    department_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'legal_name',
            'email',
            'phone',
            'city',
            'state',
            'country',
            'is_active',
            'employee_count',
            'department_count',
        ]


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for organization detail view"""
    employee_count = serializers.ReadOnlyField()
    department_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'legal_name',
            'email',
            'phone',
            'website',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'tax_id',
            'registration_number',
            'fiscal_year_start',
            'currency',
            'timezone',
            'is_active',
            'employee_count',
            'department_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'employee_count', 'department_count']


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating organizations"""
    
    class Meta:
        model = Organization
        fields = [
            'name',
            'legal_name',
            'email',
            'phone',
            'website',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'tax_id',
            'registration_number',
            'fiscal_year_start',
            'currency',
            'timezone',
            'is_active',
        ]
    
    def validate_tax_id(self, value):
        """Ensure tax_id is unique"""
        instance = self.instance
        if Organization.objects.filter(tax_id=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("An organization with this tax ID already exists.")
        return value
    
    def validate_email(self, value):
        """Ensure email is unique"""
        instance = self.instance
        if Organization.objects.filter(email=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("An organization with this email already exists.")
        return value
