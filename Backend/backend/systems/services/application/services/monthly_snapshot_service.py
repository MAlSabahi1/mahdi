"""
خدمة اللقطة الشهرية وإقفال الشهر - المهمة 2.7

المسؤوليات:
1. التحقق من اكتمال رفع الكشوفات لجميع الإدارات
2. حساب خلاصات النماذج (1, 2, 3) باستعلامات تجميعية
3. إقفال الشهر وتخزين اللقطة (locked=True)
4. منع أي ServiceEventLog جديد لشهر مغلق
"""

from datetime import date, datetime
from typing import Dict, List, Optional

from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from core.models import SecurityAdministration, CentralDepartment, Branch, DistrictPolice, Rank, ServiceStatus
from systems.personnel.models import PersonnelMaster
from systems.services.models import (
    MonthlySnapshot,
    ExportLog,
    DirectorateCompliance,
    ServiceEventLog,
    StagingRecord,
    AuditLog
)


class MonthlySnapshotError(Exception):
    """خطأ في عملية اللقطة الشهرية"""
    pass


class MonthlySnapshotService:
    """
    خدمة إقفال الشهر وإنشاء اللقطات التاريخية
    """
    
    def __init__(self, user):
        self.user = user
    
    def check_completeness(self, service_month: str) -> Dict:
        """
        التحقق من اكتمال رفع الكشوفات لجميع الإدارات
        
        Args:
            service_month: الشهر بصيغة YYYY-MM
            
        Returns:
            قاموس: submitted, not_submitted, total, is_complete
        """
        security_admin = getattr(self.user, 'authz_profile', None) and self.user.authz_profile.security_admin
        # نجمع كل الوحدات التابعة (إدارات + فروع + أمن مديريات)
        if security_admin:
            dept_ids = list(CentralDepartment.objects.filter(security_admin=security_admin).values_list('id', flat=True))
            branch_ids = list(Branch.objects.filter(security_admin=security_admin).values_list('id', flat=True))
            dp_ids = list(DistrictPolice.objects.filter(security_admin=security_admin).values_list('id', flat=True))
        else:
            dept_ids = list(CentralDepartment.objects.values_list('id', flat=True))
            branch_ids = list(Branch.objects.values_list('id', flat=True))
            dp_ids = list(DistrictPolice.objects.values_list('id', flat=True))
        
        # الإدارات العامة التي رفعت كشفها
        submitted_dept_ids = set(
            ExportLog.objects.filter(
                service_month=service_month,
                status__in=['pending', 'returned']
            ).values_list('central_department_id', flat=True)
        )
        
        # جميع الإدارات المركزية
        all_departments = CentralDepartment.objects.filter(id__in=dept_ids)
        
        submitted = []
        not_submitted = []
        
        for dept in all_departments:
            if dept.id in submitted_dept_ids:
                submitted.append({
                    'id': dept.id,
                    'name': dept.name,
                    'code': dept.code or ''
                })
            else:
                not_submitted.append({
                    'id': dept.id,
                    'name': dept.name,
                    'code': dept.code or ''
                })
        
        return {
            'submitted': submitted,
            'not_submitted': not_submitted,
            'total': len(all_departments),
            'submitted_count': len(submitted),
            'not_submitted_count': len(not_submitted),
            'is_complete': len(not_submitted) == 0
        }
    
    def calculate_summaries(self, service_month: str) -> Dict:
        """
        حساب خلاصات النماذج الثلاثة
        
        Args:
            service_month: الشهر بصيغة YYYY-MM
            
        Returns:
            قاموس: model_1, model_2, model_3
        """
        # نموذج 1: القوة العاملة حسب الرتبة
        model_1 = self._calculate_model_1()
        
        # نموذج 2: القوة العاملة حسب الفئة (سيتم تنفيذه لاحقاً مع JobTitle)
        model_2 = self._calculate_model_2()
        
        # نموذج 3: القوة غير العاملة حسب الحالة والرتبة
        model_3 = self._calculate_model_3()
        
        return {
            'service_month': service_month,
            'calculated_at': timezone.now().isoformat(),
            'model_1': model_1,
            'model_2': model_2,
            'model_3': model_3
        }
    
    def _calculate_model_1(self) -> Dict:
        """
        نموذج 1: خلاصة القوة العاملة حسب الرتبة
        لكل إدارة × لكل رتبة → عدد الأفراد (active_full + active_part)
        """
        security_admin = getattr(self.user, 'authz_profile', None) and self.user.authz_profile.security_admin
        qs = PersonnelMaster.objects.filter(
            current_status__classification__in=['active_full', 'active_part']
        )
        if security_admin:
            qs = qs.filter(security_admin=security_admin)
            
        active_personnel = qs.values(
            'central_department__name', 'current_rank__name'
        ).annotate(count=Count('pk'))
        
        # تحويل إلى pivot table
        result = {}
        for item in active_personnel:
            dept_name = item['central_department__name'] or 'بدون إدارة/مديرية'
            rank_name = item['current_rank__name'] or 'بدون رتبة'
            
            if dept_name not in result:
                result[dept_name] = {}
            result[dept_name][rank_name] = item['count']
        
        return result
    
    def _calculate_model_2(self) -> Dict:
        """
        نموذج 2: القوة العاملة حسب الفئة الوظيفية
        (سيتم تنفيذه بالكامل بعد إنشاء JobTitle + JobCategory)
        """
        # حالياً نعيد التوزيع حسب الإدارة فقط
        security_admin = getattr(self.user, 'authz_profile', None) and self.user.authz_profile.security_admin
        qs = PersonnelMaster.objects.filter(
            current_status__classification__in=['active_full', 'active_part']
        )
        if security_admin:
            qs = qs.filter(security_admin=security_admin)
            
        active_by_dept = qs.values(
            'central_department__name'
        ).annotate(count=Count('pk'))
        
        return {
            item['central_department__name'] or 'بدون إدارة/مديرية': item['count']
            for item in active_by_dept
        }
    
    def _calculate_model_3(self) -> Dict:
        """
        نموذج 3: خلاصة القوة غير العاملة
        لكل حالة خدمية (inactive) × لكل رتبة → عدد
        """
        security_admin = getattr(self.user, 'authz_profile', None) and self.user.authz_profile.security_admin
        qs = PersonnelMaster.objects.filter(
            current_status__classification__in=['inactive_temp', 'inactive_perm']
        )
        if security_admin:
            qs = qs.filter(security_admin=security_admin)
            
        inactive_personnel = qs.values(
            'current_status__name', 'current_rank__name'
        ).annotate(count=Count('pk'))
        
        result = {}
        for item in inactive_personnel:
            status_name = item['current_status__name'] or 'بدون حالة'
            rank_name = item['current_rank__name'] or 'بدون رتبة'
            
            if status_name not in result:
                result[status_name] = {}
            result[status_name][rank_name] = item['count']
        
        return result
    
    @transaction.atomic
    def close_month(self, service_month: str, force: bool = False) -> Dict:
        """
        إقفال الشهر وإنشاء اللقطة
        
        Args:
            service_month: الشهر بصيغة YYYY-MM
            force: إجبار الإقفال حتى لو لم ترفع جميع الإدارات
            
        Returns:
            نتيجة الإقفال
        """
        security_admin = getattr(self.user, 'authz_profile', None) and self.user.authz_profile.security_admin
        # التحقق: هل الشهر مغلق مسبقاً في هذه المحافظة؟
        if MonthlySnapshot.objects.filter(
            service_month=service_month, locked=True, security_admin=security_admin
        ).exists():
            raise MonthlySnapshotError(
                f'الشهر {service_month} مغلق بالفعل لهذه المحافظة'
            )
        
        # التحقق من الاكتمال
        completeness = self.check_completeness(service_month)
        
        if not completeness['is_complete'] and not force:
            raise MonthlySnapshotError(
                f"{completeness['not_submitted_count']} إدارة لم ترفع كشفها بعد. "
                f"استخدم force=True للإجبار."
            )
        
        pending_qs = StagingRecord.objects.filter(
            status='pending',
            proposed_change__service_month=service_month
        )
        if security_admin:
            pending_qs = pending_qs.filter(security_admin=security_admin)
        pending_count = pending_qs.count()
        
        if pending_count > 0 and not force:
            raise MonthlySnapshotError(
                f'يوجد {pending_count} تغيير معلق لم تتم مراجعته بعد'
            )
        
        # حساب الخلاصات
        summaries = self.calculate_summaries(service_month)
        
        # إضافة إحصائيات الشهر
        summaries['statistics'] = {
            'departments_submitted': completeness['submitted_count'],
            'departments_total': completeness['total'],
            'departments_not_submitted': [d['name'] for d in completeness['not_submitted']],
            'pending_changes': pending_count,
            'forced': force
        }
        
        # إنشاء اللقطة الخاصة بالمحافظة (لا يوجد حقل unqiue=True على service_month لوحده بعد الآن للمحافظات المتعددة، أو يمكن إنشاؤها بحيث تكون خاصة للمحافظة)
        snapshot, created = MonthlySnapshot.objects.get_or_create(
            service_month=service_month,
            security_admin=security_admin,
            defaults={
                'data': summaries,
                'locked': True
            }
        )
        if not created:
            snapshot.data = summaries
            snapshot.locked = True
            snapshot.save(update_fields=['data', 'locked'])
        
        # تحديث DirectorateCompliance للإدارات المتأخرة
        if completeness['not_submitted']:
            for dept_info in completeness['not_submitted']:
                compliance, _ = DirectorateCompliance.objects.get_or_create(
                    central_department_id=dept_info['id'],
                    security_admin=security_admin,
                    service_month=service_month,
                    defaults={'quality_score': 100}
                )
                # حساب أيام التأخير
                try:
                    year, month = service_month.split('-')
                    deadline = date(int(year), int(month), 20)
                    today = date.today()
                    if today > deadline:
                        compliance.late_days = (today - deadline).days
                        compliance.save(update_fields=['late_days'])
                except (ValueError, TypeError):
                    pass
        
        # فجوة 4: حساب quality_score لجميع الإدارات
        self._recalculate_quality_scores(service_month)
        
        # AuditLog
        AuditLog.objects.create(
            user=self.user,
            action='CREATE',
            model_name='MonthlySnapshot',
            object_id=str(snapshot.id),
            new_data={
                'service_month': service_month,
                'locked': True,
                'forced': force
            }
        )

        # إنهاء صلاحية ملفات التصدير المعلقة للشهر المقفل
        # منع رفع أي ملف إكسل قديم لشهر تم إقفاله
        expired_qs = ExportLog.objects.filter(
            service_month=service_month,
            status='pending'
        )
        if security_admin:
            expired_qs = expired_qs.filter(security_admin=security_admin)
        expired_count = expired_qs.update(status='expired')

        return {
            'success': True,
            'service_month': service_month,
            'snapshot_id': snapshot.id,
            'locked': True,
            'summaries': summaries,
            'expired_export_logs': expired_count,
        }
    
    def _recalculate_quality_scores(self, service_month: str):
        """
        فجوة 4: حساب quality_score لجميع الإدارات في الشهر
        
        المعادلة:
        quality_score = 100 - (error_count * 2) - (rejected_changes_count * 5) - (late_days * 3)
        الحد الأدنى = 0
        """
        security_admin = getattr(self.user, 'authz_profile', None) and self.user.authz_profile.security_admin
        qs = DirectorateCompliance.objects.filter(
            service_month=service_month
        )
        if security_admin:
            qs = qs.filter(security_admin=security_admin)
            
        compliances = qs
        
        for compliance in compliances:
            penalty = (
                (compliance.error_count * 2) +
                (compliance.rejected_changes_count * 5) +
                (compliance.late_days * 3)
            )
            compliance.quality_score = max(0, 100 - penalty)
            compliance.save(update_fields=['quality_score'])
    
    @staticmethod
    def is_month_locked(service_month: str) -> bool:
        """التحقق من إقفال شهر معين"""
        return MonthlySnapshot.objects.filter(
            service_month=service_month,
            locked=True
        ).exists()
    
    @staticmethod
    def validate_event_allowed(service_month: str):
        """
        التحقق من أن الشهر مفتوح قبل إنشاء ServiceEventLog
        يُستدعى من ServiceEventLog.save() أو من signal
        
        Raises:
            MonthlySnapshotError: إذا كان الشهر مغلقاً
        """
        if MonthlySnapshotService.is_month_locked(service_month):
            raise MonthlySnapshotError(
                f'لا يمكن إضافة أحداث لشهر مغلق: {service_month}'
            )
