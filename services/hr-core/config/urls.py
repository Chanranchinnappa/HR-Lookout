"""
Main URL Configuration for HR-Lookout
Compatible with existing views structure
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

# API Router
router = routers.DefaultRouter()

# Import existing viewsets
from hr_core.apps.organizations.views import OrganizationViewSet
from hr_core.apps.employees.views import (
    EmployeeViewSet,
    DepartmentViewSet,
    DocumentViewSet
)

# Register API routes
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'documents', DocumentViewSet, basename='document')

# Import auth views (function-based)
from hr_core.apps.authentication.views import (
    health_check,
    login_view,
    logout_view,
    profile_view
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API v1 - Main REST endpoints
    path('api/v1/', include(router.urls)),
    
    # Authentication endpoints (function-based views)
    path('api/v1/auth/login/', login_view, name='api-login'),
    path('api/v1/auth/logout/', logout_view, name='api-logout'),
    path('api/v1/auth/me/', profile_view, name='current-user'),
    path('api/v1/auth/profile/', profile_view, name='user-profile'),
    
    # DRF browsable API auth
    path('api-auth/', include('rest_framework.urls')),
    
    # Health check
    path('health/', health_check, name='health'),
    path('api/v1/health/', health_check, name='api-health'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
