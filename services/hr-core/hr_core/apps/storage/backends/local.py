"""
Local Filesystem Storage Backend (for development)
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
from django.conf import settings
from typing import BinaryIO, Optional
from .base import BaseStorageBackend


class LocalStorageBackend(BaseStorageBackend):
    """Local filesystem storage (development only)"""
    
    def __init__(self):
        self.storage_root = Path(settings.LOCAL_STORAGE_ROOT)
        self.storage_root.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, file_key: str) -> Path:
        """Get absolute file path"""
        return self.storage_root / file_key
    
    def upload_file(
        self,
        file: BinaryIO,
        destination: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """Upload file to local filesystem"""
        try:
            file_path = self._get_file_path(destination)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file, f)
            
            # Store metadata in sidecar file
            if metadata or content_type:
                meta_path = file_path.with_suffix(file_path.suffix + '.meta')
                import json
                with open(meta_path, 'w') as f:
                    json.dump({
                        'content_type': content_type,
                        'metadata': metadata or {},
                        'uploaded_at': datetime.utcnow().isoformat()
                    }, f)
            
            return destination
        except Exception as e:
            raise Exception(f"Local upload failed: {str(e)}")
    
    def download_file(self, file_key: str) -> bytes:
        """Download file from local filesystem"""
        try:
            file_path = self._get_file_path(file_key)
            with open(file_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"File not found: {file_key}")
    
    def delete_file(self, file_key: str) -> bool:
        """Delete file from local filesystem"""
        try:
            file_path = self._get_file_path(file_key)
            file_path.unlink()
            
            # Delete metadata file if exists
            meta_path = file_path.with_suffix(file_path.suffix + '.meta')
            if meta_path.exists():
                meta_path.unlink()
            
            return True
        except FileNotFoundError:
            return False
    
    def get_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        """Generate URL for local file (returns file path)"""
        # In development, return a local URL or file path
        return f"/media/{file_key}"
    
    def file_exists(self, file_key: str) -> bool:
        """Check if file exists locally"""
        return self._get_file_path(file_key).exists()
    
    def get_file_metadata(self, file_key: str) -> dict:
        """Get file metadata from local filesystem"""
        try:
            file_path = self._get_file_path(file_key)
            stats = file_path.stat()
            
            # Read metadata from sidecar file
            meta_path = file_path.with_suffix(file_path.suffix + '.meta')
            metadata = {}
            content_type = None
            if meta_path.exists():
                import json
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                    content_type = meta.get('content_type')
                    metadata = meta.get('metadata', {})
            
            return {
                'size': stats.st_size,
                'content_type': content_type,
                'last_modified': datetime.fromtimestamp(stats.st_mtime),
                'metadata': metadata
            }
        except FileNotFoundError:
            raise Exception(f"File not found: {file_key}")
