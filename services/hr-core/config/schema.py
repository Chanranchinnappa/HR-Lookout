"""
GraphQL Schema for HR-Core
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from hr_core.apps.employees.models import Employee, Document
from hr_core.apps.organizations.models import Organization, Department


# ============================================================================
# Types
# ============================================================================

class EmployeeType(DjangoObjectType):
    """GraphQL type for Employee"""
    full_name = graphene.String()
    is_active = graphene.Boolean()
    
    class Meta:
        model = Employee
        fields = '__all__'
    
    def resolve_full_name(self, info):
        return self.full_name
    
    def resolve_is_active(self, info):
        return self.is_active


class DocumentType(DjangoObjectType):
    """GraphQL type for Document"""
    
    class Meta:
        model = Document
        fields = '__all__'


class OrganizationType(DjangoObjectType):
    """GraphQL type for Organization"""
    employee_count = graphene.Int()
    department_count = graphene.Int()
    
    class Meta:
        model = Organization
        fields = '__all__'
    
    def resolve_employee_count(self, info):
        return self.employees.filter(employment_status='ACTIVE').count()
    
    def resolve_department_count(self, info):
        return self.departments.filter(is_active=True).count()


class DepartmentType(DjangoObjectType):
    """GraphQL type for Department"""
    employee_count = graphene.Int()
    
    class Meta:
        model = Department
        fields = '__all__'
    
    def resolve_employee_count(self, info):
        return self.employees.filter(employment_status='ACTIVE').count()


# ============================================================================
# Queries
# ============================================================================

class Query(graphene.ObjectType):
    """
    Root query type
    """
    
    # Employee queries
    employee = graphene.Field(EmployeeType, id=graphene.Int())
    all_employees = graphene.List(
        EmployeeType,
        employment_status=graphene.String(),
        organization=graphene.Int(),
        department=graphene.Int()
    )
    search_employees = graphene.List(EmployeeType, query=graphene.String(required=True))
    
    # Organization queries
    organization = graphene.Field(OrganizationType, id=graphene.Int())
    all_organizations = graphene.List(OrganizationType, is_active=graphene.Boolean())
    
    # Department queries
    department = graphene.Field(DepartmentType, id=graphene.Int())
    all_departments = graphene.List(
        DepartmentType,
        organization=graphene.Int(),
        is_active=graphene.Boolean()
    )
    department_hierarchy = graphene.Field(DepartmentType, id=graphene.Int())
    
    # Document queries
    employee_documents = graphene.List(DocumentType, employee_id=graphene.Int(required=True))
    
    # Org chart query
    org_chart = graphene.Field(EmployeeType, root_employee_id=graphene.Int())
    
    # Employee resolvers
    def resolve_employee(self, info, id):
        return Employee.objects.get(pk=id)
    
    def resolve_all_employees(self, info, employment_status=None, organization=None, department=None):
        queryset = Employee.objects.all()
        
        if employment_status:
            queryset = queryset.filter(employment_status=employment_status)
        if organization:
            queryset = queryset.filter(organization_id=organization)
        if department:
            queryset = queryset.filter(department_id=department)
        
        return queryset
    
    def resolve_search_employees(self, info, query):
        from django.db.models import Q
        return Employee.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_id__icontains=query)
        )
    
    # Organization resolvers
    def resolve_organization(self, info, id):
        return Organization.objects.get(pk=id)
    
    def resolve_all_organizations(self, info, is_active=None):
        queryset = Organization.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return queryset
    
    # Department resolvers
    def resolve_department(self, info, id):
        return Department.objects.get(pk=id)
    
    def resolve_all_departments(self, info, organization=None, is_active=None):
        queryset = Department.objects.all()
        
        if organization:
            queryset = queryset.filter(organization_id=organization)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    def resolve_department_hierarchy(self, info, id):
        return Department.objects.get(pk=id)
    
    # Document resolvers
    def resolve_employee_documents(self, info, employee_id):
        return Document.objects.filter(employee_id=employee_id)
    
    # Org chart resolver
    def resolve_org_chart(self, info, root_employee_id=None):
        if root_employee_id:
            return Employee.objects.get(pk=root_employee_id)
        # Return CEO or top-level employee
        return Employee.objects.filter(manager__isnull=True).first()


# ============================================================================
# Schema
# ============================================================================

schema = graphene.Schema(query=Query)
