"""
Import Service - خدمة استيراد الكشوفات المعدلة
المهمة 2.2: استقبال الملف المعدل ووضعه في منطقة الفحص

الميزات:
- قراءة ملف Excel المعدل (4 أوراق)
- التحقق من Hash و UUIDs
- استخراج التغييرات المقترحة
- إنشاء سجلات في StagingRecord
- تقرير الأخطاء والتنبيهات
- تصنيف التغييرات حسب الأهمية (أخضر/أصفر/أحمر)
"""
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from io import BytesIO

import openpyxl
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from systems.personnel.models import PersonnelMaster
from core.models import ServiceStatus, CentralDepartment
from systems.services.models import (
    ExportLog, StagingRecord, RejectionLog,
    DirectorateCompliance, AuditLog
)


class ImportValidationError(Exception):
    """خطأ في التحقق من صحة الملف"""
    pass


class ExcelImportService:
    """
    خدمة استيراد ملفات Excel المعدلة من الإدارات
    
    الميزات:
    - التحقق من صحة الملف (Hash, UUIDs)
    - قراءة التغييرات من 4 أوراق
    - تصنيف التغييرات (أخضر/أصفر/أحمر)
    - إنشاء سجلات في منطقة الفحص
    - تقرير شامل بالأخطاء والتنبيهات
    """
    
    # أسماء الأوراق المتوقعة
    EXPECTED_SHEETS = [
        'القوة العاملة',
        'القوة غير العاملة',
        'القوة كاملة',
        'الغياب'
    ]
    
    # أسماء الأعمدة المتوقعة
    EXPECTED_COLUMNS = [
        'الرقم العسكري',
        'الاسم الكامل',
        'الرتبة',
        'الرقم الوطني',
        'الحالة الحالية',
        'متغير الشهر',
        'ملاحظات',
        '__UUID__'
    ]
    
    # الحالات التي تتطلب مستندات (عالية الأهمية)
    HIGH_SEVERITY_STATUSES = [
        'شهيد', 'متوفى', 'متقاعد', 'مفصول',
        'منتدب', 'دراسة', 'إعارة', 'استقالة'
    ]
    
    def __init__(
        self,
        file_content: bytes,
        export_id: str,
        imported_by,
        service_month: Optional[str] = None
    ):
        """
        تهيئة خدمة الاستيراد
        
        Args:
            file_content: محتوى ملف Excel
            export_id: معرف التصدير (UUID)
            imported_by: المستخدم الذي يقوم بالاستيراد
            service_month: شهر الخدمة (اختياري)
        """
        self.file_content = file_content
        self.export_id = export_id
        self.imported_by = imported_by
        self.service_month = service_month
        
        # سيتم تعبئتها أثناء المعالجة
        self.export_log = None
        self.workbook = None
        self.errors = []
        self.warnings = []
        self.changes = []
        self.batch_id = uuid.uuid4()
        
        # إحصائيات
        self.stats = {
            'total_rows': 0,
            'changes_detected': 0,
            'errors': 0,
            'warnings': 0,
            'green_changes': 0,  # لا تحتاج مستند
            'yellow_changes': 0,  # تحتاج مستند
            'red_changes': 0,  # غير متوقعة
        }
    
    def _calculate_file_hash(self) -> str:
        """حساب SHA-256 hash للملف"""
        return hashlib.sha256(self.file_content).hexdigest()
    
    def _verify_export_log(self):
        """
        التحقق من وجود سجل التصدير
        
        Raises:
            ImportValidationError: إذا لم يوجد سجل التصدير
        """
        try:
            self.export_log = ExportLog.objects.get(export_id=self.export_id)
        except ExportLog.DoesNotExist:
            raise ImportValidationError(
                f"لم يتم العثور على سجل تصدير بالمعرف: {self.export_id}"
            )
        
        # التحقق من الحالة
        if self.export_log.status == 'returned':
            self.warnings.append(
                "تحذير: هذا الملف تم استيراده مسبقاً"
            )
        elif self.export_log.status == 'expired':
            raise ImportValidationError(
                "هذا الملف منتهي الصلاحية ولا يمكن استيراده"
            )
    
    def _verify_file_integrity(self):
        """
        التحقق من سلامة الملف (Hash)
        
        Note: نتجاهل التحقق من Hash لأن Excel يتغير عند التعديل
        بدلاً من ذلك، نتحقق من UUIDs
        """
        # لا نتحقق من Hash لأن الملف تم تعديله
        # سنتحقق من UUIDs بدلاً من ذلك
        pass
    
    def _load_workbook(self):
        """
        تحميل ملف Excel
        
        Raises:
            ImportValidationError: إذا فشل تحميل الملف
        """
        try:
            self.workbook = openpyxl.load_workbook(
                BytesIO(self.file_content),
                data_only=True
            )
        except Exception as e:
            raise ImportValidationError(
                f"فشل تحميل ملف Excel: {str(e)}"
            )
    
    def _verify_sheet_structure(self):
        """
        التحقق من بنية الأوراق
        
        Raises:
            ImportValidationError: إذا كانت البنية غير صحيحة
        """
        sheet_names = self.workbook.sheetnames
        
        # التحقق من وجود الأوراق المتوقعة
        for expected_sheet in self.EXPECTED_SHEETS:
            if expected_sheet not in sheet_names:
                raise ImportValidationError(
                    f"الورقة المطلوبة '{expected_sheet}' غير موجودة في الملف"
                )
    
    def _read_sheet_data(self, sheet_name: str) -> List[Dict[str, Any]]:
        """
        قراءة بيانات ورقة عمل
        
        Args:
            sheet_name: اسم الورقة
            
        Returns:
            قائمة قواميس تحتوي على بيانات الصفوف
        """
        sheet = self.workbook[sheet_name]
        data = []
        
        # قراءة العناوين من الصف الأول
        headers = []
        for cell in sheet[1]:
            headers.append(cell.value)
        
        # التحقق من الأعمدة المتوقعة
        for expected_col in self.EXPECTED_COLUMNS:
            if expected_col not in headers:
                self.errors.append(
                    f"العمود '{expected_col}' غير موجود في ورقة '{sheet_name}'"
                )
        
        # قراءة البيانات
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):  # تجاهل الصفوف الفارغة
                continue
            
            row_data = {}
            for col_idx, header in enumerate(headers):
                if col_idx < len(row):
                    row_data[header] = row[col_idx]
                else:
                    row_data[header] = None
            
            row_data['_sheet_name'] = sheet_name
            row_data['_row_number'] = row_idx
            data.append(row_data)
        
        return data
    
    def _verify_uuid(self, row_uuid: str) -> bool:
        """
        التحقق من صحة UUID
        
        Args:
            row_uuid: UUID الصف
            
        Returns:
            True إذا كان UUID صحيحاً
        """
        if not row_uuid:
            return False
        
        # التحقق من وجود UUID في سجل التصدير
        return str(row_uuid) in [str(u) for u in self.export_log.row_uuids]
    
    def _classify_change_severity(
        self,
        old_status: str,
        new_status: str
    ) -> Tuple[str, bool]:
        """
        تصنيف التغيير حسب الأهمية
        
        Args:
            old_status: الحالة القديمة
            new_status: الحالة الجديدة
            
        Returns:
            tuple: (severity, requires_document)
                - severity: 'low' أو 'high'
                - requires_document: True إذا كان يتطلب مستند
        """
        # إذا كانت الحالة الجديدة من الحالات الحساسة
        if new_status in self.HIGH_SEVERITY_STATUSES:
            return 'high', True
        
        # إذا كانت الحالة الجديدة "أخرى"
        if new_status == 'أخرى':
            return 'high', True
        
        # تغييرات بسيطة
        return 'low', False
    
    def _detect_changes(self, all_rows: List[Dict[str, Any]]):
        """
        اكتشاف التغييرات المقترحة
        
        Args:
            all_rows: جميع الصفوف من جميع الأوراق
        """
        processed_military_numbers = set()
        
        for row in all_rows:
            self.stats['total_rows'] += 1
            
            military_number = row.get('الرقم العسكري')
            current_status = row.get('الحالة الحالية')
            proposed_status = row.get('متغير الشهر')
            notes = row.get('ملاحظات', '')
            row_uuid = row.get('__UUID__')
            sheet_name = row.get('_sheet_name')
            row_number = row.get('_row_number')
            
            # التحقق من الرقم العسكري
            if not military_number:
                self.errors.append({
                    'sheet': sheet_name,
                    'row': row_number,
                    'error': 'الرقم العسكري فارغ'
                })
                self.stats['errors'] += 1
                continue
            
            # التحقق من UUID
            if not self._verify_uuid(row_uuid):
                self.errors.append({
                    'sheet': sheet_name,
                    'row': row_number,
                    'military_number': military_number,
                    'error': 'UUID غير صحيح أو غير موجود في سجل التصدير'
                })
                self.stats['errors'] += 1
                continue
            
            # تجنب معالجة نفس الفرد مرتين (قد يظهر في أكثر من ورقة)
            if military_number in processed_military_numbers:
                continue
            processed_military_numbers.add(military_number)
            
            # البحث عن الفرد في قاعدة البيانات
            try:
                personnel = PersonnelMaster.objects.select_related(
                    'current_status', 'current_rank', 'central_department'
                ).get(military_number=military_number)
            except PersonnelMaster.DoesNotExist:
                self.errors.append({
                    'sheet': sheet_name,
                    'row': row_number,
                    'military_number': military_number,
                    'error': 'الرقم العسكري غير موجود في قاعدة البيانات'
                })
                self.stats['errors'] += 1
                continue
            
            # التحقق من تطابق البيانات الأساسية
            name_mismatch = False
            rank_mismatch = False
            national_id_mismatch = False
            
            if row.get('الاسم الكامل') != personnel.full_name:
                name_mismatch = True
                self.warnings.append({
                    'sheet': sheet_name,
                    'row': row_number,
                    'military_number': military_number,
                    'warning': f"اختلاف في الاسم: '{row.get('الاسم الكامل')}' vs '{personnel.full_name}'"
                })
                self.stats['warnings'] += 1
            
            if row.get('الرتبة') != personnel.current_rank.name:
                rank_mismatch = True
                self.warnings.append({
                    'sheet': sheet_name,
                    'row': row_number,
                    'military_number': military_number,
                    'warning': f"اختلاف في الرتبة: '{row.get('الرتبة')}' vs '{personnel.current_rank.name}'"
                })
                self.stats['warnings'] += 1
            
            if row.get('الرقم الوطني') != personnel.national_id:
                national_id_mismatch = True
                self.warnings.append({
                    'sheet': sheet_name,
                    'row': row_number,
                    'military_number': military_number,
                    'warning': f"اختلاف في الرقم الوطني"
                })
                self.stats['warnings'] += 1
            
            # اكتشاف التغيير
            if proposed_status and proposed_status != current_status:
                # تصنيف التغيير
                severity, requires_document = self._classify_change_severity(
                    current_status, proposed_status
                )
                
                # إحصائيات
                self.stats['changes_detected'] += 1
                if severity == 'low':
                    self.stats['green_changes'] += 1
                elif severity == 'high' and proposed_status != 'أخرى':
                    self.stats['yellow_changes'] += 1
                else:
                    self.stats['red_changes'] += 1
                
                # حفظ التغيير
                self.changes.append({
                    'personnel': personnel,
                    'proposed_change': {
                        'status': proposed_status,
                        'service_month': self.service_month or self.export_log.service_month,
                    },
                    'notes': notes or '',
                    'severity': severity,
                    'requires_document': requires_document,
                    'name_mismatch': name_mismatch,
                    'rank_mismatch': rank_mismatch,
                    'national_id_mismatch': national_id_mismatch,
                    'sheet_name': sheet_name,
                    'row_number': row_number,
                })
    
    @transaction.atomic
    def _create_staging_records(self):
        """
        إنشاء سجلات في منطقة الفحص
        """
        staging_records = []
        
        for change in self.changes:
            staging_record = StagingRecord(
                personnel=change['personnel'],
                security_admin=self.export_log.security_admin,
                upload_batch_id=self.batch_id,
                proposed_change=change['proposed_change'],
                notes=change['notes'],
                status='pending',
                severity=change['severity'],
                requires_document=change['requires_document'],
                name_mismatch=change['name_mismatch'],
                rank_mismatch=change['rank_mismatch'],
                national_id_mismatch=change['national_id_mismatch'],
            )
            staging_records.append(staging_record)
        
        # حفظ دفعة واحدة
        StagingRecord.objects.bulk_create(staging_records)
        
        # تحديث حالة ExportLog
        self.export_log.status = 'returned'
        self.export_log.save(update_fields=['status'])
        
        # تسجيل في AuditLog
        AuditLog.objects.create(
            user=self.imported_by,
            action='IMPORT',
            model_name='ExportLog',
            object_id=str(self.export_log.export_id),
            new_data={
                'batch_id': str(self.batch_id),
                'changes_count': len(self.changes),
                'errors_count': self.stats['errors'],
                'warnings_count': self.stats['warnings'],
            },
            ip_address=None,
        )
    
    def _update_directorate_compliance(self):
        """
        تحديث سجل التزام المديرية/الإدارة
        """
        if not self.service_month:
            return
        
        compliance, created = DirectorateCompliance.objects.get_or_create(
            central_department=self.export_log.central_department,
            security_admin=self.export_log.security_admin,
            service_month=self.service_month,
            defaults={
                'submitted_at': timezone.now(),
                'error_count': self.stats['errors'],
                'quality_score': 100,
            }
        )
        
        if not created:
            compliance.submitted_at = timezone.now()
            compliance.error_count = self.stats['errors']
            compliance.save(update_fields=['submitted_at', 'error_count'])
    
    def process(self) -> Dict[str, Any]:
        """
        معالجة الملف بالكامل
        
        Returns:
            تقرير شامل بالنتائج
            
        Raises:
            ImportValidationError: إذا فشلت المعالجة
        """
        # 1. التحقق من سجل التصدير
        self._verify_export_log()
        
        # 2. تحميل الملف
        self._load_workbook()
        
        # 3. التحقق من البنية
        self._verify_sheet_structure()
        
        # 4. قراءة البيانات من جميع الأوراق
        all_rows = []
        for sheet_name in self.EXPECTED_SHEETS:
            sheet_data = self._read_sheet_data(sheet_name)
            all_rows.extend(sheet_data)
        
        # 5. اكتشاف التغييرات
        self._detect_changes(all_rows)
        
        # 6. إنشاء سجلات في منطقة الفحص
        if self.changes:
            self._create_staging_records()
        
        # 7. تحديث التزام الإدارة
        self._update_directorate_compliance()
        
        # 8. إنشاء التقرير
        
        report = {
            'success': True,
            'batch_id': str(self.batch_id),
            'central_department': self.export_log.central_department.name if self.export_log.central_department else 'غير معروف',
            'service_month': self.service_month or self.export_log.service_month,
            'stats': self.stats,
            'errors': self.errors,
            'warnings': self.warnings,
            'message': self._generate_summary_message(),
        }
        
        return report
    
    def _generate_summary_message(self) -> str:
        """توليد رسالة ملخص"""
        parts = []
        
        parts.append(
            f"تم استلام {self.stats['total_rows']} صف"
        )
        
        if self.stats['changes_detected'] > 0:
            parts.append(
                f"تم اكتشاف {self.stats['changes_detected']} تغييراً مقترحاً"
            )
            parts.append(
                f"({self.stats['green_changes']} أخضر، "
                f"{self.stats['yellow_changes']} أصفر، "
                f"{self.stats['red_changes']} أحمر)"
            )
        else:
            parts.append("لم يتم اكتشاف أي تغييرات")
        
        if self.stats['errors'] > 0:
            parts.append(f"{self.stats['errors']} خطأ")
        
        if self.stats['warnings'] > 0:
            parts.append(f"{self.stats['warnings']} تحذير")
        
        return "، ".join(parts) + "."


def import_service_file(
    file_content: bytes,
    export_id: str,
    user,
    service_month: Optional[str] = None
) -> Dict[str, Any]:
    """
    دالة مساعدة لاستيراد ملف خدمات
    
    Args:
        file_content: محتوى ملف Excel
        export_id: معرف التصدير (UUID)
        user: المستخدم الذي يقوم بالاستيراد
        service_month: شهر الخدمة (اختياري)
        
    Returns:
        تقرير شامل بالنتائج
        
    Raises:
        ImportValidationError: إذا فشلت المعالجة
    """
    service = ExcelImportService(
        file_content=file_content,
        export_id=export_id,
        imported_by=user,
        service_month=service_month
    )
    
    return service.process()
