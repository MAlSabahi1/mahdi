"""
Password Validators — سياسات كلمة المرور المخصصة
═══════════════════════════════════════════════════════
تُضاف إلى AUTH_PASSWORD_VALIDATORS في settings.py.
تعمل مع Django's validate_password() تلقائياً.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ArabicPasswordValidator:
    """
    تحقق من أن كلمة المرور تحتوي على مزيج من الحروف والأرقام.
    """

    def validate(self, password: str, user=None) -> None:
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not (has_upper and has_lower and has_digit):
            raise ValidationError(
                _('كلمة المرور يجب أن تحتوي على حرف كبير وحرف صغير ورقم على الأقل.'),
                code='password_too_simple',
            )

    def get_help_text(self) -> str:
        return _('كلمة المرور يجب أن تحتوي على حرف كبير وحرف صغير ورقم على الأقل.')


class NoUsernameInPasswordValidator:
    """
    تحقق من أن كلمة المرور لا تحتوي على اسم المستخدم.
    """

    def validate(self, password: str, user=None) -> None:
        if user is None:
            return

        username = getattr(user, 'username', '')
        if username and username.lower() in password.lower():
            raise ValidationError(
                _('كلمة المرور لا يجب أن تحتوي على اسم المستخدم.'),
                code='password_contains_username',
            )

    def get_help_text(self) -> str:
        return _('كلمة المرور لا يجب أن تحتوي على اسم المستخدم.')
