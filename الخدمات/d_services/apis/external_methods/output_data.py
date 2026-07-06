# """
# دوال بيانات المخرجات - Output Data Functions
# الدوال المستخدمة في حقول output_data_function و custom_output_function
# """
# import logging
# from typing import Any, Dict

# from django.db.models import Sum
# from academic_affairs.models.Batch import Batch
# from student_affairs.models.Student import Student

# from student_affairs.models.StudentBatch import StudentBatch
# from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
# from d_services.choices.choices import PaymentStatusChoice

# logger = logging.getLogger(__name__)

# from academic_affairs.models.Level import Level


# from academic_affairs.models.ClearingMaterials import ClearingMaterials
# from academic_affairs.models.SemesterSubject import SemesterSubject
# from control.models.StudentsClearingMaterials import StudentsClearingMaterials

# from system_management.choices.choices import AcademicStatusChoice, EstimateChoice, LevelStudentStatusChoice, ResultStatusChoice, StudentStatusChoice, StudentsClearingMaterialsChoice



# def call_get_status_statement_data(instance, request):
#     """مخرج بيان بالدرجات لغير الخريجيين"""
#     service_request = instance
#     service_version = service_request.version_data
#     student_batch = StudentBatch.objects.get(id=service_request.target_audience_data['fk_student_batch'])
#     student = student_batch.fk_student
#     student_levels = StudentLevel.objects.filter(
#         fk_student_batch__fk_student=student,
#         fk_student_batch__is_current=True,
#         semester_set__subjects__isnull=False
#     ).distinct().order_by("fk_level__level")
#     total_levels = student_levels.aggregate(total_levels=Sum("total_grade"))["total_levels"] or 0
#     avg_levels = student_levels.aggregate(avg_levels=Sum("avg"))["avg_levels"] or 0

#     levels = []
#     for student_level in student_levels:
#         level = {
#             "level_name": student_level.fk_level.get_level_display(),
#             "academic_year_year_h": student_level.fk_level.fk_academic_year.year_h,
#             "total_grade": student_level.total_grade,
#             "avg": student_level.avg,
#             "semesters": []
#         }
#         student_semesters = StudentSemester.objects.filter(fk_student_level=student_level).order_by('fk_semester__name')
#         for student_semester in student_semesters:
#             semester = {
#                 "name_ar": student_semester.fk_semester.get_name_display(),
#                 "total_grade": student_semester.total_grade,
#                 "avg": student_semester.avg,
#                 "subjects": []
#             }
#             semester["subjects"].append({
#                 "name_ar": student_semester.fk_semester.get_name_display(),
#                 "number_of_hours": "س-م",
#                 "grades": "الدرجة",
#                 "estimate": "التقدير"
#             })
#             student_subjects = StudentSubject.objects.filter(fk_student_semester=student_semester)
#             for student_subject in student_subjects:
#                 semester["subjects"].append({
#                     "name_ar": student_subject.fk_semmester_subject.fk_subject.name_ar,
#                     "number_of_hours": student_subject.fk_semmester_subject.number_of_hours,
#                     "grades": student_subject.total_grade,
#                     "estimate": student_subject.get_estimate_display()
#                 })
#             level['semesters'].append(semester)
#         levels.append(level)

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
#         "place_of_brith": {
#             "street": student_batch.fk_student.fk_place_of_brith.street,
#             "region": student_batch.fk_student.fk_place_of_brith.fk_region.name_ar if student_batch.fk_student.fk_place_of_brith.fk_region else None,
#             "governorate": student_batch.fk_student.fk_place_of_brith.fk_governorate.name_ar if student_batch.fk_student.fk_place_of_brith.fk_governorate else None,
#             "directorate": student_batch.fk_student.fk_place_of_brith.fk_directorate.name_ar if student_batch.fk_student.fk_place_of_brith.fk_directorate else None,
#             "country": student_batch.fk_student.fk_place_of_brith.fk_country.name_ar if student_batch.fk_student.fk_place_of_brith.fk_country else None,
#             "date_of_birth": student_batch.fk_student.date_of_birth,
#         } if student_batch.fk_student.fk_place_of_brith else {},
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
#         "levels": levels
#     }


# def call_get_payment_output_data(instance, request) -> Dict[str, Any]:
#     """
#     نموذج مصادقه الدفع(فاتوره) دالة جلب بيانات 
#     """
#     import random
    
#     service_request = instance.fk_request
    
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
#         'payment_status': PaymentStatusChoice(service_request.payment_status).label,
#         'payment_status_code': service_request.payment_status,
#         'request_number': service_request.request_number,
#         'remaining_amount': float(service_request.remaining_amount or 0),
#     }


# def call_clearance_preview(instance, request):
#     """جلب بيانات مخرج المقاصصة الداخلية"""
#     service_request = instance
#     service_version = service_request.fk_service_version
#     student_level = StudentLevel.objects.get(id=service_request.target_audience_data['fk_student_level'])
#     student = student_level.fk_student_batch.fk_student

#     """
#     تجهيز البيانات التفصيلية لكل فصل وموضوع بعد المقاصة.
#     - semesters: المواد المصنفة حسب الفصل والمستوى
#     - remaining_subjects: المواد المتبقية
#     - exempted_subjects: المواد المعفاة
#     """
#     try:
#         student = Student.objects.select_related('fk_current_specialization').get(pk=student.id)
#         new_batch = Batch.objects.filter(fk_specialization_id=1).order_by('-id').first()
#         # new_batch = Batch.objects.filter(fk_specialization_id=new_specialization_id).order_by('-id').first()
#         if not new_batch: 
#             return {'success': False, 'error': 'لا توجد دفعة للتخصص الجديد'}

#         # Fetch all subjects
#         sem_subjects = SemesterSubject.objects.filter(
#             fk_semester__fk_level__fk_batch=new_batch
#         ).select_related('fk_subject', 'fk_semester__fk_level').order_by(
#             'fk_semester__fk_level__level', 'fk_semester__name'
#         )
        
#         # Fetch clearance records
#         clearance_recs = StudentsClearingMaterials.objects.filter(
#             fk_student_batch_new__fk_student=student, 
#             fk_student_batch_new__fk_batch=new_batch
#         ).select_related('fk_semester_subject_to', 'fk_semester_subject_from__fk_subject')

#         # Map student subjects by semester_subject_id
#         student_subjects = StudentSubject.objects.filter(
#             fk_student_semester__fk_student_level__fk_student_batch__fk_student=student,
#             fk_student_semester__fk_student_level__fk_student_batch__fk_batch=new_batch
#         ).select_related('fk_semmester_subject')
#         ss_map = {ss.fk_semmester_subject_id: ss for ss in student_subjects}

#         # Process Clearance
#         cleared_map = {}
#         exempted_ids = set()
#         for rec in clearance_recs:
#             if not rec.fk_semester_subject_to: continue
#             tid = rec.fk_semester_subject_to.id
#             if rec.type == StudentsClearingMaterialsChoice.CLEARED:
#                 ss = ss_map.get(tid)
#                 cleared_map[tid] = {
#                     'old_subject_name': rec.fk_semester_subject_from.fk_subject.name_ar,
#                     'grade': ss.total_grade if ss else None,
#                     'hours': rec.fk_semester_subject_to.number_of_hours,
#                     'estimate': ss.get_estimate_display() if ss and ss.estimate else None
#                 }
#             elif rec.type == StudentsClearingMaterialsChoice.EXEMPTED:
#                 exempted_ids.add(tid)

#         # Build Response
#         semesters = {}
#         remaining, exempted = [], []
        
#         for ss in sem_subjects:
#             sem_id = ss.fk_semester.id
#             if sem_id not in semesters:
#                 semesters[sem_id] = {
#                     'semester_name': ss.fk_semester.get_name_display(), 
#                     'level': ss.fk_semester.fk_level.level, 
#                     'subjects': []
#                 }
            
#             info = cleared_map.get(ss.id)
#             is_exempt = ss.id in exempted_ids
            
#             if info:
#                 semesters[sem_id]['subjects'].append({
#                     'id': ss.id, 
#                     'name': ss.fk_subject.name_ar, 
#                     'hours': ss.number_of_hours, 
#                     'cleared_info': info, 
#                     'is_exempted': False
#                 })
#             elif is_exempt:
#                 exempted.append({'id': ss.id, 'name': ss.fk_subject.name_ar, 'hours': ss.number_of_hours})
#             else:
#                 remaining.append({'id': ss.id, 'name': ss.fk_subject.name_ar, 'hours': ss.number_of_hours})

#         return {
#             'success': True,
#             'student_info': {
#                 'name': student.full_name_ar,
#                 'old_specialization': StudentBatch.objects.filter(fk_student=student).first().fk_batch.fk_specialization.name_ar,
#                 'new_specialization': new_batch.fk_specialization.name_ar
#             },
#             'semesters': sorted(semesters.values(), key=lambda x: (x['level'], x['semester_name'])),
#             'remaining_subjects': remaining,
#             'exempted_subjects': exempted
#         }
#     except Exception as e: 
#         return {'success': False, 'error': str(e)}





"""
دوال بيانات المخرجات - Output Data Functions
الدوال المستخدمة في حقول output_data_function و custom_output_function
"""
import logging
from logging import raiseExceptions
from typing import Any, Dict

from django.db import transaction
from django.db.models import Sum
from ComponentFieldResolverGate import ComponentFieldResolverGate
from academic_affairs.models.Batch import Batch
from academic_affairs.models.Semester import Semester
from control.models.AppealGradeSubject import AppealGradeSubject
from exam.models.ExamRegistration import ExamRegistration
from portals.courses.models.Course import Course
from portals.grades.models.grade_detail_course import GradeDetailCourse
from portals.students.models.student_academic import StudentAcademic
from student_affairs.models.Student import Student

from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
from d_services.choices.choices import PaymentStatusChoice
from system_management.models.Specialization import Specialization
from django.db.models import OuterRef,Exists,F
logger = logging.getLogger(__name__)

from academic_affairs.models.Level import Level
import datetime

from academic_affairs.models.ClearingMaterials import ClearingMaterials
from academic_affairs.models.SemesterSubject import SemesterSubject
from control.models.StudentsClearingMaterials import InternalClearance, StudentsClearingMaterials
from student_affairs.models.Student import StudentLevelStatusHistory
from system_management.choices.choices import AcademicStatusChoice, ExamAttendanceChoices, ExamTypeChoices, \
    SemesterStudentStatusChoice, EstimateChoice, LevelStudentStatusChoice, ResultStatusChoice, StudentStatusChoice, \
    StudentsClearingMaterialsChoice, RecordChengeGrade, SubjectStatusChoice
from d_services.choices.choices import ServiceStatusChoice
from .utils.helpers_methods import get_student_batch
from academic_affairs.models.Period4Schedule import Period4Schedule
from control.get_number_text import number_to_arabic_text

from system_management.choices.choices import AcademicStatusChoice, EstimateChoice, LevelStudentStatusChoice, ResultStatusChoice, StudentStatusChoice, StudentsClearingMaterialsChoice
from d_services.models.ServiceRequest import ServiceRequest

############################ new code for gate #####################

def call_get_status_statement_data(instance, request):
    """مخرج بيان بالدرجات لغير الخريجيين"""
    service_request = instance
    service_version = service_request.version_data
    component = ComponentFieldResolverGate(external_id=service_request.target_audience_data['external_id'])
    student_batch = component.get_student_academic()
    student = student_batch.fk_student
    student_levels = StudentLevel.objects.filter(
        fk_student_batch__fk_student=student,
        fk_student_batch__is_current=True,
        semester_set__subjects__isnull=False
    ).distinct().order_by("fk_level__level")
    total_levels = student_levels.aggregate(total_levels=Sum("total_grade"))["total_levels"] or 0
    avg_levels = student_levels.aggregate(avg_levels=Sum("avg"))["avg_levels"] or 0

    levels = []
    for student_level in student_levels:
        level = {
            "level_name": student_level.fk_level.get_level_display(),
            "academic_year_year_h": student_level.fk_level.fk_academic_year.year_h,
            "total_grade": student_level.total_grade,
            "avg": student_level.avg,
            "semesters": []
        }
        student_semesters = StudentSemester.objects.filter(fk_student_level=student_level).order_by('fk_semester__name')
        for student_semester in student_semesters:
            semester = {
                "name_ar": student_semester.fk_semester.get_name_display(),
                "total_grade": student_semester.total_grade,
                "avg": student_semester.avg,
                "subjects": []
            }
            semester["subjects"].append({
                "name_ar": student_semester.fk_semester.get_name_display(),
                "number_of_hours": "س-م",
                "grades": "الدرجة",
                "estimate": "التقدير"
            })
            Course
            student_subjects = GradeDetailCourse.objects.filter(fk_grade_program__in=component.get_grade_detail_program())
            for student_subject in student_subjects:
                semester["subjects"].append({
                    "name_ar": student_subject.fk_grade_setting_detail.fk_course.name_ar,
                    # "number_of_hours": student_subject.fk_semmester_subject.number_of_hours,
                    "grades": student_subject.grade,
                    "estimate": student_subject.get_estimate_display()
                })
            level['semesters'].append(semester)
        levels.append(level)

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
        "place_of_brith": {
            "street": student_batch.fk_student.fk_place_of_brith.street,
            "region": student_batch.fk_student.fk_place_of_brith.fk_region.name_ar if student_batch.fk_student.fk_place_of_brith.fk_region else None,
            "governorate": student_batch.fk_student.fk_place_of_brith.fk_governorate.name_ar if student_batch.fk_student.fk_place_of_brith.fk_governorate else None,
            "directorate": student_batch.fk_student.fk_place_of_brith.fk_directorate.name_ar if student_batch.fk_student.fk_place_of_brith.fk_directorate else None,
            "country": student_batch.fk_student.fk_place_of_brith.fk_country.name_ar if student_batch.fk_student.fk_place_of_brith.fk_country else None,
            "date_of_birth": student_batch.fk_student.date_of_birth,
        } if student_batch.fk_student.fk_place_of_brith else {},
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
        "levels": levels
    }

############################ new code for gate #####################



def call_get_payment_output_data(instance, request) -> Dict[str, Any]:
    """
    نموذج مصادقه الدفع(فاتوره) دالة جلب بيانات 
    """
    import random
    
    service_request = instance.fk_request
    
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
        'payment_status': PaymentStatusChoice(service_request.payment_status).label,
        'payment_status_code': service_request.payment_status,
        'request_number': service_request.request_number,
        'remaining_amount': float(service_request.remaining_amount or 0),
    }


def call_clearance_preview(instance, request):
    """جلب بيانات مخرج المقاصصة الداخلية"""
    service_request = instance
    internal_clearance = InternalClearance.objects.filter(fk_request=instance).first()
    if internal_clearance.is_approved == False:
        return {'success': False, 'error': "لم يتم تنفيذ المقاصصة بعد"}
    old_student_batch = internal_clearance.fk_student_batch_old
    new_student_batch = internal_clearance.fk_student_batch_new
    old_student_level = old_student_batch.current_student_level
    new_student_level = new_student_batch.current_student_level
    student_levels = StudentLevel.objects.filter(
        fk_student_batch=internal_clearance.fk_student_batch_new,
        student_level_status__in=[LevelStudentStatusChoice.APPROVED,LevelStudentStatusChoice.SUSPENDED_WITH_COURSES,LevelStudentStatusChoice.CLOSED]
        )

    levels_list = []
    for student_level in student_levels:
        level_obj = {
            "name": student_level.fk_level.get_level_display(),
            "academic_year":student_level.fk_level.fk_academic_year.year_m if student_level.fk_level.fk_academic_year else None,
            "semesters": [],
            "remaining_subjects":[],
            "exempted_subjects":[],
        }
        for semester in Semester.objects.filter(fk_level=student_level.fk_level):
            semester_obj = {
                "name": semester.get_name_display(),
                "subjects": []
            }
            for subject in StudentSubject.objects.filter(fk_semmester_subject__fk_semester=semester,fk_student_semester__fk_student_level__fk_student_batch=internal_clearance.fk_student_batch_new
                ).exclude(subject_status=SubjectStatusChoice.EXEMPT):
                semester_obj["subjects"].append({
                    "new_subject_name": subject.fk_semmester_subject.fk_subject.name_ar,
                    'new_grade': subject.total_grade,
                    'new_hours': subject.fk_semmester_subject.number_of_hours,
                    'new_estimate': subject.get_estimate_display() if subject.estimate else None,
                    "old_subject_name": subject.fk_previous_result.fk_semmester_subject.fk_subject.name_ar,
                    'old_grade': subject.fk_previous_result.total_grade,
                    'old_hours': subject.fk_previous_result.fk_semmester_subject.number_of_hours,
                    'old_estimate': subject.fk_previous_result.get_estimate_display() if subject.fk_previous_result.estimate else None
                    
                })

            level_obj["semesters"].append(semester_obj)
            # المواد المتبقية على الطالب
            student_subjects = StudentSubject.objects.filter(
                fk_student_semester__fk_student_level__in=student_levels,
                fk_semmester_subject=OuterRef("pk")
            )

            level_obj['remaining_subjects'] = SemesterSubject.objects.filter(
                fk_semester__fk_level=student_level.fk_level,
                fk_semester__fk_level__fk_batch=internal_clearance.fk_student_batch_new.fk_batch,
                fk_semester__fk_level__fk_batch__fk_specialization=internal_clearance.fk_student_batch_new.fk_batch.fk_specialization
            ).annotate(
                registered=Exists(student_subjects),
                subject_name=F("fk_subject__name_ar")
            ).filter(
                registered=False
            ).values("subject_name")


            level_obj['exempted_subjects'] = StudentSubject.objects.filter(
                fk_student_semester__fk_student_level__in=student_levels,
                fk_student_semester__fk_student_level__fk_student_batch=internal_clearance.fk_student_batch_new,
                subject_status=SubjectStatusChoice.EXEMPT).annotate(
                    name=F("fk_semmester_subject__fk_subject__name_ar"),
                ).values("name")

        levels_list.append(level_obj)




    return {
        'success': True,
        'student_info': {
            'name': internal_clearance.fk_student_batch_new.fk_student.full_name_ar,
            'academic_year':old_student_level.fk_level.fk_academic_year.year_m,
            'academic_no':old_student_batch.academic_no,
            'level':old_student_level.fk_level.get_level_display(),
            'old_specialization': internal_clearance.fk_student_batch_old.fk_batch.fk_specialization.name_ar,
            'new_specialization': internal_clearance.fk_student_batch_new.fk_batch.fk_specialization.name_ar,
            'new_level':new_student_level.fk_level.get_level_display() if new_student_level else None,
        },
        # 'remaining_subjects': remaining_subjects,
        # 'exempted_subjects': exempted_subjects,
        'levels_list':levels_list,
    }


def call_enrollment_certificate_output_data(instance,request):
    """جلب بيانات وثيقة شهادة القيد الدراسي"""
    try:
        target_audience_data = instance.target_audience_data
        student_batch =  get_student_batch(instance)
        student = student_batch.fk_student
        current_student_level = student_batch.current_student_level
        current_level = current_student_level.fk_level if current_student_level else None
        batch = student_batch.fk_batch

        # الحصول على سنة التسجيل
        enrollment_year = student.fk_enrollment_year.year_m if student.fk_enrollment_year else None

        if not enrollment_year:
            # اذا لا توجد سنة التسجيل من ضمن بيانات الطالب يتم جلب السنة الدراسية الخاصة باول مستوى دراسي للطالب
            first_level = student_batch.level_set.all().order_by('fk_level__level').first()
            enrollment_year = first_level.fk_level.fk_academic_year.year_m if first_level else None

        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}

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
            "enrollment_year": enrollment_year,
            "current_academic_year": current_level.fk_academic_year.year_m if current_level else None,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}
def call_suspension_inrollment_output_data(instance, request):
    """
    جلب بيانات وثيقة وقف القيد
    """
    try:
        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if instance.version_data else {}
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        current_student_level = student_batch.current_student_level
        current_level = current_student_level.fk_level if current_student_level else None
        batch = student_batch.fk_batch
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
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
            "period":version_data.get('period', None),
            "semester": version_data.get('fk_semester', None),
            "reason": version_data.get('reason', None),
            "current_academic_year": current_level.fk_academic_year.year_m if current_level else None,
            "date_today": datetime.date.today(),
            "return_date": version_data.get('return_date', None),
        }
    except Exception as e:
        return {}

def call_cancellation_suspension_inrollment_output_data(instance, request):
    """
    جلب بيانات وثيقة الغاء وقف القيد
    """
    try:

        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if instance.version_data else {}
        fk_student_batch = target_audience_data.get('fk_student')
        old_student_batch = get_student_batch(instance)
        suspended_level = old_student_batch.level_set.filter(
            student_level_status=LevelStudentStatusChoice.WITHDRAWN).last()

        if suspended_level:
            suspended_semester = suspended_level.semester_set.filter(
                student_semester_status=SemesterStudentStatusChoice.WITHDRAWN).last()
        else:
            suspended_semester = StudentSemester.objects.filter(fk_student_level__fk_student_batch=fk_student_batch,
                                                                student_semester_status=SemesterStudentStatusChoice.WITHDRAWN).last()
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
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
        return {
            "student_name": student.full_name_ar,
            "student_id": old_student_batch.academic_no,
            "college": old_student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": old_student_batch.fk_batch.fk_specialization.name_ar,
            "level": suspended_level.fk_level.get_level_display() if suspended_level else None,
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

def call_student_withdrawal_output_data(instance, request):
    """
    جلب بيانات وثيقة سحب ملف
    """
    try:
        version_data = instance.version_data if isinstance(instance.version_data,dict) else {}
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        student_level = student_batch.level_set.filter(fk_level__is_current=True).first()
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
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
            "reason_details":version_data.get('reason_details', None),
        }

    except Exception as e:
        print(e)
        return {}

def call_retake_subject_output_data(instance, request):
    """
    جلب بيانات وثيقة إعادة مادة
    """
    try:

        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        current_level = student_batch.level_set.filter(fk_level__is_current=True).first()
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        # fk_student_subject = version_data.get('fk_student_subject', None)
        target_audience_data = instance.target_audience_data if isinstance(instance.target_audience_data, dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject', None)
        student_subject = StudentSubject.objects.select_related('fk_semmester_subject').get(id=fk_student_subject)
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "nationality": student.fk_nationality.name_ar if student.fk_nationality else None,
            "date_of_birth": student.date_of_birth,
            "place_of_birth": student.place_of_brith,
            "subject_name": student_subject.fk_semmester_subject.fk_subject.name_ar if student_subject else None,
            "subject_code": student_subject.fk_semmester_subject.fk_subject.subject_code,
            "number_of_hours": student_subject.fk_semmester_subject.number_of_hours,
            "results_status_display": student_subject.get_results_status_display(),
            "estimate": student_subject.get_estimate_display(),
            "number_of_attendance": student_subject.number_of_attendance,
            "perparatoin_grade": student_subject.perparatoin_grade,
            "total_grade": student_subject.total_grade,
            "subject_level": student_subject.fk_semmester_subject.fk_semester.fk_level.get_level_display() if student_subject else None,
            "subject_semester": student_subject.fk_semmester_subject.fk_semester.get_name_display() if student_subject else None,
            "subject_academic_year": student_subject.fk_semmester_subject.fk_semester.fk_level.fk_academic_year.year_m,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "current_level": current_level.fk_level.get_level_display() if current_level else None,
            "enrollment_year": student.fk_enrollment_year.year_m,
            "current_academic_year": student_batch.fk_batch.batch_no,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}

def call_attendance_exemption_form_data(instance, request):
    """
    جلب بيانات وثيقة اعفاء حظور
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
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
        return {
            "student_name": student.full_name_ar,
            "student_id": student_batch.academic_no,
            "university": student_batch.fk_branch.name_ar if student_batch.fk_branch else None,
            "college": student_batch.fk_batch.fk_specialization.fk_college.name_ar,
            "specialization": student_batch.fk_batch.fk_specialization.name_ar,
            "level": current_student_level.fk_level.get_level_display() if current_student_level else None,
            "semester": current_student_semester.fk_semester.get_name_display() if current_student_semester else None,
            "from_date": from_date,
            "to_date": to_date,
            "periods": [f'الفترة {number_to_arabic_text(period.order_no)}' for period in periods] if len(
                periods) > 0 else None,
            "issue_date": datetime.date.today(),
        }
    except Exception as e:
        print(e)
        return {}

def call_clearance_form_data(instance, request):
    """
    جلب بيانات وثيقة اخلاء طرف
    """
    pass

def call_grievance_course_grade_form_data(instance, request):
    """
    جلب بيانات وثيقة تظلم على نتيجة حظور
    """
    try:
        target_audience_data = instance.target_audience_data
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        student_batch = get_student_batch(instance)
        student = student_batch.fk_student
        fk_student_subject = target_audience_data.get('fk_student_subject')
        student_subject = StudentSubject.objects.get(id=fk_student_subject)
        subject = student_subject.fk_semmester_subject.fk_subject
        semester = student_subject.fk_semmester_subject.fk_semester
        level = semester.fk_level if semester else None
        batch = student_batch.fk_batch
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
        subject_data = {
            'name_ar':subject.name_ar,
            'name_en':subject.name_en,
            'code':subject.subject_code,
            'grade_records':[]
        }
        if student_subject:
            appeal_student_subject = AppealGradeSubject.objects.get(fk_student_subject=student_subject)
            for grade in student_subject.grade_record.all():
                last_grade_log = grade.grades_log_grades_record.filter(changed_when=RecordChengeGrade.r3).last()
                subject_data['grade_records'].append({
                    "new_grade": str(grade.grade),
                    "old_grade": str(last_grade_log.grade_before) if last_grade_log else 0.0,
                    "name": grade.fk_grade_distributiuon.fk_type_of_grade.name_ar,
                })
            subject_data['old_total_grade'] = appeal_student_subject.previous_total_grade
            subject_data['new_total_grade'] = appeal_student_subject.new_total_grade
            return {
                "university": batch.fk_specialization.fk_college.fk_branch.name_ar,
                "college": batch.fk_specialization.fk_college.name_ar,
                "student_name": student.full_name_ar,
                "academic_no": student_batch.academic_no,
                "current_academic_year":level.fk_academic_year.year_m if level else None ,
                "specialization": batch.fk_specialization.name_ar,
                "level": level.get_level_display() if student_subject else None,
                "semester": semester.get_name_display() if student_subject else None,
                "subject_data": subject_data,
                "appeal_status":appeal_student_subject.get_status_display() ,
                "fk_reviewer":appeal_student_subject.fk_reviewer.full_name if appeal_student_subject.fk_reviewer else None,
                "appeal_date":appeal_student_subject.appeal_date,
                "processed_at":appeal_student_subject.processed_at,
                "issue_date": datetime.date.today(),
            }
        else:
            return {}
    except Exception as e:
        print(e)
        return {}

def call_housing_form_data(instance, request):
    """
    جلب بيانات وثيقة طلب سكن
    """
    pass

def call_replacement_id_card_form_data(instance, request):
    """
    جلب بيانات وثيقة قطع بطاقة بدل فاقد
    """
    try:
        student_batch = get_student_batch(instance)
        version_data = instance.version_data if isinstance(instance.version_data, dict) else {}
        batch = student_batch.fk_batch
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
        student = student_batch.fk_student
        current_student_level = student_batch.current_student_level
        batch_level = current_student_level.fk_level
        return {
            "student_id":student.id,
            "student_name":student.full_name_ar,
            "request_reason":version_data.get('request_reason'),
            "details":version_data.get('details'),
            "student_academic_no":student_batch.academic_no,
            "has_card":current_student_level.card_has_preinted,
            "level":batch_level.get_level_display(),
            "specialization_name_ar":batch.fk_specialization.name_ar,
            "academic_year_h":batch_level.fk_academic_year.year_h,
            "academic_year_m":batch_level.fk_academic_year.year_h,
            "branch_name_ar":batch.fk_specialization.fk_college.fk_branch.name_ar,
            "student_image":student.fk_user.image_user.url if hasattr(student.fk_user,'image_user') else None,
            "collage_name_ar":batch.fk_specialization.fk_college.name_ar,
            "university_name_ar":batch.fk_specialization.fk_college.fk_branch.name_ar,
        }
    except Exception as e:
        print(e)
        return {}

def call_excused_absence_form_data(instance, request):
    """
     جلب بيانات ويثقة غياب بعذر (امتحان)
    """
    try:
        student_batch = get_student_batch(instance)
        version_data = instance.version_data if isinstance(instance.version_data,dict) else {}
        target_audience_data = instance.version_data if isinstance(instance.target_audience_data, dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject')
        student_subject_exam = ExamRegistration.objects.filter(
            fk_student_subject=fk_student_subject,
            fk_exam_schedule__exam_type=ExamTypeChoices.FINAL,
            attendance=ExamAttendanceChoices.EXCUSED
        ).last()
        if instance.status != ServiceStatusChoice.COMPLETED:
            return {}
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



# ================================== school ===================================

def call_new_student_admission_from_data(instance, request):
    """
        جلب بيانات وثيقة قبول طالب مستجد
    """
    if instance.status != ServiceStatusChoice.COMPLETED:
        return {}

    student_class = get_student_class(instance)
    student = student_class.fk_student 
    branch_class = student_class.fk_study_program
    fk_org = student_class.fk_org
    guardian = student.guardian_relationships.first()
    guardian = guardian.fk_guardian if guardian else None

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



def get_student_class(instance):
    """
    دالة مساعدة لجلب سجل الدفعة من بيانات الطلب (instance.data).
    يتم جلب المعرف من target_audience_data تحت المفتاح fk_student_class.
    """
    target_audience_data = instance.target_audience_data if isinstance(instance,ServiceRequest) else {}

    # بناءً على تحليل ملفات target_audience.json، المفتاح الرئيسي هو fk_student
    student_class_id = target_audience_data.get('fk_student_by_division')

    if not student_class_id:
        raise Exception("لم يتم العثور على معرف سجل الطالب (student__name) في بيانات الطلب.")

    try:
        return StudentAcademic.objects.get(id=student_class_id)
    except StudentAcademic.DoesNotExist:
        raise Exception(f"سجل الطالب ذو المعرف {student_class_id} غير موجود.")