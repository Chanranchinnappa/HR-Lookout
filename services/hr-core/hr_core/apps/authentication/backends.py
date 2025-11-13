"""
Django Authentication Backend with RBAC support
Replaces Keycloak with Django-native authentication
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class DjangoRBACBackend(BaseBackend):
    """
    Custom authentication backend for Django RBAC
    Supports username/email authentication and permission checking
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by username or email
        Returns User object if credentials are valid
        """
        if username is None or password is None:
            return None

        try:
            # Try to get user by username first
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Try to get user by email
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    logger.warning(f"Authentication failed: user not found - {username}")
                    return None

            # Check password
            if user.check_password(password):
                # Check if user is active
                if not user.is_active:
                    logger.warning(f"Authentication failed: user inactive - {username}")
                    return None

                logger.info(f"Authentication successful: {user.username}")
                return user
            else:
                logger.warning(f"Authentication failed: invalid password - {username}")
                return None

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None

    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user has a specific permission
        Integrates with RBAC system
        """
        if not user_obj.is_active:
            return False

        # Superusers have all permissions
        if user_obj.is_superuser:
            return True

        # Check through UserProfile RBAC
        try:
            profile = user_obj.userprofile
            
            # Super admins have all permissions
            if profile.is_super_admin:
                return True

            # Check permission through role
            return profile.has_permission(perm)

        except Exception as e:
            logger.error(f"Permission check error for user {user_obj.username}: {str(e)}")
            return False

    def has_module_perms(self, user_obj, app_label):
        """
        Check if user has permissions for a specific app/module
        """
        if not user_obj.is_active:
            return False

        # Superusers have all permissions
        if user_obj.is_superuser:
            return True

        # Super admins have all permissions
        try:
            profile = user_obj.userprofile
            if profile.is_super_admin:
                return True

            # Check if user has any permissions for this module
            permissions = profile.get_all_permissions()
            return permissions.filter(resource__startswith=app_label).exists()

        except Exception as e:
            logger.error(f"Module permission check error for user {user_obj.username}: {str(e)}")
            return False

    def get_user_permissions(self, user_obj, obj=None):
        """
        Get all permissions for a user
        """
        if not user_obj.is_active:
            return set()

        if user_obj.is_superuser:
            # Return all permission codes
            from .models import Permission
            return set(Permission.objects.filter(is_active=True).values_list('code', flat=True))

        try:
            profile = user_obj.userprofile
            
            if profile.is_super_admin:
                from .models import Permission
                return set(Permission.objects.filter(is_active=True).values_list('code', flat=True))

            # Return user's permissions through role
            return set(profile.get_all_permissions().values_list('code', flat=True))

        except Exception as e:
            logger.error(f"Get permissions error for user {user_obj.username}: {str(e)}")
            return set()

    def get_group_permissions(self, user_obj, obj=None):
        """
        Get permissions from groups (for compatibility with Django groups)
        """
        if not user_obj.is_active:
            return set()

        # Get permissions from Django groups
        return user_obj.user_permissions.all()

    def get_all_permissions(self, user_obj, obj=None):
        """
        Get all permissions (user + group) for a user
        """
        if not user_obj.is_active:
            return set()

        if user_obj.is_superuser:
            from .models import Permission
            return set(Permission.objects.filter(is_active=True).values_list('code', flat=True))

        # Combine user permissions and group permissions
        user_perms = self.get_user_permissions(user_obj, obj)
        group_perms = self.get_group_permissions(user_obj, obj)
        
        return user_perms.union(set(group_perms.values_list('codename', flat=True)))
