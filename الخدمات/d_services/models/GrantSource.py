"""
نموذج مزامنة مصدر المنحة - Grant Source Sync Model
لتخزين بيانات الجهات المانحة المتزامنة من نظام أكاديمي خارجي
"""
import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel

from d_services.choices.choices import GrantSourceTypeChoice
from OpenSoftCoreV4.common.models.Branch import Organization

from utils.core.sync_abstract_model import SyncAbastractModel

class GrantSource( SoftDeleteModel):

    external_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        verbose_name=_("المعرف الخارجي للـ ERP")
    )

    # معرف المنظمة
    fk_branch = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='grant_sources',
        verbose_name=_('المنظمة'),
        null=True,
        blank=True
    )

    code = models.CharField(
        max_length=50,
        verbose_name=_('كود الجهة المانحة')
    )
    name_ar = models.CharField(
        max_length=255,
        verbose_name=_('الاسم (عربي)')
    )
    name_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('الاسم (إنجليزي)')
    )
    source_type = models.CharField(
        max_length=100,
        choices=GrantSourceTypeChoice.choices,
        default=GrantSourceTypeChoice.OTHER,
        verbose_name=_('نوع الجهة')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('الوصف')
    )
    contact_person = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('جهة الاتصال')
    )
    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('الهاتف')
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('البريد الإلكتروني')
    )
    default_grant_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('نسبة المنحة الافتراضية (%)')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )


    def __str__(self):
        return f'{self.code} - {self.name_ar}'

    class Meta:
        verbose_name = _('مصدر المنحة')
        verbose_name_plural = _('مصادر المنح')
        constraints = [
            models.UniqueConstraint(
                fields=['code'],
                condition=Q(is_deleted=False),
                name='unique_grant_source_code',
            ),
        ]
    @property
    def partner_data(self):
        return {
            'company_type': 'Company',
            'first_name': self.name_ar,
            'middle_name': None,
            'last_name': None,
            'surename': None,
            'country': self.fk_branch.fk_country.code if hasattr(self.fk_branch, 'fk_country') else None,
            'governorate': self.fk_branch.fk_governorate.code if self.fk_branch.fk_governorate else None,
            'city': self.fk_branch.fk_directorate.code if self.fk_branch.fk_directorate else None,
            'area': self.fk_branch.fk_region.code if self.fk_branch.fk_region else None,
            'branch': None,
            'phone': self.phone,
            'mobile': self.contact_person,
            'email': self.email,
            'website': None,
            'categories': [],
        }