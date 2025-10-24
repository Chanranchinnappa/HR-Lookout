"""
Employee REST API views
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Employee, Document
from .serializers import (
    EmployeeListSerializer,
    EmployeeDetailSerializer,
    EmployeeCreateUpdateSerializer,
    DocumentSerializer,
)
from hr_core.apps.audit.logger import get_audit_logger


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations
    
    Endpoints:
    - GET /api/v1/employees/ - List all employees
    - POST /api/v1/employees/ - Create new employee
    - GET /api/v1/employees/{id}/ - Get employee details
    - PUT/PATCH /api/v1/employees/{id}/ - Update employee
    - DELETE /api/v1/employees/{id}/ - Delete employee
    - GET /api/v1/employees/me/ - Get current user's employee record
    - GET /api/v1/employees/search/ - Search employees
    """
    
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employment_status', 'employment_type', 'organization', 'department']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id', 'job_title']
    ordering_fields = ['last_name', 'first_name', 'hire_date', 'employee_id']
    ordering = ['last_name', 'first_name']
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        queryset = Employee.objects.select_related(
            'organization', 'department', 'manager'
        ).prefetch_related('direct_reports')
        
        # Apply role-based filtering
        user = self.request.user
        
        # Admins see all employees
        if hasattr(user, 'is_admin') and user.is_admin:
            return queryset
        
        # Managers see their organization's employees
        if hasattr(user, 'is_manager') and user.is_manager:
            # TODO: Filter by user's organization
            return queryset
        
        # Regular employees see only active employees
        return queryset.filter(employment_status='ACTIVE')
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return EmployeeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EmployeeCreateUpdateSerializer
        return EmployeeDetailSerializer
    
    def perform_create(self, serializer):
        """
        Create employee with audit logging
        """
        employee = serializer.save(created_by=self.request.user.id)
        
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='CREATE',
            user_id=self.request.user.id,
            resource_type='Employee',
            resource_id=str(employee.id),
            metadata={'employee_id': employee.employee_id},
            request=self.request
        )
    
    def perform_update(self, serializer):
        """
        Update employee with audit logging
        """
        old_data = serializer.instance.__dict__.copy()
        employee = serializer.save(updated_by=self.request.user.id)
        new_data = employee.__dict__
        
        # Calculate changes
        changes = {
            'before': {k: old_data[k] for k in old_data if old_data[k] != new_data.get(k)},
            'after': {k: new_data[k] for k in old_data if old_data[k] != new_data.get(k)}
        }
        
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='UPDATE',
            user_id=self.request.user.id,
            resource_type='Employee',
            resource_id=str(employee.id),
            changes=changes,
            request=self.request
        )
    
    def perform_destroy(self, instance):
        """
        Soft delete employee (mark as terminated)
        """
        instance.employment_status = 'TERMINATED'
        instance.save()
        
        # Log to audit
        audit_logger = get_audit_logger()
        audit_logger.log(
            action='DELETE',
            user_id=self.request.user.id,
            resource_type='Employee',
            resource_id=str(instance.id),
            request=self.request
        )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's employee record
        """
        try:
            employee = Employee.objects.get(keycloak_user_id=request.user.id)
            serializer = EmployeeDetailSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee record not found for current user'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced employee search
        """
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({'error': 'Search query required'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(job_title__icontains=query)
        )
        
        serializer = EmployeeListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        Get all documents for an employee
        """
        employee = self.get_object()
        documents = employee.documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for employee documents
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'document_type']
    
    def perform_create(self, serializer):
        """
        Create document with user tracking
        """
        serializer.save(uploaded_by=self.request.user.id)
