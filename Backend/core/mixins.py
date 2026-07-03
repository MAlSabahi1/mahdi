"""
StandardResponseMixin - غلاف استجابة موحد لجميع الـ API
يضمن أن جميع الاستجابات تتبع نفس التنسيق:
  - القوائم: {success: true, count, next, previous, results: [...]}
  - التفاصيل/الإنشاء/التعديل: {success: true, data: {...}, message?: str}
  - الحذف: {success: true, message: str}
"""
from rest_framework.response import Response
from rest_framework import status


class StandardResponseMixin:
    """
    Mixin يغلف استجابات DRF القياسية بتنسيق موحد.
    يتم تطبيقه تلقائياً على list/retrieve/create/update/destroy.
    الاستجابات المغلفة مسبقاً (التي تحتوي على مفتاح 'success') تمر كما هي.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if not hasattr(response, 'data') or response.data is None:
            return response

        # Skip if already wrapped
        if isinstance(response.data, dict) and 'success' in response.data:
            return response

        # Skip error responses (handled by exception_handler)
        if response.status_code >= 400:
            return response

        # Skip non-JSON responses (file downloads, etc.)
        content_type = response.get('Content-Type', '')
        if content_type and 'json' not in content_type and content_type != '':
            return response

        action = getattr(self, 'action', None)

        if action == 'list':
            # Paginated responses already have count/next/previous/results
            if isinstance(response.data, dict) and 'results' in response.data:
                response.data = {
                    'success': True,
                    **response.data,
                }
            elif isinstance(response.data, list):
                response.data = {
                    'success': True,
                    'count': len(response.data),
                    'next': None,
                    'previous': None,
                    'results': response.data,
                }
            else:
                response.data = {'success': True, 'data': response.data}

        elif action == 'retrieve':
            response.data = {'success': True, 'data': response.data}

        elif action == 'create':
            response.data = {
                'success': True,
                'data': response.data,
                'message': 'تم الإنشاء بنجاح',
            }

        elif action in ('update', 'partial_update'):
            response.data = {
                'success': True,
                'data': response.data,
                'message': 'تم التحديث بنجاح',
            }

        elif action == 'destroy':
            response.data = {
                'success': True,
                'message': 'تم الحذف بنجاح',
            }
            if response.status_code == status.HTTP_204_NO_CONTENT:
                response.status_code = status.HTTP_200_OK

        else:
            # Custom actions that return unwrapped data
            response.data = {'success': True, 'data': response.data}

        return response
