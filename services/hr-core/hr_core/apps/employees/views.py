from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Department, Document
from .serializers import (
    EmployeeListSerializer,
    EmployeeDetailSerializer,
    DepartmentSerializer,
    DocumentSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Department CRUD operations
    Supports filtering by organization, is_active
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organization', 'is_active', 'head']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Filter departments by organization if query param provided
        """
        queryset = super().get_queryset()
        
        # Filter by organization if provided
        org_id = self.request.query_params.get('organization', None)
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        
        return queryset.select_related('organization', 'head')
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """
        Get all employees in this department
        Endpoint: /api/v1/departments/{id}/employees/
        """
        department = self.get_object()
        employees = department.employees.filter(employment_status='ACTIVE')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def check_delete_permission(self, request, pk=None):
        """
        Check if department can be deleted
        Endpoint: /api/v1/departments/{id}/check_delete_permission/
        """
        department = self.get_object()
        # For now, return basic info - will enhance with user permissions later
        can_delete = department.employee_count == 0
        return Response({
            'can_delete': can_delete,
            'employee_count': department.employee_count,
            'message': f"{department.employee_count} employees assigned" if not can_delete else "No employees assigned"
        })


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations
    Uses different serializers for list and detail views
    """
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organization', 'department', 'employment_status', 'manager']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'job_title']
    ordering_fields = ['employee_id', 'first_name', 'last_name', 'hire_date']
    ordering = ['employee_id']
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve, list serializer for list"""
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeListSerializer
    
    def get_queryset(self):
        """
        Optimize queries with select_related
        Filter by organization if provided
        """
        queryset = super().get_queryset()
        
        # Optimize queries
        queryset = queryset.select_related('organization', 'department', 'manager')
        
        # Filter by organization if provided
        org_id = self.request.query_params.get('organization', None)
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        Get all documents for this employee
        Endpoint: /api/v1/employees/{id}/documents/
        """
        employee = self.get_object()
        documents = employee.documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def direct_reports(self, request, pk=None):
        """
        Get all employees reporting to this employee
        Endpoint: /api/v1/employees/{id}/direct_reports/
        """
        employee = self.get_object()
        reports = employee.direct_reports.filter(employment_status='ACTIVE')
        serializer = EmployeeListSerializer(reports, many=True)
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Document CRUD operations
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'organization', 'document_type', 'is_verified']
    search_fields = ['title', 'description', 'employee__first_name', 'employee__last_name']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Optimize queries"""
        queryset = super().get_queryset()
        return queryset.select_related('employee', 'organization', 'uploaded_by', 'verified_by')
    
    def perform_create(self, serializer):
        """Set uploaded_by to current user when creating"""
        # For now, save without user - will add when authentication is implemented
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a document
        Endpoint: /api/v1/documents/{id}/verify/
        """
        document = self.get_object()
        from django.utils import timezone
        
        document.is_verified = True
        document.verified_at = timezone.now()
        # Will set verified_by when authentication is implemented
        document.save()
        
        serializer = self.get_serializer(document)
        return Response(serializer.data)
