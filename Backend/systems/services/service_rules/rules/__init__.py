"""rules package — تصدير القواعد للاستخدام في التسجيل المركزي."""
from systems.services.service_rules.rules.common import COMMON_RULES  # noqa: F401
from systems.services.service_rules.rules import martyr               # noqa: F401
from systems.services.service_rules.rules import imprisoned           # noqa: F401
from systems.services.service_rules.rules import end_of_service       # noqa: F401
from systems.services.service_rules.rules.medical_unfit import MEDICAL_UNFIT_FORM_RULES  # noqa: F401
