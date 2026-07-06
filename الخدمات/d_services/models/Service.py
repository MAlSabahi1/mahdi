"""
نموذج الخدمة - Service Model
الجدول الرئيسي لتعريف الخدمات الديناميكية
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from OpenSoftCoreV4.utils.abstract_models.soft_delete_model import SoftDeleteModel
from OpenSoftCoreV4.utils.abstract_models.ex_id_model import ExIdModel
from d_services.apis.external_methods.base import validate_function_name

from d_services.choices.choices import (
    ServiceCategoryChoice,
    OutputTemplateTypeChoice,
    TargetAudienceComponentChoice,
    BaseComponentChoice,
    InputTemplateTypeChoice,
)
from OpenSoftCoreV4.platform_sync.platform_sync_settings import TypeOfMainSystemChoices


class Service(ExIdModel, SoftDeleteModel):
    code = models.CharField(
        max_length=50,
        verbose_name=_('كود الخدمة')
    )
    name_ar = models.CharField(
        max_length=255,
        verbose_name=_('اسم الخدمة (عربي)')
    )
    name_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('اسم الخدمة (إنجليزي)')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('وصف الخدمة')
    )
    category = models.CharField(
        max_length=100,
        choices=ServiceCategoryChoice.choices,
        default=ServiceCategoryChoice.OTHER,
        verbose_name=_('فئة الخدمة')
    )
    icon = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('أيقونة الخدمة'),
        help_text=_('اسم الأيقونة مثل: mdi-file-document, mdi-certificate')
    )
    
    # إعدادات الخدمة
    requires_approval = models.BooleanField(
        default=True,
        verbose_name=_('تتطلب موافقات')
    )
    is_repeatable = models.BooleanField(
        default=True,
        verbose_name=_('قابلة للتكرار')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('مفعلة')
    )
    
    # التواريخ
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ بدء السريان')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    

    # إعدادات المخرجات
    output_template_type = models.CharField(
        max_length=100,
        choices=OutputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نوع نموذج المخرج')
    )
    input_template_type = models.CharField(
        max_length=100,
        choices=InputTemplateTypeChoice.choices,
        null=True,
        blank=True,
        verbose_name=_('نموذج استمارة الطلب')
    )
    output_data_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب بيانات المخرج'),
        validators=[validate_function_name]
    )
    input_data_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب بيانات الاستماره'),
        validators=[validate_function_name]
    )


    # إعدادات ال ERP
    erp_data_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب بيانات ال ERP'),
        validators=[validate_function_name]
    )
    erp_specialization_data_autolist = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('قائمة التخصصات المتاحة في ال ERP'),
    )   
    erp_study_system_data_autolist = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('قائمة النظم الدراسية المتاحة في ال ERP'),
    )   
    # إعدادات الجمهور المستهدف والمكونات
    target_audience_component = models.CharField(
        max_length=100,
        choices=TargetAudienceComponentChoice.choices,
        verbose_name=_('مكون الجمهور المستهدف')
    )
    # إعدادات المكون الرئيسي والمكونات
    base_audience_component = models.CharField(
        max_length=100,
        choices=BaseComponentChoice.choices,
        verbose_name=_('المكون الرئيسي للخدمة')
    )
    requester_image_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب صورة مقدم الطلب'),
        help_text=_('مثل: get_student_image'),
        validators=[validate_function_name]
    )
    requester_info_function = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('دالة جلب بيانات مقدم الطلب'),
        help_text=_('مثل: get_student_info - ترجع dict يحتوي على name و description'),
        validators=[validate_function_name]
    )

    # نوع النظام المستهدف (للمزامنة من البوابة)
    target_system_type = models.CharField(
        max_length=100,
        choices=TypeOfMainSystemChoices.choices,
        null=True,
        blank=True,
        verbose_name=_('نوع النظام المستهدف'),
        help_text=_('النظام الذي يستقبل طلبات هذه الخدمة من البوابة (جامعات/مدارس/معاهد)')
    )


    def __str__(self):
        return f'{self.code} - {self.name_ar}'


    class Meta:
        verbose_name = _('الخدمة')
        verbose_name_plural = _('الخدمات')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['code'],
                name='unique_service_code',
                condition=Q(is_deleted=False)& models.Q(code__gt=''),
            ),
        ]


# Signal لإنشاء الصلاحيات تلقائياً عند إنشاء خدمة جديدة
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Service)
def create_service_permissions(sender, instance, created, **kwargs):
    """
    إنشاء صلاحيات الخدمة تلقائياً لكل أنواع الصلاحيات عند إنشاء خدمة جديدة
    """
    if created:
        from d_services.models.ServicePermission import ServicePermission
        from d_services.choices.choices import ServicePermissionType
        
        for permission_type in ServicePermissionType.values:
            ServicePermission.objects.get_or_create(
                fk_service=instance,
                permission_type=permission_type
            )
@receiver(post_save, sender=Service)
def create_service_permissions(sender, instance, created, **kwargs):
    """
    إنشاء صلاحيات الخدمة تلقائياً لكل أنواع الصلاحيات عند إنشاء خدمة جديدة
    """
    if created:
        from d_services.models.ServiceSync import ServiceSync
        ServiceSync.objects.create(
            fk_service = instance,
            service_name = instance.name_ar,
        )
        
        



