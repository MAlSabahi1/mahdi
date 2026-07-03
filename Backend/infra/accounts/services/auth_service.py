"""
Auth Service — خدمة المصادقة
═════════════════════════════
مسؤولة عن: Login, Logout, Refresh, Change Password.

الـ Flow الحقيقي لتسجيل الدخول (10 خطوات):
    1. Receive credentials
    2. Validate input
    3. Find user
    4. Check account state (is_active)
    5. Check lock state (SecurityProfile)
    6. Verify password
    7. Create session (SessionService)
    8. Generate tokens (JWT)
    9. Save session (DB + Redis)
    10. Return response

لا يوجد أي business logic في Views أو Serializers.
"""
import logging
from datetime import timedelta
from typing import Any, Dict, NamedTuple, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from infra.accounts.models.session import UserSession
from infra.accounts.services.security_service import SecurityService
from infra.accounts.services.session_service import SessionService

logger = logging.getLogger('accounts.auth')

User = get_user_model()

# ── ثوابت ──
ACCESS_TOKEN_LIFETIME_MINUTES: int = 15  # حسب المواصفات


class AuthResult(NamedTuple):
    """نتيجة تسجيل الدخول الناجح."""
    access_token: str
    refresh_token: str
    session_id: str
    user: Any
    expires_in: int
    is_suspicious: bool


class AuthError(Exception):
    """خطأ مصادقة مع رمز قابل للتتبع."""

    def __init__(self, message: str, code: str = 'auth_error', status_code: int = 401):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class AuthService:
    """
    خدمة المصادقة — نقطة الدخول الوحيدة لكل عمليات المصادقة.

    القواعد:
        - Views لا تحتوي على أي business logic
        - Serializers فقط للتحقق من الإدخال
        - كل الأمان والمنطق هنا
    """

    # ══════════════════════════════════════════════════════════════
    # Login — 10-Step Flow
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def login(
        username: str,
        password: str,
        ip_address: str,
        user_agent: str = '',
    ) -> AuthResult:
        """
        تسجيل الدخول — 10 خطوات كاملة.

        Raises:
            AuthError: عند فشل أي خطوة.
        """
        # ─── Step 1 & 2: Receive & Validate ───
        if not username or not password:
            raise AuthError(
                'اسم المستخدم وكلمة المرور مطلوبان',
                code='missing_credentials',
            )

        # ─── Step 3: Find User ───
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # تسجيل المحاولة الفاشلة (لا نكشف أن المستخدم غير موجود)
            SecurityService.record_failed_login(username, ip_address)
            logger.warning(f"[AuthService] Login failed — user not found: {username}")
            raise AuthError(
                'اسم المستخدم أو كلمة المرور غير صحيحة',
                code='invalid_credentials',
            )

        # ─── Step 4: Check Account State ───
        if not user.is_active:
            logger.warning(f"[AuthService] Login failed — inactive account: {username}")
            raise AuthError(
                'الحساب معطّل. تواصل مع المدير.',
                code='account_disabled',
                status_code=403,
            )

        # ─── Step 5: Check Lock State ───
        lock_state = SecurityService.check_lock_state(user)
        if lock_state.is_locked:
            minutes = lock_state.remaining_seconds // 60
            logger.warning(f"[AuthService] Login failed — account locked: {username}")
            raise AuthError(
                f'الحساب مقفل بسبب محاولات دخول فاشلة متعددة. '
                f'حاول بعد {minutes} دقيقة أو تواصل مع المدير.',
                code='account_locked',
                status_code=403,
            )

        # ─── Step 6: Verify Password ───
        if not user.check_password(password):
            SecurityService.record_failed_login(username, ip_address)
            # إعادة فحص القفل بعد التسجيل
            updated_lock = SecurityService.check_lock_state(user)
            remaining = MAX_ATTEMPTS - updated_lock.failed_attempts
            logger.warning(f"[AuthService] Login failed — wrong password: {username}")
            raise AuthError(
                f'اسم المستخدم أو كلمة المرور غير صحيحة. '
                f'متبقي {remaining} محاولة قبل قفل الحساب.',
                code='invalid_credentials',
            )

        # ─── Step 7: Create Session ───
        session, raw_refresh_token = SessionService.create_session(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        # ─── Step 8: Generate JWT Tokens ───
        access_token = AuthService._generate_access_token(user, session)

        # ─── Step 9: Record Successful Login ───
        is_suspicious = SecurityService.is_suspicious_login(
            user, ip_address, user_agent
        )
        SecurityService.record_successful_login(user, ip_address, user_agent)

        # تحديث last_login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        logger.info(
            f"[AuthService] Login successful: {username} from {ip_address} "
            f"session={session.session_id}"
            f"{' [SUSPICIOUS]' if is_suspicious else ''}"
        )

        # ─── Step 10: Return Response ───
        return AuthResult(
            access_token=str(access_token),
            refresh_token=raw_refresh_token,
            session_id=str(session.session_id),
            user=user,
            expires_in=ACCESS_TOKEN_LIFETIME_MINUTES * 60,
            is_suspicious=is_suspicious,
        )

    # ══════════════════════════════════════════════════════════════
    # Logout
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def logout(
        user,
        refresh_token: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> None:
        """
        تسجيل الخروج — إلغاء الجلسة الحالية.

        يمكن الإلغاء بـ refresh_token أو session_id.
        """
        revoked = False

        if session_id:
            revoked = SessionService.revoke_session(session_id, reason='logout')

        elif refresh_token:
            token_hash = UserSession.hash_token(refresh_token)
            try:
                session = UserSession.objects.get(
                    refresh_token_hash=token_hash,
                    user=user,
                    is_active=True,
                )
                session.revoke(reason='logout')
                from django.core.cache import cache
                cache.delete(session.redis_key)
                cache.delete(session.redis_token_key)
                revoked = True
            except UserSession.DoesNotExist:
                pass

        # Blacklist JWT refresh token (للأمان الإضافي)
        if refresh_token:
            AuthService._blacklist_refresh_token(refresh_token)

        logger.info(
            f"[AuthService] Logout: {user.username} "
            f"{'(session revoked)' if revoked else '(token blacklisted only)'}"
        )

    @staticmethod
    def logout_all_devices(user) -> int:
        """تسجيل الخروج من جميع الأجهزة."""
        count = SessionService.revoke_all_user_sessions(user, reason='logout_all')
        logger.info(f"[AuthService] Logout all devices: {user.username} — {count} sessions")
        return count

    # ══════════════════════════════════════════════════════════════
    # Refresh Token
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def refresh_token(
        raw_refresh_token: str,
        ip_address: str,
        user_agent: str = '',
    ) -> AuthResult:
        """
        تجديد التوكن — Token Rotation.

        الخطوات:
            1. التحقق من refresh token
            2. إلغاء التوكن القديم
            3. إنشاء توكن جديد
            4. إنشاء access token جديد
            5. تحديث Redis + DB
        """
        # 1. التحقق
        session = SessionService.validate_refresh_token(raw_refresh_token)

        if not session:
            logger.warning(f"[AuthService] Refresh failed — invalid token from {ip_address}")
            raise AuthError(
                'جلسة غير صالحة أو منتهية. يرجى تسجيل الدخول مجدداً.',
                code='invalid_refresh_token',
            )

        # جلب الجلسة الكاملة من DB (لأن Redis قد لا يحتوي user object)
        try:
            db_session = UserSession.objects.select_related('user').get(
                session_id=session.session_id,
                is_active=True,
            )
        except UserSession.DoesNotExist:
            raise AuthError(
                'الجلسة غير موجودة.',
                code='session_not_found',
            )

        user = db_session.user

        # فحص هل المستخدم لا يزال نشطاً
        if not user.is_active:
            db_session.revoke(reason='user_disabled')
            raise AuthError(
                'الحساب معطّل.',
                code='account_disabled',
                status_code=403,
            )

        # 2 & 3. Token Rotation
        new_raw_refresh = SessionService.rotate_refresh_token(db_session)

        # 4. Access Token جديد
        access_token = AuthService._generate_access_token(user, db_session)

        logger.debug(
            f"[AuthService] Token refreshed: {user.username} "
            f"session={db_session.session_id}"
        )

        return AuthResult(
            access_token=str(access_token),
            refresh_token=new_raw_refresh,
            session_id=str(db_session.session_id),
            user=user,
            expires_in=ACCESS_TOKEN_LIFETIME_MINUTES * 60,
            is_suspicious=False,
        )

    # ══════════════════════════════════════════════════════════════
    # Change Password
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def change_password(
        user,
        old_password: str,
        new_password: str,
    ) -> None:
        """
        تغيير كلمة المرور.

        الخطوات:
            1. التحقق من كلمة المرور الحالية
            2. فحص السياسات (تعقيد + عدم تكرار)
            3. تغيير كلمة المرور
            4. تسجيل التغيير في SecurityProfile
            5. إلغاء جميع الجلسات الأخرى (أمان)
        """
        # 1. التحقق من كلمة المرور الحالية
        if not user.check_password(old_password):
            raise AuthError(
                'كلمة المرور الحالية غير صحيحة',
                code='wrong_current_password',
                status_code=400,
            )

        # 2. فحص السياسات
        violations = SecurityService.enforce_password_policy(new_password, user=user)
        if violations:
            raise AuthError(
                ' | '.join(violations),
                code='password_policy_violation',
                status_code=400,
            )

        if SecurityService.check_password_reuse(user, new_password):
            raise AuthError(
                'لا يمكن استخدام كلمة مرور سبق استخدامها',
                code='password_reused',
                status_code=400,
            )

        # 3. تغيير كلمة المرور
        user.set_password(new_password)
        user.save(update_fields=['password'])

        # 4. تسجيل التغيير
        SecurityService.record_password_change(user)

        # 5. إلغاء جميع الجلسات الأخرى (المستخدم سيحتاج إعادة تسجيل الدخول)
        SessionService.revoke_all_user_sessions(user, reason='password_changed')

        logger.info(f"[AuthService] Password changed: {user.username}")

    # ══════════════════════════════════════════════════════════════
    # JWT Token Generation (Internal)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _generate_access_token(user, session: UserSession) -> AccessToken:
        """
        إنشاء Access Token مع claims إضافية.

        Access Token يحتوي:
            - user_id
            - session_id (لربط التوكن بالجلسة)
            - exp (15 دقيقة)
            - jti (unique ID)
        """
        token = AccessToken()
        token.set_exp(
            from_time=timezone.now(),
            lifetime=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
        )
        token['user_id'] = str(user.pk)
        token['username'] = user.username
        token['session_id'] = str(session.session_id)
        token['full_name'] = user.get_display_name()

        return token

    @staticmethod
    def _blacklist_refresh_token(raw_token: str) -> None:
        """
        إضافة refresh token لقائمة السوداء (simplejwt).
        هذا إجراء أمني إضافي — الجلسة هي المصدر الأساسي للتحقق.
        """
        try:
            token = RefreshToken(raw_token)
            token.blacklist()
        except Exception:
            # التوكن قد لا يكون JWT صالحاً (لأننا نستخدم custom tokens)
            pass


# ── ثابت مستورد من SecurityService ──
from infra.accounts.models.security import MAX_FAILED_ATTEMPTS as MAX_ATTEMPTS  # noqa: E402
