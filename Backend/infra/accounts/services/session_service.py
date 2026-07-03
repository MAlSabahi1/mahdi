"""
Session Service — خدمة إدارة الجلسات
═════════════════════════════════════════
Hybrid Architecture:
    Redis = Fast Layer (session cache, token lookup, activity tracking)
    PostgreSQL = Source of Truth (persistent truth, fallback)

التدفق:
    Client → Refresh Token → Redis lookup →
    If valid: rotate token + update session
    Else: DB fallback → rotate + sync to Redis
"""
import logging
import secrets
import uuid
from datetime import timedelta
from typing import Dict, List, Optional, NamedTuple

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from infra.accounts.models.session import UserSession

logger = logging.getLogger('accounts.session')

# ── ثوابت ──
SESSION_TTL_DAYS: int = 7
REDIS_SESSION_TTL: int = SESSION_TTL_DAYS * 24 * 60 * 60  # بالثواني
INACTIVITY_TIMEOUT_SECONDS: int = getattr(settings, 'SESSION_INACTIVITY_TIMEOUT', 1800)
MAX_SESSIONS_PER_USER: int = getattr(settings, 'MAX_SESSIONS_PER_USER', 5)


class TokenPair(NamedTuple):
    """زوج التوكنات الناتج عن Login أو Refresh."""
    access_token: str
    refresh_token: str
    session_id: str
    expires_in: int


class SessionService:
    """
    خدمة الجلسات — Hybrid JWT + Session Layer.

    المسؤوليات:
        - إنشاء جلسة جديدة عند Login
        - التحقق من Refresh Token (Redis → DB fallback)
        - تدوير التوكنات (Token Rotation) لمنع Replay Attack
        - إلغاء جلسة / جميع الجلسات
        - تتبع النشاط وإلغاء الجلسات الخاملة
        - إدارة الأجهزة النشطة
    """

    # ══════════════════════════════════════════════════════════════
    # إنشاء الجلسة
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def create_session(
        user,
        ip_address: str,
        user_agent: str = '',
        device_name: str = '',
        browser: str = '',
        os_name: str = '',
    ) -> tuple:
        """
        إنشاء جلسة جديدة عند Login.

        Returns:
            (session, raw_refresh_token) — التوكن الخام يُرسل للعميل مرة واحدة فقط.
        """
        # 1. فحص عدد الجلسات النشطة
        active_count = UserSession.objects.filter(
            user=user, is_active=True
        ).count()

        if active_count >= MAX_SESSIONS_PER_USER:
            # إلغاء أقدم جلسة
            oldest = UserSession.objects.filter(
                user=user, is_active=True
            ).order_by('created_at').first()
            if oldest:
                SessionService.revoke_session(
                    str(oldest.session_id), reason='max_sessions_exceeded'
                )
                logger.info(
                    f"[SessionService] Revoked oldest session for {user.username} "
                    f"(max {MAX_SESSIONS_PER_USER} reached)"
                )

        # 2. إنشاء refresh token خام
        raw_refresh_token = secrets.token_urlsafe(64)
        token_hash = UserSession.hash_token(raw_refresh_token)

        # 3. إنشاء الجلسة في DB
        session = UserSession.objects.create(
            user=user,
            refresh_token_hash=token_hash,
            ip_address=ip_address,
            user_agent=user_agent,
            device_name=device_name or SessionService._extract_device_name(user_agent),
            browser=browser or SessionService._extract_browser(user_agent),
            os=os_name or SessionService._extract_os(user_agent),
            expires_at=timezone.now() + timedelta(days=SESSION_TTL_DAYS),
            last_activity=timezone.now(),
        )

        # 4. مزامنة مع Redis
        SessionService._sync_to_redis(session)

        logger.info(
            f"[SessionService] Session created: {session.session_id} "
            f"for {user.username} from {ip_address}"
        )

        return session, raw_refresh_token

    # ══════════════════════════════════════════════════════════════
    # التحقق من Refresh Token (Redis → DB fallback)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def validate_refresh_token(raw_token: str) -> Optional[UserSession]:
        """
        التحقق من صحة refresh token.

        التدفق:
            1. حساب hash للتوكن
            2. البحث في Redis أولاً (سريع)
            3. إذا لم يوجد → DB fallback
            4. فحص الصلاحية (نشطة + غير منتهية)
        """
        token_hash = UserSession.hash_token(raw_token)

        # 1. Redis lookup
        session = SessionService._lookup_redis(token_hash)
        if session and session.is_valid:
            logger.debug(f"[SessionService] Token validated via Redis: {session.session_id}")
            return session

        # 2. DB fallback
        session = SessionService._fallback_to_db(token_hash)
        if session and session.is_valid:
            # إعادة مزامنة مع Redis
            SessionService._sync_to_redis(session)
            logger.info(f"[SessionService] Token validated via DB fallback: {session.session_id}")
            return session

        logger.warning(f"[SessionService] Invalid refresh token attempted")
        return None

    # ══════════════════════════════════════════════════════════════
    # Token Rotation (منع Replay Attack)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def rotate_refresh_token(session: UserSession) -> str:
        """
        تدوير Refresh Token — أهم خطوة أمنية.

        الخطوات:
            1. إنشاء refresh token جديد
            2. إلغاء التوكن القديم (تحديث الهاش)
            3. تحديث Redis
            4. تحديث DB

        Returns:
            raw_refresh_token الجديد — يُرسل للعميل.
        """
        # 1. حذف التوكن القديم من Redis
        old_token_key = f"token:{session.refresh_token_hash}"
        cache.delete(old_token_key)

        # 2. إنشاء توكن جديد
        new_raw_token = secrets.token_urlsafe(64)
        new_hash = UserSession.hash_token(new_raw_token)

        # 3. تحديث DB
        session.refresh_token_hash = new_hash
        session.last_activity = timezone.now()
        session.save(update_fields=['refresh_token_hash', 'last_activity'])

        # 4. مزامنة مع Redis
        SessionService._sync_to_redis(session)

        logger.debug(f"[SessionService] Token rotated for session {session.session_id}")

        return new_raw_token

    # ══════════════════════════════════════════════════════════════
    # إلغاء الجلسات
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def revoke_session(session_id: str, reason: str = 'manual') -> bool:
        """إلغاء جلسة واحدة."""
        try:
            session = UserSession.objects.get(
                session_id=session_id, is_active=True
            )
        except UserSession.DoesNotExist:
            logger.warning(f"[SessionService] Session not found for revoke: {session_id}")
            return False

        # إلغاء في DB
        session.revoke(reason=reason)

        # حذف من Redis
        cache.delete(session.redis_key)
        cache.delete(session.redis_token_key)

        logger.info(
            f"[SessionService] Session revoked: {session_id} "
            f"reason={reason} user={session.user}"
        )
        return True

    @staticmethod
    def revoke_all_user_sessions(user, reason: str = 'logout_all') -> int:
        """إلغاء جميع جلسات المستخدم — Logout from all devices."""
        sessions = UserSession.objects.filter(user=user, is_active=True)
        count = 0

        for session in sessions:
            session.revoke(reason=reason)
            cache.delete(session.redis_key)
            cache.delete(session.redis_token_key)
            count += 1

        logger.info(
            f"[SessionService] All sessions revoked for {user.username}: "
            f"{count} sessions, reason={reason}"
        )
        return count

    # ══════════════════════════════════════════════════════════════
    # إدارة الأجهزة (Device Management)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_active_sessions(user) -> List[UserSession]:
        """جلب الجلسات النشطة للمستخدم — لعرض الأجهزة."""
        return list(
            UserSession.objects.filter(
                user=user, is_active=True
            ).order_by('-last_activity')
        )

    # ══════════════════════════════════════════════════════════════
    # تتبع النشاط (Activity Tracking)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def update_activity(session_id: str) -> bool:
        """
        تحديث آخر نشاط — يُستدعى من Middleware.
        يُحدّث Redis أولاً (سريع)، ثم DB بشكل دوري.
        """
        redis_key = f"session:{session_id}"
        now = timezone.now().isoformat()

        # تحديث Redis
        try:
            cached = cache.get(redis_key)
            if cached and isinstance(cached, dict):
                cached['last_activity'] = now
                cache.set(redis_key, cached, REDIS_SESSION_TTL)
                return True
        except Exception as e:
            logger.debug(f"[SessionService] Redis update_activity failed: {e}")

        # Fallback: تحديث DB مباشرة
        updated = UserSession.objects.filter(
            session_id=session_id, is_active=True
        ).update(last_activity=timezone.now())

        return updated > 0

    @staticmethod
    def check_inactivity(session_id: str) -> bool:
        """
        فحص الخمول — يُعيد True إذا الجلسة خاملة ويجب إلغاؤها.

        القاعدة: 30 دقيقة بدون نشاط → session revoke.
        """
        try:
            session = UserSession.objects.get(
                session_id=session_id, is_active=True
            )
        except UserSession.DoesNotExist:
            return True

        if session.inactivity_seconds > INACTIVITY_TIMEOUT_SECONDS:
            session.revoke(reason='inactivity')
            cache.delete(session.redis_key)
            cache.delete(session.redis_token_key)
            logger.info(
                f"[SessionService] Session revoked due to inactivity: "
                f"{session_id} ({session.inactivity_seconds}s idle)"
            )
            return True

        return False

    # ══════════════════════════════════════════════════════════════
    # تنظيف الجلسات المنتهية
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def cleanup_expired_sessions() -> int:
        """حذف/إلغاء الجلسات المنتهية — يُشغّل دورياً عبر Celery."""
        expired = UserSession.objects.filter(
            is_active=True,
            expires_at__lt=timezone.now(),
        )
        count = 0
        for session in expired:
            session.revoke(reason='expired')
            cache.delete(session.redis_key)
            cache.delete(session.redis_token_key)
            count += 1

        if count > 0:
            logger.info(f"[SessionService] Cleaned up {count} expired sessions")
        return count

    # ══════════════════════════════════════════════════════════════
    # Redis Layer (الطبقة السريعة)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _sync_to_redis(session: UserSession) -> None:
        """مزامنة جلسة مع Redis."""
        try:
            redis_data = session.to_redis_dict()

            # تخزين بمفتاح session_id
            cache.set(session.redis_key, redis_data, REDIS_SESSION_TTL)

            # تخزين mapping: token_hash → session_id (للبحث السريع)
            cache.set(
                session.redis_token_key,
                str(session.session_id),
                REDIS_SESSION_TTL,
            )
        except Exception as e:
            # Redis فشل — لا نكسر العملية، DB هو Source of Truth
            logger.error(f"[SessionService] Redis sync failed: {e}")

    @staticmethod
    def _lookup_redis(token_hash: str) -> Optional[UserSession]:
        """البحث عن جلسة في Redis عبر token hash."""
        try:
            token_key = f"token:{token_hash}"
            session_id = cache.get(token_key)

            if not session_id:
                return None

            session_key = f"session:{session_id}"
            redis_data = cache.get(session_key)

            if not redis_data or not isinstance(redis_data, dict):
                return None

            return UserSession.from_redis_dict(redis_data)
        except Exception as e:
            logger.debug(f"[SessionService] Redis lookup failed: {e}")
            return None

    @staticmethod
    def _fallback_to_db(token_hash: str) -> Optional[UserSession]:
        """البحث عن جلسة في DB — fallback عندما Redis يفشل."""
        try:
            return UserSession.objects.select_related('user').get(
                refresh_token_hash=token_hash,
                is_active=True,
            )
        except UserSession.DoesNotExist:
            return None

    # ══════════════════════════════════════════════════════════════
    # User Agent Parsing (استخراج بيانات الجهاز)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _extract_device_name(user_agent: str) -> str:
        """استخراج اسم الجهاز من User Agent."""
        if not user_agent:
            return 'Unknown Device'
        ua = user_agent.lower()
        if 'iphone' in ua:
            return 'iPhone'
        if 'ipad' in ua:
            return 'iPad'
        if 'android' in ua and 'mobile' in ua:
            return 'Android Phone'
        if 'android' in ua:
            return 'Android Tablet'
        if 'macintosh' in ua or 'mac os' in ua:
            return 'Mac'
        if 'windows' in ua:
            return 'Windows PC'
        if 'linux' in ua:
            return 'Linux PC'
        return 'Unknown Device'

    @staticmethod
    def _extract_browser(user_agent: str) -> str:
        """استخراج اسم المتصفح من User Agent."""
        if not user_agent:
            return 'Unknown'
        ua = user_agent.lower()
        if 'edg/' in ua or 'edge/' in ua:
            return 'Microsoft Edge'
        if 'chrome/' in ua and 'safari/' in ua:
            return 'Google Chrome'
        if 'firefox/' in ua:
            return 'Mozilla Firefox'
        if 'safari/' in ua and 'chrome/' not in ua:
            return 'Safari'
        if 'opera' in ua or 'opr/' in ua:
            return 'Opera'
        return 'Unknown'

    @staticmethod
    def _extract_os(user_agent: str) -> str:
        """استخراج نظام التشغيل من User Agent."""
        if not user_agent:
            return 'Unknown'
        ua = user_agent.lower()
        if 'windows nt 10' in ua:
            return 'Windows 10/11'
        if 'windows' in ua:
            return 'Windows'
        if 'mac os x' in ua:
            return 'macOS'
        if 'iphone os' in ua or 'ipad' in ua:
            return 'iOS'
        if 'android' in ua:
            return 'Android'
        if 'linux' in ua:
            return 'Linux'
        return 'Unknown'
