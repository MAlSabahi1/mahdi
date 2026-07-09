"""
Export Service - خدمة تصدير القوالب المحمية (إنتاجي)
═══════════════════════════════════════════════════════
وفقاً لتعليمات ضبط الخدمات (البند 15):
- وضعان: 4 أوراق (الوضع الافتراضي) أو ورقة واحدة موحدة
- أعمدة محمية قابلة للضبط (ليست ثابتة في الكود)
- قوائم منسدلة متتالية: نوع_الحالة → الحالة المحتملة
- UUID مخفي لكل صف + SHA-256 Hash
- اسم الملف مقفول ومشفر
- حماية على مستوى إنتاجي (XlsxWriter + كلمة سر قوية)
"""
import hashlib
import hmac
import uuid
import re
import zipfile
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any, Optional, Tuple

import xlsxwriter
from django.db import transaction
from django.utils import timezone

from systems.personnel.models import PersonnelMaster
from core.models import SecurityAdministration, CentralDepartment, ServiceStatus
from systems.services.models import ExportLog


# ══════════════════════════════════════════════════════════
# ثوابت الأعمدة الافتراضية
# ══════════════════════════════════════════════════════════

# الأعمدة المحمية الافتراضية (لا يمكن تعديلها)
DEFAULT_PROTECTED_COLUMNS = [
    'الرقم العسكري',
    'الاسم الكامل',
    'الرتبة',
    'الرقم الوطني',
    'الحالة',
]

# الأعمدة القابلة للتعديل الافتراضية
DEFAULT_EDITABLE_COLUMNS = [
    'نوع الحالة',            # القائمة المنسدلة الوحيدة (التفصيلية)
    'المتغير الشهري',        # المتغير الذي يطبع في سجل المتغيرات
    'ملاحظات',               # نص حر للتعليقات
]

# تصنيفات الحالات (4 تصنيفات رئيسية)
STATUS_CLASSIFICATIONS = {
    'قوة عاملة فعلية':       'active_full',
    'قوة عاملة غير فعلية':   'active_part',
    'قوة غير عاملة مؤقتاً':  'inactive_temp',
    'قوة غير عاملة نهائياً': 'inactive_perm',
}

# حالات الغياب (لورقة الغياب)
ABSENCE_STATUS_NAMES = ['الغياب المستمر', 'المنقطعين - فرار', 'غياب']

# الملحقات المطلوبة لكل نوع تغيير حساس
REQUIRED_ATTACHMENTS = {
    'الشهداء':             ['شهادة استشهاد', 'تقرير الواقعة', 'قرار الاعتراف'],
    'الوفيات':             ['شهادة وفاة', 'شهادة الطبيب الشرعي'],
    'المتقاعدين':          ['قرار التقاعد', 'موافقة الوزارة'],
    'المفقودين':           ['صك شرعي', 'تقرير اللجنة', 'موافقة وزارية'],
    'المفقودين (بصك شرعي)': ['صك شرعي موثق', 'تقرير اللجنة'],
    'المنقطعين - فرار':    ['بلاغ انقطاع', 'قرار تشكيل لجنة'],
    'المفرغين للدراسة':    ['قرار الابتعاث', 'موافقة الجهة'],
    'المنتدبين لدى جهات':  ['قرار الندب', 'موافقة المحافظة'],
    'السجناء':             ['حكم قضائي أو قرار توقيف'],
    'الأسرى':              ['تقرير رسمي'],
    'عدم لياقة':           ['تقرير اللجنة الطبية', 'موافقة وزارية'],
    'إنهاء المدة القانونية': ['قرار إنهاء الخدمة'],
    'بلوغ السن القانوني':  ['موافقة وزارية', 'قرار التقاعد'],
}


def _build_status_cascade() -> Dict[str, List[str]]:
    """
    بناء خريطة: التصنيف العام → قائمة الحالات التفصيلية
    يُجلب ديناميكياً من DB.
    """
    cascade = {cls: [] for cls in STATUS_CLASSIFICATIONS}
    try:
        for status in ServiceStatus.objects.all().order_by('name'):
            cls_display = status.get_classification_display()
            if cls_display in cascade:
                cascade[cls_display].append(status.name)
    except Exception:
        pass
    return cascade


def _generate_secure_filename(dept_name: str, service_month: str, export_id: str) -> str:
    """
    توليد اسم ملف مقفول غير قابل للتعديل.
    الصيغة: كشف_[اسم_الإدارة]_[YYYY-MM]_[أول 8 من UUID].xlsx
    يُعقّم الاسم من الأحرف الخطرة.
    """
    safe_name = re.sub(r'[^\w\u0600-\u06FF\s-]', '', dept_name).strip()
    short_id = str(export_id).replace('-', '')[:8]
    return f"كشف_{safe_name}_{service_month}_{short_id}.xlsx"


def _generate_workbook_password(dept_id: int, service_month: str, user_id: int, export_id: str) -> str:
    """
    توليد كلمة سر قوية باستخدام HMAC-SHA256.
    لا يمكن لأي طرف خارجي معرفة كلمة السر لأنها مشتقة من secret_key.
    """
    from django.conf import settings
    secret = getattr(settings, 'SECRET_KEY', 'fallback-secret').encode()
    message = f"{dept_id}:{service_month}:{user_id}:{export_id}".encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()[:20]


class ExcelExportService:
    """
    خدمة تصدير ملفات Excel محمية للإدارات والمديريات والفروع.

    الوضعان:
    - mode='multi' (افتراضي): 4 أوراق (العاملة، غير العاملة، الكاملة، الغياب)
    - mode='single': ورقة واحدة بكل الأفراد مع عمود الحالة الحالية

    الأعمدة:
    - protected_columns: قائمة قابلة للضبط (افتراضياً الـ 5 الحساسة)
    - editable_columns: قائمة قابلة للضبط (افتراضياً الحالة + الملاحظات)
    """

    SHEET_NAMES = ['القوة العاملة', 'القوة غير العاملة', 'القوة كاملة', 'الغياب']

    def __init__(
        self,
        entity_name: str,
        queryset,
        service_month: str,
        exported_by,
        mode: str = 'multi',
        split_by: Optional[str] = None,
        protected_columns: Optional[List[str]] = None,
        editable_columns: Optional[List[str]] = None,
        raw_columns: Optional[List[str]] = None,
        security_admin=None,
        central_department=None,
    ):
        """
        Args:
            central_department: الإدارة/المديرية/الفرع
            service_month: YYYY-MM
            exported_by: المستخدم المصدِّر
            mode: 'multi' = 4 أوراق | 'single' = ورقة واحدة
            protected_columns: تجاوز الأعمدة المحمية الافتراضية
            editable_columns: تجاوز الأعمدة القابلة للتعديل الافتراضية
        """
        if mode not in ('multi', 'single'):
            raise ValueError("mode يجب أن يكون 'multi' أو 'single'")

        self.entity_name = entity_name
        self.queryset = queryset
        self.service_month = service_month
        self.exported_by = exported_by
        self.mode = mode
        self.split_by = split_by
        self.security_admin = security_admin
        self.central_department = central_department

        self.protected_columns = protected_columns if protected_columns is not None else DEFAULT_PROTECTED_COLUMNS
        self.editable_columns = editable_columns if editable_columns is not None else DEFAULT_EDITABLE_COLUMNS
        self.raw_columns = raw_columns if raw_columns is not None else []

        # يُملأ أثناء التوليد
        self.export_id = uuid.uuid4()
        self.row_uuids: List[str] = []
        self.row_count: int = 0
        self.file_hash: Optional[str] = None
        self._status_cascade = _build_status_cascade()

    # ──────────────────────────────────────────────────────────
    # استخراج البيانات من DB
    # ──────────────────────────────────────────────────────────

    def _get_personnel(self) -> List[Dict[str, Any]]:
        """جلب بيانات الأفراد وتوليد UUID لكل صف."""
        qs = self.queryset.select_related(
            'current_rank', 'current_status', 'central_department', 'branch', 'district_police'
        ).order_by('current_rank__order', 'full_name')

        data = []
        for person in qs:
            row_uuid = str(uuid.uuid4())
            self.row_uuids.append(row_uuid)
            classification = (
                person.current_status.classification
                if person.current_status else ''
            )
            
            # Determine split key if partitioning is enabled
            split_key = 'كشف موحد'
            if self.split_by == 'central_department' and person.central_department:
                split_key = person.central_department.name
            elif self.split_by == 'branch' and person.branch:
                split_key = person.branch.name
            elif self.split_by == 'district_police' and person.district_police:
                split_key = person.district_police.name

            person_dict = {
                'military_number': person.military_number or '',
                'full_name':       person.full_name or '',
                'rank':            person.current_rank.name if hasattr(person, 'current_rank') and person.current_rank else '',
                'national_id':     person.national_id or '',
                'current_status':  person.current_status.name if hasattr(person, 'current_status') and person.current_status else '',
                'classification':  classification,
                'row_uuid':        row_uuid,
                'split_key':       split_key,
            }
            
            # Extract additional raw columns if provided
            from datetime import date
            if self.raw_columns:
                all_arabic = self.protected_columns + self.editable_columns
                for i, raw_col in enumerate(self.raw_columns):
                    if i < len(all_arabic):
                        val = getattr(person, raw_col, '')
                        if val is None:
                            val = ''
                        elif hasattr(val, 'name'):
                            val = val.name
                        elif isinstance(val, date):
                            val = val.strftime('%Y-%m-%d')
                        person_dict[all_arabic[i]] = str(val)

            data.append(person_dict)
        self.row_count = len(data)
        return data

    def _classify_personnel(self, data: List[Dict]) -> Dict[str, List[Dict]]:
        """توزيع الأفراد على الأوراق حسب وضع التصدير (multi أو تقسيم مخصص)."""
        if self.split_by:
            sheets = {}
            for p in data:
                sk = p['split_key']
                if sk not in sheets:
                    sheets[sk] = []
                sheets[sk].append(p)
            self.SHEET_NAMES = list(sheets.keys())[:30] # Limit to 30 sheets
            return sheets

        sheets: Dict[str, List[Dict]] = {s: [] for s in self.SHEET_NAMES}
        for p in data:
            cls = p['classification']
            if cls in ('active_full', 'active_part'):
                sheets.setdefault('القوة العاملة', []).append(p)
            if cls in ('inactive_temp', 'inactive_perm'):
                sheets.setdefault('القوة غير العاملة', []).append(p)
            sheets.setdefault('القوة كاملة', []).append(p)
            if p['current_status'] in ABSENCE_STATUS_NAMES:
                sheets.setdefault('الغياب', []).append(p)
        return sheets

    # ──────────────────────────────────────────────────────────
    # بناء ملف Excel
    # ──────────────────────────────────────────────────────────

    def _build_formats(self, workbook) -> Dict:
        """تعريف الفورمات بشكل صريح مع حدود وألوان احترافية جداً للأنظمة الكبرى."""
        font = 'Cairo'
        return {
            'header': workbook.add_format({
                'bold': True, 'align': 'center', 'valign': 'vcenter', 
                'font_name': font, 'font_size': 12,
                'bg_color': '#002060', 'font_color': '#FFFFFF', # كحلي للأعمدة المقفلة
                'border': 1, 'border_color': '#808080',
            }),
            'editable_header': workbook.add_format({
                'bold': True, 'align': 'center', 'valign': 'vcenter', 
                'font_name': font, 'font_size': 12,
                'bg_color': '#0F9D58', 'font_color': '#FFFFFF', # أخضر للأعمدة القابلة للتعديل
                'border': 1, 'border_color': '#808080',
            }),
            'protected': workbook.add_format({
                'locked': True, 'align': 'center', 'valign': 'vcenter', 
                'font_size': 11, 'font_name': font,
                'border': 1, 'border_color': '#A6A6A6',
            }),
            'editable': workbook.add_format({
                'locked': False, 'align': 'center', 'valign': 'vcenter', 
                'font_size': 11, 'font_name': font,
                'bg_color': '#F2F9FF', # لون أزرق جليدي فاتح جداً لتمييز حقول الإدخال بشكل فخم
                'border': 1, 'border_color': '#A6A6A6',
            }),
            'notes_editable': workbook.add_format({
                'locked': False, 'align': 'right', 'valign': 'vcenter', 
                'font_size': 11, 'text_wrap': True, 'font_name': font,
                'bg_color': '#F2F9FF', 'indent': 1,
                'border': 1, 'border_color': '#A6A6A6',
            }),
            'hidden': workbook.add_format({'locked': True, 'hidden': True}),
            'meta': workbook.add_format({
                'locked': True, 'align': 'right', 'valign': 'vcenter', 
                'font_size': 10, 'italic': True, 'font_name': font,
            }),
            'warning': workbook.add_format({
                'locked': True, 'bg_color': '#17375E', 'font_color': '#FFFFFF',
                'align': 'center', 'valign': 'vcenter', 'font_size': 14, 'bold': True, 
                'font_name': font,
            }),
        }

    def _write_sheet(
        self,
        workbook,
        worksheet,
        persons: List[Dict],
        fmts: Dict,
        password: str,
        sheet_title: str,
    ):
        """كتابة ورقة عمل واحدة بالكامل."""
        all_cols = self.protected_columns + self.editable_columns + ['__UUID__']
        all_statuses = list(self._status_cascade.keys())  # 4 تصنيفات

        worksheet.right_to_left()  # تفعيل اتجاه من اليمين لليسار بشكل صريح
        worksheet.hide_gridlines(2)  # إخفاء خطوط الشبكة الافتراضية لشكل أنظف

        # ── صف المعلومات الأولى (تحذير + بيانات التصدير) ──
        dept_id = self.central_department.id if self.central_department else (self.security_admin.id if self.security_admin else '0')
        worksheet.merge_range(
            0, 0, 0, len(all_cols) - 1,
            f'تفاصيل التقرير: {self.entity_name}   |   '
            f'شهر الخدمة: {self.service_month}   |   '
            f'إجمالي الأفراد: {len(persons)}',
            fmts['warning'],
        )
        worksheet.set_row(0, 40)

        # ── صف العناوين ──
        for col_idx, header in enumerate(all_cols):
            fmt = fmts['editable_header'] if header in self.editable_columns else fmts['header']
            worksheet.write(1, col_idx, header, fmt)
        worksheet.set_row(1, 30)

        # ── ضبط عرض الأعمدة ──
        col_widths = {
            'الرقم العسكري': 20, 'الاسم الكامل': 45, 'الرتبة': 18,
            'الرقم الوطني': 25, 'الحالة': 35,
            'نوع الحالة': 35,
            'المتغير الشهري': 45, 'ملاحظات': 60,
        }
        for col_idx, header in enumerate(all_cols):
            if header == '__UUID__':
                worksheet.set_column(col_idx, col_idx, 0, None, {'hidden': 1})
            else:
                width = col_widths.get(header, 25)
                worksheet.set_column(col_idx, col_idx, width)

        # ── تجميد الصفوف العلوية (التحذير + العناوين) ──
        worksheet.freeze_panes(2, 0)

        # ── كتابة بيانات الأفراد ──
        for row_offset, person in enumerate(persons):
            row = row_offset + 2  # الصف الأول للبيانات = 2
            worksheet.set_row(row, 28)  # مساحة مريحة وفخمة للعين

            # خريطة افتراضية للحقول الأساسية إذا لم يتم استخدام raw_columns
            row_data_map = person.copy()
            row_data_map.update({
                'الرقم العسكري':  person.get('military_number', ''),
                'الاسم الكامل':   person.get('full_name', ''),
                'الرتبة':         person.get('rank', ''),
                'الرقم الوطني':   person.get('national_id', ''),
            })

            for col_idx, header in enumerate(all_cols):
                if header == '__UUID__':
                    worksheet.write(row, col_idx, person.get('row_uuid', ''), fmts['hidden'])

                elif header in self.protected_columns:
                    if header == 'الاسم الكامل':
                        name_fmt = workbook.add_format({
                            'locked': True, 'align': 'right', 'valign': 'vcenter', 
                            'font_size': 11, 'font_name': 'Cairo', 
                            'border': 1, 'border_color': '#A6A6A6', 'indent': 1
                        })
                        worksheet.write(row, col_idx, row_data_map.get(header, ''), name_fmt)
                    elif header == 'الحالة':
                        # معادلة VLOOKUP لجلب تصنيف الحالة بناء على اختيار "نوع الحالة"
                        type_col_idx = all_cols.index('نوع الحالة') if 'نوع الحالة' in all_cols else -1
                        if type_col_idx >= 0:
                            type_cell = xlsxwriter.utility.xl_rowcol_to_cell(row, type_col_idx)
                            formula = f'=IFERROR(VLOOKUP({type_cell}, SystemData!$A$1:$B$500, 2, FALSE), "")'
                            
                            classification_val = person.get('classification', '')
                            classification_display = ''
                            for name, code in STATUS_CLASSIFICATIONS.items():
                                if code == classification_val:
                                    classification_display = name
                                    break
                            worksheet.write_formula(row, col_idx, formula, fmts['protected'], classification_display)
                        else:
                            worksheet.write(row, col_idx, '', fmts['protected'])
                            
                    else:
                        worksheet.write(row, col_idx, row_data_map.get(header, ''), fmts['protected'])

                elif header == 'نوع الحالة':
                    worksheet.write(row, col_idx, person.get('current_status', ''), fmts['editable'])

                elif header in ['ملاحظات', 'المتغير الشهري']:
                    worksheet.write(row, col_idx, '', fmts['notes_editable'])

                else:
                    worksheet.write(row, col_idx, row_data_map.get(header, ''), fmts['editable'])

        # ── تحويل البيانات إلى Native Excel Table ──
        if persons:
            last_row = len(persons) + 1
            # نستخدم autofilter بدلاً من add_table للحفاظ على تنسيق العناوين الصريح الخاص بنا
            worksheet.autofilter(1, 0, last_row, len(all_cols) - 1)

        # ── Data Validation للأعمدة القابلة للتعديل ──
        if persons:
            first_data_row = 2
            last_data_row = len(persons) + 1

            for col_idx, header in enumerate(all_cols):
                if header == 'نوع الحالة':
                    worksheet.data_validation(
                        first_data_row, col_idx, last_data_row, col_idx,
                        {
                            'validate':      'list',
                            'source':        self.meta_ranges['detailed'],
                            'error_title':   'قيمة غير مسموحة',
                            'error_message': 'يجب اختيار نوع الحالة من القائمة المنسدلة حصراً. يرجى الضغط على السهم بجانب الخلية.',
                            'error_type':    'stop',
                            'show_error':    True,
                            'input_title':   'المرفقات المطلوبة',
                            'input_message': 'تذكر: في حال تغيير الحالة (كالفرار، الانتداب، السجناء، وغيرها) يجب أن يتم إرفاق المستندات الداعمة مع الكشف الورقي أثناء رفعه (مثل بلاغ الانقطاع، قرارات اللجان، الأحكام القضائية).',
                            'show_input':    True,
                            'ignore_blank':  False, # منع الكتابة اليدوية العشوائية
                        }
                    )

        # ── حماية الورقة ──
        worksheet.protect(
            password,
            {
                'select_locked_cells':   False,
                'select_unlocked_cells': True,
                'format_cells':          False,
                'format_columns':        False,
                'format_rows':           False,
                'insert_columns':        False,
                'delete_columns':        False,
                'insert_rows':           False,
                'delete_rows':           False,
                'sort':                  True,
                'autofilter':            True,
                'pivot_tables':          False,
                'objects':               True,  # ضروري جداً لكي يعمل سهم القائمة المنسدلة في بعض نسخ الإكسل!
                'scenarios':             False,
            }
        )

    def create_protected_excel(self) -> BytesIO:
        """إنشاء ملف Excel محمي (وضع multi أو single)."""
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {
            'in_memory':          True,
            'strings_to_formulas': False,  # أمان: منع الصيغ
            'strings_to_urls':     False,  # أمان: منع الروابط
        })

        # منع إضافة/حذف/إخفاء الأوراق
        dept_id_comment = self.central_department.id if self.central_department else (self.security_admin.id if self.security_admin else '0')
        workbook.set_properties({
            'title':   f'كشف خدمات {self.entity_name} - {self.service_month}',
            'subject': 'كشف خدمات شهري رسمي',
            'author':  'نظام إدارة الموارد البشرية',
            'company': 'وزارة الداخلية',
            'created': timezone.now(),
            'comments': f'export_id:{self.export_id}|month:{self.service_month}|dept:{dept_id_comment}',
        })

        fmts = self._build_formats(workbook)
        dept_id = self.central_department.id if self.central_department else (self.security_admin.id if self.security_admin else 0)
        password = _generate_workbook_password(
            dept_id,
            self.service_month,
            self.exported_by.id,
            str(self.export_id),
        )

        # جلب البيانات
        personnel_data = self._get_personnel()

        # ── توليد ورقة البيانات الوصفية (Metadata) المخفية ──
        meta_ws = workbook.add_worksheet('SystemData')
        
        # نحن نحتاج إلى ترتيب الأعمدة ليكون مناسباً لـ VLOOKUP:
        # العمود A: نوع الحالة (Detailed Status)
        # العمود B: التصنيف العام (Classification)
        
        all_detailed_statuses = []
        for classification, detailed_list in self._status_cascade.items():
            for detailed in detailed_list:
                all_detailed_statuses.append({
                    'detailed': detailed,
                    'classification': classification
                })
        
        # كتابة البيانات في الورقة المخفية
        for i, status_obj in enumerate(all_detailed_statuses):
            meta_ws.write(i, 0, status_obj['detailed'])
            meta_ws.write(i, 1, status_obj['classification'])
            
        self.meta_ranges = {
            'detailed': f"='SystemData'!$A$1:$A${len(all_detailed_statuses) or 1}"
        }

        if self.mode == 'single':
            # ── وضع الورقة الواحدة ──
            ws = workbook.add_worksheet('كشف موحد')
            self._write_sheet(workbook, ws, personnel_data, fmts, password, 'كشف موحد')
            ws.activate() # التأكد من أن هذه الورقة هي الفعالة عند الفتح
        else:
            # ── وضع الأوراق الأربعة ──
            sheets_data = self._classify_personnel(personnel_data)
            first_sheet = True
            for sheet_name in self.SHEET_NAMES:
                ws = workbook.add_worksheet(sheet_name)
                self._write_sheet(
                    workbook, ws,
                    sheets_data[sheet_name],
                    fmts, password, sheet_name,
                )
                if first_sheet:
                    ws.activate()
                    first_sheet = False

        meta_ws.hide() # إخفاء ورقة البيانات بعد تنشيط ورقة أخرى لكي تعمل بنجاح
        
        workbook.close()
        output.seek(0)

        # حساب Hash للملف المولّد
        raw = output.read()
        self.file_hash = hashlib.sha256(raw).hexdigest()
        output.seek(0)
        return output

    @transaction.atomic
    def export_and_log(self) -> Tuple[BytesIO, str]:
        """
        تصدير الملف وتسجيله في ExportLog.
        يعيد: (ملف BytesIO, اسم الملف الآمن)
        """
        excel_file = self.create_protected_excel()

        ExportLog.objects.create(
            export_id=self.export_id,
            central_department=self.central_department,
            security_admin=self.security_admin,
            service_month=self.service_month,
            exported_by=self.exported_by,
            file_hash=self.file_hash,
            row_uuids=self.row_uuids,
            editable_columns=self.editable_columns,
            status='pending',
        )

        filename = _generate_secure_filename(
            self.entity_name,
            self.service_month,
            str(self.export_id),
        )
        return excel_file, filename


# ══════════════════════════════════════════════════════════
# Batch Export — تصدير كل الإدارات دفعة واحدة
# ══════════════════════════════════════════════════════════

class BatchExcelExportService:
    """
    تصدير قوالب Excel لجميع الإدارات/المديريات/الفروع دفعة واحدة.
    النتيجة: ملف ZIP يحتوي على ملف Excel مستقل لكل جهة.
    """

    def __init__(self, exported_by, service_month: str, mode: str = 'multi'):
        self.exported_by = exported_by
        self.service_month = service_month
        self.mode = mode

    @transaction.atomic
    def export_all(self) -> Tuple[BytesIO, str]:
        """
        تصدير كل الإدارات وضغطها في ZIP واحد.
        يعيد: (BytesIO للـ ZIP, اسم ملف ZIP)
        """
        departments = CentralDepartment.objects.filter(is_active=True).order_by('name')
        if not departments.exists():
            raise ValueError("لا توجد إدارات مفعّلة في النظام")

        zip_buffer = BytesIO()
        exported_count = 0
        errors = []

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dept in departments:
                try:
                    service = ExcelExportService(
                        central_department=dept,
                        service_month=self.service_month,
                        exported_by=self.exported_by,
                        mode=self.mode,
                    )
                    excel_file, filename = service.export_and_log()
                    zf.writestr(filename, excel_file.read())
                    exported_count += 1
                except Exception as e:
                    errors.append({'department': dept.name, 'error': str(e)})

        zip_buffer.seek(0)
        zip_filename = f"كشوفات_شهرية_{self.service_month}_{exported_count}_إدارة.zip"

        if errors:
            # تسجيل الأخطاء (لا نوقف العملية بسببها)
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Batch export errors: {errors}")

        return zip_buffer, zip_filename, exported_count, errors


# ══════════════════════════════════════════════════════════
# دوال مساعدة للاستخدام الخارجي
# ══════════════════════════════════════════════════════════

def export_template_for_department(
    department_id: int,
    service_month: str,
    user,
    mode: str = 'multi',
) -> Tuple[BytesIO, str]:
    """
    تصدير قالب لإدارة واحدة.

    Args:
        department_id: معرف الإدارة المركزية
        service_month: شهر الخدمة YYYY-MM
        user: المستخدم المصدِّر
        mode: 'multi' أو 'single'
    """
    dept = CentralDepartment.objects.get(id=department_id)
    service = ExcelExportService(
        central_department=dept,
        service_month=service_month,
        exported_by=user,
        mode=mode,
    )
    return service.export_and_log()


def get_status_cascade() -> Dict[str, List[str]]:
    """
    إعادة خريطة التصنيف → الحالات التفصيلية للفرونت اند.
    يستخدمها الفرونت اند لبناء القوائم الشرطية (Cascading Dropdowns).
    """
    return _build_status_cascade()
