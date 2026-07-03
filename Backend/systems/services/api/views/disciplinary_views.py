"""
Disciplinary Views — وحدة الجزاءات والانضباط
═══════════════════════════════════════════════
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone

from systems.services.infrastructure.models.disciplinary import (
    DisciplinaryAction, AbsenceRecord, DisciplinaryCouncilVerdict,
)
from infra.storage.models import Document
from systems.services.api.serializers.disciplinary_serializers import (
    DisciplinaryActionListSerializer, DisciplinaryActionDetailSerializer,
    DisciplinaryActionCreateSerializer, DisciplinaryActionUpdateStatusSerializer,
    NotifyMinistrySerializer,
    AbsenceRecordListSerializer, AbsenceRecordDetailSerializer,
    AbsenceRecordCreateSerializer, AbsenceCloseSerializer,
    VerdictListSerializer, VerdictDetailSerializer,
    VerdictCreateSerializer, VerdictSendToMinistrySerializer,
)


# ══════════════════════════════════════════════════════════════════════════════
# 1. DisciplinaryActionViewSet
# ══════════════════════════════════════════════════════════════════════════════

class DisciplinaryActionViewSet(viewsets.ModelViewSet):
    """
    CRUD + إجراءات الجزاءات التأديبية.

    GET    /disciplinary/actions/              → قائمة
    POST   /disciplinary/actions/              → تسجيل جزاء جديد
    GET    /disciplinary/actions/{id}/         → تفاصيل
    PATCH  /disciplinary/actions/{id}/         → تعديل
    POST   /disciplinary/actions/{id}/update-status/   → تغيير الحالة
    POST   /disciplinary/actions/{id}/notify-ministry/ → تأكيد الإبلاغ للوزارة
    GET    /disciplinary/actions/choices/      → خيارات الحقول للـ Frontend
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = DisciplinaryAction.objects.select_related(
            'personnel', 'personnel__current_rank',
            'security_admin', 'created_by',
        ).order_by('-issued_date')

        p = self.request.query_params
        if p.get('personnel'):
            qs = qs.filter(personnel__military_number=p['personnel'])
        if p.get('action_type'):
            qs = qs.filter(action_type=p['action_type'])
        if p.get('status'):
            qs = qs.filter(status=p['status'])
        if p.get('security_admin'):
            qs = qs.filter(security_admin_id=p['security_admin'])
        if p.get('from_date'):
            qs = qs.filter(issued_date__gte=p['from_date'])
        if p.get('to_date'):
            qs = qs.filter(issued_date__lte=p['to_date'])
        if p.get('ministry_notified') is not None:
            qs = qs.filter(ministry_notified=p['ministry_notified'] in ('true', '1'))
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return DisciplinaryActionListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return DisciplinaryActionCreateSerializer
        return DisciplinaryActionDetailSerializer

    # ── LIST ──
    def list(self, request):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        data = DisciplinaryActionListSerializer(page or qs, many=True).data
        if page is not None:
            return self.get_paginated_response(data)
        return Response({'success': True, 'count': len(data), 'results': data})

    # ── RETRIEVE ──
    def retrieve(self, request, pk=None):
        obj = self.get_object()
        return Response({'success': True, 'data': DisciplinaryActionDetailSerializer(obj).data})

    # ── CREATE ──
    def create(self, request):
        ser = DisciplinaryActionCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        doc_ids = ser.validated_data.pop('document_ids', [])

        with transaction.atomic():
            action_obj = DisciplinaryAction.objects.create(
                **ser.validated_data,
                created_by=request.user,
            )
            if doc_ids:
                docs = Document.objects.filter(id__in=doc_ids)
                action_obj.attachments.set(docs)

        return Response({
            'success': True,
            'message': f'تم تسجيل {action_obj.get_action_type_display()} بنجاح',
            'data': DisciplinaryActionDetailSerializer(action_obj).data,
        }, status=status.HTTP_201_CREATED)

    # ── UPDATE ──
    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()
        ser = DisciplinaryActionCreateSerializer(obj, data=request.data, partial=partial)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        doc_ids = ser.validated_data.pop('document_ids', None)
        with transaction.atomic():
            obj = ser.save()
            if doc_ids is not None:
                docs = Document.objects.filter(id__in=doc_ids)
                obj.attachments.set(docs)
        return Response({'success': True, 'data': DisciplinaryActionDetailSerializer(obj).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk, partial=True)

    # ── تغيير الحالة ──
    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        obj = self.get_object()
        ser = DisciplinaryActionUpdateStatusSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.status = ser.validated_data['status']
        if ser.validated_data.get('notes'):
            obj.notes = (obj.notes + '\n' + ser.validated_data['notes']).strip()
        obj.save(update_fields=['status', 'notes'])
        return Response({
            'success': True,
            'message': f'تم تعديل الحالة إلى: {obj.get_status_display()}',
            'data': DisciplinaryActionDetailSerializer(obj).data,
        })

    # ── إبلاغ الوزارة ──
    @action(detail=True, methods=['post'], url_path='notify-ministry')
    def notify_ministry(self, request, pk=None):
        obj = self.get_object()
        if obj.ministry_notified:
            return Response({'success': False, 'error': 'تم إبلاغ الإدارة العامة مسبقاً'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser = NotifyMinistrySerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.ministry_notified    = True
        obj.ministry_notified_at = timezone.now()
        obj.ministry_sent_batch  = ser.validated_data.get('ministry_sent_batch', '')
        obj.save(update_fields=['ministry_notified', 'ministry_notified_at', 'ministry_sent_batch'])
        return Response({'success': True, 'message': 'تم تسجيل الإبلاغ للإدارة العامة'})

    # ── خيارات الحقول (للـ Frontend) ──
    @action(detail=False, methods=['get'])
    def choices(self, request):
        return Response({
            'action_types': [{'value': k, 'label': v} for k, v in DisciplinaryAction.ActionType.choices],
            'source_types': [{'value': k, 'label': v} for k, v in DisciplinaryAction.SourceType.choices],
            'statuses':     [{'value': k, 'label': v} for k, v in DisciplinaryAction.Status.choices],
        })


# ══════════════════════════════════════════════════════════════════════════════
# 2. AbsenceRecordViewSet
# ══════════════════════════════════════════════════════════════════════════════

class AbsenceRecordViewSet(viewsets.ModelViewSet):
    """
    CRUD + إجراءات سجلات الغياب.

    GET    /disciplinary/absences/              → قائمة
    POST   /disciplinary/absences/              → تسجيل غياب
    GET    /disciplinary/absences/{id}/         → تفاصيل
    POST   /disciplinary/absences/{id}/close/   → إغلاق (عاد للعمل)
    POST   /disciplinary/absences/{id}/notify-ministry/ → إبلاغ الوزارة
    POST   /disciplinary/absences/{id}/link-action/     → ربط بجزاء
    GET    /disciplinary/absences/choices/      → خيارات الحقول
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = AbsenceRecord.objects.select_related(
            'personnel', 'personnel__current_rank',
            'security_admin', 'linked_action', 'created_by',
        ).order_by('-from_date')

        p = self.request.query_params
        if p.get('personnel'):
            qs = qs.filter(personnel__military_number=p['personnel'])
        if p.get('absence_type'):
            qs = qs.filter(absence_type=p['absence_type'])
        if p.get('status'):
            qs = qs.filter(status=p['status'])
        if p.get('security_admin'):
            qs = qs.filter(security_admin_id=p['security_admin'])
        if p.get('open_only') in ('true', '1'):
            qs = qs.filter(to_date__isnull=True)
        if p.get('ministry_notified') is not None:
            qs = qs.filter(ministry_notified=p['ministry_notified'] in ('true', '1'))
        return qs

    def list(self, request):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        data = AbsenceRecordListSerializer(page or qs, many=True).data
        if page is not None:
            return self.get_paginated_response(data)
        return Response({'success': True, 'count': len(data), 'results': data})

    def retrieve(self, request, pk=None):
        return Response({'success': True, 'data': AbsenceRecordDetailSerializer(self.get_object()).data})

    def create(self, request):
        ser = AbsenceRecordCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        obj = AbsenceRecord.objects.create(**ser.validated_data, created_by=request.user)
        return Response({
            'success': True,
            'message': 'تم تسجيل الغياب بنجاح',
            'data': AbsenceRecordDetailSerializer(obj).data,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()
        ser = AbsenceRecordCreateSerializer(obj, data=request.data, partial=partial)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        obj = ser.save()
        return Response({'success': True, 'data': AbsenceRecordDetailSerializer(obj).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk, partial=True)

    # ── إغلاق الغياب (عاد الفرد) ──
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        obj = self.get_object()
        if obj.status == AbsenceRecord.Status.CLOSED:
            return Response({'success': False, 'error': 'السجل مغلق مسبقاً'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser = AbsenceCloseSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.to_date = ser.validated_data['to_date']
        obj.status  = AbsenceRecord.Status.CLOSED
        if ser.validated_data.get('notes'):
            obj.notes = (obj.notes + '\n' + ser.validated_data['notes']).strip()
        obj.save(update_fields=['to_date', 'status', 'notes'])
        return Response({'success': True, 'message': 'تم إغلاق سجل الغياب — عاد الفرد للعمل'})

    # ── إبلاغ الوزارة ──
    @action(detail=True, methods=['post'], url_path='notify-ministry')
    def notify_ministry(self, request, pk=None):
        obj = self.get_object()
        if obj.ministry_notified:
            return Response({'success': False, 'error': 'تم الإبلاغ مسبقاً'},
                            status=status.HTTP_400_BAD_REQUEST)
        batch = request.data.get('ministry_sent_batch', '')
        obj.ministry_notified    = True
        obj.ministry_notified_at = timezone.now()
        obj.ministry_sent_batch  = batch
        obj.status = AbsenceRecord.Status.NOTIFIED_MINISTRY
        obj.save(update_fields=['ministry_notified', 'ministry_notified_at',
                                'ministry_sent_batch', 'status'])
        return Response({'success': True, 'message': 'تم تسجيل الإبلاغ للإدارة العامة للقوى البشرية'})

    # ── ربط بجزاء ──
    @action(detail=True, methods=['post'], url_path='link-action')
    def link_action(self, request, pk=None):
        obj = self.get_object()
        action_id = request.data.get('action_id')
        if not action_id:
            return Response({'success': False, 'error': 'معرف الجزاء مطلوب'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            disc_action = DisciplinaryAction.objects.get(pk=action_id)
        except DisciplinaryAction.DoesNotExist:
            return Response({'success': False, 'error': 'الجزاء غير موجود'},
                            status=status.HTTP_404_NOT_FOUND)
        obj.linked_action = disc_action
        obj.status = AbsenceRecord.Status.ACTION_TAKEN
        obj.save(update_fields=['linked_action', 'status'])
        return Response({'success': True, 'message': 'تم ربط الغياب بالجزاء المترتب عليه'})

    # ── خيارات ──
    @action(detail=False, methods=['get'])
    def choices(self, request):
        return Response({
            'absence_types': [{'value': k, 'label': v} for k, v in AbsenceRecord.AbsenceType.choices],
            'sources':       [{'value': k, 'label': v} for k, v in AbsenceRecord.Source.choices],
            'statuses':      [{'value': k, 'label': v} for k, v in AbsenceRecord.Status.choices],
        })


# ══════════════════════════════════════════════════════════════════════════════
# 3. DisciplinaryCouncilVerdictViewSet
# ══════════════════════════════════════════════════════════════════════════════

class DisciplinaryCouncilVerdictViewSet(viewsets.ModelViewSet):
    """
    CRUD + إجراءات أحكام المجلس التأديبي.

    GET    /disciplinary/verdicts/              → قائمة
    POST   /disciplinary/verdicts/              → تسجيل حكم
    GET    /disciplinary/verdicts/{id}/         → تفاصيل
    POST   /disciplinary/verdicts/{id}/file/    → إيداع في ملف الفرد
    POST   /disciplinary/verdicts/{id}/send-ministry/ → إرسال للوزارة
    POST   /disciplinary/verdicts/{id}/execute/ → تنفيذ الحكم
    GET    /disciplinary/verdicts/choices/      → خيارات الحقول
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = DisciplinaryCouncilVerdict.objects.select_related(
            'personnel', 'personnel__current_rank',
            'security_admin', 'linked_action', 'created_by',
        ).order_by('-verdict_date')

        p = self.request.query_params
        if p.get('personnel'):
            qs = qs.filter(personnel__military_number=p['personnel'])
        if p.get('verdict_type'):
            qs = qs.filter(verdict_type=p['verdict_type'])
        if p.get('status'):
            qs = qs.filter(status=p['status'])
        if p.get('security_admin'):
            qs = qs.filter(security_admin_id=p['security_admin'])
        if p.get('pending_ministry') in ('true', '1'):
            qs = qs.filter(ministry_sent_at__isnull=True).exclude(
                status=DisciplinaryCouncilVerdict.Status.RECEIVED
            )
        return qs

    def list(self, request):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        data = VerdictListSerializer(page or qs, many=True).data
        if page is not None:
            return self.get_paginated_response(data)
        return Response({'success': True, 'count': len(data), 'results': data})

    def retrieve(self, request, pk=None):
        return Response({'success': True, 'data': VerdictDetailSerializer(self.get_object()).data})

    def create(self, request):
        ser = VerdictCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        doc_ids = ser.validated_data.pop('document_ids', [])
        with transaction.atomic():
            obj = DisciplinaryCouncilVerdict.objects.create(
                **ser.validated_data,
                created_by=request.user,
            )
            if doc_ids:
                docs = Document.objects.filter(id__in=doc_ids)
                obj.attachments.set(docs)
        return Response({
            'success': True,
            'message': f'تم تسجيل حكم رقم {obj.verdict_ref} بنجاح',
            'data': VerdictDetailSerializer(obj).data,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()
        ser = VerdictCreateSerializer(obj, data=request.data, partial=partial)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        doc_ids = ser.validated_data.pop('document_ids', None)
        with transaction.atomic():
            obj = ser.save()
            if doc_ids is not None:
                docs = Document.objects.filter(id__in=doc_ids)
                obj.attachments.set(docs)
        return Response({'success': True, 'data': VerdictDetailSerializer(obj).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk, partial=True)

    # ── إيداع في ملف الفرد ──
    @action(detail=True, methods=['post'])
    def file(self, request, pk=None):
        obj = self.get_object()
        if obj.status != DisciplinaryCouncilVerdict.Status.RECEIVED:
            return Response({'success': False, 'error': 'الحكم ليس في حالة "مستلَم"'},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.status = DisciplinaryCouncilVerdict.Status.FILED
        obj.save(update_fields=['status'])
        return Response({'success': True, 'message': 'تم إيداع الحكم في ملف الفرد'})

    # ── إرسال للوزارة ──
    @action(detail=True, methods=['post'], url_path='send-ministry')
    def send_ministry(self, request, pk=None):
        obj = self.get_object()
        if obj.ministry_sent_at:
            return Response({'success': False, 'error': 'تم الإرسال للإدارة العامة مسبقاً'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser = VerdictSendToMinistrySerializer(data=request.data)
        if not ser.is_valid():
            return Response({'success': False, 'errors': ser.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.ministry_sent_at    = timezone.now()
        obj.ministry_sent_batch = ser.validated_data.get('ministry_sent_batch', '')
        obj.status = DisciplinaryCouncilVerdict.Status.SENT_MINISTRY
        obj.save(update_fields=['ministry_sent_at', 'ministry_sent_batch', 'status'])
        return Response({'success': True, 'message': 'تم إرسال الحكم للإدارة العامة للقوى البشرية'})

    # ── تنفيذ الحكم ──
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        obj = self.get_object()
        if obj.status == DisciplinaryCouncilVerdict.Status.EXECUTED:
            return Response({'success': False, 'error': 'الحكم منفَّذ مسبقاً'},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.status = DisciplinaryCouncilVerdict.Status.EXECUTED
        obj.save(update_fields=['status'])
        return Response({'success': True, 'message': 'تم تسجيل تنفيذ الحكم'})

    # ── خيارات ──
    @action(detail=False, methods=['get'])
    def choices(self, request):
        return Response({
            'verdict_types': [{'value': k, 'label': v} for k, v in DisciplinaryCouncilVerdict.VerdictType.choices],
            'statuses':      [{'value': k, 'label': v} for k, v in DisciplinaryCouncilVerdict.Status.choices],
        })
