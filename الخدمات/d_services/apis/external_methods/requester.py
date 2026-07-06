import logging
from typing import Any, Optional

from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel

logger = logging.getLogger(__name__)


def call_get_student_image_for_statement(user,data:dict,**kwargs) -> Optional[Any]:
    """جلب صورة الطالب من سجل الدفعة """
    # data = kwargs.get('data')
    target_audience_data = data.get('target_audience_data')
    fk_student_batch = target_audience_data.get('fk_student_batch')
    student_batch = StudentBatch.objects.get(id=fk_student_batch)
    if hasattr(student_batch.fk_student, 'fk_user') and student_batch.fk_student.fk_user:
        fk_user = student_batch.fk_student.fk_user
        return fk_user.image_user.url if hasattr(fk_user, 'image_user') else None
    return None


def call_get_student_info_for_statement(user,data:dict,**kwargs) -> Optional[Any]:
    """جلب معلومات الطالب من سجل الدفعة"""
    # data = kwargs.get('data')
    target_audience_data = data.get('target_audience_data')
    fk_student_batch = target_audience_data.get('fk_student_batch')
    student_batch = StudentBatch.objects.get(id=fk_student_batch)
    return {
        "id": student_batch.id,
        "name": student_batch.fk_student.full_name_ar,
        "description": student_batch.academic_no
    }

def call_get_student_image_for_clearance(user,data:dict,**kwargs) -> Optional[Any]:
    """جلب صورة الطالب من سجل مستوى الطالب"""
    # data = kwargs.get('data')
    target_audience_data = data.get('target_audience_data')
    fk_student_level = target_audience_data.get('fk_student_level')
    student_level = StudentLevel.objects.get(id=fk_student_level)
    student_batch = student_level.fk_student_batch
    if hasattr(student_batch.fk_student, 'fk_user') and student_batch.fk_student.fk_user:
        fk_user = student_batch.fk_student.fk_user
        return fk_user.image_user.url if hasattr(fk_user, 'image_user') else None
    return None


def call_get_student_info_for_clearance(user,data:dict,**kwargs) -> Optional[Any]:
    """جلب معلومات الطالب من سجل مستوى الطالب"""
    # data = kwargs.get('data')
    target_audience_data = data.get('target_audience_data')
    fk_student_level = target_audience_data.get('fk_student_level')
    student_level = StudentLevel.objects.get(id=fk_student_level)
    student_batch = student_level.fk_student_batch
    return {
        "id": student_batch.id,
        "name": student_batch.fk_student.full_name_ar,
        "description": student_batch.academic_no
    }
