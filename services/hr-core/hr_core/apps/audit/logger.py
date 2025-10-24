"""
Audit logging to MongoDB
"""

from pymongo import MongoClient
from django.conf import settings
from datetime import datetime


class AuditLogger:
    """
    Centralized audit logging to MongoDB
    """
    
    def __init__(self):
        mongo_settings = settings.MONGODB_SETTINGS
        self.client = MongoClient(
            host=mongo_settings['host'],
            port=mongo_settings['port'],
            username=mongo_settings['username'],
            password=mongo_settings['password'],
        )
        self.db = self.client[mongo_settings['database']]
        self.collection = self.db['audit_logs']
    
    def log(self, action, user_id, resource_type, resource_id=None, 
            changes=None, metadata=None, request=None):
        """
        Log an audit event to MongoDB
        
        Args:
            action: Action performed (CREATE, READ, UPDATE, DELETE, etc.)
            user_id: ID of the user performing the action
            resource_type: Type of resource (Employee, Organization, etc.)
            resource_id: ID of the resource being acted upon
            changes: Dictionary of changes (before/after values)
            metadata: Additional contextual information
            request: Django request object (for IP, user agent, etc.)
        """
        audit_entry = {
            'timestamp': datetime.utcnow(),
            'service': 'hr-core',
            'action': action,
            'user_id': user_id,
            'user_email': getattr(request.user, 'email', None) if request else None,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'changes': changes or {},
            'metadata': metadata or {},
        }
        
        if request:
            audit_entry.update({
                'ip_address': self._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            })
        
        try:
            self.collection.insert_one(audit_entry)
        except Exception as e:
            # Log to Django logger as fallback
            import logging
            logger = logging.getLogger('hr_core.audit')
            logger.error(f'Failed to write audit log: {str(e)}')
    
    def _get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()


# Singleton instance
_audit_logger = None


def get_audit_logger():
    """Get or create audit logger instance"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
