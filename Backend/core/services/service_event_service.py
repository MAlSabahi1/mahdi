"""
Service Event Service — خدمة تسجيل أحداث الخدمة
═════════════════════════════════════════════════
واجهة صريحة لتسجيل أحداث تغيير بيانات الأفراد في ServiceEventLog.
"""
import logging
from typing import Any, Optional
from django.utils import timezone

logger = logging.getLogger('services')


class ServiceEventService:
    """
    خدمة تسجيل أحداث الخدمة المباشرة.
    
    الاستخدام:
        ServiceEventService.record_status_change(personnel, old_status, new_status, user)
        ServiceEventService.record_field_change(personnel, 'rank', old_val, new_val, user)
    """

    @staticmethod
    def record_status_change(
        personnel: Any,
        old_status: Any,
        new_status: Any,
        user: Any,
    ) -> None:
        """تسجيل تغيير حالة فرد في سجل الأحداث."""
        if not personnel or not new_status:
            return

        ServiceEventService._record(
            personnel=personnel,
            field_name='current_status',
            old_value=old_status.name if old_status else '',
            new_value=new_status.name,
            user=user,
        )

    @staticmethod
    def record_field_change(
        personnel: Any,
        field_name: str,
        old_value: str,
        new_value: str,
        user: Any,
    ) -> None:
        """تسجيل تغيير أي حقل آخر في بيانات الفرد."""
        if not personnel or not new_value:
            return

        ServiceEventService._record(
            personnel=personnel,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            user=user,
        )

    @staticmethod
    def _record(
        personnel: Any,
        field_name: str,
        old_value: str,
        new_value: str,
        user: Any,
    ) -> None:
        """الدالة الأساسية لإنشاء سجل حدث."""
        from systems.services.models import ServiceEventLog

        try:
            now = timezone.now()
            ServiceEventLog.objects.create(
                personnel=personnel,
                event_date=now.date(),
                service_month=now.strftime('%Y-%m'),
                field_name=field_name,
                old_value=old_value,
                new_value=new_value,
                created_by=user,
            )
            logger.debug(
                f"[ServiceEventService] Recorded '{field_name}' change for "
                f"{personnel.military_number}: '{old_value}' → '{new_value}'"
            )
        except Exception as e:
            # سجل الأحداث لا يجب أن يكسر العملية الأساسية
            logger.error(
                f"[ServiceEventService] Failed to record '{field_name}' change for "
                f"{personnel.military_number}: {e}"
            )
