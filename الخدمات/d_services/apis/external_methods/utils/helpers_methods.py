from academic_affairs.models.Level import Level
from academic_affairs.models.Semester import Semester
from academic_affairs.models.SemesterSubject import SemesterSubject
from d_services.models.ServiceRequest import ServiceRequest
from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel, StudentSemester, StudentSubject
from system_management.choices.choices import AcademicStatusChoice, LevelStudentStatusChoice, ProcessStatusChoices, ResultStatusChoice, SemesterStudentStatusChoice, StudentStatusChoice, StudentsClearingMaterialsChoice, SubjectStatusChoice
from system_management.models.Specialization import Specialization
from utils.GradeApproval import GradeApproval

def calculate_scaled_grade(old_grade, old_total, new_total):
    """
    تحويل الدرجة القديمة إلى نظام الدرجة الجديد حسب مجموع النقاط.
    إذا كان old_total <= 0 أو new_total <= 0 أو نفس المجموع، تعود الدرجة كما هي.
    """
    if old_total <= 0 or new_total <= 0 or old_total == new_total:
        return old_grade
    try:
        final_grade = (float(old_grade) / float(old_total)) * float(new_total)
        # إذا كانت النتيجة عدد صحيح بعد التقريب، نحوله int لتجنب الكسور غير الضرورية
        return int(final_grade) if round(final_grade, 2).is_integer() else round(final_grade, 2)
    except Exception:
        return old_grade  # fallback في حال حدوث خطأ

def find_equivalent_subject(old_subject, subjects_by_code, subjects_by_name):
    """
    البحث عن مادة معادلة في التخصص الجديد:
    1. أولًا عن طريق الكود
    2. إذا لم توجد، عن طريق الاسم العربي
    3. إذا لم توجد، عن طريق الاسم الإنجليزي
    """
    if old_subject.subject_code:
        code = old_subject.subject_code.strip().lower()
        if code in subjects_by_code: 
            return subjects_by_code[code]
    
    if old_subject.name_ar:
        if name := old_subject.name_ar.strip().lower():
            if name in subjects_by_name: 
                return subjects_by_name[name]
            
    if old_subject.name_en:
        if name := old_subject.name_en.strip().lower():
            if name in subjects_by_name: 
                return subjects_by_name[name]
            
    return None  # إذا لم يتم العثور على مادة معادلة


def get_student_batch(instance):
    """
    دالة مساعدة لجلب سجل الدفعة من بيانات الطلب (instance.data).
    يتم جلب المعرف من target_audience_data تحت المفتاح fk_student_batch.
    """
    target_audience_data = instance.target_audience_data if isinstance(instance,ServiceRequest) else {}

    # بناءً على تحليل ملفات target_audience.json، المفتاح الرئيسي هو fk_student_batch
    student_batch_id = target_audience_data.get('fk_student_batch')

    if not student_batch_id:
        raise Exception("لم يتم العثور على معرف سجل الدفعة (fk_student_batch) في بيانات الطلب.")

    try:
        return StudentBatch.objects.get(id=student_batch_id)
    except StudentBatch.DoesNotExist:
        raise Exception(f"سجل الدفعة ذو المعرف {student_batch_id} غير موجود.")

def get_student_level(instance):
    """
    دالة مساعدة لجلب سجل مستوى الطالب من بيانات الطلب (instance.data).
    يتم جلب المعرف من target_audience_data تحت المفتاح fk_student_level.
    """
    target_audience_data = instance.target_audience_data if isinstance(instance,ServiceRequest) else {}

    # بناءً على تحليل ملفات target_audience.json، المفتاح الرئيسي هو fk_student_level
    student_level_id = target_audience_data.get('fk_student_level')

    if not student_level_id:
        raise Exception("لم يتم العثور على معرف سجل مستوى الطالب (fk_student_level) في بيانات الطلب.")

    try:
        return StudentLevel.objects.get(id=student_level_id)
    except StudentLevel.DoesNotExist:
        raise Exception(f"سجل مستوى الطالب ذو المعرف {student_level_id} غير موجود.")


def get_specialization_and_parents_ids(specialization_id):
    """
    للتخصص نفسه + جميع ابائه ids نرجع قائمة
    تمشي للاعلى while fk_mandatory_major is not null
    """

    ids = []

    try:
        spec = Specialization.objects.select_related('fk_mandatory_major').get(id=specialization_id)
    except Specialization.DoesNotExist:
        return []

    while spec:
        ids.append(spec.id)
        spec = spec.fk_mandatory_major

    return ids


def get_student_batch_and_parents_ids(student_batch_id):
    """
    لدفعة الطالب نفسه + جميع ابائه ids نرجع قائمة
    تمشي للاعلى while fk_mandatory_major is not null
    """

    ids = []

    try:
        student_batch = StudentBatch.objects.select_related('fk_previous_batch').get(id=student_batch_id)
    except StudentBatch.DoesNotExist:
        return []

    while student_batch:
        ids.append(student_batch.id)
        student_batch = student_batch.fk_previous_batch

    return ids


def get_subs_by_code_and_subs_by_name_for_new_batch(new_batch):
        # تجهيز قاموس البحث للمواد الجديدة
        new_subs = SemesterSubject.objects.filter(fk_semester__fk_level__fk_batch=new_batch).select_related('fk_subject', 'fk_grading_system_june')
        subs_by_code = {semester_subject.fk_subject.subject_code.strip().lower(): semester_subject for semester_subject in new_subs if semester_subject.fk_subject.subject_code}
        subs_by_name = {}
        for semester_subject in new_subs:
            if semester_subject.fk_subject.name_ar: subs_by_name[semester_subject.fk_subject.name_ar.strip().lower()] = semester_subject
            if semester_subject.fk_subject.name_en: subs_by_name[semester_subject.fk_subject.name_en.strip().lower()] = semester_subject

        return subs_by_code , subs_by_name, new_subs


def get_student_subjects_history_for_old_specialization(student_id,specializations_ids):
    # جلب المواد التي تحتوي على درجة فقط
    # لضمان ان اول مادة نصادقها في الحلقة هي الاحدث ترتيب تنازلي حسب ال id 
    all_student_subjects = StudentSubject.objects.filter(
        fk_student_semester__fk_student_level__fk_student_batch__fk_batch__fk_specialization_id__in=specializations_ids,
        fk_student_semester__fk_student_level__fk_student_batch__fk_student=student_id,
        total_grade__isnull=False,
    ).exclude(results_status=ResultStatusChoice.PENDING).select_related(
        'fk_semmester_subject__fk_subject', 'fk_semmester_subject__fk_grading_system_june'
    ).order_by('-id')

    # نستخدم قاموس لضمان اخذ اخر محاولة للمادة فقط
    history_by_code = {}
    history_by_name = {}
    history_by_semester_subject_id = {}

    for student_subject in all_student_subjects:
        sem_subject = student_subject.fk_semmester_subject
        subject = sem_subject.fk_subject
        
        # 1. الفهرسة حسب الـ id الخاص بالـ SemesterSubject (للمعادلات الرسمية)
        if sem_subject.id not in history_by_semester_subject_id:
            history_by_semester_subject_id[sem_subject.id] = student_subject

        # 2. الفهرسة حسب الكود
        code = subject.subject_code.strip().lower() if subject.subject_code else None
        if code and code not in history_by_code:
            history_by_code[code] = student_subject

        # 3. الفهرسة حسب الاسم (عربي وإنجليزي)
        if subject.name_ar:
            name_ar = subject.name_ar.strip().lower()
            if name_ar not in history_by_name:
                history_by_name[name_ar] = student_subject
        
        if subject.name_en:
            name_en = subject.name_en.strip().lower()
            if name_en not in history_by_name:
                history_by_name[name_en] = student_subject

    return {
        'history_by_code': history_by_code,
        'history_by_name': history_by_name,
        'history_by_semester_subject_id': history_by_semester_subject_id
    }


# ================================
# Helper Functions for Clearance Execution
# ================================

def create_new_student_batch(student,old_sb,new_batch,academic_year):
    """
    Creates or retrieves the new StudentBatch
    Marks the old batch as non-current
    Return: 
        tuple: (StudentBatch,bool) - The new batch and whether it was created
    """
    old_sb.is_current = False
    old_sb.save()

    new_sb, created = StudentBatch.objects.get_or_create(
        fk_student=student,
        fk_batch=new_batch,
        defaults={
            "fk_academic_year": academic_year,
            "fk_previous_batch": old_sb,
            "is_current": True,
            "accademic_status":AcademicStatusChoice.MAJOR_TRANSFER,
            "fk_study_system":old_sb.fk_study_system,
            "fk_branch":old_sb.fk_branch
        }
    )

    return new_sb, created


def create_student_levels(new_sb,new_batch):
    """
    Creates StudentLevel records for all levels in the new batch>
    Marks the first level as active (current).

    Returns:
        tuple: (dict, StudentLevel) - Dictionary mapping {level_id: StudentLevel} and the current level
    """

    levels = Level.objects.filter(fk_batch=new_batch).order_by('level')
    student_levels = {}
    current_level = None

    for level in levels:
        sl = StudentLevel.objects.create(
            fk_student_batch=new_sb,
            fk_level=level,
            student_level_status=LevelStudentStatusChoice.UNDER_REVIEW,
            is_active=False
        )
        student_levels[level.id] = sl
        if not current_level:
            current_level = sl

    if current_level:
        current_level.is_active = True
        current_level.save(update_fields=['is_active'])

    return student_levels, current_level

def create_student_semesters(student_levels):
    """
    Creates StudentSemester records for all semesters in each level.
    Returns:
        dict: Dictionary mapping {(level_id, semester_id): StudentSemester}
    """
    student_semesters = {}
    for level_id, sl in student_levels.items():
        semesters = Semester.objects.filter(fk_level_id=level_id)
        for sem in semesters:
            ss, _ = StudentSemester.objects.get_or_create(
                fk_student_level=sl,
                fk_semester=sem,
                defaults={
                    "is_active": sl.is_active,
                    "student_semester_status": SemesterStudentStatusChoice.APPROVED
                }
            )
            student_semesters[(level_id,sem.id)] = ss

    return student_semesters


def process_clearance_materials(materials,old_sb,new_sb,student_levels,student_semesters):
    """
    Processes each clearance material, creates StudentSubject records,
    and updates material status to COMPLETED

    Returns:
        int: Count of processed materials
    """
    processed_count = 0
    for mat in materials:
        target = mat.fk_semester_subject_to
        old_rec = mat.fk_semester_subject_from
        sl = student_levels.get(target.fk_semester.fk_level_id)
        ss = student_semesters.get((target.fk_semester.fk_level_id,target.fk_semester.id))

        if not sl or not ss:
            continue

        grade = 0
        estimate = None
        old_ss = None
        if old_rec:
            old_ss = StudentSubject.objects.filter(
                fk_student_semester__fk_student_level__fk_student_batch=old_sb,
                fk_semmester_subject=old_rec,
                total_grade__isnull=False
            ).first()

            if old_ss:
                grade = calculate_scaled_grade(
                    old_ss.total_grade,
                    old_rec.fk_grading_system_june.grade_total,
                    target.fk_grading_system_june.grade_total
                )
                grading_system = GradeApproval.get_student_grading_system(old_ss)
                estimate, grade = GradeApproval.get_estimate_total(
                    grading_system,grade,
                    new_sb.fk_batch.fk_specialization.fk_college.fk_branch
                )

            if mat.type == StudentsClearingMaterialsChoice.REMAINING:
                results_status = ResultStatusChoice.REMAINING
                subject_status = SubjectStatusChoice.UNDER_REVIEW
            elif mat.type == StudentsClearingMaterialsChoice.EXEMPTED:
                results_status = ResultStatusChoice.CLEARANCE
                subject_status = SubjectStatusChoice.EXEMPT
            else:
                results_status = ResultStatusChoice.CLEARANCE
                subject_status = SubjectStatusChoice.UNDER_REVIEW
            
            StudentSubject.objects.create(
                fk_student_semester=ss,
                fk_semmester_subject=target,
                total_grade=grade,
                results_status=results_status,
                fk_previous_result=old_ss,
                estimate=estimate.name if estimate else None,
                subject_status=subject_status
            )
        else:
            # يتم انشاء المواد المعفية اذا كان لا يوجد لها سجل في التخصص القديم
            if mat.type == StudentsClearingMaterialsChoice.EXEMPTED:
                results_status = ResultStatusChoice.CLEARANCE
                subject_status = SubjectStatusChoice.EXEMPT
                StudentSubject.objects.create(
                    fk_student_semester=ss,
                    fk_semmester_subject=target,
                    subject_status=subject_status
                )

        mat.process_status = ProcessStatusChoices.COMPLETED
        mat.save(update_fields=['process_status'])
        processed_count += 1

    return processed_count


def calculate_and_update_levels(student_levels):
    """
    Determines the student's current level based on remaining subjects
    Updates StudentLevel statues.
    Returns the current StudentLevel object.
    """
    sorted_levels = sorted(
        student_levels.values(),
        key=lambda sl: sl.fk_level.level
    )

    current_active_sl = None

    for i,sl in enumerate(sorted_levels):
        level_obj = sl.fk_level
        allowed_failure = level_obj.allowed_failure_subjects


        # حساب مواد الخطة
        total_plan_subjects = SemesterSubject.objects.filter(fk_semester__fk_level__id=level_obj.id,
        fk_semester__fk_level__fk_batch__fk_specialization=sl.fk_level.fk_batch.fk_specialization).count()

        # المواد التي نجح بها الطالب
        passed_count = StudentSubject.objects.filter(
            fk_student_semester__fk_student_level=sl,
            fk_student_semester__fk_student_level__fk_level=level_obj,
            results_status__in=[ResultStatusChoice.PASSED,ResultStatusChoice.CLEARANCE]
        ).count()

        # المواد المتبقية للنجاح
        remaining = total_plan_subjects - passed_count
        # تحديد حالة المستوى
        move_to_next_level = False

        # الحماية 1: اذا لم توجد مواد للخطة خطأ اعدادات توقف هنا و لا تغلق المستوى
        if total_plan_subjects == 0:
            sl.student_level_status = LevelStudentStatusChoice.APPROVED
            sl.is_active = False
            sl.save()
            current_active_sl = sl
            break

        # الحمالية 2: اذا كان الطالب لم ينجح في اي مادة وكان عليه مواد متبقية
        # فهذا يعني انه طالب جديد في هذا المستوى او راسب كلياً
        # لذلك نمنع انتقاله حتى لو كان المتبقي <= المسموح
        # الاستثناء الوحيد: اذا كان (المتبقي == 0) فهذا يعني انه تم اعفاؤه بالكامل حالة مقاصة كاملة
        if passed_count == 0 and remaining > 0:
            sl.student_level_status = LevelStudentStatusChoice.APPROVED
            sl.is_active = False
            sl.save()
            current_active_sl = sl
            break

        # حالة: لم يسجل الطالب اي مادة
        if remaining == 0:
            sl.student_level_status = LevelStudentStatusChoice.CLOSED
            sl.is_active = False
            move_to_next_level = True # تجاوز المستوى
        # حالة: نجح في كل المواد
        elif remaining <= allowed_failure:
            sl.student_level_status = LevelStudentStatusChoice.SUSPENDED_WITH_COURSES
            sl.is_active = False
            move_to_next_level = True
        # حالة: المتبقي <= المسموح ناجح مع حمل مواد
        else:
            sl.student_level_status = LevelStudentStatusChoice.APPROVED
            sl.is_active = False
            move_to_next_level = False
        
        sl.save()


        # --- منطق الترفيع
        if move_to_next_level:
            if i + 1 <len(sorted_levels):
                current_active_sl = sorted_levels[i+1]
                continue
            else:
                current_active_sl = sl
                break
        else:
            current_active_sl = sl
            break

    # تفعيل المستوى النشط
    if current_active_sl:
        # تفعيل المستوى الحالي الذي وقف عنده المؤشر
        current_active_sl.is_active = True
        
        current_active_sl.student_level_status = LevelStudentStatusChoice.APPROVED
        current_active_sl.save()

    return current_active_sl

def update_student_data(student,current_level,new_batch):
    """
    Updates student's current specialization, level, and semester.
    Returns:
        Student: The updated studnet object
    """
    student.fk_current_specialization = new_batch.fk_specialization
    student.fk_current_level = current_level.fk_level
    student.fk_current_semester = current_level.fk_level.semester_set.order_by('name').first()
    student.save()
    return student
