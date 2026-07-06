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

from .form_notes import FormNote, FormEventLog, FormReturnLog, FormChecklist
from .service_catalog import ServiceCatalog, ServicePrerequisite, ChecklistTemplate
from .workflow import WorkflowStage, ServiceWorkflowStep

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
    # Services Catalog
    'FormNote', 
    'FormEventLog', 
    'FormReturnLog', 
    'FormChecklist',
    'ServiceCatalog', 
    'ServicePrerequisite', 
    'ChecklistTemplate',
    'WorkflowStage',
    'ServiceWorkflowStep',
]
