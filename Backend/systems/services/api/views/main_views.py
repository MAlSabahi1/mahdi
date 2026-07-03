"""
Services Views - واجهات API دورة الكشوفات
المرحلة 4: Export, Import, Staging, Reconciliation, Reports, Rejections, Webhooks
"""
import os
import tempfile
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from django.db import transaction
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from io import BytesIO

from systems.services.models import (
    StagingRecord, ExportLog, DirectorateCompliance,
    MonthlySnapshot, AuditLog, ReconciliationTask,
    RejectionLog, WebhookConfig, ReportTemplate,
)
from systems.services.api.serializers.main_serializers import (
    StagingRecordSerializer, ApproveSerializer,
    RejectSerializer, BulkApproveSerializer,
    ExportRequestSerializer, ExportLogSerializer,
    ImportResponseSerializer, TaskStatusSerializer,
    MonthlySnapshotSerializer, DirectorateComplianceSerializer,
    ReconciliationTaskSerializer, ReconciliationCreateSerializer,
    ReconciliationResolveSerializer,
    RejectionLogSerializer, WebhookConfigSerializer,
    ReportTemplateSerializer, ReportGenerateSerializer,
)
from infra.security.permissions import (
    ABACPermission, IsAdminPermission,
    has_permission as check_perm,
    has_department_scope, filter_by_department_scope,
    check_permission_for_department,
)
from infra.security.idempotency import IdempotencyMixin
from core.base_views import BaseModelViewSet, BaseReadOnlyViewSet, BaseViewSet


# ============================================================================
# Export View (المهمة 4.3.1)
# ============================================================================

class ExportView(BaseViewSet):
    """تصدير كشوفات Excel"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'export_sheet'
    
    @extend_schema(
        parameters=[
            OpenApiParameter('directorate_id', int, required=True),
            OpenApiParameter('month', str, required=True, description='YYYY-MM'),
        ],
        summary='تصدير كشوفة مديرية',
        tags=['service-cycle'],
    )
    def list(self, request):
        """تصدير كشوفة (متزامن)"""
        dept_id = request.query_params.get('directorate_id') or request.query_params.get('directorate_id')
        month = request.query_params.get('month')
        
        if not dept_id or not month:
            return Response(
                {'success': False, 'error': 'directorate_id و month مطلوبان'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check permissions - using has_governorate_scope to isolate by governorate
        # Ideally, we should also check if the directorate is within the user's governorate
        from core.models import CentralDepartment
        try:
            directorate = CentralDepartment.objects.get(id=int(dept_id))
            if getattr(request.user, 'profile', None) and request.user.profile.governorate_id:
                if directorate.governorate_id != request.user.profile.governorate_id:
                    return Response(
                        {'success': False, 'error': 'ليس لديك صلاحية على هذه المديرية في هذه المحافظة'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        except CentralDepartment.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المديرية غير موجودة'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        try:
            from systems.services.export_service import export_template_for_department
            
            file_output, filename = export_template_for_department(
                department_id=int(dept_id),
                service_month=month,
                user=request.user,
            )
            
            response = FileResponse(
                file_output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================================
# Import View (المهمة 4.3.2) — مع دعم Celery غير متزامن
# ============================================================================

class ImportView(IdempotencyMixin, BaseViewSet):
    """استيراد كشوفات Excel (متزامن/غير متزامن)"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'import_sheet'
    parser_classes = [MultiPartParser, FormParser]
    idempotent_actions = ['create']
    
    @extend_schema(
        summary='رفع كشوفة للاستيراد',
        tags=['service-cycle'],
        request={'multipart/form-data': {'type': 'object', 'properties': {
            'file': {'type': 'string', 'format': 'binary'},
        }}},
    )
    def create(self, request):
        """استيراد ملف Excel — غير متزامن إذا كان الملف كبيراً"""
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'success': False, 'error': 'لم يتم رفع ملف'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # ملف كبير (> 500KB) → Celery
            if file.size > 500 * 1024:
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_imports')
                os.makedirs(temp_dir, exist_ok=True)
                temp_path = os.path.join(temp_dir, f'import_{file.name}')
                with open(temp_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                
                from systems.services.tasks import import_file_task
                task = import_file_task.delay(temp_path, request.user.id)
                
                return Response({
                    'success': True,
                    'async': True,
                    'task_id': task.id,
                    'message': 'تم بدء الاستيراد في الخلفية. استخدم task_id لمتابعة الحالة.',
                }, status=status.HTTP_202_ACCEPTED)
            
            # ملف صغير → متزامن
            from systems.services.import_service import ExcelImportService
            service = ExcelImportService()
            result = service.import_file(file=file, user=request.user)
            
            return Response({'success': True, 'data': result})
        
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================================================
# Task Status View (حالة المهام غير المتزامنة)
# ============================================================================

class TaskStatusView(BaseViewSet):
    """استطلاع حالة المهام غير المتزامنة (Celery)"""
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary='حالة مهمة غير متزامنة',
        tags=['service-cycle'],
        responses={200: TaskStatusSerializer},
    )
    def retrieve(self, request, pk=None):
        """عرض حالة مهمة Celery"""
        try:
            from celery.result import AsyncResult
            result = AsyncResult(pk)
            
            data = {
                'task_id': pk,
                'status': result.status,
            }
            
            if result.successful():
                data['result'] = result.result
            elif result.failed():
                data['error'] = str(result.result)
            elif result.status == 'PROGRESS':
                data['progress'] = result.info.get('progress', 0)
            
            return Response({'success': True, 'data': data})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================================================
# Staging ViewSet (المهمة 4.3.3)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة التغييرات المقترحة', tags=['service-cycle']),
    retrieve=extend_schema(summary='تفاصيل تغيير', tags=['service-cycle']),
)
class StagingViewSet(IdempotencyMixin, BaseReadOnlyViewSet):
    """مراجعة واعتماد التغييرات المقترحة"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'review_staging'
    serializer_class = StagingRecordSerializer
    idempotent_actions = ['approve', 'reject', 'bulk_approve']
    
    filterset_fields = ['status', 'upload_batch_id', 'severity']
    search_fields = [
        'personnel__military_number', 'personnel__full_name',
    ]
    ordering = ['-created_at']
    
    def get_queryset(self):
        qs = StagingRecord.objects.select_related(
            'personnel', 'personnel__central_department',
        ).all()
        qs = filter_by_department_scope(
            self.request.user, qs, 'personnel__central_department'
        )
        return qs
    
    @extend_schema(
        request=ApproveSerializer,
        summary='الموافقة على تغيير',
        tags=['service-cycle'],
    )
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        staging = self.get_object()
        
        if staging.status != 'pending':
            return Response(
                {'success': False, 'error': 'التغيير ليس بحالة انتظار'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            from systems.services.staging_review_service import StagingReviewService
            review_service = StagingReviewService(user=request.user)
            result = review_service.approve_record(
                staging_id=staging.pk,
                document=None,  # TODO: handle document_uuid
            )
            return Response({'success': True, 'data': result})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=RejectSerializer,
        summary='رفض تغيير',
        tags=['service-cycle'],
    )
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        staging = self.get_object()
        
        if staging.status != 'pending':
            return Response(
                {'success': False, 'error': 'التغيير ليس بحالة انتظار'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = RejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            from systems.services.staging_review_service import StagingReviewService
            review_service = StagingReviewService(user=request.user)
            result = review_service.reject_record(
                staging_id=staging.pk,
                reason=serializer.validated_data['rejection_reason'],
            )
            
            # إرسال Webhook عند الرفض
            try:
                from systems.services.webhooks import dispatch_webhook
                dispatch_webhook('rejection.created', {
                    'staging_id': staging.pk,
                    'personnel': staging.personnel.military_number,
                    'reason': serializer.validated_data['rejection_reason'],
                }, directorate_id=getattr(staging.personnel, 'directorate_id', None))
            except Exception:
                pass  # Webhook failure should not block rejection
            
            return Response({'success': True, 'data': result})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=BulkApproveSerializer,
        summary='موافقة جماعية',
        tags=['service-cycle'],
    )
    @action(detail=False, methods=['post'], url_path='bulk_approve')
    def bulk_approve(self, request):
        serializer = BulkApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        ids = serializer.validated_data['staging_ids']
        results = {'approved': 0, 'failed': 0, 'errors': []}
        
        from systems.services.staging_review_service import StagingReviewService
        review_service = StagingReviewService(user=request.user)
        
        for sid in ids:
            try:
                review_service.approve_record(
                    staging_id=sid,
                    document=None,
                )
                results['approved'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({'id': sid, 'error': str(e)})
        
        return Response({'success': True, 'data': results})
    
    @extend_schema(
        summary='إحصائيات التغييرات المقترحة',
        tags=['service-cycle'],
    )
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """
        إحصائيات التغييرات المقترحة
        """
        from django.db.models import Count
        
        qs = self.get_queryset()
        
        stats = {
            'total': qs.count(),
            'pending': qs.filter(status='pending').count(),
            'approved': qs.filter(status='approved').count(),
            'rejected': qs.filter(status='rejected').count(),
            'by_severity': {
                'low': qs.filter(severity='low').count(),
                'medium': qs.filter(severity='medium').count(),
                'high': qs.filter(severity='high').count(),
            }
        }
        
        return Response({'success': True, 'data': stats})


# ============================================================================
# Rejections ViewSet (المهمة 4.3.4)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة المرفوضات', tags=['service-cycle']),
    retrieve=extend_schema(summary='تفاصيل رفض', tags=['service-cycle']),
)
class RejectionViewSet(BaseReadOnlyViewSet):
    """عرض المرفوضات"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'review_staging'
    serializer_class = RejectionLogSerializer
    filterset_fields = ['security_admin', 'central_department', 'service_month']
    ordering = ['-rejected_at']
    
    def get_queryset(self):
        qs = RejectionLog.objects.select_related(
            'personnel', 'central_department', 'rejected_by', 'staging_record'
        ).all()
        return filter_by_department_scope(
            self.request.user, qs, 'central_department'
        )
    
    @extend_schema(
        summary='تصدير تقرير المرفوضات',
        tags=['service-cycle'],
        parameters=[
            OpenApiParameter('directorate_id', int),
            OpenApiParameter('month', str),
        ],
    )
    @action(detail=False, methods=['get'])
    def export(self, request):
        """تصدير Excel للمرفوضات"""
        from systems.services.report_service import ReportGenerationService
        service = ReportGenerationService(request.user)
        
        filters = {
            'directorate_id': request.query_params.get('directorate_id'),
            'month': request.query_params.get('month'),
        }
        
        try:
            result = service.generate('rejections_report', filters, 'excel')
            return FileResponse(
                open(result['file_path'], 'rb'),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                filename='rejections_report.xlsx',
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================================
# Reconciliation ViewSet (المهمة 4.4)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة مهام المطابقة', tags=['reconciliation']),
    retrieve=extend_schema(summary='تفاصيل مهمة مطابقة', tags=['reconciliation']),
)
class ReconciliationViewSet(IdempotencyMixin, BaseViewSet):
    """مهام المطابقة"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = {
        'list': 'create_reconciliation',
        'retrieve': 'create_reconciliation',
        'create': 'create_reconciliation',
        'resolve': 'approve_change',
    }
    idempotent_actions = ['create', 'resolve']
    parser_classes = [MultiPartParser, FormParser]
    
    def list(self, request):
        tasks = ReconciliationTask.objects.select_related(
            'created_by'
        ).all()
        serializer = ReconciliationTaskSerializer(tasks, many=True)
        return Response({
            'success': True,
            'count': tasks.count(),
            'data': serializer.data,
        })
    
    def retrieve(self, request, pk=None):
        try:
            task = ReconciliationTask.objects.get(pk=pk)
        except ReconciliationTask.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المهمة غير موجودة'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReconciliationTaskSerializer(task)
        return Response({'success': True, 'data': serializer.data})
    
    @extend_schema(
        summary='إنشاء مهمة مطابقة',
        tags=['reconciliation'],
    )
    def create(self, request):
        serializer = ReconciliationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'success': False, 'error': 'ملف المصدر مطلوب'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from systems.services.reconciliation_service import ReconciliationService
            service = ReconciliationService(request.user)
            task = service.create_task(
                name=serializer.validated_data['name'],
                task_type=serializer.validated_data['task_type'],
                source_file=file,
                key_field=serializer.validated_data.get('key_field', 'military_number'),
            )
            
            # معالجة غير متزامنة
            from systems.services.tasks import process_reconciliation_task
            celery_task = process_reconciliation_task.delay(task.id, request.user.id)
            
            return Response({
                'success': True,
                'data': {
                    'task_id': task.id,
                    'celery_task_id': celery_task.id,
                    'status': 'pending',
                    'message': 'تم إنشاء المهمة. يتم المعالجة في الخلفية.',
                },
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=ReconciliationResolveSerializer,
        summary='تطبيق حلول اختلافات المطابقة',
        tags=['reconciliation'],
    )
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        serializer = ReconciliationResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            from systems.services.reconciliation_service import ReconciliationService
            service = ReconciliationService(request.user)
            
            results = {'applied': 0, 'failed': 0, 'errors': []}
            
            for resolution in serializer.validated_data['resolutions']:
                try:
                    service.apply_change(
                        task_id=int(pk),
                        record_index=resolution.get('record_index', 0),
                        source=resolution.get('source', 'file'),
                    )
                    results['applied'] += 1
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(str(e))
            
            return Response({'success': True, 'data': results})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================================================
# Reports ViewSet (المهمة 4.5)
# ============================================================================

class ReportViewSet(IdempotencyMixin, BaseViewSet):
    """توليد التقارير"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'view_reports'
    idempotent_actions = ['generate']
    
    @extend_schema(
        summary='قائمة قوالب التقارير المتاحة',
        tags=['reports'],
        responses={200: ReportTemplateSerializer(many=True)},
    )
    def list(self, request):
        templates = ReportTemplate.objects.filter(is_active=True)
        serializer = ReportTemplateSerializer(templates, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    @extend_schema(
        request=ReportGenerateSerializer,
        summary='توليد تقرير',
        tags=['reports'],
    )
    @action(detail=False, methods=['post'])
    def generate(self, request):
        serializer = ReportGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        template_slug = serializer.validated_data['template_slug']
        filters = serializer.validated_data.get('filters', {})
        output_format = serializer.validated_data.get('format', 'excel')
        
        try:
            from systems.services.report_service import ReportGenerationService
            service = ReportGenerationService(request.user)
            result = service.generate(template_slug, filters, output_format)
            
            return Response({
                'success': True,
                'data': {
                    'file_url': result.get('file_url', ''),
                    'file_name': result.get('file_name', ''),
                },
            })
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary='تحميل تقرير مُنشأ',
        tags=['reports'],
    )
    @action(detail=False, methods=['get'], url_path='download/(?P<filename>[^/.]+\\.xlsx)')
    def download(self, request, filename=None):
        file_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
        if not os.path.exists(file_path):
            return Response(
                {'success': False, 'error': 'الملف غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return FileResponse(
            open(file_path, 'rb'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            filename=filename,
        )


# ============================================================================
# Webhook Config ViewSet (المدير فقط)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary='قائمة إعدادات Webhook', tags=['webhooks']),
    create=extend_schema(summary='إنشاء إعداد Webhook', tags=['webhooks']),
    update=extend_schema(summary='تعديل إعداد Webhook', tags=['webhooks']),
    destroy=extend_schema(summary='حذف إعداد Webhook', tags=['webhooks']),
)
class WebhookConfigViewSet(BaseModelViewSet):
    """إدارة إعدادات Webhook (للمدير فقط)"""
    permission_classes = [permissions.IsAuthenticated, IsAdminPermission]
    serializer_class = WebhookConfigSerializer
    queryset = WebhookConfig.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Compliance & Snapshots
# ============================================================================

class ComplianceViewSet(BaseReadOnlyViewSet):
    """التزام المديريات"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'view_reports'
    serializer_class = DirectorateComplianceSerializer
    filterset_fields = ['security_admin', 'central_department', 'service_month']
    ordering = ['-service_month', 'central_department__name']

    def get_queryset(self):
        qs = DirectorateCompliance.objects.select_related('central_department').all()
        return filter_by_department_scope(
            self.request.user, qs, 'central_department'
        )


class SnapshotViewSet(BaseReadOnlyViewSet):
    """اللقطات الشهرية"""
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'view_reports'
    serializer_class = MonthlySnapshotSerializer
    filterset_fields = ['service_month', 'locked']
    ordering = ['-service_month']
    
    def get_queryset(self):
        return MonthlySnapshot.objects.all()
    
    @extend_schema(summary='إقفال الشهر', tags=['service-cycle'])
    @action(detail=False, methods=['post'], url_path='close-month')
    def close_month(self, request):
        """إقفال شهر"""
        if not check_perm(request.user, 'close_month'):
            return Response(
                {'success': False, 'error': 'ليس لديك صلاحية إقفال الشهر'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        month = request.data.get('month')
        dept_id = request.data.get('directorate_id')
        
        if not month:
            return Response(
                {'success': False, 'error': 'الشهر مطلوب'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from systems.services.monthly_snapshot_service import MonthlySnapshotService
            service = MonthlySnapshotService(user=request.user)
            # force parameter could be extracted from request data if needed
            force = request.data.get('force', False)
            result = service.close_month(
                service_month=month,
                force=force
            )
            return Response({'success': True, 'data': result})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
