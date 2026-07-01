from django.utils.translation import gettext_lazy as _
from .core import BusinessRule, ValidationContext


class StrictDataConsistencyRule(BusinessRule):
    """
    قاعدة التوافق الصارم للبيانات (تعمل أولاً).
    الهدف: الرد بخطأ (Error) إذا حاول النظام أو المستخدم إرسال بيانات متناقضة،
    بدلاً من تصحيحها في الخفاء.

    ========================================================================
    [ملاحظات هامة لمطور الواجهة الأمامية - Frontend Developer]:
    يجب أن لا يسمح الفرونت إند للمستخدم بالوصول إلى هذه الأخطاء من الأساس، 
    وذلك بتطبيق القواعد التالية في الشاشة (UI) أثناء الإدخال:
    
    1. عند اختيار "المنصب" (Position):
       - يجب تحديد "نوع العمل" (JobTitle) تلقائياً بناءً على اسم المنصب (مع تجاهل 'ال' التعريف).
       - يجب تحديد "الفئة" (Category) تلقائياً لتكون متطابقة مع المنصب ونوع العمل.
       - يجب (تعطيل / Disable) حقل "نوع العمل" وحقل "الفئة" بحيث لا يمكن تغييرهما يدوياً!
       
    2. في حال كان الفرد ميداني وليس له منصب (أغلب الميدانيين):
       - يُترك حقل المنصب فارغاً (أو يُعطل إذا اختار نوع عمل لا يقبل منصباً).
       - عند اختيار "نوع العمل"، تتحدد "الفئة" تلقائياً وتُقفل.
       
    إذا فشل الفرونت إند في تطبيق هذا، فإن هذه القاعدة (StrictDataConsistencyRule) 
    في الباك إند ستتصدى للبيانات المتناقضة وترفض الحفظ وتعيد رسالة الخطأ النصية.
    ========================================================================
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        
        def normalize_ar(text: str) -> str:
            if not text: return ""
            # إزالة ال التعريف والمسافات لضمان التطابق بين "مدير الإدارة" و "مدير إدارة"
            return text.replace('ال', '').replace(' ', '')
            
        # 1. التوافق بين المنصب ونوع العمل
        if instance.position_id and instance.job_title_id:
            # يجب أن يكون نوع العمل يحمل نفس اسم المنصب متجاهلاً "ال"
            if normalize_ar(instance.job_title.name) != normalize_ar(instance.position.name):
                context.add_error(
                    'job_title',
                    _(f"تناقض في البيانات: لا يمكن اختيار نوع العمل '{instance.job_title.name}' مع المنصب '{instance.position.name}'. يجب أن يتطابقان.")
                )
                
        # 2. التوافق بين نوع العمل والفئة
        if instance.job_title_id and instance.category_id:
            if instance.category_id != instance.job_title.category_id:
                context.add_error(
                    'category',
                    _(f"تناقض في البيانات: نوع العمل '{instance.job_title.name}' يتبع فئة '{instance.job_title.category.name}'، ولا يمكن اختياره مع الفئة '{instance.category.name}'.")
                )


class PermanentDeactivationRule(BusinessRule):
    """
    قاعدة الحالات النهائية (الشهداء، الوفيات، المتقاعدين).
    المنطق الجديد (بناءً على طلب العميل العبقري):
    - لا يتم تفريغ (مسح) الإدارة أو القسم أو نوع العمل أبداً!
    - يجب أن يحتفظ الفرد بمكانه ومنصبه لكي نعرف تاريخه وأين كان يعمل.
    - خروج الفرد من (القوة الفعلية) سيتم برمجياً في الـ Views/Dashboards 
      عن طريق استبعاد أي فرد حالته النهائية (شهيد/متوفي/متقاعد) من الإحصائيات.
    """
    def execute(self, context: ValidationContext) -> None:
        # لم يعد هناك حاجة لمسح البيانات، نحتفظ بها للتاريخ
        pass


class RankCategoryCompatibilityRule(BusinessRule):
    """
    قاعدة التوافق بين الرتبة والفئة.
    المرجع: الدليل الإرشادي - السطر 182 ("لا يمكن أن يكون عميد وفئته حرفي").
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        if instance.current_rank_id and instance.category_id:
            rank = instance.current_rank
            cat_name = instance.category.name
            
            OFFICER_FORBIDDEN_CATEGORIES = ['حرفي']
            if rank.is_officer and cat_name in OFFICER_FORBIDDEN_CATEGORIES:
                context.add_error(
                    'category',
                    _(f'الرتبة "{rank.name}" (ضابط) لا تتوافق مع الفئة "{cat_name}". يجب اختيار فئة إدارية أو تخصصية أو فنية.')
                )


class PositionRequirementsRule(BusinessRule):
    """
    قاعدة متطلبات المنصب (الفئات المسموحة والحد الأدنى للرتبة).
    المرجع: الدليل الإرشادي - السطر 421.
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        if instance.position_id:
            pos = instance.position
            
            # 1. التحقق من الفئات المسموحة
            if pos.allowed_categories and instance.category_id:
                if instance.category.name not in pos.allowed_categories:
                    allowed = '، '.join(pos.allowed_categories)
                    context.add_error(
                        'category',
                        _(f'الفئة "{instance.category.name}" غير مسموحة لمنصب "{pos.name}". الفئات المسموحة: {allowed}')
                    )
            
            # 2. التحقق من الحد الأدنى للرتبة
            if pos.requires_rank_id and instance.current_rank_id:
                if instance.current_rank.order > pos.requires_rank.order:
                    context.add_error(
                        'position',
                        _(f'منصب "{pos.name}" يتطلب رتبة "{pos.requires_rank.name}" أو أعلى. الرتبة الحالية "{instance.current_rank.name}" أقل من المطلوب.')
                    )


class AdministrativePositionRule(BusinessRule):
    """
    منع إعطاء منصب إداري عالي لشخص فئته ميدانية صرفة.
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        if instance.position_id and instance.category_id:
            if instance.category.name == 'ميداني':
                if 'مدير' in instance.position.name or 'رئيس' in instance.position.name:
                    context.add_error(
                        'position',
                        _('لا يمكن تعيين منصب قيادي/إداري لشخص فئته ميدانية. يرجى تعديل الفئة أولاً.')
                    )


class MilitaryNumberPrefixRule(BusinessRule):
    """
    قاعدة البوادئ العسكرية وتصنيف القوة.
    - الضباط: يبدأ بـ 60
    - الأفراد: يبدأ بـ 7 أو 50
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        
        # 1. التوافق بين البادئة والرتبة
        if instance.military_number and instance.current_rank_id:
            prefix = instance.military_number[:2]
            first_digit = instance.military_number[0]
            is_officer_rank = instance.current_rank.is_officer
            
            if prefix == '60' and not is_officer_rank:
                context.add_error(
                    'current_rank',
                    _('الرقم العسكري يبدأ بـ 60 (ضابط) لكن الرتبة المختارة هي رتبة أفراد. يجب اختيار رتبة ضباط.')
                )
            
            if first_digit in ('7', '5') and prefix != '60' and is_officer_rank:
                context.add_error(
                    'current_rank',
                    _(f'الرقم العسكري يبدأ بـ {prefix} (أفراد) لكن الرتبة المختارة هي رتبة ضباط. يجب اختيار رتبة أفراد.')
                )
        
        # 2. التوافق بين تصنيف القوة والرتبة
        if instance.force_classification_id and instance.current_rank_id:
            fc = instance.force_classification
            is_officer_rank = instance.current_rank.is_officer
            
            if fc.rank_type == 'officer' and not is_officer_rank:
                context.add_error(
                    'force_classification',
                    _(f'تصنيف القوة "{fc.name}" مخصص للضباط، لكن الرتبة الحالية هي رتبة أفراد.')
                )
            elif fc.rank_type == 'personnel' and is_officer_rank:
                context.add_error(
                    'force_classification',
                    _(f'تصنيف القوة "{fc.name}" مخصص للأفراد، لكن الرتبة الحالية هي رتبة ضباط.')
                )


class NoStateOverlapRule(BusinessRule):
    """
    منع تداخل الحالات (No State Overlap).
    يضمن النظام عدم التداخل منطقياً (بما أنه يوجد current_status واحد).
    لكن هذه القاعدة تتأكد من أن البيانات الأساسية لا تتعارض، 
    مثل محاولة جعل الرتبة المعلقة مساوية للحالية، أو الرقم العسكري القديم مساوياً للحالي.
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        
        if instance.old_military_number and instance.old_military_number == instance.military_number:
            context.add_error(
                'old_military_number',
                _('الرقم العسكري القديم لا يمكن أن يكون نفس الرقم العسكري الحالي.')
            )
            
        if instance.pending_rank_id and instance.current_rank_id:
            if instance.pending_rank_id == instance.current_rank_id:
                context.add_error(
                    'pending_rank',
                    _('الرتبة المعلقة قيد التنفيذ لا يمكن أن تكون نفس الرتبة الحالية الفعالة.')
                )


class PositionImmutabilityRule(BusinessRule):
    """
    قاعدة منع التعديل اليدوي على نوع العمل والفئة لمن يمتلك منصباً.
    المرجع: "لا يمكن تغيير نوع العمل لمن لديه منصب"
    
    ========================================================================
    [ملاحظات هامة لمطور الواجهة الأمامية - Frontend Developer]:
    عند عرض بيانات فرد "مسجل مسبقاً" ولديه منصب في قاعدة البيانات:
    - يجب أن تكون حقول (نوع العمل) و (الفئة) في حالة (Disabled / Read-Only).
    - إذا أراد المستخدم تغيير نوع العمل، يجب عليه أولاً تفريغ (مسح) المنصب،
      حينها فقط تفتح الواجهة حقل (نوع العمل) للتعديل بحرية.
    ========================================================================
    """
    def execute(self, context: ValidationContext) -> None:
        instance = context.instance
        
        if instance.position_id and instance.pk:
            try:
                # نحصل على البيانات السابقة عبر Model.objects.get
                from systems.personnel.models import PersonnelMaster
                old = PersonnelMaster.objects.get(pk=instance.pk)
                # إذا المنصب لم يتغير → لا يسمح بتغيير job_title 
                if old.position_id == instance.position_id:
                    if old.job_title_id and instance.job_title_id != old.job_title_id:
                        context.add_error(
                            'job_title',
                            _('لا يمكن تغيير نوع العمل أثناء وجود منصب. قم بإزالة المنصب أولاً ثم غيّر نوع العمل.')
                        )
            except Exception:
                pass  # للفرد الجديد

