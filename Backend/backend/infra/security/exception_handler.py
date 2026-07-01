"""
Security Exception Handler — DEPRECATED
════════════════════════════════════════════
⚠️  Global Exception Handler moved to core/exception_handler.py
    This file re-exports for backward compatibility only.
"""
import warnings

warnings.warn(
    "security.exception_handler is deprecated. "
    "Use core.exception_handler.global_exception_handler instead.",
    DeprecationWarning, stacklevel=2,
)

from core.exception_handler import global_exception_handler as custom_exception_handler  # noqa: F401
