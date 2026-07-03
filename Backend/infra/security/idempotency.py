"""
Idempotency System - نظام منع تكرار العمليات

يمنع تنفيذ نفس العملية مرتين عند إعادة إرسال الطلب.
يُستخدم مع العمليات الكتابية (POST/PUT/DELETE).
"""
import json
import hashlib
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from datetime import timedelta

User = get_user_model()


class IdempotencyRecord(models.Model):
    """
    سجل Idempotency: يخزن نتيجة العملية الأولى
    لإعادتها عند تكرار الطلب بنفس المفتاح.
    """
    key = models.CharField(
        max_length=64,
        verbose_name=_('مفتاح Idempotency')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='idempotency_records',
        verbose_name=_('المستخدم')
    )
    status_code = models.IntegerField(
        verbose_name=_('كود الاستجابة')
    )
    response_data = models.JSONField(
        verbose_name=_('بيانات الاستجابة')
    )
    endpoint = models.CharField(
        max_length=255,
        verbose_name=_('نقطة النهاية')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    expires_at = models.DateTimeField(
        verbose_name=_('تنتهي في')
    )
    
    class Meta:
        db_table = 'security_idempotency_record'
        verbose_name = _('سجل Idempotency')
        verbose_name_plural = _('سجلات Idempotency')
        unique_together = ['key', 'user']
        indexes = [
            models.Index(fields=['key', 'user']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}:{self.key[:16]}..."
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @classmethod
    def cleanup_expired(cls):
        """حذف السجلات المنتهية"""
        return cls.objects.filter(expires_at__lt=timezone.now()).delete()


class IdempotencyMixin:
    """
    Mixin لـ ViewSets يدعم Idempotency Keys
    
    Usage:
        class MyViewSet(IdempotencyMixin, ModelViewSet):
            idempotent_actions = ['create', 'update', 'partial_update', 'destroy']
    """
    idempotent_actions = ['create']
    
    def get_idempotency_key(self, request):
        """استخراج مفتاح Idempotency من الهيدر أو البيانات"""
        key = request.META.get('HTTP_X_IDEMPOTENCY_KEY')
        if not key:
            key = request.data.get('idempotency_key')
        return key
    
    def initial(self, request, *args, **kwargs):
        """فحص Idempotency قبل تنفيذ الطلب"""
        super().initial(request, *args, **kwargs)
        
        action = getattr(self, 'action', None)
        if action not in self.idempotent_actions:
            return
        
        key = self.get_idempotency_key(request)
        if not key:
            return
        
        # البحث عن سجل سابق
        try:
            record = IdempotencyRecord.objects.get(
                key=key,
                user=request.user,
            )
            if not record.is_expired():
                # إعادة نفس الاستجابة
                self._idempotency_response = Response(
                    record.response_data,
                    status=record.status_code,
                    headers={'X-Idempotency-Replay': 'true'}
                )
            else:
                record.delete()
                self._idempotency_response = None
        except IdempotencyRecord.DoesNotExist:
            self._idempotency_response = None
    
    def finalize_response(self, request, response, *args, **kwargs):
        """حفظ الاستجابة للـ Idempotency"""
        response = super().finalize_response(request, response, *args, **kwargs)
        
        # فحص إذا كانت استجابة مكررة
        if hasattr(self, '_idempotency_response') and self._idempotency_response:
            return self._idempotency_response
        
        action = getattr(self, 'action', None)
        if action not in self.idempotent_actions:
            return response
        
        key = self.get_idempotency_key(request)
        if not key:
            return response
        
        # حفظ فقط الاستجابات الناجحة
        if 200 <= response.status_code < 300:
            try:
                if hasattr(response, 'data') and response.data is not None:
                    IdempotencyRecord.objects.create(
                        key=key,
                        user=request.user,
                        status_code=response.status_code,
                        response_data=response.data,
                        endpoint=request.path,
                    )
            except Exception:
                pass  # لا نريد فشل الـ Idempotency أن يؤثر على الاستجابة
        
        return response
