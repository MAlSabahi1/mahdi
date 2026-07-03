"""
Core Audit Models — DEPRECATED
════════════════════════════════
⚠️  Audit models moved to dedicated audit app.
    Use: from infra.audit.models import AuditLog, LoginAuditLog
    
    This file provides lazy re-exports for backward compatibility.
    Direct imports avoided to prevent circular dependency.
"""


def __getattr__(name):
    _names = {'AuditLog', 'LoginAuditLog'}
    if name in _names:
        from infra.audit import models as audit_models
        return getattr(audit_models, name)
    raise AttributeError(f"module 'core.models.audit' has no attribute {name!r}")
