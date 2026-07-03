"""
═══════════════════════════════════════════════════════
Services Registries — نقطة الاستيراد الموحدة
═══════════════════════════════════════════════════════

الاستخدام:
    from systems.services.registries import FormRegistry, ReportRegistry
"""
from .form_registry import FormRegistry, FormDefinition, FormField, AttachmentSpec
from .report_registry import ReportRegistry, ReportDefinition, ReportColumn

__all__ = [
    'FormRegistry', 'FormDefinition', 'FormField', 'AttachmentSpec',
    'ReportRegistry', 'ReportDefinition', 'ReportColumn',
]
