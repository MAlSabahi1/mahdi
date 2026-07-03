"""
systems/services/models.py
═══════════════════════════
⭐ جسر الاستيراد — لا تعديل هنا.

كل النماذج انتقلت إلى:
    systems/services/infrastructure/models/

هذا الملف يعيد تصديرها للحفاظ على التوافق الخلفي مع:
- admin.py
- views.py
- serializers.py
- tasks.py
- اختبارات الـ tests/
وأي كود يستورد من `systems.services.models`.

الاستيراد الصحيح الجديد (اختياري):
    from systems.services.infrastructure.models import StatusChangeForm
"""

# ── إعادة تصدير كل النماذج ──────────────────────────────────────────────────
from systems.services.infrastructure.models import (  # noqa: F401
    ServiceEventLog,
    StagingRecord,
    ReconciliationTask,
    MonthlySnapshot,
    DirectorateCompliance,
    ExportLog,
    RejectionLog,
    WebhookConfig,
    ReportTemplate,
    CustomFormTemplate,
    CustomReportTemplate,
    StatusChangeForm,
)

# ── Re-exports للتوافق الخلفي (من الكود الأصلي) ─────────────────────────────
from infra.audit.models import AuditLog          # noqa: F401
from core.models import NotificationRecord       # noqa: F401

__all__ = [
    # Infrastructure Models
    'ServiceEventLog',
    'StagingRecord',
    'ReconciliationTask',
    'MonthlySnapshot',
    'DirectorateCompliance',
    'ExportLog',
    'RejectionLog',
    'WebhookConfig',
    'ReportTemplate',
    'CustomFormTemplate',
    'CustomReportTemplate',
    'StatusChangeForm',
    # Re-exports
    'AuditLog',
    'NotificationRecord',
]
