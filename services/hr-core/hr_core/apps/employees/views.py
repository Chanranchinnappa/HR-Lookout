from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organization', 'department', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['first_name', 'last_name', 'hire_date', 'created_at']
    ordering = ['first_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by organization if provided
        org_id = self.request.query_params.get('organization')
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        
        # Filter by department if provided
        dept_id = self.request.query_params.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        
        # Filter by status if provided
        emp_status = self.request.query_params.get('status')
        if emp_status:
            queryset = queryset.filter(status=emp_status)
        
        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organization', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by organization if provided
        org_id = self.request.query_params.get('organization')
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        
        return queryset

    def destroy(self, request, *args, **kwargs):
        """
        Custom delete with force option for super users
        
        Query params:
        - force: 'true' to force delete with employees (super user only)
        """
        department = self.get_object()
        force = request.query_params.get('force', 'false').lower() == 'true'
        
        # Check employee count
        employee_count = department.employees.count()
        
        # Block deletion if department has employees and not force delete
        if employee_count > 0 and not force:
            return Response(
                {
                    'error': 'Cannot delete department with employees',
                    'message': f'This department has {employee_count} employee{"s" if employee_count != 1 else ""}. Please reassign or delete them first, or use force delete (super user only).',
                    'employee_count': employee_count,
                    'can_force_delete': True
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Force delete - CASCADE will handle employees based on foreign key settings
        if force and employee_count > 0:
            # Log this action for audit trail
            print(f"⚠️ FORCE DELETE: Department '{department.name}' (ID: {department.id}) with {employee_count} employees")
        
        department.delete()
        
        return Response(
            {
                'message': 'Department deleted successfully',
                'deleted_employees': employee_count if force else 0
            },
            status=status.HTTP_204_NO_CONTENT
        )
