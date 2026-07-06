from functools import wraps
from typing import Optional, Dict, Any, List, Union
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.db import DatabaseError, IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class ServiceRequestException(Exception):
    default_message = _('حدث خطأ في معالجة الطلب')
    default_status_code = status.HTTP_400_BAD_REQUEST
    
    def __init__(
        self, 
        message: str = None, 
        details: Optional[Dict] = None, 
        hint: Optional[str] = None,
        status_code: int = None
    ):
        self.message = message or str(self.default_message)
        self.details = details or {}
        self.hint = hint
        self.status_code = status_code or self.default_status_code
        super().__init__(self.message)
    
    def to_response(self) -> Response:
        response_data = {
            'success': False,
            'error': self.message,
        }
        if self.details:
            response_data['details'] = self.details
        if self.hint:
            response_data['hint'] = self.hint
        return Response(response_data, status=self.status_code)


class ValidationException(ServiceRequestException):
    default_message = _('بيانات غير صالحة')
    default_status_code = status.HTTP_400_BAD_REQUEST


class PermissionDeniedException(ServiceRequestException):
    default_message = _('ليس لديك صلاحية تنفيذ هذا الإجراء')
    default_status_code = status.HTTP_403_FORBIDDEN


class ResourceNotFoundException(ServiceRequestException):
    default_message = _('المورد المطلوب غير موجود')
    default_status_code = status.HTTP_404_NOT_FOUND


class LockedResourceException(ServiceRequestException):
    default_message = _('المورد مقفول ولا يمكن تعديله')
    default_status_code = status.HTTP_400_BAD_REQUEST


class InvalidStatusException(ServiceRequestException):
    default_message = _('لا يمكن تنفيذ هذا الإجراء في الحالة الحالية')
    default_status_code = status.HTTP_400_BAD_REQUEST


class BusinessRuleException(ServiceRequestException):
    default_message = _('العملية تخالف قواعد العمل')
    default_status_code = status.HTTP_400_BAD_REQUEST


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except ServiceRequestException as e:
            return e.to_response()
        
        except DRFValidationError as e:
            return Response({
                'success': False,
                'error': _('بيانات غير صالحة'),
                'details': e.detail if hasattr(e, 'detail') else str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except DjangoValidationError as e:
            return Response({
                'success': False,
                'error': _('خطأ في التحقق من البيانات'),
                'details': e.message_dict if hasattr(e, 'message_dict') else str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError as e:
            return Response({
                'success': False,
                'error': _('خطأ في سلامة البيانات'),
                'hint': _('قد يكون هناك تعارض في البيانات أو قيم مكررة'),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except DatabaseError as e:
            return Response({
                'success': False,
                'error': _('خطأ في قاعدة البيانات'),
                'hint': _('يرجى المحاولة مرة أخرى لاحقاً'),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except ValueError as e:
            return Response({
                'success': False,
                'error': _('قيمة غير صالحة'),
                'details': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except TypeError as e:
            return Response({
                'success': False,
                'error': _('نوع بيانات غير صالح'),
                'details': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception(f"Unexpected error in {func.__name__}: {str(e)}")
            
            return Response({
                'success': False,
                'error': _('حدث خطأ غير متوقع'),
                'hint': _('يرجى التواصل مع الدعم الفني إذا استمرت المشكلة'),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return wrapper

def validate_required_field(value: Any, field_name: str) -> None:
    if value is None or value == '':
        raise ValidationException(
            message=_('الحقل %s مطلوب') % field_name,
            details={'field': field_name}
        )


def validate_positive_number(value: Any, field_name: str) -> None:
    try:
        num = float(value)
        if num <= 0:
            raise ValidationException(
                message=_('الحقل %s يجب أن يكون أكبر من صفر') % field_name,
                details={'field': field_name, 'value': value}
            )
    except (ValueError, TypeError):
        raise ValidationException(
            message=_('الحقل %s يجب أن يكون رقماً صالحاً') % field_name,
            details={'field': field_name, 'value': value}
        )


def validate_percentage(value: Any, field_name: str) -> None:
    try:
        num = float(value)
        if num < 0 or num > 100:
            raise ValidationException(
                message=_('الحقل %s يجب أن يكون بين 0 و 100') % field_name,
                details={'field': field_name, 'value': value}
            )
    except (ValueError, TypeError):
        raise ValidationException(
            message=_('الحقل %s يجب أن يكون نسبة مئوية صالحة') % field_name,
            details={'field': field_name, 'value': value}
        )
