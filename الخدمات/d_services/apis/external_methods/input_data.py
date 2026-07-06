# import logging
# from typing import Any, Dict
# from academic_affairs.models.Batch import Batch
# from academic_affairs.models.ClearingMaterials import ClearingMaterials
# from academic_affairs.models.Level import Level
# from academic_affairs.models.SemesterSubject import SemesterSubject
# from control.models.StudentsClearingMaterials import StudentsClearingMaterials
# from d_services.apis.external_methods.utils.helpers_methods import calculate_scaled_grade, find_equivalent_subject

# from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
# from system_management.choices.choices import LevelStudentStatusChoice, ResultStatusChoice, StudentsClearingMaterialsChoice
# from system_management.models.Specialization import Specialization

# logger = logging.getLogger(__name__)
# from django.db.models import Sum

# from student_affairs.models.StudentBatch import StudentBatch
# from student_affairs.models.StudentCourse import StudentLevel, StudentSemester
# from d_services.choices.choices import PaymentStatusChoice
# from system_management.choices.choices import AcademicStatusChoice, StudentStatusChoice

# def call_get_statement_form_data(instance, request):
#     """بيان بالدرجات لغير الخريجيين"""
#     service_request = instance
#     service_version = service_request.version_data
#     student_batch = StudentBatch.objects.get(id=service_request.target_audience_data['fk_student_batch'])
#     student = student_batch.fk_student
#     student_levels = StudentLevel.objects.filter(
#         fk_student_batch__fk_student=student,
#         fk_student_batch=student_batch,
#         semester_set__subjects__isnull=False
#     ).distinct().order_by("fk_level__level")

#     total_levels = student_levels.aggregate(total_levels=Sum("total_grade"))["total_levels"] or 0
#     avg_levels = student_levels.aggregate(avg_levels=Sum("avg"))["avg_levels"] or 0

#     active_level = StudentLevel.objects.filter(fk_student_batch=student_batch, is_active=True).first()
#     active_semester = StudentSemester.objects.filter(fk_student_level=active_level, is_active=True).first()

#     return {
#         "student_name_ar": student_batch.fk_student.full_name_ar,
#         "student_name_en": student_batch.fk_student.full_name_en,
#         "college_name_ar": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
#         "college_name_en": student_batch.fk_batch.fk_specialization.fk_college.name_en,
#         "section_name_ar": student_batch.fk_batch.fk_specialization.fk_section.name_ar,
#         "section_name_en": student_batch.fk_batch.fk_specialization.fk_section.name_en,
#         "student_level_name": active_level.fk_level.get_level_display() if active_level and active_level.fk_level else None,
#         "student_semester_name": active_semester.fk_semester.get_name_display() if active_semester and active_semester.fk_semester else None,
#         "academic_year_h": student_batch.fk_academic_year.year_h,
#         "academic_year_m": student_batch.fk_academic_year.year_m,
#         "student_academic_no": student_batch.academic_no,
#         "total_levels": total_levels,
#         "avg_levels": avg_levels,
#         "service_version": service_version,
#         "target_audience_data": instance.target_audience_data,
#         "base_component_data": instance.base_component_data,
#         "payment_status": PaymentStatusChoice(instance.payment_status).label,
#         "amount_paid": instance.amount_paid,
#         "remaining_amount": instance.remaining_amount,
#         "total_fee": instance.total_fee,
#         "specialization_name_ar": student_batch.fk_batch.fk_specialization.name_ar,
#         "specialization_name_en": student_batch.fk_batch.fk_specialization.name_en,
#         "organization_ar": student_batch.fk_batch.fk_specialization.fk_college.fk_branch.name_ar,
#         "organization_en": student_batch.fk_batch.fk_specialization.fk_college.fk_branch.name_en,
#         "nationality_name_ar": student_batch.fk_student.fk_nationality.nationality_name_ar if student_batch.fk_student.fk_nationality else None,
#         "nationality_name_en": student_batch.fk_student.fk_nationality.nationality_name_en if student_batch.fk_student.fk_nationality else None,
#         "date_of_birth": student_batch.fk_student.date_of_birth,
#         "enrollment_year_year_h": student_batch.fk_student.fk_enrollment_year.year_h if student_batch.fk_student.fk_enrollment_year else None,
#         "enrollment_year_year_m": student_batch.fk_student.fk_enrollment_year.year_m if student_batch.fk_student.fk_enrollment_year else None,
#         "accademic_status": AcademicStatusChoice(student_batch.accademic_status).label,
#         "student_status": StudentStatusChoice(student_batch.student_status).label,
#     }


# def call_get_payment_input_data(instance, request) -> Dict[str, Any]:
#     """
#     جلب بيانات  استمارة رقم الحافظة
#     """
#     import random
    
#     service_request = instance.fk_request
    
#     # توليد رقم رقم حافظه
#     random_number = random.randint(10000000, 99999999)
    
#     # الحصول على صورة مقدم الطلب
#     requester_image = None
#     if service_request.requester_image:
#         requester_image = service_request.requester_image.url
    
#     return {
#         'requested_at': str(service_request.requested_at),
#         'requester_image': requester_image,
#         'requester_name': service_request.requester_name,
#         'requester_description': service_request.requester_description,
#         'requester_id': service_request.requester_id,
#         'total_fee': float(service_request.total_fee or 0),
#         'amount_paid': float(service_request.amount_paid or 0),
#         'request_number': service_request.request_number,
#         'random_number': str(random_number),
#     }


# def call_get_transfer_form_data(instance, request):
#     """بيانات مدخل استمارة المقاصه الداخلية"""
#     service_request = instance
#     service_version = service_request.fk_service_version

#     try:
#         """
#         تجهيز جدول معاينة المقاصة للطالب قبل التنفيذ:
#         - يعرض المواد المكتملة والمقاصة لها
#         - يعرض الدرجات بعد المقاصة
#         - يحدد أهلية الطالب للمقاصة حسب المواد الراسبة
#         """
#         results = {
#             'table_data': [], 
#             'failed_subjects_count': 0, 
#             'allowed_failure_subjects': 0, 
#             'is_eligible': True, 
#             'error': None
#         }

#         # جلب مستوى الطالب مع علاقاته
#         sl = StudentLevel.objects.select_related('fk_student_batch__fk_batch__fk_specialization', 'fk_student_batch__fk_student', 'fk_level').get(pk=service_request.target_audience_data['fk_student_level'])
#         student = sl.fk_student_batch.fk_student
#         old_spec = sl.fk_student_batch.fk_batch.fk_specialization
#         new_specialization = Specialization.objects.filter(id=1).first()
        
#         # جلب أحدث دفعة للتخصص الجديد
#         new_batch = Batch.objects.filter(fk_specialization=new_specialization).order_by('-id').first()
#         if not new_batch: 
#             return {**results, 'error': "لا توجد دفعات مسجلة للتخصص الجديد"}

#         # ==========================
#         # التحقق من أهلية المقاصة
#         # ==========================
#         failed_count = StudentSubject.objects.filter(
#             fk_student_semester__fk_student_level=sl,
#             results_status__in=[
#                 ResultStatusChoice.REMAINING, 
#                 ResultStatusChoice.ABSENCE, 
#                 ResultStatusChoice.DEPRIVATION
#             ]
#         ).count()
#         results.update({
#             'failed_subjects_count': failed_count,
#             'allowed_failure_subjects': sl.fk_level.allowed_failure_subjects,
#             'is_eligible': failed_count <= sl.fk_level.allowed_failure_subjects
#         })

#         # ==========================
#         # تجهيز بيانات البحث للمواد الجديدة
#         # ==========================
#         new_subs = SemesterSubject.objects.filter(
#             fk_semester__fk_level__fk_batch=new_batch
#         ).select_related('fk_subject', 'fk_grading_system_june')

#         subs_by_code = {s.fk_subject.subject_code.strip().lower(): s for s in new_subs if s.fk_subject.subject_code}
#         subs_by_name = {}
#         for s in new_subs:
#             if s.fk_subject.name_ar: 
#                 subs_by_name[s.fk_subject.name_ar.strip().lower()] = s
#             if s.fk_subject.name_en: 
#                 subs_by_name[s.fk_subject.name_en.strip().lower()] = s

#         # ==========================
#         # معالجة المواد القديمة
#         # ==========================
#         processed = set()
#         old_levels = StudentLevel.objects.filter(
#             fk_student_batch__fk_student=student, 
#             fk_student_batch__fk_batch__fk_specialization=old_spec
#         ).order_by('fk_level__level')
        
#         for level in old_levels:
#             for ss in StudentSemester.objects.filter(fk_student_level=level).prefetch_related('subjects__fk_semmester_subject__fk_subject', 'subjects__fk_semmester_subject__fk_grading_system_june'):
#                 for subj in ss.subjects.all():
#                     old_ss = subj.fk_semmester_subject
#                     if old_ss.id in processed: 
#                         continue
#                     processed.add(old_ss.id)

#                     # فقط المواد الناجحة أو المقاصة سابقًا
#                     if subj.results_status not in [ResultStatusChoice.PASSED, ResultStatusChoice.CLEARANCE]: 
#                         continue

#                     # البحث عن المقاصة الرسمية
#                     target = ClearingMaterials.objects.filter(
#                         fk_semester_subject_from=old_ss, active=True, 
#                         fk_semester_subject_to__fk_semester__fk_level__fk_batch__fk_specialization=new_specialization
#                     ).select_related('fk_semester_subject_to__fk_subject', 'fk_semester_subject_to__fk_grading_system_june').first()
                    
#                     # إذا لم توجد، البحث عن مادة معادلة
#                     target_ss = target.fk_semester_subject_to if target else find_equivalent_subject(old_ss.fk_subject, subs_by_code, subs_by_name)
                    
#                     if target_ss:
#                         grade = calculate_scaled_grade(
#                             subj.total_grade, 
#                             old_ss.fk_grading_system_june.grade_total, 
#                             target_ss.fk_grading_system_june.grade_total
#                         )
#                         results['table_data'].append({
#                             'completed_subject': old_ss.fk_subject.name_ar, 
#                             'equivalent_subject': target_ss.fk_subject.name_ar, 
#                             'grade': grade
#                         })
#         return results
#     except Exception as e:
#         return {**results, 'error': str(e)}





import datetime
import logging
from typing import Any, Dict
from academic_affairs.models.Batch import Batch
from academic_affairs.models.ClearingMaterials import ClearingMaterials
from academic_affairs.models.Level import Level
from academic_affairs.models.Period4Schedule import Period4Schedule
from academic_affairs.models.SemesterSubject import SemesterSubject
from control.models.StudentsClearingMaterials import InternalClearance, StudentsClearingMaterials
from d_services.apis.external_methods.execution import execute_internal_clearance
from d_services.apis.external_methods.utils.helpers_methods import calculate_and_update_levels, calculate_scaled_grade, create_student_semesters, find_equivalent_subject, get_specialization_and_parents_ids, \
    get_student_batch, process_clearance_materials, get_student_level
from exam.models.ExamRegistration import ExamRegistration
from portals.students.models.student_academic import StudentAcademic

from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
from system_management.choices.choices import ExamAttendanceChoices, ExamTypeChoices, LevelStudentStatusChoice, ResultStatusChoice, StudentsClearingMaterialsChoice,SemesterStudentStatusChoice
from system_management.models.Specialization import Specialization

logger = logging.getLogger(__name__)
from django.db.models import Sum
from control.get_number_text import number_to_arabic_text


from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel, StudentSemester
from d_services.choices.choices import PaymentStatusChoice
from system_management.choices.choices import AcademicStatusChoice, StudentStatusChoice

def call_get_statement_form_data(instance, request):
    """بيان بالدرجات لغير الخريجيين"""
    service_request = instance
    service_version = service_request.version_data
    student_batch = StudentBatch.objects.get(id=service_request.target_audience_data['fk_student_batch'])
    student = student_batch.fk_student
    student_levels = StudentLevel.objects.filter(
        fk_student_batch__fk_student=student,
        fk_student_batch=student_batch,
        semester_set__subjects__isnull=False
    ).distinct().order_by("fk_level__level")

    total_levels = student_levels.aggregate(total_levels=Sum("total_grade"))["total_levels"] or 0
    avg_levels = student_levels.aggregate(avg_levels=Sum("avg"))["avg_levels"] or 0

    active_level = StudentLevel.objects.filter(fk_student_batch=student_batch, is_active=True).first()
    active_semester = StudentSemester.objects.filter(fk_student_level=active_level, is_active=True).first()

    return {
        "student_name_ar": student_batch.fk_student.full_name_ar,
        "student_name_en": student_batch.fk_student.full_name_en,
        "college_name_ar": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
        "college_name_en": student_batch.fk_batch.fk_specialization.fk_college.name_en,
        "section_name_ar": student_batch.fk_batch.fk_specialization.fk_section.name_ar,
        "section_name_en": student_batch.fk_batch.fk_specialization.fk_section.name_en,
        "student_level_name": active_level.fk_level.get_level_display() if active_level and active_level.fk_level else None,
        "student_semester_name": active_semester.fk_semester.get_name_display() if active_semester and active_semester.fk_semester else None,
        "academic_year_h": student_batch.fk_academic_year.year_h,
        "academic_year_m": student_batch.fk_academic_year.year_m,
        "student_academice_no": student_batch.fk_student.academice_no,
        "total_levels": total_levels,
        "avg_levels": avg_levels,
        "service_version": service_version,
        "target_audience_data": instance.target_audience_data,
        "base_component_data": instance.base_component_data,
        "payment_status": PaymentStatusChoice(instance.payment_status).label,
        "amount_paid": instance.amount_paid,
        "remaining_amount": instance.remaining_amount,
        "total_fee": instance.total_fee,
        "specialization_name_ar": student_batch.fk_batch.fk_specialization.name_ar,
        "specialization_name_en": student_batch.fk_batch.fk_specialization.name_en,
        "organization_ar": student_batch.fk_batch.fk_specialization.fk_college.fk_branch.name_ar,
        "organization_en": student_batch.fk_batch.fk_specialization.fk_college.fk_branch.name_en,
        "nationality_name_ar": student_batch.fk_student.fk_nationality.nationality_name_ar if student_batch.fk_student.fk_nationality else None,
        "nationality_name_en": student_batch.fk_student.fk_nationality.nationality_name_en if student_batch.fk_student.fk_nationality else None,
        "date_of_birth": student_batch.fk_student.date_of_birth,
        "enrollment_year_year_h": student_batch.fk_student.fk_enrollment_year.year_h if student_batch.fk_student.fk_enrollment_year else None,
        "enrollment_year_year_m": student_batch.fk_student.fk_enrollment_year.year_m if student_batch.fk_student.fk_enrollment_year else None,
        "accademic_status": AcademicStatusChoice(student_batch.accademic_status).label,
        "student_status": StudentStatusChoice(student_batch.student_status).label,
    }

def call_get_erp_invoice_data_for_student_batch(instance,request)-> Dict[str, Any]:
    """جلب بيانات الفاتورة لنظام الـ ERP اعتمادا على سجل الدفعة للطالب"""
    instance = instance.fk_request
    student_batch = get_student_batch(instance)
    student = student_batch.fk_student
    grant_source = instance.fk_grant_source
    return {

    }

def call_get_erp_invoice_data_for_student_level(instance,request)-> Dict[str, Any]:
    """جلب بيانات الفاتورة لنظام الـ ERP اعتمادا على سجل المستوى للطالب"""
    instance = instance.fk_request
    student_level = get_student_level(instance)
    student_batch = student_level.fk_student_batch
    student = student_batch.fk_student
    grant_source = instance.fk_grant_source

    return {

    }



def call_get_payment_input_data(instance, request) -> Dict[str, Any]:
    """
    جلب بيانات  استمارة رقم الحافظة
    """
    import random
    
    service_request = instance.fk_request
    college_name = None
    specialization_name = None
    academic_number = None
    try:
        student_batch = get_student_batch(instance.fk_request)
        batch = student_batch.fk_batch
        college_name = batch.fk_specialization.fk_college.name_ar
        specialization_name = batch.fk_specialization.name_ar
        academic_number = student_batch.academic_no
    except Exception as e:
        print(str(e),'=============')

    
    # توليد رقم رقم حافظه
    random_number = random.randint(10000000, 99999999)
    
    # الحصول على صورة مقدم الطلب
    requester_image = None
    if service_request.requester_image:
        requester_image = service_request.requester_image.url
    
    return {
        'requested_at': str(service_request.requested_at),
        'requester_image': requester_image,
        'requester_name': service_request.requester_name,
        'requester_description': service_request.requester_description,
        'requester_id': service_request.requester_id,
        'total_fee': float(service_request.total_fee or 0),
        'amount_paid': float(service_request.amount_paid or 0),
        'request_number': service_request.request_number,
        'random_number': str(random_number),
        'discounted_fee':service_request.discounted_fee,
        'service_name': service_request.fk_service.name_ar,
        'college_name': college_name,
        'specialization_name': specialization_name,
        'academic_number': academic_number,
        'service_category': service_request.fk_service.get_category_display(),
    }


def call_get_transfer_form_data(instance, request):
    """بيانات مدخل استمارة المقاصه الداخلية"""
    service_request = instance
    service_version = service_request.fk_service_version

    try:
        """
        تجهيز جدول معاينة المقاصة للطالب قبل التنفيذ:
        - يعرض المواد المكتملة والمقاصة لها
        - يعرض الدرجات بعد المقاصة
        - يحدد أهلية الطالب للمقاصة حسب المواد الراسبة
        """
        target_audience_data = instance.target_audience_data if isinstance(instance.target_audience_data, dict) else {}
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        fk_student_level = target_audience_data.get('fk_student_level')
        student_level = StudentLevel.objects.get(id=fk_student_level)
        student_batch = student_level.fk_student_batch
        student = student_batch.fk_student
        fk_new_specialization = version_data.get('fk_new_specialization')
        new_specialization = Specialization.objects.get(id=fk_new_specialization)
        old_specialization = student_batch.fk_batch.fk_specialization
        results = {
            'student_name': student.full_name_ar,
            'academic_no': student_batch.academic_no,
            'avg': student_level.avg,
            'total_grade':student_level.total_grade,
            'estimate':student_level.get_estimate_display(),
            'old_specialization':old_specialization.name_ar,
            'old_section':old_specialization.fk_section.name_ar,
            'old_college':old_specialization.fk_college.name_ar,
            'new_specialization':new_specialization.name_ar,
            'new_section':new_specialization.fk_section.name_ar,
            'new_college':new_specialization.fk_college.name_ar,
            'issue_date':datetime.date.today(),
            'current_level':student_level.fk_level.get_level_display(),
            'table_data': [],
            'failed_subjects_count': 0,
            'allowed_failure_subjects': 0,
            'is_eligible': True,
            'error': None
        }


        # جلب مستوى الطالب مع علاقاته
        student_level = StudentLevel.objects.select_related('fk_student_batch__fk_batch__fk_specialization', 'fk_student_batch__fk_student', 'fk_level').get(pk=fk_student_level)
        student = student_level.fk_student_batch.fk_student
        old_spec = student_level.fk_student_batch.fk_batch.fk_specialization
        new_specialization_id = version_data.get('fk_new_specialization')
        new_specialization_obj = Specialization.objects.get(id=new_specialization_id)
        # جلب أحدث دفعة للتخصص الجديد
        new_batch = Batch.objects.filter(fk_specialization=new_specialization_obj).order_by('-id').first()
        if not new_batch:
            return {**results, 'error': "لا توجد دفعات مسجلة للتخصص الجديد"}

        # ==========================
        # التحقق من أهلية المقاصة
        # ==========================

        failed_count = StudentSubject.objects.filter(
            fk_student_semester__fk_student_level=student_level,
            results_status__in=[
                ResultStatusChoice.REMAINING,
                ResultStatusChoice.ABSENCE,
                ResultStatusChoice.DEPRIVATION
            ]
        ).count()
        results.update({
            'failed_subjects_count': failed_count,
            'allowed_failure_subjects': student_level.fk_level.allowed_failure_subjects,
            'is_eligible': failed_count <= student_level.fk_level.allowed_failure_subjects
        })

        # ==========================
        # تجهيز بيانات البحث للمواد الجديدة
        # ==========================

        new_subs = SemesterSubject.objects.filter(
            fk_semester__fk_level__fk_batch=new_batch
        ).select_related('fk_subject', 'fk_grading_system_june')

        subs_by_code = {s.fk_subject.subject_code.strip().lower(): s for s in new_subs if s.fk_subject.subject_code}
        subs_by_name = {}
        for s in new_subs:
            if s.fk_subject.name_ar:
                subs_by_name[s.fk_subject.name_ar.strip().lower()] = s
            if s.fk_subject.name_en:
                subs_by_name[s.fk_subject.name_en.strip().lower()] = s

        # ==========================
        # معالجة المواد القديمة
        # ==========================
        processed = set()
        specializations_ids = get_specialization_and_parents_ids(old_spec.id)

        old_levels = StudentLevel.objects.filter(fk_student_batch__fk_student=student,fk_student_batch__fk_batch__fk_specialization_id__in=specializations_ids
        ).exclude(student_level_status__in=[LevelStudentStatusChoice.UNDER_REVIEW,LevelStudentStatusChoice.REGISTERED_FOR_REPEAT]).order_by('fk_level__level')

        for level in old_levels:
            for ss in StudentSemester.objects.filter(fk_student_level=level).prefetch_related('subjects__fk_semmester_subject__fk_subject', 'subjects__fk_semmester_subject__fk_grading_system_june'):
                for subj in ss.subjects.all():
                    old_ss = subj.fk_semmester_subject
                    if old_ss.id in processed:
                        continue
                    processed.add(old_ss.id)
                    # فقط المواد الناجحة أو المقاصة سابقًا
                    if subj.results_status == ResultStatusChoice.PENDING or subj.results_status == None:
                    # if subj.results_status not in [ResultStatusChoice.PASSED, ResultStatusChoice.CLEARANCE, ResultStatusChoice.REMAINING]:
                        continue

                    # البحث عن المقاصة الرسمية
                    target = ClearingMaterials.objects.filter(
                        fk_semester_subject_from=old_ss, active=True,
                        fk_semester_subject_to__fk_semester__fk_level__fk_batch__fk_specialization=new_specialization_obj
                    ).select_related('fk_semester_subject_to__fk_subject', 'fk_semester_subject_to__fk_grading_system_june').first()

                    # إذا لم توجد، البحث عن مادة معادلة
                    target_ss = target.fk_semester_subject_to if target else find_equivalent_subject(old_ss.fk_subject, subs_by_code, subs_by_name)

                    if target_ss:
                        grade = calculate_scaled_grade(
                            subj.total_grade,
                            old_ss.fk_grading_system_june.grade_total,
                            target_ss.fk_grading_system_june.grade_total
                        )
                        results['table_data'].append({
                            'completed_subject': old_ss.fk_subject.name_ar,
                            'equivalent_subject': target_ss.fk_subject.name_ar,
                            'grade': grade
                        })
        # print('ddddddddddddddddssssssssssssssssssssssssssssssssssssssfares')
        # print(service_request,type(service_request))
        # internal = InternalClearance.objects.filter(fk_request=service_request).first()
        # student_levels = {}
        # for sl in StudentLevel.objects.filter(fk_student_batch=internal.fk_student_batch_new):
        #     student_levels[sl.fk_level.id] = sl
        # # calculate_and_update_levels(student_levels)
        # execute_internal_clearance(internal,request)
        # materials = StudentsClearingMaterials.objects.select_related(
        # 'fk_semester_subject_from',
        # 'fk_semester_subject_to__fk_grading_system_june',
        # 'fk_semester_subject_to__fk_semester__fk_level'
        # ).filter(
        #     fk_internal_clearance=internal,
        #     # process_status=ProcessStatusChoices.APPROVED
        # )
        # student_semesters = create_student_semesters(student_levels)
        # process_clearance_materials(materials,internal.fk_student_batch_old,internal.fk_student_batch_new,student_levels,student_semesters)
        return results
    except Exception as e:
        print(str(e),'============')
        return {**results, 'error': str(e)}



def call_enrollment_certificate_form_data(instance, request):
    """
    جلب بيانات استمارة شهادة القيد الدراسي
    """
    try:
        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if instance.version_data else {}
        student_batch = get_student_batch(instance)
        batch = student_batch.fk_batch
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
            "enrollment_year": student.fk_enrollment_year.year_m if student.fk_enrollment_year else None,
            "current_academic_year": current_level.fk_academic_year.year_m if current_level else None,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}


def call_suspension_inrollment_form_data(instance, request):
    """
    جلب بيانات استمارة وقف القيد
    """
    try:

        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if instance.version_data else {}

        student_batch = get_student_batch(instance)
        batch = student_batch.fk_batch
        student = student_batch.fk_student
        current_student_level = student_batch.current_student_level
        current_level = current_student_level.fk_level if current_student_level else None
        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "nationality": student.fk_nationality.name_ar if student.fk_nationality else None,
            "date_of_birth": student.date_of_birth,
            "place_of_birth": student.place_of_brith,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": batch.fk_specialization.fk_college.name_ar if batch.fk_specialization else None,
            "specialization": batch.fk_specialization.name_ar if batch.fk_specialization else None,
            "level": current_level.get_level_display() if current_level else None,
            "period": version_data.get('period', None),
            "semester": version_data.get('fk_semester_name', None),
            "reason": version_data.get('reason', None),
            "current_academic_year": current_level.fk_academic_year.year_m if current_level else None,
            "date_today": datetime.date.today(),
            "return_date": version_data.get('return_date', None),
        }
    except Exception as e:
        print(e)
        return {}




def call_cancellation_suspension_inrollment_form_data(instance, request):
    """
    جلب بيانات استمارة الغاء وقف القيد
    """
    try:
        from .execution import call_execute_cancellation_suspension_inrollment
        call_execute_cancellation_suspension_inrollment(instance, request)

        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if instance.version_data else {}
        fk_student_batch = target_audience_data.get('fk_student_batch')
        old_student_batch = get_student_batch(instance)
        suspended_level = old_student_batch.level_set.filter(student_level_status=LevelStudentStatusChoice.WITHDRAWN).last()



        if suspended_level:
            suspended_semester = suspended_level.semester_set.filter(student_semester_status=SemesterStudentStatusChoice.WITHDRAWN).last()
        else:
            suspended_semester = StudentSemester.objects.filter(fk_student_level__fk_student_batch=fk_student_batch, student_semester_status=SemesterStudentStatusChoice.WITHDRAWN).last()
            suspended_level = suspended_semester.fk_student_level if suspended_semester else None

        if suspended_level:
            new_batch = Level.objects.get(
                level=suspended_level.fk_level.level,
                is_current=True,
                fk_batch__fk_specialization=old_student_batch.fk_batch.fk_specialization,
            )
        else:
            new_batch = None
        student = old_student_batch.fk_student
        return {
            "student_name": student.full_name_ar,
            "student_id": old_student_batch.academic_no,
            "college": old_student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": old_student_batch.fk_batch.fk_specialization.name_ar,
            "level":  suspended_level.fk_level.get_level_display() if suspended_level else None,
            "semester": suspended_semester.fk_semester.get_name_display() if suspended_semester else None,
            "reason": version_data.get('reason', None),
            "old_batch": target_audience_data.get('fk_batch_name'),
            "new_batch": new_batch.fk_batch.batch_no if new_batch else None,
            "date_today": datetime.date.today(),
            "return_date": version_data.get('return_date', None),
        }
    except Exception as e:
        print(e)
        return {}


def call_student_withdrawal_form_data(instance, request):
    """
    جلب بيانات استمارة سحب ملف
    """
    try:
        target_audience_data = instance.target_audience_data
        student_batch = get_student_batch(instance)

        student = student_batch.fk_student
        student_level = student_batch.level_set.filter(fk_level__is_current=True).first()

        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "nationality": student.fk_nationality.name_ar if student.fk_nationality else None,
            "date_of_birth": student.date_of_birth,
            "place_of_birth": student.place_of_brith,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "level": student_level.fk_level.get_level_display() if student_level else None,
            "enrollment_year": student.fk_enrollment_year.year_m,
            "current_academic_year": student_batch.fk_batch.batch_no,
            "issue_date": datetime.date.today(),
        }
    except:
        return {}



def call_retake_subject_form_data(instance, request):
    """
    جلب بيانات استمارة إعادة مادة
    """
    try:

        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        current_level = student_batch.level_set.filter(fk_level__is_current=True).first()
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        target_audience_data = instance.target_audience_data if isinstance(instance.target_audience_data, dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject', None)
        # fk_student_subject = version_data.get('fk_student_subject', None)
        student_subject = StudentSubject.objects.select_related('fk_semmester_subject').get(id=fk_student_subject)
        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "nationality": student.fk_nationality.name_ar if student.fk_nationality else None,
            "date_of_birth": student.date_of_birth,
            "place_of_birth": student.place_of_brith,
            "subject_name": student_subject.fk_semmester_subject.fk_subject.name_ar if student_subject else None,
            "subject_code":student_subject.fk_semmester_subject.fk_subject.subject_code,
            "number_of_hours":student_subject.fk_semmester_subject.number_of_hours,
            "results_status_display":student_subject.get_results_status_display(),
            "estimate":student_subject.get_estimate_display(),
            "number_of_attendance":student_subject.number_of_attendance,
            "perparatoin_grade":student_subject.perparatoin_grade,
            "total_grade":student_subject.total_grade,
            "subject_level":student_subject.fk_semmester_subject.fk_semester.fk_level.get_level_display() if student_subject else None,
            "subject_semester":student_subject.fk_semmester_subject.fk_semester.get_name_display() if student_subject else None,
            "subject_academic_year":student_subject.fk_semmester_subject.fk_semester.fk_level.fk_academic_year.year_m,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "current_level": current_level.fk_level.get_level_display() if current_level else None,
            "enrollment_year": student.fk_enrollment_year.year_m if student.fk_enrollment_year else None,
            "current_academic_year": student_batch.fk_batch.batch_no,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}


def call_attendance_exemption_form_data(instance, request):
    """
    جلب بيانات استمارة اعفاء حظور
    """
    try:
        target_audience_data = instance.target_audience_data
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        periods = []
        fk_periods_4_schedule = version_data.get('fk_periods')
        if fk_periods_4_schedule:
            periods = Period4Schedule.objects.filter(id__in=fk_periods_4_schedule)
        from_date = version_data.get('from_date')
        to_date = version_data.get('to_date')
        current_student_level = student_batch.current_student_level
        current_student_semester = current_student_level.current_student_semester if current_student_level else None

        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "level": current_student_level.fk_level.get_level_display() if current_student_level else None,
            "semester":current_student_semester.fk_semester.get_name_display() if current_student_semester else None,
            "from_date": from_date,
            "to_date": to_date,
            "periods":[f'الفترة {number_to_arabic_text(period.order_no)}' for period in periods] if len(periods)>0 else None,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}


def call_clearance_form_data(instance, request):
    """
    جلب بيانات استمارة اخلاء طرف
    """
    try:
        target_audience_data = instance.target_audience_data
        student_batch = get_student_batch(instance)

        student = student_batch.fk_student
        student_level = student_batch.level_set.filter(is_active=True,fk_level__is_current=True).first()
        student_semester = student_level.semester_set.filter(is_active=True,fk_semester__is_current=True).first() if student_level else None

        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "nationality": student.fk_nationality.name_ar if student.fk_nationality else None,
            "date_of_birth": student.date_of_birth,
            "place_of_birth": student.place_of_brith,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "level": student_level.fk_level.get_level_display() if student_level else None,
            "enrollment_year": student.fk_enrollment_year.year_m,
            "current_academic_year": student_batch.fk_batch.batch_no,
            "issue_date": datetime.date.today(),
        }
    except:
        return {}

def call_grievance_course_grade_form_data(instance, request):
    """
    جلب بيانات استمارة تظلم على نتيجة مقرر
    """
    try:
        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if isinstance(instance.version_data,dict) else {}
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        fk_student_subject = target_audience_data.get('fk_student_subject')
        student_subject = StudentSubject.objects.get(id=fk_student_subject)
        student_level = student_batch.current_student_level
        semester = student_subject.fk_semmester_subject.fk_semester
        level = semester.fk_level if semester else None
        subject = student_subject.fk_semmester_subject.fk_subject

        subject_data = {
            'name_ar': subject.name_ar,
            'name_en': subject.name_en,
            'code': subject.subject_code,
            'total': str(student_subject.total_grade),
            'grades_records':[]
        }
        if student_subject:
            for grade in student_subject.grade_record.all():
                subject_data['grades_records'].append({
                    "grade": str(grade.grade),
                    "name": grade.fk_grade_distributiuon.fk_type_of_grade.name_ar,
                    'max_grade':str(grade.fk_grade_distributiuon.grade)
                })

        return {
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "service_name":instance.fk_service.name_ar,
            "student_name": student.full_name_ar,
            "academic_no": student_batch.academic_no,
            "current_academic_year": level.fk_academic_year.year_m if student_level else None,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "level": student_subject.fk_student_semester.fk_student_level.fk_level.get_level_display() if student_subject else None,
            "semester":student_subject.fk_student_semester.fk_semester.get_name_display() if student_subject else None,
            "subject_data": subject_data,
            "reason":version_data.get('notes'),
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}



def call_housing_form_data(instance, request):
    """
    جلب بيانات استمارة طلب سكن
    """
    pass

def call_replacement_id_card_form_data(instance, request):
    """
    جلب بيانات استمارة قطع بطاقة بدل فاقد
    """
    try:
        student_batch = get_student_batch(instance)
        batch = student_batch.fk_batch
        student = student_batch.fk_student
        current_student_level = student_batch.current_student_level
        batch_level = current_student_level.fk_level
        return {
            "student_id": student.id,
            "student_name": student.full_name_ar,
            "student_academic_no": student_batch.academic_no,
            "has_card": current_student_level.card_has_preinted,
            "level": batch_level.get_level_display(),
            "specialization_name_ar": batch.fk_specialization.name_ar,
            "academic_year_h": batch_level.fk_academic_year.year_h,
            "academic_year_m": batch_level.fk_academic_year.year_h,
            "branch_name_ar": batch.fk_specialization.fk_college.fk_branch.name_ar,
            "student_image": student.fk_user.image_user.url if hasattr(student.fk_user, 'image_user') else None,
            "collage_name_ar": batch.fk_specialization.fk_college.name_ar,
            'issue_date': datetime.date.today()
        }
    except Exception as e:
        print(e)
        return {}

def call_excused_absence_form_data(instance, request):
    """
    جلب بيانات استمارة غياب بعذر (امتحان)
    """
    try:
        student_batch = get_student_batch(instance)
        version_data = instance.version_data if isinstance(instance.version_data,dict) else {}
        target_audience_data = instance.version_data if isinstance(instance.target_audience_data,dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject')
        student_subject_exam = ExamRegistration.objects.filter(
            fk_student_subject=fk_student_subject,
            fk_exam_schedule__exam_type=ExamTypeChoices.FINAL,
            attendance__in=[ExamAttendanceChoices.ABSENCE, ExamAttendanceChoices.OTHER]
        ).last()
        student_subject = student_subject_exam.fk_student_subject
        subject = student_subject.fk_semmester_subject.fk_subject
        subject_semester = student_subject.fk_student_semester.fk_semester
        subject_level = subject_semester.fk_level
        student = student_batch.fk_student
        batch = student_batch.fk_batch
        exam_schedule = student_subject_exam.fk_exam_schedule

        return {
            "student_name": student.full_name_ar,
            "academic_no": student_batch.academic_no,
            "level": subject_level.get_level_display(),
            "semester":subject_semester.get_name_display(),
            "specialization_name_ar": batch.fk_specialization.name_ar,
            "academic_year_h": subject_level.fk_academic_year.year_h,
            "academic_year_m": subject_level.fk_academic_year.year_m,
            "attendance_date": exam_schedule.exam_date,
            "attendance_status":student_subject_exam.get_attendance_display(),
            "subject":subject.name_ar,
            "branch_name_ar": batch.fk_specialization.fk_college.fk_branch.name_ar,
            "collage_name_ar": batch.fk_specialization.fk_college.name_ar,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}




#============================== school =======================================

def call_get_statement_form_data(instance, request):
    """تسجيل الطلاب المستجدين"""
    service_request = instance
    service_version = service_request.version_data
    student_class = StudentAcademic.objects.get(id=service_request.name_ar)
    fk_org = student_class.fk_org
    student = student_class.fk_student
    guardian = student.guardian_relationships.first()
    guardian = guardian.fk_guardian if guardian else None
    branch_class = student_class.fk_study_program
    return {
            "student_name":student.name_ar,
            "academic_number":student.academic_no,
            "birthdate":student.birth_date,
            "gender":student.gender,
            "guardian_name":guardian.name,
            "guardian_phone":guardian.phone_number,
            "school_name":fk_org.name_ar,
            "district":fk_org.fk_parent_organization.name_ar,
            "governorate":fk_org.fk_parent_organization.fk_parent_organization.name_ar,
            "fk_branch_class":branch_class.name_ar,
        }