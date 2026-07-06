# import json
# import os
# import logging
# from typing import Any, Dict
# from decimal import Decimal
# from django.db import transaction
# from academic_affairs.models.Batch import Batch
# from academic_affairs.models.ClearingMaterials import ClearingMaterials
# from academic_affairs.models.Level import Level
# from academic_affairs.models.SemesterSubject import SemesterSubject
# from control.models.StudentsClearingMaterials import StudentsClearingMaterials
# from d_services.apis.external_methods.utils.helpers_methods import calculate_scaled_grade, find_equivalent_subject

# from d_services.choices.choices import PaymentStatusChoice, GrantStatusChoice, DiscountStatusChoice
# from student_affairs.models.Student import Student
# from student_affairs.models.StudentBatch import StudentBatch
# from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
# from system_management.choices.choices import AcademicStatusChoice, LevelStudentStatusChoice, ResultStatusChoice, SemesterStudentStatusChoice, StudentStatusChoice, StudentsClearingMaterialsChoice, SubjectStatusChoice
# from system_management.models.AcademicYear import AcademicYear

# logger = logging.getLogger(__name__)

# # مسار ملف البيانات المالية المؤقت
# MOCK_FINANCIAL_DATA_PATH = os.path.join(
#     os.path.dirname(__file__), 
#     'mock_financial_data.json'
# )


# def _load_financial_data() -> Dict[str, Any]:
#     """تحميل بيانات النظام المالي المؤقت من ملف JSON"""
#     try:
#         with open(MOCK_FINANCIAL_DATA_PATH, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         logger.warning(f"ملف البيانات المالية غير موجود: {MOCK_FINANCIAL_DATA_PATH}")
#         return {'payments': {}, 'grants': {}, 'discounts': {}}
#     except json.JSONDecodeError as e:
#         logger.error(f"خطأ في قراءة ملف البيانات المالية: {e}")
#         return {'payments': {}, 'grants': {}, 'discounts': {}}


# def _calculate_payment_status(
#     total_fee: Decimal,
#     amount_paid: Decimal,
#     remaining_amount: Decimal,
#     has_grant: bool,
#     is_full_grant: bool,
#     has_discount: bool,
#     is_full_discount: bool
# ) -> str:
#     """
#     حساب حالة الدفع بناءً على جميع الاحتمالات
#     """
#     # الخدمة مجانية
#     if total_fee <= 0:
#         return PaymentStatusChoice.FREE
    
#     # حساب نسبة المبلغ المدفوع
#     is_fully_paid = (remaining_amount <= 0 or amount_paid >= total_fee)
#     is_partially_paid = (amount_paid > 0 and remaining_amount > 0)
    
#     if is_fully_paid:
#         if has_grant and has_discount:
#             return PaymentStatusChoice.PAID_BY_GRANT_DISCOUNT
#         elif has_grant and is_full_grant:
#             return PaymentStatusChoice.PAID_BY_GRANT
#         elif has_discount and is_full_discount:
#             return PaymentStatusChoice.PAID_BY_DISCOUNT
#         else:
#             return PaymentStatusChoice.PAID
    
#     if is_partially_paid:
#         if has_grant and has_discount:
#             return PaymentStatusChoice.PARTIAL_GRANT_DISCOUNT
#         elif has_grant:
#             return PaymentStatusChoice.PARTIAL_GRANT
#         elif has_discount:
#             return PaymentStatusChoice.PARTIAL_DISCOUNT
#         else:
#             return PaymentStatusChoice.PARTIAL
    
#     return PaymentStatusChoice.UNPAID


# def call_execute_update_financial_status(action, request) -> Dict[str, Any]:
#     """
#     تحديث البيانات المالية للطلب من النظام المالي
#     """
#     service_request = action.fk_request
#     request_number = service_request.request_number
    
#     logger.info(f"تحديث البيانات المالية للطلب: {request_number}")
    
#     try:
#         financial_data = _load_financial_data()
#         updated_fields = []
        
#         # تحديث بيانات الدفع والأقساط
#         payment_data = financial_data.get('payments', {}).get(request_number)
#         if payment_data:
#             service_request.amount_paid = Decimal(str(payment_data.get('amount_paid', 0)))
#             service_request.remaining_amount = Decimal(str(payment_data.get('remaining_amount', 0)))
#             updated_fields.extend(['amount_paid', 'remaining_amount'])
            
#             if payment_data.get('has_installments'):
#                 installments = payment_data.get('installments', [])
#                 paid_count = sum(1 for inst in installments if inst.get('paid'))
#                 total_count = len(installments)
#                 logger.info(f"الأقساط: {paid_count}/{total_count} مدفوعة")
        
#         # تحديث بيانات المنحة
#         grant_data = financial_data.get('grants', {}).get(request_number)
#         has_grant = False
#         is_full_grant = False
        
#         if grant_data and grant_data.get('has_grant'):
#             grant_status_map = {
#                 'APPROVED': GrantStatusChoice.APPROVED,
#                 'PENDING': GrantStatusChoice.PENDING,
#                 'REJECTED': GrantStatusChoice.REJECTED,
#                 'NO_GRANT': GrantStatusChoice.NO_GRANT,
#             }
            
#             service_request.grant_status = grant_status_map.get(
#                 grant_data.get('grant_status'),
#                 GrantStatusChoice.NO_GRANT
#             )
#             service_request.grant_percentage = Decimal(str(grant_data.get('grant_percentage', 0)))
#             service_request.grant_amount = Decimal(str(grant_data.get('grant_amount', 0)))
            
#             updated_fields.extend(['grant_status', 'grant_percentage', 'grant_amount'])
            
#             if grant_data.get('grant_status') == 'APPROVED':
#                 has_grant = True
#                 grant_type = grant_data.get('grant_type')
#                 is_full_grant = (grant_type == 'FULL' or service_request.grant_percentage >= 100)
        
#         # تحديث بيانات الخصم
#         discount_data = financial_data.get('discounts', {}).get(request_number)
#         has_discount = False
#         is_full_discount = False
        
#         if discount_data and discount_data.get('has_discount'):
#             discount_status_map = {
#                 'APPROVED': DiscountStatusChoice.APPROVED,
#                 'PENDING': DiscountStatusChoice.PENDING,
#                 'REJECTED': DiscountStatusChoice.REJECTED,
#                 'NO_DISCOUNT': DiscountStatusChoice.NO_DISCOUNT,
#             }
            
#             service_request.discount_status = discount_status_map.get(
#                 discount_data.get('discount_status'),
#                 DiscountStatusChoice.NO_DISCOUNT
#             )
#             service_request.discount_amount = Decimal(str(discount_data.get('discount_amount', 0)))
            
#             if discount_data.get('discount_reason'):
#                 service_request.discount_reason = discount_data.get('discount_reason')
            
#             updated_fields.extend(['discount_status', 'discount_amount', 'discount_reason'])
            
#             if discount_data.get('discount_status') == 'APPROVED':
#                 has_discount = True
#                 is_full_discount = (service_request.discount_amount >= service_request.total_fee)
        
#         # تحديد حالة الدفع النهائية
#         payment_status = _calculate_payment_status(
#             total_fee=service_request.total_fee,
#             amount_paid=service_request.amount_paid,
#             remaining_amount=service_request.remaining_amount,
#             has_grant=has_grant,
#             is_full_grant=is_full_grant,
#             has_discount=has_discount,
#             is_full_discount=is_full_discount
#         )
        
#         service_request.payment_status = payment_status
#         updated_fields.append('payment_status')
        
#         if updated_fields:
#             service_request.save(update_fields=updated_fields)
#             logger.info(f"تم تحديث الحقول: {updated_fields}")
        
#         return {
#             'success': True,
#             'message': 'تم تحديث البيانات المالية بنجاح',
#             'data': {
#                 'request_number': request_number,
#                 'updated_fields': updated_fields,
#                 'payment_status': service_request.payment_status,
#             }
#         }
        
#     except Exception as e:
#         logger.error(f"خطأ في تحديث البيانات المالية: {e}")
#         return {
#             'success': False,
#             'message': f'حدث خطأ أثناء تحديث البيانات المالية: {str(e)}',
#             'data': {}
#         }


# def call_perform_internal_clearance(action, request):
#     """دالة تنفيذ المقاصه الداخلية"""
#     """
#     تنفيذ المقاصة فعليًا:
#     - نقل الطالب للتخصص الجديد
#     - تطبيق المقاصة على المواد الناجحة
#     - إضافة المواد المعفاة
#     - تحديث الحالة الأكاديمية والمستوى الحالي
#     """
#     student_id, new_specialization_id, exempted_subject_ids=None
#     exempted_subject_ids = exempted_subject_ids or []
#     try:
#         with transaction.atomic():  # ضمان atomicity للمعاملة كاملة
#             student = Student.objects.select_for_update().get(pk=student_id)
#             new_batch = Batch.objects.filter(fk_specialization_id=new_specialization_id).order_by('-id').first()
#             if not new_batch: 
#                 return {'success': False, 'error': 'لا توجد دفعات للتخصص الجديد'}

#             new_specialization = new_batch.fk_specialization
            
#             old_sb = StudentBatch.objects.filter(fk_student=student, is_current=True).first() \
#                         or StudentBatch.objects.filter(fk_student=student).order_by('-id').first()
#             academic_year = AcademicYear.objects.filter(is_cournt=True).first() \
#                             or AcademicYear.objects.order_by('-id').first()

#             # تجهيز قاموس البحث للمواد الجديدة
#             new_subs = SemesterSubject.objects.filter(
#                 fk_semester__fk_level__fk_batch=new_batch
#             ).select_related('fk_subject', 'fk_grading_system_june')
#             subs_by_code = {s.fk_subject.subject_code.strip().lower(): s for s in new_subs if s.fk_subject.subject_code}
#             subs_by_name = {}
#             for s in new_subs:
#                 if s.fk_subject.name_ar: subs_by_name[s.fk_subject.name_ar.strip().lower()] = s
#                 if s.fk_subject.name_en: subs_by_name[s.fk_subject.name_en.strip().lower()] = s

#             # ==========================
#             # مطابقة المواد القديمة مع الجديدة
#             # ==========================
#             cleared_subjects = []  # قائمة المواد المقاصة [(old_rec, target_ss, grade)]
#             used_targets = set()
            
#             old_subjects = StudentSubject.objects.filter(
#                 fk_student_semester__fk_student_level__fk_student_batch__fk_student=student,
#                 results_status__in=[ResultStatusChoice.PASSED, ResultStatusChoice.CLEARANCE]
#             ).select_related('fk_semmester_subject__fk_subject', 'fk_semmester_subject__fk_grading_system_june')

#             for old_rec in old_subjects:
#                 old_ss = old_rec.fk_semmester_subject
#                 # البحث عن المقاصة الرسمية
#                 rule = ClearingMaterials.objects.filter(
#                     fk_semester_subject_from=old_ss, 
#                     active=True, 
#                     fk_semester_subject_to__fk_semester__fk_level__fk_batch=new_batch
#                 ).select_related('fk_semester_subject_to__fk_grading_system_june').first()
#                 target = rule.fk_semester_subject_to if rule else find_equivalent_subject(old_ss.fk_subject, subs_by_code, subs_by_name)

#                 if target and target.id not in used_targets:
#                     used_targets.add(target.id)
#                     grade = calculate_scaled_grade(
#                         old_rec.total_grade, 
#                         old_ss.fk_grading_system_june.grade_total, 
#                         target.fk_grading_system_june.grade_total
#                     )
#                     cleared_subjects.append((old_rec, target, grade))

#             # ==========================
#             # إضافة المواد المعفاة
#             # ==========================
#             for sid in exempted_subject_ids:
#                 if sid not in used_targets:
#                     if target := next((s for s in new_subs if s.id == sid), None):
#                         used_targets.add(target.id)
#                         cleared_subjects.append((None, target, 0))

#             # ==========================
#             # تحديد حالة كل مستوى
#             # ==========================
#             levels = Level.objects.filter(fk_batch=new_batch).order_by('level')
#             level_status = {}
#             current_level = None
            
#             # Pre-calculate cleared counts per level
#             cleared_by_level = {l.id: [c for c in cleared_subjects if c[1].fk_semester.fk_level_id == l.id] for l in levels}
            
#             for level in levels:
#                 total_subs = SemesterSubject.objects.filter(fk_semester__fk_level=level).count()
#                 cleared_count = len(cleared_by_level[level.id])
#                 remaining = total_subs - cleared_count
                
#                 has_higher_clearance = any(len(cleared_by_level[l.id]) > 0 for l in levels if l.level > level.level)
                
#                 if remaining > level.allowed_failure_subjects and has_higher_clearance:
#                     level_status[level.id] = LevelStudentStatusChoice.SUSPENDED_WITH_COURSES
#                 else:
#                     level_status[level.id] = LevelStudentStatusChoice.APPROVED
#                     current_level = level
#                     # وضع المستويات الأعلى تحت المراجعة
#                     for l in levels:
#                         if l.level > level.level: 
#                             level_status[l.id] = LevelStudentStatusChoice.UNDER_REVIEW
#                     break
            
#             current_level = current_level or levels.first()

#             # ==========================
#             # إنشاء السجلات الجديدة
#             # ==========================
#             new_sb = StudentBatch.objects.create(
#                 fk_student=student, 
#                 fk_batch=new_batch, 
#                 fk_academic_year=academic_year, 
#                 fk_previous_batch=old_sb, 
#                 is_current=True, 
#                 accademic_status=AcademicStatusChoice.APPROVED
#             )
#             StudentBatch.objects.filter(fk_student=student).exclude(id=new_sb.id).update(is_current=False)

#             for level in levels:
#                 sl = StudentLevel.objects.create(
#                     fk_student_batch=new_sb, 
#                     fk_level=level, 
#                     student_level_status=level_status[level.id], 
#                     is_active=(level == current_level)
#                 )
#                 for sem in level.semester_set.all():
#                     ss = StudentSemester.objects.create(
#                         fk_student_level=sl, 
#                         fk_semester=sem, 
#                         student_semester_status=SemesterStudentStatusChoice.APPROVED
#                     )
                    
#                     for old_rec, target, grade in cleared_by_level[level.id]:
#                         if target.fk_semester_id == sem.id:
#                             StudentSubject.objects.create(
#                                 fk_student_semester=ss, 
#                                 fk_semmester_subject=target, 
#                                 total_grade=grade, 
#                                 results_status=ResultStatusChoice.CLEARANCE, 
#                                 subject_status=SubjectStatusChoice.EXEMPT, 
#                                 fk_previous_result=old_rec
#                             )
#                             StudentsClearingMaterials.objects.create(
#                                 fk_student_batch_old=old_sb, 
#                                 fk_student_batch_new=new_sb, 
#                                 fk_semester_subject_from=old_rec.fk_semmester_subject if old_rec else None, 
#                                 fk_semester_subject_to=target, 
#                                 type=StudentsClearingMaterialsChoice.EXEMPTED if old_rec is None else StudentsClearingMaterialsChoice.CLEARED
#                             )

#             # تحديث بيانات الطالب الأساسية
#             student.fk_current_specialization = new_specialization
#             student.fk_current_level = current_level
#             student.fk_current_semester = current_level.semester_set.order_by('name').first()
#             student.save()
#             student_batch = StudentBatch.objects.filter(fk_student=student,is_current=True).first()
#             student_batch.student_status = StudentStatusChoice.ACTIVE
#             student_batch.save()

#             return {
#                 'success': True, 
#                 'student_id': student.id, 
#                 'new_level': current_level.level, 
#                 'cleared_subjects': len(cleared_subjects)
#             }

#     except Exception as e: 
#         return {'success': False, 'error': str(e)}






import json
import os
import logging
from typing import Any, Dict
from decimal import Decimal
from django.utils import timezone
import datetime

from academic_affairs.models.DailySchedule import DailySchedule
from academic_affairs.models.Semester import Semester
from exam.models.ExamRegistration import ExamRegistration
from student_affairs.models.StudentBatch import StudentBatch
from django.db import transaction
from academic_affairs.models.Batch import Batch
from academic_affairs.models.ClearingMaterials import ClearingMaterials
from academic_affairs.models.Level import Level
from academic_affairs.models.SemesterSubject import SemesterSubject
from control.models.StudentsClearingMaterials import InternalClearance, StudentsClearingMaterials
from d_services.apis.external_methods.utils.helpers_methods import calculate_scaled_grade, find_equivalent_subject
from django.core.exceptions import ValidationError



from d_services.choices.choices import PaymentStatusChoice, GrantStatusChoice, DiscountStatusChoice
from student_affairs.models.Student import Student, StudentLevelStatusHistory,StudentBranchStatusHistory
from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
from student_affairs.models.StudentSchedules import StudentSchedules
from system_management.choices.choices import AcademicStatusChoice, LevelStudentStatusChoice, ProcessStatusChoices, ResultStatusChoice, \
    SemesterStudentStatusChoice, StudentStatusChoice, StudentsClearingMaterialsChoice, SubjectStatusChoice, \
    ExamAttendanceChoices, PrepareChoice, ProcessStatusChoices
from system_management.models.AcademicYear import AcademicYear
from system_management.models.Specialization import Specialization
from system_management.models.Subject import Subject
from utils.GradeApproval import GradeApproval
from .utils.helpers_methods import calculate_and_update_levels, create_new_student_batch, create_student_levels, create_student_semesters, get_specialization_and_parents_ids, get_student_batch, get_student_batch_and_parents_ids, get_student_subjects_history_for_old_specialization, get_subs_by_code_and_subs_by_name_for_new_batch, process_clearance_materials, update_student_data

from control.models.GradesLog import GradesLog
from exam.models.ExamRegistration import ExamRegistration
from student_affairs.models.StudentBatch import StudentBatch
from django.db import transaction
from academic_affairs.models.Batch import Batch
from academic_affairs.models.ClearingMaterials import ClearingMaterials
from academic_affairs.models.Level import Level
from academic_affairs.models.SemesterSubject import SemesterSubject
from control.models.StudentsClearingMaterials import StudentsClearingMaterials
from d_services.apis.external_methods.utils.helpers_methods import calculate_scaled_grade, find_equivalent_subject
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone




from d_services.choices.choices import PaymentStatusChoice, GrantStatusChoice, DiscountStatusChoice
from student_affairs.models.Student import Student, StudentLevelStatusHistory,StudentBranchStatusHistory
from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject, GradesRecord
from student_affairs.models.StudentSchedules import StudentSchedules
from system_management.choices.choices import AcademicStatusChoice, LevelStudentStatusChoice, ResultStatusChoice, \
    SemesterStudentStatusChoice, StudentStatusChoice, StudentsClearingMaterialsChoice, SubjectStatusChoice, \
    ExamAttendanceChoices, PrepareChoice, RecordChengeGrade, AppealStatusChoice, ExamTypeChoices
from system_management.models.AcademicYear import AcademicYear
from system_management.models.Subject import Subject
from .utils.helpers_methods import get_student_batch
from django.utils.translation import gettext_lazy as _
from control.models.AppealGradeSubject import AppealGradeSubject


logger = logging.getLogger(__name__)

# مسار ملف البيانات المالية المؤقت
MOCK_FINANCIAL_DATA_PATH = os.path.join(
    os.path.dirname(__file__), 
    'mock_financial_data.json'
)


def _load_financial_data() -> Dict[str, Any]:
    """تحميل بيانات النظام المالي المؤقت من ملف JSON"""
    try:
        with open(MOCK_FINANCIAL_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"ملف البيانات المالية غير موجود: {MOCK_FINANCIAL_DATA_PATH}")
        return {'payments': {}, 'grants': {}, 'discounts': {}}
    except json.JSONDecodeError as e:
        logger.error(f"خطأ في قراءة ملف البيانات المالية: {e}")
        return {'payments': {}, 'grants': {}, 'discounts': {}}


def _calculate_payment_status(
    total_fee: Decimal,
    amount_paid: Decimal,
    remaining_amount: Decimal,
    has_grant: bool,
    is_full_grant: bool,
    has_discount: bool,
    is_full_discount: bool
) -> str:
    """
    حساب حالة الدفع بناءً على جميع الاحتمالات
    """
    # الخدمة مجانية
    if total_fee <= 0:
        return PaymentStatusChoice.FREE
    
    # حساب نسبة المبلغ المدفوع
    is_fully_paid = (remaining_amount <= 0 or amount_paid >= total_fee)
    is_partially_paid = (amount_paid > 0 and remaining_amount > 0)
    
    if is_fully_paid:
        if has_grant and has_discount:
            return PaymentStatusChoice.PAID_BY_GRANT_DISCOUNT
        elif has_grant and is_full_grant:
            return PaymentStatusChoice.PAID_BY_GRANT
        elif has_discount and is_full_discount:
            return PaymentStatusChoice.PAID_BY_DISCOUNT
        else:
            return PaymentStatusChoice.PAID
    
    if is_partially_paid:
        if has_grant and has_discount:
            return PaymentStatusChoice.PARTIAL_GRANT_DISCOUNT
        elif has_grant:
            return PaymentStatusChoice.PARTIAL_GRANT
        elif has_discount:
            return PaymentStatusChoice.PARTIAL_DISCOUNT
        else:
            return PaymentStatusChoice.PARTIAL
    
    return PaymentStatusChoice.UNPAID


def call_execute_update_financial_status(action, request) -> Dict[str, Any]:
    """
    تحديث البيانات المالية للطلب من النظام المالي
    """
    service_request = action.fk_request
    request_number = service_request.request_number
    
    logger.info(f"تحديث البيانات المالية للطلب: {request_number}")
    
    try:
        financial_data = _load_financial_data()
        updated_fields = []
        
        # تحديث بيانات الدفع والأقساط
        payment_data = financial_data.get('payments', {}).get(request_number)
        if payment_data:
            service_request.amount_paid = Decimal(str(payment_data.get('amount_paid', 0)))
            service_request.remaining_amount = Decimal(str(payment_data.get('remaining_amount', 0)))
            updated_fields.extend(['amount_paid', 'remaining_amount'])
            
            if payment_data.get('has_installments'):
                installments = payment_data.get('installments', [])
                paid_count = sum(1 for inst in installments if inst.get('paid'))
                total_count = len(installments)
                logger.info(f"الأقساط: {paid_count}/{total_count} مدفوعة")
        
        # تحديث بيانات المنحة
        grant_data = financial_data.get('grants', {}).get(request_number)
        has_grant = False
        is_full_grant = False
        
        if grant_data and grant_data.get('has_grant'):
            grant_status_map = {
                'APPROVED': GrantStatusChoice.APPROVED,
                'PENDING': GrantStatusChoice.PENDING,
                'REJECTED': GrantStatusChoice.REJECTED,
                'NO_GRANT': GrantStatusChoice.NO_GRANT,
            }
            
            service_request.grant_status = grant_status_map.get(
                grant_data.get('grant_status'),
                GrantStatusChoice.NO_GRANT
            )
            service_request.grant_percentage = Decimal(str(grant_data.get('grant_percentage', 0)))
            service_request.grant_amount = Decimal(str(grant_data.get('grant_amount', 0)))
            
            updated_fields.extend(['grant_status', 'grant_percentage', 'grant_amount'])
            
            if grant_data.get('grant_status') == 'APPROVED':
                has_grant = True
                grant_type = grant_data.get('grant_type')
                is_full_grant = (grant_type == 'FULL' or service_request.grant_percentage >= 100)
        
        # تحديث بيانات الخصم
        discount_data = financial_data.get('discounts', {}).get(request_number)
        has_discount = False
        is_full_discount = False
        
        if discount_data and discount_data.get('has_discount'):
            discount_status_map = {
                'APPROVED': DiscountStatusChoice.APPROVED,
                'PENDING': DiscountStatusChoice.PENDING,
                'REJECTED': DiscountStatusChoice.REJECTED,
                'NO_DISCOUNT': DiscountStatusChoice.NO_DISCOUNT,
            }
            
            service_request.discount_status = discount_status_map.get(
                discount_data.get('discount_status'),
                DiscountStatusChoice.NO_DISCOUNT
            )
            service_request.discount_amount = Decimal(str(discount_data.get('discount_amount', 0)))
            
            if discount_data.get('discount_reason'):
                service_request.discount_reason = discount_data.get('discount_reason')
            
            updated_fields.extend(['discount_status', 'discount_amount', 'discount_reason'])
            
            if discount_data.get('discount_status') == 'APPROVED':
                has_discount = True
                is_full_discount = (service_request.discount_amount >= service_request.total_fee)
        
        # تحديد حالة الدفع النهائية
        payment_status = _calculate_payment_status(
            total_fee=service_request.total_fee,
            amount_paid=service_request.amount_paid,
            remaining_amount=service_request.remaining_amount,
            has_grant=has_grant,
            is_full_grant=is_full_grant,
            has_discount=has_discount,
            is_full_discount=is_full_discount
        )
        
        service_request.payment_status = payment_status
        updated_fields.append('payment_status')
        
        if updated_fields:
            service_request.save(update_fields=updated_fields)
            logger.info(f"تم تحديث الحقول: {updated_fields}")
        
        return {
            'success': True,
            'message': 'تم تحديث البيانات المالية بنجاح',
            'data': {
                'request_number': request_number,
                'updated_fields': updated_fields,
                'payment_status': service_request.payment_status,
            }
        }
        
    except Exception as e:
        logger.error(f"خطأ في تحديث البيانات المالية: {e}")
        return {
            'success': False,
            'message': f'حدث خطأ أثناء تحديث البيانات المالية: {str(e)}',
            'data': {}
        }


@transaction.atomic
def call_create_internal_clearance(action, request):
    """موافقة على اجراء المقاصه الداخلية"""
    instance = action.fk_request
    version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
    target_audience_data = instance.target_audience_data if isinstance(instance.target_audience_data, dict) else {}
    fk_student_level = target_audience_data.get('fk_student_level')
    student_level = StudentLevel.objects.get(id=fk_student_level)
    internal_clearance = InternalClearance.objects.filter(fk_request=instance).first()
    # الحصول على السنة الاكاديمية للطالب الحالي
    student_academic_year = student_level.fk_student_batch.fk_academic_year

    # السيناريو 1 البحث عن دفعة بنفس السنة الاكاديمية
    new_batch = Batch.objects.filter(fk_specialization_id=version_data.get('fk_new_specialization'),
                                     fk_academic_year=student_academic_year).first()

    # السيناريو 2 اذا لم توجد دفعة بنفس السنة استخدم احدث دفعة
    if not new_batch:
        new_batch = Batch.objects.filter(
            fk_specialization_id=version_data.get('fk_new_specialization'),
        ).order_by("-fk_academic_year").first()

    if not internal_clearance:
        internal_clearance = InternalClearance.objects.create(
            fk_request=instance,
            fk_student_batch_old=student_level.fk_student_batch,
            fk_batch_new=new_batch,
        )
    specializations_ids = get_specialization_and_parents_ids(
        student_level.fk_student_batch.fk_batch.fk_specialization.id)


    # 1. جلب تاريخ الطالب باستخدام الدالة الجديدة (المقسمة لقواميس)
    student_history_maps = get_student_subjects_history_for_old_specialization(
        student_level.fk_student_batch.fk_student.id,
        specializations_ids
    )

    history_by_id = student_history_maps['history_by_semester_subject_id']
    history_by_code = student_history_maps['history_by_code']
    history_by_name = student_history_maps['history_by_name']

    # 2. جلب قواعد المقاصة الرسمية (المعرفة مسبقاً من الإدارة)
    # {id_المادة_الجديدة: id_المادة_القديمة}
    official_rules = {
        rule.fk_semester_subject_to_id: rule.fk_semester_subject_from_id
        for rule in ClearingMaterials.objects.filter(active=True)
    }

    # 3. جلب جميع مواد التخصص الجديد
    new_subjects = SemesterSubject.objects.filter(
        fk_semester__fk_level__fk_batch=new_batch
    ).select_related('fk_subject')

    internal_clearance.internal_clearance_clearing_set.all().delete()
    clearing_materials_to_create = []

    for new_ss in new_subjects:
        matched_attempt = None

        # --- سلم أولويات المطابقة ---

        # أولاً: البحث عبر القواعد الرسمية (Official Rules)
        old_ss_id_from_rule = official_rules.get(new_ss.id)
        if old_ss_id_from_rule:
            matched_attempt = history_by_id.get(old_ss_id_from_rule)

        # ثانياً: البحث عبر الكود (Code Matching)
        if not matched_attempt and new_ss.fk_subject.subject_code:
            code = new_ss.fk_subject.subject_code.strip().lower()
            matched_attempt = history_by_code.get(code)

        # ثالثاً: البحث عبر الاسم (Name Matching)
        if not matched_attempt:
            # نجرب الاسم العربي ثم الإنجليزي
            names_to_check = [new_ss.fk_subject.name_ar, new_ss.fk_subject.name_en]
            for name in names_to_check:
                if name:
                    matched_attempt = history_by_name.get(name.strip().lower())
                    if matched_attempt: break

        # 4. بناء السجل بناءً على نتيجة البحث
        if matched_attempt:
            clearing_materials_to_create.append(StudentsClearingMaterials(
                fk_internal_clearance=internal_clearance,
                fk_semester_subject_from=matched_attempt.fk_semmester_subject,
                fk_semester_subject_to=new_ss,
                type=StudentsClearingMaterialsChoice.CLEARED,
                process_status=ProcessStatusChoices.UNDER_REVIEW
            ))
        else:
            clearing_materials_to_create.append(StudentsClearingMaterials(
                fk_internal_clearance=internal_clearance,
                fk_semester_subject_from=None,
                fk_semester_subject_to=new_ss,
                type=StudentsClearingMaterialsChoice.REMAINING,
                process_status=ProcessStatusChoices.UNDER_REVIEW
            ))

    # الحفظ الجماعي
    if clearing_materials_to_create:
        StudentsClearingMaterials.objects.bulk_create(clearing_materials_to_create)

    return {"success": True, "count": len(clearing_materials_to_create)}

@transaction.atomic
def execute_internal_clearance(internal_clearance:InternalClearance, request):
    """تنفيذ اجراء المقاصه الداخلية"""
    """
    تنفيذ المقاصة فعليًا:
    - إنشاء دفعة جديدة للتخصص الجديد
    - إنشاء مستويات وفصول لكل مستوى
    - تطبيل المقاصة على المواد الناجحة و المعفاة
    - تحديث حالة الطالب والمستوى الحالي
    """
    instance = internal_clearance.fk_request

    version_data = instance.version_data if isinstance(instance.version_data,dict) else {}

    new_batch = Batch.objects.filter(fk_specialization_id=version_data.get('fk_new_specialization')).order_by('-id').first()
    if not new_batch:
        return {'success': False, 'error': 'لا توجد دفعات للتخصص الجديد'}

    old_sb = internal_clearance.fk_student_batch_old
    new_batch = internal_clearance.fk_batch_new
    student = old_sb.fk_student

    # ==========================
    # 1 تجهيز المواد المقاصة
    # ==========================
    materials = StudentsClearingMaterials.objects.select_related(
        'fk_semester_subject_from',
        'fk_semester_subject_to__fk_grading_system_june',
        'fk_semester_subject_to__fk_semester__fk_level'
    ).filter(
        fk_internal_clearance=internal_clearance,
        process_status=ProcessStatusChoices.APPROVED
    )

    if not materials.exists():
        return {'sucess': False, 'error': 'لا يوجد مواد مقبولة للتنفيذ'}
    # ==========================
    # 2. إنشاء StudentBatch جديد
    # ==========================
    # academic_year = AcademicYear.objects.filter(is_cournt=True).first() or AcademicYear.objects.order_by('-id').first()
    new_sb, created = create_new_student_batch(student,old_sb,new_batch,new_batch.fk_academic_year)

    internal_clearance.fk_student_batch_new = new_sb
    internal_clearance.save(update_fields=['fk_student_batch_new'])

    # ==========================
    # انشاء مستويات الطالب
    # ==========================
    student_levels, current_level = create_student_levels(new_sb,new_batch)

    # ==========================
    # إنشاء فصول لكل مستوى
    # ==========================
    student_semesters = create_student_semesters(student_levels)

    # ==========================
    # معالجة المواد المقاصة
    # ==========================
    processed_count = process_clearance_materials(materials,old_sb,new_sb,student_levels,student_semesters)

    # ==========================
    # تحديث بيانات الطالب
    # ==========================
    current_level = calculate_and_update_levels(student_levels)

    update_student_data(student,current_level,new_batch)

    # ==========================
    # تحديث حالة المقاصة
    # ==========================
    internal_clearance.is_approved = True
    internal_clearance.save(update_fields=['is_approved'])

    return {
        'success': True,
        'student_id': student.id,
        'new_level': current_level.fk_level.get_level_display(),
        'executed_subjects': processed_count
    }



def call_execute_enrollment_certificate(action,request):
    """
    طباعة شهادة القيد الدراسي.
    """
    try:
        instance = action.fk_request
        student_batch = get_student_batch(instance)
        batch = student_batch.fk_student_batch
        student = student_batch.fk_student
        current_student_level = student_batch.current_student_level
        current_level = current_student_level.fk_level if current_student_level else None
        return {
            "student_name": student.full_name_ar,
            "student_id": student.academice_no,
            "nationality": student.fk_nationality.name_ar if student.fk_nationality else None,
            "date_of_birth": student.date_of_birth,
            "place_of_birth": student.place_of_brith,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": batch.fk_specialization.fk_college.name_ar if batch.fk_specialization else None,
            "specialization": batch.fk_specialization.name_ar if batch.fk_specialization else None,
            "level": current_level.get_level_display() if current_level else None,
            "enrollment_year": student.fk_enrollment_year.year_m,
            "current_academic_year": current_level.fk_academic_year.year_m if current_level else None,
            "issue_date": datetime.date.today(),
        }
    except:
        return {
            'success': False,
            'message': 'حدث خطأ ما في الحصول على بيانات شهادة القيد الدراسي.'
        }

@transaction.atomic
def call_execute_suspension_inrollment(action,request):
    """
    تنفيذ اجراء وقف القيد.
    """
    try:
        instance = action.fk_request
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        version_data = instance.version_data if instance.version_data else {}

        # التحقق من أن الطالب مستمر ليتم وقفه
        # if student_batch.student_status != StudentStatusChoice.ACTIVE:
        #     raise ValidationError("يمكن وقف قيد الطلاب المستمرين فقط.")

        # تسجيل تاريخ تغيير الحالة للطالب
        StudentBranchStatusHistory.objects.create(
            fk_student_batch=student_batch,
            academic_status_before=student_batch.student_status,
            academic_status_after=StudentStatusChoice.WITHDRAWN,
            reason=f"تنفيذ خدمة وقف القيد",
            changed_by=request.user
        )

        # تحديث حالة الطالب إلى موقف قيد
        student_batch.student_status = StudentStatusChoice.WITHDRAWN
        student.save()

        # تحديث حالة الدفعة إلى وقف قيد
        student_batch.accademic_status = AcademicStatusChoice.SUSPENDED
        student_batch.save()

        current_level = student_batch.level_set.filter(is_active=True,fk_level__is_current=True).first()
        if not current_level:
            current_level = student_batch.level_set.filter(is_active=True).first()

        if current_level:
            # تسجيل تاريخ تغيير حالة المستوى
            StudentLevelStatusHistory.objects.create(
                fk_student_level=current_level,
                student_level_status_before=current_level.student_level_status,
                student_level_status_after=LevelStudentStatusChoice.WITHDRAWN,
                reason="وقف قيد مستوى",
                changed_by=request.user
            )
            current_level.student_level_status = LevelStudentStatusChoice.WITHDRAWN
            current_level.save()

            # وقف جميع الفصول التابعة للمستوى النشط وتسجيل تاريخها
            current_semester = current_level.semester_set.filter(is_active=True,fk_semester__is_current=True).first()
            if not current_semester:
                current_semester = current_level.semester_set.filter(is_active=True).first()
            if current_semester:
                current_semester.student_semester_status=SemesterStudentStatusChoice.WITHDRAWN
                current_semester.save()

            logger.info(f"تم وقف قيد المستوى للطالب {student.full_name_ar}")

    except ValidationError as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ عند تنفيذ وقف القيد: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة وقف القيد: {str(e)}")

@transaction.atomic
def call_execute_cancellation_suspension_inrollment(action,request):
    """
    تنفيذ اجراء الغاء وقف القيد.
    """
    try:
        instance = action.fk_request
        # instance = action
        old_student_batch = get_student_batch(instance)
        student = old_student_batch.fk_student


        suspended_level = old_student_batch.level_set.filter(
            student_level_status=LevelStudentStatusChoice.WITHDRAWN).last()

        if not suspended_level:
            raise ValidationError('لم يتم العثور على مستوى دراسي موقوف لهذا الطالب.')

        # الحصول على الفصل الدراسي الموقوف قيد فيه.
        suspended_semester = suspended_level.semester_set.filter(
            student_semester_status=SemesterStudentStatusChoice.WITHDRAWN
        ).first()

        # اذا لم يوجد فصل دراسي موقوف قيد, نقوم بالبحث عن الفصل الاول للمستوى الموقوف قيد فيه.
        if not suspended_semester:
            suspended_semester = suspended_level.semester_set.filter(is_active=True).first()

        try:
            current_academic_level = Level.objects.get(
                level=suspended_level.fk_level.level,
                is_current=True,
                fk_batch__fk_specialization=old_student_batch.fk_batch.fk_specialization,
            )
        except Level.DoesNotExist:
            raise Exception((f"لا توجد دفعة حالية نشطة للمستوى {suspended_level.fk_level.get_level_display()}"))

        except Level.MultipleObjectsReturned:
            raise Exception("يوجد اكثر من دفعة دراسية تدرس نفس المستوى.")

        try:
            current_academic_semester = Semester.objects.get(
                fk_level=current_academic_level,
                is_current=True,
            )

        except Semester.DoesNotExist:
            raise Exception((f"لا يوجد فصل دراسي حالي للمستوى {suspended_level.fk_level.get_level_display()}"))

        except Semester.MultipleObjectsReturned:
            raise Exception("يوجد اكثر من فصل دراسي حالي لنفس المستوى.")

        # اذا كان الغاء وقف القيد في نفس الدفعة لوقف القيد يتم تحديث حالة الطالب فقط
        if suspended_level.fk_level.fk_batch == current_academic_level.fk_batch:

            old_student_batch.student_status = StudentStatusChoice.ACTIVE
            old_student_batch.save()

            suspended_level.student_level_status = LevelStudentStatusChoice.APPROVED
            suspended_level.save()

            if suspended_semester:
                suspended_semester.student_semester_status = SemesterStudentStatusChoice.APPROVED
                suspended_semester.save()

        else:

            if not current_academic_level:
                raise ValidationError(f"لا توجد دفعة حالية نشطة للمستوى {suspended_level.fk_level.get_level_display()}")

            # انشاء سجل دفعة جديد للطالب مرتبط بالدفعة الحالية لمستوى الطالب
            old_student_batch.is_current = False
            old_student_batch.save()

            new_student_batch = StudentBatch.objects.create(
                fk_student=student,
                fk_academic_year=current_academic_level.fk_academic_year,
                fk_previous_batch=suspended_level.fk_student_batch,
                fk_batch=current_academic_level.fk_batch,
                accademic_status=AcademicStatusChoice.APPROVED,
                is_current=True,
                number_based_on_status=old_student_batch.number_based_on_status,
                fk_study_system=old_student_batch.fk_study_system,
                fk_branch=old_student_batch.fk_branch,
                academic_no=old_student_batch.academic_no,
                certification_has_printed=old_student_batch.certification_has_printed,
            )

            # انشاء سجل مستوى جديد للطالب
            new_student_level = StudentLevel.objects.create(
                fk_student_batch=new_student_batch,
                fk_level=current_academic_level,
                is_active=suspended_level.is_active,
                estimate=suspended_level.estimate,
                avg=suspended_level.avg,
                total_grade=suspended_level.total_grade,
                card_has_preinted=suspended_level.card_has_preinted,
                student_level_status=LevelStudentStatusChoice.APPROVED,
            )

            # نسخ سجل الفصل الدراسي الذي تم وقف القيد فيه
            if suspended_semester:
                # TODO يجب تعديل قيد unique_seating_no_fk_semester_no_deleted بحيث يسمح بعملية التكرار
                student_semester = StudentSemester.objects.create(
                    fk_student_level=new_student_level,
                    fk_semester=current_academic_semester,
                    is_active=suspended_semester.is_active,
                    estimate=suspended_semester.estimate,
                    avg=suspended_semester.avg,
                    total_grade=suspended_semester.total_grade,
                    PIN=suspended_semester.PIN,
                    seating_no=None,
                    student_semester_status=suspended_semester.student_semester_status,
                )
                current_semester_subjects = current_academic_semester.subjects.all()
                # ربط الطالب بمواد الفصل
                for sub in current_semester_subjects:
                    StudentSubject.objects.get_or_create(
                        fk_student_semester= student_semester,
                        fk_semmester_subject=sub,
                    )
            # انشاء سجلات الفصل الدراسي التي لم يدرسها الطالب وربطها مع الدفعة الجديدة
            remaining_level_semester = suspended_level.semester_set.exclude(
                fk_semester=current_academic_semester).values_list('fk_semester__name', flat=True)
            new_level_semesters = current_academic_level.semester_set.filter(
                name__in=remaining_level_semester)

            if remaining_level_semester:
                for semester in new_level_semesters:
                    StudentSemester.objects.create(
                        fk_student_level=new_student_level,
                        fk_semester=semester,
                        is_active=True,
                        seating_no=None,
                        student_semester_status=SemesterStudentStatusChoice.UNDER_REVIEW,
                    )

            # تحديث مستويات الطالب التي تم انشائها من قبل للدفعة القديمة
            remaining_student_levels = old_student_batch.level_set.filter(
                fk_level__level__gt=suspended_level.fk_level.level)
            remaining_student_levels.update(is_active=False)

            # الحصول على المستويات المتبقية بالدفعة الجديدة لربطها مع الطالب
            new_batch_levels = current_academic_level.fk_batch.level_set.exclude(level=current_academic_level.level)

            for new_batch_level in new_batch_levels:
                new_student_batch_level = StudentLevel.objects.create(
                    fk_student_batch=new_student_batch,
                    fk_level=new_batch_level,
                    is_active=True,
                    student_level_status=LevelStudentStatusChoice.UNDER_REVIEW
                )

                # الحصول على فصول المستوى الدراسي للدفعة الجديد.
                new_level_semesters = new_batch_level.semester_set.all()

                # انشاء سجلات الفصل الدراسي للمستويات مع الدفعة الجديد
                for new_semester in new_level_semesters:
                    student_semester = StudentSemester.objects.create(
                        fk_student_level=new_student_batch_level,
                        fk_semester=new_semester,
                        is_active=True,
                        seating_no=None,
                        student_semester_status=SemesterStudentStatusChoice.UNDER_REVIEW,
                    )
                    new_semester_subjects = new_semester.subjects.all()
                    # ربط الطالب بمواد الفصل الدراسي
                    for sub in new_semester_subjects:
                        StudentSubject.objects.get_or_create(
                            fk_student_semester = student_semester,
                            fk_semmester_subject = sub
                        )

            # # تحديث فصول الطالب التي تم انشائها من قبل للدفعة القديمة
            # remaining_student_semesters = StudentSemester.objects.filter(
            #     fk_student_level__fk_student_batch=old_student_batch,
            #     fk_semester__name__gt=suspended_semester.fk_semester.name)
            #
            # for remaining_semester in remaining_student_semesters:
            #     remaining_semester.is_active = False
            #     remaining_semester.save()
        logger.info(f"تم الغاء وقف قيد الطالب { student.full_name_ar}")

    except ValidationError as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ عند تنفيذ الغاء وقف القيد: {str(e)} ")
        raise Exception(f"فشل تنفيذ خدمة  الغاءوقف القيد: {str(e)}")

@transaction.atomic
def call_execute_student_withdrawal(action,request):
    """
    تنفيذ اجراء سحب ملف الطالب.
    """
    try:
        instance = action.fk_request
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        withdrawal_reason = version_data.get('withdrawal_reason')

        # التحقق من أن الطالب ليس منسحباً بالفعل
        if student_batch.student_status == StudentStatusChoice.DROPPED_OUT:
            raise ValidationError("الطالب منسحب بالفعل.")

        # تسجيل تاريخ تغيير الحالة
        StudentBranchStatusHistory.objects.create(
            fk_student_batch=student_batch,
            academic_status_before=student_batch.student_status,
            academic_status_after=StudentStatusChoice.DROPPED_OUT,
            reason=  withdrawal_reason if withdrawal_reason else "تنفيذ خدمة سحب ملف",
            changed_by=request.user
        )

        # تحديث حالة الطالب إلى منسحب
        student_batch.student_status = StudentStatusChoice.DROPPED_OUT
        student_batch.save()

        # ايقاف المستويات النشطة وتغيير حالتها
        active_levels = student_batch.level_set.filter(is_active=True)
        for student_level in active_levels:
            StudentLevelStatusHistory.objects.create(
                fk_student_level=student_level,
                student_level_status_before=student_level.student_level_status,
                student_level_status_after=LevelStudentStatusChoice.WITHDRAWN,
                reason=withdrawal_reason if withdrawal_reason else "تنفيذ خدمة سحب ملف",
                changed_by=request.user,
            )

            #  ايقاف الفصول النشطة وتغيير حالتها لكل مستوى
            for semester in student_level.semester_set.all():
                # (تنازل) تغيير حالة مواد الطالب للفصل الى
                for subject in semester.subjects.all():
                    subject.subject_status = SubjectStatusChoice.WITHDRAWN
                    subject.results_status = ResultStatusChoice.WITHDRAWN
                    subject.save()

                semester.is_active = False
                semester.student_semester_status = SemesterStudentStatusChoice.WITHDRAWN
                semester.save()

            student_level.is_active = False
            student_level.student_level_status = LevelStudentStatusChoice.WITHDRAWN
            student_level.save()



        # إلغاء تفعيل الدفعة الحالية
        student_batch.is_current = False
        student_batch.save()
        logger.info(f"تم سحب ملف الطالب {student.full_name_ar}")
        return True

    except ValidationError as e:
        raise e
    except Exception as e:
        logger.error(f"خطأ عند سحب الملف: {str(e)}")
        raise Exception(f"فشل سحب الملف: {str(e)}")


@transaction.atomic
def call_execute_retake_subject(action,request):
    """
    تنفيذ اجراء اعادة مادة.
    """
    try:
        instance = action.fk_request
        # instance = action
        target_audience_data = instance.target_audience_data
        student_batch = get_student_batch(instance)
        version_data = instance.version_data
        fk_student_subject = target_audience_data.get('fk_student_subject', None)

        old_student_subject = StudentSubject.objects.get(id=fk_student_subject)
        old_semester = old_student_subject.fk_student_semester.fk_semester
        old_level = old_semester.fk_level

        if not fk_student_subject:
            raise ValidationError("لم يتم اختيار مادة للإعاة.")

        # التحقق من حالة الطالب
        if student_batch.student_status != StudentStatusChoice.ACTIVE:
            raise ValidationError("لا يمكن تنفيذ خدمة الإعادة لطالب غير مستمر.")

        if old_student_subject.fk_previous_result:
            raise ValidationError("لا يمكنك اعادة مادة تم اعادتها مسبقا.")

        # منطق إضافة المادة
        try:
            current_academic_level = Level.objects.get(
                level=old_level.level,
                is_current=True,
                fk_batch__fk_specialization=student_batch.fk_batch.fk_specialization,
            )
            if old_level == current_academic_level:
                raise Exception("لا يمكن اعادة المادة مع نفس الدفعة الدراسية التي درس فيها المادة.")

        except Level.DoesNotExist:
            raise Exception(f"لا توجد دفعة حالية نشطة للمستوى. ")

        except Level.MultipleObjectsReturned:
            raise Exception("يوجد اكثر من دفعة دراسية تدرس نفس المستوى.")

        try:
            current_academic_semester = Semester.objects.get(
                fk_level=current_academic_level,
                is_current=True,
            )

            if old_semester == current_academic_semester:
                raise Exception("لا يمكن اعادة المادة مع نفس الدفعة الدراسية التي درس فيها المادة.")

        except Semester.DoesNotExist:
            raise Exception(f"لا يوجد فصل دراسي حالي لمستوى الدفعة ")

        except Semester.MultipleObjectsReturned:
            raise Exception("يوجد اكثر من فصل دراسي فعال لنفس المستوى.")

        try:
            # التحقق من تواجد المادة في خطة الفصل الدراسي للدفعة الحالية
            current_semester_subject = SemesterSubject.objects.get(
                fk_semester=current_academic_semester,
                fk_subject=old_student_subject.fk_semmester_subject.fk_subject,
            )

        except SemesterSubject.DoesNotExist:
            raise Exception("لا توجد المادة المراد اعادتها في خطة الفصل الدراسي الحالي.")

        except SemesterSubject.MultipleObjectsReturned:
            raise Exception("يوجد اكثر من سجل لنفس المادة في خطة الفصل الدراسي")

        StudentSubject.objects.create(
            fk_student_semester=old_student_subject.fk_student_semester,
            fk_previous_result=old_student_subject,
            fk_semmester_subject=current_semester_subject,
            results_status=ResultStatusChoice.PENDING,
            subject_status=SubjectStatusChoice.UNDER_REVIEW,
        )
        # تحديث حالة نتيجة المادة التي تم اعادتها
        old_student_subject.results_status = ResultStatusChoice.WITHDRAWN
        old_student_subject.save()
        logger.info(f"تم تنفيذ خدمة الإعادة للطالب {student_batch.fk_student.full_name_ar}")
        return True

    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ إعادة مادة: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ إعادة مادة: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة الإعادة: {str(e)}")


def call_execute_attendance_exemption(action,request):
    """
    تنفيذ اجراء خدمة اعفاء حظور
    """
    try:
        instance = action.fk_request
        # instance = action
        student_batch = get_student_batch(instance)
        version_data = instance.version_data
        fk_periods_4_schedule = version_data.get('fk_periods')
        from_date = version_data.get('from_date')
        to_date = version_data.get('to_date')
        current_student_level = student_batch.current_student_level
        current_student_semester = current_student_level.current_student_semester if current_student_level else None
        if not from_date or not to_date:
            raise ValidationError("يتطلب تحديد التاريخ المطلوب لاعفاء الحظور")

        if not current_student_semester:
            raise ValidationError("لا يوجد فصل دراسي حالي للدفعة.")

        semester_subjects = SemesterSubject.objects.filter(
            fk_semester=current_student_semester.fk_semester,
        )
        if not semester_subjects:
            raise ValidationError("لا يوجد مواد دراسية للفصل الدراسي لكي يتم اعفاء الطالب من حظورها.")

        # الحصول على سجلات الحظور لمود الطالب في الفصل الدراسي الحالي للدفعة, باستثناء حالة الحظور (حاضر - معفي)
        student_attendance_records = StudentSchedules.objects.filter(
            fk_student_group__fk_student_semester=current_student_semester,
            fk_semester_subject__in=semester_subjects,
            fk_daily_schedule__date__gte=from_date,
            fk_daily_schedule__date__lte=to_date,

        ).exclude(status__in=[PrepareChoice.PRESENT,PrepareChoice.EXEMPTED])

        # لتحديد السجلات للفترات المطلوبة
        if fk_periods_4_schedule:
            student_attendance_records = student_attendance_records.filter(
                fk_daily_schedule__fk_period_4_schedule_id__in=fk_periods_4_schedule,
            )

        if not student_attendance_records:
            raise ValidationError("لا يوجد سجلات حظور لمواد الطالب تتطلب اعفاء.")

        student_attendance_records.update(status=PrepareChoice.EXEMPTED)
        logger.info("تم تنفيذ خدمة اعفاء حظور للطالب {} في المستوى {} للفصل الدراسي {} من تاريخ {} الى تاريخ {}".format(
            student_batch.fk_student.full_name_ar,
            current_student_level.fk_level.get_level_display(),
            current_student_semester.fk_semester.get_name_display(),
            from_date,
            to_date
        ))

    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ اعفاء حظور: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ اعفاء حظور: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة اعفاء حظور: {str(e)}")

def call_execute_clearance(action,request):
    """
    تنفيذ اجراء خدمة اخلاء طرف
    """
    try:
        # instance = action.fk_request
        instance = action
        student_batch = get_student_batch(instance)
        version_data = instance.version_data

    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ اخلاء طرف: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ اخلاء طرف: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة اخلاء طرف: {str(e)}")

def call_execute_add_student_subjects_to_appeal(action,request):
    """اضافة مواد الطالب المطلوبة الى قائمة التظلمات"""
    try:
        instance = action.fk_request
        version_data = instance.version_data
        target_audience_data = instance.target_audience_data if isinstance(instance.target_audience_data,dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject')
        try:
            student_subject = StudentSubject.objects.get(id=fk_student_subject)

        except StudentSubject.DoesNotExist:
            raise Exception(_(f" {fk_student_subject}لم يتم العثور على سجل مادة الطالب ذو المعرف "))
        # التحقق من اقفال الفصل الدراسي
        subject_semester = student_subject.fk_semmester_subject.fk_semester

        if subject_semester.is_locked:
            raise ValidationError(_("لا يمكن التظلم بعد اقفال الفصل الدراسي."))

        AppealGradeSubject.objects.create(
            fk_request=instance,
            fk_student_subject=student_subject,
            previous_total_grade=student_subject.total_grade,
        )
    
    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ تظلم على نتيجة مادة: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ تظلم على نتيجة مادة: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة تظلم على نتيجة مادة: {str(e)}")

@transaction.atomic
def call_execute_grievance_course_grade(appeal:AppealGradeSubject,grades_list: list,user):
    """
    تنفيذ اجراء خدمة تظلم على نتيجة حظور
    """
    try:
        student_subject = appeal.fk_student_subject
        old_total_grade = student_subject.total_grade

        for grade_record in grades_list:
            grade_record_obj = GradesRecord.objects.get(id=grade_record.get('id'))
            old_grade = grade_record_obj.grade
            new_grade = Decimal(grade_record.get('new_grade',0.0))

            if old_grade != new_grade:
                GradesLog.objects.create(
                    fk_grade_record=grade_record_obj,
                    fk_user= user,
                    grade_before= old_grade,
                    grade_after= new_grade,
                    changed_when= RecordChengeGrade.r3,
                    date= timezone.now(),
                )
                grade_record_obj.grade = new_grade
                grade_record_obj.save()

        new_total_grade = student_subject.grade_record.aggregate(total=models.Sum('grade'))['total']
        if new_total_grade != old_total_grade:
            appeal.new_total_grade = new_total_grade
            appeal.status = AppealStatusChoice.GRADE_CHANGED
            student_subject.total_grade = new_total_grade
            student_subject.adding_results_date=None
            student_subject.save()
        else:
            appeal.new_total_grade = old_total_grade
            appeal.status = AppealStatusChoice.GRADE_NOT_CHANGED
        appeal.processed_at = timezone.now()
        appeal.save()


    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ تظلم على نتيجة مادة: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ تظلم على نتيجة مادة: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة تظلم على نتيجة مادة: {str(e)}")

def call_execute_housing(action,request):
    """
    تنفيذ اجراء خدمة طلب سكن
    """
    pass

def call_execute_replacement_id_card(action,request):
    """
    تنفيذ اجراء خدمة قطع بطاقة بدل فاقد
    """
    try:
        instance = action.fk_request
        # instance = action
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        version_data = instance.version_data
        current_student_level = student_batch.current_student_level
        if not current_student_level:
            raise Exception("لم يتم العثور على المستوى الحالي للطالب.")
        if not current_student_level.is_active:
            raise Exception("سجل الطالب في المستوى الحالي غير نشط.")
        current_student_level.card_has_preinted = True
        current_student_level.save()
        logger.info(f"تم قطع بطاقة بدل فاقد للطالب {student.full_name_ar} للمستوى  {current_student_level.fk_level.get_level_display()}")

    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ قطع بطاقة بدل فاقد: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ قطع بطاقة بدل فاقد: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة قطع بطاقة بدل فاقد: {str(e)}")

def call_execute_excused_absence(action,request):
    """
    تنفيذ اجراء خدمة غياب بعذر
    """
    try:
        instance = action.fk_request
        student_batch = get_student_batch(instance)
        version_data = instance.version_data if isinstance(instance.version_data,dict) else {}

        target_audience_data = instance.target_audience_data if isinstance(instance.target_audience_data, dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject')
        student_subject = StudentSubject.objects.filter(id=fk_student_subject).first()
        if not fk_student_subject:
            raise ValidationError("لا توجد مادة مختارة لطلب الغياب بعذر.")

        if not student_subject:
            raise ValidationError(f"الطالب غير مسجل بالمادة ذو المعرف {fk_student_subject}.")
        subject = student_subject.fk_semmester_subject.fk_subject

        # الحصول على سجل الامتحان للطالب لهذه المادة
        exam_registration = ExamRegistration.objects.filter(
            fk_student_subject=student_subject,
            fk_exam_schedule__exam_type=ExamTypeChoices.FINAL
        ).first()

        if not exam_registration:
            raise ValidationError("الطالب غير مسجل للامتحان بهذه المادة.")

        if exam_registration.attendance not in [ExamAttendanceChoices.ABSENCE, ExamAttendanceChoices.OTHER]:
            raise ValidationError(f' حالة الطالب بالامتحان لا تسمح بطلب العذر ({exam_registration.get_attendance_display()}).')

        # تعديل حالة الحظور للطالب الى غائب بعذر
        exam_registration.attendance = ExamAttendanceChoices.EXCUSED
        exam_registration.save()
        logger.info(f"تم تنفيذ غياب بعذر للطالب {student_batch.fk_student.full_name_ar}  في المادة {subject.name_ar}")

    except ValidationError as e:
        logger.warning(f"خطأ في التحقق عند تنفيذ خدمة غياب بعذر: {str(e)}")
        raise Exception(str(e))

    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تنفيذ خدمة غياب بعذر: {str(e)}")
        raise Exception(f"فشل تنفيذ خدمة غياب بعذر: {str(e)}")



#============================== school =======================================

@transaction.atomic 
def call_execute_book_distribution(action,request):
    """
     صرف الكتب وتحديث المخزون
    """
    instance = action.fk_request 
    student_batch = get_student_class(instance)
    
    current_year = get_current_year()

    inventories = SchoolInventory.objects.select_for_update().filter(
        fk_branch = student_batch.fk_branch,
        fk_year_of_study = current_year,
        fk_branch_class_subject__fk_branch_class = student_batch.fk_branch_class
    )
    if not inventories:
        raise ValidationException(_("لا توجد كتب مطابقة للصرف"))
    
    already_issued_ids = set(
        StudentBook.objects.filter(
            fk_student_class = student_batch,
            fk_inventory_id__in = inventories,
            operation_type =TYPE_CHOICES.DISBURSE
        ).values_list("fk_inventory_id",flat=True)
    )   

    new_records = [] 
    issued = [] 
    
    for inventorie in inventories:
        if inventorie.id in already_issued_ids:
            raise ValidationException(_(" تم صرف هذا الكتاب مسبقا للطالب"))
        
        if inventorie.available_quantity < 1 :
            raise ValidationException(f"الكتاب {inventorie.fk_branch_class_subject.fk_subject.name_ar}  غير متوفره للصرف")

        inventorie.available_quantity -=1
        inventorie.save(update_fields=["available_quantity"])

        new_records.append(
            StudentBook(
                fk_student_class = student_batch,
                fk_inventory = inventorie,
                quantity = 1,
                operation_type = TYPE_CHOICES.DISBURSE
            )
        )
        issued.append(inventorie.id)

    if new_records:
        StudentBook.objects.bulk_create(new_records)
        
    return {
        "issued":issued,
    }

@transaction.atomic 
def call_excute_uniform_payment(action,request):
    """
     التحقق المالي قبل صرف الزي
    """
    instance = action.fk_request 
    student_batch = get_student_class(instance)
    
    current_year = get_current_year()

    inventories = UniformInventory.objects.select_for_update().filter(
        fk_branch = student_batch.fk_branch,
        fk_year_of_study = current_year,
        gender = student_batch.fk_student.gender,
    )
    if not inventories:
        raise ValidationException(_("لا توجد زي مطابقة للصرف"))
    
    already_issued_ids = set(
        UniformOperation.objects.filter(
            fk_student_class = student_batch,
            fk_uniform_id__in = inventories,
            operation_type =OperationTypeChoice.FIRST_ISSUE
        ).values_list("fk_uniform_id",flat=True)
    )

    new_operations = [] 
    issued = [] 
    
    for inventorie in inventories:
        if inventorie.id in already_issued_ids:
            # continue
            raise ValidationException(_(" تم صرف هذا الزي مسبقا للطالب"))
        if inventorie.available_quantity < 1 :
            raise ValidationException(f"الزي {inventorie.uniform_name}  غير متوفره للصرف")
        
        inventorie.available_quantity -=1
        inventorie.save(update_fields=["available_quantity"])
        quantity = 1
        total_amount = inventorie.unit_price * quantity

        new_operations.append(
            UniformOperation(
            fk_student_class = student_batch,
            fk_uniform = inventorie,
            quantity = 1,
            operation_type = OperationTypeChoice.FIRST_ISSUE,
            unit_price_at_time = inventorie.unit_price,
            total_amount = total_amount,
            paid_amount = 0,
            remaining_amount = total_amount 
            )
        )
        issued.append(inventorie.id)

    if new_operations:
        UniformOperation.objects.bulk_create(new_operations)
        
    return {
        "issued":issued,
    }

def call_excute_uniform_delivery(action,request):
    """
    تسليم الزي للطالب
    """
    instance = action.fk_request 
    student_batch = get_student_class(instance)
    
    current_year = get_current_year()
    version_data = instance.version_data
    size = version_data.get("Size_choice")
    if not size:
        raise ValidationException("لم يتم تحديد المقاس")
    
    inventory = UniformInventory.objects.filter(
        fk_branch = student_batch.fk_branch,
        fk_year_of_study = current_year,
        gender = student_batch.fk_student.gender,
        size = size
    ).first()

    if not inventory:
        raise ValidationException("لا يوجد زي مطابق")
    
    operation = UniformOperation.objects.filter(
        fk_student_class = student_batch,
        fk_uniform = inventory,
        operation_type = OperationTypeChoice.FIRST_ISSUE        
    ).first()
    if not operation:
        raise ValidationException("لم يتم صرف هذا المقاس للطالب مسبقا")
    
    if getattr(operation,'delivered',False):
        raise ValidationException("لم يتم تسليم هذا المقاس للطالب مسبقا")
    
    operation.delivered = True 
    operation.delivered_at = timezone.now()
    operation.save(update_fields=['delivered','delivered_at'])
    return {
        "success":True,
        "message":f"تم تسليم {inventory.uniform_name} - {size} للطالب بنجاح"
    }

@transaction.atomic
def call_execute_create_new_students(action,request)-> Dict[str,Any]:
    """
     تنفيذ إدخال الطلاب المستجدين
    """
    instance = action.fk_request 
    version_data =instance.version_data if isinstance(instance.version_data, dict) else {}
    import json 
    if isinstance(instance.version_data,str):
        try:
            version_data = json.load(instance.version_data)
        except Exception:
            version_data ={}
    elif isinstance(instance.version_data,dict):
            version_data = instance.version_data
    else:
        version_data ={}

    if not version_data:
        raise ValidationException( _("لا توجد بيانات طلاب"))
    identity_numbers = set()
    country_ids = set()
    directorate_ids = set()

    if version_data.get('fk_parent__identity_number'):
        identity_numbers.add(version_data['fk_parent__identity_number'])
    if version_data.get('nationality'):
        country_ids.add(version_data['nationality'])
    if version_data.get('fk_country'):
        country_ids.add(version_data['fk_country'])
    if version_data.get('fk_directorate'):
        directorate_ids.add(version_data['fk_directorate'])
   
    parents_map = {
        obj.id : obj 
        for obj in Guardian.objects.filter(identity_number__in=identity_numbers)
    }
    countries_map = {
        obj.id : obj 
        for obj in Country.objects.filter(id__in=country_ids)
    }
    directorates_map = {
        obj.id : obj 
        for obj in Directorate.objects.filter(id__in=directorate_ids)
    }
   
    branch_class_id = version_data.get("branch_class_set__fk_branch_class")
    if not branch_class_id:
        return {"success":False,"message":"لم يتم تحديد الصف "}
    
    branch_class = BranchClass.objects.filter(id=branch_class_id).first()
    if not branch_class:
        return {"success":False,"message":"الصف غير موجود "}
    registration_year = get_current_year() 
    students_to_create = []
    guardians_to_create = []

    identity_number = version_data.get('fk_parent__identity_number')
    if identity_number and identity_number not in parents_map:
        if identity_number and identity_number not in parents_map:
            guardian = Guardian(
               name = version_data.get("fk_parent__name") ,
               identity_type = version_data.get("fk_parent__identity_type") ,
               identity_number = version_data.get("fk_parent__identity_number") ,
               phone_number = version_data.get("fk_parent__phone_number") ,
               fk_branch = request.user.fk_organization,
            )
            guardians_to_create.append(guardian)
            parents_map[identity_number] = guardian
        
    if guardians_to_create:
        Guardian.objects.bulk_create(guardians_to_create)

        created_guardians = Guardian.objects.filter(
            identity_number__in = [g.identity_number for g in guardians_to_create]
        )
        for g in created_guardians:
            parents_map[g.identity_number] = g
    # for data in version_data:
    student = Student.objects.create(
        fk_parent=parents_map.get(version_data.get('fk_parent__identity_number')) ,
        name_ar = version_data['name_ar'],
        gender = version_data['gender'],
        birthdate = version_data['student_age'],
        nationality = countries_map.get(version_data.get('nationality')),
        fk_country = countries_map.get(version_data.get('fk_country')),
        fk_directorate = directorates_map.get(version_data.get('fk_directorate')),
        registration_date = registration_year
        )
            
    StudentClass.objects.create(
        fk_student=student,
        fk_branch_class=branch_class,
        fk_branch=request.user.fk_organization,
        fk_year_of_study = registration_year
    )
        
    
    try:
        return {
            'success': True,
            'created_students':len(students_to_create),
            'created_guardians':len(guardians_to_create),
            'message': "تم إدخال الطلاب المستجدين بنجاح"
        }
   
    except IntegrityError as e:
        return {
            'success': False,
            "message":str(e)
        }

def call_confirm_student_registration(action,request):
    """
     التسجيل للعام الجديد
    """

    try:
        instance = action.fk_request 
        student_batch = get_student_class(instance)
        student = student_batch.fk_student 

        current_year = get_current_year()

        student_class = StudentClass.objects.select_for_update().filter(
            fk_student = student,
            fk_year_of_study = current_year,
        ).first()
        if not student_class:
            raise ValidationException("لا يوجد طلاب للسنه الدراسية الحالية")
        
        if student_class.registration_mode is True:
            raise ValidationException("تم تأكيد تسجيل الطالب مسبقا")
        
        if student_class.study_mode in [
            StudyModeChoice.STAGE_GRADUATED,
            StudyModeChoice.GRADUATED
        ]:
          raise ValidationException("لا يمكن تأكيد تسجيل طالب متخرج")
        
        student_class.registration_mode = True
        student_class.save(update_fields=['registration_mode'])

        return True
    except ValidationError as e:
        logger.warning(f"خطأ في تأكيد التسجيل: {str(e)}")
        raise Exception(str(e))
    except Exception as e:
        logger.error(f"خطأ غير متوقع في تأكيد التسجيل: {str(e)}")
        raise Exception(f"فشل تنفيذ تأكيد التسجيل: {str(e)}")

def call_excute_request_transfer(action,request):
    """
       تنفيذ طلب نقل طالب من المدرسة الحالية
    """
    try:
        instance = action.fk_request 
        version_data = instance.version_data
        student_batch = get_student_class(instance)
        student = student_batch.fk_student 

        current_year = get_current_year()

        to_branch_id = version_data.get("org_school_by_directorate")
        reason = version_data.get('transfer_reason')

        if not student or not to_branch_id:
            return {"success":False,"message":"بيانات النقل غير مكتملة"}

        student_class = StudentClass.objects.select_related("fk_student").get(
            fk_student = student,
            fk_year_of_study = current_year,
        )
        
        student_class.study_mode = StudyModeChoice.TRANSFERABLE
        student_class.save(update_fields=['study_mode'])
        to_branch =Organization.objects.get(id=to_branch_id)
        SchoolTransfer.objects.create(
            fk_student_class = student_class,
            fk_from_branch = student_class.fk_branch,
            fk_to_branch = to_branch,
            reason = reason
        )
        
        return True
    except ValidationError as e:
        logger.warning(f"Transfer request error: {str(e)}")
        raise Exception(str(e))

def call_excute_approve_transfer(action,request):
    """
        موافقة المدرسة المستقبلة على نقل الطالب
    """
    try:
        instance = action.fk_request 
        version_data = instance.version_data

        transfer_id = version_data.get("transfer_id")

        transfer = SchoolTransfer.objects.select_related("fk_student_class").get(id = transfer_id)
        if transfer.status:
            raise ValidationException(_("تمت الموافقة على الطالب مسبقا"))
        
        transfer.statuse = True
        transfer.save(update_fields=['statuse'])

        student_class = StudentClass.objects.get(
            fk_student = transfer.fk_student_class
        )
        student_class.fk_branch = transfer.fk_to_branch
        student_class.study_mode = StudyModeChoice.CONTINUOUS
        
        return True
    except ValidationError as e:
        logger.warning(f"Transfer approval error: {str(e)}")
        raise Exception(str(e))
