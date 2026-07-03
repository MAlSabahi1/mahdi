"""
Audit Service — خدمة التدقيق المركزية
══════════════════════════════════════════
نقطة الدخول الوحيدة لتسجيل أي عملية تدقيق في النظام.

الاستخدام:
    from infra.audit.services.audit_service import AuditService

    AuditService.log_action(user, 'CREATE', 'Personnel', '123', new_data={...})
    AuditService.log_action(user, 'DELETE', 'Form', '456', change_reason='مذكرة رقم 789')

    # مساعدات جاهزة:
    AuditService.log_create(user, obj)
    AuditService.log_update(user, obj, old_data, new_data)
    AuditService.log_delete(user, obj)
"""
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger('audit')


class AuditService:
    """
    خدمة تدقيق مركزية — تخدم كل التطبيقات.

    القواعد:
        1. التدقيق لا يكسر العملية الأساسية — إذا فشل يسجل error ويكمل
        2. change_reason إجباري للعمليات الحساسة (DELETE, APPROVE, REJECT)
        3. كل سجل يُوقّع رقمياً تلقائياً (HMAC-SHA256)
    """

    # ══════════════════════════════════════════════════════════════
    # الدالة الأساسية — كل شيء يمر من هنا
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def log_action(
        user,
        action: str,
        model_name: str,
        object_id: str,
        old_data: Optional[Dict] = None,
        new_data: Optional[Dict] = None,
        change_reason: str = '',
        severity: str = 'info',
        module: str = '',
    ) -> None:
        """
        تسجيل عملية تدقيق عامة.

        Args:
            user:           المستخدم المنفذ
            action:         نوع العملية (CREATE, UPDATE, DELETE, APPROVE, etc.)
            model_name:     اسم النموذج
            object_id:      معرف الكائن
            old_data:       البيانات قبل التغيير
            new_data:       البيانات بعد التغيير
            change_reason:  سبب التغيير / رقم المذكرة
            severity:       مستوى الحساسية (info, low, medium, high, critical)
            module:         النظام الفرعي (personnel, services, security, etc.)
        """
        from infra.audit.models.audit_log import AuditLog

        try:
            AuditLog.objects.create(
                user=user if hasattr(user, 'pk') else None,
                action=action,
                model_name=model_name,
                object_id=str(object_id),
                old_data=old_data,
                new_data=new_data,
                change_reason=change_reason,
                severity=severity,
                module=module,
            )
            logger.debug(
                f"[AuditService] {action} on {model_name}#{object_id} "
                f"by {getattr(user, 'username', 'system')}"
            )
        except Exception as e:
            # التدقيق لا يكسر العملية الأساسية
            logger.error(
                f"[AuditService] Failed to log {action} on "
                f"{model_name}#{object_id}: {e}"
            )

    # ══════════════════════════════════════════════════════════════
    # مساعدات CRUD
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def log_create(
        user, obj: Any, new_data: Optional[Dict] = None,
        module: str = '', change_reason: str = '',
    ) -> None:
        """تسجيل عملية إنشاء."""
        AuditService.log_action(
            user=user, action='CREATE',
            model_name=obj.__class__.__name__,
            object_id=str(getattr(obj, 'pk', '')),
            new_data=new_data,
            module=module, change_reason=change_reason,
        )

    @staticmethod
    def log_update(
        user, obj: Any,
        old_data: Optional[Dict] = None,
        new_data: Optional[Dict] = None,
        change_reason: str = '', module: str = '',
    ) -> None:
        """تسجيل عملية تحديث."""
        AuditService.log_action(
            user=user, action='UPDATE',
            model_name=obj.__class__.__name__,
            object_id=str(getattr(obj, 'pk', '')),
            old_data=old_data, new_data=new_data,
            module=module, change_reason=change_reason,
        )

    @staticmethod
    def log_delete(
        user, obj: Any,
        old_data: Optional[Dict] = None,
        change_reason: str = '', module: str = '',
    ) -> None:
        """تسجيل عملية حذف — severity عالي تلقائياً."""
        AuditService.log_action(
            user=user, action='DELETE',
            model_name=obj.__class__.__name__,
            object_id=str(getattr(obj, 'pk', '')),
            old_data=old_data,
            severity='high', module=module,
            change_reason=change_reason,
        )

    # ══════════════════════════════════════════════════════════════
    # مساعدات Workflow / حالات
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def log_status_change(
        personnel: Any, old_status: Any, new_status: Any,
        user: Any, form: Any = None, change_reason: str = '',
    ) -> None:
        """تسجيل تغيير حالة فرد."""
        AuditService.log_action(
            user=user, action='STATUS_CHANGE',
            model_name=personnel.__class__.__name__,
            object_id=getattr(personnel, 'military_number', str(personnel.pk)),
            old_data={
                'status': getattr(old_status, 'name', str(old_status)) if old_status else '',
                'form_id': form.pk if form else None,
            },
            new_data={
                'status': getattr(new_status, 'name', str(new_status)) if new_status else '',
                'form_type': form.form_type if form else None,
            },
            severity='medium', module='personnel',
            change_reason=change_reason,
        )

    @staticmethod
    def log_approval(
        user: Any, obj: Any,
        old_state: str = '', new_state: str = '',
        change_reason: str = '',
    ) -> None:
        """تسجيل موافقة/اعتماد."""
        AuditService.log_action(
            user=user, action='APPROVE',
            model_name=obj.__class__.__name__,
            object_id=str(getattr(obj, 'pk', '')),
            old_data={'state': old_state},
            new_data={'state': new_state},
            severity='high', change_reason=change_reason,
        )

    @staticmethod
    def log_rejection(
        user: Any, obj: Any,
        reason: str = '', change_reason: str = '',
    ) -> None:
        """تسجيل رفض."""
        AuditService.log_action(
            user=user, action='REJECT',
            model_name=obj.__class__.__name__,
            object_id=str(getattr(obj, 'pk', '')),
            new_data={'rejection_reason': reason},
            severity='medium', change_reason=change_reason,
        )

    @staticmethod
    def log_export(
        user: Any, model_name: str,
        record_count: int = 0, export_format: str = '',
    ) -> None:
        """تسجيل عملية تصدير بيانات."""
        AuditService.log_action(
            user=user, action='EXPORT',
            model_name=model_name, object_id='bulk',
            new_data={
                'record_count': record_count,
                'format': export_format,
            },
            severity='medium',
        )

    # ══════════════════════════════════════════════════════════════
    # مساعدات تسجيل الدخول
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def log_login(
        user: Any = None, username: str = '',
        action: str = 'LOGIN_SUCCESS',
        failure_reason: str = '',
        extra_data: Optional[Dict] = None,
    ) -> None:
        """تسجيل حدث دخول/خروج."""
        from infra.audit.models.login_audit import LoginAuditLog

        try:
            LoginAuditLog.objects.create(
                user=user if hasattr(user, 'pk') else None,
                username_attempted=username or getattr(user, 'username', ''),
                action=action,
                failure_reason=failure_reason,
                extra_data=extra_data,
            )
        except Exception as e:
            logger.error(f"[AuditService] Failed to log login event: {e}")

    # ══════════════════════════════════════════════════════════════
    # استعلامات — للـ API
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_object_history(model_name: str, object_id: str, limit: int = 50):
        """تاريخ تغييرات كائن محدد — Timeline."""
        from infra.audit.models.audit_log import AuditLog
        return AuditLog.objects.filter(
            model_name=model_name,
            object_id=str(object_id),
        ).order_by('-timestamp')[:limit]

    @staticmethod
    def get_user_activity(user_id: str, limit: int = 100):
        """نشاط مستخدم محدد."""
        from infra.audit.models.audit_log import AuditLog
        return AuditLog.objects.filter(user_id=user_id).order_by('-timestamp')[:limit]

    @staticmethod
    def verify_integrity(audit_id: int) -> bool:
        """التحقق من سلامة سجل تدقيق (HMAC verification)."""
        from infra.audit.models.audit_log import AuditLog
        try:
            log = AuditLog.objects.get(pk=audit_id)
            return log.verify()
        except AuditLog.DoesNotExist:
            return False
