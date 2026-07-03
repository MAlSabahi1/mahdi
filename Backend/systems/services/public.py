"""
systems/services/public.py
═══════════════════════════
🔒 الواجهة العامة لنظام الخدمات — Public API

هذا هو المكان الوحيد الذي يُسمح فيه لأنظمة أخرى باستيراد أي شيء من نظام الخدمات.

القاعدة الصارمة:
    ✅ مسموح:  from systems.services.public import ...
    ❌ ممنوع:  from systems.services.models import ...
    ❌ ممنوع:  from systems.services.application.services.xxx import ...
    ❌ ممنوع:  from systems.services.infrastructure.models.xxx import ...

الأنظمة التي قد تحتاج هذه الواجهة:
    - systems.secretariat  ← عند بناؤه
    - systems.information  ← عند بناؤه
    - systems.recruitment  ← عند بناؤه
"""

# ── نماذج القراءة العامة (Read-only DTOs) ──────────────────────────────────
from systems.services.infrastructure.models.status_change import StatusChangeForm
from systems.services.infrastructure.models.staging import StagingRecord
from systems.services.infrastructure.models.snapshots import MonthlySnapshot

# ── خدمات يُسمح باستخدامها خارجياً ────────────────────────────────────────
from systems.services.application.services.attachment_service import AttachmentService

# ── استعلامات مفيدة للأنظمة الأخرى ────────────────────────────────────────


def get_personnel_service_status(military_number: str) -> dict:
    """
    جلب الحالة الخدمية الحالية للفرد.
    يُستخدم من: الأمانة العامة، نظام النظم والمعلومات.
    """
    from systems.services.infrastructure.models.status_change import StatusChangeForm
    last_approved = StatusChangeForm.objects.filter(
        personnel__military_number=military_number,
        status='approved',
    ).order_by('-updated_at').first()

    if not last_approved:
        return {'has_active_form': False, 'form_type': None}

    return {
        'has_active_form': True,
        'form_type': last_approved.form_type,
        'effective_date': last_approved.effective_date,
    }


def get_pending_forms_count(security_admin_id: int) -> int:
    """
    عدد الاستمارات المعلقة لإدارة أمن معينة.
    يُستخدم لعرض الإشعارات في الأنظمة الأخرى.
    """
    from systems.services.infrastructure.models.status_change import StatusChangeForm
    return StatusChangeForm.objects.filter(
        security_admin_id=security_admin_id,
        status__in=['pending_services', 'pending_hr', 'pending_director'],
    ).count()


def get_monthly_snapshot(security_admin_id: int, service_month: str) -> dict | None:
    """
    جلب اللقطة الشهرية لإدارة أمن وشهر محددين.
    يُستخدم من: نظام النظم والمعلومات للتقارير المركزية.
    """
    snapshot = MonthlySnapshot.objects.filter(
        security_admin_id=security_admin_id,
        service_month=service_month,
    ).first()

    if not snapshot:
        return None

    return {
        'service_month': snapshot.service_month,
        'locked': snapshot.locked,
        'data': snapshot.data,
    }


__all__ = [
    # Models (read-only references)
    'StatusChangeForm',
    'StagingRecord',
    'MonthlySnapshot',
    # Services
    'AttachmentService',
    # Query functions
    'get_personnel_service_status',
    'get_pending_forms_count',
    'get_monthly_snapshot',
]
