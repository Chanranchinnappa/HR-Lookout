"""
Main URL Configuration for HR-Lookout
Complete with Authentication + Organizations + Employees + Departments
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# API Router for ViewSets
router = routers.DefaultRouter()

# Import Authentication views (function-based)
from hr_core.apps.authentication.views import (
    health_check,
    login_view,
    logout_view,
    profile_view
)

# Import ViewSets
from hr_core.apps.organizations.views import OrganizationViewSet
from hr_core.apps.employees.views import EmployeeViewSet, DepartmentViewSet

# Register ViewSets with router
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', health_check, name='health'),
    path('api/v1/health/', health_check, name='api-health'),
    
    # Authentication endpoints (function-based views)
    path('api/v1/auth/login/', login_view, name='api-login'),
    path('api/v1/auth/logout/', logout_view, name='api-logout'),
    path('api/v1/auth/me/', profile_view, name='current-user'),
    path('api/v1/auth/profile/', profile_view, name='user-profile'),
    
    # API v1 endpoints (ViewSets via router)
    path('api/v1/', include(router.urls)),
    
    # DRF browsable API auth
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
