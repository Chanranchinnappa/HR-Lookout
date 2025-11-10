"""
Cloud-agnostic storage backend
Supports AWS S3, Google Cloud Storage, Azure Blob, and local filesystem
"""
from .config import get_storage_backend

__all__ = ['get_storage_backend']
