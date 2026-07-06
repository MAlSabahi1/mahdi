"""
نموذج مرفق الطلب - Request Attachment Model
لتخزين الملفات المرفقة بطلب الخدمة
"""
import os
import mimetypes
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel

from utils.core.sync_abstract_model import SyncAbastractModel


class RequestAttachment(SyncAbastractModel, SoftDeleteModel):
    """
    مرفق الطلب - Request Attachment
    لتخزين الملفات المرفقة بطلب الخدمة
    """
    fk_request = models.ForeignKey(
        'ServiceRequest',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('الطلب')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('اسم المرفق')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف المرفق')
    )
    file = models.FileField(
        upload_to='requests/attachments/',
        verbose_name=_('الملف')
    )
    
    # حقول مشتقة - يتم حسابها تلقائياً عند الحفظ
    attachment_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('نوع المرفق')
    )
    attachment_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('حجم المرفق')
    )
    attachment_extension = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name=_('امتداد المرفق')
    )
    
    # بيانات الرفع
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الرفع')
    )
    fk_uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='uploaded_attachments',
        verbose_name=_('رفع بواسطة'),
        null=True,
        blank=True
    )
    
    # بيانات التعديل
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التعديل')
    )
    fk_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='updated_attachments',
        verbose_name=_('تعديل بواسطة'),
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        """
        حفظ المرفق مع حساب الحقول المشتقة تلقائياً
        attachment_type: نوع MIME للملف
        attachment_size: حجم الملف بالبايت
        attachment_extension: امتداد الملف
        """
        if self.file:
            # حساب حجم الملف
            try:
                self.attachment_size = self.file.size
            except (AttributeError, OSError):
                self.attachment_size = 0
            
            # حساب امتداد الملف
            file_name = self.file.name if hasattr(self.file, 'name') else ''
            if file_name:
                _, ext = os.path.splitext(file_name)
                self.attachment_extension = ext.lower().lstrip('.') if ext else ''
            else:
                self.attachment_extension = ''
            
            # حساب نوع MIME للملف
            if file_name:
                mime_type, _ = mimetypes.guess_type(file_name)
                self.attachment_type = mime_type or 'application/octet-stream'
            else:
                self.attachment_type = 'application/octet-stream'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.fk_request.request_number} - {self.name}'
    
    @property
    def size_display(self):
        """عرض حجم الملف بشكل مقروء"""
        if not self.attachment_size:
            return '0 B'
        
        size = self.attachment_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} TB'

    class Meta:
        verbose_name = _('مرفق الطلب')
        verbose_name_plural = _('مرفقات الطلبات')
        ordering = ['fk_request', '-uploaded_at']

