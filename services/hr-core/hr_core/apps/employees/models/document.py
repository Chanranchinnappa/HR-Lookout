from django.db import models
from hr_core.apps.core.models import TenantAwareModel


class DocumentType(models.TextChoices):
    CONTRACT = 'CONTRACT', 'Employment Contract'
    ID_PROOF = 'ID_PROOF', 'ID Proof'
    EDUCATION = 'EDUCATION', 'Educational Certificate'
    EXPERIENCE = 'EXPERIENCE', 'Experience Letter'
    RESIGNATION = 'RESIGNATION', 'Resignation Letter'
    OTHER = 'OTHER', 'Other'


class Document(TenantAwareModel):
    """
    Document model - stores employee-related documents
    """
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='documents',
        help_text="Employee this document belongs to"
    )
    
    title = models.CharField(max_length=200, help_text="Document title")
    
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        help_text="Type of document"
    )
    
    file = models.FileField(
        upload_to='employee_documents/%Y/%m/',
        help_text="Document file"
    )
    
    description = models.TextField(blank=True, help_text="Document description")
    
    uploaded_by = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents',
        help_text="Who uploaded this document"
    )
    
    is_verified = models.BooleanField(default=False, help_text="Is document verified")
    verified_by = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents',
        help_text="Who verified this document"
    )
    verified_at = models.DateTimeField(null=True, blank=True, help_text="When was it verified")
    
    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text="Document expiry date (if applicable)"
    )
    
    class Meta:
        db_table = 'employee_documents'
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
    def __str__(self):
        return f"{self.title} - {self.employee.full_name}"
