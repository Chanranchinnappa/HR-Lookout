"""
Organization REST API views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Organization, Department
from .serializers import (
    OrganizationListSerializer,
    OrganizationDetailSerializer,
    OrganizationCreateUpdateSerializer,
    DepartmentListSerializer,
    DepartmentDetailSerializer,
    DepartmentCreateUpdateSerializer,
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
        organization = self.get_object()
        departments = organization.departments.filter(is_active=True)
        serializer = DepartmentListSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees for an organization"""
        from hr_core.apps.employees.serializers import EmployeeListSerializer
        
        organization = self.get_object()
        employees = organization.employees.filter(employment_status='ACTIVE')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Department CRUD operations
    
    Endpoints:
    - GET /api/v1/departments/ - List all departments
    - POST /api/v1/departments/ - Create new department
    - GET /api/v1/departments/{id}/ - Get department details
    - PUT/PATCH /api/v1/departments/{id}/ - Update department
    - DELETE /api/v1/departments/{id}/ - Delete department
    """
    
    queryset = Department.objects.select_related('organization', 'parent_department', 'head')
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['organization', 'is_active', 'parent_department']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return DepartmentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DepartmentCreateUpdateSerializer
        return DepartmentDetailSerializer
    
    def perform_create(self, serializer):
        """Create department with audit logging"""
        department = serializer.save()
        
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='CREATE',
            user_id=self.request.user.id,
            resource_type='Department',
            resource_id=str(department.id),
            metadata={'department_name': department.name},
            request=self.request
        )
    
    def perform_update(self, serializer):
        """Update department with audit logging"""
        department = serializer.save()
        
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='UPDATE',
            user_id=self.request.user.id,
            resource_type='Department',
            resource_id=str(department.id),
            request=self.request
        )
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a department"""
        from hr_core.apps.employees.serializers import EmployeeListSerializer
        
        department = self.get_object()
        employees = department.employees.filter(employment_status='ACTIVE')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def hierarchy(self, request, pk=None):
        """Get department hierarchy tree"""
        department = self.get_object()
        
        def build_tree(dept):
            return {
                'id': dept.id,
                'name': dept.name,
                'code': dept.code,
                'employee_count': dept.employees.filter(employment_status='ACTIVE').count(),
                'children': [build_tree(sub) for sub in dept.sub_departments.filter(is_active=True)]
            }
        
        tree = build_tree(department)
        return Response(tree)
