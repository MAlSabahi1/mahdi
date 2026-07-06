# """
# خيارات الحقول للخدمات الديناميكية
# Dynamic Service System Choice Classes
# """
# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class BaseIntegerChoices(models.IntegerChoices):
#     """Base class for integer choices with helper methods"""
#     @classmethod
#     def get_value(cls, label):
#         for item in cls.choices:
#             if item[1] == label:
#                 return item[0]
#         return None


# class BaseTextChoices(models.TextChoices):
#     """Base class for text choices with helper methods"""
#     @classmethod
#     def get_value(cls, label):
#         for item in cls.choices:
#             if item[1] == label:
#                 return item[0]
#         return None


# # ========================================
# # فئات الخدمة - Service Categories
# # ========================================
# class ServiceCategoryChoice(BaseTextChoices):
#     """فئات الخدمة"""
#     TUITION = 'tuition', _('رسوم دراسية')
#     ACADEMIC = 'academic', _('أكاديمية')
#     FINANCIAL = 'financial', _('مالية')
#     ADMINISTRATIVE = 'administrative', _('إدارية')
#     HOUSING = 'housing', _('سكن')
#     TRANSPORT = 'transport', _('نقل')
#     HEALTH = 'health', _('صحية')
#     OTHER = 'other', _('أخرى')


# # ========================================
# # حالات الطلب - Request Status
# # ========================================
# class ServiceStatusChoice(BaseTextChoices):
#     """حالات طلب الخدمة"""
#     PENDING = 'pending', _('قيد الانتظار')
#     APPROVED = 'approved', _('تمت الموافقة')
#     IN_PROGRESS = 'in_progress', _('قيد التنفيذ')
#     COMPLETED = 'completed', _('مكتمل')
#     REJECTED = 'rejected', _('مرفوض')
#     CANCELLED = 'cancelled', _('ملغى')


# # ========================================
# # حالات الدفع - Payment Status
# # ========================================
# class PaymentStatusChoice(BaseTextChoices):
#     """حالات الدفع"""
#     FREE = 'free', _('مجاني')
#     UNPAID = 'unpaid', _('غير مدفوع')
#     PAID = 'paid', _('مدفوع')
#     PARTIAL = 'partial', _('مدفوع جزئياً')
#     PAID_BY_GRANT = 'paid_by_grant', _('مدفوع منحه')
#     PAID_BY_DISCOUNT = 'paid_by_discount', _('مدفوع خصم')
#     PAID_BY_GRANT_DISCOUNT = 'paid_by_grant_discount', _('مدفوع منحة و خصم')
#     PARTIAL_GRANT = 'partial_grant', _('مدفوع جزئي منحة')
#     PARTIAL_DISCOUNT = 'partial_discount', _('مدفوع جزئي خصم')
#     PARTIAL_GRANT_DISCOUNT = 'partial_grant_discount', _('مدفوع جزئي منحة و خصم')

# class DueStatusChoice(BaseTextChoices):
#     """حالات الاستحقاق"""
#     UPCOMING = 'upcoming', _('قادم')
#     DUE = 'due', _('مستحق')
#     OVERDUE = 'overdue', _('متأخر')


# class PaymentTypeChoice(BaseTextChoices):
#     """أنواع الدفع"""
#     CASH = 'cash', _('نقداً')
#     BANK = 'bank', _('تحويل بنكي')
#     CHECK = 'check', _('شيك')
#     CARD = 'card', _('بطاقة ائتمان')
#     OTHER = 'other', _('أخرى')


# # ========================================
# # أنواع الجهات المانحة - Grant Source Types
# # ========================================
# class GrantSourceTypeChoice(BaseTextChoices):
#     """أنواع الجهات المانحة"""
#     DOMESTIC = 'domestic', _('داخليه')
#     GOVERNMENT = 'government', _('حكومية')
#     PRIVATE = 'private', _('خاصة')
#     INTERNATIONAL = 'international', _('دولية')
#     UNIVERSITY = 'university', _('جامعية')
#     CHARITY = 'charity', _('خيرية')
#     SCHOLARSHIP = 'scholarship', _('منحة دراسية')
#     OTHER = 'other', _('أخرى')


# # ========================================
# # مصدر الطلب - Request Source
# # ========================================
# class RequestSourceChoice(BaseTextChoices):
#     """مصدر الطلب"""
#     PLATFORM = 'platform', _('المنصة')
#     PORTAL = 'portal', _('البوابة')


# # ========================================
# # أولويات الطلب - Request Priority
# # ========================================
# class PriorityChoice(BaseTextChoices):
#     """أولويات الطلب"""
#     LOW = 'low', _('منخفضة')
#     NORMAL = 'normal', _('عادية')
#     HIGH = 'high', _('عالية')
#     URGENT = 'urgent', _('عاجلة')


# # ========================================
# # أنواع نموذج المخرج - Output Template Types
# # ========================================
# class OutputTemplateTypeChoice(BaseTextChoices):
#     """أنواع نموذج المخرج"""
#     STATEMENT_OF_GRADES_DOCUMENT = 'StatementOfGradesDocument', _('نموذج بيان درجات لغير الخرجين')
#     UNIVERSITY_INVOICE = 'UniversityInvoice', _('نموذج مصادقه الدفع(فاتوره)')
#     CLEARANCE_PREVIEW = 'ClearancePreview', _('استمارة المقاصه الداخليه')


# # ========================================
# # أنواع نموذج الاستماره - input Template Types
# # ========================================
# class InputTemplateTypeChoice(BaseTextChoices):
#     # STATUS_STATEMENT_DOCUMENT = 'StatusStatementDocunment',_("استماره بيان حالة")
#     STATEMENT_OF_GRADES_REQUEST_FORM = 'StatementOfGradesRequestForm', _('استمارة تقديم طلب بيان درجات لغير الخريجين')
#     POST_OFFICE_INVOICE = 'PostOfficeInvoice', _('استماره رقم الحافظة')
#     TRANSFER_FORM = 'TransferForm', _('استماره تقديم المقاصه الداخليه')


# # ========================================
# # فترة التقسيط - Installment Period
# # ========================================
# class InstallmentPeriodChoice(BaseTextChoices):
#     """فترة التقسيط"""
#     MONTHLY = 'monthly', _('شهري')
#     QUARTERLY = 'quarterly', _('ربع سنوي')
#     SEMESTER = 'semester', _('فصلي')
#     YEARLY = 'yearly', _('سنوي')


# # ========================================
# # أنواع مراحل سير العمل - Workflow Stage Types
# # ========================================
# class WorkflowStageTypeChoice(BaseTextChoices):
#     """أنواع مراحل سير العمل"""
#     PAYMENT = 'payment', _('الدفع')
#     APPROVAL = 'approval', _('الموافقة')
#     REVIEW = 'review', _('المراجعة')
#     EXECUTION = 'execution', _('التنفيذ')
#     OUTPUT_PRINT = 'output_print', _('طباعة المخرج')
#     DELIVERY = 'delivery', _('التسليم')


# # ========================================
# # حالات الشروط المسبقة - Prerequisite Status
# # ========================================
# class PrerequisiteStatusChoice(BaseTextChoices):
#     """حالات الشروط المسبقة"""
#     MANDATORY = 'mandatory', _('إجباري')
#     PREFERRED = 'preferred', _('مفضل')


# # ========================================
# # حالات المرحلة - Stage Status
# # ========================================
# class StageStatusChoice(BaseTextChoices):
#     """حالات المرحلة"""
#     PENDING = 'pending', _('قيد الانتظار')
#     IN_PROGRESS = 'in_progress', _('قيد التنفيذ')
#     COMPLETED = 'completed', _('مكتمل')
#     REJECTED = 'rejected', _('مرفوض')
#     CANCELLED = 'cancelled', _('ملغي')
#     RETURNED = 'returned', _('مرجع')


# # ========================================
# # أسباب الإرجاع - Return Reasons
# # ========================================
# class ReturnReasonChoice(BaseTextChoices):
#     """أسباب الإرجاع"""
#     MISSING_ATTACHMENTS = 'missing_attachments', _('نقص المرفقات')
#     INCORRECT_DATA = 'incorrect_data', _('بيانات غير صحيحة')
#     INCOMPLETE_FORM = 'incomplete_form', _('نموذج غير مكتمل')
#     OTHER = 'other', _('أخرى')


# # ========================================
# # أنواع المكونات - Component Types
# # ========================================
# class ComponentTypeChoice(BaseTextChoices):
#     WIZARD = 'wizard', _('تابات - (Wizard)')
#     FORM = 'form', _('نموذج - (Form)')


# class BaseComponentChoice(BaseTextChoices):
#     BASE_COMPONENT =  "base_component",_("الكمبوننت الرئيسي")
    

# class TargetAudienceComponentChoice(BaseTextChoices):
#     STUDENT_STATUS_CERTIFICATE = ("enrolled_student_component", _("طلب بيان حالة"))
#     INTERNAL_TRANSFER = ("internal_transfer_component", _("مقاصصة داخلية"))

# # ========================================
# # إجراءات السجل - Log Actions
# # ========================================
# class LogActionChoice(BaseTextChoices):
#     """إجراءات السجل"""
#     VIEW = 'view', _('العرض')
#     CREATE = 'create', _('إنشاء')
#     UPDATE = 'update', _('تحديث')
#     DELETE = 'delete', _('حذف')
#     RESTORE = 'restore', _('استرجاع')
#     ACTIVATE = 'activate', _('تفعيل')
#     DEACTIVATE = 'deactivate', _('تعطيل')
#     APPROVE = 'approve', _('موافقة')
#     REJECT = 'reject', _('رفض')
#     MOVE = 'move', _('نقل')
#     RETURN = 'return', _('إرجاع')
#     # إجراءات جديدة للسجلات
#     START = 'start', _('بدء')
#     COMPLETE = 'complete', _('إكمال')
#     LOCK = 'lock', _('قفل')
#     UNLOCK = 'unlock', _('فتح')
#     CANCEL = 'cancel', _('إلغاء')
#     ASSIGN_GRANT = 'assign_grant', _('تعيين منحة')
#     APPROVE_GRANT = 'approve_grant', _('موافقة منحة')
#     REJECT_GRANT = 'reject_grant', _('رفض منحة')
#     CANCEL_GRANT = 'cancel_grant', _('إلغاء منحة')
#     ADD_DISCOUNT = 'add_discount', _('إضافة خصم')
#     APPROVE_DISCOUNT = 'approve_discount', _('موافقة خصم')
#     REJECT_DISCOUNT = 'reject_discount', _('رفض خصم')
#     CANCEL_DISCOUNT = 'cancel_discount', _('إلغاء خصم')
#     PERMISSION_CHANGE = 'permission_change', _('تغيير صلاحية')
#     EXECUTE = 'execute', _('تنفيذ')
#     UPLOAD = 'upload', _('رفع ملف')
#     NOTE_ADDED = 'note_added', _('إضافة ملاحظة')


# # ========================================
# # مستويات أهمية السجل - Log Severity
# # ========================================
# class LogSeverityChoice(BaseTextChoices):
#     """مستويات أهمية السجل"""
#     DEBUG = 'debug', _('تصحيح')
#     INFO = 'info', _('معلومات')
#     WARNING = 'warning', _('تحذير')
#     ERROR = 'error', _('خطأ')
#     CRITICAL = 'critical', _('حرج')


# # ========================================
# # حالات SLA - SLA Status
# # ========================================
# class SLAStatusChoice(BaseTextChoices):
#     """حالات SLA"""
#     ON_TIME = 'on_time', _('في الوقت')
#     AT_RISK = 'at_risk', _('معرض للخطر')
#     OVERDUE = 'overdue', _('متأخر')
#     NOT_APPLICABLE = 'na', _('غير متاح')


# # ========================================
# # أنواع الجمهور المستهدف - Target Audience Types
# # ========================================
# class TargetAudienceTypeChoice(BaseTextChoices):
#     """أنواع الجمهور المستهدف"""
#     STUDENT = 'student', _('طالب')
#     EMPLOYEE = 'employee', _('موظف')
#     FACULTY = 'faculty', _('هيئة تدريس')
#     GRADUATE = 'graduate', _('خريج')
#     EXTERNAL = 'external', _('خارجي')





# class ServicePermissionType(BaseTextChoices):
#     CREATE = 'CREATE', _('إنشاء')
#     START = 'START', _('بدء')
#     REJECT = 'REJECT', _('رفض')
#     CANCEL = 'CANCEL', _('إلغاء')
#     LOCK = 'LOCK', _('قفل')
#     UNLOCK = 'UNLOCK', _('فتح')
#     READ = 'READ', _('قراءة')
#     UPDATE = 'UPDATE', _('تعديل')
#     DELETE = 'DELETE', _('حذف')
#     PRINT = 'PRINT', _('طباعة')
#     COMPLETE = 'COMPLETE', _('تسليم')
#     ASSIGN_GRANT = 'ASSIGN_GRANT', _('تعيين منحة')
#     REJECT_GRANT = 'REJECT_GRANT', _('رفض منحة')
#     APPROVE_GRANT = 'APPROVE_GRANT', _('موافقة على منحة')
#     CANCEL_GRANT = 'CANCEL_GRANT', _('إلغاء منحة')
#     UPDATE_GRANT = 'UPDATE_GRANT', _('تعديل منحة')
#     ADD_DISCOUNT = 'ADD_DISCOUNT', _('إضافة خصم')
#     UPDATE_DISCOUNT = 'UPDATE_DISCOUNT', _('تعديل خصم')
#     REJECT_DISCOUNT = 'REJECT_DISCOUNT', _('رفض خصم')
#     APPROVE_DISCOUNT = 'APPROVE_DISCOUNT', _('موافقة على خصم')
#     CANCEL_DISCOUNT = 'CANCEL_DISCOUNT', _('إلغاء خصم')
#     # صلاحيات المستندات
#     GET_INPUT_DATA = 'GET_INPUT_DATA', _('جلب بيانات المدخل')
#     GET_OUTPUT_DATA = 'GET_OUTPUT_DATA', _('جلب بيانات المخرج')
#     UPLOAD_INPUT = 'UPLOAD_INPUT', _('رفع ملف المدخل')
#     UPLOAD_OUTPUT = 'UPLOAD_OUTPUT', _('رفع ملف المخرج')
#     DELETE_INPUT = 'DELETE_INPUT', _('حذف ملف المدخل')
#     DELETE_OUTPUT = 'DELETE_OUTPUT', _('حذف ملف المخرج')

# class ActionPermissionType(BaseTextChoices):
#     START = 'START', _('بدء')
#     APPROVE = 'APPROVE', _('موافقة')
#     EXECUTE = 'EXECUTE', _('تنفيذ')
#     INPUT = 'INPUT', _('طباعه ورفع الاستمارة')
#     OUTPUT = 'OUTPUT', _('طباعه ورفع المخرج')
#     REJECT = 'REJECT', _('رفض')
#     CANCEL = 'CANCEL', _('إلغاء')
#     COMPLETE = 'COMPLETE', _('تسليم')
#     CHECKLIST_ADD = 'CHECKLIST_ADD', _('إضافة عنصر للقائمة')
#     CHECKLIST_DELETE = 'CHECKLIST_DELETE', _('حذف عنصر من القائمة')
#     CHECKLIST_CHECK = 'CHECKLIST_CHECK', _('تحقق من عنصر')
#     CHECKLIST_UNCHECK = 'CHECKLIST_UNCHECK', _('إلغاء تحقق من عنصر')


# class GrantStatusChoice(BaseTextChoices):
#     """حالات المنحة"""
#     NO_GRANT = 'no_grant', _('لا يوجد منحة')
#     PENDING = 'pending', _('قيد الانتظار')
#     APPROVED = 'approved', _('مقبول')
#     REJECTED = 'rejected', _('مرفوض')
#     CANCELLED = 'cancelled', _('ملغي')

# class DiscountStatusChoice(BaseTextChoices):
#     """حالات الخصم"""
#     NO_DISCOUNT = 'no_discount', _('لا يوجد خصم')
#     PENDING = 'pending', _('قيد الانتظار')
#     APPROVED = 'approved', _('مقبول')
#     REJECTED = 'rejected', _('مرفوض')
#     CANCELLED = 'cancelled', _('ملغي')


# ###############################
# ### قوائم بيانات الاصدارات ###
# ###############################

# class PurposeChoice(BaseTextChoices):
#     """الغرض من البيان"""
#     Employment = 'employment', _('توظيف')
#     Military = 'military', _('التجنيد')
#     Embassy = 'embassy', _('سفارة')
#     ForeignAffairs = 'foreign_affairs', _('وزارة الخارجية')
#     Bank = 'bank', _('بنك')
#     Other = 'other', _('أخرى')

# class LanguageChoice(BaseTextChoices):
#     """لغة البيان"""
#     Arabic = 'ar',_('عربي')
#     English = 'en',_('إنجليزي')
#     Both = 'both',_('الاثنين معاً')



"""
خيارات الحقول للخدمات الديناميكية
Dynamic Service System Choice Classes
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseIntegerChoices(models.IntegerChoices):
    """Base class for integer choices with helper methods"""
    @classmethod
    def get_value(cls, label):
        for item in cls.choices:
            if item[1] == label:
                return item[0]
        return None


class BaseTextChoices(models.TextChoices):
    """Base class for text choices with helper methods"""
    @classmethod
    def get_value(cls, label):
        for item in cls.choices:
            if item[1] == label:
                return item[0]
        return None


# ========================================
# فئات الخدمة - Service Categories
# ========================================
class ServiceCategoryChoice(BaseTextChoices):
    """فئات الخدمة"""
    TUITION = 'tuition', _('رسوم دراسية')
    ACADEMIC = 'academic', _('أكاديمية')
    FINANCIAL = 'financial', _('مالية')
    ADMINISTRATIVE = 'administrative', _('إدارية')
    HOUSING = 'housing', _('سكن')
    TRANSPORT = 'transport', _('نقل')
    HEALTH = 'health', _('صحية')
    OTHER = 'other', _('أخرى')
    REGISTER_STUDENT = 'register_student', _("تسجيل طالب")
    COORDINATION_AND_ADMISSION = "coordinition_and_admission", _("التنسيق و القبول")

# ========================================
# حالات الطلب - Request Status
# ========================================
class ServiceStatusChoice(BaseTextChoices):
    """حالات طلب الخدمة"""
    PENDING = 'pending', _('قيد الانتظار')
    APPROVED = 'approved', _('تمت الموافقة')
    IN_PROGRESS = 'in_progress', _('قيد التنفيذ')
    COMPLETED = 'completed', _('مكتمل')
    REJECTED = 'rejected', _('مرفوض')
    CANCELLED = 'cancelled', _('ملغى')


# ========================================
# حالات الدفع - Payment Status
# ========================================
class PaymentStatusChoice(BaseTextChoices):
    """حالات الدفع"""
    FREE = 'free', _('مجاني')
    UNPAID = 'unpaid', _('غير مدفوع')
    PAID = 'paid', _('مدفوع')
    PARTIAL = 'partial', _('مدفوع جزئياً')
    PAID_BY_GRANT = 'paid_by_grant', _('مدفوع منحه')
    PAID_BY_DISCOUNT = 'paid_by_discount', _('مدفوع خصم')
    PAID_BY_GRANT_DISCOUNT = 'paid_by_grant_discount', _('مدفوع منحة و خصم')
    PARTIAL_GRANT = 'partial_grant', _('مدفوع جزئي منحة')
    PARTIAL_DISCOUNT = 'partial_discount', _('مدفوع جزئي خصم')
    PARTIAL_GRANT_DISCOUNT = 'partial_grant_discount', _('مدفوع جزئي منحة و خصم')

class DueStatusChoice(BaseTextChoices):
    """حالات الاستحقاق"""
    UPCOMING = 'upcoming', _('قادم')
    DUE = 'due', _('مستحق')
    OVERDUE = 'overdue', _('متأخر')


class PaymentTypeChoice(BaseTextChoices):
    """أنواع الدفع"""
    CASH = 'cash', _('نقداً')
    BANK = 'bank', _('تحويل بنكي')
    CHECK = 'check', _('شيك')
    CARD = 'card', _('بطاقة ائتمان')
    OTHER = 'other', _('أخرى')


# ========================================
# أنواع الجهات المانحة - Grant Source Types
# ========================================
class GrantSourceTypeChoice(BaseTextChoices):
    """أنواع الجهات المانحة"""
    DOMESTIC = 'domestic', _('داخليه')
    GOVERNMENT = 'government', _('حكومية')
    PRIVATE = 'private', _('خاصة')
    INTERNATIONAL = 'international', _('دولية')
    UNIVERSITY = 'university', _('جامعية')
    CHARITY = 'charity', _('خيرية')
    SCHOLARSHIP = 'scholarship', _('منحة دراسية')
    OTHER = 'other', _('أخرى')


# ========================================
# مصدر الطلب - Request Source
# ========================================
class RequestSourceChoice(BaseTextChoices):
    """مصدر الطلب"""
    PLATFORM = 'platform', _('المنصة')
    PORTAL = 'portal', _('البوابة')


# ========================================
# أولويات الطلب - Request Priority
# ========================================
class PriorityChoice(BaseTextChoices):
    """أولويات الطلب"""
    LOW = 'low', _('منخفضة')
    NORMAL = 'normal', _('عادية')
    HIGH = 'high', _('عالية')
    URGENT = 'urgent', _('عاجلة')


# ========================================
# أنواع نموذج المخرج - Output Template Types
# ========================================
class OutputTemplateTypeChoice(BaseTextChoices):
    """أنواع نموذج المخرج"""
    STATEMENT_OF_GRADES_DOCUMENT = 'StatementOfGradesDocument', _('نموذج بيان درجات لغير الخرجين')
    UNIVERSITY_INVOICE = 'UniversityInvoice', _('نموذج مصادقه الدفع(فاتوره)')
    INROLLMENT_CERTIFICATE_Document = 'InrollmentCertificateDocument', _('وثيقة شهادة قيد دراسي')

    INTERNAL_CLEARANCE_DOCUMENT = 'InternalClearanceDocument', _('وثيقة المقاصه الداخليه')
    SUSPENSION_INROLLMENT_DOCUMENT = 'SuspensionInrollmentDocument', _('وثيقة وقف قيد')
    UN_SUSPENSION_INROLLMENT_DOCUMENT = 'UnSuspensionInrollmentDocument', _('وثيقة الغاء وقف قيد ')
    STUDENT_WITHDRAWAL_DOCUMENT = 'StudentWithdrawalDocument', _('وثيقة سحب ملف ')
    RETAKE_SUBJECT_DOCUMENT = 'RetakeSubjectDocument', _('وثيقة إعادة مادة ')
    ATTENDANCE_EXEMPTION_DOCUMENT = 'AttendanceExemptionDocument', _('وثيقة اعفاء حظور ')
    CLEARANCE_DOCUMENT = 'ClearanceDocument', _('وثيقة اخلاء طرف ')
    GRIEVANCE_COURSE_GRADE_DOCUMENT = 'GrievanceCourseGradeDocument', _('وثيقة تظلم على نتيجة مقرر ')
    HOUSING_DOCUMENT = 'HousingDocument', _('وثيقة طلب سكن ')
    REPLACEMENT_ID_CARD_DOCUMENT = 'ReplacementIDCardDocument', _('وثيقة قطع بطاقة بدل فاقد ')
    EXCUSED_ABSENCE_DOCUMENT = 'ExcusedAbsenceDocument', _('وثيقة غياب بعذر (امتحان) ')



# ========================================
# أنواع نموذج الاستماره - input Template Types
# ========================================
class InputTemplateTypeChoice(BaseTextChoices):
    # STATUS_STATEMENT_DOCUMENT = 'StatusStatementDocunment',_("استماره بيان حالة")
    STATEMENT_OF_GRADES_REQUEST_FORM = 'StatementOfGradesRequestForm', _('استمارة تقديم طلب بيان درجات لغير الخريجين')
    POST_OFFICE_INVOICE = 'PostOfficeInvoice', _('استماره رقم الحافظة')
    INROLLMENT_CERTIFICATE_REQUEST_FORM = 'InrollmentCertificateRequestForm', _('استماره شهادة قيد دراسي')
    INTERNAL_CLEARANCE_REQUEST_FORM = 'InternalClearanceRequestForm', _('استماره تقديم المقاصه الداخليه')
    SUSPENSION_INROLLMENT_REQUEST_FORM = 'SuspensionInrollmentRequestForm', _('استماره وقف قيد ')
    UN_SUSPENSION_INROLLMENT_REQUEST_FORM = 'UnSuspensionInrollmentRequestForm', _('استماره الغاء وقف قيد ')
    STUDENT_WITHDRAWAL_REQUEST_FORM = 'StudentWithdrawalRequestForm', _('استماره سحب ملف ')
    RETAKE_SUBJECT_REQUEST_FORM = 'RetakeSubjectRequestForm', _('استماره إعادة مادة ')
    ATTENDANCE_EXEMPTION_REQUEST_FORM = 'AttendanceExemptionRequestForm', _('استماره اعفاء حظور ')
    CLEARANCE_REQUEST_FORM = 'ClearanceRequestForm', _('استماره اخلاء طرف ')
    GRIEVANCE_COURSE_GRADE_REQUEST_FORM = 'GrievanceCourseGradeRequestForm', _('استماره تظلم على نتيجة مقرر ')
    HOUSING_REQUEST_FORM = 'HousingRequestForm', _('استماره طلب سكن ')
    REPLACEMENT_ID_CARD_REQUEST_FORM = 'ReplacementIDCardRequestForm', _('استماره قطع بطاقة بدل فاقد ')
    EXCUSED_ABSENCE_RequestForm = 'ExcusedAbsenceRequestForm', _('استمارة غياب بعذر (امتحان) ')


# ========================================
# فترة التقسيط - Installment Period
# ========================================
class InstallmentPeriodChoice(BaseTextChoices):
    """فترة التقسيط"""
    MONTHLY = 'monthly', _('شهري')
    QUARTERLY = 'quarterly', _('ربع سنوي')
    SEMESTER = 'semester', _('فصلي')
    YEARLY = 'yearly', _('سنوي')


# ========================================
# أنواع مراحل سير العمل - Workflow Stage Types
# ========================================
class WorkflowStageTypeChoice(BaseTextChoices):
    """أنواع مراحل سير العمل"""
    PAYMENT = 'payment', _('الدفع')
    APPROVAL = 'approval', _('الموافقة')
    REVIEW = 'review', _('المراجعة')
    EXECUTION = 'execution', _('التنفيذ')
    OUTPUT_PRINT = 'output_print', _('طباعة المخرج')
    DELIVERY = 'delivery', _('التسليم')


# ========================================
# حالات الشروط المسبقة - Prerequisite Status
# ========================================
class PrerequisiteStatusChoice(BaseTextChoices):
    """حالات الشروط المسبقة"""
    MANDATORY = 'mandatory', _('إجباري')
    PREFERRED = 'preferred', _('مفضل')


# ========================================
# حالات المرحلة - Stage Status
# ========================================
class StageStatusChoice(BaseTextChoices):
    """حالات المرحلة"""
    PENDING = 'pending', _('قيد الانتظار')
    IN_PROGRESS = 'in_progress', _('قيد التنفيذ')
    COMPLETED = 'completed', _('مكتمل')
    REJECTED = 'rejected', _('مرفوض')
    CANCELLED = 'cancelled', _('ملغي')
    RETURNED = 'returned', _('مرجع')


# ========================================
# أسباب الإرجاع - Return Reasons
# ========================================
class ReturnReasonChoice(BaseTextChoices):
    """أسباب الإرجاع"""
    MISSING_ATTACHMENTS = 'missing_attachments', _('نقص المرفقات')
    INCORRECT_DATA = 'incorrect_data', _('بيانات غير صحيحة')
    INCOMPLETE_FORM = 'incomplete_form', _('نموذج غير مكتمل')
    OTHER = 'other', _('أخرى')


# ========================================
# أنواع المكونات - Component Types
# ========================================
class ComponentTypeChoice(BaseTextChoices):
    WIZARD = 'wizard', _('تابات - (Wizard)')
    FORM = 'form', _('نموذج - (Form)')


class BaseComponentChoice(BaseTextChoices):
    BASE_COMPONENT =  "base_component",_("الكمبوننت الرئيسي")
    

class TargetAudienceComponentChoice(BaseTextChoices):
    STUDENT_STATUS_CERTIFICATE = ("enrolled_student_component", _("طلب بيان حالة"))
    INTERNAL_TRANSFER = ("internal_transfer_component", _("مقاصصة داخلية"))
    INROLLMENT_CERTIFICATE = ("inrollment_certificate_component",_("شهادة القيد الدراسي"))
    SUSPENSION_INROLLMENT = ("suspension_inrollment_component", _("وقف قيد"))
    STUDENT_WITHDRAWAL = ("student_withdrawal_component", _("سحب ملف"))
    RETAKE_SUBJECT = ("retake_subject_component", _(" إعادة مادة"))
    GRIEVANCE_COURSE_GRADE = ("grievance_course_grade_component",_("تظلم على نتيجة مقرر"))
    ATTENDANCE_EXEMPTION = ("attendance_exemption_component",_("اعفاء حظور"))
    CLEARANCE = ("clearance_component",_("اخلاء طرف"))
    REPLACEMENT_ID_CARD = ("replacement_id_card_component",_("قطع بطاقة بدل فاقد"))
    HOUSING = ("housing_component",_("طلب سكن"))
    EXCUSED_ABSENCE = ("excused_absence_component", _("غياب بعذر"))

# ========================================
# إجراءات السجل - Log Actions
# ========================================
class LogActionChoice(BaseTextChoices):
    """إجراءات السجل"""
    VIEW = 'view', _('العرض')
    CREATE = 'create', _('إنشاء')
    UPDATE = 'update', _('تحديث')
    DELETE = 'delete', _('حذف')
    RESTORE = 'restore', _('استرجاع')
    ACTIVATE = 'activate', _('تفعيل')
    DEACTIVATE = 'deactivate', _('تعطيل')
    APPROVE = 'approve', _('موافقة')
    REJECT = 'reject', _('رفض')
    MOVE = 'move', _('نقل')
    RETURN = 'return', _('إرجاع')
    # إجراءات جديدة للسجلات
    START = 'start', _('بدء')
    COMPLETE = 'complete', _('إكمال')
    LOCK = 'lock', _('قفل')
    UNLOCK = 'unlock', _('فتح')
    CANCEL = 'cancel', _('إلغاء')
    ASSIGN_GRANT = 'assign_grant', _('تعيين منحة')
    APPROVE_GRANT = 'approve_grant', _('موافقة منحة')
    REJECT_GRANT = 'reject_grant', _('رفض منحة')
    CANCEL_GRANT = 'cancel_grant', _('إلغاء منحة')
    ADD_DISCOUNT = 'add_discount', _('إضافة خصم')
    APPROVE_DISCOUNT = 'approve_discount', _('موافقة خصم')
    REJECT_DISCOUNT = 'reject_discount', _('رفض خصم')
    CANCEL_DISCOUNT = 'cancel_discount', _('إلغاء خصم')
    PERMISSION_CHANGE = 'permission_change', _('تغيير صلاحية')
    EXECUTE = 'execute', _('تنفيذ')
    UPLOAD = 'upload', _('رفع ملف')
    NOTE_ADDED = 'note_added', _('إضافة ملاحظة')


# ========================================
# مستويات أهمية السجل - Log Severity
# ========================================
class LogSeverityChoice(BaseTextChoices):
    """مستويات أهمية السجل"""
    DEBUG = 'debug', _('تصحيح')
    INFO = 'info', _('معلومات')
    WARNING = 'warning', _('تحذير')
    ERROR = 'error', _('خطأ')
    CRITICAL = 'critical', _('حرج')


# ========================================
# حالات SLA - SLA Status
# ========================================
class SLAStatusChoice(BaseTextChoices):
    """حالات SLA"""
    ON_TIME = 'on_time', _('في الوقت')
    AT_RISK = 'at_risk', _('معرض للخطر')
    OVERDUE = 'overdue', _('متأخر')
    NOT_APPLICABLE = 'na', _('غير متاح')


# ========================================
# أنواع الجمهور المستهدف - Target Audience Types
# ========================================
class TargetAudienceTypeChoice(BaseTextChoices):
    """أنواع الجمهور المستهدف"""
    STUDENT = 'student', _('طالب')
    EMPLOYEE = 'employee', _('موظف')
    FACULTY = 'faculty', _('هيئة تدريس')
    GRADUATE = 'graduate', _('خريج')
    EXTERNAL = 'external', _('خارجي')





class ServicePermissionType(BaseTextChoices):
    CREATE = 'CREATE', _('إنشاء')
    START = 'START', _('بدء')
    REJECT = 'REJECT', _('رفض')
    CANCEL = 'CANCEL', _('إلغاء')
    LOCK = 'LOCK', _('قفل')
    UNLOCK = 'UNLOCK', _('فتح')
    READ = 'READ', _('قراءة')
    UPDATE = 'UPDATE', _('تعديل')
    DELETE = 'DELETE', _('حذف')
    PRINT = 'PRINT', _('طباعة')
    COMPLETE = 'COMPLETE', _('تسليم')
    ASSIGN_GRANT = 'ASSIGN_GRANT', _('تعيين منحة')
    REJECT_GRANT = 'REJECT_GRANT', _('رفض منحة')
    APPROVE_GRANT = 'APPROVE_GRANT', _('موافقة على منحة')
    CANCEL_GRANT = 'CANCEL_GRANT', _('إلغاء منحة')
    UPDATE_GRANT = 'UPDATE_GRANT', _('تعديل منحة')
    ADD_DISCOUNT = 'ADD_DISCOUNT', _('إضافة خصم')
    UPDATE_DISCOUNT = 'UPDATE_DISCOUNT', _('تعديل خصم')
    REJECT_DISCOUNT = 'REJECT_DISCOUNT', _('رفض خصم')
    APPROVE_DISCOUNT = 'APPROVE_DISCOUNT', _('موافقة على خصم')
    CANCEL_DISCOUNT = 'CANCEL_DISCOUNT', _('إلغاء خصم')
    # صلاحيات المستندات
    GET_INPUT_DATA = 'GET_INPUT_DATA', _('جلب بيانات المدخل')
    GET_OUTPUT_DATA = 'GET_OUTPUT_DATA', _('جلب بيانات المخرج')
    UPLOAD_INPUT = 'UPLOAD_INPUT', _('رفع ملف المدخل')
    UPLOAD_OUTPUT = 'UPLOAD_OUTPUT', _('رفع ملف المخرج')
    DELETE_INPUT = 'DELETE_INPUT', _('حذف ملف المدخل')
    DELETE_OUTPUT = 'DELETE_OUTPUT', _('حذف ملف المخرج')

class ActionPermissionType(BaseTextChoices):
    START = 'START', _('بدء')
    APPROVE = 'APPROVE', _('موافقة')
    EXECUTE = 'EXECUTE', _('تنفيذ')
    INPUT = 'INPUT', _('طباعه ورفع الاستمارة')
    OUTPUT = 'OUTPUT', _('طباعه ورفع المخرج')
    REJECT = 'REJECT', _('رفض')
    CANCEL = 'CANCEL', _('إلغاء')
    COMPLETE = 'COMPLETE', _('تسليم')
    CHECKLIST_ADD = 'CHECKLIST_ADD', _('إضافة عنصر للقائمة')
    CHECKLIST_DELETE = 'CHECKLIST_DELETE', _('حذف عنصر من القائمة')
    CHECKLIST_CHECK = 'CHECKLIST_CHECK', _('تحقق من عنصر')
    CHECKLIST_UNCHECK = 'CHECKLIST_UNCHECK', _('إلغاء تحقق من عنصر')


class GrantStatusChoice(BaseTextChoices):
    """حالات المنحة"""
    NO_GRANT = 'no_grant', _('لا يوجد منحة')
    PENDING = 'pending', _('قيد الانتظار')
    APPROVED = 'approved', _('مقبول')
    REJECTED = 'rejected', _('مرفوض')
    CANCELLED = 'cancelled', _('ملغي')

class DiscountStatusChoice(BaseTextChoices):
    """حالات الخصم"""
    NO_DISCOUNT = 'no_discount', _('لا يوجد خصم')
    PENDING = 'pending', _('قيد الانتظار')
    APPROVED = 'approved', _('مقبول')
    REJECTED = 'rejected', _('مرفوض')
    CANCELLED = 'cancelled', _('ملغي')


###############################
### قوائم بيانات الاصدارات ###
###############################

class PurposeChoice(BaseTextChoices):
    """الغرض من البيان"""
    Employment = 'employment', _('توظيف')
    Military = 'military', _('التجنيد')
    Embassy = 'embassy', _('سفارة')
    ForeignAffairs = 'foreign_affairs', _('وزارة الخارجية')
    Bank = 'bank', _('بنك')
    Other = 'other', _('أخرى')

class LanguageChoice(BaseTextChoices):
    """لغة البيان"""
    Arabic = 'ar',_('عربي')
    English = 'en',_('إنجليزي')
    Both = 'both',_('الاثنين معاً')


class ResolveByChoice(BaseTextChoices):
    """طرق تحويل حقول البوابة إلى حقول QAS"""
    EX_ID = 'ex_id', _('معرف خارجي UUID (ex_id)')
    CODE = 'code', _('كود (code)')
    DIRECT = 'direct', _('قيمة مباشرة (نفس الـ ID)')
    CUSTOM = 'custom_function', _('دالة مخصصة')
