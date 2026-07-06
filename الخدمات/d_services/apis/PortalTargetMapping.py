"""
Portal Target Mapping API
واجهة إدارة ربط حقول البوابة مع حقول QAS
"""
import os
import json
import logging

from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from config.imports.viewmodel_core import AllMVS
from d_services.models.PortalTargetMapping import PortalTargetMapping
from d_services.models.Service import Service
from d_services.serializers.PortalTargetMapping import PortalTargetMappingSerializer
from d_services.utils.response_handler import ResponseHandler
from OpenSoftCoreV4.utils.helpers.utils.requires import require_field,require_instance

logger = logging.getLogger(__name__)


class PortalTargetMappingMVS(AllMVS):
    """
    ViewSet for PortalTargetMapping — CRUD + bulk-sync + schema-fields
    """
    queryset = PortalTargetMapping.objects.select_related(
        'fk_service',
    )
    serializer_class = PortalTargetMappingSerializer
    enable_actions = ['all', 'select', 'log', 'log_details', 'retrieve', 'list']

    def list(self, request, *args, **kwargs):
        """
        قائمة ربط حقول البوابة لخدمة محددة
        GET /portal-target-mapping/?fk_service=<id>
        """
        service_id = request.query_params.get('fk_service')
        if not service_id:
            return ResponseHandler.bad_request(_('يجب تحديد معرف الخدمة (fk_service)'))
        
        queryset = self.get_queryset().filter(
            fk_service_id=service_id, is_deleted=False
        ).order_by('field_order')
        
        serializer = self.get_serializer(queryset, many=True)
        return ResponseHandler.success(
            message=_('تم جلب ربط حقول البوابة بنجاح'),
            data=serializer.data
        )

    # def create(self, request, *args, **kwargs):
    #     """إنشاء ربط جديد"""
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return ResponseHandler.created(
    #         message=_('تم إنشاء ربط الحقل بنجاح'),
    #         data=serializer.data
    #     )

    # def update(self, request, pk=None, *args, **kwargs):
    #     """تعديل ربط"""
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return ResponseHandler.success(
    #         message=_('تم تعديل ربط الحقل بنجاح'),
    #         data=serializer.data
    #     )

    # def partial_update(self, request, pk=None, *args, **kwargs):
    #     return self.update(request, pk, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='schema-fields')
    def schema_fields(self, request):
        """
        جلب حقول Target المتاحة من ملف JSON schema للخدمة
        GET /portal-target-mapping/schema-fields/<service_id>/
        يرجع الحقول المتاحة حتى الفرونت يعرضها في dropdown
        """
        data = request.query_params.copy()

        service_id= require_field(data,'service_id')
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(_('الخدمة غير موجودة'))
        
        component_name = service.target_audience_component
        if not component_name:
            return ResponseHandler.bad_request(
                _('الخدمة لا تحتوي على مكون جمهور مستهدف')
            )
        
        # قراءة ملف JSON schema
        component_base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'apis', 'component'
        )
        json_file_path = os.path.join(component_base_path, 'target', f'{component_name}.json')
        
        if not os.path.exists(json_file_path):
            return ResponseHandler.not_found(
                _('ملف Schema غير موجود'),
                hint=f'Expected: {component_name}.json'
            )
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            return ResponseHandler.error(
                _('خطأ في قراءة ملف Schema'),
                details={'error': str(e)}
            )
        
        fields_info = []
        for field in schema.get('fields', []):
            fields_info.append({
                'name': field['name'],
                'type': field.get('type', 'Unknown'),
                'model': field.get('model', ''),
                'is_main': field.get('is_main', False),
                'name_list': field.get('name_list', ''),
            })
        
        # جلب الربط الحالي (إن وجد)
        existing_mappings = PortalTargetMapping.objects.filter(
            fk_service=service, is_deleted=False
        ).values('qas_field_name', 'portal_field_name', 'resolve_by', 'resolve_field', 'id')
        
        existing_map = {m['qas_field_name']: m for m in existing_mappings}
        
        return ResponseHandler.success(
            message=_('حقول Target المتاحة'),
            data={
                'service_id': service.id,
                'service_code': service.code,
                'service_name': service.name_ar,
                'component_name': component_name,
                'label_ar': schema.get('label_ar', ''),
                'label_en': schema.get('label_en', ''),
                'fields': fields_info,
                'existing_mappings': existing_map,
            }
        )

    @action(detail=False, methods=['post'], url_path='bulk-sync')
    def bulk_sync(self, request):
        """
        مزامنة جماعية لربط الحقول
        POST /portal-target-mapping/bulk-sync/
        
        Body:
        {
            "fk_service": <id>,
            "mappings": [
                {
                    "id": null,              // null = جديد
                    "qas_field_name": "fk_college",
                    "qas_model_name": "College",
                    "portal_field_name": "college_ex_id",
                    "resolve_by": "ex_id",
                    "resolve_field": "ex_id",
                    "is_main_target": false,
                    "field_order": 0
                },
                ...
            ]
        }
        """
        service_id = request.data.get('fk_service')
        mappings_data = request.data.get('mappings', [])
        
        if not service_id:
            return ResponseHandler.bad_request(_('يجب تحديد معرف الخدمة'))
        
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(_('الخدمة غير موجودة'))
        
        with transaction.atomic():
            # جلب الموجود حالياً
            existing = {
                m.id: m for m in PortalTargetMapping.objects.filter(
                    fk_service=service, is_deleted=False
                )
            }
            
            sent_ids = set()
            created_count = 0
            updated_count = 0
            
            for mapping_data in mappings_data:
                mapping_id = mapping_data.get('id')
                
                if mapping_id and mapping_id in existing:
                    # تحديث موجود
                    obj = existing[mapping_id]
                    for field in ['qas_field_name', 'qas_model_name', 'portal_field_name',
                                  'resolve_by', 'resolve_field', 'custom_resolver',
                                  'is_main_target', 'field_order']:
                        if field in mapping_data:
                            setattr(obj, field, mapping_data[field])
                    obj.save()
                    sent_ids.add(mapping_id)
                    updated_count += 1
                else:
                    # إنشاء جديد
                    PortalTargetMapping.objects.create(
                        fk_service=service,
                        qas_field_name=mapping_data['qas_field_name'],
                        qas_model_name=mapping_data.get('qas_model_name', ''),
                        portal_field_name=mapping_data['portal_field_name'],
                        resolve_by=mapping_data.get('resolve_by', 'ex_id'),
                        resolve_field=mapping_data.get('resolve_field', 'ex_id'),
                        custom_resolver=mapping_data.get('custom_resolver'),
                        is_main_target=mapping_data.get('is_main_target', False),
                        field_order=mapping_data.get('field_order', 0),
                    )
                    created_count += 1
            
            # حذف ما لم يرسل (soft delete)
            deleted_count = 0
            for existing_id, obj in existing.items():
                if existing_id not in sent_ids:
                    obj.is_deleted = True
                    obj.save(update_fields=['is_deleted'])
                    deleted_count += 1
        
        # جلب النتيجة النهائية
        final_mappings = PortalTargetMapping.objects.filter(
            fk_service=service, is_deleted=False
        ).order_by('field_order')
        serializer = self.get_serializer(final_mappings, many=True)
        
        return ResponseHandler.success(
            message=_('تم مزامنة ربط الحقول بنجاح'),
            data=serializer.data,
            extra={
                'created': created_count,
                'updated': updated_count,
                'deleted': deleted_count,
            }
        )
