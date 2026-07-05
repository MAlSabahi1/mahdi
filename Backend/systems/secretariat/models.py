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


class CorrespondenceAttachment(SoftDeletableModel):
    correspondence = models.ForeignKey(Correspondence, on_delete=models.CASCADE, related_name='attachments', verbose_name=_('المراسلة المرتبطة'))
    file = models.FileField(upload_to='correspondence_attachments/', verbose_name=_('الملف'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان المرفق'))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الرفع'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('مرفق المراسلة')
        verbose_name_plural = _('مرفقات المراسلات')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class MeetingMinutes(SoftDeletableModel):
    title = models.CharField(max_length=255, verbose_name=_('عنوان الاجتماع'))
    date = models.DateField(verbose_name=_('تاريخ الاجتماع'))
    attendees = models.ManyToManyField(PersonnelMaster, related_name='meetings_attended', verbose_name=_('الحاضرين من المنتسبين'))
    external_attendees = models.TextField(blank=True, null=True, verbose_name=_('الحاضرين من الخارج'))
    content = models.TextField(verbose_name=_('محضر الاجتماع/النقاش'))
    decisions = models.TextField(blank=True, null=True, verbose_name=_('القرارات والتوصيات'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='meeting_minutes', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_meetings', verbose_name=_('منشئ المحضر'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('محضر اجتماع')
        verbose_name_plural = _('محاضر الاجتماعات')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.date}"


class DocumentWorkRequest(SoftDeletableModel):
    class Type(models.TextChoices):
        PRINT = 'print', _('طباعة')
        PHOTOCOPY = 'photocopy', _('تصوير ورق')
        SCAN = 'scan', _('مسح ضوئي')
        OTHER = 'other', _('أخرى')

    class Status(models.TextChoices):
        PENDING = 'pending', _('قيد الانتظار')
        IN_PROGRESS = 'in_progress', _('جاري التنفيذ')
        COMPLETED = 'completed', _('مكتمل')
        CANCELLED = 'cancelled', _('ملغي')

    type = models.CharField(max_length=20, choices=Type.choices, default=Type.PRINT, verbose_name=_('نوع العمل المكتبى'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('الحالة'))
    title = models.CharField(max_length=255, verbose_name=_('العنوان/الموضوع'))
    description = models.TextField(blank=True, null=True, verbose_name=_('الوصف/تعليمات إضافية'))
    copies_count = models.PositiveIntegerField(default=1, verbose_name=_('عدد النسخ'))
    pages_count = models.PositiveIntegerField(default=1, verbose_name=_('عدد الصفحات للنسخة'))
    
    requested_by = models.ForeignKey(PersonnelMaster, on_delete=models.SET_NULL, null=True, related_name='document_requests', verbose_name=_('الموظف طالب الخدمة'))
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name=_('تاريخ الاكتمال'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='document_requests', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_document_requests', verbose_name=_('منشئ الطلب'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('طلب أعمال مكتبية')
        verbose_name_plural = _('طلبات الأعمال المكتبية')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class InventoryItem(SoftDeletableModel):
    class Type(models.TextChoices):
        STATIONERY = 'stationery', _('قرطاسية ومواد مكتبية')
        FURNITURE = 'furniture', _('أثاث مكتبي')
        EQUIPMENT = 'equipment', _('أجهزة وتجهيزات')
        OTHER = 'other', _('أخرى')

    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_('نوع المادة'))
    name = models.CharField(max_length=255, verbose_name=_('اسم المادة'))
    code = models.CharField(max_length=100, unique=True, verbose_name=_('كود المادة/الباركود'))
    quantity_in_stock = models.PositiveIntegerField(default=0, verbose_name=_('الكمية في المخزن'))
    unit = models.CharField(max_length=50, default=_('حبة'), verbose_name=_('الوحدة'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='inventory_items', verbose_name=_('إدارة الأمن'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('مادة مخزنية')
        verbose_name_plural = _('المواد المخزنية')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class InventoryRequest(SoftDeletableModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('قيد الانتظار')
        APPROVED = 'approved', _('تم الصرف/الموافقة')
        REJECTED = 'rejected', _('مرفوض')

    item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name='requests', verbose_name=_('المادة المطلوبة'))
    requested_by = models.ForeignKey(PersonnelMaster, on_delete=models.SET_NULL, null=True, related_name='inventory_requests', verbose_name=_('الموظف طالب الصرف'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('الكمية المطلوبة'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('الحالة'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات المتابعة والرفض/الموافقة'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='inventory_requests', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_inventory_requests', verbose_name=_('منشئ الطلب'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('طلب صرف مواد')
        verbose_name_plural = _('طلبات صرف المواد')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requested_by} - {self.item.name} ({self.quantity})"


class Custody(SoftDeletableModel):
    class Status(models.TextChoices):
        ASSIGNED = 'assigned', _('في العهدة')
        RETURNED = 'returned', _('تم إرجاعها')
        DAMAGED = 'damaged', _('تالفة')

    item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name='custodies', verbose_name=_('المادة (الأثاث/الجهاز)'))
    assigned_to = models.ForeignKey(PersonnelMaster, on_delete=models.PROTECT, related_name='custodies', verbose_name=_('الموظف المستلم'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('الكمية'))
    date_assigned = models.DateField(verbose_name=_('تاريخ الاستلام/الإسناد'))
    date_returned = models.DateField(blank=True, null=True, verbose_name=_('تاريخ الإرجاع'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED, verbose_name=_('الحالة'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('تفاصيل وملاحظات العهدة'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='custodies', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_custodies', verbose_name=_('منشئ القيد'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('عهدة موظف')
        verbose_name_plural = _('عهد الموظفين')
        ordering = ['-date_assigned']

    def __str__(self):
        return f"{self.assigned_to} - {self.item.name} ({self.quantity})"


class AttendanceLog(SoftDeletableModel):
    class Status(models.TextChoices):
        PRESENT = 'present', _('حاضر')
        ABSENT = 'absent', _('غائب')
        LATE = 'late', _('متأخر')
        LEAVE = 'leave', _('إجازة/رخصة')

    employee = models.ForeignKey(PersonnelMaster, on_delete=models.CASCADE, related_name='attendance_logs', verbose_name=_('الموظف'))
    date = models.DateField(verbose_name=_('التاريخ'))
    check_in = models.TimeField(blank=True, null=True, verbose_name=_('وقت الحضور'))
    check_out = models.TimeField(blank=True, null=True, verbose_name=_('وقت الانصراف'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT, verbose_name=_('الحالة'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات/أسباب التأخير والغياب'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='attendance_logs', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attendance_logs', verbose_name=_('مسجل الحضور'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('سجل دوام يومي')
        verbose_name_plural = _('سجلات الدوام اليومية')
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee__full_name']

    def __str__(self):
        return f"{self.employee} - {self.date} ({self.get_status_display()})"


class FinancialAllocation(SoftDeletableModel):
    month = models.DateField(verbose_name=_('شهر الاعتماد (تاريخ أول يوم في الشهر)'))
    allocated_amount = models.DecimalField(max_length=15, max_digits=12, decimal_places=2, verbose_name=_('قيمة الاعتماد المالي المرصود'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات وتفاصيل الاعتماد'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='financial_allocations', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_allocations', verbose_name=_('منشئ القيد'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('الاعتماد المالي الشهري')
        verbose_name_plural = _('الاعتمادات المالية الشهرية')
        unique_together = ('security_admin', 'month')
        ordering = ['-month']

    def __str__(self):
        return f"{self.month.strftime('%Y-%m')} - {self.allocated_amount}"


class Expense(SoftDeletableModel):
    allocation = models.ForeignKey(FinancialAllocation, on_delete=models.CASCADE, related_name='expenses', verbose_name=_('الاعتماد المالي المرتبط'))
    amount = models.DecimalField(max_length=15, max_digits=12, decimal_places=2, verbose_name=_('المبلغ المصروف'))
    date = models.DateField(verbose_name=_('تاريخ الصرف'))
    description = models.TextField(verbose_name=_('بيان الصرف/الوصف'))
    category = models.CharField(max_length=100, verbose_name=_('بند الصرف (قرطاسية، صيانة، نقل، ضيافة، إلخ)'))
    receipt_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('رقم سند الصرف/الفاتورة'))
    
    security_admin = models.ForeignKey(SecurityAdministration, on_delete=models.PROTECT, related_name='expenses', verbose_name=_('إدارة الأمن'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses', verbose_name=_('مسجل المصروف'))
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('مستند صرف/مصروف')
        verbose_name_plural = _('المصروفات والسندات')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"
