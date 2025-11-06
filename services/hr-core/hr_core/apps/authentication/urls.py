"""
Authentication app URL configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('ready/', views.readiness_check, name='readiness-check'),
    path('live/', views.liveness_check, name='liveness-check'),
    path('me/', views.user_info, name='user-info'),
]
