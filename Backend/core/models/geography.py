"""
Geographic Models — البيانات الجغرافية الموحدة
═══════════════════════════════════════════════════
مصدر الحقيقة الجغرافي الوحيد — يُغذّى من yemen-info.json

التسلسل الهرمي:
    GeoGovernorate (22 محافظة)
        └── GeoDistrict (335 مديرية)
            └── GeoSubDistrict (2234 عزلة)
                └── GeoVillage (41494 قرية)
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import TimeStampedModel


class GeoGovernorate(TimeStampedModel):
    """المحافظة الجغرافية — من yemen-info.json"""

    name_ar = models.CharField(
        max_length=100, unique=True,
        verbose_name=_('الاسم بالعربي'),
    )
    name_en = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي'),
    )
    name_ar_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالعربي (بدون تشكيل)'),
    )
    name_en_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي (موحد)'),
    )
    phone_numbering_plan = models.CharField(
        max_length=10, blank=True,
        verbose_name=_('مفتاح المحافظة'),
    )
    capital_name_ar = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('العاصمة بالعربي'),
    )
    capital_name_en = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('العاصمة بالإنجليزي'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشطة'),
    )

    class Meta:
        db_table = 'geo_governorate'
        verbose_name = _('محافظة جغرافية')
        verbose_name_plural = _('المحافظات الجغرافية')
        ordering = ['name_ar']

    def __str__(self):
        return self.name_ar


class GeoDistrict(TimeStampedModel):
    """المديرية الجغرافية — من yemen-info.json"""

    governorate = models.ForeignKey(
        GeoGovernorate,
        on_delete=models.CASCADE,
        related_name='districts',
        verbose_name=_('المحافظة'),
    )
    name_ar = models.CharField(
        max_length=100,
        verbose_name=_('الاسم بالعربي'),
    )
    name_en = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي'),
    )
    name_ar_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالعربي (بدون تشكيل)'),
    )
    name_en_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي (موحد)'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشطة'),
    )

    class Meta:
        db_table = 'geo_district'
        verbose_name = _('مديرية جغرافية')
        verbose_name_plural = _('المديريات الجغرافية')
        ordering = ['governorate', 'name_ar']
        unique_together = [('governorate', 'name_ar')]
        indexes = [
            models.Index(fields=['governorate']),
        ]

    def __str__(self):
        return f"{self.governorate.name_ar} - {self.name_ar}"


class GeoSubDistrict(TimeStampedModel):
    """العزلة — من yemen-info.json"""

    district = models.ForeignKey(
        GeoDistrict,
        on_delete=models.CASCADE,
        related_name='sub_districts',
        verbose_name=_('المديرية'),
    )
    name_ar = models.CharField(
        max_length=100,
        verbose_name=_('الاسم بالعربي'),
    )
    name_en = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي'),
    )
    name_ar_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالعربي (بدون تشكيل)'),
    )
    name_en_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي (موحد)'),
    )

    class Meta:
        db_table = 'geo_sub_district'
        verbose_name = _('عزلة')
        verbose_name_plural = _('العزل')
        ordering = ['district', 'name_ar']
        indexes = [
            models.Index(fields=['district']),
        ]

    def __str__(self):
        return f"{self.district.name_ar} - {self.name_ar}"


class GeoVillage(TimeStampedModel):
    """القرية — من yemen-info.json"""

    sub_district = models.ForeignKey(
        GeoSubDistrict,
        on_delete=models.CASCADE,
        related_name='villages',
        verbose_name=_('العزلة'),
    )
    name_ar = models.CharField(
        max_length=100,
        verbose_name=_('الاسم بالعربي'),
    )
    name_en = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي'),
    )
    name_ar_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالعربي (بدون تشكيل)'),
    )
    name_en_normalized = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('الاسم بالإنجليزي (موحد)'),
    )

    class Meta:
        db_table = 'geo_village'
        verbose_name = _('قرية')
        verbose_name_plural = _('القرى')
        ordering = ['sub_district', 'name_ar']
        indexes = [
            models.Index(fields=['sub_district']),
        ]

    def __str__(self):
        return self.name_ar
