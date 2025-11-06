"""
URL configuration for hr-core microservice.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from hr_core.apps.authentication import views as auth_views
from hr_core.apps.employees.urls import department_urlpatterns

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Root health check endpoint (for Docker healthchecks and k8s probes)
    path('health/', auth_views.health_check, name='root-health-check'),
    
    # App-scoped authentication routes
    path('api/v1/auth/', include('hr_core.apps.authentication.urls')),

    # REST API endpoints
    path('api/v1/employees/', include('hr_core.apps.employees.urls')),
    path('api/v1/organizations/', include('hr_core.apps.organizations.urls')),
    path('api/v1/departments/', include(department_urlpatterns)),

    # GraphQL endpoint
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
