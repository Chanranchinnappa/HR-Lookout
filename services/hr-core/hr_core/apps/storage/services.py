"""
High-level storage service API
Convenience wrapper around storage backends
"""
from typing import BinaryIO, Optional
from .config import get_storage_backend


class StorageService:
    """
    High-level storage service
    Use this instead of directly accessing backends
    """
    
    @staticmethod
    def upload(
        file: BinaryIO,
        destination: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """Upload a file"""
        backend = get_storage_backend()
        return backend.upload_file(file, destination, content_type, metadata)
    
    @staticmethod
    def download(file_key: str) -> bytes:
        """Download a file"""
        backend = get_storage_backend()
        return backend.download_file(file_key)
    
    @staticmethod
    def delete(file_key: str) -> bool:
        """Delete a file"""
        backend = get_storage_backend()
        return backend.delete_file(file_key)
    
    @staticmethod
    def get_url(file_key: str, expiration: int = 3600) -> str:
        """Get temporary download URL"""
        backend = get_storage_backend()
        return backend.get_presigned_url(file_key, expiration)
    
    @staticmethod
    def exists(file_key: str) -> bool:
        """Check if file exists"""
        backend = get_storage_backend()
        return backend.file_exists(file_key)
    
    @staticmethod
    def get_metadata(file_key: str) -> dict:
        """Get file metadata"""
        backend = get_storage_backend()
        return backend.get_file_metadata(file_key)
