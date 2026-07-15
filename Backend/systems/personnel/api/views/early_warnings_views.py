"""
Early Warning Engine API
═══════════════════════════════════════
يستدعي الخدمة المركزية (ProactiveEngineService) ويعيد النتائج مباشرة.
لا يوجد أي منطق فحص هنا — كل شيء في proactive_engine.py
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from systems.personnel.services.proactive_engine import run_engine_scan


class EarlyWarningsEngineView(APIView):
    """
    GET /api/v1/personnel/early-warnings/
    يفحص قاعدة البيانات بالكامل ويُعيد قائمة الإنذارات المبكرة.
    """
    permission_classes = [permissions.AllowAny]  # في الإنتاج: IsAdminUser

    def get(self, request):
        warnings, stats, settings_used = run_engine_scan()

        return Response({
            'stats': stats,
            'settings': settings_used,
            'results': warnings,
        })
