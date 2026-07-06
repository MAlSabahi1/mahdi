"""
External Methods - الدوال الخارجية المسموح بها
هذا الملف للتوافق العكسي فقط - الدوال موجودة في الملفات المنفصلة

الملفات الجديدة:
- validators.py: دوال التحقق من الشروط
- execution.py: دوال تنفيذ خطوات سير العمل
- output_data.py: دوال بيانات المخرجات
- input_data.py: دوال بيانات المدخلات
- requester.py: دوال معلومات مقدم الطلب
"""

# استيراد الدوال من الملفات الجديدة للتوافق العكسي
from d_services.apis.external_methods.validators import (
    validate_student_not_graduated_or_certified,
    check_student_is_in_first_level,
    validate_student_active,
    validate_student_enrolled,
    validate_no_pending_fees,
    validate_employee_active,
    brohome,
)

from d_services.apis.external_methods.execution import (
    execute_update_financial_status,
    execute_certificate_generation,
    execute_document_review,
    execute_approval_workflow,
)

from d_services.apis.external_methods.output_data import (
    get_statement_form_data,
    get_status_statement_data,
    academic_transcript_for_non_graduate_student,
    get_student_output_data,
    get_employee_output_data,
    get_request_summary_data,
)

from d_services.apis.external_methods.input_data import (
    brohme_input,
    get_student_input_data,
    get_employee_input_data,
)

from d_services.apis.external_methods.requester import (
    get_student_image_for_statement,
    get_student_info_for_statement,
    get_employee_image,
    get_user_avatar,
)

from d_services.apis.external_methods.erp_data import (
    call_get_erp_defaults,
)

# قائمة الدوال المتجاهلة (للتوافق مع الكود القديم)
ignore_func_list = [
    'Any', 'Dict', 'Optional', 'StudentLevel', 'StudentSemester', 'StudentSubject',
    'PaymentStatusChoice', 'StudentBatch', 'Sum', 'AcademicStatusChoice',
    'StudentStatusChoice', 'GenderChoice', 'logger', 'StudyTypeChoice',
]


