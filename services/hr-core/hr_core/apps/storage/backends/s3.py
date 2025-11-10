"""
AWS S3 Storage Backend
"""
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from typing import BinaryIO, Optional
from .base import BaseStorageBackend


class S3StorageBackend(BaseStorageBackend):
    """AWS S3 storage implementation"""
    
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME or 'us-east-1'
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
    
    def upload_file(
        self,
        file: BinaryIO,
        destination: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """Upload file to S3"""
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
        if metadata:
            extra_args['Metadata'] = metadata
        
        try:
            self.client.upload_fileobj(
                file,
                self.bucket,
                destination,
                ExtraArgs=extra_args
            )
            return destination
        except ClientError as e:
            raise Exception(f"S3 upload failed: {str(e)}")
    
    def download_file(self, file_key: str) -> bytes:
        """Download file from S3"""
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=file_key)
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"S3 download failed: {str(e)}")
    
    def delete_file(self, file_key: str) -> bool:
        """Delete file from S3"""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=file_key)
            return True
        except ClientError:
            return False
    
    def get_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for temporary access"""
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")
    
    def file_exists(self, file_key: str) -> bool:
        """Check if file exists in S3"""
        try:
            self.client.head_object(Bucket=self.bucket, Key=file_key)
            return True
        except ClientError:
            return False
    
    def get_file_metadata(self, file_key: str) -> dict:
        """Get file metadata from S3"""
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=file_key)
            return {
                'size': response['ContentLength'],
                'content_type': response.get('ContentType'),
                'last_modified': response['LastModified'],
                'metadata': response.get('Metadata', {})
            }
        except ClientError as e:
            raise Exception(f"Failed to get metadata: {str(e)}")
