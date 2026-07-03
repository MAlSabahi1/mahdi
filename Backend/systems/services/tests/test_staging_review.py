"""
اختبارات خدمة المراجعة والاعتماد - المهمة 2.3

تتحقق من:
- قبول تغيير أخضر → PersonnelMaster يتحدث + ServiceEventLog ينشأ
- قبول تغيير أصفر بدون مستند → يفشل
- رفض تغيير → RejectionLog ينشأ + DepartmentCompliance يتحدث
- رفض بدون سبب → يفشل
- قبول جماعي للتغييرات الخضراء
- إعادة فتح رفض خاطئ
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import GeoGovernorate, SecurityAdministration, CentralDepartment, GeoDistrict, Rank, ServiceStatus, Qualification
from systems.personnel.models import PersonnelMaster
from systems.services.models import (
    StagingRecord, ServiceEventLog, AuditLog,
    RejectionLog, DirectorateCompliance
)
from systems.services.staging_review_service import StagingReviewService, ReviewValidationError

User = get_user_model()


class StagingReviewTestCase(TestCase):
    """اختبارات خدمة المراجعة"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='reviewer', password='pass123', is_staff=True
        )

        self.governorate = GeoGovernorate.objects.create(name_ar='بغداد')
        self.security_admin = SecurityAdministration.objects.create(name='أمن العاصمة', geo_governorate=self.governorate)

        self.directorate = CentralDepartment.objects.create(
            code='DEP01', name='إدارة المرور',
            security_admin=self.security_admin
        )

        self.rank = Rank.objects.create(
            name='ملازم', is_officer=True, order=5
        )

        self.status_active = ServiceStatus.objects.create(
            name='مباشر عمل', classification='active_full',
            receives_salary=True, requires_document=False
        )

        self.status_absent = ServiceStatus.objects.create(
            name='منقطع', classification='inactive_temp',
            receives_salary=False, requires_document=False
        )

        self.status_martyr = ServiceStatus.objects.create(
            name='شهيد', classification='inactive_perm',
            receives_salary=False, requires_document=True
        )

        self.qualification = Qualification.objects.create(name='بكالوريوس', order=3)
        self.location = GeoDistrict.objects.create(name_ar='بغداد', governorate=self.governorate)

        self.personnel = PersonnelMaster.objects.create(
            military_number='1234567',
            national_id='12345678901',
            full_name='أحمد محمد علي',
            birth_date='1990-01-01',
            join_date='2010-01-01',
            current_rank=self.rank,
            central_department=self.directorate,
            current_status=self.status_active,
            qualification=self.qualification,
            geo_location=self.location
        )

        self.service = StagingReviewService(self.user)

    def _create_staging_record(self, status_name='منقطع', severity='low',
                                requires_document=False):
        """مساعد لإنشاء StagingRecord"""
        return StagingRecord.objects.create(
            personnel=self.personnel,
            upload_batch_id='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
            proposed_change={
                'status': status_name,
                'notes': 'ملاحظة اختبار',
                'service_month': '2026-03',
                'central_department_id': self.directorate.id
            },
            notes='ملاحظة اختبار',
            status='pending',
            severity=severity,
            requires_document=requires_document
        )

    def test_approve_low_severity_success(self):
        """قبول تغيير أخضر بنجاح"""
        record = self._create_staging_record()
        result = self.service.approve_record(record.id)

        self.assertTrue(result['success'])
        self.assertEqual(result['old_status'], 'مباشر عمل')
        self.assertEqual(result['new_status'], 'منقطع')

        # التحقق من تحديث PersonnelMaster
        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status.name, 'منقطع')

        # التحقق من ServiceEventLog
        event = ServiceEventLog.objects.get(personnel=self.personnel)
        self.assertEqual(event.old_value, 'مباشر عمل')
        self.assertEqual(event.new_value, 'منقطع')
        self.assertEqual(event.field_name, 'current_status')

        # التحقق من تحديث StagingRecord
        record.refresh_from_db()
        self.assertEqual(record.status, 'approved')
        self.assertEqual(record.reviewed_by, self.user)

        # التحقق من AuditLog
        self.assertTrue(AuditLog.objects.filter(
            model_name='PersonnelMaster',
            action='UPDATE'
        ).exists())

    def test_approve_high_severity_without_document_fails(self):
        """قبول تغيير أصفر بدون مستند → يفشل"""
        record = self._create_staging_record(
            status_name='شهيد', severity='high', requires_document=True
        )

        with self.assertRaises(ReviewValidationError) as ctx:
            self.service.approve_record(record.id)

        self.assertIn('مذكرة رسمية', str(ctx.exception))

        # التأكد أن PersonnelMaster لم يتغير
        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status.name, 'مباشر عمل')

    def test_approve_nonexistent_record_fails(self):
        """قبول سجل غير موجود → يفشل"""
        with self.assertRaises(ReviewValidationError):
            self.service.approve_record(99999)

    def test_reject_record_success(self):
        """رفض تغيير بنجاح"""
        record = self._create_staging_record()
        result = self.service.reject_record(record.id, 'بيانات غير صحيحة')

        self.assertTrue(result['success'])
        self.assertEqual(result['rejection_reason'], 'بيانات غير صحيحة')

        # التحقق من StagingRecord
        record.refresh_from_db()
        self.assertEqual(record.status, 'rejected')

        # التحقق من RejectionLog
        rejection = RejectionLog.objects.get(personnel=self.personnel)
        self.assertEqual(rejection.rejection_reason, 'بيانات غير صحيحة')
        self.assertEqual(rejection.central_department, self.directorate)

        # التحقق من DirectorateCompliance
        compliance = DirectorateCompliance.objects.get(
            central_department=self.directorate, service_month='2026-03'
        )
        self.assertEqual(compliance.rejected_changes_count, 1)

    def test_reject_without_reason_fails(self):
        """رفض بدون سبب → يفشل"""
        record = self._create_staging_record()

        with self.assertRaises(ReviewValidationError) as ctx:
            self.service.reject_record(record.id, '')

        self.assertIn('إلزامي', str(ctx.exception))

    def test_approve_all_low_severity(self):
        """قبول جماعي للتغييرات الخضراء"""
        # إنشاء شخصين إضافيين
        p2 = PersonnelMaster.objects.create(
            military_number='7654321',
            national_id='10987654321',
            full_name='محمد أحمد',
            birth_date='1992-01-01',
            join_date='2012-01-01',
            current_rank=self.rank,
            central_department=self.directorate,
            current_status=self.status_active,
            qualification=self.qualification,
            geo_location=self.location
        )

        batch_id = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'

        # سجل أخضر لكل واحد
        StagingRecord.objects.create(
            personnel=self.personnel,
            upload_batch_id=batch_id,
            proposed_change={'status': 'منقطع', 'service_month': '2026-03'},
            status='pending', severity='low', requires_document=False
        )
        StagingRecord.objects.create(
            personnel=p2,
            upload_batch_id=batch_id,
            proposed_change={'status': 'منقطع', 'service_month': '2026-04'},
            status='pending', severity='low', requires_document=False
        )

        result = self.service.approve_all_low_severity(batch_id=batch_id)

        self.assertEqual(result['approved_count'], 2)
        self.assertEqual(result['error_count'], 0)

        # التحقق من تحديث الحالات
        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status.name, 'منقطع')
        p2.refresh_from_db()
        self.assertEqual(p2.current_status.name, 'منقطع')

    def test_reopen_rejection(self):
        """إعادة فتح رفض خاطئ"""
        record = self._create_staging_record()

        # رفض أولاً
        self.service.reject_record(record.id, 'خطأ مني')

        # إعادة فتح
        rejection = RejectionLog.objects.get(staging_record=record)
        result = self.service.reopen_rejection(rejection.id)

        self.assertTrue(result['success'])

        # التحقق من وجود سجل جديد بحالة pending
        new_record = StagingRecord.objects.get(id=result['new_staging_id'])
        self.assertEqual(new_record.status, 'pending')
        self.assertEqual(new_record.personnel, self.personnel)

    def test_get_pending_records(self):
        """جلب السجلات المعلقة مع التصنيف"""
        self._create_staging_record(severity='low')
        self._create_staging_record(
            status_name='شهيد', severity='high', requires_document=True
        )

        pending = self.service.get_pending_records()

        self.assertEqual(pending['total'], 2)
        self.assertEqual(len(pending['low_severity']), 1)
        self.assertEqual(len(pending['high_severity']), 1)

    def test_personnel_not_changed_on_reject(self):
        """التأكد أن PersonnelMaster لا يتغير عند الرفض"""
        record = self._create_staging_record()
        self.service.reject_record(record.id, 'سبب')

        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status.name, 'مباشر عمل')

    def test_double_approve_fails(self):
        """محاولة قبول نفس السجل مرتين → يفشل"""
        record = self._create_staging_record()
        self.service.approve_record(record.id)

        with self.assertRaises(ReviewValidationError):
            self.service.approve_record(record.id)
