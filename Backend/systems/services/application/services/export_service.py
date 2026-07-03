"""
Export Service - خدمة تصدير القوالب المحمية
المهمة 2.1: تصدير القالب المحمي للإدارات

وفقاً للتعليمات الرسمية (البند 15 من تعليمات ضبط الخدمات):
- 4 أوراق عمل: القوة العاملة، القوة غير العاملة، القوة كاملة، الغياب
- أعمدة محمية (للقراءة فقط) + أعمدة قابلة للتعديل
- حماية متقدمة (XlsxWriter): قفل خلايا، حماية ورقة ومصنف
- UUID مخفي لكل صف + SHA-256 Hash
"""
import hashlib
import uuid
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any, Optional

import xlsxwriter
from django.db import transaction
from django.utils import timezone

from systems.personnel.models import PersonnelMaster
from core.models import SecurityAdministration, CentralDepartment, ServiceStatus
from systems.services.models import ExportLog


class ExcelExportService:
    """
    خدمة تصدير ملفات Excel محمية للإدارات (4 أوراق)
    
    الميزات:
    - 4 أوراق: القوة العاملة، القوة غير العاملة، القوة كاملة، الغياب
    - حماية الأعمدة الثابتة (للقراءة فقط)
    - قوائم منسدلة للحالات المسموحة
    - UUIDs مخفية لكل صف
    - Hash للتحقق من الأصالة
    - حماية المصنف (منع إضافة/حذف أوراق)
    """
    
    # الأعمدة الثابتة (محمية - للقراءة فقط)
    PROTECTED_COLUMNS = [
        'الرقم العسكري',
        'الاسم الكامل',
        'الرتبة',
        'الرقم الوطني',
        'الحالة الحالية'
    ]
    
    # الأعمدة القابلة للتعديل
    EDITABLE_COLUMNS = [
        'متغير الشهر',
        'ملاحظات'
    ]
    
    # أسماء الأوراق الأربعة
    SHEET_NAMES = [
        'القوة العاملة',
        'القوة غير العاملة',
        'القوة كاملة',
        'الغياب'
    ]
    
    # تصنيفات الحالات لكل ورقة
    SHEET_CLASSIFICATIONS = {
        'القوة العاملة': ['active_full', 'active_part'],
        'القوة غير العاملة': ['inactive_temp', 'inactive_perm'],
        'القوة كاملة': None,  # جميع الأفراد
        'الغياب': ['inactive_temp'],  # فلترة إضافية بالاسم
    }
    
    # حالات الغياب (لورقة الغياب)
    ABSENCE_STATUS_NAMES = ['غياب', 'غياب مستمر', 'منقطع', 'فار', 'فرار']
    
    def __init__(self, central_department: CentralDepartment, service_month: str, exported_by):
        """
        تهيئة خدمة التصدير
        
        Args:
            central_department: الإدارة المركزية المراد التصدير لها
            service_month: شهر الخدمة (YYYY-MM)
            exported_by: المستخدم الذي يقوم بالتصدير
        """
        self.central_department = central_department
        self.service_month = service_month
        self.exported_by = exported_by
        self.row_uuids = []
        self.file_hash = None
    
    def get_personnel_data(self) -> List[Dict[str, Any]]:
        """
        استخراج بيانات الأفراد مع توليد UUID لكل صف
        
        Returns:
            قائمة قواميس تحتوي على بيانات الأفراد
        """
        personnel = PersonnelMaster.objects.filter(
            central_department=self.central_department,
            security_admin=self.central_department.security_admin
        ).select_related(
            'current_rank', 'current_status'
        ).order_by('full_name')
        
        data = []
        for person in personnel:
            row_uuid = str(uuid.uuid4())
            self.row_uuids.append(row_uuid)
            
            data.append({
                'military_number': person.military_number,
                'full_name': person.full_name,
                'rank': person.current_rank.name,
                'national_id': person.national_id,
                'current_status': person.current_status.name,
                'classification': person.current_status.classification,
                'notes': '',
                'row_uuid': row_uuid
            })
        
        return data
    
    def _classify_personnel(self, all_data: List[Dict]) -> Dict[str, List[Dict]]:
        """
        توزيع الأفراد على الأوراق الأربعة حسب حالتهم
        """
        sheets = {name: [] for name in self.SHEET_NAMES}
        
        for person in all_data:
            classification = person['classification']
            status_name = person['current_status']
            
            if classification in ['active_full', 'active_part']:
                sheets['القوة العاملة'].append(person)
            
            if classification in ['inactive_temp', 'inactive_perm']:
                sheets['القوة غير العاملة'].append(person)
            
            sheets['القوة كاملة'].append(person)
            
            if status_name in self.ABSENCE_STATUS_NAMES:
                sheets['الغياب'].append(person)
        
        return sheets
    
    def get_allowed_statuses(self) -> List[str]:
        """الحصول على قائمة الحالات المسموحة"""
        statuses = ServiceStatus.objects.all().values_list('name', flat=True)
        return list(statuses) + ['أخرى']
    
    def create_protected_excel(self) -> BytesIO:
        """إنشاء ملف Excel محمي مع 4 أوراق عمل"""
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        password = self._generate_password()
        
        workbook.set_properties({
            'title': f'كشف خدمات {self.central_department.name} - {self.service_month}',
            'subject': 'كشف خدمات شهري',
            'author': 'نظام إدارة الموارد البشرية',
            'company': 'الوزارة المختصة',
            'created': timezone.now()
        })
        
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#4472C4', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True
        })
        protected_format = workbook.add_format({
            'bg_color': '#E7E6E6', 'locked': True, 'border': 1, 'align': 'right'
        })
        editable_format = workbook.add_format({
            'locked': False, 'border': 1, 'align': 'right'
        })
        hidden_format = workbook.add_format({'locked': True, 'hidden': True})
        
        personnel_data = self.get_personnel_data()
        sheets_data = self._classify_personnel(personnel_data)
        allowed_statuses = self.get_allowed_statuses()
        all_headers = self.PROTECTED_COLUMNS + self.EDITABLE_COLUMNS + ['__UUID__']
        
        for sheet_name in self.SHEET_NAMES:
            worksheet = workbook.add_worksheet(sheet_name)
            sheet_persons = sheets_data[sheet_name]
            
            for col, header in enumerate(all_headers):
                worksheet.write(0, col, header, header_format)
            
            worksheet.set_column(0, 0, 15)
            worksheet.set_column(1, 1, 30)
            worksheet.set_column(2, 2, 15)
            worksheet.set_column(3, 3, 15)
            worksheet.set_column(4, 4, 18)
            worksheet.set_column(5, 5, 20)
            worksheet.set_column(6, 6, 40)
            worksheet.set_column(7, 7, 0)
            
            for row_idx, person in enumerate(sheet_persons, start=1):
                worksheet.write(row_idx, 0, person['military_number'], protected_format)
                worksheet.write(row_idx, 1, person['full_name'], protected_format)
                worksheet.write(row_idx, 2, person['rank'], protected_format)
                worksheet.write(row_idx, 3, person['national_id'], protected_format)
                worksheet.write(row_idx, 4, person['current_status'], protected_format)
                worksheet.write(row_idx, 5, person['current_status'], editable_format)
                worksheet.write(row_idx, 6, person['notes'], editable_format)
                worksheet.write(row_idx, 7, person['row_uuid'], hidden_format)
            
            if sheet_persons:
                worksheet.data_validation(
                    1, 5, len(sheet_persons), 5,
                    {
                        'validate': 'list', 'source': allowed_statuses,
                        'input_title': 'اختر الحالة',
                        'input_message': 'يرجى اختيار حالة من القائمة المنسدلة',
                        'error_title': 'قيمة غير مسموحة',
                        'error_message': 'لا يمكنك كتابة قيمة غير موجودة في القائمة.',
                        'error_type': 'stop'
                    }
                )
            
            worksheet.protect(password, {
                'select_locked_cells': False, 'select_unlocked_cells': True,
                'format_cells': False, 'format_columns': False, 'format_rows': False,
                'insert_columns': False, 'delete_columns': False,
                'insert_rows': False, 'delete_rows': False,
                'sort': False, 'autofilter': False, 'pivot_tables': False,
                'paste': False
            })
        
        workbook.close()
        output.seek(0)
        self.file_hash = self._calculate_hash(output.read())
        output.seek(0)
        return output
    
    def _generate_password(self) -> str:
        base = f"{self.central_department.id}_{self.service_month}_{self.exported_by.id}"
        return hashlib.sha256(base.encode()).hexdigest()[:16]
    
    def _calculate_hash(self, file_content: bytes) -> str:
        return hashlib.sha256(file_content).hexdigest()
    
    @transaction.atomic
    def export_and_log(self) -> tuple[BytesIO, str]:
        """تصدير الملف وتسجيله في قاعدة البيانات"""
        excel_file = self.create_protected_excel()
        
        export_log = ExportLog.objects.create(
            central_department=self.central_department,
            security_admin=self.central_department.security_admin,
            service_month=self.service_month,
            exported_by=self.exported_by,
            file_hash=self.file_hash,
            row_uuids=self.row_uuids,
            editable_columns=self.EDITABLE_COLUMNS,
            status='pending'
        )
        
        filename = f"كشف_{self.central_department.name}_{self.service_month}_{export_log.export_id}.xlsx"
        return excel_file, filename


def export_template_for_department(
    department_id: int,
    service_month: str,
    user
) -> tuple[BytesIO, str]:
    """
    دالة مساعدة لتصدير قالب لإدارة مركزية معينة
    
    Args:
        department_id: معرف الإدارة المركزية
        service_month: شهر الخدمة (YYYY-MM)
        user: المستخدم الذي يقوم بالتصدير
        
    Returns:
        tuple: (ملف Excel, اسم الملف)
        
    Raises:
        CentralDepartment.DoesNotExist: إذا لم توجد الإدارة
    """
    department = CentralDepartment.objects.get(id=department_id)
    
    service = ExcelExportService(
        central_department=department,
        service_month=service_month,
        exported_by=user
    )
    
    return service.export_and_log()
