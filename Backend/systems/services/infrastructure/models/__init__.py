"""
infrastructure/models/__init__.py
══════════════════════════════════
يعيد تصدير كل نماذج الـ Infrastructure في مكان واحد.
هذا يضمن أن أي كود يستورد من:
    from systems.services.infrastructure.models import StatusChangeForm
أو من:
    from systems.services.models import StatusChangeForm
سيجد نفس الكلاس بدون أي تغيير.
"""
from .event_log    import ServiceEventLog
from .staging      import StagingRecord
from .reconciliation import ReconciliationTask
from .snapshots    import MonthlySnapshot, DirectorateCompliance
from .logs         import ExportLog, RejectionLog
from .webhooks     import WebhookConfig
from .templates    import ReportTemplate, CustomFormTemplate, CustomReportTemplate
from .status_change import StatusChangeForm
from .disciplinary import DisciplinaryAction, AbsenceRecord, DisciplinaryCouncilVerdict


__all__ = [
    # Event
    'ServiceEventLog',
    # Staging
    'StagingRecord',
    # Reconciliation
    'ReconciliationTask',
    # Snapshots
    'MonthlySnapshot',
    'DirectorateCompliance',
    # Logs
    'ExportLog',
    'RejectionLog',
    # Webhooks
    'WebhookConfig',
    # Templates
    'ReportTemplate',
    'CustomFormTemplate',
    'CustomReportTemplate',
    # Forms
    'StatusChangeForm',
    # Disciplinary
    'DisciplinaryAction',
    'AbsenceRecord',
    'DisciplinaryCouncilVerdict',
]

