"""
Personnel Views - واجهات API إدارة الأفراد
المرحلة 4 - المهمة 4.2: CRUD + ABAC + History + Shadow Table
"""
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import connection
from django.core.files.storage import FileSystemStorage
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import PersonnelMaster, SuggestedCorrection
from .serializers import (
    PersonnelListSerializer, PersonnelDetailSerializer,
    PersonnelCreateSerializer, PersonnelUpdateSerializer,
    PersonnelHistorySerializer, SuggestedCorrectionSerializer,
    HistoricalMonthlyVariablesSerializer
)
from infra.security.permissions import (
    ABACPermission, has_permission as check_perm,
    has_department_scope, filter_by_department_scope,
    check_permission, check_permission_for_department,
)
from core.base_views import BaseModelViewSet
from infra.security.dual_auth_service import DualAuthorizationService, DualAuthError
from infra.audit.models import AuditLog


@extend_schema_view(
    list=extend_schema(summary='قائمة الأفراد', tags=['personnel']),
    retrieve=extend_schema(summary='تفاصيل فرد', tags=['personnel']),
    create=extend_schema(summary='إضافة فرد جديد', tags=['personnel']),
    update=extend_schema(summary='تعديل بيانات فرد', tags=['personnel']),
    partial_update=extend_schema(summary='تعديل جزئي', tags=['personnel']),
    destroy=extend_schema(summary='حذف فرد (يتطلب تفويض مزدوج)', tags=['personnel']),
)
class PersonnelViewSet(BaseModelViewSet):
    """
    إدارة الأفراد الكاملة مع ABAC scope filtering
    
    - GET /personnel/ — قائمة (مع بحث وفلترة + ABAC)
    - GET /personnel/{military_number}/ — تفاصيل
    - POST /personnel/ — إضافة (idempotent)
    - PUT /personnel/{military_number}/ — تعديل (idempotent)
    - DELETE /personnel/{military_number}/ — حذف (Four-Eyes)
    - GET /personnel/{military_number}/history/ — تاريخ Shadow Table
    """
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    lookup_field = 'military_number'
    idempotent_actions = ['create', 'update', 'partial_update']
    
    # صلاحيات حسب الإجراء
    required_permission = {
        'list': ['personnel.view.all', 'personnel.view.security_admin', 'personnel.view.own'],
        'retrieve': ['personnel.view.all', 'personnel.view.security_admin', 'personnel.view.own'],
        'create': ['personnel.create.all', 'personnel.create.security_admin'],
        'update': ['personnel.edit.all', 'personnel.edit.security_admin'],
        'partial_update': ['personnel.edit.all', 'personnel.edit.security_admin'],
        'destroy': ['personnel.delete.all', 'personnel.delete.security_admin'],
        'history': ['personnel.view.all', 'personnel.view.security_admin'],
    }
    
    filterset_fields = [
        'security_admin', 'central_department', 'branch', 'district_police',
        'current_rank', 'current_status',
        'is_complete', 'is_data_clean',
    ]
    search_fields = ['full_name', 'military_number', 'old_military_number', 'national_id']
    ordering_fields = [
        'military_number', 'full_name', 'join_date',
        'data_quality_score', 'updated_at',
    ]
    ordering = ['military_number']
    
    def get_queryset(self):
        qs = PersonnelMaster.objects.select_related(
            'current_rank', 'central_department', 'current_status',
            'qualification',
        ).all()

        # ABAC: تصفية حسب نطاق المستخدم (استخدام .* للبحث عن أعلى صلاحية يمتلكها)
        from infra.authorization.services.permission_service import PermissionService
        qs = PermissionService.get_scoped_queryset(
            self.request.user, qs, 'personnel.view.*'
        )
        print(f"[DEBUG] After scoped queryset: {qs.count()}")
        
        # فلتر حالة الرقم الوطني (missing/valid/invalid_format/invalid_length)
        nid_status = self.request.query_params.get('national_id_status')
        if nid_status == 'missing':
            from django.db.models import Q
            qs = qs.filter(Q(national_id__isnull=True) | Q(national_id=''))
        elif nid_status == 'valid':
            qs = qs.filter(national_id__regex=r'^\d{11}$')
        elif nid_status == 'invalid':
            qs = qs.exclude(national_id__isnull=True).exclude(national_id='').exclude(national_id__regex=r'^\d{11}$')
        print(f"[DEBUG] After nid filter: {qs.count()}")
        
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PersonnelListSerializer
        elif self.action in ('create',):
            return PersonnelCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return PersonnelUpdateSerializer
        return PersonnelDetailSerializer
    
    def perform_create(self, serializer):
        personnel = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            new_data=serializer.validated_data,
            ip_address=self._get_ip(),
        )
    
    def perform_update(self, serializer):
        print(">>> SERIALIZER TYPE:", type(serializer), "\n>>> FIELDS:", list(serializer.fields.keys()))
        old_data = PersonnelListSerializer(self.get_object()).data
        personnel = serializer.save()
        if 'expense_status' in self.request.data:
            personnel.expense_status = self.request.data['expense_status']
            personnel.save()
        print(">>> DB EXP STATUS AFTER EXPLICIT SAVE:", personnel.expense_status, "\n>>> VALIDATED DATA:", serializer.validated_data)
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data=old_data,
            new_data=serializer.validated_data,
            ip_address=self._get_ip(),
        )
    
    def destroy(self, request, *args, **kwargs):
        """حذف يتطلب تفويض مزدوج"""
        personnel = self.get_object()
        
        try:
            service = DualAuthorizationService(request.user)
            reason = request.data.get('reason', '')
            if not reason:
                return Response(
                    {'success': False, 'error': 'يجب تحديد سبب الحذف'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            req = service.create_request(
                action_type='DELETE_PERSONNEL',
                target_object_type='PersonnelMaster',
                target_object_id=personnel.military_number,
                reason=reason,
            )
            
            return Response({
                'success': True,
                'requires_dual_auth': True,
                'dual_auth_request_id': str(req.pk),
                'message': 'تم إنشاء طلب تفويض مزدوج للحذف. '
                          'بانتظار موافقة مدير آخر.',
            })
        except DualAuthError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary='تاريخ الفرد من جدول الظل',
        tags=['personnel'],
        responses={200: PersonnelHistorySerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def history(self, request, military_number=None):
        """عرض التاريخ الكامل من Shadow Table"""
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT history_id, history_action, history_user,
                       history_timestamp, history_version,
                       military_number, full_name, national_id,
                       central_department_id, current_rank_id,
                       current_status_id
                FROM personnel_master_history
                WHERE military_number = %s
                ORDER BY history_timestamp DESC
                LIMIT 100
                """,
                [military_number]
            )
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        serializer = PersonnelHistorySerializer(rows, many=True)
        return Response({
            'success': True,
            'count': len(rows),
            'data': serializer.data,
        })
    
    @extend_schema(
        summary='المتغيرات الشهرية للفرد',
        tags=['personnel'],
        responses={200: HistoricalMonthlyVariablesSerializer(many=True)},
    )
    @action(detail=True, methods=['get'], url_path='monthly-variables')
    def monthly_variables(self, request, military_number=None):
        """عرض المتغيرات الشهرية للفرد"""
        from .models import HistoricalMonthlyVariables
        from .serializers import HistoricalMonthlyVariablesSerializer
        personnel = self.get_object()
        qs = HistoricalMonthlyVariables.objects.filter(personnel=personnel).order_by('-month')
        serializer = HistoricalMonthlyVariablesSerializer(qs, many=True)
        return Response({
            'success': True,
            'count': qs.count(),
            'data': serializer.data,
        })

    @extend_schema(
        summary='جلب الأفراد مع متغيراتهم لشهر محدد (لشبكة البيانات)',
        parameters=[OpenApiParameter(name='month', description='مثال: 2026-05', type=str)],
        tags=['personnel']
    )
    @action(detail=False, methods=['get'], url_path='active-variables')
    def active_variables(self, request):
        month = request.query_params.get('month')
        if not month:
            return Response({"error": "يجب تحديد الشهر parameter: month"}, status=400)

        from .models import HistoricalMonthlyVariables
        from django.db.models import Prefetch
        from .serializers import PersonnelActiveVariableSerializer
        
        prefetch = Prefetch(
            'monthly_variables',
            queryset=HistoricalMonthlyVariables.objects.filter(month=month),
            to_attr='prefetched_active_variables'
        )
        
        qs = self.get_queryset().select_related('current_rank', 'central_department').prefetch_related(prefetch)
        page = self.paginate_queryset(qs)
        serializer = PersonnelActiveVariableSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        summary='إنشاء طلبات تصحيح جماعية (للتأسيس الأولي)',
        tags=['personnel'],
        request=SuggestedCorrectionSerializer(many=True),
    )
    @action(detail=False, methods=['post'], url_path='bulk-corrections')
    def bulk_corrections(self, request):
        """إنشاء طلبات تصحيح جماعية للأسماء أو غيرها"""
        items = request.data.get('data', [])
        if not items:
            return Response({'error': 'لم يتم إرسال بيانات'}, status=400)
            
        created_count = 0
        from .models import SuggestedCorrection, PersonnelMaster
        
        for item in items:
            military_number = item.get('military_number')
            new_value = item.get('new_value')
            field_name = item.get('field_name', 'full_name')
            correction_type = item.get('correction_type', 'name_correction')
            
            if not military_number or not new_value:
                continue
                
            try:
                personnel = PersonnelMaster.objects.get(military_number=military_number)
                SuggestedCorrection.objects.create(
                    personnel=personnel,
                    field_name=field_name,
                    old_value=personnel.full_name if field_name == 'full_name' else '',
                    new_value=new_value,
                    correction_type=correction_type,
                    status='pending',
                    requested_by=request.user,
                )
                created_count += 1
            except PersonnelMaster.DoesNotExist:
                continue
                
        return Response({
            'success': True,
            'message': f'تم إنشاء {created_count} طلب تصحيح بنجاح، وتم إحالتها للوزارة.',
            'created_count': created_count
        })

    @extend_schema(summary='إضافة أو تعديل متغير شهري من شبكة البيانات (Inline Edit)', tags=['personnel'])
    @action(detail=False, methods=['post', 'patch'], url_path='upsert-variable')
    def upsert_variable(self, request):
        from .serializers import ActiveVariableUpsertSerializer
        from .models import HistoricalMonthlyVariables
        from django.shortcuts import get_object_or_404
        
        serializer = ActiveVariableUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        personnel = get_object_or_404(self.get_queryset(), military_number=data['military_number'])
        
        if not data['value'].strip():
            HistoricalMonthlyVariables.objects.filter(personnel=personnel, month=data['month']).delete()
        else:
            HistoricalMonthlyVariables.objects.update_or_create(
                personnel=personnel,
                month=data['month'],
                defaults={'variable_value': data['value'], 'source': 'manual'}
            )
        
        return Response({"success": True})

    @extend_schema(
        summary='إحصائيات الأفراد',
        tags=['personnel'],
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """إحصائيات سريعة"""
        qs = self.get_queryset()
        from django.db.models import Count, Avg
        
        stats = {
            'total': qs.count(),
            'complete': qs.filter(is_complete=True).count(),
            'incomplete': qs.filter(is_complete=False).count(),
            'clean_data': qs.filter(is_data_clean=True).count(),
            'avg_quality': qs.aggregate(
                avg=Avg('data_quality_score')
            )['avg'],
            'by_status': list(
                qs.values('current_status__name')
                .annotate(count=Count('military_number'))
                .order_by('-count')
            ),
            'by_department': list(
                qs.values('central_department__name')
                .annotate(count=Count('military_number'))
                .order_by('-count')
            ),
        }
        
        return Response({'success': True, 'data': stats})
    
    def _get_ip(self):
        xff = self.request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else self.request.META.get('REMOTE_ADDR')

    @extend_schema(summary='جلب قائمة الحقول وأنواعها من قاعدة البيانات', tags=['personnel'])
    @action(detail=False, methods=['get'], url_path='schema')
    def schema(self, request):
        """
        يقرأ الموديل PersonnelMaster ويعيد جميع الحقول وأنواعها لبرمجة الاستمارات ديناميكياً.
        """
        from django.db import models
        fields_data = []
        
        for field in PersonnelMaster._meta.fields:
            # تخطي الحقول الداخلية
            if field.name in ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']:
                continue
                
            field_type = 'text'
            options = []
            
            if isinstance(field, models.ForeignKey):
                field_type = 'select'
                # يمكن جلب الخيارات إذا لزم الأمر، لكن الأفضل ترك الفرونت إند يتعامل مع lookup_table
            elif isinstance(field, models.DateField):
                field_type = 'date'
            elif isinstance(field, models.BooleanField):
                field_type = 'checkbox'
            elif isinstance(field, models.IntegerField):
                field_type = 'number'
                
            fields_data.append({
                'key': field.name,
                'label': str(field.verbose_name),
                'type': field_type,
                'auto_mapped': True  # ليعرف الفرونت إند أن هذا الحقل مقفول
            })
            
        return Response({'success': True, 'data': fields_data})

class LegacyImportView(APIView):
    """
    مسار مخصص لمدير النظام حصراً لرفع البيانات الخام التاريخية
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary='رفع ملف البيانات الأصلية التأسيسية',
        description='API مخصص لرفع الملف المليء بالفوضى لأول مرة. يتطلب صلاحيات سوبر يوزر ويعمل من خلال Celery Task',
        tags=['admin', 'import']
    )
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'success': False, 'error': 'يجب إرفاق ملف إكسل'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        is_dry_run = request.data.get('dry_run', 'true').lower() == 'true'

        from django.core.files.storage import default_storage
        import os
        from django.conf import settings
        
        # حفظ الملف في مجلد مؤقت
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_imports'))
        if not fs.exists(''):
            os.makedirs(fs.location, exist_ok=True)
            
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        
        # تشغيل Celery Task
        from .tasks import process_legacy_import_task
        task = process_legacy_import_task.delay(file_path=file_path, dry_run=is_dry_run)
        
        return Response({
            'success': True,
            'message': 'تم استلام الملف وجاري المعالجة النظيفة في الخلفية',
            'task_id': task.id,
            'dry_run': is_dry_run
        }, status=status.HTTP_202_ACCEPTED)
# ═══════════════════════════════════════════════════
# Endpoints: إدارة الرقم الوطني
# ═══════════════════════════════════════════════════

class CheckNationalIdView(APIView):
    """
    فحص فوري للرقم الوطني — يُفوّض لـ PersonnelService.check_national_id
    GET /api/v1/personnel/check-national-id/?value=01010409070&exclude=7348799
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        from .services import PersonnelService
        
        value = request.query_params.get('value', '').strip()
        exclude_mil = request.query_params.get('exclude', '')
        
        if not value:
            return Response({'error': 'الرجاء إرسال الرقم الوطني في الباراميتر value'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        result = PersonnelService.check_national_id(value, exclude_mil or None)
        return Response(result)


class UpdateNationalIdView(APIView):
    """
    تحديث الرقم الوطني — يُفوّض لـ PersonnelService.
    - مدير/رئيس خدمات: تحديث مباشر
    - مستخدم عادي: إنشاء طلب تصحيح
    
    POST /api/v1/personnel/<military_number>/update-national-id/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, military_number):
        from .services import PersonnelService
        
        user = request.user
        try:
            personnel = PersonnelMaster.objects.get(military_number=military_number)
        except PersonnelMaster.DoesNotExist:
            return Response({'success': False, 'error': 'الفرد غير موجود'},
                            status=status.HTTP_404_NOT_FOUND)
        
        new_national_id = request.data.get('national_id', '').strip()
        document_ids = request.data.get('document_ids', [])
        
        # دعم الطريقة القديمة
        front_doc_id = request.data.get('front_document_id')
        back_doc_id = request.data.get('back_document_id')
        if front_doc_id and back_doc_id and not document_ids:
            document_ids = [front_doc_id, back_doc_id]
        
        ip_address = (
            request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
            or request.META.get('REMOTE_ADDR')
        )
        
        is_admin = user.is_superuser or (
            hasattr(user, 'role') and user.role and
            user.role.name in ('مدير النظام', 'رئيس الخدمات')
        )
        
        try:
            if is_admin:
                PersonnelService.update_national_id(
                    personnel, new_national_id, document_ids,
                    user=user, ip_address=ip_address,
                )
                return Response({
                    'success': True,
                    'message': 'تم تحديث الرقم الوطني وربط المرفقات بنجاح',
                    'mode': 'direct_save',
                    'updated_by': user.username,
                })
            else:
                correction = PersonnelService.request_national_id_correction(
                    personnel, new_national_id, document_ids,
                    user=user, ip_address=ip_address,
                )
                return Response({
                    'success': True,
                    'message': 'تم إرسال طلب تعديل الرقم الوطني إلى رئيس الخدمات',
                    'mode': 'correction_request',
                    'correction_id': correction.pk,
                    'requested_by': user.username,
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# SuggestedCorrection already imported at top from .models
from django.utils import timezone

class SuggestedCorrectionViewSet(BaseModelViewSet):
    """
    ViewSet لإدارة طلبات التصحيح (SuggestedCorrection).

    ─── للمطور ──────────────────────────────────────────────────
    GET    /corrections/                    → قائمة الطلبات
    POST   /corrections/                    → إنشاء طلب فردي
    GET    /corrections/{id}/               → تفاصيل طلب
    POST   /corrections/{id}/approve/       → موافقة فردية
    POST   /corrections/{id}/reject/        → رفض فردي
    POST   /corrections/approve_batch/      → موافقة جماعية (مع مذكرة الوزارة)
    POST   /corrections/reject_batch/       → رفض جماعي
    POST   /corrections/bulk-create/        → إنشاء طلبات اسم جماعية
    GET    /corrections/needs-correction/   → أفراد يحتاجون تصحيح اسم
    GET    /corrections/export/             → تصدير نموذج 23
    ─────────────────────────────────────────────────────────────
    ABAC Scope:
      - superuser / staff → يرى كل الطلبات
      - مستخدم عادي      → يرى فقط طلبات إدارة الأمن التابعة له
    """
    queryset = SuggestedCorrection.objects.select_related(
        'personnel', 'personnel__current_rank',
        'personnel__central_department',
        'security_admin',
        'requested_by', 'reviewed_by',
        'supporting_document', 'approval_document',
    )
    serializer_class = SuggestedCorrectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        ABAC Scope: المستخدم يرى فقط طلبات نطاق إدارته.
        Superuser / staff يرون كل شيء.
        """
        qs = super().get_queryset()

        # ── تصفية النطاق الأمني ──
        user = self.request.user
        if not (user.is_superuser or user.is_staff):
            # جلب security_admin من ملف المستخدم إن وُجد
            security_admin_id = getattr(
                getattr(user, 'authz_profile', None),
                'security_admin_id', None
            )
            if security_admin_id:
                qs = qs.filter(security_admin_id=security_admin_id)
            else:
                # المستخدم ليس له إدارة أمن → لا يرى شيئاً
                qs = qs.none()

        # ── Query Params حسب API Contract ──
        params = self.request.query_params

        status_param = params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        type_param = params.get('type')
        if type_param:
            qs = qs.filter(correction_type=type_param)

        personnel_param = params.get('personnel')
        if personnel_param:
            qs = qs.filter(personnel__military_number=personnel_param)

        return qs.order_by('-requested_at')

    def create(self, request, *args, **kwargs):
        """
        إنشاء طلب تصحيح فردي — الـ Serializer يتولى كل التحقق والحفظ.
        """
        import logging
        print(f"FRONTEND PAYLOAD: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        correction = serializer.save()
        return Response(
            self.get_serializer(correction).data,
            status=status.HTTP_201_CREATED
        )



    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """قبول طلب التصحيح وتحديث البيانات الرسمية باستخدام الخدمات لضمان التدقيق"""
        correction = self.get_object()
        if correction.status != 'pending':
            return Response({'success': False, 'error': 'الطلب ليس في حالة الانتظار'}, status=status.HTTP_400_BAD_REQUEST)
        
        approval_doc_id = request.data.get('approval_document_id')
        if not approval_doc_id:
            return Response({'success': False, 'error': 'يجب إرفاق مستند الموافقة (مذكرة الوزارة) لاعتماد الطلب'}, status=status.HTTP_400_BAD_REQUEST)
            
        personnel = correction.personnel
        if personnel:
            from systems.personnel.services import PersonnelService
            from systems.services.attachment_service import AttachmentService
            try:
                # جمع مرفقات السياق المرتبطة بالطلب
                linked_docs = AttachmentService.get_by_context(
                    'SuggestedCorrection', correction.pk, status='temp'
                )
                doc_ids = list(linked_docs.values_list('id', flat=True))
                
                if correction.field_name in ['full_name', 'name_correction']:
                    # ── تصحيح الاسم عبر الخدمة المركزية ──
                    PersonnelService.correct_name(
                        personnel,
                        correction.new_value,
                        document=correction.supporting_document,
                        document_ids=doc_ids if doc_ids else None,
                        user=request.user,
                    )
                elif correction.field_name in ['national_id', 'national_id_correction']:
                    PersonnelService.update_personnel(
                        personnel, {'national_id': correction.new_value}, user=request.user
                    )
                    # تثبيت المرفقات
                    if doc_ids:
                        AttachmentService.commit_documents(doc_ids)
                    
                elif correction.field_name in ['military_number', 'military_number_correction']:
                    # تحديث الرقم العسكري: نحتفظ بالقديم كرقم عسكري سابق ثم نحدّث الجديد
                    old_mil = personnel.military_number
                    # تحديث الرقم العسكري بشكل آمن
                    from django.db import transaction as db_transaction
                    with db_transaction.atomic():
                        # حفظ الرقم القديم كرقم سابق إذا لم يكن محفوظاً
                        if not personnel.old_military_number:
                            personnel.old_military_number = old_mil
                            personnel.save(update_fields=['old_military_number'])
                        PersonnelService.update_personnel(
                            personnel, {'military_number': correction.new_value}, user=request.user
                        )
                    if doc_ids:
                        AttachmentService.commit_documents(doc_ids)
                elif correction.field_name in ['rank', 'current_rank_id', 'rank_correction']:
                    from core.models import Rank
                    rank_obj = Rank.objects.get(pk=int(correction.new_value))
                    PersonnelService.update_personnel(
                        personnel, {'current_rank': rank_obj}, user=request.user
                    )
                    if doc_ids:
                        AttachmentService.commit_documents(doc_ids)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f'Correction approval error: {e}', exc_info=True)
                return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        correction.approval_document_id = approval_doc_id
        
        # ربط المرفق بطلب التصحيح وتثبيته
        from systems.services.attachment_service import AttachmentService
        AttachmentService.link_to_context(
            document_ids=[approval_doc_id],
            context_type='SuggestedCorrection',
            context_id=correction.pk,
            related_field='approval_document'
        )
        AttachmentService.commit_documents([approval_doc_id])
            
        correction.status = 'approved'
        correction.reviewed_by = request.user
        correction.reviewed_at = timezone.now()
        correction.save()
        
        return Response({
            'success': True,
            'message': 'تم قبول طلب التصحيح وتحديث السجلات بنجاح',
            'approved_by': request.user.username,
            'requested_by': correction.requested_by.username if correction.requested_by else None,
        })

    @action(detail=True, methods=['post'], url_path='mark_printed')
    def mark_printed(self, request, pk=None):
        """تسجيل طباعة النموذج رقم 23"""
        correction = self.get_object()
        # Use update() to bypass full_clean() which might fail on legacy or incomplete data
        SuggestedCorrection.objects.filter(pk=correction.pk).update(is_printed=True)
        return Response({
            'success': True,
            'message': 'تم تسجيل طباعة النموذج بنجاح',
            'id': correction.id,
            'is_printed': True
        })

    @action(detail=False, methods=['post'], url_path='approve_batch')
    def approve_batch(self, request):
        """
        موافقة جماعية على طلبات التصحيح.
        يتطلب: correction_ids, memo_document_id
        """
        correction_ids = request.data.get('correction_ids', [])
        memo_document_id = request.data.get('memo_document_id')

        if not correction_ids:
            return Response({'success': False, 'error': 'لم يتم تحديد طلبات للموافقة عليها'}, status=status.HTTP_400_BAD_REQUEST)
        if not memo_document_id:
            return Response({'success': False, 'error': 'يجب إرفاق المذكرة الوزارية (memo_document_id)'}, status=status.HTTP_400_BAD_REQUEST)

        from systems.personnel.services import PersonnelService
        try:
            result = PersonnelService.bulk_approve_corrections(
                correction_ids=correction_ids,
                memo_document_ids=[memo_document_id],
                user=request.user
            )
            return Response({'success': True, 'data': result})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='reject_batch')
    def reject_batch(self, request):
        """
        رفض جماعي لطلبات التصحيح.

        --- لمطور الفرونت إند ---
        POST /api/v1/personnel/corrections/reject_batch/
        Content-Type: application/json

        الجسم (Body):
        {
          "correction_ids": [1, 2, 5],   // إلزامي — معرّفات الطلبات
          "reason": "سبب الرفض",        // إلزامي
          "clear_name": false            // اختياري — true = الوزارة أكدت صحة الاسم
        }

        الاستجابة (Response):
        { "success": true, "rejected_count": 3 }
        """
        correction_ids = request.data.get('correction_ids', [])
        reason = request.data.get('reason', '')
        clear_name = bool(request.data.get('clear_name', False))

        if not correction_ids:
            return Response(
                {'success': False, 'error': 'لم يتم تحديد طلبات للرفض'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not reason:
            return Response(
                {'success': False, 'error': 'يجب ذكر سبب الرفض'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from systems.personnel.services import PersonnelService
        try:
            count = PersonnelService.bulk_reject_corrections(
                correction_ids=correction_ids,
                reason=reason,
                user=request.user,
                clear_name=clear_name,
            )
            return Response({'success': True, 'rejected_count': count})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        رفض طلب تصحيح فردي.

        --- لمطور الفرونت إند ---
        POST /api/v1/personnel/corrections/{id}/reject/
        Content-Type: application/json

        الجسم (Body):
        {
          "reason": "سبب الرفض",        // إلزامي
          "clear_name": false            // اختياري — true يُفرّغ corrected_name
                                         //   استخدم true فقط عندما تؤكد الوزارة
                                         //   أن الاسم صحيح ولا حاجة لإعادة تقديم
        }

        الاستجابة (Response):
        { "success": true, "message": "..." }
        """
        correction = self.get_object()
        if correction.status != 'pending':
            return Response(
                {'success': False, 'error': 'الطلب ليس في حالة الانتظار'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reason = request.data.get('reason', '')
        if not reason:
            return Response(
                {'success': False, 'error': 'يجب ذكر سبب الرفض'},
                status=status.HTTP_400_BAD_REQUEST
            )
        clear_name = bool(request.data.get('clear_name', False))

        from systems.personnel.services import PersonnelService
        PersonnelService.bulk_reject_corrections(
            correction_ids=[correction.pk],
            reason=reason,
            user=request.user,
            clear_name=clear_name,
        )
        return Response({'success': True, 'message': 'تم رفض طلب التصحيح'})

    # ═══════════════════════════════════════════════════
    # طلب تصحيح جماعي (Bulk Create)
    # ═══════════════════════════════════════════════════
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """
        إنشاء طلبات تصحيح اسم لمجموعة أفراد دفعة واحدة.
        يُفوّض لـ PersonnelService.submit_name_corrections_batch
        """
        from .services import PersonnelService
        
        corrections_data = request.data.get('corrections', [])
        document_ids = request.data.get('document_ids', [])
        source = request.data.get('source', 'manual')  # 'initial_seed' أو 'manual'
        if not corrections_data:
            return Response(
                {'success': False, 'error': 'لم يتم إرسال أي بيانات تصحيح'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # المرفقات إلزامية فقط للطلبات اليدوية، واختيارية لطلبات التأسيس الأولي
        if not document_ids and source != 'initial_seed':
            return Response(
                {'success': False, 'error': 'يجب إرفاق مستند داعم (document_ids) لتصحيح الأسماء'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = PersonnelService.submit_name_corrections_batch(
            corrections_data, document_ids=document_ids or [], user=request.user,
        )
        
        return Response({
            'success': True,
            'message': f'تم إنشاء {len(result["created"])} طلب تصحيح',
            'created_count': len(result['created']),
            'error_count': len(result['errors']),
            'created': result['created'],
            'errors': result['errors'],
        }, status=status.HTTP_201_CREATED)

    # ═══════════════════════════════════════════════════
    # أفراد يحتاجون تصحيح اسم
    # ═══════════════════════════════════════════════════
    @action(detail=False, methods=['get'], url_path='needs-correction')
    def needs_correction(self, request):
        """
        قائمة الأفراد الذين لديهم طلبات تصحيح اسم معلقة (بانتظار التصحيح).
        يستخدمه رئيس الخدمات لعرض من يحتاج تصحيح.

        مصدر البيانات: SuggestedCorrection (correction_type='name_correction', status='pending')
        لا يوجد corrected_name في قاعدة البيانات بعد الآن.
        """
        qs = SuggestedCorrection.objects.filter(
            correction_type='name_correction',
            status='pending',
            personnel__isnull=False,
        ).select_related(
            'personnel', 'personnel__current_rank', 'personnel__central_department'
        ).values(
            'id',
            'personnel__military_number',
            'personnel__full_name',
            'new_value',
            'requested_at',
            'personnel__current_rank__name',
            'personnel__central_department__name',
        )

        data = [{
            'correction_id': r['id'],
            'military_number': r['personnel__military_number'],
            'current_name': r['personnel__full_name'],
            'corrected_name': r['new_value'],
            'requested_at': r['requested_at'],
            'rank': r['personnel__current_rank__name'],
            'department': r['personnel__central_department__name'],
        } for r in qs]

        return Response({
            'success': True,
            'count': len(data),
            'data': data,
        })

    # ═══════════════════════════════════════════════════
    # تصدير كشف التصحيح — نموذج (23)
    # ═══════════════════════════════════════════════════
    @action(detail=False, methods=['get'], url_path='export')
    def export_corrections(self, request):
        """
        تصدير كشف طلبات التصحيح المعلقة (نموذج 23) بصيغة JSON جاهزة للتحويل إلى Excel/PDF.
        
        Params: ?status=pending&type=name_correction
        """
        qs = self.get_queryset()
        
        # فلاتر
        corr_status = request.query_params.get('status', 'pending')
        corr_type = request.query_params.get('type')
        
        qs = qs.filter(status=corr_status)
        if corr_type:
            qs = qs.filter(correction_type=corr_type)
        
        qs = qs.select_related('personnel', 'personnel__current_rank')
        
        rows = []
        for i, c in enumerate(qs, 1):
            p = c.personnel
            rows.append({
                'seq': i,
                'rank': p.current_rank.name if p and p.current_rank else '',
                'military_number': p.military_number if p else '',
                'correct_name': c.new_value,
                'wrong_name': c.old_value,
                'correction_target': c.field_name,
                'notes': '',
                'correction_id': c.pk,
                'status': c.get_status_display(),
                'requested_by': c.requested_by.username if c.requested_by else '',
                'requested_at': c.requested_at.isoformat() if c.requested_at else '',
            })
        
        return Response({
            'success': True,
            'title': 'كشف بأسماء المطلوب تصحيح أسماؤهم — نموذج رقم (23)',
            'count': len(rows),
            'columns': [
                {'key': 'seq', 'label': 'م'},
                {'key': 'rank', 'label': 'الرتبة'},
                {'key': 'military_number', 'label': 'الرقم العسكري'},
                {'key': 'correct_name', 'label': 'الاسم الصحيح'},
                {'key': 'wrong_name', 'label': 'الاسم الخطأ'},
                {'key': 'correction_target', 'label': 'المطلوب تصحيحه'},
                {'key': 'notes', 'label': 'ملاحظات'},
            ],
            'data': rows,
        })


class RankSettlementView(APIView):
    """
    تسوية الرتب لعدة أفراد دفعة واحدة
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """جلب الأفراد الذين لديهم رتبة جديدة معلقة بانتظار التسوية"""
        from .models import PersonnelMaster
        qs = PersonnelMaster.objects.select_related(
            'current_rank', 'pending_rank', 'central_department'
        ).filter(pending_rank__isnull=False)
        data = [{
            'military_number': p.military_number,
            'full_name': p.full_name,
            'current_rank_name': p.current_rank.name if p.current_rank else 'غير محدد',
            'pending_rank_name': p.pending_rank.name if p.pending_rank else 'غير محدد',
            'department_name': p.central_department.name if p.central_department else 'غير محدد',
        } for p in qs]
        return Response({'success': True, 'data': data})

    def post(self, request):
        """تسوية الرتب للمجموعة المحددة مع تسجيل حركة التعديل في سجلات التدقيق"""
        military_numbers = request.data.get('military_numbers', [])
        if not military_numbers:
            return Response({'success': False, 'error': 'لم يتم تحديد أي أفراد للتسوية'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.db import transaction
        from core.models import AuditLog
        
        with transaction.atomic():
            qs = PersonnelMaster.objects.select_related('pending_rank').filter(
                military_number__in=military_numbers, 
                pending_rank__isnull=False
            )
            
            audit_logs = []
            updated_personnel = []
            count = 0
            
            for p in qs:
                old_data = {
                    'full_name': p.full_name,
                    'national_id': p.national_id,
                    'phone_number': p.phone_number,
                }
                
                new_data = {
                    'current_rank': p.pending_rank.pk if p.pending_rank else None,
                    'pending_rank': None,
                }
                
                p.current_rank = p.pending_rank
                p.pending_rank = None
                updated_personnel.append(p)
                
                audit_logs.append(AuditLog(
                    user=request.user,
                    action='UPDATE',
                    model_name='PersonnelMaster',
                    object_id=p.military_number,
                    old_data=old_data,
                    new_data=new_data,
                ))
                count += 1
                
            if updated_personnel:
                PersonnelMaster.objects.bulk_update(updated_personnel, ['current_rank', 'pending_rank'])
                AuditLog.objects.bulk_create(audit_logs)
                
        return Response({'success': True, 'message': f'تمت تسوية رتب {count} فرد بنجاح وتسجيل الحركات'})


# ═══════════════════════════════════════════════════
# RankSettlement CRUD + Apply/Reject
# ═══════════════════════════════════════════════════

class RankSettlementViewSet(BaseModelViewSet):
    """
    إدارة طلبات تسوية الرتب الرسمية.
    
    - GET    /rank-settlements/                  → قائمة الطلبات
    - POST   /rank-settlements/                  → إنشاء طلب جديد
    - GET    /rank-settlements/{id}/             → تفاصيل طلب
    - POST   /rank-settlements/{id}/apply/       → تطبيق (تغيير الرتبة فعلياً)
    - POST   /rank-settlements/{id}/reject/      → رفض
    """
    from .serializers import RankSettlementSerializer
    
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    serializer_class = RankSettlementSerializer
    
    required_permission = {
        'list': 'view_personnel',
        'retrieve': 'view_personnel',
        'create': 'edit_personnel_basic',
        'apply': 'approve_change',
        'reject': 'approve_change',
    }
    
    filterset_fields = ['status', 'settlement_type']
    search_fields = [
        'personnel__military_number', 'personnel__full_name',
        'decision_number',
    ]
    ordering = ['-created_at']
    
    def get_queryset(self):
        from .models import RankSettlement
        return RankSettlement.objects.select_related(
            'personnel', 'from_rank', 'to_rank',
            'supporting_document', 'requested_by', 'applied_by',
        ).all()
    
    def perform_create(self, serializer):
        """حفظ الطالب + from_rank تلقائياً من الفرد"""
        personnel = serializer.validated_data['personnel']
        settlement = serializer.save(
            requested_by=self.request.user,
            from_rank=personnel.current_rank,
            status='pending',
        )
        
        # ربط المرفق بالطالب والفرد
        if settlement.supporting_document:
            doc = settlement.supporting_document
            doc.context_type = 'RankSettlement'
            doc.context_id = str(settlement.pk)
            doc.personnel = personnel
            doc.save(update_fields=['context_type', 'context_id', 'personnel'])
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """
        تطبيق طلب التسوية — يُفوّض لـ PersonnelService.apply_settlement
        يدعم: ترقية ضمن نفس الصنف، فرد→ضابط، تخفيض (عقوبة)
        """
        from .services import PersonnelService
        
        settlement = self.get_object()
        
        if settlement.status not in ('pending', 'approved'):
            return Response(
                {'success': False, 'error': 'الطلب ليس في حالة قابلة للتطبيق'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # الموافقة أولاً إذا كان pending
        if settlement.status == 'pending':
            settlement.status = 'approved'
            settlement.save(update_fields=['status'])
        
        ip_address = (
            request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
            or request.META.get('REMOTE_ADDR')
        )
        
        try:
            old_rank_name = settlement.from_rank.name
            PersonnelService.apply_settlement(
                settlement, user=request.user, ip_address=ip_address,
            )
            return Response({
                'success': True,
                'message': f'تم تطبيق التسوية: {old_rank_name} → {settlement.to_rank.name}',
                'settlement_type': settlement.settlement_type,
                'applied_by': request.user.username,
            })
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """رفض طلب تسوية"""
        from django.utils import timezone
        
        settlement = self.get_object()
        
        if settlement.status != 'pending':
            return Response(
                {'success': False, 'error': 'الطلب ليس في حالة الانتظار'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reason = request.data.get('reason', 'تم الرفض')
        
        settlement.status = 'rejected'
        settlement.rejection_reason = reason
        settlement.applied_by = request.user
        settlement.applied_at = timezone.now()
        settlement.save(update_fields=['status', 'rejection_reason', 'applied_by', 'applied_at'])
        
        return Response({
            'success': True,
            'message': 'تم رفض طلب التسوية',
        })
