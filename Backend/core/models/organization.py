"""
Security Organization Models — الهيكل التنظيمي الأمني
═══════════════════════════════════════════════════════
الوزارة (ثابتة)
    └── SecurityAdministration (إدارة أمن محافظة X)
            ├── CentralDepartment (إدارة مركزية)
            ├── Branch (فرع)
            └── DistrictPolice (أمن مديرية X)
                    └── Division (قسم) — يتبع أي من الثلاثة
                        └── Unit (وحدة)
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import TimeStampedModel


# ══════════════════════════════════════════════════════════
# المستوى الأول: إدارة أمن المحافظة
# ══════════════════════════════════════════════════════════

class SecurityAdministration(TimeStampedModel):
    """
    إدارة أمن المحافظة — المستوى الأعلى في الهيكل الأمني.
    مثال: إدارة أمن المحافظة الأولى

    مرتبطة بمحافظة جغرافية واحدة (1:1).
    """
    geo_governorate = models.OneToOneField(
        'core.GeoGovernorate',
        on_delete=models.PROTECT,
        related_name='security_admin',
        verbose_name=_('المحافظة الجغرافية'),
    )
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name=_('الاسم'),
        help_text=_('مثال: إدارة أمن المحافظة الأولى'),
    )
    code = models.CharField(
        max_length=20, unique=True, blank=True, null=True,
        verbose_name=_('الكود'),
    )
    head = models.ForeignKey(
        'personnel.PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_security_admin',
        verbose_name=_('المدير العام'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشطة'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))

    class Meta:
        db_table = 'security_administration'
        verbose_name = _('إدارة أمن محافظة')
        verbose_name_plural = _('إدارات أمن المحافظات')
        ordering = ['name']

    def __str__(self):
        return self.name


# ══════════════════════════════════════════════════════════
# المستوى الثاني: الإدارات المركزية / الفروع / أمن المديريات
# ══════════════════════════════════════════════════════════

class CentralDepartment(TimeStampedModel):
    """
    إدارة مركزية — تتبع إدارة أمن المحافظة.
    مثال: إدارة الموارد، إدارة البحث الجنائي
    """
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.CASCADE,
        related_name='central_departments',
        verbose_name=_('إدارة أمن المحافظة'),
    )
    name = models.CharField(max_length=200, verbose_name=_('اسم الإدارة'))
    code = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name=_('الكود'),
    )
    head = models.ForeignKey(
        'personnel.PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_central_dept',
        verbose_name=_('مدير الإدارة'),
    )
    head_position = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('منصب المدير'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشطة'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'central_department'
        verbose_name = _('إدارة مركزية')
        verbose_name_plural = _('الإدارات المركزية')
        ordering = ['security_admin', 'order', 'name']
        unique_together = [('security_admin', 'code')]

    def __str__(self):
        return f"{self.security_admin.name} - {self.name}"


class Branch(TimeStampedModel):
    """
    فرع — يتبع إدارة أمن المحافظة.
    مثال: فرع القوات الخاصة، فرع النجدة
    """
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name=_('إدارة أمن المحافظة'),
    )
    name = models.CharField(max_length=200, verbose_name=_('اسم الفرع'))
    code = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name=_('الكود'),
    )
    head = models.ForeignKey(
        'personnel.PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_branch',
        verbose_name=_('مدير الفرع'),
    )
    head_position = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('منصب المدير'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'branch'
        verbose_name = _('فرع')
        verbose_name_plural = _('الفروع')
        ordering = ['security_admin', 'order', 'name']
        unique_together = [('security_admin', 'code')]

    def __str__(self):
        return f"{self.security_admin.name} - {self.name}"


class DistrictPolice(TimeStampedModel):
    """
    أمن مديرية — يتبع إدارة أمن المحافظة ومرتبط بمديرية جغرافية.
    مثال: أمن مديرية الجوبة

    يُنشأ تلقائياً من yemen-info.json لكل مديرية جغرافية تابعة للمحافظة.
    الاسم يُولّد تلقائياً: "أمن مديرية " + geo_district.name_ar
    """
    security_admin = models.ForeignKey(
        SecurityAdministration,
        on_delete=models.CASCADE,
        related_name='district_police_units',
        verbose_name=_('إدارة أمن المحافظة'),
    )
    geo_district = models.OneToOneField(
        'core.GeoDistrict',
        on_delete=models.PROTECT,
        related_name='police_unit',
        verbose_name=_('المديرية الجغرافية'),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('الاسم'),
        help_text=_('يُولّد تلقائياً: أمن مديرية + اسم المديرية'),
    )
    code = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name=_('الكود'),
    )
    head = models.ForeignKey(
        'personnel.PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_district_police',
        verbose_name=_('مدير أمن المديرية'),
    )
    head_position = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('منصب المدير'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'district_police'
        verbose_name = _('أمن مديرية')
        verbose_name_plural = _('أمن المديريات')
        ordering = ['security_admin', 'order', 'name']

    def save(self, *args, **kwargs):
        # توليد الاسم تلقائياً من المديرية الجغرافية
        if self.geo_district_id and not self.name:
            self.name = f"أمن مديرية {self.geo_district.name_ar}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ══════════════════════════════════════════════════════════
# المستوى الثالث: القسم (يتبع أي من الثلاثة)
# ══════════════════════════════════════════════════════════

class Division(TimeStampedModel):
    """
    القسم — يتبع واحداً فقط من:
    - إدارة مركزية (CentralDepartment)
    - فرع (Branch)
    - أمن مديرية (DistrictPolice)

    يُفرض بـ CHECK constraint أن واحداً فقط من الثلاثة يكون مملوءاً.
    """
    central_department = models.ForeignKey(
        CentralDepartment,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='divisions',
        verbose_name=_('الإدارة المركزية'),
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='divisions',
        verbose_name=_('الفرع'),
    )
    district_police = models.ForeignKey(
        DistrictPolice,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='divisions',
        verbose_name=_('أمن المديرية'),
    )
    name = models.CharField(max_length=200, verbose_name=_('اسم القسم'))
    code = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name=_('الكود'),
    )
    head = models.ForeignKey(
        'personnel.PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_division',
        verbose_name=_('رئيس القسم'),
    )
    head_position = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('منصب رئيس القسم'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'core_division'
        verbose_name = _('قسم')
        verbose_name_plural = _('الأقسام')
        ordering = ['order', 'name']
        constraints = [
            # واحد فقط من الثلاثة يكون مملوءاً
            models.CheckConstraint(
                check=(
                    models.Q(
                        central_department__isnull=False,
                        branch__isnull=True,
                        district_police__isnull=True,
                    ) | models.Q(
                        central_department__isnull=True,
                        branch__isnull=False,
                        district_police__isnull=True,
                    ) | models.Q(
                        central_department__isnull=True,
                        branch__isnull=True,
                        district_police__isnull=False,
                    )
                ),
                name='division_single_parent',
            ),
        ]

    def clean(self):
        super().clean()
        parents = [
            self.central_department_id,
            self.branch_id,
            self.district_police_id,
        ]
        filled = sum(1 for p in parents if p is not None)
        if filled != 1:
            raise ValidationError(
                _('يجب ربط القسم بواحد فقط من: إدارة مركزية، فرع، أو أمن مديرية.')
            )

    @property
    def parent(self):
        """إرجاع الوحدة الأب (إدارة أو فرع أو أمن مديرية)."""
        return self.central_department or self.branch or self.district_police

    @property
    def parent_type(self):
        """نوع الوحدة الأب."""
        if self.central_department_id:
            return 'central_department'
        if self.branch_id:
            return 'branch'
        if self.district_police_id:
            return 'district_police'
        return None

    def __str__(self):
        parent = self.parent
        parent_name = parent.name if parent else '—'
        return f"{parent_name} - {self.name}"


# ══════════════════════════════════════════════════════════
# المستوى الرابع: الوحدة (تتبع القسم)
# ══════════════════════════════════════════════════════════

class Unit(TimeStampedModel):
    """الوحدة — أدنى مستوى تنظيمي، تتبع القسم."""
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name=_('القسم'),
    )
    name = models.CharField(max_length=200, verbose_name=_('اسم الوحدة'))
    code = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name=_('الكود'),
    )
    head = models.ForeignKey(
        'personnel.PersonnelMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_unit',
        verbose_name=_('رئيس الوحدة'),
    )
    head_position = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('منصب رئيس الوحدة'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.IntegerField(default=0, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'core_unit'
        verbose_name = _('وحدة')
        verbose_name_plural = _('الوحدات')
        ordering = ['division', 'order', 'name']

    def __str__(self):
        return f"{self.division.name} - {self.name}"
