"""
URL configuration for hr-core microservice.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from hr_core.apps.employees.urls import department_urlpatterns

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', include('hr_core.apps.authentication.urls')),
    
    # REST API endpoints
    path('api/v1/employees/', include('hr_core.apps.employees.urls')),
    path('api/v1/organizations/', include('hr_core.apps.organizations.urls')),
    path('api/v1/departments/', include(department_urlpatterns)),  # ✅ ADD THIS LINE
    
    # GraphQL endpoint
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
