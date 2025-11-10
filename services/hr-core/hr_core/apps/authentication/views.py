"""
Authentication views for Django Token Auth
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for Docker/Kubernetes
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'hr-core',
        'version': '1.0.0'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint - returns auth token
    
    POST /api/v1/auth/login/
    Body: {"username": "user", "password": "pass"}
    Returns: {"token": "xxx", "user": {...}}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user
    user = authenticate(request, username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Create or get token
    token, created = Token.objects.get_or_create(user=user)
    
    # Return token + user info
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_super_admin': user.is_super_admin,
            'organization': {
                'id': user.organization.id,
                'name': user.organization.name,
                'org_unique_id': user.organization.org_unique_id
            } if user.organization else None,
            'role': {
                'id': user.role.id,
                'name': user.role.name,
                'level': user.role.level
            } if user.role else None
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint - deletes auth token
    
    POST /api/v1/auth/logout/
    Headers: Authorization: Token xxx
    """
    # Delete user's token
    request.user.auth_token.delete()
    
    return Response({
        'message': 'Successfully logged out'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Get current user profile
    
    GET /api/v1/auth/profile/
    Headers: Authorization: Token xxx
    """
    user = request.user
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_super_admin': user.is_super_admin,
        'organization': {
            'id': user.organization.id,
            'name': user.organization.name,
            'org_unique_id': user.organization.org_unique_id
        } if user.organization else None,
        'role': {
            'id': user.role.id,
            'name': user.role.name,
            'level': user.role.level,
            'permissions': list(user.role.permissions.values_list('codename', flat=True))
        } if user.role else None,
        'employee': {
            'id': user.employee.id,
            'employee_id': user.employee.employee_id,
            'full_name': user.employee.get_full_name(),
            'department': user.employee.department.name if user.employee.department else None
        } if user.employee else None
    })
