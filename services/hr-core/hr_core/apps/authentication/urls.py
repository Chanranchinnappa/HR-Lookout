"""
Authentication URL patterns
"""

from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile management
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    
    # Password management
    path('password/change/', views.change_password_view, name='change_password'),
    
    # Permissions
    path('permissions/check/<str:permission_code>/', views.check_permission_view, name='check_permission'),
]
