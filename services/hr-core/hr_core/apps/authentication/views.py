"""
Authentication views for Django Token Auth with RBAC
Handles user registration, login, logout, profile management
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone

from .models import UserProfile, Role

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for Docker/Kubernetes
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'hr-core',
        'version': '1.0.0',
        'timestamp': timezone.now().isoformat()
    })


def serialize_user_with_role(user, profile):
    """
    Helper function to serialize user with role and permissions
    """
    # Serialize role with permissions
    role_data = None
    permissions_list = []
    
    if profile.role:
        # Get all permissions from role
        permissions_data = []
        for perm in profile.role.permissions.all():
            permissions_data.append({
                'id': perm.id,
                'name': perm.name,
                'code': perm.code,  # FIXED: was code_name
                'resource': perm.resource,
                'action': perm.action,
            })
            permissions_list.append(perm.code)  # FIXED: was code_name
        
        role_data = {
            'id': profile.role.id,
            'name': profile.role.name,
            'level': profile.role.level,
            'description': profile.role.description or '',
            'permissions': permissions_data
        }
    
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_super_admin': profile.is_super_admin,
        'organization': {
            'id': profile.organization.id,
            'name': profile.organization.name,
            'org_unique_id': profile.organization.org_unique_id
        } if profile.organization else None,
        'role': role_data,
        'permissions': permissions_list
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint
    POST /api/v1/auth/register/
    Body: {
        "username": "user",
        "email": "user@example.com",
        "password": "securepass",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        # Validation
        if not username or not email or not password:
            return Response(
                {'error': 'Username, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {'error': list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Get or create profile (should be created by signal)
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Create token
        token = Token.objects.create(user=user)
        
        logger.info(f"New user registered: {username}")
        
        return Response({
            'message': 'User registered successfully',
            'token': token.key,
            'user': serialize_user_with_role(user, profile)
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return Response(
            {'error': 'Registration failed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint - returns auth token
    POST /api/v1/auth/login/
    Body: {"username": "user", "password": "pass"}
    Returns: {"token": "xxx", "user": {...}}
    """
    try:
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
        
        # Check if user is active
        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        logger.info(f"User logged in: {username}")
        
        # Return token + user info
        return Response({
            'token': token.key,
            'user': serialize_user_with_role(user, profile)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response(
            {'error': 'Login failed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint - deletes auth token
    POST /api/v1/auth/logout/
    Headers: Authorization: Token xxx
    """
    try:
        # Delete user's token
        request.user.auth_token.delete()
        logger.info(f"User logged out: {request.user.username}")
        
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response(
            {'error': 'Logout failed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Get current user profile with role and permissions
    GET /api/v1/auth/profile/ or /api/v1/auth/me/
    Headers: Authorization: Token xxx
    """
    try:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Serialize role with full permission details
        role_data = None
        permissions_list = []
        
        if profile.role:
            permissions_data = []
            for perm in profile.role.permissions.all():
                permissions_data.append({
                    'id': perm.id,
                    'name': perm.name,
                    'code': perm.code,  # FIXED: was code_name
                    'resource': perm.resource,
                    'action': perm.action,
                })
                permissions_list.append(perm.code)  # FIXED: was code_name
            
            role_data = {
                'id': profile.role.id,
                'name': profile.role.name,
                'level': profile.role.level,
                'description': profile.role.description or '',
                'permissions': permissions_data
            }
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_super_admin': profile.is_super_admin,
            'phone': profile.phone or '',
            'avatar': profile.avatar.url if profile.avatar else None,
            'is_2fa_enabled': profile.is_2fa_enabled,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
            'organization': {
                'id': profile.organization.id,
                'name': profile.organization.name,
                'org_unique_id': profile.organization.org_unique_id
            } if profile.organization else None,
            'organization_name': profile.organization.name if profile.organization else None,
            'role': role_data,
            'employee': {
                'id': profile.employee.id,
                'employee_id': profile.employee.employee_id,
                'full_name': profile.employee.get_full_name(),
                'department': profile.employee.department.name if profile.employee.department else None
            } if profile.employee else None,
            'permissions': permissions_list
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Profile retrieval error: {str(e)}")
        return Response(
            {'error': 'Failed to retrieve profile'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Update user profile
    PUT/PATCH /api/v1/auth/profile/
    Headers: Authorization: Token xxx
    Body: {"first_name": "John", "last_name": "Doe", "phone": "+1234567890"}
    """
    try:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update user fields
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            # Check if email is already taken
            email = request.data['email']
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response(
                    {'error': 'Email already in use'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.email = email
        
        user.save()
        
        # Update profile fields
        if 'phone' in request.data:
            profile.phone = request.data['phone']
        if 'avatar' in request.data:
            profile.avatar = request.data['avatar']
        
        profile.save()
        
        logger.info(f"Profile updated: {user.username}")
        
        return Response({
            'message': 'Profile updated successfully',
            'user': serialize_user_with_role(user, profile)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        return Response(
            {'error': 'Failed to update profile'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Change user password
    POST /api/v1/auth/password/change/
    Headers: Authorization: Token xxx
    Body: {"old_password": "old", "new_password": "new"}
    """
    try:
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'Old password and new password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify old password
        if not user.check_password(old_password):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {'error': list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Update profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.last_password_change = timezone.now()
        profile.save()
        
        # Delete old token and create new one
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        logger.info(f"Password changed: {user.username}")
        
        return Response({
            'message': 'Password changed successfully',
            'token': token.key
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        return Response(
            {'error': 'Failed to change password'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_permission_view(request, permission_code):
    """
    Check if user has a specific permission
    GET /api/v1/auth/permissions/check/{permission_code}/
    Headers: Authorization: Token xxx
    """
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Check if user has permission
        has_permission = False
        if profile.role:
            has_permission = profile.role.permissions.filter(code=permission_code).exists()  # FIXED: was code_name=
        
        # Super admins have all permissions
        if profile.is_super_admin:
            has_permission = True
        
        return Response({
            'permission': permission_code,
            'has_permission': has_permission
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Permission check error: {str(e)}")
        return Response(
            {'error': 'Failed to check permission'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
