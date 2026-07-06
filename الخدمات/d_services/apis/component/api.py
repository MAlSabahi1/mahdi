"""
Component API - واجهة برمجة المكونات
API for retrieving service schema and component data
"""
import os
import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from d_services.models.Service import Service
from d_services.utils.validation_handler import ValidationHandler
from d_services.utils.response_handler import ResponseHandler


class ServiceSchemaAPIView(APIView):
    """
    واجهة جلب مخطط الخدمة
    GET /api/d-services/service-schema/{pk}/
    """
    permission_classes = []
    
    # المسار الأساسي لملفات المكونات
    COMPONENT_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    
    def _load_schema_file(self, folder_name, component_name):
        """
        تحميل ملف schema من المجلد المحدد
        يبحث عن ملف JSON بنفس اسم المكون
        """
        if not component_name:
            return None
        
        # البحث عن ملف JSON أولاً
        json_file_path = os.path.join(
            self.COMPONENT_BASE_PATH, 
            folder_name, 
            f'{component_name}.json'
        )
        
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        
        # إذا لم يوجد JSON، حاول قراءة schema.json العام
        default_schema_path = os.path.join(
            self.COMPONENT_BASE_PATH, 
            folder_name, 
            'schema.json'
        )
        
        if os.path.exists(default_schema_path):
            try:
                with open(default_schema_path, 'r', encoding='utf-8') as f:
                    schemas = json.load(f)
                    # إرجاع schema المكون المحدد
                    return schemas.get(component_name)
            except (json.JSONDecodeError, IOError):
                return None
        
        return None
    
    def get(self, request, pk=None):
        """
        جلب مخطط الخدمة للإنشاء
        - التحقق من صلاحية CREATE
        - إرجاع بيانات الإصدار الحالي
        - إرجاع مخططات المكونات
        - إرجاع رقم الطلب التالي وتاريخ الطلب
        """
        from django.utils import timezone
        from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
        from d_services.models.ServiceRequest import ServiceRequest
        
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(_('الخدمة غير موجودة'))
        
        # التحقق من صلاحية المستخدم
        if not ValidationHandler.check_service_permission(request.user, service.id, 'CREATE'):
            return ResponseHandler.forbidden(_('ليس لديك صلاحية إنشاء طلب لهذه الخدمة'))
        
        # Get current version schema
        current_version = service.versions.filter(is_current=True).first()
        
        # جلب مخططات المكونات من الملفات
        base_component_schema = self._load_schema_file('base', service.base_audience_component)
        target_component_schema = self._load_schema_file('target', service.target_audience_component)
        
        # جلب تكوين المنظمة للخدمة
        user_org = getattr(request.user, 'fk_organization', None)
        org_config = None
        next_request_number = None
        
        if user_org:
            org_config = OrganizationServiceConfig.objects.filter(
                fk_service=service,
                fk_organization=user_org
            ).first()
            
            if org_config:
                # توليد رقم الطلب التالي
                prefix = org_config.request_prefix or service.code or 'REQ'
                
                # جلب آخر رقم طلب للمنظمة والخدمة
                last_request = ServiceRequest.objects.filter(
                    fk_service=service,
                    fk_organization=user_org,
                    is_deleted=False
                ).order_by('-id').first()
                
                if last_request and last_request.request_number:
                    # استخراج الرقم من آخر طلب
                    try:
                        last_num = int(''.join(filter(str.isdigit, last_request.request_number)))
                        next_num = last_num + 1
                    except ValueError:
                        next_num = 1
                else:
                    next_num = 1
                
                next_request_number = f"{prefix}-{next_num:06d}"
        
        return ResponseHandler.success(
            message=_('تم جلب مخطط الخدمة بنجاح'),
            data={
                'fk_service': service.id,
                'fk_service__name': service.name_ar,
                'fk_service__code': service.code,
                'input_template_type': service.input_template_type,
                'output_template_type': service.output_template_type,
                # مكون الجمهور المستهدف
                'target_audience_component': service.target_audience_component,
                'target_audience_schema': target_component_schema,
                # المكون الأساسي
                'base_audience_component': service.base_audience_component,
                'base_audience_schema': base_component_schema,
                # بيانات الإصدار
                'version_name': current_version.version_name if current_version else None,
                'version_schema': current_version.fields_schema if current_version else {},
                'component_type': current_version.component_type if current_version else None,
                # بيانات الطلب
                'next_request_number': next_request_number,
                'request_date': timezone.now().today(),
            }
        )




class ComponentFieldsResolver:

    def get_branch_class(self,program):
        student = StudentClass.object.filter(id=program).first()
        return student.fk_class_division_hall_id if student else None

    def get_class_division_hall(self,program):
        student = StudentClass.object.filter(id=program).first()
        return student.fk_class_division_hall_id if student else None

    # def get_student_by_division(self,program):
    #     student = StudentClass.object.get(id=program)
    #     return student.id if student else None

    # def get_branch_class_subject(self,course):
    #     return course

