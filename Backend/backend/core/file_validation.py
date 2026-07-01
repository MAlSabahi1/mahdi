"""
FileValidationService — خدمة مركزية لفحص الملفات المرفوعة
═══════════════════════════════════════════════════════════
تُستخدم في كل مكان يتم فيه رفع ملف — ليس فقط الرقم الوطني.

الفحوصات:
1. فحص الامتداد (whitelist)
2. فحص Magic Bytes (محتوى الملف الفعلي)
3. فحص الحجم الأقصى
4. منع الأسماء الخبيثة (path traversal)
"""
import os
import uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# ═══════════════════════════════════════════════════
# التكوين — يمكن نقله لـ settings.py لاحقاً
# ═══════════════════════════════════════════════════

# الأنواع المسموحة: امتداد → (MIME, Magic Bytes prefixes)
ALLOWED_IMAGE_TYPES = {
    '.jpg':  ('image/jpeg', [b'\xff\xd8\xff']),
    '.jpeg': ('image/jpeg', [b'\xff\xd8\xff']),
    '.png':  ('image/png',  [b'\x89PNG\r\n\x1a\n']),
}

# PDF اختياري — يُفعّل حسب السياسة
ALLOWED_DOCUMENT_TYPES = {
    '.pdf': ('application/pdf', [b'%PDF']),
}

# الحجم الأقصى (بالبايت)
MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5 MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB


class FileValidationService:
    """
    خدمة مركزية لفحص سلامة الملفات المرفوعة.
    
    الاستخدام:
        from core.file_validation import FileValidationService
        
        # فحص صورة فقط (بطاقة وطنية)
        FileValidationService.validate_image(uploaded_file)
        
        # فحص صورة أو PDF (قرار ترقية)
        FileValidationService.validate_document(uploaded_file)
        
        # توليد اسم آمن
        safe_name = FileValidationService.generate_safe_filename(uploaded_file)
    """
    
    @staticmethod
    def validate_image(file_obj):
        """
        فحص ملف كصورة فقط (JPEG/PNG).
        يرمي ValidationError إذا فشل أي فحص.
        """
        FileValidationService._validate(file_obj, ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE)
    
    @staticmethod
    def validate_document(file_obj):
        """
        فحص ملف كصورة أو مستند (JPEG/PNG/PDF).
        """
        allowed = {**ALLOWED_IMAGE_TYPES, **ALLOWED_DOCUMENT_TYPES}
        FileValidationService._validate(file_obj, allowed, MAX_DOCUMENT_SIZE)
    
    @staticmethod
    def _validate(file_obj, allowed_types, max_size):
        """محرك الفحص الداخلي"""
        if not file_obj:
            raise ValidationError(_('لم يتم تقديم ملف.'))
        
        # 1. فحص الحجم
        if file_obj.size > max_size:
            max_mb = max_size / (1024 * 1024)
            file_mb = file_obj.size / (1024 * 1024)
            raise ValidationError(
                _('حجم الملف %(file_mb).1f MB يتجاوز الحد الأقصى %(max_mb).1f MB.')
                % {'file_mb': file_mb, 'max_mb': max_mb}
            )
        
        # 2. فحص الامتداد
        _base, ext = os.path.splitext(file_obj.name)
        ext = ext.lower()
        if ext not in allowed_types:
            allowed_exts = ', '.join(allowed_types.keys())
            raise ValidationError(
                _('نوع الملف "%(ext)s" غير مسموح. الأنواع المسموحة: %(allowed)s')
                % {'ext': ext, 'allowed': allowed_exts}
            )
        
        # 3. فحص Magic Bytes (المحتوى الفعلي)
        _mime, magic_prefixes = allowed_types[ext]
        file_obj.seek(0)
        header = file_obj.read(16)  # أول 16 بايت كافية
        file_obj.seek(0)  # إعادة المؤشر
        
        if not any(header.startswith(prefix) for prefix in magic_prefixes):
            raise ValidationError(
                _('محتوى الملف لا يتطابق مع الامتداد "%(ext)s". '
                  'قد يكون الملف تالفاً أو ملفاً خبيثاً متنكراً.')
                % {'ext': ext}
            )
        
        # 4. فحص اسم الملف (منع path traversal)
        if '..' in file_obj.name or '/' in file_obj.name or '\\' in file_obj.name:
            raise ValidationError(
                _('اسم الملف يحتوي على رموز غير مسموحة.')
            )
    
    @staticmethod
    def generate_safe_filename(file_obj):
        """
        توليد اسم آمن للملف — UUID + الامتداد الأصلي.
        يمنع تنفيذ أي أكواد خبيثة عبر اسم الملف.
        """
        _base, ext = os.path.splitext(file_obj.name)
        return f"{uuid.uuid4().hex}{ext.lower()}"
