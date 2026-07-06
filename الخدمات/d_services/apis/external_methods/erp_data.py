"""
دوال بيانات ERP - ERP Data Functions
الدوال المستخدمة في حقل erp_data_function على Service model.
تُستدعى لجلب القيم الافتراضية لـ ERP.

Signature: function(user, data) -> dict
  - user:  request.user
  - data:  request data dict (could be None)
"""
import logging
from typing import Any, Dict, Optional

from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.ServiceERPSettings import ServiceERPSettings
from student_affairs.models.StudentBatch import StudentBatch
from student_affairs.models.StudentCourse import StudentLevel
from student_affairs.models.Student import Student

logger = logging.getLogger(__name__)
def get_student_batch(data):
    """
    دالة مساعدة لجلب سجل الدفعة من بيانات الطلب (data).
    يتم جلب المعرف من target_audience_data تحت المفتاح fk_student_batch.
    """
    target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}

    # بناءً على تحليل ملفات target_audience.json، المفتاح الرئيسي هو fk_student_batch
    student_batch_id = target_audience_data.get('fk_student_batch')

    if not student_batch_id:
        raise Exception("لم يتم العثور على معرف سجل الدفعة (fk_student_batch) في بيانات الطلب.")

    try:
        return StudentBatch.objects.get(id=student_batch_id)
    except StudentBatch.DoesNotExist:
        raise Exception(f"سجل الدفعة ذو المعرف {student_batch_id} غير موجود.")



def get_erp_defaults(user, data=None) -> Dict[str, Any]:
    """
    مثال: جلب بيانات ERP الافتراضية.

    يتم استدعاؤها من ERPHandler.get_erp_data عبر ExternalMethodHandler
    عندما يكون service.erp_data_function = 'call_get_erp_defaults'.

    Args:
        user:  request.user
        data:  request data dict (يحتوي على target_audience_data, specialization_id, etc.)

    Returns:
        dict يحتوي على القيم الافتراضية مثل:
        {
            'service_fee': Decimal('500.00'),
            'fk_currency': 1,
            'is_donor_invoice_allowed': True,
            'is_discount_allowed': True,
            'erp_product_id': 'PROD-001',
            'erp_product_name': 'رسوم خدمة',
            ...
        }
    """
    # --- هنا يمكن الاتصال بنظام ERP خارجي أو تطبيق منطق خاص ---
    # يمكنك استخدام user و data لتحديد القيم المناسبة

    # مثال: إرجاع قيم ثابتة (استبدلها بمنطقك الخاص)
    return {
        # 'service_fee': Decimal('500.00'),
        # 'fk_currency': 1,
        # 'erp_product_id': 'PROD-001',
        # 'erp_product_name': 'رسوم خدمة',
    }

def get_service_erp_settings(student,specialization_id,study_system_id,user,data=None):

    fk_service = data.get('fk_service')
    fk_organization = user.fk_organization if hasattr(user, 'fk_organization') else None
    available_grant_sources_ids = []

    if isinstance(student,Student):
        available_grant_sources_ids = list(student.fk_grant_sources.values_list('id', flat=True))
    student_address= student.fk_address if student.fk_address  else None
    country_code = student_address.fk_country.code if hasattr(student_address, 'fk_country') else None
    governorate_code = student_address.fk_governorate.code if hasattr(student_address, 'fk_governorate') else None
    directorate_code = student_address.fk_directorate.code if hasattr(student_address, 'fk_directorate') else None
    street = student_address.street if hasattr(student_address, 'street') else None

    erp_settings = {
        "available_grant_sources_ids":available_grant_sources_ids,
        "partner_data":{
            'company_type':'individule',
            'first_name':student.full_name_ar,
            'middle_name':None,
            'last_name':None,
            'surename':None,
            'country':country_code,
            'governorate':governorate_code,
            'city':directorate_code,
            'area':street,
            'branch':None,
            'phone': student.phone_no,
            'mobile':student.mobile_no,
            'email':student.fk_user.email if hasattr(student,'fk_user') else None,
            'website':None,
            'categories':[],
        }
    }
    org_config = OrganizationServiceConfig.objects.filter(
        fk_service_id=fk_service, fk_organization=fk_organization, is_active=True
    ).first()
    erp_service_settings = ServiceERPSettings.objects.filter(
        specialization_id=specialization_id,
        study_system_id=study_system_id,
        fk_org_service_config=org_config
    ).first()
    if not erp_service_settings:
        from ..ServiceERPSettings import _get_org_config_defaults
        erp_settings.update(_get_org_config_defaults(org_config))
        return erp_settings
    erp_settings.update({
        'service_fee': erp_service_settings.service_fee,
        'fk_currency': erp_service_settings.fk_currency.code if erp_service_settings.fk_currency else None,
        'is_donor_invoice_allowed': erp_service_settings.is_donor_invoice_allowed,
        'is_discount_allowed': erp_service_settings.is_discount_allowed,
        'erp_product_id': erp_service_settings.erp_product_id,
        'erp_product_name': erp_service_settings.erp_product_name,
        'erp_product_for_discount_id': erp_service_settings.erp_product_for_discount_id,
        'erp_product_for_discount_name': erp_service_settings.erp_product_for_discount_name,
        'erp_product_for_internal_donors_id': erp_service_settings.erp_product_for_internal_donors_id,
        'erp_product_for_internal_donors_name': erp_service_settings.erp_product_for_internal_donors_name,
        'erp_project_id': erp_service_settings.erp_project_id,
        'erp_project_name': erp_service_settings.erp_project_name,
        'erp_activity_id': erp_service_settings.erp_activity_id,
        'erp_activity_name': erp_service_settings.erp_activity_name,
        'erp_cost_center_id': erp_service_settings.erp_cost_center_id,
        'erp_cost_center_name': erp_service_settings.erp_cost_center_name,
    })
    return erp_settings

def call_get_erp_settings_by_student_batch(user, data=None) -> Dict[str, Any]:
    """جلب اعدادات الـ ERP اعتمادا على سجل الدفعة للطالب"""
    student_batch = get_student_batch(data)
    student = student_batch.fk_student
    specialization = student_batch.fk_batch.fk_specialization.id if student_batch.fk_batch.fk_specialization else None
    study_system = student_batch.fk_study_system.id if student_batch.fk_study_system else None
    return get_service_erp_settings(student,specialization, study_system, user, data)

def call_get_erp_settings_by_student_level(user, data=None) -> Dict[str, Any]:
    """جلب اعدادات الـ ERP اعتمادا على سجل المستوى للطالب"""
    target_audience_data = data.get('target_audience_data') if isinstance(data,dict) else {}
    fk_student_level = target_audience_data.get('fk_student_level')
    student_level = StudentLevel.objects.get(id=fk_student_level)
    student_batch = student_level.fk_student_batch if student_level else None
    student = student_batch.fk_student if student_batch else None
    specialization = student_batch.fk_batch.fk_specialization.id if student_batch.fk_batch.fk_specialization else None
    study_system = student_batch.fk_study_system.id if student_batch.fk_study_system else None
    return get_service_erp_settings(student,specialization, study_system, user, data)
