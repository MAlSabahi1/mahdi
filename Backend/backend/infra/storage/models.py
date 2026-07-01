import hashlib
import mimetypes
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel
from systems.personnel.models import PersonnelMaster

User = get_user_model()


class Document(TimeStampedModel):
    """المرفقات - مع دعم الرفع المؤقت وتصنيف النوع"""
    
    STATUS_CHOICES = [
        ('temp', _('مؤقت')),
        ('committed', _('مثبت')),
        ('archived', _('مؤرشف')),
    ]
    
    @staticmethod
    def _load_document_choices():
        """
        تحميل كسول (Lazy) — يُستدعى عند الطلب فقط، ليس عند تحميل الكلاس.
        يمنع فشل الـ migrations إذا كان documents.json غير موجود أو لم يتم تحميل الإعدادات بعد.
        """
        import json
        import os
        try:
            from django.conf import settings
            file_path = os.path.join(settings.BASE_DIR, 'core', 'dictionaries', 'documents.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [(k, _(v)) for k, v in data.items()]
        except Exception:
            # Fallback آمن: يعمل دائماً حتى بدون الملف
            return [('other', _('أخرى'))]

    def _get_document_type_choices():
        """
        Callable للـ choices — Django يستدعيها لحظة التحقق وليس عند تعريف الكلاس.
        متوافق مع CharField.choices في Django 3.2+
        """
        return Document._load_document_choices()

    DOCUMENT_TYPE_CHOICES = _get_document_type_choices
    
    # طريقة الرفع — يعرف الفرونت اند كيف أُدخل المرفق
    SOURCE_METHOD_CHOICES = [
        ('upload', _('رفع من الكمبيوتر')),
        ('scanner', _('ماسح ضوئي')),
        ('camera', _('كاميرا / هاتف')),
    ]
    
    # الفرد المرتبط بالمرفق (اختياري — بعض المرفقات عامة)
    # PROTECT: لا يمكن حذف فرد لديه مرفقات — يجب أرشفته أولاً
    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name=_('الفرد')
    )
    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES,
        default='other',
        verbose_name=_('نوع المرفق'),
        help_text=_('تصنيف المرفق — بطاقة وطنية، قرار ترقية، إلخ')
    )
    
    # ── ربط السياق: لأي حقل أو عملية هذا المرفق؟ ──
    related_field = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('الحقل المرتبط'),
        help_text=_(
            'اسم الحقل الذي يخص هذا المرفق — مثل: '
            'national_id, military_number, current_rank, current_status, full_name'
        )
    )
    context_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('نوع السياق'),
        help_text=_(
            'نوع الكيان المرتبط — مثل: '
            'SuggestedCorrection, RankSettlement, ServiceEventLog'
        )
    )
    context_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('معرف السياق'),
        help_text=_('المعرف الفريد للكيان المرتبط')
    )
    
    # طريقة الرفع
    source_method = models.CharField(
        max_length=10,
        choices=SOURCE_METHOD_CHOICES,
        default='upload',
        verbose_name=_('طريقة الرفع'),
    )
    
    file = models.FileField(upload_to='documents/%Y/%m/', verbose_name=_('الملف'))
    original_filename = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('اسم الملف الأصلي'))
    mime_type = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('نوع الملف (MIME)'))
    size = models.BigIntegerField(null=True, blank=True, verbose_name=_('حجم الملف'))
    file_hash = models.CharField(max_length=64, editable=False, verbose_name=_('Hash'))
    version = models.IntegerField(default=1, verbose_name=_('الإصدار'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name=_('رفع بواسطة')
    )
    # المرحلة 3: فصل رفع الملفات عن المعاملة الذرية
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='committed',
        verbose_name=_('حالة الملف')
    )
    temp_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='temp_documents',
        verbose_name=_('مالك الملف المؤقت')
    )
    temp_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تنتهي صلاحية المؤقت في')
    )
    
    class Meta:
        db_table = 'services_document'  # هام جداً: نحافظ على اسم الجدول لمنع حذف البيانات
        verbose_name = _('مرفق')
        verbose_name_plural = _('المرفقات')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['document_type']),
            models.Index(fields=['related_field']),
            models.Index(fields=['context_type', 'context_id']),
            models.Index(fields=['personnel', 'document_type']),
        ]
    
    def __str__(self):
        return f"Document {self.id} - v{self.version}"
    
    def save(self, *args, **kwargs):
        """حساب hash + فحص أمني + إعادة تسمية آمنة"""
        is_new = self._state.adding
        
        if self.file:
            # ── استخراج البيانات الوصفية تلقائياً قبل فحص وتغيير الاسم ──
            if not self.original_filename:
                # FileField contains the original filename upon upload
                self.original_filename = self.file.name
            if not self.size:
                try:
                    self.size = self.file.size
                except Exception:
                    pass
            if not self.mime_type:
                mime, _ = mimetypes.guess_type(self.file.name)
                self.mime_type = mime or 'application/octet-stream'

            # ── فحص أمني عند الرفع الأول فقط ──
            if is_new or 'file' in (kwargs.get('update_fields') or []):
                from core.file_validation import FileValidationService
                
                # اختيار نوع الفحص حسب تصنيف المرفق
                image_types = ('national_id_front', 'national_id_back', 'national_id_scan')
                if self.document_type in image_types:
                    FileValidationService.validate_image(self.file)
                else:
                    FileValidationService.validate_document(self.file)
                
                # إعادة تسمية الملف بـ UUID لمنع تنفيذ أكواد خبيثة
                safe_name = FileValidationService.generate_safe_filename(self.file)
                self.file.name = safe_name
            
            # ── حساب hash SHA-256 ──
            self.file.seek(0)
            file_hash = hashlib.sha256()
            for chunk in self.file.chunks():
                file_hash.update(chunk)
            self.file_hash = file_hash.hexdigest()
        
        super().save(*args, **kwargs)
    
    def verify_integrity(self):
        """التحقق من سلامة الملف"""
        if not self.file:
            return False
        self.file.seek(0)
        file_hash = hashlib.sha256()
        for chunk in self.file.chunks():
            file_hash.update(chunk)
        return file_hash.hexdigest() == self.file_hash
