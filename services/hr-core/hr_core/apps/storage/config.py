"""
Storage backend configuration factory
Dynamically loads the correct storage backend based on settings
"""
from django.conf import settings
from typing import Optional
from .backends.base import BaseStorageBackend


_storage_instance: Optional[BaseStorageBackend] = None


def get_storage_backend() -> BaseStorageBackend:
    """
    Get the configured storage backend instance (singleton)
    
    Configured via STORAGE_PROVIDER in settings:
    - 's3' → AWS S3
    - 'gcs' → Google Cloud Storage
    - 'azure' → Azure Blob Storage
    - 'local' → Local filesystem (dev only)
    
    Returns:
        BaseStorageBackend: Configured storage backend
    """
    global _storage_instance
    
    if _storage_instance is not None:
        return _storage_instance
    
    provider = getattr(settings, 'STORAGE_PROVIDER', 'local').lower()
    
    if provider == 's3':
        from .backends.s3 import S3StorageBackend
        _storage_instance = S3StorageBackend()
    
    elif provider == 'gcs':
        from .backends.gcs import GCSStorageBackend
        _storage_instance = GCSStorageBackend()
    
    elif provider == 'azure':
        from .backends.azure import AzureStorageBackend
        _storage_instance = AzureStorageBackend()
    
    elif provider == 'local':
        from .backends.local import LocalStorageBackend
        _storage_instance = LocalStorageBackend()
    
    else:
        raise ValueError(
            f"Invalid STORAGE_PROVIDER: {provider}. "
            f"Must be one of: s3, gcs, azure, local"
        )
    
    return _storage_instance


def reset_storage_backend():
    """Reset storage backend (useful for testing)"""
    global _storage_instance
    _storage_instance = None
