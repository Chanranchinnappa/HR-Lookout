"""
Document model with cloud-agnostic storage backend
"""
from django.db import models
from django.conf import settings
from hr_core.apps.core.models import TenantAwareModel
from hr_core.apps.storage.services import StorageService


class DocumentType(models.TextChoices):
    CONTRACT = 'CONTRACT', 'Employment Contract'
    ID_PROOF = 'ID_PROOF', 'ID Proof'
    EDUCATION = 'EDUCATION', 'Educational Certificate'
    EXPERIENCE = 'EXPERIENCE', 'Experience Letter'
    RESIGNATION = 'RESIGNATION', 'Resignation Letter'
    PERFORMANCE_REVIEW = 'PERFORMANCE_REVIEW', 'Performance Review'
    OTHER = 'OTHER', 'Other'


class Document(TenantAwareModel):
    """
    Document model - stores employee-related documents
    Uses cloud-agnostic storage backend (S3/GCS/Azure/Local)
    """
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='documents',
        help_text="Employee this document belongs to"
    )
    
    title = models.CharField(max_length=200, help_text="Document title")
    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        help_text="Type of document"
    )
    
    # Storage key (path in cloud storage)
    file_key = models.CharField(
        max_length=500,
        help_text="Storage key/path for the file"
    )
    
    # File metadata
    file_name = models.CharField(max_length=255, help_text="Original filename")
    file_size = models.BigIntegerField(help_text="File size in bytes")
    mime_type = models.CharField(max_length=100, help_text="MIME type")
    description = models.TextField(blank=True, help_text="Document description")
    
    # Upload tracking - CHANGED: 'auth.User' instead of 'authentication.User'
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Uses Django's built-in User model
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        help_text="User who uploaded the document"
    )
    
    # Versioning
    version = models.IntegerField(default=1, help_text="Document version number")
    replaces = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_by',
        help_text="Previous version of this document"
    )
    
    # Status
    is_archived = models.BooleanField(default=False, help_text="Is document archived")
    
    class Meta:
        db_table = 'documents'
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        indexes = [
            models.Index(fields=['employee', 'document_type']),
            models.Index(fields=['organization', 'is_archived']),
            models.Index(fields=['file_key']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.employee.get_full_name()})"
    
    def get_download_url(self, expiration=3600):
        """
        Get temporary download URL for this document
        
        Args:
            expiration: URL expiration time in seconds (default 1 hour)
        
        Returns:
            str: Temporary download URL
        """
        return StorageService.get_url(self.file_key, expiration)
    
    def download(self):
        """Download document content as bytes"""
        return StorageService.download(self.file_key)
    
    def delete(self, *args, **kwargs):
        """Override delete to also remove file from storage"""
        # Delete from storage backend
        StorageService.delete(self.file_key)
        
        # Delete database record
        super().delete(*args, **kwargs)
    
    @classmethod
    def upload_new(cls, employee, file, title, document_type, uploaded_by, description=''):
        """
        Upload a new document
        
        Args:
            employee: Employee instance
            file: File object (UploadedFile from request.FILES)
            title: Document title
            document_type: DocumentType choice
            uploaded_by: User who uploaded
            description: Optional description
        
        Returns:
            Document: Created document instance
        """
        from datetime import datetime
        
        # Generate storage key
        timestamp = datetime.now().strftime('%Y/%m/%d/%H%M%S')
        file_key = f"documents/{employee.employee_id}/{timestamp}_{file.name}"
        
        # Upload to storage backend
        StorageService.upload(
            file=file,
            destination=file_key,
            content_type=file.content_type,
            metadata={
                'employee_id': employee.employee_id,
                'document_type': document_type,
                'uploaded_by': uploaded_by.username
            }
        )
        
        # Create database record
        document = cls.objects.create(
            organization=employee.organization,
            employee=employee,
            title=title,
            document_type=document_type,
            file_key=file_key,
            file_name=file.name,
            file_size=file.size,
            mime_type=file.content_type,
            description=description,
            uploaded_by=uploaded_by
        )
        
        return document
