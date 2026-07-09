"""
Personnel Models - نماذج الأفراد
"""
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import (
    SoftDeletableModel, TimeStampedModel, Rank, ServiceStatus,
    JobCategory, JobTitle, Qualification,
    GeoGovernorate, GeoDistrict,
    SecurityAdministration, CentralDepartment, Branch, DistrictPolice,
    Division, Unit, Position, ForceType
)
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
import re
import uuid


# ═══ Name Validators ═══
# ═══ Arabic digit → English digit mapping ═══
ARABIC_DIGIT_MAP = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')

def normalize_phone_number(value):
    """
    تطبيع رقم الهاتف:
    - تحويل الأرقام العربية (٠-٩) إلى إنجليزية (0-9)
    - إزالة المسافات والشرطات
    - معالجة "لا يوجد" / "بدون رقم" → None
    """
    if not value:
        return None
    # معالجة النصوص التي تعني "لا يوجد رقم"
    no_phone_phrases = ['لا يوجد', 'بدون رقم', 'لايوجد', 'بدون', '-', 'لا']
    cleaned = value.strip()
    if cleaned.lower() in no_phone_phrases or cleaned in no_phone_phrases:
        return None
    # تحويل الأرقام العربية → إنجليزية
    cleaned = cleaned.translate(ARABIC_DIGIT_MAP)
    # إزالة المسافات والشرطات
    cleaned = re.sub(r'[\s\-\.\(\)\+]', '', cleaned)
    # إزالة مفتاح الدولة إن وُجد (967 أو 00967)
    if cleaned.startswith('00967'):
        cleaned = cleaned[5:]
    elif cleaned.startswith('967'):
        cleaned = cleaned[3:]
    elif cleaned.startswith('+967'):
        cleaned = cleaned[4:]
    return cleaned if cleaned else None


def validate_arabic_name(value):
    """يمنع إدخال أرقام أو رموز أو أحرف لاتينية في الاسم"""
    if re.search(r'[0-9a-zA-Z]', value):
        raise ValidationError(
            _('الاسم يجب أن يحتوي على أحرف عربية فقط — بدون أرقام أو رموز أو أحرف لاتينية'),
            code='invalid_name_chars',
        )
    # السماح بالعربي + مسافات + الهمزات والتشكيل
    if not re.match(r'^[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\s\-]+$', value.strip()):
        raise ValidationError(
            _('الاسم يحتوي على رموز غير مسموحة'),
            code='invalid_name_symbols',
        )


def validate_name_parts(value):
    """
    الاسم يجب أن يكون رباعياً على الأقل (اسم + أب + جد + لقب).
    الحد الأدنى قابل للتكوين عبر SystemConfig لاحقاً.
    """
    MIN_PARTS = 4  # افتراضي — يمكن جعله ديناميكياً
    MAX_PARTS = 7
    parts = value.strip().split()
    if len(parts) < MIN_PARTS:
        raise ValidationError(
            _('الاسم يجب أن يكون %(min)d أجزاء على الأقل (الاسم + الأب + الجد + اللقب). تم إدخال %(count)d أجزاء فقط.'),
            code='name_too_short',
            params={'min': MIN_PARTS, 'count': len(parts)},
        )
    if len(parts) > MAX_PARTS:
        raise ValidationError(
            _('الاسم يجب ألا يزيد عن %(max)d أجزاء. تم إدخال %(count)d أجزاء.'),
            code='name_too_long',
            params={'max': MAX_PARTS, 'count': len(parts)},
        )

User = get_user_model()


class PersonnelMaster(SoftDeletableModel):
    """
    الملف الأساسي للفرد - الحقيقة المطلقة
    
    ملاحظة مهمة:
    - يوجد Trigger على مستوى PostgreSQL يمنع تعديل military_number مباشرة
    - يوجد Trigger يحسب data_quality_score و is_complete تلقائياً
    - بعد save() استخدم refresh_from_db() للحصول على القيم المحدثة من Triggers
    - يوجد CHECK Constraint يتطلب أن يكون join_date بعد birth_date بـ 18 سنة على الأقل
    
    مثال:
        personnel.save()
        personnel.refresh_from_db()  # للحصول على is_complete و data_quality_score المحدثة
    """
    
    # الهوية
    military_number = models.CharField(
        max_length=7,
        unique=True,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message=_('الرقم العسكري يجب أن يكون 7 أرقام بالضبط')
            )
        ],
        verbose_name=_('الرقم العسكري')
    )
    old_military_number = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message=_('الرقم العسكري القديم يجب أن يكون 7 أرقام')
            )
        ],
        verbose_name=_('الرقم العسكري القديم'),
        help_text=_('يُملأ فقط عند ترقية فرد إلى ضابط أو مجند إلى جندي — يحفظ الرقم القديم للرجوع إليه')
    )
    national_id = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message=_('الرقم الوطني يجب أن يكون 11 رقماً بالضبط')
            )
        ],
        verbose_name=_('الرقم الوطني')
    )
    full_name = models.CharField(
        max_length=200,
        validators=[validate_arabic_name, validate_name_parts],
        verbose_name=_('الاسم الكامل'),
        help_text=_('الاسم الرباعي أو الخماسي مع اللقب — عربي فقط')
    )
    # البيانات الشخصية
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('تاريخ الميلاد'))
    join_date = models.DateField(null=True, blank=True, verbose_name=_('تاريخ الالتحاق'))
    phone_number = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^7\d{8}$',
                message=_('رقم الهاتف يجب أن يتكون من 9 أرقام ويبدأ بالرقم 7')
            )
        ],
        verbose_name=_('رقم الهاتف')
    )
    
    # العلاقات
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('المؤهل الدراسي')
    )
    # الموقع الجغرافي الفعلي (من yemen-info.json)
    geo_location = models.ForeignKey(
        GeoGovernorate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stationed_personnel',
        verbose_name=_('الموقع الجغرافي'),
        help_text=_('المحافظة الجغرافية الفعلية للخدمة والانتشار')
    )
    
    # البيانات الحيوية (للمستقبل)
    photo = models.ImageField(
        upload_to='personnel/photos/',
        null=True,
        blank=True,
        verbose_name=_('الصورة الشخصية')
    )
    fingerprint_hash = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('بصمة (hash)')
    )
    
    # ══════════════════════════════════════════════════════════
    # الهيكل التنظيمي الأمني — المرحلة 2.0
    # ══════════════════════════════════════════════════════════
    
    # المستوى 1: إدارة أمن المحافظة
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.PROTECT,
        null=True,
        related_name='personnel',
        verbose_name=_('إدارة أمن المحافظة')
    )
    
    # ========================================================================
    # [ملاحظات هامة لمطور الواجهة الأمامية - Frontend Developer]:
    # لتبسيط تجربة المستخدم (UX)، لا تعرض هذه الحقول الثلاثة كقوائم منفصلة!
    # يجب دمجها في (قائمة منسدلة واحدة) تُسمى: "جهة العمل الرئيسية" (الإدارة/الفرع/المديرية).
    #
    # **طريقة العرض (UI Design):**
    # يجب أن تكون القائمة مجمعة (Grouped) وقابلة للطي (Collapsible)!
    # بحيث تظهر 3 عناوين رئيسية وبجوارها "سهم صغير" لفتحها:
    # 1. ▶ الإدارات المركزية (عند النقر تفتح لتظهر الإدارات)
    # 2. ▶ الفروع (عند النقر تفتح لتظهر الفروع)
    # 3. ▶ شرطات المديريات (عند النقر تفتح لتظهر المديريات)
    #
    # عندما يختار المستخدم أحدها، يقوم الـ React بتعبئة الـ ID في الحقل الصحيح 
    # (central_department أو branch أو district_police) ويترك الحقلين الآخرين فارغين (null).
    # ========================================================================
    
    # المستوى 2: الفرد يتبع واحداً فقط من الثلاثة
    central_department = models.ForeignKey(
        CentralDepartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('الإدارة المركزية')
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('الفرع')
    )
    district_police = models.ForeignKey(
        DistrictPolice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('شرطة المديرية')
    )
    # ========================================================================
    # [ملاحظات هامة لمطور الواجهة الأمامية - Frontend Developer]:
    # هذه القائمة المنسدلة (القسم) يجب أن لا تظهر جميع الأقسام في قاعدة البيانات!
    # بل يجب أن تتفلتر (Filtered) تلقائياً لتعرض فقط الأقسام التابعة للجهة التي 
    # تم اختيارها في القائمة السابقة (جهة العمل الرئيسية).
    # ========================================================================
    
    # المستوى 3-4: القسم والوحدة
    division = models.ForeignKey(
        Division,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('القسم')
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('الوحدة')
    )
    
    # التوصيف الوظيفي
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('الفئة')
    )
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('نوع العمل')
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('المنصب')
    )
    force_classification = models.ForeignKey(
        ForceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personnel',
        verbose_name=_('تصنيف القوة')
    )
    
    # الحالة الحالية
    current_rank = models.ForeignKey(
        Rank,
        on_delete=models.PROTECT,
        related_name='current_personnel',
        verbose_name=_('الرتبة الحالية')
    )
    current_status = models.ForeignKey(
        ServiceStatus,
        on_delete=models.PROTECT,
        related_name='current_personnel',
        verbose_name=_('نوع الحالة الخدمية (التفصيلي)')
    )
    temp_status_details = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('تفاصيل الحالة المؤقتة'),
        help_text=_('بيانات إضافية مثل: اسم المستشفى، نوع القضية، جهة الانتداب، الخ')
    )
    perm_status_details = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('تفاصيل الحالة النهائية'),
        help_text=_('بيانات إضافية مثل: تاريخ الوفاة، نسبة العجز الطبي، رقم القرار، الخ')
    )
    audit_movement_details = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('تفاصيل التدقيق والحركة'),
        help_text=_('بيانات التنقلات، الانتداب، الغياب، وتصحيح الأسماء')
    )
    # علامة الاكتمال
    is_complete = models.BooleanField(default=False, verbose_name=_('بيانات كاملة'))
    
    # حقول المرحلة 1.5 - معالجة البيانات الفوضوية
    pending_rank = models.ForeignKey(
        Rank,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pending_personnel',
        verbose_name=_('الرتبة المعلقة')
    )

    # ملاحظة: تم حذف is_temporary — لا يوجد رقم عسكري مؤقت (ممنوع مهما كان)
    is_data_clean = models.BooleanField(
        default=False,
        verbose_name=_('بيانات نظيفة')
    )
    data_quality_score = models.IntegerField(
        default=0,
        verbose_name=_('درجة جودة البيانات')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    # محرك التتبع التاريخي (Time Machine)
    history = HistoricalRecords()
    
    # حقول إضافية من البيانات الخام
    # ملاحظة: تم حذف حقل officer_number — الرقم العسكري هو المصدر الوحيد للحقيقة
    # عند ترقية فرد إلى ضابط، يتغير military_number ويُحفظ القديم في old_military_number
    expense_status = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=[
            ('has_expenses', _('لديه نفقات')),
            ('no_expenses', _('بدون نفقات')),
            ('expenses', _('نفقات')),
        ],
        verbose_name=_('حالة النفقات')
    )
    appointment_info = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('معلومات التعيين')
    )
    decision_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ صدور القرار')
    )
    transfer_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ التصدور إلينا')
    )

    
    class Meta:
        db_table = 'personnel_master'
        verbose_name = _('فرد')
        verbose_name_plural = _('الأفراد')
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['full_name']),
            models.Index(fields=['security_admin', 'current_status']),
            models.Index(fields=['current_rank']),
            # فهارس الـ Enterprise
            models.Index(fields=['is_deleted']),
            models.Index(
                fields=['security_admin', 'current_status', 'current_rank'],
                name='idx_hr_dashboard_filter'
            ),
            models.Index(fields=['central_department']),
            models.Index(fields=['branch']),
            models.Index(fields=['district_police']),
        ]
        constraints = [
            # منع تساوي الرقم العسكري القديم مع الحالي
            models.CheckConstraint(
                check=~models.Q(old_military_number=models.F('military_number')),
                name='chk_old_mil_num_differs',
            ),
            # ضمان تفرد الرقم العسكري القديم (مع السماح بعدة NULL)
            models.UniqueConstraint(
                fields=['old_military_number'],
                condition=models.Q(old_military_number__isnull=False),
                name='unique_old_military_number_when_set',
            ),
            # قيد النزاهة الهرمية: يمنع اختيار أكثر من جهة واحدة في نفس الوقت (المستوى الثاني)
            models.CheckConstraint(
                check=(
                    models.Q(central_department__isnull=False, branch__isnull=True, district_police__isnull=True) |
                    models.Q(central_department__isnull=True, branch__isnull=False, district_police__isnull=True) |
                    models.Q(central_department__isnull=True, branch__isnull=True, district_police__isnull=False) |
                    models.Q(central_department__isnull=True, branch__isnull=True, district_police__isnull=True)
                ),
                name='chk_single_level2_hierarchy',
                violation_error_message='لا يمكن أن يتبع الفرد لأكثر من جهة واحدة في نفس الوقت (إدارة مركزية، فرع، أو أمن مديرية).'
            ),
        ]
    
    def __str__(self):
        return f"{self.military_number} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        """
        تحديث تلقائي عند الحفظ:
        1. حساب is_complete
        """
        # حساب is_complete
        self.is_complete = all([
            self.photo,
            self.fingerprint_hash,
            self.national_id,
        ])
        super().save(*args, **kwargs)
    
    def clean(self):
        # 1. تطبيع رقم الهاتف (يجب أن يتم قبل الـ Validation)
        if self.phone_number:
            normalized = normalize_phone_number(self.phone_number)
            self.phone_number = normalized
        
        # 2. إصلاح مشكلة قيد الرقم العسكري القديم (تحويل النص الفارغ إلى Null)
        if self.old_military_number == "":
            self.old_military_number = None

        super().clean()
        # ============================================================
        # تشغيل محرك القواعد (Rules Engine)
        # ============================================================
        from systems.personnel.rules_engine.core import RulesEngine
        engine = RulesEngine.get_default()
        engine.execute_all(self)
    
    # ============================================================================
    # ثوابت حالة الرقم الوطني (للاستخدام في الـ Serializers والـ Views)
    # ============================================================================
    NATIONAL_ID_STATUS_CHOICES = [
        ('valid', _('صحيح')),
        ('missing', _('ناقص')),
        ('invalid_format', _('صيغة غير صحيحة')),
        ('invalid_length', _('طول غير صحيح')),
    ]
    NATIONAL_ID_STATUS_DISPLAY = {
        'valid': 'صحيح',
        'missing': 'ناقص',
        'invalid_format': 'صيغة غير صحيحة',
        'invalid_length': 'طول غير صحيح',
    }

    # ============================================================================
    # خصائص محسوبة (Computed Properties)
    # ============================================================================

    @property
    def military_number_type(self):
        """
        تحديد نوع الرقم العسكري بناءً على البادئة.
        المرجع: تحليل البيانات الخام + كلام رئيس الخدمات.
        
        بادئة 60 → ضابط
        بادئة 7  → أساسي أفراد
        بادئة 50 → لجان أمنية أفراد أو مستجدين جديد
                   (TODO: تحديد المعيار الدقيق للتفريق بين لجان ومستجدين — مطلوب مراجعة مع رئيس الخدمات)
        
        Returns: dict with 'type' and 'label' keys
        """
        if not self.military_number or len(self.military_number) < 2:
            return {'type': 'unknown', 'label': 'غير محدد'}
        
        prefix = self.military_number[:2]
        first_digit = self.military_number[0]
        
        if prefix == '60':
            return {'type': 'officer', 'label': 'ضابط'}
        elif first_digit == '7':
            return {'type': 'basic_personnel', 'label': 'أساسي أفراد'}
        elif first_digit == '5':
            # TODO: مراجعة — متى يكون "لجان أمنية" ومتى "مستجدين جديد"؟
            # حالياً نصنفه كـ "لجان/مستجدين" ويحتاج اختيار يدوي لتصنيف القوة
            return {'type': 'committee_or_newcomer', 'label': 'لجان أمنية أفراد / مستجدين'}
        else:
            return {'type': 'unknown', 'label': 'بادئة غير معروفة'}

    @property
    def national_id_status(self):
        """حالة الرقم الوطني — محسوبة تلقائياً من البيانات، صادقة دائماً"""
        if not self.national_id:
            return 'missing'
        if not self.national_id.isdigit():
            return 'invalid_format'
        if len(self.national_id) != 11:
            return 'invalid_length'
        return 'valid'

    @property
    def national_id_status_display(self):
        """العرض النصي لحالة الرقم الوطني"""
        return self.NATIONAL_ID_STATUS_DISPLAY.get(self.national_id_status, 'غير معروف')

    @property
    def age(self):
        """حساب العمر"""
        from datetime import date
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    @property
    def service_years(self):
        """حساب سنوات الخدمة"""
        from datetime import date
        if not self.join_date:
            return None
        today = date.today()
        return today.year - self.join_date.year - (
            (today.month, today.day) < (self.join_date.month, self.join_date.day)
        )



# ============================================================================
# المرحلة 1.5: نماذج معالجة البيانات الفوضوية
# ============================================================================

class RawDataImport(TimeStampedModel):
    """سجل الإدخال الأول الخام - شبكة الأمان"""
    
    row_index = models.IntegerField(verbose_name=_('رقم الصف'))
    raw_data = models.JSONField(verbose_name=_('البيانات الخام'))
    import_batch_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('معرف دفعة الاستيراد')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('قيد الانتظار')),
            ('processed', _('تمت المعالجة')),
            ('error', _('خطأ')),
        ],
        default='pending',
        verbose_name=_('الحالة')
    )
    error_message = models.TextField(
        blank=True,
        verbose_name=_('رسالة الخطأ')
    )
    # رابط بالفرد المُنشأ — يُملأ بعد المعالجة الناجحة لتجنّب السجلات اليتيمة (Orphaned)
    linked_personnel = models.ForeignKey(
        'PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='raw_imports',
        verbose_name=_('الفرد المرتبط'),
        help_text=_('يُعبّأ بعد تحويل الصف الخام إلى سجل فرد فعلي')
    )
    
    class Meta:
        db_table = 'personnel_raw_data_import'
        verbose_name = _('بيانات خام مستوردة')
        verbose_name_plural = _('البيانات الخام المستوردة')
        ordering = ['import_batch_id', 'row_index']
        indexes = [
            models.Index(fields=['import_batch_id']),
            models.Index(fields=['status']),
            models.Index(fields=['linked_personnel']),
        ]
    
    def __str__(self):
        return f"Row {self.row_index} - Batch {str(self.import_batch_id)[:8]}"


class SuggestedCorrection(TimeStampedModel):
    """
    اقتراحات التصحيح — فصل البيانات المقترحة عن المعتمدة.

    قواعد المرفقات (مطبّقة في clean()):
    ─────────────────────────────────────────
    • name_correction          → مرفق إلزامي (نموذج 23 + صورة البطاقة)
    • national_id_correction   → مرفق مطلوب عبر Service Layer حسب الدور
    • rank_correction          → يُعالج عبر RankSettlement (نموذج منفصل)
    • military_number_correction → مرفق وزاري إلزامي
    """

    CORRECTION_TYPE_CHOICES = [
        ('name_correction', _('تصحيح الاسم')),
        ('national_id_correction', _('تصحيح الرقم الوطني')),
        ('military_number_correction', _('تصحيح الرقم العسكري')),
        ('data_correction', _('تصحيح بيانات أخرى')),
    ]

    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('approved', _('موافق عليه')),
        ('rejected', _('مرفوض')),
    ]

    # ── خريطة متطلبات المرفقات لكل نوع تصحيح ──
    # حقوق التحقق مطبقة على مستويين:
    #   required=True  → يرفض clean() الحفظ بدون مرفق عند الطلب
    #   required=False → يُتحقق منه في Service Layer حسب صلاحية المستخدم
    DOCUMENT_REQUIREMENTS = {
        'name_correction': {
            'required': True,
            'description': _('صورة البطاقة الشخصية أو نموذج 23'),
            'note': 'إجراء رسمي كامل وفق الدليل الإرشادي البند 8',
            'approval_required': True,     # يتطلب مذكرة وزارية عند الموافقة
            'ministry_required': True,     # يمر عبر الوزارة
        },
        'national_id_correction': {
            'required': False,             # يُتحقق في Service Layer حسب صلاحية المستخدم
            'description': _('صورة البطاقة الوطنية (أمام + خلف)'),
            'note': 'يُتحقق منه عند الموافقة في PersonnelService',
            'approval_required': False,    # يوافق عليه رئيس الخدمات داخلياً
            'ministry_required': False,
        },
        'military_number_correction': {
            'required': True,
            'description': _('قرار وزاري رسمي'),
            'note': 'أعلى مستوى حساسية — مرفق إلزامي عند الطلب وعند الموافقة',
            'approval_required': True,
            'ministry_required': True,
        },
    }
    
    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='suggested_corrections',
        verbose_name=_('الفرد')
    )
    security_admin = models.ForeignKey(
        'core.SecurityAdministration',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='suggested_corrections',
        verbose_name=_('إدارة الأمن')
    )
    field_name = models.CharField(
        max_length=50,
        verbose_name=_('اسم الحقل')
    )
    old_value = models.TextField(
        blank=True,
        verbose_name=_('القيمة القديمة')
    )
    new_value = models.TextField(
        verbose_name=_('القيمة الجديدة')
    )
    correction_type = models.CharField(
        max_length=30,
        choices=CORRECTION_TYPE_CHOICES,
        verbose_name=_('نوع التصحيح')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('الحالة')
    )
    supporting_document = models.ForeignKey(
        'storage.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='corrections',
        verbose_name=_('المستند الداعم (الطلب)')
    )
    approval_document = models.ForeignKey(
        'storage.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_corrections',
        verbose_name=_('مستند الموافقة (مذكرة الوزارة)')
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requested_corrections',
        verbose_name=_('طلب بواسطة')
    )
    requested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الطلب')
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_corrections',
        verbose_name=_('راجع بواسطة')
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ المراجعة')
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name=_('سبب الرفض')
    )
    # ── بيانات إضافية مرنة (JSON) — تستوعب حقولاً غير متوقعة ──
    # استخدام رئيسي في military_number_correction:
    #   {'other_personnel_id': 42, 'other_military_number': '0012345',
    #    'other_full_name': 'محمد علي', 'rank_at_correction': 'ملازم'}
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('بيانات إضافية')
    )
    # ── ربط طلبين مترابطين — حالة تبديل الرقم العسكري بين شخصين ──
    linked_correction = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_corrections',
        verbose_name=_('الطلب المرتبط (تبديل الأرقام)')
    )
    # ── ملاحظات داخلية — تواصل مقدم الطلب مع رئيس الخدمات ──
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name=_('ملاحظات داخلية')
    )
    is_printed = models.BooleanField(
        default=False,
        verbose_name=_('تمت الطباعة')
    )
    class Meta:
        db_table = 'personnel_suggested_correction'
        verbose_name = _('اقتراح تصحيح')
        verbose_name_plural = _('اقتراحات التصحيح')
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['correction_type', 'status']),
            models.Index(fields=['requested_at']),
        ]
    
    def __str__(self):
        return f"{self.get_correction_type_display()} - {self.personnel}"

    def clean(self):
        """
        التحقق من صحة البيانات قبل الحفظ:
        1. المرفق إلزامي لتصحيح الاسم والرقم العسكري.
        2. لا يمكن تعديل طلب موافق عليه أو مرفوض.
        3. الفرد المحذوف لا يقبل طلبات جديدة.
        """
        from django.core.exceptions import ValidationError

        # ── 1. فحص حالة الفرد ──
        if self.personnel_id and self.personnel and self.personnel.is_deleted:
            raise ValidationError(
                _('لا يمكن إنشاء طلب تصحيح لفرد محذوف من النظام.')
            )

        # ── 2. فحص المرفق الإلزامي ──
        req = self.DOCUMENT_REQUIREMENTS.get(self.correction_type, {})
        if req.get('required') and not self.supporting_document_id:
            raise ValidationError({
                'supporting_document': _(
                    'هذا النوع من التصحيح يتطلب مرفقاً داعماً: %(desc)s'
                ) % {'desc': req.get('description', '')}
            })

        # ── 3. تجميد السجلات المكتملة ──
        if self.pk:  # تعديل سجل موجود
            try:
                original = SuggestedCorrection.objects.get(pk=self.pk)
                if original.status in ('approved', 'rejected'):
                    # السماح فقط بحقول المراجعة عند الرفض
                    immutable_changed = (
                        original.correction_type != self.correction_type
                        or original.field_name != self.field_name
                        or original.old_value != self.old_value
                        or original.new_value != self.new_value
                        or original.personnel_id != self.personnel_id
                    )
                    if immutable_changed:
                        raise ValidationError(
                            _('لا يمكن تعديل بيانات طلب تم البت فيه (موافق/مرفوض).')
                        )
            except SuggestedCorrection.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def requires_document(self):
        """هل هذا النوع يتطلب مرفقاً إلزامياً؟"""
        return self.DOCUMENT_REQUIREMENTS.get(
            self.correction_type, {}
        ).get('required', False)

    @property
    def document_description(self):
        """وصف المرفق المطلوب لهذا النوع"""
        return self.DOCUMENT_REQUIREMENTS.get(
            self.correction_type, {}
        ).get('description', '')


class HistoricalMonthlyVariables(TimeStampedModel):
    """
    سجل المتغيرات الشهرية — حل مشكلة الأعمدة الأفقية في الإكسل
    ═══════════════════════════════════════════════════════════════════
    بدل إنشاء عمود جديد كل شهر (متغير أبريل، متغير مايو...)
    كل متغير يُسجّل كسطر مستقل مرتبط بالفرد + الشهر + نوع المتغير.

    يُستخدم لـ:
    1. أرشفة المتغيرات المستوردة من ملفات الإكسل القديمة
    2. تسجيل المتغيرات الشهرية الجارية (الشهر الحالي)
    3. استعراض سجل المتغيرات في تبويب "سجل المتغيرات" في ملف الفرد
    4. تصدير المتغيرات للوزارة
    """

    SOURCE_CHOICES = [
        ('excel_import', _('استيراد من إكسل')),
        ('manual', _('إدخال يدوي')),
        ('system', _('النظام تلقائياً')),
    ]

    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.CASCADE,
        related_name='monthly_variables',
        verbose_name=_('الفرد')
    )
    month = models.CharField(
        max_length=7,
        verbose_name=_('الشهر'),
        help_text=_('بصيغة YYYY-MM')
    )
    variable_type = models.ForeignKey(
        'core.VariableType',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='monthly_records',
        verbose_name=_('نوع المتغير'),
        help_text=_('من القاموس الموحد — فارغ فقط للسجلات المستوردة القديمة')
    )
    variable_value = models.TextField(
        verbose_name=_('قيمة المتغير'),
        help_text=_('النص الأصلي — يُحفظ دائماً حتى لو تم الربط بالقاموس')
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='manual',
        verbose_name=_('المصدر')
    )
    source_column = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_('العمود المصدر'),
        help_text=_('اسم العمود الأصلي في الإكسل — يُملأ تلقائياً عند الاستيراد')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='monthly_variables_created',
        verbose_name=_('أُدخل بواسطة')
    )

    class Meta:
        db_table = 'personnel_historical_monthly_variables'
        verbose_name = _('متغير شهري')
        verbose_name_plural = _('المتغيرات الشهرية')
        ordering = ['personnel', '-month']
        indexes = [
            models.Index(fields=['personnel', 'month']),
            models.Index(fields=['month']),
            models.Index(fields=['variable_type']),
            models.Index(fields=['source']),
            # فهرس مركّب للاستعلام السريع عن كل متغيرات نوع محدد لفرد محدد
            models.Index(
                fields=['personnel', 'variable_type'],
                name='idx_mv_person_vartype'
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['personnel', 'month', 'source_column'],
                condition=models.Q(source='excel_import'),
                name='unique_monthly_variable_import'
            ),
        ]

    def __str__(self):
        type_name = self.variable_type.name if self.variable_type else self.variable_value[:30]
        return f"{self.personnel.military_number} - {self.month} - {type_name}"


class RankSettlement(TimeStampedModel):
    """
    طلب تسوية الرتبة — نموذج متكامل لإدارة عملية الترقية
    
    المرجع: الدليل الإرشادي - البند 17 (الترقيات من واقع القرارات)
    
    سيناريوهات الاستخدام:
    ─────────────────────────────────────
    1. ترقية فرد ضمن الأفراد (مثل: جندي → عريف)
       - يتغير: current_rank فقط
       - يتطلب: مرفق قرار الترقية
    
    2. ترقية ضابط ضمن الضباط (مثل: ملازم → نقيب)
       - يتغير: current_rank فقط
       - يتطلب: مرفق قرار الترقية
    
    3. تسوية فرد إلى ضابط (مثل: مساعد1 → ملازم ثاني)
       - يتغير: current_rank + military_number (يبدأ بـ 60)
       - يُحفظ: الرقم القديم في old_military_number
       - يتطلب: مرفق قرار الترقية + الرقم العسكري الجديد
    
    ملاحظة: هذا النموذج يدعم طلبات فردية وجماعية.
    الوزارة أحياناً ترسل قوائم ترقيات لعدة أفراد دفعة واحدة — يمكن
    ربطها عبر batch_reference.
    """
    
    SETTLEMENT_TYPE_CHOICES = [
        ('same_class_promotion', _('ترقية ضمن نفس الصنف')),
        ('personnel_to_officer', _('تسوية فرد إلى ضابط')),
        ('demotion', _('تخفيض رتبة (عقوبة/قرار قضائي)')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('قيد الانتظار')),
        ('approved', _('تمت الموافقة')),
        ('rejected', _('مرفوض')),
        ('applied', _('تم التطبيق')),
    ]
    
    # الفرد المعني
    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.CASCADE,
        related_name='rank_settlements',
        verbose_name=_('الفرد')
    )
    
    # نوع التسوية
    settlement_type = models.CharField(
        max_length=30,
        choices=SETTLEMENT_TYPE_CHOICES,
        verbose_name=_('نوع التسوية')
    )
    
    # الرتبة الحالية (وقت الطلب — تُحفظ للتاريخ)
    from_rank = models.ForeignKey(
        Rank,
        on_delete=models.PROTECT,
        related_name='settlements_from',
        verbose_name=_('من رتبة')
    )
    
    # الرتبة المطلوبة
    to_rank = models.ForeignKey(
        Rank,
        on_delete=models.PROTECT,
        related_name='settlements_to',
        verbose_name=_('إلى رتبة')
    )
    
    # الرقم العسكري الجديد — مطلوب فقط في حالة فرد → ضابط
    new_military_number = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message=_('الرقم العسكري الجديد يجب أن يكون 7 أرقام')
            )
        ],
        verbose_name=_('الرقم العسكري الجديد'),
        help_text=_('مطلوب فقط عند تسوية فرد إلى ضابط — يجب أن يبدأ بـ 60')
    )
    
    # بيانات القرار الرسمي
    decision_number = models.CharField(
        max_length=50,
        verbose_name=_('رقم القرار/المذكرة')
    )
    decision_date = models.DateField(
        verbose_name=_('تاريخ القرار')
    )
    
    # المرفق الرسمي (إلزامي)
    supporting_document = models.ForeignKey(
        'storage.Document',
        on_delete=models.PROTECT,
        related_name='rank_settlements',
        verbose_name=_('المرفق الرسمي'),
        help_text=_('صورة القرار الرسمي — إلزامي')
    )
    
    # مرجع الدفعة — لربط ترقيات جماعية
    batch_reference = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('مرجع الدفعة'),
        help_text=_('لربط عدة ترقيات صادرة بنفس القرار')
    )
    
    # الحالة
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('حالة الطلب')
    )
    
    # التدقيق
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requested_settlements',
        verbose_name=_('طلب بواسطة')
    )
    applied_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applied_settlements',
        verbose_name=_('تم التطبيق بواسطة')
    )
    applied_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ التطبيق')
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name=_('سبب الرفض')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    
    class Meta:
        db_table = 'personnel_rank_settlement'
        verbose_name = _('طلب تسوية رتبة')
        verbose_name_plural = _('طلبات تسوية الرتب')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['personnel', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['batch_reference']),
            models.Index(fields=['decision_date']),
        ]
    
    def __str__(self):
        return f"{self.personnel} — {self.from_rank} → {self.to_rank} ({self.get_status_display()})"
    
    def clean(self):
        super().clean()
        
        # ============================================================
        # 1. الرتبة المطلوبة: التحقق حسب نوع التسوية
        # المرجع: الدليل الإرشادي - البند 17
        # ============================================================
        if self.from_rank_id and self.to_rank_id:
            if self.from_rank_id == self.to_rank_id:
                raise ValidationError({
                    'to_rank': _('الرتبة المطلوبة لا يمكن أن تكون نفس الرتبة الحالية.')
                })
            
            if self.settlement_type == 'demotion':
                # التخفيض: الرتبة المطلوبة يجب أن تكون أقل
                if self.to_rank.order <= self.from_rank.order:
                    raise ValidationError({
                        'to_rank': _(
                            'التخفيض يتطلب اختيار رتبة أقل من الحالية.'
                        )
                    })
            else:
                # الترقية: الرتبة المطلوبة يجب أن تكون أعلى
                if self.to_rank.order > self.from_rank.order:
                    raise ValidationError({
                        'to_rank': _(
                            'الترقية يجب أن تكون لرتبة أعلى. '
                            'المرجع: الدليل الإرشادي، البند 17.'
                        )
                    })
        
        # ============================================================
        # 2. تسوية فرد → ضابط يتطلب رقم عسكري جديد يبدأ بـ 60
        # ============================================================
        if self.settlement_type == 'personnel_to_officer':
            if not self.new_military_number:
                raise ValidationError({
                    'new_military_number': _(
                        'تسوية فرد إلى ضابط تتطلب إدخال الرقم العسكري الجديد.'
                    )
                })
            if not self.new_military_number.startswith('60'):
                raise ValidationError({
                    'new_military_number': _(
                        'الرقم العسكري الجديد للضابط يجب أن يبدأ بـ 60.'
                    )
                })
            
            # التحقق أن الرتبة المطلوبة هي رتبة ضابط
            if self.to_rank_id and not self.to_rank.is_officer:
                raise ValidationError({
                    'to_rank': _(
                        'تسوية فرد إلى ضابط تتطلب اختيار رتبة من رتب الضباط.'
                    )
                })
        
        # ============================================================
        # 3. ترقية ضمن نفس الصنف — لا يتطلب رقم عسكري جديد
        # ============================================================
        if self.settlement_type == 'same_class_promotion' and self.new_military_number:
            raise ValidationError({
                'new_military_number': _(
                    'ترقية ضمن نفس الصنف لا تتطلب رقماً عسكرياً جديداً.'
                )
            })


# ============================================================================
# السجل التاريخي والأحداث (Timeline / Events)
# ============================================================================

class PersonnelEvent(TimeStampedModel):
    """
    سجل الأحداث التاريخية للفرد: الترقيات، التنقلات، التعديلات الهامة.
    """
    EVENT_TYPE_CHOICES = [
        ('promotion', _('ترقية')),
        ('transfer', _('نقل')),
        ('status_change', _('تغيير حالة')),
        ('correction', _('تصحيح بيانات')),
        ('document_added', _('إضافة مستند')),
        ('note', _('ملاحظة عامة')),
        ('other', _('أخرى')),
    ]

    personnel = models.ForeignKey(
        PersonnelMaster,
        on_delete=models.CASCADE,
        related_name='personnel_events',
        verbose_name=_('الفرد')
    )
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPE_CHOICES,
        verbose_name=_('نوع الحدث')
    )
    event_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الحدث')
    )
    description = models.TextField(
        verbose_name=_('وصف الحدث')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_personnel_events',
        verbose_name=_('بواسطة')
    )

    class Meta:
        db_table = 'personnel_event'
        verbose_name = _('حدث')
        verbose_name_plural = _('الأحداث')
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.personnel.full_name}"

    @property
    def event_type_display(self):
        return dict(self.EVENT_TYPE_CHOICES).get(self.event_type, self.event_type)


class MonthlySnapshot(models.Model):
    """
    جدول اللقطة الشهرية (الأرشيف التاريخي).
    يتم تسجيل لقطة لحالة الفرد في نهاية كل شهر لتكون مرجعاً ثابتاً لا يتأثر بالتعديلات اللاحقة.
    """
    personnel = models.ForeignKey(PersonnelMaster, on_delete=models.CASCADE, related_name='monthly_snapshots', verbose_name=_('الفرد'))
    snapshot_date = models.CharField(max_length=7, verbose_name=_('تاريخ اللقطة (YYYY-MM)'))
    
    # نسخة من الحقول الأساسية لسهولة الاستعلام دون فتح الـ JSON
    rank = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('الرتبة'))
    status_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('الحالة'))
    unit_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('الجهة'))
    
    # نسخة كاملة من البيانات
    snapshot_data = models.JSONField(verbose_name=_('بيانات الفرد كاملة'), help_text=_('لقطة JSON كاملة لجميع حقول الفرد وقت الأرشفة'))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('بواسطة'))

    class Meta:
        db_table = 'personnel_monthly_snapshot'
        verbose_name = _('لقطة شهرية')
        verbose_name_plural = _('اللقطات الشهرية')
        unique_together = ('personnel', 'snapshot_date')
        indexes = [
            models.Index(fields=['snapshot_date']),
        ]

    def __str__(self):
        return f"{self.personnel.military_number} - {self.snapshot_date}"
