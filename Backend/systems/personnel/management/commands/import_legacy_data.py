"""
Smart Migration Script - استيراد البيانات القديمة من Excel
"""
import uuid
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
import openpyxl
from systems.personnel.models import (
    PersonnelMaster, RawDataImport, SuggestedCorrection,
    HistoricalMonthlyVariables
)
from core.models import Rank, ServiceStatus, Qualification


class Command(BaseCommand):
    help = 'استيراد البيانات القديمة من ملف Excel'
    
    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='مسار ملف Excel')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='تشغيل تجريبي بدون حفظ البيانات'
        )
    
    def handle(self, *args, **options):
        excel_file = options['excel_file']
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS(f'بدء استيراد البيانات من: {excel_file}'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('تشغيل تجريبي - لن يتم حفظ البيانات'))
        
        # فتح ملف Excel
        try:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'خطأ في فتح الملف: {e}'))
            return
        
        # إنشاء معرف دفعة الاستيراد
        import_batch_id = uuid.uuid4()
        
        # قراءة الأعمدة من الصف الأول
        headers = []
        for cell in sheet[1]:
            headers.append(cell.value)
        
        self.stdout.write(f'عدد الأعمدة: {len(headers)}')
        self.stdout.write(f'الأعمدة: {", ".join([str(h) for h in headers if h])}')
        
        # إحصائيات
        stats = {
            'total_rows': 0,
            'created_personnel': 0,
            'updated_personnel': 0,
            'corrections_created': 0,
            'monthly_variables_created': 0,
            'errors': 0
        }
        
        # معالجة كل صف
        for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            stats['total_rows'] += 1
            
            # تحويل الصف إلى قاموس
            row_data = {}
            for i, value in enumerate(row):
                if i < len(headers) and headers[i]:
                    row_data[headers[i]] = value
            
            try:
                with transaction.atomic():
                    # الخطوة 1: حفظ البيانات الخام
                    if not dry_run:
                        RawDataImport.objects.create(
                            row_index=row_index,
                            raw_data=row_data,
                            import_batch_id=import_batch_id,
                            status='pending'
                        )
                    
                    # الخطوة 2: معالجة البيانات
                    result = self.process_row(row_data, row_index, dry_run)
                    
                    if result['created']:
                        stats['created_personnel'] += 1
                    elif result['updated']:
                        stats['updated_personnel'] += 1
                    
                    stats['corrections_created'] += result['corrections']
                    stats['monthly_variables_created'] += result['monthly_variables']
                    
            except Exception as e:
                stats['errors'] += 1
                self.stdout.write(
                    self.style.ERROR(f'خطأ في الصف {row_index}: {e}')
                )
                
                if not dry_run:
                    RawDataImport.objects.filter(
                        row_index=row_index,
                        import_batch_id=import_batch_id
                    ).update(
                        status='error',
                        error_message=str(e)
                    )
        
        # طباعة الإحصائيات
        self.stdout.write(self.style.SUCCESS('\n=== إحصائيات الاستيراد ==='))
        self.stdout.write(f'إجمالي الصفوف: {stats["total_rows"]}')
        self.stdout.write(f'أفراد جدد: {stats["created_personnel"]}')
        self.stdout.write(f'أفراد محدثين: {stats["updated_personnel"]}')
        self.stdout.write(f'اقتراحات تصحيح: {stats["corrections_created"]}')
        self.stdout.write(f'متغيرات شهرية: {stats["monthly_variables_created"]}')
        self.stdout.write(f'أخطاء: {stats["errors"]}')
        
        if not dry_run:
            self.stdout.write(f'\nمعرف الدفعة: {import_batch_id}')
            

            # إنشاء تقرير الفجوات
            self.generate_gap_report(import_batch_id)
    
    def process_row(self, row_data, row_index, dry_run):
        """معالجة صف واحد"""
        result = {
            'created': False,
            'updated': False,
            'corrections': 0,
            'monthly_variables': 0
        }
        
        # تحديد الرقم العسكري
        military_number = (
            row_data.get('الرقم العسكري الصحيح') or
            row_data.get('الرقم العسكري') or
            f'TEMP_{row_index}'
        )
        
        is_temporary = military_number.startswith('TEMP_')
        
        default_rank = Rank.objects.first()
        default_status = ServiceStatus.objects.first()

        # البحث عن الفرد أو إنشاؤه
        personnel, created = PersonnelMaster.objects.get_or_create(
            military_number=military_number,
            defaults={
                'full_name': row_data.get('الأسم', 'غير محدد'),
                'national_id': row_data.get('الرقم الوطني', '00000000000'),
                'birth_date': self.parse_date(row_data.get('تاريخ الميلاد')),
                'join_date': self.parse_date(row_data.get('تاريخ الالتحاق')),
                'is_data_clean': False,
                'data_quality_score': 0,
                'current_rank': default_rank,
                'current_status': default_status
            }
        ) if not dry_run else (None, True)
        
        result['created'] = created
        result['updated'] = not created
        
        if dry_run:
            return result
        
        # معالجة التصحيحات
        if row_data.get('تصحيح الأسم') and row_data['تصحيح الأسم'] != row_data.get('الأسم'):
            SuggestedCorrection.objects.create(
                personnel=personnel,
                field_name='full_name',
                old_value=row_data.get('الأسم', ''),
                new_value=row_data['تصحيح الأسم'],
                correction_type='name_correction',
                status='pending'
            )
            result['corrections'] += 1
        
        # معالجة المتغيرات الشهرية
        for key, value in row_data.items():
            if key and 'متغير' in str(key) and value:
                month = self.extract_month_from_column(key)
                if month:
                    HistoricalMonthlyVariables.objects.create(
                        personnel=personnel,
                        month=month,
                        variable_value=str(value),
                        source_column=key
                    )
                    result['monthly_variables'] += 1
        
        return result
    
    def parse_date(self, date_value):
        """تحويل التاريخ"""
        if not date_value:
            return timezone.now().date()
        
        if isinstance(date_value, datetime):
            return date_value.date()
            
        if isinstance(date_value, str):
            try:
                # Try parsing standard YYYY-MM-DD
                return datetime.strptime(date_value.strip(), '%Y-%m-%d').date()
            except ValueError:
                pass
        
        return timezone.now().date()
    
    def extract_month_from_column(self, column_name):
        """استخراج الشهر من اسم العمود"""
        # محاولة استخراج الشهر والسنة
        months = {
            'يناير': '01', 'فبراير': '02', 'مارس': '03', 'أبريل': '04',
            'مايو': '05', 'يونيو': '06', 'يوليو': '07', 'أغسطس': '08',
            'سبتمبر': '09', 'أكتوبر': '10', 'نوفمبر': '11', 'ديسمبر': '12'
        }
        
        for month_name, month_num in months.items():
            if month_name in column_name:
                # محاولة استخراج السنة
                year_match = re.search(r'20\d{2}', column_name)
                if year_match:
                    return f'{year_match.group()}-{month_num}'
        
        return None
    

    def generate_gap_report(self, import_batch_id):
        """إنشاء تقرير الفجوات"""
        self.stdout.write('\nإنشاء تقرير الفجوات...')
        
        missing_national_id = PersonnelMaster.objects.filter(
            Q(national_id__isnull=True) | Q(national_id='')
        ).count()
        
        invalid_national_id = PersonnelMaster.objects.exclude(
            Q(national_id__isnull=True) | Q(national_id='')
        ).exclude(national_id__regex=r'^\d{11}$').count()
        
        pending_corrections = SuggestedCorrection.objects.filter(
            status='pending'
        ).count()
        
        temporary_military_numbers = PersonnelMaster.objects.filter(
            military_number__startswith='TEMP_'
        ).count()
        
        self.stdout.write(f'\n=== تقرير الفجوات ===')
        self.stdout.write(f'أرقام وطنية ناقصة: {missing_national_id}')
        self.stdout.write(f'أرقام وطنية غير صحيحة: {invalid_national_id}')
        self.stdout.write(f'اقتراحات تصحيح معلقة: {pending_corrections}')
        self.stdout.write(f'أرقام عسكرية مؤقتة: {temporary_military_numbers}')
