from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel, SoftDeletableModel, SecurityAdministration
from systems.personnel.public import PersonnelMaster
from simple_history.models import HistoricalRecords

User = get_user_model()

class Correspondence(SoftDeletableModel):
    class Type(models.TextChoices):
        INCOMING = 'incoming', _('وارد')
        OUTGOING = 'outgoing', _('صادر')

    class Status(models.TextChoices):
        NEW = 'new', _('جديد')
        IN_PROGRESS = 'in_progress', _('قيد الإجراء')
        COMPLETED = 'completed', _('مكتمل')
        REQUIRES_REPLY = 'requires_reply', _('يتطلب رد')

    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_('النوع'))
    reference_number = models.CharField(max_length=100, unique=True, verbose_name=_('رقم المرجع'))
    subject = models.CharField(max_length=255, verbose_name=_('الموضوع'))
    date = models.DateField(verbose_name=_('تاريخ المراسلة'))
    
    sender = models.CharField(max_length=255, verbose_name=_('الجهة المرسلة'))
    receiver = models.CharField(max_length=255, verbose_name=_('الجهة المستقبلة'))
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, verbose_name=_('الحالة'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='correspondences', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_correspondences', verbose_name=_('مدخل البيانات'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('مراسلة')
        verbose_name_plural = _('المراسلات')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.reference_number} - {self.subject}"


class Task(SoftDeletableModel):
    class Priority(models.TextChoices):
        HIGH = 'high', _('عالية')
        MEDIUM = 'medium', _('متوسطة')
        LOW = 'low', _('منخفضة')

    class Status(models.TextChoices):
        PENDING = 'pending', _('قيد الانتظار')
        IN_PROGRESS = 'in_progress', _('جاري العمل')
        COMPLETED = 'completed', _('مكتملة')
        DELAYED = 'delayed', _('متأخرة')

    title = models.CharField(max_length=255, verbose_name=_('عنوان المهمة'))
    description = models.TextField(verbose_name=_('الوصف'))
    
    assigned_to = models.ForeignKey(PersonnelMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name=_('الموظف المكلف'))
    related_correspondence = models.ForeignKey(Correspondence, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', verbose_name=_('المراسلة المرتبطة'))
    
    due_date = models.DateField(verbose_name=_('تاريخ الاستحقاق'))
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM, verbose_name=_('الأولوية'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('الحالة'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='tasks', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks', verbose_name=_('منشئ المهمة'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('مهمة')
        verbose_name_plural = _('المهام')
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return self.title


class Circular(SoftDeletableModel):
    title = models.CharField(max_length=255, verbose_name=_('عنوان التعميم'))
    content = models.TextField(verbose_name=_('محتوى التعميم'))
    date_issued = models.DateField(verbose_name=_('تاريخ الإصدار'))
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='circulars', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_circulars', verbose_name=_('منشئ التعميم'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('تعميم')
        verbose_name_plural = _('التعاميم')
        ordering = ['-date_issued']

    def __str__(self):
        return self.title
