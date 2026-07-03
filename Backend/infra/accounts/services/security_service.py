"""
Security Service — خدمة الأمان
═══════════════════════════════
مسؤولة عن: lockout, password policies, suspicious login detection.
لا تتدخل في المصادقة — AuthService يستدعيها عند الحاجة.
"""
import hashlib
import logging
from typing import List, Optional, NamedTuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from infra.accounts.models.security import SecurityProfile, MAX_FAILED_ATTEMPTS, LOCKOUT_DURATION_MINUTES

logger = logging.getLogger('accounts.security')

User = get_user_model()


class LockState(NamedTuple):
    """نتيجة فحص حالة القفل."""
    is_locked: bool
    remaining_seconds: int
    failed_attempts: int
    max_attempts: int


class SecurityService:
    """
    خدمة الأمان — نقطة الدخول الوحيدة لكل عمليات الأمان.

    القواعد:
        - 5 محاولات فاشلة → قفل 15 دقيقة
        - كشف تسجيل دخول مشبوه (تغيير IP + User Agent)
        - منع إعادة استخدام آخر 5 كلمات مرور
        - سياسات كلمة المرور عبر Django validators
    """

    # ── Profile Management ──

    @staticmethod
    def get_or_create_profile(user) -> SecurityProfile:
        """جلب أو إنشاء ملف الأمان للمستخدم."""
        profile, created = SecurityProfile.objects.get_or_create(user=user)
        if created:
            logger.info(f"[SecurityService] Created SecurityProfile for {user.username}")
        return profile

    # ── Login Attempts ──

    @staticmethod
    def record_failed_login(username: str, ip_address: str) -> None:
        """
        تسجيل محاولة دخول فاشلة.
        يبحث عن المستخدم بـ username — إذا لم يجده يتجاهل (لا نكشف وجود المستخدم).
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.warning(
                f"[SecurityService] Failed login for non-existent user: {username} from {ip_address}"
            )
            return

        profile = SecurityService.get_or_create_profile(user)
        profile.record_failed_attempt(ip_address)

        logger.warning(
            f"[SecurityService] Failed login #{profile.failed_login_attempts} "
            f"for {username} from {ip_address}"
        )

        if profile.is_locked:
            logger.critical(
                f"[SecurityService] Account LOCKED: {username} — "
                f"{profile.failed_login_attempts} failed attempts from {ip_address}"
            )

    @staticmethod
    def record_successful_login(user, ip_address: str, user_agent: str) -> None:
        """تسجيل دخول ناجح — يُعيد تعيين العداد ويُحدّث بيانات الجهاز."""
        profile = SecurityService.get_or_create_profile(user)
        profile.record_successful_login(ip_address, user_agent)
        logger.info(f"[SecurityService] Successful login: {user.username} from {ip_address}")

    # ── Lock State ──

    @staticmethod
    def check_lock_state(user) -> LockState:
        """
        فحص حالة القفل — يُعيد LockState.
        يفك القفل تلقائياً إذا انتهت المدة.
        """
        profile = SecurityService.get_or_create_profile(user)
        is_locked = profile.check_lock_state()

        return LockState(
            is_locked=is_locked,
            remaining_seconds=profile.lockout_remaining_seconds,
            failed_attempts=profile.failed_login_attempts,
            max_attempts=MAX_FAILED_ATTEMPTS,
        )

    @staticmethod
    def unlock_account(user_id: str, unlocked_by) -> None:
        """فك قفل حساب بواسطة المدير."""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError('المستخدم غير موجود')

        profile = SecurityService.get_or_create_profile(user)
        profile.unlock()

        logger.info(
            f"[SecurityService] Account unlocked: {user.username} "
            f"by {unlocked_by.username}"
        )

    # ── Suspicious Login Detection ──

    @staticmethod
    def is_suspicious_login(user, ip_address: str, user_agent: str) -> bool:
        """
        كشف تسجيل دخول مشبوه.
        لا يمنع الدخول — فقط يُسجّل في الـ Audit Log.
        """
        profile = SecurityService.get_or_create_profile(user)
        is_suspicious = profile.is_suspicious_login(ip_address, user_agent)

        if is_suspicious:
            logger.warning(
                f"[SecurityService] Suspicious login detected: {user.username} "
                f"from {ip_address} (previous: {profile.last_known_ip})"
            )

        return is_suspicious

    # ── Password Policies ──

    @staticmethod
    def enforce_password_policy(password: str, user=None) -> List[str]:
        """
        فحص كلمة المرور ضد سياسات Django + سياساتنا الإضافية.
        يُعيد قائمة الانتهاكات (فارغة = كلمة المرور صالحة).
        """
        violations: List[str] = []

        # Django built-in validators
        try:
            validate_password(password, user=user)
        except ValidationError as e:
            violations.extend(e.messages)

        # سياسة إضافية: الحد الأدنى لأنواع الحروف
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not (has_upper and has_lower and has_digit):
            violations.append(
                'كلمة المرور يجب أن تحتوي على حرف كبير وحرف صغير ورقم على الأقل'
            )

        return violations

    @staticmethod
    def check_password_reuse(user, new_password: str) -> bool:
        """
        فحص هل كلمة المرور مُستخدمة سابقاً.
        يُعيد True إذا كانت مُكررة.
        """
        profile = SecurityService.get_or_create_profile(user)
        password_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        return profile.is_password_reused(password_hash)

    @staticmethod
    def record_password_change(user) -> None:
        """تسجيل تغيير كلمة المرور في ملف الأمان."""
        profile = SecurityService.get_or_create_profile(user)
        # نستخدم هاش كلمة المرور الحالية (المُشفرة بالفعل بواسطة Django)
        password_hash = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        profile.record_password_change(password_hash)
        logger.info(f"[SecurityService] Password changed for {user.username}")
