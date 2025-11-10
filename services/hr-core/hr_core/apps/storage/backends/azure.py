"""
Google Cloud Storage Backend
"""
from google.cloud import storage
from google.cloud.exceptions import NotFound
from django.conf import settings
from typing import BinaryIO, Optional
from .base import BaseStorageBackend


class GCSStorageBackend(BaseStorageBackend):
    """Google Cloud Storage implementation"""
    
    def __init__(self):
        # Expects GOOGLE_APPLICATION_CREDENTIALS env var or service account JSON
        self.client = storage.Client()
        self.bucket_name = settings.GCS_BUCKET_NAME
        self.bucket = self.client.bucket(self.bucket_name)
    
    def upload_file(
        self,
        file: BinaryIO,
        destination: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """Upload file to GCS"""
        try:
            blob = self.bucket.blob(destination)
            
            if content_type:
                blob.content_type = content_type
            if metadata:
                blob.metadata = metadata
            
            blob.upload_from_file(file, rewind=True)
            return destination
        except Exception as e:
            raise Exception(f"GCS upload failed: {str(e)}")
    
    def download_file(self, file_key: str) -> bytes:
        """Download file from GCS"""
        try:
            blob = self.bucket.blob(file_key)
            return blob.download_as_bytes()
        except NotFound:
            raise Exception(f"File not found: {file_key}")
    
    def delete_file(self, file_key: str) -> bool:
        """Delete file from GCS"""
        try:
            blob = self.bucket.blob(file_key)
            blob.delete()
            return True
        except NotFound:
            return False
    
    def get_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        """Generate signed URL for temporary access"""
        try:
            blob = self.bucket.blob(file_key)
            url = blob.generate_signed_url(
                expiration=expiration,
                method='GET'
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate signed URL: {str(e)}")
    
    def file_exists(self, file_key: str) -> bool:
        """Check if file exists in GCS"""
        blob = self.bucket.blob(file_key)
        return blob.exists()
    
    def get_file_metadata(self, file_key: str) -> dict:
        """Get file metadata from GCS"""
        try:
            blob = self.bucket.blob(file_key)
            blob.reload()
            return {
                'size': blob.size,
                'content_type': blob.content_type,
                'last_modified': blob.updated,
                'metadata': blob.metadata or {}
            }
        except NotFound:
            raise Exception(f"File not found: {file_key}")
