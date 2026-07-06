"""
Image Handler - معالج الصور
دوال مساعدة لجلب وحفظ صور المستخدمين
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ImageHandler:
    """معالج صور المستخدمين"""
    
    @staticmethod
    def get_user_image_url(user) -> Optional[str]:
        """جلب URL صورة المستخدم من البيانات المتاحة"""
        if hasattr(user, 'image') and user.image:
            return user.image.url
        
        if hasattr(user, 'profile') and hasattr(user.profile, 'image') and user.profile.image:
            return user.profile.image.url
        
        if hasattr(user, 'avatar') and user.avatar:
            return user.avatar.url
        
        if hasattr(user, 'student_sync') and user.student_sync:
            student = user.student_sync
            if hasattr(student, 'image') and student.image:
                return student.image.url
        
        return None
    
    @staticmethod
    def get_user_image_for_request(user):
        """جلب صورة المستخدم لحفظها في الطلب (الطريقة الافتراضية)"""
        if hasattr(user, 'image') and user.image:
            return user.image
        
        if hasattr(user, 'avatar') and user.avatar:
            return user.avatar
        
        if hasattr(user, 'student_sync') and user.student_sync:
            student = user.student_sync
            if hasattr(student, 'image') and student.image:
                return student.image
        
        return None
    
    @staticmethod
    def get_image_from_function(function_name: str, user, data=None):
        """
        جلب الصورة باستخدام دالة خارجية آمنة
        تستخدم ExternalMethodHandler للأمان
        """
        if not function_name:
            return ImageHandler.get_user_image_for_request(user)
        
        try:
            from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
            
            success, result = ExternalMethodHandler.call_function(
                function_name, user, data, function_type=FunctionType.REQUESTER
            )
            if success and result:
                return result
            else:
                logger.warning(f"Failed to get image from function {function_name}, using default")
                return ImageHandler.get_user_image_for_request(user)
                
        except Exception as e:
            logger.warning(f"Error calling image function {function_name}: {e}")
            return ImageHandler.get_user_image_for_request(user)
    
    @staticmethod
    def get_image_for_service(service, user, data=None):
        """
        جلب صورة مقدم الطلب حسب إعدادات الخدمة
        يستخدم الدالة المحددة في Service.requester_image_function إذا وجدت
        """
        function_name = getattr(service, 'requester_image_function', None)
        return ImageHandler.get_image_from_function(function_name, user, data)
    
    @staticmethod
    def get_info_for_service(service, user, data=None):
        """
        جلب بيانات مقدم الطلب (الاسم والوصف) حسب إعدادات الخدمة
        يستخدم الدالة المحددة في Service.requester_info_function إذا وجدت
        
        Returns:
            dict: {'name': str, 'description': str} أو None
        """
        function_name = getattr(service, 'requester_info_function', None)
        
        if not function_name:
            # الطريقة الافتراضية - استخدام بيانات المستخدم
            return ImageHandler.get_default_user_info(user)
        
        try:
            from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
            
            success, result = ExternalMethodHandler.call_function(
                function_name, user, data, function_type=FunctionType.REQUESTER
            )
            if success and result and isinstance(result, dict):
                return {
                    'id':result.get('id'),
                    'name': result.get('name', ''),
                    'description': result.get('description', '')
                }
            else:
                logger.warning(f"Failed to get info from function {function_name}, using default")
                return ImageHandler.get_default_user_info(user)
                
        except Exception as e:
            logger.warning(f"Error calling info function {function_name}: {e}")
            return ImageHandler.get_default_user_info(user)
    
    @staticmethod
    def get_default_user_info(user):
        """جلب بيانات المستخدم الافتراضية"""
        user_id = getattr(user,'id',None)
        name = ''
        description = ''
        
        # جلب الاسم
        if hasattr(user, 'get_full_name'):
            name = user.get_full_name() or ''
        if not name:
            name = getattr(user, 'first_name', '') + ' ' + getattr(user, 'last_name', '')
            name = name.strip()
        if not name:
            name = getattr(user, 'username', '')
        
        # جلب الوصف من student_sync إذا وجد
        if hasattr(user, 'student_sync') and user.student_sync:
            student = user.student_sync
            parts = []
            if hasattr(student, 'fk_college') and student.fk_college:
                parts.append(str(student.fk_college))
            if hasattr(student, 'fk_specialization') and student.fk_specialization:
                parts.append(str(student.fk_specialization))
            if hasattr(student, 'fk_level') and student.fk_level:
                parts.append(str(student.fk_level))
            description = ' - '.join(parts)
        
        return {'id':user_id,'name': name, 'description': description}


# دالة مثال لجلب صورة طالب
def get_student_image(user):
    """دالة مثال لجلب صورة الطالب"""
    if hasattr(user, 'student_sync') and user.student_sync:
        student = user.student_sync
        if hasattr(student, 'image') and student.image:
            return student.image
    return None


# دالة مثال لجلب صورة موظف
def get_employee_image(user):
    """دالة مثال لجلب صورة الموظف"""
    if hasattr(user, 'employee') and user.employee:
        emp = user.employee
        if hasattr(emp, 'image') and emp.image:
            return emp.image
    return None


class ERPHandler:
    """
    معالج بيانات ERP
    يستدعي erp_data_function المحددة في Service model
    لجلب القيم الافتراضية (المنتجات، المشاريع، الرسوم...)
    ويوفر fallback إلى org_config
    """

    @staticmethod
    def get_erp_data(service, user, data=None, org_config=None):
        """
        جلب بيانات ERP حسب إعدادات الخدمة.
        يستدعي erp_data_function إذا وجدت، وإلا يُرجع القيم من org_config.

        Args:
            service: Service instance
            user: request.user
            data: request data dict (اختياري)
            org_config: OrganizationServiceConfig instance (للـ fallback)

        Returns:
            dict بالقيم الافتراضية لحقول ERP
        """
        function_name = getattr(service, 'erp_data_function', None)

        if function_name:
            try:
                from d_services.apis.external_methods import ExternalMethodHandler, FunctionType

                success, result = ExternalMethodHandler.call_function(
                    function_name, user, data,
                    function_type=FunctionType.ERP_DATA,
                )
                if success and isinstance(result, dict):
                    return result
                else:
                    logger.warning(
                        "erp_data_function '%s' failed or returned non-dict, using org_config fallback",
                        function_name,
                    )
            except Exception as e:
                logger.warning("Error calling erp_data_function '%s': %s", function_name, e)

        # Fallback: return values from org_config
        if org_config:
            return ERPHandler._defaults_from_config(org_config)
        return {}

    @staticmethod
    def _defaults_from_config(org_config):
        """Build a dict of ERP defaults from org_config (fallback)."""
        return {
            'service_fee': org_config.fee_amount,
            'fk_currency': org_config.fk_currency_id,
            'is_donor_invoice_allowed': org_config.is_donor_invoice_allowed,
            'is_discount_allowed': org_config.is_discount_allowed,
            'erp_product_id': org_config.erp_product_id,
            'erp_product_name': org_config.erp_product_name,
            'erp_product_for_discount_id': org_config.erp_product_for_discount_id,
            'erp_product_for_discount_name': org_config.erp_product_for_discount_name,
            'erp_product_for_internal_donors_id': org_config.erp_product_for_internal_donors_id,
            'erp_product_for_internal_donors_name': org_config.erp_product_for_internal_donors_name,
            'erp_project_id': org_config.erp_project_id,
            'erp_project_name': org_config.erp_project_name,
            'erp_activity_id': org_config.erp_activity_id,
            'erp_activity_name': org_config.erp_activity_name,
            'erp_cost_center_id': org_config.erp_cost_center_id,
            'erp_cost_center_name': org_config.erp_cost_center_name,
        }

    @staticmethod
    def get_field(erp_data, field, org_fallback=None):
        """Get an ERP field value: erp_data_function result → org_config fallback."""
        val = erp_data.get(field)
        if val is not None:
            return val
        return org_fallback

