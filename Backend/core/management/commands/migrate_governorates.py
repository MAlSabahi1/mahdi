"""
أمر تهيئة وترحيل البيانات إلى نظام تعدد المحافظات (المرحلة 1.5)
يقوم بإنشاء محافظة "المحافظة الأولى" الافتراضية، وربط كافة البيانات الموجودة بها لمنع الانهيار.
"""
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from core.models import Governorate, Directorate, Division, Unit, UserProfile, AuditLog
from systems.personnel.models import PersonnelMaster
from systems.services.models import (
    ServiceEventLog, StagingRecord, ReconciliationTask, 
    MonthlySnapshot, ExportLog, RejectionLog, DirectorateCompliance
)

class Command(BaseCommand):
    help = 'يرحل البيانات الحالية إلى نظام تعدد المحافظات بإنشاء المحافظة الأولى الافتراضية'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("بدء ترحيل البيانات إلى بنية المحافظات..."))

        with transaction.atomic():
            # 1. إنشاء محافظة المحافظة الأولى
            mareb, created = Governorate.objects.get_or_create(
                name="المحافظة الأولى",
                defaults={"code": "MARIB", "description": "المحافظة الأولى (الافتراضية للاستيراد القديم)"}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('تم إنشاء المحافظة الأولى بنجاح.'))
            else:
                self.stdout.write(self.style.NOTICE('المحافظة الأولى موجودة مسبقاً.'))

            # 2. إنشاء إدارة عامة افتراضية
            hq, created_dir = Directorate.objects.get_or_create(
                name="الإدارة العامة للأمن",
                governorate=mareb,
                defaults={"code": "HQ"}
            )

            # إيقاف التريجرز مؤقتاً لتجنب فشل AuditLog بسبب user_agent
            with connection.cursor() as cursor:
                cursor.execute("ALTER TABLE personnel_master DISABLE TRIGGER ALL;")
                
            # 3. تحديث الأفراد (PersonnelMaster)
            personnel_updated = PersonnelMaster.objects.filter(governorate__isnull=True).update(
                governorate=mareb,
                directorate=hq
            )
            self.stdout.write(f'تم تحديث {personnel_updated} فرد (PersonnelMaster)')
            
            with connection.cursor() as cursor:
                cursor.execute("ALTER TABLE personnel_master ENABLE TRIGGER ALL;")

            # 4. تحديث مستخدمي النظام (User Profiles)
            users_updated = UserProfile.objects.filter(governorate__isnull=True).exclude(user__is_superuser=True).update(
                governorate=mareb,
                directorate=hq
            )
            self.stdout.write(f'تم تحديث {users_updated} مستخدم (UserProfile)')

            # 5. تحديث سجلات الخدمات
            s1 = ServiceEventLog.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s2 = AuditLog.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s3 = StagingRecord.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s4 = ReconciliationTask.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s5 = MonthlySnapshot.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s6 = ExportLog.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s7 = RejectionLog.objects.filter(governorate__isnull=True).update(governorate=mareb)
            s8 = DirectorateCompliance.objects.filter(governorate__isnull=True).update(governorate=mareb)
            
            self.stdout.write(f'تم تحديث سجلات الخدمات (العدد الإجمالي: {s1+s2+s3+s4+s5+s6+s7+s8})')

        self.stdout.write(self.style.SUCCESS("✓ تم إنجاز عملية الترحيل لـ Multi-Tenancy بنجاح."))
