from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime


class StatusTransitionError(Exception):
    """خطأ في انتقال الحالة — الانتقال غير مسموح"""
    pass


class AtomicService:
    """
    خدمة المعاملات الذرية المركزية
    تضمن تنفيذ جميع العمليات المترابطة (تغيير حالة، سجل أحداث، إشعارات، لقطات)
    في transaction واحد، لتجنب عدم اتساق البيانات (Data Inconsistency)
    """

    @classmethod
    def validate_transition(cls, from_status, to_status, user_priority=0):
        """
        التحقق من قاعدة الانتقال قبل التنفيذ
        
        Returns:
            StateTransitionRule إذا كان الانتقال مسموحاً
            
        Raises:
            StatusTransitionError إذا كان الانتقال ممنوعاً
        """
        from core.models import StateTransitionRule
        
        if from_status == to_status:
            return None  # لا يوجد تغيير
        
        try:
            rule = StateTransitionRule.objects.get(
                from_status=from_status,
                to_status=to_status,
                is_active=True
            )
        except StateTransitionRule.DoesNotExist:
            raise StatusTransitionError(
                f'الانتقال من "{from_status.name}" إلى "{to_status.name}" غير مسموح. '
                f'لا توجد قاعدة انتقال مُعرّفة لهذا المسار.'
            )
        
        if user_priority < rule.min_role_priority:
            raise StatusTransitionError(
                f'صلاحياتك غير كافية لتنفيذ هذا الانتقال. '
                f'الحد الأدنى المطلوب: {rule.min_role_priority}, صلاحياتك: {user_priority}'
            )
        
        return rule

    @classmethod
    @transaction.atomic
    def execute_status_change(cls, personnel, new_status, user, document=None, notes=''):
        """
        تغيير حالة الفرد بشكل ذري مع جميع الآثار الجانبية
        """
        from systems.services.models import ServiceEventLog, MonthlySnapshot
        from infra.audit.models import AuditLog
        from core.models import NotificationRecord
        
        # 0. التحقق من قاعدة الانتقال
        old_status = personnel.current_status
        user_priority = 0
        if hasattr(user, 'profile') and hasattr(user.profile, 'role'):
            user_priority = user.profile.role.priority
        
        rule = cls.validate_transition(old_status, new_status, user_priority)
        
        if rule:
            if rule.requires_document and not document:
                raise StatusTransitionError(
                    f'هذا الانتقال يتطلب مستنداً رسمياً ({", ".join(rule.required_document_types)})'
                )
            if rule.requires_dual_auth:
                raise StatusTransitionError(
                    f'هذا الانتقال يتطلب تفويضاً مزدوجاً (Four-Eyes). '
                    f'يرجى استخدام نظام التفويض المزدوج.'
                )
        
        # 1. تحديث الحالة
        personnel.current_status = new_status
        personnel.save(update_fields=['current_status', 'updated_at'])
        
        # 3. إنشاء حدث في السجل
        current_date = datetime.date.today()
        service_month = current_date.strftime('%Y-%m')
        
        event = ServiceEventLog.objects.create(
            personnel=personnel,
            governorate=personnel.governorate,
            event_date=current_date,
            service_month=service_month,
            field_name='current_status',
            old_value=str(old_status) if old_status else '',
            new_value=str(new_status),
            order_document=document,
            created_by=user
        )
        
        # 4. تحديث اللقطة الشهرية (إذا كانت موجودة ومفتوحة)
        # نحدث اللقطة إذا كان للفرد مديرية/إدارة عامة
        if personnel.directorate:
            try:
                snapshot = MonthlySnapshot.objects.select_for_update().get(
                    governorate=personnel.governorate,
                    directorate=personnel.directorate,
                    service_month=service_month,
                    locked=False
                )
                
                # تحديث بيانات الفرد في اللقطة
                # (هذا تبسيط، في الواقع نحتاج لتحديث المصفوفة أو القاموس حسب الهيكل)
                if 'personnel_updates' not in snapshot.data:
                    snapshot.data['personnel_updates'] = []
                
                snapshot.data['personnel_updates'].append({
                    'military_number': personnel.military_number,
                    'field': 'current_status',
                    'old_value': str(old_status) if old_status else '',
                    'new_value': str(new_status),
                    'timestamp': timezone.now().isoformat()
                })
                snapshot.save(update_fields=['data'])
            except MonthlySnapshot.DoesNotExist:
                pass # لا توجد لقطة مفتوحة أو لم تنشأ بعد
                
        # 5. تسجيل في Audit Log
        AuditLog.objects.create(
            user=user,
            governorate=personnel.governorate,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data={'status': old_status.name if old_status else None},
            new_data={'status': new_status.name, 'notes': notes},
            ip_address=None, # سيتم إضافته من مستوى الـ View إذا لزم
            timestamp=timezone.now()
        )
        
        # 6. إرسال إشعار للمدير/المسؤول (اختياري، مثلاً للحالات الحرجة)
        if new_status.classification in ['inactive_perm', 'inactive_temp']:
            NotificationRecord.objects.create(
                notification_type='status_change_approved',
                priority='high',
                target_governorate=personnel.governorate,
                target_directorate=personnel.directorate,
                personnel=personnel,
                title=f'تغيير حالة حرج للفرد {personnel.military_number}',
                message=f'تم تغيير حالة الفرد {personnel.full_name} إلى {new_status.name}',
            )
            
        return personnel, event
