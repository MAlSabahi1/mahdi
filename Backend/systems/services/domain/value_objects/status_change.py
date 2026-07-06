"""
Domain Value Objects: Status Change
═════════════════════════════════════
قيم ثابتة لاستمارة إثبات الحالة.
Python نقي — لا Django.
"""
from enum import Enum


class FormStatus(str, Enum):
    """حالات الاستمارة — تعكس STATUS_CHOICES في النموذج الموجود"""
    DRAFT             = "draft"
    IN_PROGRESS       = "in_progress"
    APPROVED          = "approved"
    REJECTED          = "rejected"
    RETURNED          = "returned"


class FormType(str, Enum):
    """أنواع الاستمارة — تعكس FORM_TYPE_CHOICES الـ 11 في النموذج الموجود"""
    RETIREMENT_AGE = "retirement_age"
    DEATH          = "death"
    MISSING        = "missing"
    MEDICAL_UNFIT  = "medical_unfit"
    END_OF_SERVICE = "end_of_service"
    RETIRED        = "retired"
    IMPRISONED     = "imprisoned"
    ESCORT         = "escort"
    MARTYR         = "martyr"
    STUDY_LEAVE    = "study_leave"
    SECONDED       = "seconded"


class ApprovalLevel(int, Enum):
    """مستويات الاعتماد الثلاثة"""
    SERVICES = 1   # قسم الخدمات
    HR       = 2   # الموارد البشرية
    DIRECTOR = 3   # المدير العام


# الحالات التي يمكن رفضها
REJECTABLE_STATUSES = {
    FormStatus.IN_PROGRESS,
}
