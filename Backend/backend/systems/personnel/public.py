"""
systems/personnel/public.py
═════════════════════════════
🔒 الواجهة العامة لنظام الأفراد — Public API

القاعدة الصارمة:
    ✅ مسموح:  from systems.personnel.public import ...
    ❌ ممنوع:  from systems.personnel.models import ...
    ❌ ممنوع:  from systems.personnel.services import ...

الأنظمة التي تستخدم هذه الواجهة:
    - systems.services   ← يستورد PersonnelMaster للاستمارات
    - systems.secretariat ← عند بناؤه
    - systems.information ← عند بناؤه
"""

# ── النموذج الأساسي للفرد ─────────────────────────────────────────────────
from systems.personnel.models import PersonnelMaster  # noqa: F401

# ── استعلامات مفيدة للأنظمة الأخرى ────────────────────────────────────────


def get_personnel_by_military_number(military_number: str):
    """
    جلب سجل فرد بالرقم العسكري.
    يُستخدم من: نظام الخدمات عند إنشاء الاستمارات.
    """
    try:
        return PersonnelMaster.objects.get(military_number=military_number)
    except PersonnelMaster.DoesNotExist:
        return None


def get_personnel_by_admin(security_admin_id: int, active_only: bool = True):
    """
    جلب قائمة الأفراد لإدارة أمن معينة.
    يُستخدم من: نظام الخدمات للكشوفات الشهرية.
    """
    qs = PersonnelMaster.objects.filter(security_admin_id=security_admin_id)
    if active_only:
        qs = qs.filter(is_active=True)
    return qs


def get_personnel_count_by_admin(security_admin_id: int) -> int:
    """
    عدد الأفراد في إدارة أمن.
    يُستخدم للإحصاءات والتقارير.
    """
    return PersonnelMaster.objects.filter(
        security_admin_id=security_admin_id,
        is_active=True,
    ).count()


__all__ = [
    'PersonnelMaster',
    'get_personnel_by_military_number',
    'get_personnel_by_admin',
    'get_personnel_count_by_admin',
]
