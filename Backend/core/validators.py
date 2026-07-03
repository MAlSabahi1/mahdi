"""
Custom Validators - محققات مخصصة
توفير تحقق قوي وآمن من البيانات
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

# Pre-compiled Regex patterns for performance
PHONE_PATTERN_INTL = re.compile(r'^\+967\d{9}$')
PHONE_PATTERN_LOCAL = re.compile(r'^7\d{8}$')
SERVICE_MONTH_PATTERN = re.compile(r'^\d{4}-(0[1-9]|1[0-2])$')
PHONE_CLEANUP = re.compile(r'[\s\-]')


def validate_military_number(value):
    """
    التحقق من صحة الرقم العسكري
    - يجب أن يكون 7 أرقام بالضبط
    - أرقام فقط (0-9)
    """
    if not value:
        raise ValidationError(_('الرقم العسكري مطلوب'))
    
    # إزالة المسافات
    value = str(value).strip()
    
    # التحقق من الطول
    if len(value) != 7:
        raise ValidationError(
            _('الرقم العسكري يجب أن يكون 7 أرقام بالضبط (الحالي: %(length)d)'),
            params={'length': len(value)},
            code='invalid_length'
        )
    
    # التحقق من أنها أرقام فقط
    if not value.isdigit():
        raise ValidationError(
            _('الرقم العسكري يجب أن يحتوي على أرقام فقط'),
            code='invalid_format'
        )
    
    # التحقق من عدم البدء بصفر (اختياري)
    if value.startswith('0'):
        raise ValidationError(
            _('الرقم العسكري لا يمكن أن يبدأ بصفر'),
            code='invalid_start'
        )


def validate_national_id(value):
    """
    التحقق من صحة الرقم الوطني
    - يجب أن يكون 11 رقماً بالضبط
    - أرقام فقط (0-9)
    """
    if not value:
        raise ValidationError(_('الرقم الوطني مطلوب'))
    
    # إزالة المسافات
    value = str(value).strip()
    
    # التحقق من الطول
    if len(value) != 11:
        raise ValidationError(
            _('الرقم الوطني يجب أن يكون 11 رقماً بالضبط (الحالي: %(length)d)'),
            params={'length': len(value)},
            code='invalid_length'
        )
    
    # التحقق من أنها أرقام فقط
    if not value.isdigit():
        raise ValidationError(
            _('الرقم الوطني يجب أن يحتوي على أرقام فقط'),
            code='invalid_format'
        )


def validate_phone_number(value):
    """
    التحقق من صحة رقم الهاتف
    - يبدأ بـ 7 (للأرقام الوطنية)
    - 9 أرقام
    - أو يبدأ بـ +967
    """
    if not value:
        return  # اختياري
    
    value = str(value).strip()
    
    # إزالة المسافات والشرطات (using pre-compiled regex)
    value = PHONE_CLEANUP.sub('', value)
    
    # التحقق باستخدام Regex مُجمّع مسبقاً
    if not (PHONE_PATTERN_INTL.match(value) or PHONE_PATTERN_LOCAL.match(value)):
        raise ValidationError(
            _('رقم الهاتف يجب أن يكون بصيغة +967xxxxxxxxx أو 7xxxxxxxx'),
            code='invalid_format'
        )


def validate_birth_date(value):
    """
    التحقق من صحة تاريخ الميلاد
    - لا يمكن أن يكون في المستقبل
    - العمر يجب أن يكون بين 18 و 70 سنة
    """
    if not value:
        raise ValidationError(_('تاريخ الميلاد مطلوب'))
    
    today = date.today()
    
    # التحقق من عدم كونه في المستقبل
    if value > today:
        raise ValidationError(
            _('تاريخ الميلاد لا يمكن أن يكون في المستقبل'),
            code='future_date'
        )
    
    # حساب العمر
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    # التحقق من العمر المنطقي
    if age < 18:
        raise ValidationError(
            _('العمر يجب أن يكون 18 سنة على الأقل (الحالي: %(age)d)'),
            params={'age': age},
            code='too_young'
        )
    
    if age > 70:
        raise ValidationError(
            _('العمر يجب أن يكون أقل من 70 سنة (الحالي: %(age)d)'),
            params={'age': age},
            code='too_old'
        )


def validate_join_date(value, birth_date=None):
    """
    التحقق من صحة تاريخ الالتحاق
    - لا يمكن أن يكون في المستقبل
    - يجب أن يكون بعد تاريخ الميلاد بـ 18 سنة على الأقل
    """
    if not value:
        raise ValidationError(_('تاريخ الالتحاق مطلوب'))
    
    today = date.today()
    
    # التحقق من عدم كونه في المستقبل
    if value > today:
        raise ValidationError(
            _('تاريخ الالتحاق لا يمكن أن يكون في المستقبل'),
            code='future_date'
        )
    
    # التحقق من العلاقة مع تاريخ الميلاد
    if birth_date:
        min_join_date = date(birth_date.year + 18, birth_date.month, birth_date.day)
        if value < min_join_date:
            raise ValidationError(
                _('تاريخ الالتحاق يجب أن يكون بعد بلوغ 18 سنة'),
                code='too_early'
            )


def validate_service_month(value):
    """
    التحقق من صحة شهر الخدمة
    - صيغة YYYY-MM
    - لا يمكن أن يكون في المستقبل بأكثر من شهر
    """
    if not value:
        raise ValidationError(_('شهر الخدمة مطلوب'))
    
    # التحقق من الصيغة (using pre-compiled regex)
    if not SERVICE_MONTH_PATTERN.match(value):
        raise ValidationError(
            _('شهر الخدمة يجب أن يكون بصيغة YYYY-MM (مثال: 2026-03)'),
            code='invalid_format'
        )
    
    # استخراج السنة والشهر
    try:
        year, month = map(int, value.split('-'))
    except ValueError:
        raise ValidationError(
            _('شهر الخدمة غير صحيح'),
            code='invalid_value'
        )
    
    # التحقق من صحة الشهر
    if month < 1 or month > 12:
        raise ValidationError(
            _('الشهر يجب أن يكون بين 1 و 12'),
            code='invalid_month'
        )
    
    # التحقق من عدم كونه في المستقبل البعيد
    today = date.today()
    service_date = date(year, month, 1)
    
    # السماح بشهر واحد في المستقبل فقط
    max_future_date = date(today.year, today.month, 1)
    if today.day > 20:  # بعد يوم 20، يمكن إدخال الشهر القادم
        if today.month == 12:
            max_future_date = date(today.year + 1, 1, 1)
        else:
            max_future_date = date(today.year, today.month + 1, 1)
    
    if service_date > max_future_date:
        raise ValidationError(
            _('شهر الخدمة لا يمكن أن يكون في المستقبل البعيد'),
            code='future_month'
        )


def validate_file_size(value, max_size_mb=5):
    """
    التحقق من حجم الملف
    - الحد الأقصى 5 ميجابايت افتراضياً
    """
    if not value:
        return
    
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if value.size > max_size_bytes:
        raise ValidationError(
            _('حجم الملف يجب أن يكون أقل من %(max_size)d ميجابايت (الحالي: %(current_size).2f ميجابايت)'),
            params={
                'max_size': max_size_mb,
                'current_size': value.size / (1024 * 1024)
            },
            code='file_too_large'
        )


def validate_file_extension(value, allowed_extensions=None):
    """
    التحقق من امتداد الملف والنوع الحقيقي (MIME type)
    - PDF, JPG, PNG افتراضياً
    - يتحقق من المحتوى الفعلي وليس الاسم فقط
    """
    if not value:
        return
    
    if allowed_extensions is None:
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
    
    import os
    ext = os.path.splitext(value.name)[1][1:].lower()
    
    # التحقق من الامتداد
    if ext not in allowed_extensions:
        raise ValidationError(
            _('امتداد الملف غير مسموح. الامتدادات المسموحة: %(extensions)s'),
            params={'extensions': ', '.join(allowed_extensions)},
            code='invalid_extension'
        )
    
    # التحقق من النوع الحقيقي باستخدام python-magic
    try:
        import magic
        
        # قراءة أول 2048 بايت للتحقق
        value.seek(0)
        file_header = value.read(2048)
        value.seek(0)
        
        mime = magic.from_buffer(file_header, mime=True)
        
        # MIME types المسموحة
        allowed_mimes = {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
        }
        
        expected_mime = allowed_mimes.get(ext)
        if expected_mime and mime != expected_mime:
            raise ValidationError(
                _('نوع الملف الحقيقي (%(actual)s) لا يطابق الامتداد (%(expected)s). محاولة تلاعب محتملة!'),
                params={'actual': mime, 'expected': expected_mime},
                code='mime_mismatch'
            )
    except ImportError:
        # إذا لم تكن python-magic مثبتة، نكتفي بالتحقق من الامتداد
        pass


def validate_image_dimensions(value, max_width=2000, max_height=2000):
    """
    التحقق من أبعاد الصورة
    - الحد الأقصى 2000x2000 بكسل افتراضياً
    """
    if not value:
        return
    
    try:
        from PIL import Image
        img = Image.open(value)
        width, height = img.size
        
        if width > max_width or height > max_height:
            raise ValidationError(
                _('أبعاد الصورة يجب أن تكون أقل من %(max_width)dx%(max_height)d بكسل (الحالي: %(width)dx%(height)d)'),
                params={
                    'max_width': max_width,
                    'max_height': max_height,
                    'width': width,
                    'height': height
                },
                code='dimensions_too_large'
            )
    except Exception:
        raise ValidationError(
            _('فشل قراءة الصورة. تأكد من أن الملف صورة صحيحة'),
            code='invalid_image'
        )



# ========================================
# Class-based Validators (للمرونة)
# ========================================

class FileSizeValidator:
    """
    محقق حجم الملف (Class-based)
    يسمح بتمرير max_size عند التعريف
    
    Usage:
        file = models.FileField(validators=[FileSizeValidator(max_size_mb=10)])
    """
    
    def __init__(self, max_size_mb=5):
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    def __call__(self, value):
        if not value:
            return
        
        if value.size > self.max_size_bytes:
            raise ValidationError(
                _('حجم الملف يجب أن يكون أقل من %(max_size)d ميجابايت (الحالي: %(current_size).2f ميجابايت)'),
                params={
                    'max_size': self.max_size_mb,
                    'current_size': value.size / (1024 * 1024)
                },
                code='file_too_large'
            )
    
    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator) and
            self.max_size_mb == other.max_size_mb
        )


class FileExtensionValidator:
    """
    محقق امتداد الملف (Class-based)
    يسمح بتمرير allowed_extensions عند التعريف
    
    Usage:
        file = models.FileField(validators=[FileExtensionValidator(['pdf', 'docx'])])
    """
    
    def __init__(self, allowed_extensions=None):
        self.allowed_extensions = allowed_extensions or ['pdf', 'jpg', 'jpeg', 'png']
    
    def __call__(self, value):
        if not value:
            return
        
        import os
        ext = os.path.splitext(value.name)[1][1:].lower()
        
        if ext not in self.allowed_extensions:
            raise ValidationError(
                _('امتداد الملف غير مسموح. الامتدادات المسموحة: %(extensions)s'),
                params={'extensions': ', '.join(self.allowed_extensions)},
                code='invalid_extension'
            )
        
        # التحقق من النوع الحقيقي
        try:
            import magic
            
            value.seek(0)
            file_header = value.read(2048)
            value.seek(0)
            
            mime = magic.from_buffer(file_header, mime=True)
            
            allowed_mimes = {
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            }
            
            expected_mime = allowed_mimes.get(ext)
            if expected_mime and mime != expected_mime:
                raise ValidationError(
                    _('نوع الملف الحقيقي (%(actual)s) لا يطابق الامتداد (%(expected)s)'),
                    params={'actual': mime, 'expected': expected_mime},
                    code='mime_mismatch'
                )
        except ImportError:
            pass
    
    def __eq__(self, other):
        return (
            isinstance(other, FileExtensionValidator) and
            self.allowed_extensions == other.allowed_extensions
        )


class ImageDimensionsValidator:
    """
    محقق أبعاد الصورة (Class-based)
    
    Usage:
        photo = models.ImageField(validators=[ImageDimensionsValidator(max_width=1920, max_height=1080)])
    """
    
    def __init__(self, max_width=2000, max_height=2000):
        self.max_width = max_width
        self.max_height = max_height
    
    def __call__(self, value):
        if not value:
            return
        
        try:
            from PIL import Image
            img = Image.open(value)
            width, height = img.size
            
            if width > self.max_width or height > self.max_height:
                raise ValidationError(
                    _('أبعاد الصورة يجب أن تكون أقل من %(max_width)dx%(max_height)d بكسل (الحالي: %(width)dx%(height)d)'),
                    params={
                        'max_width': self.max_width,
                        'max_height': self.max_height,
                        'width': width,
                        'height': height
                    },
                    code='dimensions_too_large'
                )
        except Exception:
            raise ValidationError(
                _('فشل قراءة الصورة. تأكد من أن الملف صورة صحيحة'),
                code='invalid_image'
            )
    
    def __eq__(self, other):
        return (
            isinstance(other, ImageDimensionsValidator) and
            self.max_width == other.max_width and
            self.max_height == other.max_height
        )
