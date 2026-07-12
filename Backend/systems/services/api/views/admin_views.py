"""
Admin Views — إدارة الاستمارات والنماذج المخصصة
صلاحية: مدير النظام فقط (is_staff)
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from systems.services.models import CustomFormTemplate, CustomReportTemplate, DocumentFormTemplate
from systems.services.registries import FormRegistry, ReportRegistry


class CustomFormTemplateViewSet(viewsets.ViewSet):
    """
    CRUD لاستمارات مخصصة.
    GET    /api/services/admin/forms/          → قائمة
    POST   /api/services/admin/forms/          → إنشاء
    GET    /api/services/admin/forms/{id}/     → تفاصيل
    PUT    /api/services/admin/forms/{id}/     → تعديل
    DELETE /api/services/admin/forms/{id}/     → حذف
    GET    /api/services/admin/forms/preview/  → معاينة schema
    """
    permission_classes = [IsAdminUser]

    def _serialize(self, obj):
        return {
            'id': obj.id,
            'form_type': obj.form_type,
            'label': obj.label,
            'target_status': obj.target_status,
            'description': obj.description,
            'fields': obj.fields,
            'attachments': obj.attachments,
            'min_documents': obj.min_documents,
            'max_documents': obj.max_documents,
            'is_active': obj.is_active,
            'created_at': obj.created_at,
        }

    def list(self, request):
        qs = CustomFormTemplate.objects.all().order_by('label')
        return Response({
            'success': True,
            'count': qs.count(),
            'results': [self._serialize(o) for o in qs],
        })

    def create(self, request):
        d = request.data
        try:
            obj = CustomFormTemplate.objects.create(
                form_type=d['form_type'],
                label=d['label'],
                target_status=d['target_status'],
                description=d.get('description', ''),
                fields=d.get('fields', []),
                attachments=d.get('attachments', []),
                min_documents=d.get('min_documents', 1),
                max_documents=d.get('max_documents', 10),
                created_by=request.user,
            )
            return Response({
                'success': True, 'data': self._serialize(obj),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = CustomFormTemplate.objects.get(pk=pk)
            return Response({'success': True, 'data': self._serialize(obj)})
        except CustomFormTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    def update(self, request, pk=None):
        try:
            obj = CustomFormTemplate.objects.get(pk=pk)
            d = request.data
            for field in ['label', 'target_status', 'description', 'fields',
                          'attachments', 'min_documents', 'max_documents', 'is_active']:
                if field in d:
                    setattr(obj, field, d[field])
            obj.save()
            return Response({'success': True, 'data': self._serialize(obj)})
        except CustomFormTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    def destroy(self, request, pk=None):
        try:
            CustomFormTemplate.objects.get(pk=pk).delete()
            return Response({'success': True})
        except CustomFormTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    @action(detail=False, methods=['post'])
    def preview(self, request):
        """معاينة schema استمارة قبل حفظها"""
        ft = request.data.get('form_type', '_preview')
        return Response({
            'success': True,
            'schema': FormRegistry.schema(ft) if FormRegistry.exists(ft) else {
                'form_type': ft,
                'label': request.data.get('label', ''),
                'sections': 3,
                'note': 'سيتم إنشاء 3 أقسام تلقائياً (شخصية + ميلاد + حالة)',
            },
        })


class CustomReportTemplateViewSet(viewsets.ViewSet):
    """
    CRUD لنماذج تقارير مخصصة.
    GET    /api/services/admin/reports/          → قائمة
    POST   /api/services/admin/reports/          → إنشاء
    GET    /api/services/admin/reports/{id}/     → تفاصيل
    PUT    /api/services/admin/reports/{id}/     → تعديل
    DELETE /api/services/admin/reports/{id}/     → حذف
    """
    permission_classes = [IsAdminUser]

    def _serialize(self, obj):
        return {
            'id': obj.id,
            'model_number': obj.model_number,
            'title': obj.title,
            'report_type': obj.report_type,
            'category': obj.category,
            'parent_section': obj.parent_section,
            'sub_section': obj.sub_section,
            'columns': obj.columns,
            'base_filter': obj.base_filter,
            'is_active': obj.is_active,
            'created_at': obj.created_at,
        }

    def list(self, request):
        qs = CustomReportTemplate.objects.all().order_by('model_number')
        return Response({
            'success': True,
            'count': qs.count(),
            'results': [self._serialize(o) for o in qs],
        })

    def create(self, request):
        d = request.data
        try:
            obj = CustomReportTemplate(
                title=d['title'],
                report_type=d.get('report_type', 'detail'),
                category=d.get('category', ''),
                parent_section=d.get('parent_section', ''),
                sub_section=d.get('sub_section', ''),
                columns=d.get('columns', []),
                base_filter=d.get('base_filter', {}),
                created_by=request.user,
            )
            if 'model_number' in d:
                obj.model_number = d['model_number']
            obj.save()  # auto-numbers from 26 if not provided
            return Response({
                'success': True, 'data': self._serialize(obj),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = CustomReportTemplate.objects.get(pk=pk)
            return Response({'success': True, 'data': self._serialize(obj)})
        except CustomReportTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    def update(self, request, pk=None):
        try:
            obj = CustomReportTemplate.objects.get(pk=pk)
            d = request.data
            for field in ['title', 'report_type', 'category', 'parent_section',
                          'sub_section', 'columns', 'base_filter', 'is_active']:
                if field in d:
                    setattr(obj, field, d[field])
            obj.save()
            return Response({'success': True, 'data': self._serialize(obj)})
        except CustomReportTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    def destroy(self, request, pk=None):
        try:
            CustomReportTemplate.objects.get(pk=pk).delete()
            return Response({'success': True})
        except CustomReportTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)


class DocumentFormTemplateViewSet(viewsets.ViewSet):
    """
    CRUD للاستمارات الديناميكية.
    GET    /api/v1/services/admin/document-templates/          → قائمة
    POST   /api/v1/services/admin/document-templates/          → إنشاء
    GET    /api/v1/services/admin/document-templates/presets/  → القوالب الجاهزة
    GET    /api/v1/services/admin/document-templates/{id}/     → تفاصيل
    PUT    /api/v1/services/admin/document-templates/{id}/     → تعديل
    DELETE /api/v1/services/admin/document-templates/{id}/     → حذف
    """
    permission_classes = [IsAdminUser]

    def _serialize(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'slug': obj.slug,
            'category': obj.category,
            'is_preset': obj.is_preset,
            'is_active': obj.is_active,
            'header_columns': obj.header_columns,
            'header_blocks': obj.header_blocks,
            'body_content': obj.body_content,
            'footer_columns': obj.footer_columns,
            'footer_blocks': obj.footer_blocks,
            'page_size': obj.page_size,
            'orientation': obj.orientation,
            'created_at': obj.created_at,
        }

    def list(self, request):
        qs = DocumentFormTemplate.objects.all().order_by('-id')
        return Response({
            'success': True,
            'count': qs.count(),
            'results': [self._serialize(o) for o in qs],
        })

    @action(detail=False, methods=['get'])
    def presets(self, request):
        qs = DocumentFormTemplate.objects.filter(is_preset=True).order_by('name')
        return Response({
            'success': True,
            'count': qs.count(),
            'results': [self._serialize(o) for o in qs],
        })

    def create(self, request):
        d = request.data
        try:
            obj = DocumentFormTemplate.objects.create(
                name=d['name'],
                slug=d['slug'],
                category=d.get('category', 'رسمية'),
                is_preset=d.get('is_preset', False),
                is_active=d.get('is_active', True),
                header_columns=d.get('header_columns', 3),
                header_blocks=d.get('header_blocks', []),
                body_content=d.get('body_content', ''),
                footer_columns=d.get('footer_columns', 1),
                footer_blocks=d.get('footer_blocks', []),
                page_size=d.get('page_size', 'A4'),
                orientation=d.get('orientation', 'portrait'),
                created_by=request.user,
            )
            return Response({
                'success': True, 'data': self._serialize(obj),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)

    def retrieve(self, request, pk=None):
        try:
            obj = DocumentFormTemplate.objects.get(pk=pk)
            return Response({'success': True, 'data': self._serialize(obj)})
        except DocumentFormTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    def update(self, request, pk=None):
        try:
            obj = DocumentFormTemplate.objects.get(pk=pk)
            d = request.data
            for field in ['name', 'slug', 'category', 'is_preset', 'is_active',
                          'header_columns', 'header_blocks', 'body_content',
                          'footer_columns', 'footer_blocks', 'page_size', 'orientation']:
                if field in d:
                    setattr(obj, field, d[field])
            obj.save()
            return Response({'success': True, 'data': self._serialize(obj)})
        except DocumentFormTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)

    def destroy(self, request, pk=None):
        try:
            DocumentFormTemplate.objects.get(pk=pk).delete()
            return Response({'success': True})
        except DocumentFormTemplate.DoesNotExist:
            return Response({'success': False, 'error': 'غير موجود'}, status=404)
