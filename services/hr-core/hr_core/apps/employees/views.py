"""
ViewSets for Employee, Department, and Document models
"""
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
        """Filter departments by organization if query param provided"""
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('organization', None)
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        return queryset.select_related('organization', 'head', 'parent_department')


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations
    Supports filtering by organization, department, status, manager
    List view uses lightweight serializer, detail view uses full serializer
    """
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organization', 'department', 'status', 'manager', 'job_title']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['first_name', 'last_name', 'hire_date', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve, list serializer for list"""
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeListSerializer

    def get_queryset(self):
        """Optimize queries with select_related"""
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            queryset = queryset.select_related(
                'organization',
                'department',
                'manager'
            )
        else:
            queryset = queryset.select_related('organization', 'department')
        return queryset

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Get all documents for an employee"""
        employee = self.get_object()
        documents = Document.objects.filter(employee=employee)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Document CRUD operations
    Supports filtering by employee, organization, document_type
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'organization', 'document_type', 'is_archived']
    search_fields = ['title', 'file_name']
    ordering_fields = ['title', 'uploaded_at', 'file_size']
    ordering = ['-uploaded_at']

    def get_queryset(self):
        """Optimize queries with select_related"""
        return super().get_queryset().select_related(
            'employee',
            'organization',
            'uploaded_by'
        )

    def perform_create(self, serializer):
        """Set uploaded_by to current user"""
        serializer.save(uploaded_by=self.request.user)
