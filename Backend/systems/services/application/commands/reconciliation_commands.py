"""
Commands — عمليات الكتابة (CQRS)
══════════════════════════════════
Data classes بسيطة تحمل البيانات اللازمة لتنفيذ أمر ما.
لا منطق هنا — فقط بنية البيانات.
"""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateReconciliationCommand:
    """أمر: إنشاء مهمة مطابقة جديدة"""
    name:              str
    task_type:         str    # 'attendance' | 'payroll' | 'qualification'
    security_admin_id: int
    created_by_id:     int
    key_field:         str    # الحقل المستخدم للربط (military_number)
    source_file_path:  str    # مسار الملف المرفوع


@dataclass(frozen=True)
class ExecuteReconciliationCommand:
    """أمر: تشغيل مطابقة موجودة"""
    task_id:       UUID
    requested_by:  int    # معرف المستخدم الذي طلب التشغيل
