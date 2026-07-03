"""
Core Base Models - النماذج الأساسية المشتركة
═══════════════════════════════════════════════
كل نموذج في النظام يرث من هنا.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """نموذج أساسي يحتوي على حقول التوقيت"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """
    QuerySet مخصص لمنع الحذف الفيزيائي (Hard Delete)
    """
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())
    
    def hard_delete(self):
        return super().delete()
        
    def alive(self):
        return self.filter(is_deleted=False)
        
    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """
    Manager مخصص يعرض فقط السجلات غير المحذوفة بشكل افتراضي
    """
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super().__init__(*args, **kwargs)
        
    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)
        return SoftDeleteQuerySet(self.model, using=self._db)
        
    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletableModel(TimeStampedModel):
    """
    نموذج أساسي مؤسسي — يمنع الحذف الفيزيائي للبيانات
    """
    is_deleted = models.BooleanField(default=False, verbose_name=_('محذوف'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('تاريخ الحذف'))

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """تجاوز الحذف الفيزيائي ليصبح حذف ناعم (Soft Delete)"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])
        return (1, {self._meta.label: 1})

    def hard_delete(self, *args, **kwargs):
        """الحذف الفيزيائي الحقيقي (للاستخدامات النادرة جداً)"""
        super().delete(*args, **kwargs)
        
    def restore(self):
        """استعادة السجل المحذوف"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])
