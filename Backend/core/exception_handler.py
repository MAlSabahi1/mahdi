"""
Global Exception Handler — معالج الأخطاء المركزي
════════════════════════════════════════════════════
يعمل مع كل الأخطاء في النظام:
    1. AppError وأبناؤه (core.exceptions) ← يُحوّل تلقائياً
    2. DRF Exceptions ← يُلف بتنسيق موحد
    3. Django Exceptions ← يُلتقط ويُترجم

التنسيق الموحد:
    {
        "success": false,
        "error": {
            "code": 400,
            "type": "validation_error",
            "message": "بيانات غير صالحة",
            "details": {...}
        }
    }

الإعداد في settings.py:
    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'core.exception_handler.global_exception_handler',
    }
"""
import logging

from django.core.exceptions import PermissionDenied, ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core.exceptions import AppError

logger = logging.getLogger('core.exceptions')


def global_exception_handler(exc, context):
    """
    معالج أخطاء مركزي — نقطة واحدة لكل الأخطاء.

    التدفق:
        1. AppError → to_dict() مباشرة
        2. DRF Exception → تنسيق موحد
        3. Django Exception → تحويل + تنسيق
        4. أي شيء آخر → 500 مع رسالة آمنة
    """

    # ── 1. AppError (core.exceptions) ──
    if isinstance(exc, AppError):
        logger.warning(
            f"[AppError] {exc.code}: {exc.message}",
            extra={'details': exc.details},
        )
        return Response(exc.to_dict(), status=exc.status_code)

    # ── 2. DRF Built-in Exceptions ──
    response = drf_exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'type': type(exc).__name__,
                'detail': _extract_detail(response.data),
            },
        }

        # رسائل مخصصة حسب الكود
        messages = {
            401: 'غير مصادق — يرجى تسجيل الدخول',
            403: 'ليس لديك صلاحية للقيام بهذه العملية',
            404: 'المورد المطلوب غير موجود',
            405: 'الطريقة غير مسموحة',
            429: 'تجاوزت الحد الأقصى للطلبات — حاول لاحقاً',
            400: 'بيانات غير صالحة',
        }
        error_data['error']['message'] = messages.get(
            response.status_code, 'حدث خطأ'
        )

        # Retry-After header (429)
        if response.status_code == 429:
            retry_after = response.get('Retry-After')
            if retry_after:
                error_data['error']['retry_after'] = int(retry_after)

        response.data = error_data
        return response

    # ── 3. Django Built-in Exceptions ──
    if isinstance(exc, PermissionDenied):
        return Response(
            {
                'success': False,
                'error': {
                    'code': 403,
                    'type': 'PermissionDenied',
                    'message': str(exc) or 'ليس لديك صلاحية',
                },
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                'success': False,
                'error': {
                    'code': 400,
                    'type': 'ValidationError',
                    'message': 'بيانات غير صالحة',
                    'detail': exc.messages if hasattr(exc, 'messages') else [str(exc)],
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, Http404):
        return Response(
            {
                'success': False,
                'error': {
                    'code': 404,
                    'type': 'NotFound',
                    'message': 'المورد المطلوب غير موجود',
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # ── 4. أخطاء غير متوقعة ──
    logger.exception(f"[Unhandled Exception] {type(exc).__name__}: {exc}")
    return None  # Django يعالج الباقي (500 page في DEBUG=True)


def _extract_detail(data):
    """استخراج تفاصيل الخطأ من بيانات DRF."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, list):
                result[key] = [str(v) for v in value]
            else:
                result[key] = str(value)
        return result
    elif isinstance(data, list):
        return [str(item) for item in data]
    return str(data)
