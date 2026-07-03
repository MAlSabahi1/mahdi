"""
User Service — خدمة إدارة المستخدمين
═════════════════════════════════════════
CRUD كامل للمستخدمين — يُستدعى من Views فقط.
كل business logic هنا — Views نحيفة.
"""
import logging
from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from infra.accounts.models.security import SecurityProfile
from infra.accounts.services.security_service import SecurityService

logger = logging.getLogger('accounts.user')

User = get_user_model()


class UserServiceError(Exception):
    """خطأ في عمليات المستخدم."""

    def __init__(self, message: str, code: str = 'user_error', status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class UserService:
    """
    خدمة إدارة المستخدمين — CRUD + عمليات إدارية.

    القواعد:
        - كل عملية تكون داخل transaction.atomic
        - كل عملية تُسجّل في الـ log
        - SecurityProfile يُنشأ تلقائياً مع المستخدم الجديد
    """

    # ══════════════════════════════════════════════════════════════
    # Create
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def create_user(
        username: str,
        password: str,
        full_name: str = '',
        email: str = '',
        phone: str = '',
        is_staff: bool = False,
        created_by: Optional[Any] = None,
    ) -> Any:
        """
        إنشاء مستخدم جديد مع SecurityProfile.

        Raises:
            UserServiceError: إذا كان اسم المستخدم مستخدماً أو كلمة المرور ضعيفة.
        """
        # التحقق من تكرار اسم المستخدم
        if User.objects.filter(username=username).exists():
            raise UserServiceError(
                'اسم المستخدم مستخدم بالفعل',
                code='username_exists',
            )

        # التحقق من سياسات كلمة المرور
        violations = SecurityService.enforce_password_policy(password)
        if violations:
            raise UserServiceError(
                ' | '.join(violations),
                code='weak_password',
            )

        with transaction.atomic():
            # إنشاء المستخدم
            user = User.objects.create_user(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                is_staff=is_staff,
            )

            # إنشاء SecurityProfile تلقائياً
            SecurityProfile.objects.create(user=user)

            logger.info(
                f"[UserService] User created: {username} "
                f"by {getattr(created_by, 'username', 'system')}"
            )

        return user

    # ══════════════════════════════════════════════════════════════
    # Read
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def get_user(user_id: str) -> Any:
        """جلب مستخدم بالمعرف."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise UserServiceError(
                'المستخدم غير موجود',
                code='user_not_found',
                status_code=404,
            )

    @staticmethod
    def get_user_by_username(username: str) -> Any:
        """جلب مستخدم باسم المستخدم."""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise UserServiceError(
                'المستخدم غير موجود',
                code='user_not_found',
                status_code=404,
            )

    @staticmethod
    def list_users(
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        ordering: str = '-created_at',
    ) -> QuerySet:
        """
        قائمة المستخدمين مع فلترة وبحث.

        Args:
            search: بحث في username, full_name, email
            is_active: فلترة حسب الحالة
            ordering: ترتيب النتائج
        """
        qs = User.objects.all()

        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(username__icontains=search)
                | Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
            )

        return qs.order_by(ordering)

    @staticmethod
    def get_user_detail(user_id: str) -> Dict[str, Any]:
        """
        جلب تفاصيل المستخدم الكاملة (بما في ذلك الأمان والجلسات).
        يُستخدم في صفحة تفاصيل المستخدم للمدير.
        """
        user = UserService.get_user(user_id)
        security = SecurityService.get_or_create_profile(user)

        from infra.accounts.services.session_service import SessionService
        active_sessions = SessionService.get_active_sessions(user)

        return {
            'user': user,
            'security': security,
            'active_sessions_count': len(active_sessions),
            'active_sessions': active_sessions,
        }

    # ══════════════════════════════════════════════════════════════
    # Update
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def update_user(
        user_id: str,
        data: Dict[str, Any],
        updated_by: Optional[Any] = None,
    ) -> Any:
        """
        تحديث بيانات المستخدم.

        الحقول القابلة للتحديث:
            full_name, email, phone, is_active, is_staff
        """
        user = UserService.get_user(user_id)

        allowed_fields = {
            'full_name', 'email', 'phone', 'is_active', 'is_staff',
            'profile_picture', 'bio', 'facebook_link', 'x_link', 'linkedin_link', 'instagram_link'
        }
        update_fields: List[str] = []

        with transaction.atomic():
            for field, value in data.items():
                if field in allowed_fields:
                    if field == 'profile_picture' and value:
                        # Save the physical file first
                        user.profile_picture.save(value.name, value, save=False)
                        update_fields.append(field)
                    else:
                        setattr(user, field, value)
                        update_fields.append(field)

            if update_fields:
                user.save(update_fields=update_fields)

        logger.info(
            f"[UserService] User updated: {user.username} "
            f"fields={update_fields} "
            f"by {getattr(updated_by, 'username', 'system')}"
        )

        return user

    # ══════════════════════════════════════════════════════════════
    # Deactivate / Activate
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def deactivate_user(user_id: str, deactivated_by: Optional[Any] = None) -> None:
        """
        تعطيل حساب مستخدم.
        يُلغي جميع جلساته النشطة فوراً.
        """
        user = UserService.get_user(user_id)

        if not user.is_active:
            raise UserServiceError(
                'الحساب معطّل بالفعل',
                code='already_deactivated',
            )

        with transaction.atomic():
            user.is_active = False
            user.save(update_fields=['is_active'])

            # إلغاء جميع الجلسات
            from infra.accounts.services.session_service import SessionService
            SessionService.revoke_all_user_sessions(user, reason='account_deactivated')

        logger.info(
            f"[UserService] User deactivated: {user.username} "
            f"by {getattr(deactivated_by, 'username', 'system')}"
        )

    @staticmethod
    def activate_user(user_id: str, activated_by: Optional[Any] = None) -> None:
        """تفعيل حساب مستخدم معطّل."""
        user = UserService.get_user(user_id)

        if user.is_active:
            raise UserServiceError(
                'الحساب نشط بالفعل',
                code='already_active',
            )

        user.is_active = True
        user.save(update_fields=['is_active'])

        logger.info(
            f"[UserService] User activated: {user.username} "
            f"by {getattr(activated_by, 'username', 'system')}"
        )

    # ══════════════════════════════════════════════════════════════
    # Password Management (Admin)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def reset_password(
        user_id: str,
        new_password: str,
        reset_by: Optional[Any] = None,
    ) -> None:
        """
        إعادة تعيين كلمة المرور بواسطة المدير.
        يُفعّل must_change_password ويُلغي جميع الجلسات.
        """
        user = UserService.get_user(user_id)

        # فحص سياسات كلمة المرور
        violations = SecurityService.enforce_password_policy(new_password, user=user)
        if violations:
            raise UserServiceError(
                ' | '.join(violations),
                code='weak_password',
            )

        with transaction.atomic():
            user.set_password(new_password)
            user.save(update_fields=['password'])

            # تسجيل التغيير + تفعيل must_change_password
            security = SecurityService.get_or_create_profile(user)
            security.must_change_password = True
            security.save(update_fields=['must_change_password'])
            SecurityService.record_password_change(user)

            # إلغاء جميع الجلسات
            from infra.accounts.services.session_service import SessionService
            SessionService.revoke_all_user_sessions(user, reason='password_reset')

        logger.info(
            f"[UserService] Password reset: {user.username} "
            f"by {getattr(reset_by, 'username', 'system')}"
        )

    # ══════════════════════════════════════════════════════════════
    # Account Unlock (Admin)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def unlock_account(user_id: str, unlocked_by: Optional[Any] = None) -> None:
        """فك قفل حساب مستخدم — للمدير فقط."""
        SecurityService.unlock_account(user_id, unlocked_by)
        logger.info(
            f"[UserService] Account unlocked for user_id={user_id} "
            f"by {getattr(unlocked_by, 'username', 'system')}"
        )
