import io
import logging
from typing import List, Dict, Optional
import fitz  # PyMuPDF
from weasyprint import HTML

from django.template.loader import render_to_string
from infra.storage.models import Document
from core.models import CentralDepartment, SecurityAdministration

logger = logging.getLogger(__name__)

class PdfExportService:
    """
    خدمة توليد التقارير بصيغة PDF ودمج المرفقات الخاصة بها (للوزارة).
    يقوم بتوليد الكشف (النموذج) كملف PDF ثم إلحاق كافة المستندات الخاصة
    بالأفراد في نفس الملف في تسلسل احترافي.
    """
    def __init__(
        self, 
        service_month: str, 
        central_department: Optional[CentralDepartment] = None, 
        security_admin: Optional[SecurityAdministration] = None
    ):
        self.service_month = service_month
        self.central_department = central_department
        self.security_admin = security_admin

    def export_form_with_attachments(
        self, 
        form_title: str, 
        personnel_list: List[Dict], 
        context_types: Optional[List[str]] = None
    ) -> io.BytesIO:
        """
        توليد PDF مدمج:
        1. بناء الجدول (النموذج) باستخدام WeasyPrint.
        2. جمع المرفقات المرتبطة بكل فرد.
        3. تحويل الصور إلى PDF إن لزم الأمر، ودمج كل شيء في ملف واحد باستخدام PyMuPDF.
        
        Args:
            form_title: عنوان التقرير (مثل "القوة غير العاملة - وفيات")
            personnel_list: قائمة قواميس ببيانات الأفراد (military_number, full_name, rank, id, status_notes)
            context_types: أنواع السياقات المطلوبة للمرفقات (مثال: ['StatusChange_Death'])
        """
        # 1. تحديد اسم الجهة
        department_name = "الوزارة"
        if self.central_department:
            department_name = self.central_department.name
        elif self.security_admin:
            department_name = self.security_admin.name

        # 2. توليد الغلاف (النموذج) HTML -> PDF
        html_string = render_to_string('reports/monthly_form.html', {
            'form_title': form_title,
            'service_month': self.service_month,
            'department': department_name,
            'personnel_list': personnel_list
        })
        
        form_pdf_bytes = HTML(string=html_string).write_pdf()
        merged_pdf = fitz.open("pdf", form_pdf_bytes)

        # 3. دمج المرفقات
        if context_types and personnel_list:
            personnel_ids = [p.get('id') for p in personnel_list if p.get('id')]
            
            # جلب كافة المرفقات المعتمدة (committed) لهذا السياق وهؤلاء الأفراد
            docs = Document.objects.filter(
                personnel_id__in=personnel_ids,
                context_type__in=context_types,
                status='committed'
            ).order_by('personnel_id', 'created_at')

            for doc in docs:
                if not doc.file:
                    continue
                try:
                    file_path = doc.file.path
                    file_ext = doc.file.name.lower().split('.')[-1]
                    
                    if file_ext == 'pdf':
                        doc_pdf = fitz.open(file_path)
                        merged_pdf.insert_pdf(doc_pdf)
                        doc_pdf.close()
                    elif file_ext in ['png', 'jpg', 'jpeg']:
                        # تحويل الصورة لـ PDF ثم الدمج
                        img_doc = fitz.open(file_path)
                        pdf_bytes = img_doc.convert_to_pdf()
                        img_pdf = fitz.open("pdf", pdf_bytes)
                        merged_pdf.insert_pdf(img_pdf)
                        img_pdf.close()
                        img_doc.close()
                except Exception as e:
                    logger.error(f"Error merging document ID {doc.id}: {e}")

        # 4. إخراج الملف النهائي كـ BytesIO
        output_buffer = io.BytesIO()
        merged_pdf.save(output_buffer)
        merged_pdf.close()
        output_buffer.seek(0)
        
        return output_buffer
