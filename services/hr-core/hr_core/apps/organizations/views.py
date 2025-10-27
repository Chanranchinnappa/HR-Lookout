"""
Organization REST API views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Organization
from .serializers import (
    OrganizationListSerializer,
    OrganizationDetailSerializer,
    OrganizationCreateUpdateSerializer,
)

from hr_core.apps.audit.logger import get_audit_logger


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Organization CRUD operations
    Endpoints:
    - GET /api/v1/organizations/ - List all organizations
    - POST /api/v1/organizations/ - Create new organization
    - GET /api/v1/organizations/{id}/ - Get organization details
    - PUT/PATCH /api/v1/organizations/{id}/ - Update organization
    - DELETE /api/v1/organizations/{id}/ - Delete organization
    """
    queryset = Organization.objects.all()
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'country']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return OrganizationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrganizationCreateUpdateSerializer
        return OrganizationDetailSerializer
    
    def perform_create(self, serializer):
        """Create organization with audit logging"""
        organization = serializer.save()
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='CREATE',
            user_id=self.request.user.id,
            resource_type='Organization',
            resource_id=str(organization.id),
            metadata={'organization_name': organization.name},
            request=self.request
        )
    
    def perform_update(self, serializer):
        """Update organization with audit logging"""
        organization = serializer.save()
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='UPDATE',
            user_id=self.request.user.id,
            resource_type='Organization',
            resource_id=str(organization.id),
            request=self.request
        )
    
    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        """Get all departments for an organization"""
        from hr_core.apps.employees.serializers import DepartmentSerializer
        organization = self.get_object()
        departments = organization.department_set.filter(is_active=True)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees for an organization"""
        from hr_core.apps.employees.serializers import EmployeeListSerializer
        organization = self.get_object()
        employees = organization.employee_set.filter(employment_status='ACTIVE')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)
