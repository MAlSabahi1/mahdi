"""
نظام المقاصة الداخلية بين التخصصات في نفس الكلية
Internal Subject Credit Transfer (Clearance) System
"""
from django.db import transaction
from django.db.models import Q
from core.models import (
    Student, StudentBatch, StudentLevel, StudentSemester, StudentSubject,
    Specialization, Subject, SemesterSubject, Semester, Level, Batch,
    ResultStatusChoice, SubjectStatusChoice, EstimateChoices,
    LevelStudentsStatusChoices, SemesterStudentsStatusChoices,
    StudentStatusChoices, AcademicStatus, StudentsClearingMaterials,
    StudentsClearingMaterialsChoice, ClearingMaterials
)

# ==========================
# دوال مساعدة عامة
# ==========================

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

# ==========================
# معاينة المقاصة بدون حفظ
# ==========================

def get_clearance_preview_table_data(student_level_id, new_specialization_id):
    """
    تجهيز جدول معاينة المقاصة للطالب قبل التنفيذ:
    - يعرض المواد المكتملة والمقاصة لها
    - يعرض الدرجات بعد المقاصة
    - يحدد أهلية الطالب للمقاصة حسب المواد الراسبة
    """
    results = {
        'table_data': [], 
        'failed_subjects_count': 0, 
        'allowed_failure_subjects': 0, 
        'is_eligible': True, 
        'error': None
    }
    try:
        # جلب مستوى الطالب مع علاقاته
        sl = StudentLevel.objects.select_related(
            'fk_student_batch__fk_batch__fk_specialization', 
            'fk_student_batch__fk_student', 
            'fk_level'
        ).get(pk=student_level_id)
        student = sl.fk_student_batch.fk_student
        old_spec = sl.fk_student_batch.fk_batch.fk_specialization
        
        # جلب أحدث دفعة للتخصص الجديد
        new_batch = Batch.objects.filter(fk_specialization_id=new_specialization_id).order_by('-id').first()
        if not new_batch: 
            return {**results, 'error': "لا توجد دفعات مسجلة للتخصص الجديد"}

        # ==========================
        # التحقق من أهلية المقاصة
        # ==========================
        failed_count = StudentSubject.objects.filter(
            fk_student_semester__fk_student_level=sl,
            results_status__in=[
                ResultStatusChoice.REMAINING, 
                ResultStatusChoice.ABSENCE, 
                ResultStatusChoice.DEPRIVATION
            ]
        ).count()
        results.update({
            'failed_subjects_count': failed_count,
            'allowed_failure_subjects': sl.fk_level.allowed_failure_subjects,
            'is_eligible': failed_count <= sl.fk_level.allowed_failure_subjects
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
        old_levels = StudentLevel.objects.filter(
            fk_student_batch__fk_student=student, 
            fk_student_batch__fk_batch__fk_specialization=old_spec
        ).order_by('fk_level__level')
        
        for level in old_levels:
            for ss in StudentSemester.objects.filter(fk_student_level=level).prefetch_related(
                'subjects__fk_semmester_subject__fk_subject', 
                'subjects__fk_semmester_subject__fk_grading_system_june'
            ):
                for subj in ss.subjects.all():
                    old_ss = subj.fk_semmester_subject
                    if old_ss.id in processed: 
                        continue
                    processed.add(old_ss.id)

                    # فقط المواد الناجحة أو المقاصة سابقًا
                    if subj.results_status not in [ResultStatusChoice.PASSED, ResultStatusChoice.CLEARANCE]: 
                        continue

                    # البحث عن المقاصة الرسمية
                    target = ClearingMaterials.objects.filter(
                        fk_semester_subject_from=old_ss, 
                        active=True, 
                        fk_semester_subject_to__fk_semester__fk_level__fk_batch__fk_specialization_id=new_specialization_id
                    ).select_related(
                        'fk_semester_subject_to__fk_subject', 
                        'fk_semester_subject_to__fk_grading_system_june'
                    ).first()
                    
                    # إذا لم توجد، البحث عن مادة معادلة
                    target_ss = target.fk_semester_subject_to if target else find_equivalent_subject(
                        old_ss.fk_subject, subs_by_code, subs_by_name
                    )
                    
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
        return results
    except Exception as e:
        return {**results, 'error': str(e)}

# ==========================
# تنفيذ المقاصة داخليًا وحفظ البيانات
# ==========================

def perform_internal_clearance(student_id, new_specialization_id, exempted_subject_ids=None):
    """
    تنفيذ المقاصة فعليًا:
    - نقل الطالب للتخصص الجديد
    - تطبيق المقاصة على المواد الناجحة
    - إضافة المواد المعفاة
    - تحديث الحالة الأكاديمية والمستوى الحالي
    """
    exempted_subject_ids = exempted_subject_ids or []
    try:
        with transaction.atomic():  # ضمان atomicity للمعاملة كاملة
            student = Student.objects.select_for_update().get(pk=student_id)
            new_batch = Batch.objects.filter(fk_specialization_id=new_specialization_id).order_by('-id').first()
            if not new_batch: 
                return {'success': False, 'error': 'لا توجد دفعات للتخصص الجديد'}
            
            old_sb = StudentBatch.objects.filter(fk_student=student, is_current=True).first() \
                     or StudentBatch.objects.filter(fk_student=student).order_by('-id').first()
            academic_year = AcademicYear.objects.filter(is_cournt=True).first() \
                            or AcademicYear.objects.order_by('-id').first()

            # تجهيز قاموس البحث للمواد الجديدة
            new_subs = SemesterSubject.objects.filter(
                fk_semester__fk_level__fk_batch=new_batch
            ).select_related('fk_subject', 'fk_grading_system_june')
            subs_by_code = {s.fk_subject.subject_code.strip().lower(): s for s in new_subs if s.fk_subject.subject_code}
            subs_by_name = {}
            for s in new_subs:
                if s.fk_subject.name_ar: subs_by_name[s.fk_subject.name_ar.strip().lower()] = s
                if s.fk_subject.name_en: subs_by_name[s.fk_subject.name_en.strip().lower()] = s

            # ==========================
            # مطابقة المواد القديمة مع الجديدة
            # ==========================
            cleared_subjects = []  # قائمة المواد المقاصة [(old_rec, target_ss, grade)]
            used_targets = set()
            
            old_subjects = StudentSubject.objects.filter(
                fk_student_semester__fk_student_level__fk_student_batch__fk_student=student,
                results_status__in=[ResultStatusChoice.PASSED, ResultStatusChoice.CLEARANCE]
            ).select_related('fk_semmester_subject__fk_subject', 'fk_semmester_subject__fk_grading_system_june')

            for old_rec in old_subjects:
                old_ss = old_rec.fk_semmester_subject
                # البحث عن المقاصة الرسمية
                rule = ClearingMaterials.objects.filter(
                    fk_semester_subject_from=old_ss, 
                    active=True, 
                    fk_semester_subject_to__fk_semester__fk_level__fk_batch=new_batch
                ).select_related('fk_semester_subject_to__fk_grading_system_june').first()
                target = rule.fk_semester_subject_to if rule else find_equivalent_subject(old_ss.fk_subject, subs_by_code, subs_by_name)

                if target and target.id not in used_targets:
                    used_targets.add(target.id)
                    grade = calculate_scaled_grade(
                        old_rec.total_grade, 
                        old_ss.fk_grading_system_june.grade_total, 
                        target.fk_grading_system_june.grade_total
                    )
                    cleared_subjects.append((old_rec, target, grade))

            # ==========================
            # إضافة المواد المعفاة
            # ==========================
            for sid in exempted_subject_ids:
                if sid not in used_targets:
                    if target := next((s for s in new_subs if s.id == sid), None):
                        used_targets.add(target.id)
                        cleared_subjects.append((None, target, 0))

            # ==========================
            # تحديد حالة كل مستوى
            # ==========================
            levels = Level.objects.filter(fk_batch=new_batch).order_by('level')
            level_status = {}
            current_level = None
            
            # Pre-calculate cleared counts per level
            cleared_by_level = {l.id: [c for c in cleared_subjects if c[1].fk_semester.fk_level_id == l.id] for l in levels}
            
            for level in levels:
                total_subs = SemesterSubject.objects.filter(fk_semester__fk_level=level).count()
                cleared_count = len(cleared_by_level[level.id])
                remaining = total_subs - cleared_count
                
                has_higher_clearance = any(len(cleared_by_level[l.id]) > 0 for l in levels if l.level > level.level)
                
                if remaining > level.allowed_failure_subjects and has_higher_clearance:
                    level_status[level.id] = LevelStudentsStatusChoices.SUSPENDED_WITH_COURSES
                else:
                    level_status[level.id] = LevelStudentsStatusChoices.APPROVED
                    current_level = level
                    # وضع المستويات الأعلى تحت المراجعة
                    for l in levels:
                        if l.level > level.level: 
                            level_status[l.id] = LevelStudentsStatusChoices.UNDER_REVIEW
                    break
            
            current_level = current_level or levels.first()

            # ==========================
            # إنشاء السجلات الجديدة
            # ==========================
            new_sb = StudentBatch.objects.create(
                fk_student=student, 
                fk_batch=new_batch, 
                fk_academic_year=academic_year, 
                fk_previous_batch=old_sb, 
                is_current=True, 
                accademic_status=AcademicStatus.APPROVED
            )
            StudentBatch.objects.filter(fk_student=student).exclude(id=new_sb.id).update(is_current=False)

            for level in levels:
                sl = StudentLevel.objects.create(
                    fk_student_batch=new_sb, 
                    fk_level=level, 
                    student_level_status=level_status[level.id], 
                    is_active=(level == current_level)
                )
                for sem in level.semester_set.all():
                    ss = StudentSemester.objects.create(
                        fk_student_level=sl, 
                        fk_semester=sem, 
                        student_semester_status=SemesterStudentsStatusChoices.APPROVED
                    )
                    
                    for old_rec, target, grade in cleared_by_level[level.id]:
                        if target.fk_semester_id == sem.id:
                            StudentSubject.objects.create(
                                fk_student_semester=ss, 
                                fk_semmester_subject=target, 
                                total_grade=grade, 
                                results_status=ResultStatusChoice.CLEARANCE, 
                                subject_status=SubjectStatusChoice.EXEMPT, 
                                fk_previous_result=old_rec
                            )
                            StudentsClearingMaterials.objects.create(
                                fk_student_batch_old=old_sb, 
                                fk_student_batch_new=new_sb, 
                                fk_semester_subject_from=old_rec.fk_semmester_subject if old_rec else None, 
                                fk_semester_subject_to=target, 
                                type=StudentsClearingMaterialsChoice.EXEMPTED if old_rec is None else StudentsClearingMaterialsChoice.CLEARED
                            )

            # تحديث بيانات الطالب الأساسية
            student.fk_current_specialization = new_specialization
            student.fk_current_level = current_level
            student.fk_current_semester = current_level.semester_set.order_by('name').first()
            student.student_status = StudentStatusChoices.ACTIVE
            student.save()

            return {
                'success': True, 
                'student_id': student.id, 
                'new_level': current_level.level, 
                'cleared_subjects': len(cleared_subjects)
            }

    except Exception as e: 
        return {'success': False, 'error': str(e)}

# ==========================
# معاينة تفصيلية للمقاصة بعد التنفيذ
# ==========================

def get_clearance_preview(student_id, new_specialization_id):
    """
    تجهيز البيانات التفصيلية لكل فصل وموضوع بعد المقاصة.
    - semesters: المواد المصنفة حسب الفصل والمستوى
    - remaining_subjects: المواد المتبقية
    - exempted_subjects: المواد المعفاة
    """
    try:
        student = Student.objects.select_related('fk_current_specialization').get(pk=student_id)
        new_batch = Batch.objects.filter(fk_specialization_id=new_specialization_id).order_by('-id').first()
        if not new_batch: 
            return {'success': False, 'error': 'لا توجد دفعة للتخصص الجديد'}

        # Fetch all subjects
        sem_subjects = SemesterSubject.objects.filter(
            fk_semester__fk_level__fk_batch=new_batch
        ).select_related('fk_subject', 'fk_semester__fk_level').order_by(
            'fk_semester__fk_level__level', 'fk_semester__name'
        )
        
        # Fetch clearance records
        clearance_recs = StudentsClearingMaterials.objects.filter(
            fk_student_batch_new__fk_student=student, 
            fk_student_batch_new__fk_batch=new_batch
        ).select_related('fk_semester_subject_to', 'fk_semester_subject_from__fk_subject')

        # Map student subjects by semester_subject_id
        student_subjects = StudentSubject.objects.filter(
            fk_student_semester__fk_student_level__fk_student_batch__fk_student=student,
            fk_student_semester__fk_student_level__fk_student_batch__fk_batch=new_batch
        ).select_related('fk_semmester_subject')
        ss_map = {ss.fk_semmester_subject_id: ss for ss in student_subjects}

        # Process Clearance
        cleared_map = {}
        exempted_ids = set()
        for rec in clearance_recs:
            if not rec.fk_semester_subject_to: continue
            tid = rec.fk_semester_subject_to.id
            if rec.type == StudentsClearingMaterialsChoice.CLEARED:
                ss = ss_map.get(tid)
                cleared_map[tid] = {
                    'old_subject_name': rec.fk_semester_subject_from.fk_subject.name_ar,
                    'grade': ss.total_grade if ss else None,
                    'hours': rec.fk_semester_subject_to.number_of_hours,
                    'estimate': ss.get_estimate_display() if ss and ss.estimate else None
                }
            elif rec.type == StudentsClearingMaterialsChoice.EXEMPTED:
                exempted_ids.add(tid)

        # Build Response
        semesters = {}
        remaining, exempted = [], []
        
        for ss in sem_subjects:
            sem_id = ss.fk_semester.id
            if sem_id not in semesters:
                semesters[sem_id] = {
                    'semester_name': ss.fk_semester.get_name_display(), 
                    'level': ss.fk_semester.fk_level.level, 
                    'subjects': []
                }
            
            info = cleared_map.get(ss.id)
            is_exempt = ss.id in exempted_ids
            
            if info:
                semesters[sem_id]['subjects'].append({
                    'id': ss.id, 
                    'name': ss.fk_subject.name_ar, 
                    'hours': ss.number_of_hours, 
                    'cleared_info': info, 
                    'is_exempted': False
                })
            elif is_exempt:
                exempted.append({'id': ss.id, 'name': ss.fk_subject.name_ar, 'hours': ss.number_of_hours})
            else:
                remaining.append({'id': ss.id, 'name': ss.fk_subject.name_ar, 'hours': ss.number_of_hours})

        return {
            'success': True,
            'student_info': {
                'name': student.full_name_ar,
                'old_specialization': StudentBatch.objects.filter(fk_student=student).first().fk_differentioation_batch.fk_specialization.name_ar,
                'new_specialization': new_batch.fk_specialization.name_ar
            },
            'semesters': sorted(semesters.values(), key=lambda x: (x['level'], x['semester_name'])),
            'remaining_subjects': remaining,
            'exempted_subjects': exempted
        }
    except Exception as e: 
        return {'success': False, 'error': str(e)}
