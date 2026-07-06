"""
AccessPolicy Model — السياسات الديناميكية
═══════════════════════════════════════════
Dynamic Policy Engine: شروط مركّبة تتحكم بالوصول.

بدلاً من صلاحيات ثابتة، يمكن تعريف شروط مثل:
    إذا كان المستخدم مديراً
    وإذا كان من نفس الفرع
    وإذا كان الملف غير مؤرشف
    → اسمح بالتعديل

الشروط تُخزّن كـ JSON:
    [
        {"field": "user.branch_id", "op": "eq", "value_ref": "obj.branch_id"},
        {"field": "obj.status",     "op": "ne", "value": "archived"}
    ]

العمليات المدعومة (op):
    eq, ne, gt, lt, gte, lte, in, not_in, contains, is_null
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import TimeStampedModel


class PolicyEffect(models.TextChoices):
    """تأثير السياسة: سماح أو منع."""
    ALLOW = 'allow', _('سماح')
    DENY = 'deny', _('منع')


class AccessPolicy(TimeStampedModel):
    """
    سياسة وصول ديناميكية — شروط مركّبة.

    القواعد:
        - deny يتغلب على allow (Deny-First)
        - الأولوية الأعلى تُنفَّذ أولاً
        - الشروط تُقيّم كـ AND (جميعها يجب أن تتحقق)
        - value_ref: يشير لحقل ديناميكي (user.branch_id, obj.status)
        - value: قيمة ثابتة
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('اسم السياسة'),
    )
    code = models.CharField(
        max_length=100, unique=True, db_index=True,
        verbose_name=_('الرمز'),
        help_text=_('رمز فريد للسياسة'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('الوصف'),
    )
    permission_code = models.CharField(
        max_length=100,
        verbose_name=_('الصلاحية المستهدفة'),
        help_text=_('كود الصلاحية التي تُطبَّق عليها: personnel.edit.all'),
    )
    model_name = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name=_('النموذج المستهدف'),
        help_text=_('اسم النموذج: PersonnelMaster, Document (فارغ = كل النماذج)'),
    )
    conditions = models.JSONField(
        default=list,
        verbose_name=_('الشروط'),
        help_text=_(
            'قائمة شروط JSON. كل شرط: '
            '{"field": "user.branch_id", "op": "eq", "value_ref": "obj.branch_id"}'
        ),
    )
    effect = models.CharField(
        max_length=10,
        choices=PolicyEffect.choices,
        default=PolicyEffect.ALLOW,
        verbose_name=_('التأثير'),
    )
    priority = models.IntegerField(
        default=0,
        verbose_name=_('الأولوية'),
        help_text=_('رقم أعلى = أولوية أعلى — يُنفَّذ أولاً'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشطة'),
    )
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_policies',
        verbose_name=_('أُنشئت بواسطة'),
    )

    class Meta:
        db_table = 'authorization_access_policy'
        verbose_name = _('سياسة وصول')
        verbose_name_plural = _('سياسات الوصول')
        ordering = ['-priority', 'name']
        indexes = [
            models.Index(fields=['permission_code', 'is_active']),
            models.Index(fields=['-priority']),
            models.Index(fields=['model_name']),
        ]

    def __str__(self) -> str:
        return f"[{self.effect}] {self.name} — {self.permission_code}"
