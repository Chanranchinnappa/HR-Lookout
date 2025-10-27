#services/hr-core/hr_core/apps/employees/urls.py

"""
Employee app URL configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Main employee router
employee_router = DefaultRouter()
employee_router.register(r'', views.EmployeeViewSet, basename='employee')
employee_router.register(r'documents', views.DocumentViewSet, basename='document')

# Separate department router
department_router = DefaultRouter()
department_router.register(r'', views.DepartmentViewSet, basename='department')

# Default urlpatterns for /api/v1/employees/
urlpatterns = [
    path('', include(employee_router.urls)),
]

# Export department patterns separately for main urls.py
department_urlpatterns = [
    path('', include(department_router.urls)),
]
