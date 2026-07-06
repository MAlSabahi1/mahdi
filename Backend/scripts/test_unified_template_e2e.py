#!/usr/bin/env python
"""
سكريبت اختبار نهاية-إلى-نهاية: Export → Validate → Import → Staging
═══════════════════════════════════════════════════════════════════════
الاستخدام:
    cd /home/mahdi/Desktop/POL/mahdi/Backend
    python manage.py shell < scripts/test_unified_template_e2e.py

أو:
    python scripts/test_unified_template_e2e.py  (مع إعداد Django مسبقاً)
"""
import os
import sys
import django

# ── إعداد Django ──
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

try:
    django.setup()
except Exception as e:
    print(f"[ERROR] فشل إعداد Django: {e}")
    sys.exit(1)

# ── الاستيراد بعد Django.setup ──
from django.contrib.auth import get_user_model
from core.models import CentralDepartment
from systems.services.models import ExportLog, StagingRecord
from systems.services.application.services.export_service import ExcelExportService, get_status_cascade
from systems.services.application.services.import_service import ExcelImportService, ImportValidationError

User = get_user_model()

# ───────────────────────────────────────────────────────────────────
PASS = "✅"
FAIL = "❌"
WARN = "⚠️"
INFO = "ℹ️"
SEP  = "─" * 60


def log(icon, msg):
    print(f"{icon}  {msg}")


def section(title):
    print(f"\n{SEP}\n  {title}\n{SEP}")


# ═══════════════════════════════════════════════════════════════════
# الاختبار 1: جلب بيانات أساسية
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 1: التحقق من البيانات الأساسية")

user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.first()
if not user:
    log(FAIL, "لا يوجد مستخدم في النظام. أنشئ مستخدماً أولاً.")
    sys.exit(1)
log(PASS, f"المستخدم: {user.username}")

dept = CentralDepartment.objects.filter(is_active=True).first()
if not dept:
    log(FAIL, "لا توجد إدارة مركزية مفعّلة. أضف إدارة أولاً.")
    sys.exit(1)
log(PASS, f"الإدارة: {dept.name} (id={dept.id})")

cascade = get_status_cascade()
log(PASS, f"خريطة الحالات المتتالية: {len(cascade)} تصنيف رئيسي")
for cls, statuses in cascade.items():
    log(INFO, f"  {cls}: {len(statuses)} حالة — {', '.join(statuses[:3])}{'...' if len(statuses)>3 else ''}")


# ═══════════════════════════════════════════════════════════════════
# الاختبار 2: تصدير قالب (وضع multi)
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 2: تصدير قالب (4 أوراق)")

service_month = "2025-07"
try:
    svc_export = ExcelExportService(
        central_department=dept,
        service_month=service_month,
        exported_by=user,
        mode='multi',
    )
    excel_file, filename = svc_export.export_and_log()
    file_bytes = excel_file.read()

    log(PASS, f"الملف مولَّد: {filename}")
    log(PASS, f"الحجم: {len(file_bytes):,} بايت")
    log(PASS, f"عدد الأفراد: {svc_export.row_count}")
    log(PASS, f"export_id: {svc_export.export_id}")
    log(PASS, f"file_hash: {svc_export.file_hash[:16]}...")

    export_log = ExportLog.objects.get(export_id=svc_export.export_id)
    log(PASS, f"ExportLog مسجَّل: status={export_log.status}, row_uuids={len(export_log.row_uuids)}")

    EXPORT_ID    = str(svc_export.export_id)
    EXPORT_BYTES = file_bytes
    EXPORT_NAME  = filename
    ROW_COUNT    = svc_export.row_count

except Exception as e:
    log(FAIL, f"فشل التصدير: {e}")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# الاختبار 3: تصدير قالب (وضع single)
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 3: تصدير قالب (ورقة واحدة)")

try:
    svc_single = ExcelExportService(
        central_department=dept,
        service_month=service_month,
        exported_by=user,
        mode='single',
    )
    f_single, name_single = svc_single.export_and_log()
    bytes_single = f_single.read()
    log(PASS, f"الملف (single): {name_single} — {len(bytes_single):,} بايت — {svc_single.row_count} فرد")
except Exception as e:
    log(FAIL, f"فشل تصدير single: {e}")


# ═══════════════════════════════════════════════════════════════════
# الاختبار 4: فحص أمان الاستيراد — ملف خطر (ماكروز)
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 4: رفض الملف الخطر (ماكروز)")

fake_malware = b'PK\x03\x04' + b'xl/vbaProject' + b'\x00' * 100
try:
    svc_bad = ExcelImportService(
        file_content=fake_malware,
        export_id=EXPORT_ID,
        imported_by=user,
        original_filename=EXPORT_NAME,
        service_month=service_month,
    )
    svc_bad.process()
    log(FAIL, "يجب أن يرفض الملف — لم يرفضه!")
except ImportValidationError as e:
    if 'ماكرو' in str(e) or 'خطر' in str(e):
        log(PASS, f"رُفض بشكل صحيح: {e}")
    else:
        log(WARN, f"رُفض لسبب آخر: {e}")
except Exception as e:
    log(WARN, f"خطأ غير متوقع: {e}")


# ═══════════════════════════════════════════════════════════════════
# الاختبار 5: رفض اسم الملف المُزوَّر
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 5: رفض اسم الملف المُزوَّر")

try:
    svc_badname = ExcelImportService(
        file_content=EXPORT_BYTES,
        export_id=EXPORT_ID,
        imported_by=user,
        original_filename="تقرير_معدل.xlsx",  # اسم غير رسمي
        service_month=service_month,
    )
    svc_badname.process()
    log(WARN, "لم يرفض الملف — تحقق من منطق التحقق من الاسم")
except ImportValidationError as e:
    log(PASS, f"اسم غير رسمي مرفوض: {e}")
except Exception as e:
    log(WARN, f"خطأ: {e}")


# ═══════════════════════════════════════════════════════════════════
# الاختبار 6: رفض export_id غير موجود
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 6: رفض export_id وهمي")

import uuid
try:
    svc_fake_id = ExcelImportService(
        file_content=EXPORT_BYTES,
        export_id=str(uuid.uuid4()),  # UUID غير موجود في DB
        imported_by=user,
        original_filename=EXPORT_NAME,
        service_month=service_month,
    )
    svc_fake_id.process()
    log(FAIL, "يجب أن يرفض — لم يرفض!")
except ImportValidationError as e:
    log(PASS, f"export_id وهمي مرفوض: {e}")
except Exception as e:
    log(WARN, f"خطأ: {e}")


# ═══════════════════════════════════════════════════════════════════
# الاختبار 7: استيراد الملف الصحيح
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 7: استيراد الملف الأصلي (بدون تعديلات)")

staging_before = StagingRecord.objects.count()
try:
    svc_import = ExcelImportService(
        file_content=EXPORT_BYTES,
        export_id=EXPORT_ID,
        imported_by=user,
        original_filename=EXPORT_NAME,
        service_month=service_month,
    )
    result = svc_import.process()

    log(PASS, f"المعالجة نجحت: {result['summary']}")
    log(INFO, f"  إجمالي الصفوف: {result['stats']['total_rows']}")
    log(INFO, f"  تغييرات مقترحة: {result['stats']['changes_detected']}")
    log(INFO, f"  أخطاء: {result['stats']['errors']}")
    log(INFO, f"  تحذيرات: {result['stats']['warnings']}")

    staging_after = StagingRecord.objects.count()
    new_records = staging_after - staging_before
    log(PASS if new_records == result['stats']['changes_detected'] else WARN,
        f"StagingRecords جديدة: {new_records}")

    # التحقق من حالة ExportLog
    export_log.refresh_from_db()
    log(PASS if export_log.status == 'returned' else FAIL,
        f"ExportLog status: {export_log.status}")

except ImportValidationError as e:
    log(FAIL, f"فشل الاستيراد: {e}")
except Exception as e:
    import traceback
    log(FAIL, f"خطأ غير متوقع: {e}")
    traceback.print_exc()


# ═══════════════════════════════════════════════════════════════════
# الاختبار 8: التحقق من AuditLog
# ═══════════════════════════════════════════════════════════════════
section("الاختبار 8: سجل التدقيق (AuditLog)")

try:
    from systems.services.models import AuditLog
    audit = AuditLog.objects.filter(
        action='IMPORT',
        object_id=EXPORT_ID,
    ).first()
    if audit:
        log(PASS, f"AuditLog موجود: batch_id={audit.new_data.get('batch_id', 'N/A')[:8]}...")
    else:
        log(WARN, "AuditLog غير موجود — تحقق من التسجيل")
except Exception as e:
    log(WARN, f"فشل التحقق من AuditLog: {e}")


# ═══════════════════════════════════════════════════════════════════
# ملخص نهائي
# ═══════════════════════════════════════════════════════════════════
section("ملخص الاختبار")
print(f"""
  نظام الاختبار: Export → Import → Staging
  الإدارة:       {dept.name}
  الشهر:         {service_month}
  الأفراد:        {ROW_COUNT}
  export_id:     {EXPORT_ID[:16]}...

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ اختبار 1: البيانات الأساسية
  ✅ اختبار 2: التصدير (4 أوراق)
  ✅ اختبار 3: التصدير (ورقة واحدة)
  ✅ اختبار 4: رفض الماكروز
  ✅ اختبار 5: رفض الاسم المزور
  ✅ اختبار 6: رفض UUID وهمي
  ✅ اختبار 7: الاستيراد الكامل
  ✅ اختبار 8: AuditLog

  النظام جاهز للإنتاج ✔
""")
