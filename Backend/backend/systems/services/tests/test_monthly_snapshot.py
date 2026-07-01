"""
اختبارات اللقطة الشهرية وإقفال الشهر - المهمة 2.7
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import GeoGovernorate, SecurityAdministration, CentralDepartment, GeoDistrict, Rank, ServiceStatus, Qualification
from systems.personnel.models import PersonnelMaster
from systems.services.models import MonthlySnapshot, ExportLog, DirectorateCompliance
from systems.services.monthly_snapshot_service import (
    MonthlySnapshotService, MonthlySnapshotError
)

User = get_user_model()


class MonthlySnapshotTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='pass123', is_staff=True
        )

        self.governorate = GeoGovernorate.objects.create(name_ar='بغداد')
        self.security_admin = SecurityAdministration.objects.create(name='أمن العاصمة', geo_governorate=self.governorate)

        self.dept1 = CentralDepartment.objects.create(
            code='D01', name='إدارة المرور',
            security_admin=self.security_admin
        )
        self.dept2 = CentralDepartment.objects.create(
            code='D02', name='إدارة الجوازات',
            security_admin=self.security_admin
        )

        self.rank = Rank.objects.create(name='ملازم', is_officer=True, order=5)

        self.status_active = ServiceStatus.objects.create(
            name='مباشر عمل', classification='active_full',
            receives_salary=True, requires_document=False
        )
        self.status_inactive = ServiceStatus.objects.create(
            name='منقطع', classification='inactive_temp',
            receives_salary=False, requires_document=False
        )

        self.qualification = Qualification.objects.create(name='بكالوريوس', order=3)
        self.location = GeoDistrict.objects.create(name_ar='بغداد', governorate=self.governorate)

        # أفراد
        PersonnelMaster.objects.create(
            military_number='1111111', national_id='11111111111',
            full_name='أحمد', birth_date='1990-01-01', join_date='2010-01-01',
            current_rank=self.rank, central_department=self.dept1,
            current_status=self.status_active,
            qualification=self.qualification, geo_location=self.location
        )
        PersonnelMaster.objects.create(
            military_number='2222222', national_id='22222222222',
            full_name='محمد', birth_date='1992-01-01', join_date='2012-01-01',
            current_rank=self.rank, central_department=self.dept2,
            current_status=self.status_inactive,
            qualification=self.qualification, geo_location=self.location
        )

        self.service = MonthlySnapshotService(self.user)

    def test_check_completeness_none_submitted(self):
        """لا إدارة رفعت كشفها"""
        result = self.service.check_completeness('2026-03')
        self.assertEqual(result['not_submitted_count'], 2)
        self.assertFalse(result['is_complete'])

    def test_check_completeness_all_submitted(self):
        """جميع الإدارات رفعت"""
        ExportLog.objects.create(
            central_department=self.dept1, service_month='2026-03',
            exported_by=self.user, file_hash='abc', row_uuids=[],
            editable_columns=[], status='pending'
        )
        ExportLog.objects.create(
            central_department=self.dept2, service_month='2026-03',
            exported_by=self.user, file_hash='def', row_uuids=[],
            editable_columns=[], status='pending'
        )

        result = self.service.check_completeness('2026-03')
        self.assertTrue(result['is_complete'])

    def test_calculate_summaries(self):
        """حساب الخلاصات"""
        summaries = self.service.calculate_summaries('2026-03')

        self.assertIn('model_1', summaries)
        self.assertIn('model_2', summaries)
        self.assertIn('model_3', summaries)

        # نموذج 1: فرد واحد نشط في إدارة المرور
        self.assertIn('إدارة المرور', summaries['model_1'])

        # نموذج 3: فرد واحد غير عامل
        self.assertIn('منقطع', summaries['model_3'])

    def test_close_month_with_force(self):
        """إقفال الشهر بالقوة"""
        result = self.service.close_month('2026-03', force=True)

        self.assertTrue(result['success'])
        self.assertTrue(result['locked'])

        snapshot = MonthlySnapshot.objects.get(service_month='2026-03')
        self.assertTrue(snapshot.locked)

    def test_close_month_without_force_fails(self):
        """إقفال الشهر بدون force عند عدم اكتمال الرفع"""
        with self.assertRaises(MonthlySnapshotError) as ctx:
            self.service.close_month('2026-03', force=False)

        self.assertIn('إدارة لم ترفع', str(ctx.exception))

    def test_close_month_twice_fails(self):
        """محاولة إقفال الشهر مرتين"""
        self.service.close_month('2026-03', force=True)

        with self.assertRaises(MonthlySnapshotError):
            self.service.close_month('2026-03', force=True)

    def test_is_month_locked(self):
        """التحقق من إقفال الشهر"""
        self.assertFalse(MonthlySnapshotService.is_month_locked('2026-03'))

        self.service.close_month('2026-03', force=True)

        self.assertTrue(MonthlySnapshotService.is_month_locked('2026-03'))

    def test_validate_event_allowed_on_locked_month(self):
        """منع أحداث على شهر مغلق"""
        self.service.close_month('2026-03', force=True)

        with self.assertRaises(MonthlySnapshotError):
            MonthlySnapshotService.validate_event_allowed('2026-03')
