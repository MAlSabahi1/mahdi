#!/usr/bin/env python
"""
توليد ملف Excel تجريبي احترافي — لفحص القالب الموحد
═══════════════════════════════════════════════════════
ينشئ ملفين:
1. multi_demo.xlsx (4 أوراق)
2. single_demo.xlsx (ورقة واحدة)
مع بيانات تجريبية واقعية لـ 30 فرد.
"""
import os
import sys
import hashlib
import hmac
import uuid
from io import BytesIO
from datetime import datetime

# ── إعداد Django ──
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import django
django.setup()

from core.models import ServiceStatus
import xlsxwriter

# ═══════════════════════════════════════════════════
# بيانات تجريبية واقعية
# ═══════════════════════════════════════════════════
DEMO_PERSONNEL = [
    {'mil': '100001', 'name': 'أحمد محمد عبدالله السعيدي',     'rank': 'عميد',    'nid': '01012345678901', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100002', 'name': 'خالد علي حسين الهاشمي',         'rank': 'عقيد',    'nid': '01012345678902', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100003', 'name': 'محمد سالم أحمد الزبيدي',        'rank': 'مقدم',    'nid': '01012345678903', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100004', 'name': 'عبدالرحمن فهد ناصر القحطاني',   'rank': 'رائد',    'nid': '01012345678904', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100005', 'name': 'فيصل عمر سعيد البكري',          'rank': 'نقيب',    'nid': '01012345678905', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100006', 'name': 'سلطان ماجد عبدالله العتيبي',    'rank': 'ملازم أول','nid': '01012345678906', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100007', 'name': 'عبدالله سعد محمد الدوسري',      'rank': 'ملازم',   'nid': '01012345678907', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100008', 'name': 'ناصر حمد خالد الحربي',          'rank': 'مساعد 1', 'nid': '01012345678908', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100009', 'name': 'ماجد سليمان أحمد المطيري',      'rank': 'مساعد 2', 'nid': '01012345678909', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100010', 'name': 'تركي عبدالعزيز فهد الشمري',     'rank': 'رقيب أول','nid': '01012345678910', 'status': 'تعمل في الميدان', 'cls': 'active_full'},
    {'mil': '100011', 'name': 'سامي يوسف علي الجابري',         'rank': 'رقيب',    'nid': '01012345678911', 'status': 'بدون عمل',        'cls': 'active_part'},
    {'mil': '100012', 'name': 'عمر إبراهيم محمد النعيمي',      'rank': 'عريف',    'nid': '01012345678912', 'status': 'بدون عمل',        'cls': 'active_part'},
    {'mil': '100013', 'name': 'يوسف حسن عبدالله الكندي',       'rank': 'جندي أول','nid': '01012345678913', 'status': 'قوة احتياطية',     'cls': 'active_part'},
    {'mil': '100014', 'name': 'حمد راشد سالم المنصوري',        'rank': 'جندي',    'nid': '01012345678914', 'status': 'قوة احتياطية',     'cls': 'active_part'},
    {'mil': '100015', 'name': 'علي محمد أحمد الفلاسي',         'rank': 'نقيب',    'nid': '01012345678915', 'status': 'الإجازات',         'cls': 'inactive_temp'},
    {'mil': '100016', 'name': 'سعيد خلفان ناصر الكعبي',       'rank': 'رائد',    'nid': '01012345678916', 'status': 'الأمراض والمصابين','cls': 'inactive_temp'},
    {'mil': '100017', 'name': 'راشد عبدالله محمد الشامسي',     'rank': 'ملازم',   'nid': '01012345678917', 'status': 'المفرغين للدراسة', 'cls': 'inactive_temp'},
    {'mil': '100018', 'name': 'حسين علي جاسم البلوشي',        'rank': 'عقيد',    'nid': '01012345678918', 'status': 'المنتدبين لدى جهات','cls': 'inactive_temp'},
    {'mil': '100019', 'name': 'جاسم محمد سعيد الرميثي',       'rank': 'مقدم',    'nid': '01012345678919', 'status': 'السجناء',          'cls': 'inactive_temp'},
    {'mil': '100020', 'name': 'مبارك سالم حمد الأحبابي',       'rank': 'رقيب',    'nid': '01012345678920', 'status': 'غياب',             'cls': 'inactive_temp'},
    {'mil': '100021', 'name': 'عبدالعزيز فهد تركي العنزي',     'rank': 'عميد',    'nid': '01012345678921', 'status': 'المتقاعدين',       'cls': 'inactive_perm'},
    {'mil': '100022', 'name': 'بدر ناصر سعود المري',           'rank': 'عقيد',    'nid': '01012345678922', 'status': 'الشهداء',          'cls': 'inactive_perm'},
    {'mil': '100023', 'name': 'منصور حمد خليفة الهاجري',       'rank': 'مقدم',    'nid': '01012345678923', 'status': 'الوفيات',          'cls': 'inactive_perm'},
    {'mil': '100024', 'name': 'سلمان عبدالله راشد الكثيري',    'rank': 'نقيب',    'nid': '01012345678924', 'status': 'المنقطعين - فرار', 'cls': 'inactive_perm'},
    {'mil': '100025', 'name': 'هاني محمد علي الظاهري',         'rank': 'ملازم أول','nid': '01012345678925', 'status': 'عدم لياقة',        'cls': 'inactive_perm'},
    {'mil': '100026', 'name': 'وليد أحمد سعيد المهيري',        'rank': 'رائد',    'nid': '01012345678926', 'status': 'الغياب المستمر',   'cls': 'inactive_perm'},
    {'mil': '100027', 'name': 'طارق خالد محمد السويدي',        'rank': 'مساعد 1', 'nid': '01012345678927', 'status': 'بلوغ السن القانوني','cls': 'inactive_perm'},
    {'mil': '100028', 'name': 'نواف سلطان فهد الدرعي',         'rank': 'رقيب أول','nid': '01012345678928', 'status': 'المفقودين',        'cls': 'inactive_temp'},
    {'mil': '100029', 'name': 'ثامر عبدالرحمن حسن المزروعي',   'rank': 'عريف',    'nid': '01012345678929', 'status': 'الجرحى',           'cls': 'inactive_temp'},
    {'mil': '100030', 'name': 'حمدان راشد سيف النعيمي',        'rank': 'جندي أول','nid': '01012345678930', 'status': 'الأسرى',           'cls': 'inactive_temp'},
]

DEPT_NAME = 'مديرية شرطة المحافظة'
SERVICE_MONTH = '2025-07'
EXPORT_ID = str(uuid.uuid4())

ABSENCE_STATUSES = {'الغياب المستمر', 'المنقطعين - فرار', 'غياب'}

# الحالات من DB
STATUS_CASCADE = {}
try:
    for s in ServiceStatus.objects.all().order_by('name'):
        cls_display = s.get_classification_display()
        STATUS_CASCADE.setdefault(cls_display, []).append(s.name)
except Exception:
    STATUS_CASCADE = {
        'قوة عاملة فعلية': ['تعمل في الميدان'],
        'قوة عاملة غير فعلية': ['بدون عمل', 'قوة احتياطية'],
        'قوة غير عاملة مؤقتاً': ['الإجازات', 'الأمراض والمصابين', 'السجناء'],
        'قوة غير عاملة نهائياً': ['المتقاعدين', 'الشهداء', 'الوفيات'],
    }

ALL_CLASSIFICATIONS = list(STATUS_CASCADE.keys())
ALL_DETAILED = []
for v in STATUS_CASCADE.values():
    ALL_DETAILED.extend(v)

PROTECTED_COLS = ['الرقم العسكري', 'الاسم الكامل', 'الرتبة', 'الرقم الوطني', 'الحالة الحالية']
EDITABLE_COLS  = ['الحالة الجديدة', 'نوع الحالة الجديدة', 'ملاحظات']
ALL_COLS = PROTECTED_COLS + EDITABLE_COLS + ['__UUID__']


def build_formats(wb):
    return {
        'header': wb.add_format({
            'bold': True, 'bg_color': '#1F3864', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1,
            'text_wrap': True, 'font_size': 12, 'font_name': 'Arial',
        }),
        'protected': wb.add_format({
            'bg_color': '#F2F2F2', 'locked': True, 'border': 1,
            'align': 'right', 'valign': 'vcenter', 'font_size': 11,
            'font_name': 'Arial',
        }),
        'editable': wb.add_format({
            'locked': False, 'border': 1, 'align': 'right',
            'valign': 'vcenter', 'bg_color': '#EBF5FB', 'font_size': 11,
            'font_name': 'Arial',
        }),
        'notes': wb.add_format({
            'locked': False, 'border': 1, 'align': 'right',
            'valign': 'vcenter', 'font_size': 11, 'text_wrap': True,
            'font_name': 'Arial',
        }),
        'hidden': wb.add_format({'locked': True, 'hidden': True, 'font_size': 1}),
        'warning': wb.add_format({
            'locked': True, 'bg_color': '#FFE0B2', 'font_color': '#E65100',
            'align': 'center', 'valign': 'vcenter', 'font_size': 10,
            'bold': True, 'font_name': 'Arial', 'border': 1,
        }),
        'seq': wb.add_format({
            'bg_color': '#E8EAF6', 'locked': True, 'border': 1,
            'align': 'center', 'valign': 'vcenter', 'font_size': 11,
            'font_name': 'Arial', 'bold': True,
        }),
    }


def write_sheet(wb, ws, persons, fmts, sheet_title, password):
    cols_with_seq = ['ت'] + ALL_COLS

    # صف التحذير
    ws.merge_range(
        0, 0, 0, len(cols_with_seq) - 1,
        f'⚠ ملف رسمي محمي — {DEPT_NAME} | الشهر: {SERVICE_MONTH} | '
        f'التصدير: {EXPORT_ID[:8]} | العدد: {len(persons)} فرد | '
        f'⛔ أي تعديل على الأعمدة الرمادية يُعدّ تلاعباً',
        fmts['warning'],
    )
    ws.set_row(0, 22)

    # صف العناوين
    for ci, header in enumerate(cols_with_seq):
        ws.write(1, ci, header, fmts['header'])
    ws.set_row(1, 25)

    # عرض الأعمدة
    widths = {'ت': 5, 'الرقم العسكري': 16, 'الاسم الكامل': 38, 'الرتبة': 14,
              'الرقم الوطني': 20, 'الحالة الحالية': 26,
              'الحالة الجديدة': 30, 'نوع الحالة الجديدة': 34,
              'ملاحظات': 45, '__UUID__': 0}
    for ci, header in enumerate(cols_with_seq):
        ws.set_column(ci, ci, widths.get(header, 18))

    # تجميد
    ws.freeze_panes(2, 0)

    # بيانات الأفراد
    for ri, p in enumerate(persons):
        row = ri + 2
        row_uuid = str(uuid.uuid4())

        for ci, header in enumerate(cols_with_seq):
            if header == 'ت':
                ws.write(row, ci, ri + 1, fmts['seq'])
            elif header == '__UUID__':
                ws.write(row, ci, row_uuid, fmts['hidden'])
            elif header in PROTECTED_COLS:
                val_map = {
                    'الرقم العسكري': p['mil'],
                    'الاسم الكامل': p['name'],
                    'الرتبة': p['rank'],
                    'الرقم الوطني': p['nid'],
                    'الحالة الحالية': p['status'],
                }
                ws.write(row, ci, val_map.get(header, ''), fmts['protected'])
            elif header == 'ملاحظات':
                ws.write(row, ci, '', fmts['notes'])
            else:
                ws.write(row, ci, '', fmts['editable'])

    # Data Validation
    if persons:
        first = 2
        last = len(persons) + 1

        # عمود "الحالة الجديدة" — تصنيفات رئيسية
        col_cls = cols_with_seq.index('الحالة الجديدة')
        ws.data_validation(first, col_cls, last, col_cls, {
            'validate': 'list', 'source': ALL_CLASSIFICATIONS,
            'input_title': '⬇ اختر التصنيف العام',
            'input_message': 'اختر التصنيف الرئيسي ثم اختر النوع في العمود التالي',
            'error_title': '⛔ قيمة غير مسموحة',
            'error_message': 'يجب الاختيار من القائمة فقط. لا يُسمح بالكتابة اليدوية.',
            'error_type': 'stop', 'show_input': True, 'show_error': True,
        })

        # عمود "نوع الحالة الجديدة" — حالات تفصيلية
        col_type = cols_with_seq.index('نوع الحالة الجديدة')
        ws.data_validation(first, col_type, last, col_type, {
            'validate': 'list', 'source': ALL_DETAILED[:255],
            'input_title': '⬇ اختر نوع الحالة',
            'input_message': 'اختر الحالة التفصيلية المناسبة بناءً على التصنيف في العمود السابق',
            'error_title': '⛔ قيمة غير مسموحة',
            'error_message': 'يجب الاختيار من القائمة فقط.',
            'error_type': 'stop', 'show_input': True, 'show_error': True,
        })

    # حماية الورقة
    ws.protect(password, {
        'select_locked_cells': False, 'select_unlocked_cells': True,
        'format_cells': False, 'format_columns': False, 'format_rows': False,
        'insert_columns': False, 'delete_columns': False,
        'insert_rows': False, 'delete_rows': False,
        'sort': False, 'autofilter': False, 'pivot_tables': False,
        'objects': False, 'scenarios': False,
    })


def generate(mode, output_path):
    wb = xlsxwriter.Workbook(output_path, {
        'strings_to_formulas': False,
        'strings_to_urls': False,
    })
    wb.set_properties({
        'title': f'كشف خدمات {DEPT_NAME} - {SERVICE_MONTH}',
        'subject': 'كشف خدمات شهري رسمي',
        'author': 'نظام إدارة الموارد البشرية',
        'company': 'وزارة الداخلية',
        'comments': f'export_id:{EXPORT_ID}|month:{SERVICE_MONTH}',
    })
    fmts = build_formats(wb)
    password = 'DEMO_PROTECTED_2025'

    if mode == 'single':
        ws = wb.add_worksheet('كشف موحد')
        write_sheet(wb, ws, DEMO_PERSONNEL, fmts, 'كشف موحد', password)
    else:
        # القوة العاملة
        active = [p for p in DEMO_PERSONNEL if p['cls'] in ('active_full', 'active_part')]
        ws1 = wb.add_worksheet('القوة العاملة')
        write_sheet(wb, ws1, active, fmts, 'القوة العاملة', password)

        # القوة غير العاملة
        inactive = [p for p in DEMO_PERSONNEL if p['cls'] in ('inactive_temp', 'inactive_perm')]
        ws2 = wb.add_worksheet('القوة غير العاملة')
        write_sheet(wb, ws2, inactive, fmts, 'القوة غير العاملة', password)

        # القوة كاملة
        ws3 = wb.add_worksheet('القوة كاملة')
        write_sheet(wb, ws3, DEMO_PERSONNEL, fmts, 'القوة كاملة', password)

        # الغياب
        absence = [p for p in DEMO_PERSONNEL if p['status'] in ABSENCE_STATUSES]
        ws4 = wb.add_worksheet('الغياب')
        write_sheet(wb, ws4, absence, fmts, 'الغياب', password)

    wb.close()
    print(f'✅ تم إنشاء: {output_path}')


# ══════════════════════════════════════
# التوليد
# ══════════════════════════════════════
OUTPUT_DIR = os.path.join(BASE_DIR, 'media', 'demo_templates')
os.makedirs(OUTPUT_DIR, exist_ok=True)

generate('multi',  os.path.join(OUTPUT_DIR, f'كشف_{DEPT_NAME}_{SERVICE_MONTH}_multi.xlsx'))
generate('single', os.path.join(OUTPUT_DIR, f'كشف_{DEPT_NAME}_{SERVICE_MONTH}_single.xlsx'))

print(f'\n📁 الملفات في: {OUTPUT_DIR}')
print('افتح الملفات في Excel أو LibreOffice للفحص.')
print(f'كلمة سر فك الحماية (للاختبار فقط): DEMO_PROTECTED_2025')
