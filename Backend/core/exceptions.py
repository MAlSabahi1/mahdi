"""
Core Base Exceptions — أخطاء أساسية موحدة
═══════════════════════════════════════════════
كل أخطاء النظام ترث من هنا.
أي مشروع جديد يستخدم نفس الهيكل.

الاستخدام:
    from core.exceptions import ValidationError, NotFoundError, PermissionError

    raise ValidationError('الحقل مطلوب', field='username')
    raise NotFoundError('المستخدم غير موجود')
    raise BusinessRuleError('لا يمكن حذف سجل مقفل')
"""
from django.utils.translation import gettext_lazy as _


class AppError(Exception):
    """
    الخطأ الأساسي لكل النظام.
    كل Exception مخصص يرث من هنا.

    Attributes:
        message:     رسالة الخطأ (عربي/إنجليزي)
        code:        رمز الخطأ البرمجي (مثل: 'not_found', 'validation_failed')
        status_code: HTTP status code
        details:     معلومات إضافية (dict)
    """
    default_message = _('حدث خطأ غير متوقع')
    default_code = 'error'
    default_status_code = 500

    def __init__(
        self,
        message: str = None,
        code: str = None,
        status_code: int = None,
        details: dict = None,
    ):
        self.message = message or str(self.default_message)
        self.code = code or self.default_code
        self.status_code = status_code or self.default_status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """تحويل الخطأ إلى dict لاستجابة JSON."""
        result = {
            'success': False,
            'error': {
                'code': self.status_code,
                'type': self.code,
                'message': self.message,
            },
        }
        if self.details:
            result['error']['details'] = self.details
        return result


# ══════════════════════════════════════════════════════════════
# أخطاء 400 — بيانات خاطئة
# ══════════════════════════════════════════════════════════════

class ValidationError(AppError):
    """خطأ تحقق — بيانات غير صالحة."""
    default_message = _('بيانات غير صالحة')
    default_code = 'validation_error'
    default_status_code = 400

    def __init__(self, message=None, field: str = None, **kwargs):
        super().__init__(message, **kwargs)
        if field:
            self.details['field'] = field


class DuplicateError(AppError):
    """خطأ تكرار — السجل موجود مسبقاً."""
    default_message = _('السجل موجود مسبقاً')
    default_code = 'duplicate'
    default_status_code = 409


# ══════════════════════════════════════════════════════════════
# أخطاء 401/403 — صلاحيات
# ══════════════════════════════════════════════════════════════

class AuthenticationError(AppError):
    """خطأ مصادقة — غير مسجل الدخول."""
    default_message = _('غير مصادق — يرجى تسجيل الدخول')
    default_code = 'authentication_required'
    default_status_code = 401


class PermissionError(AppError):
    """خطأ صلاحية — لا يملك الإذن."""
    default_message = _('ليس لديك صلاحية للقيام بهذه العملية')
    default_code = 'permission_denied'
    default_status_code = 403


class AccountLockedError(AppError):
    """الحساب مغلق."""
    default_message = _('الحساب مغلق — حاول لاحقاً')
    default_code = 'account_locked'
    default_status_code = 403


# ══════════════════════════════════════════════════════════════
# أخطاء 404 — غير موجود
# ══════════════════════════════════════════════════════════════

class NotFoundError(AppError):
    """المورد غير موجود."""
    default_message = _('المورد المطلوب غير موجود')
    default_code = 'not_found'
    default_status_code = 404


# ══════════════════════════════════════════════════════════════
# أخطاء 422 — قواعد العمل
# ══════════════════════════════════════════════════════════════

class BusinessRuleError(AppError):
    """
    خطأ قاعدة عمل — العملية مرفوضة منطقياً.
    
    أمثلة:
        - لا يمكن حذف سجل مقفل
        - لا يمكن الموافقة على طلب مرفوض مسبقاً
        - تجاوز الحد الأقصى للجلسات
    """
    default_message = _('العملية غير مسموحة')
    default_code = 'business_rule_violation'
    default_status_code = 422


class StateTransitionError(BusinessRuleError):
    """خطأ انتقال حالة — الانتقال غير مسموح."""
    default_message = _('انتقال الحالة غير مسموح')
    default_code = 'invalid_state_transition'


class QuotaExceededError(BusinessRuleError):
    """تجاوز الحصة — مثل الحد الأقصى للجلسات."""
    default_message = _('تم تجاوز الحد المسموح')
    default_code = 'quota_exceeded'


# ══════════════════════════════════════════════════════════════
# أخطاء 429 — Rate Limiting
# ══════════════════════════════════════════════════════════════

class RateLimitError(AppError):
    """تجاوز معدل الطلبات."""
    default_message = _('تجاوزت الحد الأقصى للطلبات — حاول لاحقاً')
    default_code = 'rate_limit_exceeded'
    default_status_code = 429

    def __init__(self, message=None, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        if retry_after:
            self.details['retry_after'] = retry_after


# ══════════════════════════════════════════════════════════════
# أخطاء 500 — نظامية
# ══════════════════════════════════════════════════════════════

class InfrastructureError(AppError):
    """خطأ بنية تحتية — DB, Redis, etc."""
    default_message = _('خطأ في البنية التحتية — حاول لاحقاً')
    default_code = 'infrastructure_error'
    default_status_code = 503


class ExternalServiceError(AppError):
    """خطأ خدمة خارجية."""
    default_message = _('خطأ في الخدمة الخارجية')
    default_code = 'external_service_error'
    default_status_code = 502
