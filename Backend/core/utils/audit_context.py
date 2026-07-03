"""
Core Audit Context — DEPRECATED
════════════════════════════════════
⚠️  Moved to audit.utils.audit_context
"""
from infra.audit.utils.audit_context import (  # noqa: F401
    set_audit_context,
    get_audit_context,
    clear_audit_context,
)
