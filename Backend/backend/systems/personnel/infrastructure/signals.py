"""
Personnel Signals — إشارات وحدة الأفراد
══════════════════════════════════════════
1. إغلاق طلبات التصحيح المعلقة عند الحذف الناعم لفرد.
2. التأكد من ترتيب العمليات بالتسلسل الصحيح.
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger('personnel.signals')


@receiver(post_save, sender='personnel.PersonnelMaster')
def close_pending_corrections_on_soft_delete(sender, instance, created, **kwargs):
    """
    عند الحذف الناعم لـ PersonnelMaster (is_deleted=True):
    → يُغلق جميع طلبات SuggestedCorrection المعلقة تلقائياً
    → يُسجّل الحدث في AuditLog

    المبرر: طلب التصحيح لفرد محذوف لا قيمة له ويتسبب في بيانات يتيمة.
    """
    if created:
        return  # السجلات الجديدة لا تحتاج هذا الإجراء

    # التحقق أن is_deleted تغيّر إلى True
    if not instance.is_deleted:
        return

    # استيراد داخلي لتجنب الحلقات الدائرية
    from systems.personnel.models import SuggestedCorrection
    from infra.audit.models import AuditLog

    pending_qs = SuggestedCorrection.objects.filter(
        personnel=instance,
        status='pending',
    )
    count = pending_qs.count()

    if count == 0:
        return

    # إغلاق الطلبات المعلقة
    pending_qs.update(
        status='rejected',
        rejection_reason=(
            'أُغلق تلقائياً — الفرد أُزيل من النظام (حذف ناعم). '
            f'الرقم العسكري: {instance.military_number}'
        ),
        reviewed_at=timezone.now(),
    )

    # تسجيل في AuditLog
    try:
        AuditLog.objects.create(
            user=None,  # عملية نظام تلقائية
            username='SYSTEM',
            action='AUTO_REJECT',
            model_name='SuggestedCorrection',
            object_id=instance.military_number,
            new_data={
                'reason': 'soft_delete_triggered',
                'closed_corrections_count': count,
                'personnel_military_number': instance.military_number,
                'personnel_full_name': instance.full_name,
            },
            severity='medium',
            module='personnel',
            change_reason=(
                f'إغلاق تلقائي لـ {count} طلب تصحيح معلق '
                f'بسبب حذف الفرد {instance.military_number}'
            ),
        )
    except Exception as exc:
        # لا نوقف العملية الأساسية بسبب فشل AuditLog
        logger.error(
            'Failed to create AuditLog for auto-reject corrections '
            'on soft-delete of %s: %s',
            instance.military_number, exc,
        )

    logger.info(
        'Auto-rejected %d pending correction(s) for soft-deleted '
        'personnel %s (%s)',
        count, instance.military_number, instance.full_name,
    )
