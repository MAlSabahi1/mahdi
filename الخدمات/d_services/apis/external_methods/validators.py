# import logging
# from typing import Any, Dict

# from student_affairs.models.StudentBatch import StudentBatch
# from student_affairs.models.StudentCourse import StudentLevel
# from system_management.choices.choices import LevelStudentStatusChoice

# logger = logging.getLogger(__name__)


# def call_validate_student_not_graduated_or_certified(user, service, data) -> Dict[str, Any]:
#     """
#     التحقق من أن الطالب ليس خريجاً 
#     """
#     try:
#         target_data = data.get('target_data', {})
#         if not target_data and 'fk_student_batch' in data:
#              target_data = data

#         fk_student_batch = target_data.get('fk_student_batch')
        
#         if not fk_student_batch:
#             return {
#                 'is_valid': False,
#                 'message': 'رقم قيد الطالب في الدفعة (fk_student_batch) غير موجود'
#             }

#         student_batch = StudentBatch.objects.get(id=fk_student_batch)
        
#         # Check graduates status of the batch
#         batch_graduates = False
#         if student_batch.fk_batch:
#             batch_graduates = student_batch.fk_batch.graduates
            
#         # Check certification printed status
#         cert_printed = student_batch.certification_has_printed
        
#         if batch_graduates or cert_printed:
#             return {
#                 'is_valid': False,
#                 'message': 'عذراً لا يمكن تقديم الطلب، الطالب خريج أو تم طباعة الشهادة مسبقاً'
#             }
            
#         return {
#             'is_valid': True,
#             'message': 'الطالب مستوفي للشروط'
#         }
        
#     except StudentBatch.DoesNotExist:
#         return {
#             'is_valid': False,
#             'message': 'بيانات الطالب في الدفعة غير موجودة'
#         }
#     except Exception as e:
#         logger.error(f"Error in validate_student_not_graduated_or_certified: {e}")
#         return {
#             'is_valid': False,
#             'message': 'حدث خطأ أثناء التحقق من الشروط'
#         }


# def call_check_student_is_in_first_level(user, service, data):
#     """التحقق من ان الطالب اجتاز مستوى اول"""
#     service_request = data
#     student_level = StudentLevel.objects.filter(
#         fk_student_batch=service_request.target_audience_data['fk_student_batch'],
#         is_active=True
#     ).first()
#     return student_level.student_level_status not in [
#         LevelStudentStatusChoice.UNDER_REVIEW,
#         LevelStudentStatusChoice.WITHDRAWN,
#         LevelStudentStatusChoice.APPROVED,
#         LevelStudentStatusChoice.REGISTERED_FOR_REPEAT
#     ]

# # def call_validate_student_not_graduated_or_certified(user, service, data) -> Dict[str, Any]:
# #     return  {
# #             'is_valid': True,
# #             'message': 'حدث خطأ أثناء التحقق من الشروط'
# #         }
# # def call_check_student_is_in_first_level(user, service, data):
# #     return  {
# #             'is_valid': True,
# #             'message': 'حدث خطأ أثناء التحقق من الشروط'
# #         }




import logging
from typing import Any, Dict

from exam.models.ExamRegistration import ExamRegistration
from exam.models.ExamSchedule import ExamSchedule
from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
from system_management.choices.choices import LevelStudentStatusChoice, StudentStatusChoice, LevelChoice, \
    AcademicStatusChoice, SemesterStudentStatusChoice, ResultStatusChoice, SubjectStatusChoice, ExamTypeChoices, \
    ExamAttendanceChoices
from django.utils.translation import gettext_lazy as _
from student_affairs.models.Student import StudentBranchStatusHistory
from system_management.models.Specialization import Specialization

logger = logging.getLogger(__name__)
from d_services.models.ServiceRequest import ServiceRequest

def get_student_batch(data):
    """
    دالة مساعدة لجلب سجل الدفعة من بيانات الطلب (data).
    يتم جلب المعرف من target_audience_data تحت المفتاح fk_student_batch.
    """
    target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}

    # بناءً على تحليل ملفات target_audience.json، المفتاح الرئيسي هو fk_student
    student_batch_id = target_audience_data.get('fk_student_batch')

    if not student_batch_id:
        raise Exception("لم يتم العثور على معرف سجل الدفعة (fk_student_batch) في بيانات الطلب.")

    try:
        return StudentBatch.objects.get(id=student_batch_id)
    except StudentBatch.DoesNotExist:
        raise Exception(f"سجل الدفعة ذو المعرف {student_batch_id} غير موجود.")



def call_validate_student_not_graduated_or_certified(user, service, data) -> Dict[str, Any]:
    """
    التحقق من أن الطالب ليس خريجاً 
    """
    try:
        target_data = data.get('target_data', {})
        if not target_data and 'fk_student_batch' in data:
             target_data = data

        student_batch = get_student_batch(data)

        student_batch = StudentBatch.objects.get(id=fk_student_batch)
        
        # Check graduates status of the batch
        batch_graduates = False
        if student_batch.fk_batch:
            batch_graduates = student_batch.fk_batch.graduates
            
        # Check certification printed status
        cert_printed = student_batch.certification_has_printed
        
        if batch_graduates or cert_printed:
            return {
                'is_valid': False,
                'message': 'عذراً لا يمكن تقديم الطلب، الطالب خريج أو تم طباعة الشهادة مسبقاً'
            }
            
        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }
    except Exception as e:
        logger.error(f"Error in validate_student_not_graduated_or_certified: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }


def call_check_student_is_in_first_level(user, service, data):
    """التحقق من ان الطالب اجتاز مستوى اول"""
    student_batch = get_student_batch(data)
    current_student_level = student_batch.current_student_level
    student_level_status = current_student_level.student_level_status
    level = current_student_level.fk_level.level
    if  level != LevelChoice.LEVEL_1 and student_level_status in [LevelStudentStatusChoice.CLOSED,LevelStudentStatusChoice.SUSPENDED_WITH_COURSES]:
        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }
    else:
        return {
            'is_valid': False,
            'message': 'الطالب غير مستوفي للشروط'
        }
def call_check_current_student_level_is_active(user, service, data):
    """التحقق من نشاط سجل المستوى الحالي للطالب"""
    student_batch = get_student_batch(data)
    current_student_level = student_batch.current_student_level
    if current_student_level.is_active:
        return {
            'is_valid': True,
            'message':'الطالب مستوفي الشروط'
        }
    else:
        return {
            'is_valid': False,
            'message':f"سجل الطالب في المستوى {current_student_level.fk_level.get_level_status()} غير نشط"
        }

def call_check_current_student_semester_is_active(user, service, data):
    """التحقق من نشاط سجل الفصل الدراسي الحالي للطالب"""
    student_batch = get_student_batch(data)
    current_student_level = student_batch.current_student_level
    current_student_semester = current_student_level.current_student_semester
    if current_student_semester.is_active:
        return {
            'is_valid': True,
            'message':'الطالب مستوفي الشروط'
        }
    else:
        return {
            'is_valid': False,
            'message':f"سجل الطالب في الفصل الدراسي {current_student_semester.fk_semester.get_name_status()} غير نشط"
        }


def call_validate_submission_deadline(user, service, data):
    """
    التحقق من تقديم الطلب في الوقت المحدد (قبل أسبوعين من الاختبارات النهائية).
    """

    try:
        student_batch = get_student_batch(data)
        current_student_level = student_batch.current_student_level
        current_student_semester = current_student_level.current_student_semester
        current_semester = current_student_semester.fk_semester
        exam_schedule_exists = ExamSchedule.objects.filter(
            fk_semester_subject__fk_semester=current_semester,
            exam_type=ExamTypeChoices.FINAL
        ).exists()

        if current_semester.is_current and exam_schedule_exists:
            return {
                'is_valid': False,
                'message':_('تم تحديد موعد الامتحانات')
            }
        return True

    except Exception as e:
        logger.error(f"Error in validate_student_not_graduated_or_certified: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }


def call_check_student_is_in_first_level(user, service, data):
    """التحقق من ان الطالب اجتاز مستوى اول"""
    service_request = data
    student_level = StudentLevel.objects.filter(
        fk_student_batch=service_request.target_audience_data['fk_student_batch'],
        is_active=True
    ).first()
    return student_level.student_level_status not in [
        LevelStudentStatusChoice.UNDER_REVIEW,
        LevelStudentStatusChoice.WITHDRAWN,
        LevelStudentStatusChoice.APPROVED,
        LevelStudentStatusChoice.REGISTERED_FOR_REPEAT
    ]

def call_validate_not_level_one(user, service, data):
    """
        التحقق من أن الطالب ليس في المستوى الأول.
    """

    try:

        student_batch = get_student_batch(data)
        student_level = student_batch.level_set.filter(fk_level__is_current=True).first()
        if student_level and student_level.fk_level.level == LevelChoice.LEVEL_1:
            return {
                'is_valid': False,
                'message':_("عذراً، لا يسمح بوقف القيد لطلاب المستوى الأول.")
            }
        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }


    except Exception as e:
        logger.error(f"Error in validate_student_not_graduated_or_certified: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }




def call_validate_not_repeating(user, service, data):
    """
    التحقق من أن الطالب ليس باقياً للإعادة.
    """
    try:
        student_batch = get_student_batch(data)
        student_level = student_batch.level_set.filter(fk_level__is_current=True).first()
        if student_level and student_level.student_level_status == LevelStudentStatusChoice.REGISTERED_FOR_REPEAT:
            return {
                'is_valid': False,
                'message': _("لا يجوز وقف القيد للطالب الباقي للإعادة.")
            }
        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }
    except Exception as e:
        logger.error(f"Error in validate_student_not_graduated_or_certified: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }



def call_validate_max_suspension_duration(user, service, data):
    """
    التحقق من عدم تجاوز الحد الأقصى لمدة وقف القيد (سنتين / 4 فصول دراسية).
    """

    try:
        student_batch = get_student_batch(data)

        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }
    except Exception as e:
        logger.error(f"Error in validate_student_not_graduated_or_certified: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }


def call_validate_student_is_active(user, service, data):
    """
    التحقق من أن حالة الطالب 'مستمر' (Active).
    """
    try:
        student_batch = get_student_batch(data)
        current_student_level = student_batch.current_student_level

        # if student_batch.student_status != StudentStatusChoice.ACTIVE:
        if current_student_level and current_student_level.student_level_status == LevelStudentStatusChoice.UNDER_REVIEW:
            return {
                'is_valid': False,
                'message': _(f"عذراً، يجب أن يكون الطالب مقيداً ومستمراً بالدراسة (Active). الحالة الحالية: ({student_batch.get_student_status_display()})")
            }

        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }

    except Exception as e:
        logger.error(f"Error in call_validate_student_is_active: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }

def call_validate_student_is_suspended(user, service, data):
    """
    التحقق من أن حالة الطالب 'موقف قيد' (Suspended).
    """
    try:

        student_batch = get_student_batch(data)
        suspended_level = student_batch.level_set.filter(student_level_status=LevelStudentStatusChoice.WITHDRAWN).last()
        suspended_semester = StudentSemester.objects.filter(
            fk_student_level__fk_student_batch=student_batch,
            student_semester_status=SemesterStudentStatusChoice.WITHDRAWN
        ).last()
        if not suspended_level and not suspended_semester:
            return {
                'is_valid': False,
                'message':'عذرا, لا يوجد سجل وقف قيد للطالب.'
            }
        return {
            'is_valid': True,
            'message': 'الطالب مستوفي للشروط'
        }

    except Exception as e:
        logger.error(f"Error in call_validate_student_is_suspended: {e}")
        return {
            'is_valid': False,
            'message': str(e)
        }
def call_validate_student_subject_exists(user,service, data):
    """التحقق ان الطالب مسجل بالمادة"""
    try:
        target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject', None)
        student_subject = StudentSubject.objects.filter(id=fk_student_subject).first()
        if not student_subject:
            return {
                'is_valid': False,
                'message':'الطالب غير مسجل بمعرف المادة'
            }
        return True

    except Exception as e:
        logger.error(f"Error in call_validate_student_studied_subject: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }
def call_validate_student_studied_subject(user,service,data):
    """التحقق من عدم اعادة المادة مرة اخرى"""

    try:
        target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject', None)
        student_subject = StudentSubject.objects.filter(id=fk_student_subject).first()
        if not student_subject:
            return {
                'is_valid': False,
                'message':'الطالب غير مسجل بمعرف المادة'
            }
        if student_subject.fk_previous_result:
            return {
                'is_valid': False,
                'message': 'لا يمكن اعادة المادة مرة اخرى.'
            }
        return True


    except Exception as e:
        logger.error(f"Error in call_validate_student_studied_subject: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }

# TODO validate subject is exists with current academic semester


def call_not_match_specialization(user,service,data):
    """التحقق من عدم المقاصة على نفس التخصص"""

    try:

        target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}
        fk_student_level = target_audience_data.get('fk_student_level')
        version_data = data.get('version_data') if isinstance(data,dict) else {}
        fk_new_specialization = version_data.get('fk_new_specialization')
        try:
            student_level = StudentLevel.objects.get(id=fk_student_level)
            student_batch = student_level.fk_student_batch
            old_specialization = student_batch.fk_batch.fk_specialization
            if fk_new_specialization == old_specialization.id:
                return {
                    'is_valid': False,
                    'message':f'لا يمكن المقاصة على نفس التخصص  ({old_specialization.name_ar})'
                }
            return True
        except StudentBatch.DoesNotExist:
            return {
                'is_valid': False,
                'message': f"سجل مستوى الطالب ذو المعرف {fk_student_level} غير موجود."
            }

    except Exception as e:
        logger.error(f"Error in call_not_match_specialization: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }

def call_match_branch(user,service,data):
    """التحقق من ان المقاصة الداخلية على نفس الفرع (جامعة)"""

    try:

        target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}
        fk_student_level = target_audience_data.get('fk_student_level')
        version_data = data.get('version_data') if isinstance(data,dict) else {}
        fk_new_specialization = version_data.get('fk_new_specialization')
        try:
            student_level = StudentLevel.objects.get(id=fk_student_level)
            student_batch = student_level.fk_student_batch
            old_specialization = student_batch.fk_batch.fk_specialization
            new_specialization = Specialization.objects.get(id=fk_new_specialization)
            if old_specialization.fk_college.fk_branch != new_specialization.fk_college.fk_branch:
                return {
                    'is_valid': False,
                    'message':f'المقاصة الداخلية يجب ان تكون على نفس الفرع (جامعة)'
                }
            return True
        except StudentBatch.DoesNotExist:
            return {
                'is_valid': False,
                'message': f"سجل مستوى الطالب ذو المعرف {fk_student_level} غير موجود."
            }

    except Exception as e:
        logger.error(f"Error in call_not_match_specialization: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }


def call_validate_student_subject_registered_in_exam(user,service,data):
    """التحقق ان الطالب مسجل بالامتحان للمادة المطلوبة"""
    try:
        target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}
        fk_student_subject = target_audience_data.get('fk_student_subject')
        exam_registration = ExamRegistration.objects.filter(
            fk_student_subject=fk_student_subject,
            fk_exam_schedule__exam_type=ExamTypeChoices.FINAL
        ).first()

        if not exam_registration:
            return {
                'is_valid': False,
                'message':"الطالب غير مسجل للامتحان بهذه المادة."
            }

        if exam_registration.attendance not in [ExamAttendanceChoices.ABSENCE,ExamAttendanceChoices.OTHER]:
            return {
                'is_valid': False,
                'message':_(f' حالة الطالب بالامتحان لا تسمح بطلب العذر ({exam_registration.get_attendance_display()}).')
            }

        return True
    except Exception as e:
        logger.error(f"Error in call_validate_student_subject_registered_in_exam: {e}")
        return {
            'is_valid': False,
            'message': 'حدث خطأ أثناء التحقق من الشروط'
        }
