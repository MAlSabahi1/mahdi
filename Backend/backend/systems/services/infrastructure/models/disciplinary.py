"""
Infrastructure Models: Disciplinary Actions Unit — وحدة الجزاءات والانضباط
═══════════════════════════════════════════════════════════════════════════
يغطي:
  - DisciplinaryAction       → سجل الجزاءات والإجراءات (إنذار، وقف، خصم...)
  - AbsenceRecord            → سجل الغيابات وكشوفات المنقطعين
  - DisciplinaryCouncilVerdict → أحكام المجلس التأديبي

قرارات هندسية مبنية على هيكل النظام الحالي:
  - الوقف عن العمل يُحدِّث current_status للفرد إلى inactive_temp تلقائياً
  - دورة التسجيل مباشرة (موظف الخدمات يُسجّل بمجرد وصول القرار)
  - الإرسال للوزارة مرتبط برقم دفعة (ministry_sent_batch) لربطه برفع الخدمات
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from core.models import TimeStampedModel, SecurityAdministration
from systems.personnel.models import PersonnelMaster
from infra.storage.models import Document

User = get_user_model()


# ══════════════════════════════════════════════════════════════════════════════
# 1. سجل الجزاءات والإجراءات
# ══════════════════════════════════════════════════════════════════════════════

class DisciplinaryAction(TimeStampedModel):
    """
    سجل الجزاءات والإجراءات التأديبية

    يشمل كل إجراء يُتخذ بحق فرد بسبب مخالفة أو تقصير:
    - إنذارات كتابية/شفهية صادرة من الرئيس المباشر
    - إيقاف عن العمل (يُحدِّث حالة الفرد تلقائياً)
    - خصومات مالية وحبس عسكري
    - أحكام تخفيض الرتبة (مرتبطة بـ RankSettlement)

    [ملاحظة للـ Frontend]:
    عند اختيار action_type = 'suspension':
      - يجب إظهار حقل duration_days كإلزامي
      - عند الحفظ يتغير current_status للفرد إلى inactive_temp تلقائياً
    """

    class ActionType(models.TextChoices):
        WARNING_VERBAL  = 'warning_verbal',  _('إنذار شفهي')
        WARNING_WRITTEN = 'warning_written', _('إنذار كتابي')
        SALARY_DEDUCT   = 'salary_deduction', _('خصم من الراتب')
        SUSPENSION      = 'suspension',      _('إيقاف عن العمل')
        DEMOTION        = 'demotion',        _('تخفيض رتبة')
        DETENTION       = 'military_detention', _('حبس عسكري')
        DISMISSAL       = 'dismissal',       _('فصل من الخدمة')
        OTHER           = 'other',           _('أخرى')

    class SourceType(models.TextChoices):
        DIRECT_SUPERIOR  = 'direct_superior', _('رئيس مباشر')
        DISCIPLINARY_COUNCIL = 'disciplinary_council', _('مجلس تأديبي')
        JUDICIAL         = 'judicial',        _('قضائي')
        MINISTRY         = 'ministry',        _('وزارة')

    class Status(models.TextChoices):
        ACTIVE    = 'active',    _('قيد التنفيذ')
        EXECUTED  = 'executed',  _('منفذ')
        CANCELLED = 'cancelled', _('ملغى')
        APPEALED  = 'appealed',  _('قيد الطعن')

    # ── الفرد والجهة ──
    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        related_name='disciplinary_actions',
        verbose_name=_('الفرد المعني'),
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='disciplinary_actions',
        verbose_name=_('إدارة الأمن'),
    )

    # ── بيانات الجزاء ──
    action_type = models.CharField(
        max_length=30,
        choices=ActionType.choices,
        verbose_name=_('نوع الجزاء'),
    )
    source_type = models.CharField(
        max_length=30,
        choices=SourceType.choices,
        verbose_name=_('مصدر القرار'),
    )
    issued_by_name = models.CharField(
        max_length=200,
        verbose_name=_('الجهة المُصدِرة'),
        help_text=_('اسم الرئيس أو المجلس أو المحكمة التي أصدرت القرار'),
    )
    decision_ref = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('رقم القرار / الأمر'),
    )
    issued_date = models.DateField(
        verbose_name=_('تاريخ صدور الجزاء'),
    )
    effective_date = models.DateField(
        verbose_name=_('تاريخ سريانه'),
    )
    duration_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('المدة (بالأيام)'),
        help_text=_('يُملأ للإيقاف والحبس العسكري'),
    )
    description = models.TextField(
        verbose_name=_('وصف المخالفة'),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_('الحالة'),
    )

    # ── الإبلاغ ──
    ministry_notified = models.BooleanField(
        default=False,
        verbose_name=_('تم إبلاغ الإدارة العامة'),
    )
    ministry_notified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الإبلاغ'),
    )
    ministry_sent_batch = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('رقم دفعة الإرسال'),
        help_text=_('يُربط بدفعة رفع الخدمات الشهرية لمتابعة التنفيذ'),
    )

    # ── الإداريون والمرفقات ──
    attachments = models.ManyToManyField(
        Document,
        blank=True,
        related_name='disciplinary_actions',
        verbose_name=_('المرفقات'),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_disciplinary_actions',
        verbose_name=_('سجّله'),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات داخلية'),
    )

    class Meta:
        app_label = 'services'
        db_table = 'services_disciplinary_action'
        verbose_name = _('جزاء تأديبي')
        verbose_name_plural = _('الجزاءات التأديبية')
        ordering = ['-issued_date']
        indexes = [
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['action_type', 'status']),
            models.Index(fields=['security_admin', 'issued_date']),
            models.Index(fields=['ministry_notified']),
        ]

    def __str__(self):
        return f"{self.get_action_type_display()} — {self.personnel} ({self.issued_date})"

    def clean(self):
        # إلزامية المدة للإيقاف والحبس
        if self.action_type in (self.ActionType.SUSPENSION, self.ActionType.DETENTION):
            if not self.duration_days:
                raise ValidationError({
                    'duration_days': _('المدة بالأيام إلزامية لجزاء الإيقاف والحبس العسكري.')
                })
        # تاريخ السريان يجب أن يكون بعد أو مساوياً لتاريخ الصدور
        if self.effective_date and self.issued_date:
            if self.effective_date < self.issued_date:
                raise ValidationError({
                    'effective_date': _('تاريخ السريان لا يمكن أن يسبق تاريخ صدور الجزاء.')
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self._state.adding
        super().save(*args, **kwargs)

        # ── عند إيقاف الفرد: تحديث حالته تلقائياً ──
        if self.action_type == self.ActionType.SUSPENSION and self.status == self.Status.ACTIVE:
            from core.models import ServiceStatus
            suspension_status = ServiceStatus.objects.filter(
                classification='inactive_temp'
            ).first()
            if suspension_status:
                # نحدِّث مباشرة بدون تشغيل Rules Engine لتفادي التعارض
                PersonnelMaster.objects.filter(
                    military_number=self.personnel_id
                ).update(current_status=suspension_status)

        # ── عند إلغاء الإيقاف: استرداد حالة الفرد الأصلية ──
        if (
            self.action_type == self.ActionType.SUSPENSION
            and self.status == self.Status.CANCELLED
            and not is_new
        ):
            # نُرجعه لقوة عاملة فعلية — المدير يمكن تعديل ذلك لاحقاً
            from core.models import ServiceStatus
            active_status = ServiceStatus.objects.filter(
                classification='active_full'
            ).first()
            if active_status:
                PersonnelMaster.objects.filter(
                    military_number=self.personnel_id
                ).update(current_status=active_status)


# ══════════════════════════════════════════════════════════════════════════════
# 2. سجل الغيابات وكشوفات المنقطعين
# ══════════════════════════════════════════════════════════════════════════════

class AbsenceRecord(TimeStampedModel):
    """
    سجل الغيابات — كشوفات الغياب وقوائم المتواصلين

    مصادر البيانات:
    - كشوفات غياب ترفعها الإدارات والمديريات
    - مطابقة الخدمات الشهرية (يظهر الفرد غائباً في كشف الخدمات)

    الدورة:
    1. ترِد الكشوفة من الوحدة → تُسجَّل هنا
    2. يراجعها موظف الخدمات مع الخدمات الشهرية
    3. يُبلَّغ الإدارة العامة للقوى البشرية عبر مدير أمن المحافظة
    4. يُتخذ الإجراء القانوني (قد يُنشئ DisciplinaryAction مرتبطاً)
    """

    class AbsenceType(models.TextChoices):
        UNAUTHORIZED       = 'unauthorized',        _('غياب بدون إذن')
        CONTINUOUS         = 'continuous_absence',  _('انقطاع متواصل')
        IN_MONTHLY         = 'absent_in_monthly',   _('غائب في الخدمات الشهرية')
        SUSPENDED          = 'suspended',            _('موقوف بقرار')

    class Source(models.TextChoices):
        UNIT_REPORT   = 'unit_report',   _('بلاغ الوحدة')
        MONTHLY_SHEET = 'monthly_sheet', _('كشف الخدمات الشهري')
        DIRECTORATE   = 'directorate',  _('كشف المديرية')
        BRANCH        = 'branch',        _('كشف الفرع')

    class Status(models.TextChoices):
        PENDING          = 'pending',          _('قيد المراجعة')
        NOTIFIED_MINISTRY= 'notified_ministry',_('تم الإبلاغ للإدارة العامة')
        ACTION_TAKEN     = 'action_taken',     _('تم اتخاذ إجراء')
        CLOSED           = 'closed',           _('مغلق — عاد للعمل')

    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        related_name='absence_records',
        verbose_name=_('الفرد الغائب'),
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='absence_records',
        verbose_name=_('إدارة الأمن'),
    )
    absence_type = models.CharField(
        max_length=30,
        choices=AbsenceType.choices,
        verbose_name=_('نوع الغياب'),
    )
    from_date = models.DateField(verbose_name=_('من تاريخ'))
    to_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('إلى تاريخ'),
        help_text=_('اتركه فارغاً إذا لم يعد الفرد بعد'),
    )
    reported_by_unit = models.CharField(
        max_length=200,
        verbose_name=_('الوحدة المُبلِّغة'),
    )
    source = models.CharField(
        max_length=30,
        choices=Source.choices,
        verbose_name=_('مصدر البلاغ'),
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('الحالة'),
    )

    # ── الإبلاغ والمتابعة ──
    ministry_notified = models.BooleanField(
        default=False,
        verbose_name=_('تم الإبلاغ للإدارة العامة'),
    )
    ministry_notified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الإبلاغ'),
    )
    ministry_sent_batch = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('رقم دفعة الإرسال'),
    )

    # ── ربط بالجزاء المترتب ──
    linked_action = models.ForeignKey(
        DisciplinaryAction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='absence_records',
        verbose_name=_('الجزاء المترتب'),
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_absence_records',
        verbose_name=_('سجّله'),
    )
    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))

    class Meta:
        app_label = 'services'
        db_table = 'services_absence_record'
        verbose_name = _('سجل غياب')
        verbose_name_plural = _('سجلات الغياب')
        ordering = ['-from_date']
        indexes = [
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['security_admin', 'from_date']),
            models.Index(fields=['absence_type']),
            models.Index(fields=['ministry_notified']),
        ]

    def __str__(self):
        return f"{self.personnel} — {self.get_absence_type_display()} ({self.from_date})"

    def clean(self):
        if self.to_date and self.from_date and self.to_date < self.from_date:
            raise ValidationError({
                'to_date': _('تاريخ الانتهاء لا يمكن أن يسبق تاريخ البداية.')
            })

    @property
    def duration_days(self):
        """عدد أيام الغياب (None إذا لم يُحدَّد تاريخ النهاية)"""
        if self.from_date and self.to_date:
            return (self.to_date - self.from_date).days
        return None


# ══════════════════════════════════════════════════════════════════════════════
# 3. أحكام المجلس التأديبي
# ══════════════════════════════════════════════════════════════════════════════

class DisciplinaryCouncilVerdict(TimeStampedModel):
    """
    أحكام المجلس التأديبي

    دورة الحياة:
    1. يصل الحكم من المجلس التأديبي → يُسجَّل هنا بحالة 'received'
    2. تُحفَظ نسخة في ملف الفرد (attachments)
    3. ترسل نسخة للإدارة العامة للقوى البشرية للتنفيذ
       - إما مع دورة رفع الخدمات (ministry_sent_batch)
       - أو منفردة (ministry_sent_at)
    4. عند التنفيذ تصبح 'executed' وقد تُنشئ DisciplinaryAction مرتبطاً
    """

    class VerdictType(models.TextChoices):
        ACQUITTAL   = 'acquittal',   _('براءة')
        WARNING     = 'warning',     _('إنذار')
        DEMOTION    = 'demotion',    _('تخفيض رتبة')
        SUSPENSION  = 'suspension',  _('إيقاف مؤقت')
        DISMISSAL   = 'dismissal',   _('فصل من الخدمة')
        OTHER       = 'other',       _('أخرى')

    class Status(models.TextChoices):
        RECEIVED        = 'received',        _('مستلَم — في انتظار الإيداع')
        FILED           = 'filed',           _('مودَع في ملف المعني')
        SENT_MINISTRY   = 'sent_ministry',   _('أُرسِل للإدارة العامة')
        EXECUTED        = 'executed',        _('منفَّذ')
        APPEALED        = 'appealed',        _('قيد الطعن / الاستئناف')

    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.PROTECT,
        related_name='disciplinary_verdicts',
        verbose_name=_('الفرد المحكوم عليه'),
    )
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='disciplinary_verdicts',
        verbose_name=_('إدارة الأمن'),
    )

    verdict_ref = models.CharField(
        max_length=100,
        verbose_name=_('رقم الحكم'),
    )
    verdict_date = models.DateField(
        verbose_name=_('تاريخ صدور الحكم'),
    )
    verdict_type = models.CharField(
        max_length=30,
        choices=VerdictType.choices,
        verbose_name=_('نوع الحكم'),
    )
    verdict_details = models.TextField(
        verbose_name=_('تفاصيل الحكم'),
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.RECEIVED,
        verbose_name=_('الحالة'),
    )

    # ── التتبع والإرسال ──
    ministry_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الإرسال للإدارة العامة'),
    )
    ministry_sent_batch = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('رقم دفعة الإرسال'),
        help_text=_('يُربط بدفعة رفع الخدمات لمتابعة ما لم يُرسَل بعد'),
    )

    # ── الجزاء المترتب على الحكم ──
    linked_action = models.ForeignKey(
        DisciplinaryAction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verdicts',
        verbose_name=_('الجزاء المترتب على الحكم'),
    )

    attachments = models.ManyToManyField(
        Document,
        blank=True,
        related_name='disciplinary_verdicts',
        verbose_name=_('نسخ الحكم والمرفقات'),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_verdicts',
        verbose_name=_('سجّله'),
    )
    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))

    class Meta:
        app_label = 'services'
        db_table = 'services_disciplinary_verdict'
        verbose_name = _('حكم تأديبي')
        verbose_name_plural = _('الأحكام التأديبية')
        ordering = ['-verdict_date']
        indexes = [
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['security_admin', 'verdict_date']),
            models.Index(fields=['verdict_type']),
            models.Index(fields=['ministry_sent_at']),
            models.Index(fields=['ministry_sent_batch']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['verdict_ref', 'security_admin'],
                name='unique_verdict_ref_per_admin',
            ),
        ]

    def __str__(self):
        return f"حكم {self.verdict_ref} — {self.personnel} ({self.get_verdict_type_display()})"
