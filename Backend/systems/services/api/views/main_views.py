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
# Export View — تصدير قالب لإدارة واحدة
# ============================================================================

class ExportView(BaseViewSet):
    """
    GET  /api/services/export/?directorate_id=X&month=YYYY-MM&mode=multi
    يدعم وضعين: mode=multi (4 أوراق) | mode=single (ورقة واحدة)
    """
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'export_sheet'

    @extend_schema(
        summary='تصدير قالب كشف للإدارات',
        tags=['service-cycle'],
    )
    def list(self, request):
        columns_str = request.query_params.get('columns', '')
        locked_columns_str = request.query_params.get('locked_columns', '')
        statuses_str = request.query_params.get('statuses', '')
        security_admins_id = request.query_params.get('security_admins')
        central_departments_id = request.query_params.get('central_departments')
        branches_id = request.query_params.get('branches')
        district_polices_id = request.query_params.get('district_polices')
        split_by = request.query_params.get('split_by')
        
        # Determine month
        from datetime import datetime
        month = request.query_params.get('month') or datetime.today().strftime('%Y-%m')

        columns = [c for c in columns_str.split(',') if c]
        locked_columns = [c for c in locked_columns_str.split(',') if c]
        
        # Calculate protected and editable
        protected_columns = []
        editable_columns = []
        if columns:
            # We map frontend field names to Excel headers. Note: The frontend sends english field names (e.g. 'military_number')
            # But the export_service expects Arabic headers (e.g. 'الرقم العسكري') for `protected_columns` logic?
            # Let's map them.
            pass

        from systems.personnel.models import PersonnelMaster
        qs = PersonnelMaster.objects.all()

        entity_name = "محافظة/إدارة"
        sec_admin = None
        cen_dept = None
        
        from core.models import SecurityAdministration, CentralDepartment, Branch, DistrictPolice
        
        if central_departments_id:
            try:
                cen_dept = CentralDepartment.objects.get(id=int(central_departments_id))
                qs = qs.filter(central_department=cen_dept)
                entity_name = cen_dept.name
            except CentralDepartment.DoesNotExist:
                pass
        elif branches_id:
            try:
                br = Branch.objects.get(id=int(branches_id))
                qs = qs.filter(branch=br)
                entity_name = br.name
            except Branch.DoesNotExist:
                pass
        elif district_polices_id:
            try:
                dp = DistrictPolice.objects.get(id=int(district_polices_id))
                qs = qs.filter(district_police=dp)
                entity_name = dp.name
            except DistrictPolice.DoesNotExist:
                pass
        elif security_admins_id:
            try:
                sec_admin = SecurityAdministration.objects.get(id=int(security_admins_id))
                qs = qs.filter(central_department__security_admin=sec_admin)
                entity_name = sec_admin.name
            except SecurityAdministration.DoesNotExist:
                pass

        if statuses_str:
            status_ids = [int(s) for s in statuses_str.split(',') if s.isdigit()]
            if status_ids:
                qs = qs.filter(current_status_id__in=status_ids)

        try:
            from systems.services.application.services.export_service import ExcelExportService
            from django.apps import apps
            
            export_mode = request.query_params.get('mode', 'single')
            columns_str = request.query_params.get('columns', '')
            locked_columns_str = request.query_params.get('locked_columns', '')
            
            def get_field_label(field_name):
                mapping = {
                    'qualification': 'المؤهل الدراسي',
                    'current_rank': 'الرتبة',
                    'current_status': 'الحالة',
                    'force_classification': 'تصنيف القوة',
                    'job_title': 'نوع العمل',
                    'notes': 'ملاحظات',
                    'military_number': 'الرقم العسكري',
                    'full_name': 'الاسم الكامل',
                    'national_id': 'الرقم الوطني',
                    'category': 'الفئة',
                    'position': 'المنصب',
                    'phone_number': 'رقم التليفون',
                    'expense_status': 'حالة النفقات',
                }
                if field_name in mapping:
                    return mapping[field_name]
                    
                from django.apps import apps
                PersonnelMaster = apps.get_model('personnel', 'PersonnelMaster')
                try:
                    return str(PersonnelMaster._meta.get_field(field_name).verbose_name)
                except Exception:
                    return field_name
            
            # Parse custom columns requested by frontend
            protected_arabic = None
            editable_arabic = None
            raw_columns = None
            if columns_str:
                selected_cols = [c.strip() for c in columns_str.split(',') if c.strip()]
                locked_cols = [c.strip() for c in locked_columns_str.split(',') if c.strip()] if locked_columns_str else []
                
                if selected_cols:
                    raw_columns = list(selected_cols)
                    
                    # Map correctly
                    protected_arabic = []
                    editable_arabic = []
                    ordered_arabic = []
                    
                    final_raw = []
                    for c in raw_columns:
                        is_locked = c in locked_cols
                        
                        if c == 'security_admin':
                            lbl = 'الوحدة'
                            final_raw.append('__UNIT__')
                        elif c == 'central_department_or_branch':
                            lbl = 'الإدارة_السرية'
                            final_raw.append('__DEPT_BRANCH__')
                        elif c == 'district_police_or_division':
                            lbl = 'القسم_فرع السرية'
                            final_raw.append('__DISTRICT_DIVISION__')
                        elif c == 'pseudo_status_type':
                            lbl = 'الحالة'
                            final_raw.append('__STATUS_TYPE__')
                        elif c == 'current_status':
                            lbl = 'نوع الحالة'
                            final_raw.append(c)
                        elif c == 'pseudo_monthly_var':
                            # Get month dynamically from query param or default to current
                            service_month = request.query_params.get('service_month', '')
                            lbl = f'متغيرات {service_month}' if service_month else 'متغيرات الشهر'
                            final_raw.append('__EMPTY__')
                        elif c == 'pseudo_notes':
                            lbl = 'ملاحظات'
                            final_raw.append('notes')
                        elif c == 'full_name':
                            lbl = 'الأسم'
                            final_raw.append(c)
                        else:
                            lbl = get_field_label(c)
                            final_raw.append(c)
                            
                        ordered_arabic.append(lbl)
                        if is_locked:
                            protected_arabic.append(lbl)
                        else:
                            editable_arabic.append(lbl)

                    raw_columns = final_raw
            
            service = ExcelExportService(
                entity_name=entity_name,
                queryset=qs,
                service_month=month,
                exported_by=request.user,
                mode=export_mode,
                split_by=split_by,
                protected_columns=protected_arabic,
                editable_columns=editable_arabic,
                raw_columns=raw_columns,
                ordered_columns=ordered_arabic if selected_cols else None,
                security_admin=sec_admin,
                central_department=cen_dept,
            )
            file_output, filename = service.export_and_log()
            resp = FileResponse(
                file_output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            # تشفير اسم الملف (RFC 5987)
            encoded = filename.encode('utf-8').decode('latin-1', errors='replace')
            resp['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename.encode('utf-8').hex()}"
            resp['X-Export-Filename'] = filename
            return resp
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# Batch Export View — تصدير كل الإدارات دفعة واحدة (ZIP)
# ============================================================================

class BatchExportView(BaseViewSet):
    """
    POST /api/services/export/batch/
    Body: {"month": "YYYY-MM", "mode": "multi|single"}
    يعيد: ملف ZIP يحتوي على كشف Excel لكل إدارة.
    """
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'export_sheet'

    @extend_schema(
        summary='تصدير كشوفات جميع الإدارات دفعة واحدة (ZIP)',
        tags=['service-cycle'],
        request={'application/json': {'type': 'object', 'properties': {
            'month': {'type': 'string', 'example': '2025-07'},
            'mode':  {'type': 'string', 'enum': ['multi', 'single'], 'default': 'multi'},
        }}},
    )
    def create(self, request):
        month = request.data.get('month') or request.query_params.get('month')
        mode  = request.data.get('mode', 'multi')

        if not month:
            return Response({'success': False, 'error': 'month مطلوب'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from systems.services.export_service import BatchExcelExportService
            svc = BatchExcelExportService(
                exported_by=request.user,
                service_month=month,
                mode=mode,
            )
            zip_buffer, zip_filename, count, errors = svc.export_all()

            resp = FileResponse(zip_buffer, content_type='application/zip')
            resp['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            resp['X-Exported-Count'] = str(count)
            resp['X-Export-Errors']  = str(len(errors))
            return resp
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# Import View — استيراد الكشوف المعدلة مع التحقق الكامل
# ============================================================================

class ImportView(IdempotencyMixin, BaseViewSet):
    """
    POST /api/services/import/
    Form-data: file (Excel), export_id (UUID), month (YYYY-MM)
    سلسلة التحقق: اسم الملف → ExportLog → ماكروز → بنية → عدد → UUID → تلاعب → تغييرات
    """
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    required_permission = 'import_sheet'
    parser_classes = [MultiPartParser, FormParser]
    idempotent_actions = ['create']

    @extend_schema(
        summary='رفع كشوف معدلة للمراجعة',
        tags=['service-cycle'],
        request={'multipart/form-data': {'type': 'object', 'properties': {
            'file':      {'type': 'string', 'format': 'binary'},
            'export_id': {'type': 'string', 'description': 'UUID سجل التصدير'},
            'month':     {'type': 'string', 'description': 'YYYY-MM'},
        }}},
    )
    def create(self, request):
        file      = request.FILES.get('file')
        export_id = request.data.get('export_id', '').strip()
        month     = request.data.get('month', '').strip()

        if not file:
            return Response({'success': False, 'error': 'الملف مطلوب'}, status=status.HTTP_400_BAD_REQUEST)
        if not export_id:
            return Response({'success': False, 'error': 'export_id مطلوب'}, status=status.HTTP_400_BAD_REQUEST)

        from systems.services.application.services.import_service import (
            ExcelImportService, ImportValidationError
        )

        try:
            file_content = file.read()

            # ملفات كبيرة (> 2MB) → Celery
            if len(file_content) > 2 * 1024 * 1024:
                import os
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_imports')
                os.makedirs(temp_dir, exist_ok=True)
                temp_path = os.path.join(temp_dir, f'{export_id}_{file.name}')
                with open(temp_path, 'wb') as fp:
                    fp.write(file_content)
                try:
                    from systems.services.tasks import import_file_task
                    task = import_file_task.delay(
                        temp_path, request.user.id, export_id, month, file.name
                    )
                    return Response({
                        'success': True, 'async': True,
                        'task_id': task.id,
                        'message': 'الملف كبير — يتم المعالجة في الخلفية.',
                    }, status=status.HTTP_202_ACCEPTED)
                except Exception:
                    pass  # إذا فشل Celery نكمل متزامناً

            svc = ExcelImportService(
                file_content=file_content,
                export_id=export_id,
                imported_by=request.user,
                original_filename=file.name,
                service_month=month,
            )
            result = svc.process()
            http_status = status.HTTP_200_OK if not result['errors'] else status.HTTP_207_MULTI_STATUS
            return Response({'success': True, 'data': result}, status=http_status)

        except ImportValidationError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ── API لخريطة الحالات المتتالية (للفرونت اند) ──
class StatusCascadeView(BaseViewSet):
    """
    GET /api/services/status-cascade/
    يعيد: {"قوة عاملة فعلية": ["تعمل في الميدان", ...], ...}
    للفرونت اند لبناء القوائم الشرطية في شاشة المراجعة.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        from systems.services.export_service import get_status_cascade, get_required_attachments
        cascade = get_status_cascade()
        # إضافة المرفقات المطلوبة لكل حالة
        attachments = {}
        for statuses in cascade.values():
            for s in statuses:
                atts = get_required_attachments(s)
                if atts:
                    attachments[s] = atts
        return Response({'success': True, 'data': {'cascade': cascade, 'required_attachments': attachments}})


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
