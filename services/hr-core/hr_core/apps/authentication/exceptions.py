"""
Custom exception handler for authentication errors
"""

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses
    """
    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'message': _get_error_message(exc, response),
            'details': response.data if isinstance(response.data, dict) else {'detail': response.data},
        }
        response.data = custom_response_data
    
    return response


def _get_error_message(exc, response):
    """
    Extract a user-friendly error message
    """
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            return list(exc.detail.values())[0] if exc.detail else 'An error occurred'
        return str(exc.detail)
    
    return 'An error occurred'
