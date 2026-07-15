"""
Core Models Package — النواة المركزية
═══════════════════════════════════════
Single Source of Truth — كل شيء يُستورد من هنا.

الاستخدام:
    from core.models import Rank, ServiceStatus, SecurityAdministration
    from core.models import GeoGovernorate, GeoDistrict
    from infra.audit.models import AuditLog, LoginAuditLog         # ← تدقيق
    from infra.authorization.models import Permission, Role        # ← صلاحيات
"""

from .base import TimeStampedModel, SoftDeletableModel

# ── البيانات الجغرافية (yemen-info.json) ──
from .geography import (
    GeoGovernorate,
    GeoDistrict,
    GeoSubDistrict,
    GeoVillage,
)

# ── الهيكل التنظيمي الأمني ──
from .organization import (
    SecurityAdministration,
    CentralDepartment,
    Branch,
    DistrictPolice,
    Division,
    Unit,
)

# ── البيانات المرجعية ──
from .personnel_refs import (
    Rank,
    ServiceStatus,
    JobCategory,
    JobTitle,
    Qualification,
    Position,
    ForceType,
    VariableType,
)

# ── محرك الحالات ──
from .workflow import StateTransitionRule

# ── الإشعارات ──
from .notification import NotificationRecord

# ── إعدادات النظام ──
from .settings import SystemSetting


def __getattr__(name):
    """
    Lazy import للتوافق الخلفي.
    RBAC → authorization app.
    Audit → audit app.
    النماذج القديمة المحذوفة → تحذير واضح.
    """
    # النماذج القديمة المحذوفة
    _removed = {
        'Governorate': 'SecurityAdministration',
        'Directorate': 'CentralDepartment / Branch / DistrictPolice',
        'Location': 'GeoGovernorate / GeoDistrict',
    }
    if name in _removed:
        raise AttributeError(
            f"'core.models.{name}' has been removed. "
            f"Use '{_removed[name]}' instead."
        )

    # RBAC models → authorization
    _auth_names = {
        'Permission', 'Role', 'RolePermission', 'UserProfile', 'UserRole',
    }
    if name in _auth_names:
        import warnings
        warnings.warn(
            f"'core.models.{name}' moved to 'authorization.models.{name}'. "
            f"Update your import.",
            DeprecationWarning, stacklevel=2,
        )
        from infra.authorization import models as auth_models
        return getattr(auth_models, name)

    # Audit models → audit
    _audit_names = {'AuditLog', 'LoginAuditLog'}
    if name in _audit_names:
        import warnings
        warnings.warn(
            f"'core.models.{name}' moved to 'audit.models.{name}'. "
            f"Update your import.",
            DeprecationWarning, stacklevel=2,
        )
        from infra.audit import models as audit_models
        return getattr(audit_models, name)

    raise AttributeError(f"module 'core.models' has no attribute {name!r}")


__all__ = [
    # Base
    'TimeStampedModel', 'SoftDeletableModel',
    # Geography
    'GeoGovernorate', 'GeoDistrict', 'GeoSubDistrict', 'GeoVillage',
    # Security Organization
    'SecurityAdministration', 'CentralDepartment', 'Branch', 'DistrictPolice',
    'Division', 'Unit',
    # Personnel Refs
    'Rank', 'ServiceStatus', 'JobCategory', 'JobTitle', 'Qualification',
    'Position', 'ForceType', 'VariableType',
    # Workflow
    'StateTransitionRule',
    # Notifications
    'NotificationRecord',
    # Settings
    'SystemSetting',
]
