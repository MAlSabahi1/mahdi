"""
اختبار الدورة الكاملة - المهمة 2.9

دورة: تصدير → استيراد → مراجعة → قبول → إقفال الشهر
"""

import io
import uuid
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
import openpyxl

from core.models import GeoGovernorate, SecurityAdministration, CentralDepartment, GeoDistrict, Rank, ServiceStatus, Qualification
from systems.personnel.models import PersonnelMaster
from systems.services.models import (
    StagingRecord, ServiceEventLog, ExportLog, MonthlySnapshot
)
from systems.services.export_service import ExcelExportService
from systems.services.import_service import ExcelImportService
from systems.services.staging_review_service import StagingReviewService
from systems.services.monthly_snapshot_service import MonthlySnapshotService

User = get_user_model()


class FullCycleTestCase(TestCase):
    """اختبار الدورة الكاملة للخدمات الشهرية"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='chief', password='pass123', is_staff=True
        )

        self.governorate = GeoGovernorate.objects.create(name_ar='بغداد')
        self.security_admin = SecurityAdministration.objects.create(name='أمن العاصمة', geo_governorate=self.governorate)

        self.directorate = CentralDepartment.objects.create(
            code='TRAFFIC', name='إدارة المرور',
            security_admin=self.security_admin
        )

        self.rank = Rank.objects.create(name='نقيب', is_officer=True, order=8)

        self.status_active = ServiceStatus.objects.create(
            name='مباشر عمل', classification='active_full',
            receives_salary=True, requires_document=False
        )
        self.status_absent = ServiceStatus.objects.create(
            name='منقطع', classification='inactive_temp',
            receives_salary=False, requires_document=False
        )

        self.qualification = Qualification.objects.create(name='ثانوية', order=1)
        self.location = GeoDistrict.objects.create(name_ar='بغداد', governorate=self.governorate)

        self.personnel = PersonnelMaster.objects.create(
            military_number='5555555',
            national_id='55555555555',
            full_name='خالد عبد الله محمد',
            birth_date='1988-05-15',
            join_date='2008-01-01',
            current_rank=self.rank,
            central_department=self.directorate, security_admin=self.security_admin,
            current_status=self.status_active,
            qualification=self.qualification,
            geo_location=self.location
        )

    def test_full_export_import_review_approve_cycle(self):
        """
        الدورة الكاملة:
        1. تصدير ملف Excel محمي
        2. تعديل الملف (محاكاة إدارة)
        3. استيراد الملف المعدل
        4. مراجعة وقبول التغيير
        5. التحقق من تحديث PersonnelMaster
        """
        service_month = '2026-04'

        # === الخطوة 1: تصدير ===
        export_service = ExcelExportService(
            central_department=self.directorate,
            service_month=service_month,
            exported_by=self.user
        )
        excel_file, filename = export_service.export_and_log()

        # التحقق من التصدير
        self.assertTrue(filename.endswith('.xlsx'))
        self.assertTrue(ExportLog.objects.filter(
            central_department=self.directorate, security_admin=self.security_admin, service_month=service_month
        ).exists())

        # === الخطوة 2: محاكاة تعديل الإدارة ===
        # الحصول على UUID من ExportLog
        export_log = ExportLog.objects.get(
            central_department=self.directorate, security_admin=self.security_admin,
            service_month=service_month
        )
        row_uuid = export_log.row_uuids[0] if export_log.row_uuids else str(uuid.uuid4())
        
        # إنشاء ملف جديد يحاكي ما تعيده الإدارة
        modified_file = self._create_modified_excel(
            military_number='5555555',
            full_name='خالد عبد الله محمد',
            rank='نقيب',
            national_id='55555555555',
            current_status='مباشر عمل',
            proposed_status='منقطع',
            notes='غائب منذ أسبوعين',
            uuid=row_uuid
        )

        # === الخطوة 3: استيراد ===
        # الحصول على export_id من ExportLog
        export_log = ExportLog.objects.get(
            central_department=self.directorate, security_admin=self.security_admin,
            service_month=service_month
        )
        
        # قراءة محتوى الملف
        modified_file.seek(0)
        file_content = modified_file.read()
        
        import_service = ExcelImportService(
            file_content=file_content,
            export_id=str(export_log.export_id),
            imported_by=self.user,
            service_month=service_month
        )
        import_result = import_service.process()

        self.assertTrue(import_result['success'])
        self.assertEqual(import_result['stats']['changes_detected'], 1)

        # التحقق من StagingRecord
        staging = StagingRecord.objects.get(personnel=self.personnel)
        self.assertEqual(staging.status, 'pending')
        self.assertEqual(staging.proposed_change['status'], 'منقطع')

        # === الخطوة 4: مراجعة وقبول ===
        review_service = StagingReviewService(self.user)
        approve_result = review_service.approve_record(staging.id)

        self.assertTrue(approve_result['success'])
        self.assertEqual(approve_result['old_status'], 'مباشر عمل')
        self.assertEqual(approve_result['new_status'], 'منقطع')

        # === الخطوة 5: التحقق من النتائج ===
        self.personnel.refresh_from_db()
        self.assertEqual(self.personnel.current_status.name, 'منقطع')

        # التحقق من ServiceEventLog
        event = ServiceEventLog.objects.get(
            personnel=self.personnel,
            field_name='current_status'
        )
        self.assertEqual(event.old_value, 'مباشر عمل')
        self.assertEqual(event.new_value, 'منقطع')

        # === الخطوة 6 (اختيارية): إقفال الشهر ===
        snapshot_service = MonthlySnapshotService(self.user)
        close_result = snapshot_service.close_month(service_month, force=True)

        self.assertTrue(close_result['success'])
        self.assertTrue(MonthlySnapshotService.is_month_locked(service_month))

    def _create_modified_excel(self, **kwargs):
        """إنشاء ملف Excel معدل يحاكي ما تعيده الإدارة"""
        wb = openpyxl.Workbook()

        sheets = ['القوة العاملة', 'القوة غير العاملة', 'القوة كاملة', 'الغياب']
        headers = [
            'الرقم العسكري', 'الاسم الكامل', 'الرتبة',
            'الرقم الوطني', 'الحالة الحالية', 'متغير الشهر',
            'ملاحظات', '__UUID__'
        ]

        for i, sheet_name in enumerate(sheets):
            if i == 0:
                ws = wb.active
                ws.title = sheet_name
            else:
                ws = wb.create_sheet(sheet_name)

            ws.append(headers)

            # إضافة البيانات فقط في "القوة كاملة"
            if sheet_name == 'القوة كاملة':
                ws.append([
                    kwargs.get('military_number', ''),
                    kwargs.get('full_name', ''),
                    kwargs.get('rank', ''),
                    kwargs.get('national_id', ''),
                    kwargs.get('current_status', ''),
                    kwargs.get('proposed_status', ''),
                    kwargs.get('notes', ''),
                    kwargs.get('uuid', '')
                ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output
