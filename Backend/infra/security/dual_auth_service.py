"""
Dual Authorization Service - خدمة التفويض المزدوج (Four-Eyes)

العمليات فائقة الحساسية تتطلب موافقة مستخدمين اثنين:
- حذف فرد نهائياً
- إلغاء إقفال شهر
- تعديل صلاحيات super_admin
"""
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from infra.audit.services.audit_service import AuditService


class DualAuthError(Exception):
    """خطأ في التفويض المزدوج"""
    pass


class DualAuthorizationService:
    
    def __init__(self, user):
        self.user = user
    
    def create_request(self, action_type: str, target_object_type: str,
                       target_object_id: str, reason: str = '',
                       extra_data: dict = None) -> 'DualAuthorizationRequest':
        """
        إنشاء طلب تفويض مزدوج
        
        Args:
            action_type: نوع العملية (DELETE_PERSONNEL, UNLOCK_MONTH, ...)
            target_object_type: نوع الكائن (PersonnelMaster, MonthlySnapshot)
            target_object_id: معرف الكائن
            reason: سبب الطلب (إلزامي)
            extra_data: بيانات إضافية
        """
        from infra.security.models import DualAuthorizationRequest
        from infra.security.permissions import has_permission
        
        if not reason.strip():
            raise DualAuthError('يجب تحديد سبب الطلب')
        
        # التحقق من عدم وجود طلب معلق لنفس الكائن
        existing = DualAuthorizationRequest.objects.filter(
            action_type=action_type,
            target_object_id=target_object_id,
            status='pending'
        ).exists()
        
        if existing:
            raise DualAuthError(
                'يوجد طلب معلق بالفعل لنفس العملية'
            )
        
        request_data = {
            'reason': reason,
            **(extra_data or {})
        }
        
        request = DualAuthorizationRequest.objects.create(
            requester=self.user,
            action_type=action_type,
            target_object_type=target_object_type,
            target_object_id=target_object_id,
            request_data=request_data,
            status='pending',
        )
        
        # تسجيل عبر AuditService
        AuditService.log_action(
            user=self.user,
            action='CREATE',
            model_name='DualAuthorizationRequest',
            object_id=str(request.pk),
            new_data={
                'action_type': action_type,
                'target': target_object_id,
                'reason': reason,
            },
            severity='high', module='security',
            change_reason=reason,
        )
        
        return request
    
    @transaction.atomic
    def approve_request(self, request_id) -> dict:
        """
        الموافقة على طلب تفويض مزدوج
        
        الشروط:
        - الموافق ≠ الطالب
        - الموافق لديه صلاحية approve_dual_auth
        - الطلب لم ينتهِ
        """
        from infra.security.models import DualAuthorizationRequest
        
        try:
            request = DualAuthorizationRequest.objects.select_for_update().get(
                pk=request_id
            )
        except DualAuthorizationRequest.DoesNotExist:
            raise DualAuthError('الطلب غير موجود')
        
        if request.status != 'pending':
            raise DualAuthError(f'لا يمكن الموافقة: الطلب بحالة {request.status}')
        
        if request.is_expired():
            request.status = 'expired'
            request.save(update_fields=['status'])
            raise DualAuthError('انتهت صلاحية الطلب')
        
        if not request.can_be_approved_by(self.user):
            raise DualAuthError(
                'لا يمكنك الموافقة على هذا الطلب '
                '(يجب أن يكون الموافق مختلفاً عن الطالب ولديه صلاحية)'
            )
        
        # تنفيذ العملية
        result = self._execute_action(request)
        
        # تحديث الطلب
        request.approver = self.user
        request.status = 'executed'
        request.approved_at = timezone.now()
        request.executed_at = timezone.now()
        request.execution_result = result
        request.save()
        
        # تسجيل عبر AuditService
        AuditService.log_approval(
            user=self.user, obj=request,
            old_state='pending', new_state='executed',
            change_reason=f'Dual-auth approved by {self.user.username}',
        )
        
        return result
    
    def reject_request(self, request_id, reason: str = '') -> dict:
        """رفض طلب تفويض مزدوج"""
        from infra.security.models import DualAuthorizationRequest
        
        if not reason.strip():
            raise DualAuthError('يجب تحديد سبب الرفض')
        
        try:
            request = DualAuthorizationRequest.objects.get(pk=request_id)
        except DualAuthorizationRequest.DoesNotExist:
            raise DualAuthError('الطلب غير موجود')
        
        if request.status != 'pending':
            raise DualAuthError(f'لا يمكن الرفض: الطلب بحالة {request.status}')
        
        request.approver = self.user
        request.status = 'rejected'
        request.rejection_reason = reason
        request.save(update_fields=['approver', 'status', 'rejection_reason'])
        
        # تسجيل عبر AuditService
        AuditService.log_rejection(
            user=self.user, obj=request,
            reason=reason,
            change_reason=f'Dual-auth rejected: {reason}',
        )
        
        return {'success': True, 'status': 'rejected'}
    
    @staticmethod
    def expire_old_requests():
        """
        انتهاء الطلبات القديمة (تُشغل كمهمة مجدولة)
        """
        from infra.security.models import DualAuthorizationRequest
        
        expired = DualAuthorizationRequest.objects.filter(
            status='pending',
            expires_at__lt=timezone.now()
        ).update(status='expired')
        
        return {'expired_count': expired}
    
    @staticmethod
    def get_pending_requests(user=None):
        """جلب الطلبات المعلقة"""
        from infra.security.models import DualAuthorizationRequest
        
        qs = DualAuthorizationRequest.objects.filter(
            status='pending',
            expires_at__gt=timezone.now()
        ).select_related('requester')
        
        if user:
            # استبعاد طلبات المستخدم نفسه (لا يمكنه الموافقة عليها)
            qs = qs.exclude(requester=user)
        
        return qs
    
    def _execute_action(self, request) -> dict:
        """
        تنفيذ العملية بعد الموافقة
        """
        action = request.action_type
        
        if action == 'DELETE_PERSONNEL':
            return self._delete_personnel(request)
        elif action == 'UNLOCK_MONTH':
            return self._unlock_month(request)
        elif action == 'MODIFY_SUPER_ADMIN':
            return self._modify_super_admin(request)
        else:
            return {
                'success': True,
                'message': f'تم تنفيذ العملية: {action}'
            }
    
    def _delete_personnel(self, request) -> dict:
        """حذف فرد (أرشفة في جدول الظل ثم حذف)"""
        from systems.personnel.models import PersonnelMaster
        
        military_number = request.target_object_id
        
        try:
            personnel = PersonnelMaster.objects.get(
                military_number=military_number
            )
        except PersonnelMaster.DoesNotExist:
            return {'success': False, 'error': 'الفرد غير موجود'}
        
        # الحذف سيتم تسجيله تلقائياً في Shadow Table بواسطة Trigger
        name = personnel.full_name
        personnel.delete()
        
        return {
            'success': True,
            'deleted': military_number,
            'name': name,
        }
    
    def _unlock_month(self, request) -> dict:
        """إلغاء إقفال شهر"""
        from systems.services.models import MonthlySnapshot
        
        service_month = request.target_object_id
        
        updated = MonthlySnapshot.objects.filter(
            service_month=service_month,
            locked=True
        ).update(locked=False)
        
        return {
            'success': updated > 0,
            'unlocked_month': service_month,
            'snapshots_updated': updated,
        }
    
    def _modify_super_admin(self, request) -> dict:
        """تعديل صلاحيات مدير النظام"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        target_user_id = request.target_object_id
        new_data = request.request_data
        
        try:
            target_user = User.objects.get(pk=target_user_id)
        except User.DoesNotExist:
            return {'success': False, 'error': 'المستخدم غير موجود'}
        
        # تطبيق التعديلات
        if 'role_id' in new_data:
            from infra.authorization.models import Role
            try:
                new_role = Role.objects.get(pk=new_data['role_id'])
                target_user.profile.role = new_role
                target_user.profile.save(update_fields=['role'])
            except Exception as e:
                return {'success': False, 'error': str(e)}
        
        return {
            'success': True,
            'modified_user': target_user.username,
        }
