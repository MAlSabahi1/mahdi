"""
State Machine - محرك الحالات
"""
from django.db import transaction
from django_fsm import FSMField, transition
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StateTransitionError(Exception):
    """خطأ في الانتقال بين الحالات"""
    pass


class ServiceStateMachine:
    """
    محرك الحالات للأفراد - نسخة مبسطة للاختبارات
    """
    
    def can_transition(self, from_status, to_status, has_document=False):
        """التحقق من إمكانية الانتقال"""
        try:
            self.validate_transition(from_status, to_status, has_document)
            return True
        except StateTransitionError:
            return False
    
    def validate_transition(self, from_status, to_status, has_document=False):
        """التحقق من صحة الانتقال"""
        # التحقق من المستند المطلوب
        if to_status.requires_document and not has_document:
            raise StateTransitionError(
                f'الحالة "{to_status.name}" تتطلب رفع مستند رسمي'
            )
        
        # منع الانتقال من حالة نهائية
        if from_status.is_permanent_deactivation:
            raise StateTransitionError(
                'لا يمكن تغيير حالة فرد في حالة خروج نهائي'
            )
        
        return True


class PersonnelStateMachine:
    """
    محرك الحالات للأفراد
    يطبق قواعد الانتقال بين الحالات من قاعدة البيانات (StateTransitionRule)
    """
    
    @staticmethod
    def validate_document_required(personnel, new_status, document=None):
        """التحقق من وجود المستند المطلوب"""
        if new_status.requires_document and not document:
            raise ValidationError(
                _('الحالة "{}" تتطلب رفع مستند رسمي').format(new_status.name)
            )
    
    @staticmethod
    def validate_transition(from_status, to_status, user=None, document=None):
        """التحقق من صحة الانتقال بناءً على قواعد قاعدة البيانات"""
        from core.models import StateTransitionRule
        
        # منع الانتقال من حالة نهائية (صلبة في الكود كحماية إضافية)
        if from_status and from_status.is_permanent_deactivation:
            raise ValidationError(
                _('لا يمكن تغيير حالة فرد في حالة خروج نهائي')
            )
            
        # إذا لم يكن هناك حالة سابقة (تعيين جديد)
        if not from_status:
            return True
            
        try:
            rule = StateTransitionRule.objects.get(
                from_status=from_status,
                to_status=to_status,
                is_active=True
            )
        except StateTransitionRule.DoesNotExist:
            raise ValidationError(
                _('الانتقال من "{}" إلى "{}" غير مسموح أو غير معرف في النظام').format(
                    from_status.name, to_status.name
                )
            )
            
        # التحقق من المستندات إذا كانت مطلوبة
        if rule.requires_document and not document:
            raise ValidationError(
                _('هذا الانتقال يتطلب إرفاق مستند رسمي')
            )
            
        # التحقق من استمارة إثبات الحالة (في حال كانت مطلوبة، يجب أن تأتي من مسار آخر أو يتم التحقق منها هنا)
        # هذا التبسيط يفترض أن الاستمارة سيتم التعامل معها في الـ view
        
        return rule
    
    @staticmethod
    def change_status(personnel, new_status, document=None, user=None, notes=''):
        """
        تغيير حالة الفرد بشكل آمن باستخدام الخدمة الذرية
        """
        from systems.services.atomic_service import AtomicService
        
        old_status = personnel.current_status
        
        # 1. التحقق من صحة الانتقال
        PersonnelStateMachine.validate_transition(
            old_status,
            new_status,
            user=user,
            document=document
        )
        
        # 2. التنفيذ الآمن عبر الخدمة الذرية
        personnel, event = AtomicService.execute_status_change(
            personnel=personnel,
            new_status=new_status,
            user=user,
            document=document,
            notes=notes
        )
        
        return personnel
