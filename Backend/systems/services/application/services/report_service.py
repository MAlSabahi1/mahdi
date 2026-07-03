"""
Report Generation Service - خدمة توليد التقارير
المرحلة 4 - المهمة 4.5: توليد التقارير الرسمية
"""
import os
import uuid
from io import BytesIO
from datetime import date

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from django.conf import settings
from django.db.models import Count, Q

from systems.personnel.models import PersonnelMaster
from systems.services.models import (
    AuditLog, RejectionLog, DirectorateCompliance,
    ReportTemplate,
)
from core.models import CentralDepartment


class ReportGenerationService:
    """خدمة توليد التقارير"""
    
    def __init__(self, user):
        self.user = user
    
    def generate(self, template_slug, filters, output_format='excel'):
        """
        توليد تقرير حسب القالب

        Args:
            template_slug: رمز القالب
            filters: معايير التصفية (month, directorate_id, etc.)
            output_format: تنسيق الإخراج ('excel' أو 'pdf')
        """
        generators = {
            'personnel_summary': self._generate_personnel_summary,
            'department_strength': self._generate_directorate_strength,
            'monthly_changes': self._generate_monthly_changes,
            'rejections_report': self._generate_rejections_report,
        }
        
        generator = generators.get(template_slug)
        if not generator:
            raise ValueError(f'قالب غير مدعوم: {template_slug}')
        
        content = generator(filters)
        
        # حفظ الملف
        file_name = f'{template_slug}_{uuid.uuid4().hex[:8]}.xlsx'
        file_path = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # تسجيل في AuditLog
        AuditLog.objects.create(
            user=self.user,
            action='EXPORT',
            model_name='ReportTemplate',
            object_id=template_slug,
            new_data={'filters': filters, 'format': output_format},
        )
        
        return {
            'file_path': file_path,
            'file_name': file_name,
            'file_url': f'{settings.MEDIA_URL}reports/{file_name}',
        }
    
    def _generate_personnel_summary(self, filters):
        """نموذج 1: ملخص الأفراد"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'ملخص الأفراد'
        ws.sheet_view.rightToLeft = True
        
        # عناوين
        headers = ['الرقم العسكري', 'الاسم الكامل', 'الرتبة', 'الإدارة', 'الحالة', 'المؤهل']
        header_font = Font(bold=True, size=12)
        for i, h in enumerate(headers, 1):
            cell = ws.cell(row=1, column=i, value=h)
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')
        
        qs = PersonnelMaster.objects.select_related(
            'current_rank', 'central_department', 'current_status', 'qualification'
        )
        
        dept_id = filters.get('directorate_id')
        if dept_id:
            qs = qs.filter(central_department_id=dept_id)
        
        for row_num, p in enumerate(qs, 2):
            ws.cell(row=row_num, column=1, value=p.military_number)
            ws.cell(row=row_num, column=2, value=p.full_name)
            ws.cell(row=row_num, column=3, value=p.current_rank.name if p.current_rank else '')
            ws.cell(row=row_num, column=4, value=p.central_department.name if p.central_department else '')
            ws.cell(row=row_num, column=5, value=p.current_status.name if p.current_status else '')
            ws.cell(row=row_num, column=6, value=p.qualification.name if p.qualification else '')
        
        output = BytesIO()
        wb.save(output)
        return output.getvalue()
    
    def _generate_directorate_strength(self, filters):
        """نموذج 2: قوة المديريات"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'قوة المديريات'
        ws.sheet_view.rightToLeft = True
        
        headers = ['المديرية', 'العدد الكلي', 'على رأس العمل', 'إجازة', 'منقطع', 'أخرى']
        for i, h in enumerate(headers, 1):
            cell = ws.cell(row=1, column=i, value=h)
            cell.font = Font(bold=True, size=12)
        
        directorates = CentralDepartment.objects.filter(is_active=True)
        
        for row_num, dept in enumerate(directorates, 2):
            personnel = PersonnelMaster.objects.filter(central_department=dept)
            total = personnel.count()
            active = personnel.filter(
                current_status__classification='active_full'
            ).count()
            leave = personnel.filter(
                current_status__classification='inactive_temp'
            ).count()
            absent = personnel.filter(
                current_status__classification__in=['absent', 'inactive_temp']
            ).exclude(current_status__classification='inactive_temp').count()
            other = total - active - leave - absent
            
            ws.cell(row=row_num, column=1, value=dept.name)
            ws.cell(row=row_num, column=2, value=total)
            ws.cell(row=row_num, column=3, value=active)
            ws.cell(row=row_num, column=4, value=leave)
            ws.cell(row=row_num, column=5, value=absent)
            ws.cell(row=row_num, column=6, value=other)
        
        output = BytesIO()
        wb.save(output)
        return output.getvalue()
    
    def _generate_monthly_changes(self, filters):
        """نموذج 3: التغييرات الشهرية"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'التغييرات الشهرية'
        ws.sheet_view.rightToLeft = True
        
        headers = ['الرقم العسكري', 'الاسم', 'الإدارة', 'التغيير', 'القيمة القديمة', 'القيمة الجديدة', 'التاريخ']
        for i, h in enumerate(headers, 1):
            ws.cell(row=1, column=i, value=h)
        
        from systems.services.models import ServiceEventLog
        month = filters.get('month', date.today().strftime('%Y-%m'))
        events = ServiceEventLog.objects.select_related(
            'personnel', 'personnel__central_department'
        ).filter(service_month=month)
        
        dept_id = filters.get('directorate_id')
        if dept_id:
            events = events.filter(personnel__central_department_id=dept_id)
        
        for row_num, event in enumerate(events, 2):
            ws.cell(row=row_num, column=1, value=event.personnel.military_number)
            ws.cell(row=row_num, column=2, value=event.personnel.full_name)
            ws.cell(row=row_num, column=3, value=event.personnel.central_department.name if event.personnel.central_department else '')
            ws.cell(row=row_num, column=4, value=event.field_name)
            ws.cell(row=row_num, column=5, value=event.old_value)
            ws.cell(row=row_num, column=6, value=event.new_value)
            ws.cell(row=row_num, column=7, value=str(event.event_date))
        
        output = BytesIO()
        wb.save(output)
        return output.getvalue()
    
    def _generate_rejections_report(self, filters):
        """نموذج 4: تقرير المرفوضات"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'المرفوضات'
        ws.sheet_view.rightToLeft = True
        
        headers = ['الرقم العسكري', 'الاسم', 'الإدارة', 'الحالة المقترحة', 'سبب الرفض', 'رفض بواسطة', 'التاريخ']
        for i, h in enumerate(headers, 1):
            ws.cell(row=1, column=i, value=h)
        
        qs = RejectionLog.objects.select_related(
            'personnel', 'central_department', 'rejected_by'
        ).all()
        
        month = filters.get('month')
        if month:
            qs = qs.filter(service_month=month)
        dept_id = filters.get('directorate_id')
        if dept_id:
            qs = qs.filter(central_department_id=dept_id)
        
        for row_num, rej in enumerate(qs, 2):
            ws.cell(row=row_num, column=1, value=rej.personnel.military_number)
            ws.cell(row=row_num, column=2, value=rej.personnel.full_name)
            ws.cell(row=row_num, column=3, value=rej.central_department.name)
            ws.cell(row=row_num, column=4, value=rej.proposed_status)
            ws.cell(row=row_num, column=5, value=rej.rejection_reason)
            ws.cell(row=row_num, column=6, value=rej.rejected_by.username if rej.rejected_by else '')
            ws.cell(row=row_num, column=7, value=str(rej.rejected_at))
        
        output = BytesIO()
        wb.save(output)
        return output.getvalue()
