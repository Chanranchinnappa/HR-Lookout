"""
Abstract base class for storage backends
All storage providers must implement this interface
"""
from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


class BaseStorageBackend(ABC):
    """
    Abstract storage backend interface
    Implement this for each cloud provider
    """
    
    @abstractmethod
    def upload_file(
        self,
        file: BinaryIO,
        destination: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Upload file to storage
        
        Args:
            file: File object to upload
            destination: Destination path (e.g., 'documents/2025/file.pdf')
            content_type: MIME type
            metadata: Additional metadata
        
        Returns:
            str: Public URL or file key
        """
        pass
    
    @abstractmethod
    def download_file(self, file_key: str) -> bytes:
        """Download file from storage"""
        pass
    
    @abstractmethod
    def delete_file(self, file_key: str) -> bool:
        """Delete file from storage"""
        pass
    
    @abstractmethod
    def get_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        """Generate temporary download URL"""
        pass
    
    @abstractmethod
    def file_exists(self, file_key: str) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    def get_file_metadata(self, file_key: str) -> dict:
        """Get file metadata (size, content type, etc.)"""
        pass
