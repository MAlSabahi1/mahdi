"""
Session Views — واجهات API الجلسات (إدارة الأجهزة)
═══════════════════════════════════════════════════════
يعرض للمستخدم أجهزته النشطة ويسمح له بإلغاء أي جلسة.

Endpoints:
    GET    /sessions/              — الأجهزة النشطة
    POST   /sessions/terminate/    — إلغاء جلسة معينة
    POST   /sessions/terminate-all/ — إلغاء جميع الجلسات
"""
import logging

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from infra.accounts.serializers.session_serializers import (
    SessionOutputSerializer,
    TerminateSessionSerializer,
)
from infra.accounts.services.session_service import SessionService

logger = logging.getLogger('accounts.views.session')


class SessionViewSet(ViewSet):
    """
    إدارة الأجهزة النشطة.
    المستخدم يمكنه رؤية أجهزته وإلغاء أي جلسة.
    """
    permission_classes = [permissions.IsAuthenticated]

    # ── List Active Sessions ──

    @extend_schema(
        responses={200: SessionOutputSerializer(many=True)},
        tags=['sessions'],
        summary='الأجهزة النشطة',
        description='عرض جميع الأجهزة/الجلسات النشطة للمستخدم الحالي',
    )
    def list(self, request) -> Response:
        """GET /sessions/"""
        sessions = SessionService.get_active_sessions(request.user)
        serializer = SessionOutputSerializer(
            sessions,
            many=True,
            context={'request': request},
        )

        return Response({
            'success': True,
            'count': len(sessions),
            'data': serializer.data,
        })

    # ── Terminate Single Session ──

    @extend_schema(
        request=TerminateSessionSerializer,
        tags=['sessions'],
        summary='إلغاء جلسة',
        description='إلغاء جلسة معينة (تسجيل خروج من جهاز محدد)',
    )
    def terminate(self, request) -> Response:
        """POST /sessions/terminate/"""
        serializer = TerminateSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = str(serializer.validated_data['session_id'])
        success = SessionService.revoke_session(
            session_id=session_id,
            reason='user_terminated',
        )

        if not success:
            return Response(
                {
                    'success': False,
                    'error': 'الجلسة غير موجودة أو ملغاة بالفعل',
                },
                status=404,
            )

        return Response({
            'success': True,
            'message': 'تم إلغاء الجلسة بنجاح',
        })

    # ── Terminate All Sessions ──

    @extend_schema(
        tags=['sessions'],
        summary='إلغاء جميع الجلسات',
        description='تسجيل الخروج من جميع الأجهزة',
    )
    def terminate_all(self, request) -> Response:
        """POST /sessions/terminate-all/"""
        count = SessionService.revoke_all_user_sessions(
            user=request.user,
            reason='user_terminated_all',
        )

        return Response({
            'success': True,
            'message': f'تم إلغاء {count} جلسة',
            'data': {'revoked_count': count},
        })
