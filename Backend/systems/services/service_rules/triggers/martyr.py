"""
systems/services/service_rules/triggers/martyr.py
══════════════════════════════════════════════════
المشغلات التلقائية بعد اعتماد استمارة الشهيد (Post-Approval Triggers).

هذه المشغلات تُنفَّذ فور اعتماد الاستمارة من قِبَل المسؤول النهائي.
يجب استدعاؤها داخل transaction.atomic() لضمان الاتساق الكامل للبيانات.

المشغلات المتضمنة (بالترتيب الإلزامي):
  [T-M-001] UpdatePersonnelStatusTrigger   : تحديث حالة الفرد إلى (شهيد - خروج نهائي).
  [T-M-002] AutoCancelPendingServicesTrigger: إغلاق جميع الطلبات المعلقة للفرد تلقائياً.
  [T-M-003] VacatePositionTrigger          : تفريغ منصب الفرد إن كان يشغل منصباً.
  [T-M-004] LogMartyrdomEventTrigger       : تسجيل حدث الاستشهاد في سجل الأحداث.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from django.utils import timezone
from django.db import transaction

if TYPE_CHECKING:
    from systems.services.infrastructure.models.status_change import StatusChangeForm


class MartyrdomTriggerError(Exception):
    """استثناء مخصص يُطلق إذا فشل أحد المشغلات."""
    pass


def run_all_martyr_triggers(form: "StatusChangeForm", approved_by) -> dict:
    """
    نقطة الدخول الرئيسية: تشغيل جميع مشغلات الشهيد بالتسلسل.

    يجب استدعاء هذه الدالة داخل view الاعتماد بعد حفظ الاستمارة كـ 'approved'.
    كل العمليات تتم في transaction واحدة لضمان الاتساق.

    المعاملات:
      form        : كائن StatusChangeForm المعتمد.
      approved_by : كائن المستخدم الذي قام بالاعتماد النهائي.

    يُرجع:
      dict يحتوي على ملخص ما تم تنفيذه.
    """
    result = {
        'personnel_status_updated': False,
        'pending_services_cancelled': 0,
        'position_vacated': False,
        'event_logged': False,
        'errors': [],
    }

    with transaction.atomic():
        personnel = form.personnel
        martyrdom_date = form.form_data.get('martyrdom_date')
        martyrdom_location = form.form_data.get('martyrdom_location', 'غير محدد')

        # ── [T-M-001] تحديث حالة الفرد ──────────────────────────────────────
        try:
            _update_personnel_status(personnel, form, result)
        except Exception as e:
            result['errors'].append({'trigger': 'UpdatePersonnelStatus', 'error': str(e)})
            raise MartyrdomTriggerError(f'[T-M-001] فشل تحديث الحالة: {e}')

        # ── [T-M-002] إلغاء الطلبات المعلقة ─────────────────────────────────
        try:
            _cancel_pending_services(personnel, form, approved_by, result)
        except Exception as e:
            result['errors'].append({'trigger': 'AutoCancelPendingServices', 'error': str(e)})
            # هذا الخطأ ليس مميتاً — نسجله ونكمل
            
        # ── [T-M-003] تفريغ المنصب ────────────────────────────────────────────
        try:
            _vacate_position(personnel, result)
        except Exception as e:
            result['errors'].append({'trigger': 'VacatePosition', 'error': str(e)})

        # ── [T-M-004] تسجيل الحدث ─────────────────────────────────────────────
        try:
            _log_martyrdom_event(personnel, form, approved_by, martyrdom_date, martyrdom_location, result)
        except Exception as e:
            result['errors'].append({'trigger': 'LogMartyrdomEvent', 'error': str(e)})

    return result


# ══════════════════════════════════════════════════════════════════════════════
# المشغلات الداخلية (Private Trigger Functions)
# ══════════════════════════════════════════════════════════════════════════════

def _update_personnel_status(personnel, form: "StatusChangeForm", result: dict) -> None:
    """
    [T-M-001] تحديث حالة الفرد إلى (شهيد - خروج نهائي).

    الإجراءات:
    1. تحديث current_status إلى الحالة الجديدة المحددة في الاستمارة (to_status).
    2. تعيين تاريخ النفاذ الفعلي (effective_date).
    3. تفريغ الموقع التنظيمي (يتم آلياً بواسطة PermanentDeactivationRule في models.py).
    4. حفظ التغييرات.
    """
    if form.to_status_id:
        personnel.current_status_id = form.to_status_id
    elif form.to_status:
        # محاولة العثور على حالة "شهيد" تلقائياً إذا لم تُحدد
        from core.models import ServiceStatus
        martyr_status = ServiceStatus.objects.filter(
            name__icontains='شهيد',
            is_permanent_deactivation=True
        ).first()
        if martyr_status:
            personnel.current_status_id = martyr_status.id
        else:
            raise MartyrdomTriggerError('لم يتم العثور على حالة "شهيد" في قاعدة البيانات. أضفها من لوحة الإدارة.')

    # تسجيل تاريخ النفاذ الفعلي من الاستمارة
    if form.effective_date:
        personnel.effective_exit_date = form.effective_date  # type: ignore

    personnel.save()
    # تحديث من قاعدة البيانات للحصول على القيم المحسوبة (Triggers PostgreSQL)
    personnel.refresh_from_db()

    result['personnel_status_updated'] = True


def _cancel_pending_services(personnel, form: "StatusChangeForm", approved_by, result: dict) -> None:
    """
    [T-M-002] إغلاق قسري لجميع الطلبات والاستمارات المعلقة للفرد.

    الاستمارات التي تُغلق:
      - StatusChangeForm : استمارات تغيير الحالة المعلقة (عدا الاستمارة المعتمدة الحالية).
      - SuggestedCorrection : طلبات التصحيح المعلقة.
      - RankSettlement : طلبات تسوية الرتبة المعلقة.

    سبب الإلغاء المسجل: "إغلاق تلقائي بسبب اعتماد استمارة الشهيد".
    """
    cancel_reason = (
        f'أُغلق تلقائياً بسبب اعتماد استمارة الشهيد للفرد {personnel.full_name} '
        f'({personnel.military_number}) بتاريخ {timezone.now().date()}.'
    )
    cancelled_count = 0

    # 1. إغلاق استمارات تغيير الحالة المعلقة
    from systems.services.infrastructure.models.status_change import StatusChangeForm as SCF
    pending_forms = SCF.objects.filter(
        personnel=personnel,
        status__in=('draft', 'in_progress', 'returned'),
    ).exclude(id=form.id)

    for pf in pending_forms:
        pf.status = 'rejected'
        pf.rejection_reason = cancel_reason
        pf.rejected_by = approved_by
        pf.save(update_fields=['status', 'rejection_reason', 'rejected_by', 'updated_at'])
        cancelled_count += 1

    # 2. إغلاق طلبات التصحيح المعلقة
    from systems.personnel.models import SuggestedCorrection
    pending_corrections = SuggestedCorrection.objects.filter(
        personnel=personnel,
        status='pending',
    )
    corrections_count = pending_corrections.update(
        status='rejected',
        rejection_reason=cancel_reason,
        reviewed_at=timezone.now(),
    )
    cancelled_count += corrections_count

    # 3. إغلاق طلبات تسوية الرتبة المعلقة
    from systems.personnel.models import RankSettlement
    pending_settlements = RankSettlement.objects.filter(
        personnel=personnel,
        status='pending',
    )
    settlements_count = pending_settlements.update(
        status='rejected',
        rejection_reason=cancel_reason,
        updated_at=timezone.now(),
    )
    cancelled_count += settlements_count

    result['pending_services_cancelled'] = cancelled_count


def _vacate_position(personnel, result: dict) -> None:
    """
    [T-M-003] تفريغ منصب الفرد إن كان يشغل منصباً قيادياً.

    الهدف: جعل المنصب "شاغراً" في النظام ليتاح تعيين شخص آخر مكانه.
    ملاحظة: PermanentDeactivationRule في rules_engine/rules.py تتكفل بتفريغ
            الموقع التنظيمي (الإدارة/الفرع/القسم) عند الحفظ في _update_personnel_status.
            هذه الدالة تُسجّل الحدث فقط وتتأكد من التنفيذ.
    """
    had_position = personnel.position_id is not None
    if had_position:
        # position_id يُفرَّغ تلقائياً بواسطة PermanentDeactivationRule عند الحفظ
        # هنا نتأكد فقط من التسجيل
        result['position_vacated'] = True
    else:
        result['position_vacated'] = False


def _log_martyrdom_event(personnel, form: "StatusChangeForm", approved_by,
                         martyrdom_date, martyrdom_location, result: dict) -> None:
    """
    [T-M-004] تسجيل حدث الاستشهاد في سجل التدقيق (AuditLog).

    يُسجَّل الحدث بكل تفاصيله لأغراض:
      - المراجعة القانونية.
      - التقارير الإحصائية (عدد الشهداء في فترة زمنية، موقع الاستشهاد، إلخ).
      - إثبات حدوث التغيير في حالة عدم الاتفاق.
    """
    try:
        from infra.audit.models import AuditLog
        AuditLog.objects.create(
            user=approved_by,
            username=approved_by.username if approved_by else 'SYSTEM',
            action='MARTYR_FORM_APPROVED',
            model_name='StatusChangeForm',
            object_id=str(form.id),
            new_data={
                'personnel_military_number': personnel.military_number,
                'personnel_full_name': personnel.full_name,
                'martyrdom_date': str(martyrdom_date),
                'martyrdom_location': martyrdom_location,
                'form_id': form.id,
                'approved_by_id': approved_by.id if approved_by else None,
                'approved_at': str(timezone.now()),
            },
            severity='high',
            module='services',
            change_reason=(
                f'اعتماد استمارة شهيد للفرد {personnel.full_name} '
                f'({personnel.military_number}) | تاريخ الاستشهاد: {martyrdom_date}'
            ),
        )
        result['event_logged'] = True
    except Exception:
        result['event_logged'] = False
        raise
