from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404

from systems.services.models import (
    StatusChangeForm, 
    FormNote, 
    FormEventLog, 
    FormReturnLog, 
    FormChecklist
)
from systems.services.api.serializers.service_catalog_serializers import (
    FormNoteSerializer,
    FormEventLogSerializer,
    FormReturnLogSerializer,
    FormChecklistSerializer
)


class FormActionsViewSet(viewsets.ViewSet):
    """
    مجموعة مسارات لإجراءات الطلب: Timeline, Notes, Return, Checklist
    """
    permission_classes = [IsAuthenticated]

    @decorators.action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """جلب Timeline الطلب"""
        form = get_object_or_404(StatusChangeForm, pk=pk)
        logs = FormEventLog.objects.filter(form=form).order_by('-created_at')
        serializer = FormEventLogSerializer(logs, many=True)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['get', 'post'])
    def notes(self, request, pk=None):
        """جلب أو إضافة ملاحظات للطلب"""
        form = get_object_or_404(StatusChangeForm, pk=pk)
        
        if request.method == 'GET':
            notes = FormNote.objects.filter(form=form).order_by('created_at')
            serializer = FormNoteSerializer(notes, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            content = request.data.get('content')
            if not content:
                return Response({'error': 'محتوى الملاحظة مطلوب'}, status=status.HTTP_400_BAD_REQUEST)
                
            note = FormNote.objects.create(
                form=form,
                content=content,
                created_by=request.user
            )
            
            # تسجيل حدث
            FormEventLog.objects.create(
                form=form,
                action='note_added',
                performed_by=request.user,
                notes=f'تمت إضافة ملاحظة: {content[:50]}...'
            )
            
            serializer = FormNoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['post'])
    def return_form(self, request, pk=None):
        """إرجاع الطلب لمرحلة سابقة"""
        form = get_object_or_404(StatusChangeForm, pk=pk)
        
        reason = request.data.get('reason')
        details = request.data.get('details', '')
        to_status = request.data.get('to_status', 'pending_services')
        
        if not reason:
            return Response({'error': 'سبب الإرجاع مطلوب'}, status=status.HTTP_400_BAD_REQUEST)
            
        from_status = form.status
        form.status = 'returned'
        form.save()
        
        # إنشاء سجل الإرجاع
        return_log = FormReturnLog.objects.create(
            form=form,
            return_reason=reason,
            return_details=details,
            from_status=from_status,
            to_status=to_status,
            returned_by=request.user
        )
        
        # إنشاء حدث Timeline
        FormEventLog.objects.create(
            form=form,
            action='returned',
            from_status=from_status,
            to_status='returned',
            performed_by=request.user,
            notes=f'سبب الإرجاع: {return_log.get_return_reason_display()} - {details}'
        )
        
        return Response({'message': 'تم إرجاع الطلب بنجاح'})

    @decorators.action(detail=True, methods=['post'])
    def update_attachments(self, request, pk=None):
        """إضافة مرفقات جديدة أو استبدال المرفقات — مع إعادة حساب attachments_complete"""
        form = get_object_or_404(StatusChangeForm, pk=pk)

        if form.status in ['approved', 'rejected']:
            return Response({'error': 'لا يمكن تعديل المرفقات لطلب معتمد أو مرفوض'}, status=status.HTTP_400_BAD_REQUEST)

        doc_ids = request.data.get('document_ids', [])
        action_type = request.data.get('action', 'add')  # 'add' أو 'replace'

        from infra.storage.models import Document
        docs = Document.objects.filter(id__in=doc_ids)

        if action_type == 'replace':
            form.attachments.set(docs)
        else:
            form.attachments.add(*docs)

        # ── ربط المرفقات بالفرد ──
        for doc in docs:
            if not doc.personnel_id:
                doc.personnel = form.personnel
                doc.context_type = 'StatusChangeForm'
                doc.context_id = str(form.id)
                doc.save(update_fields=['personnel_id', 'context_type', 'context_id'])

        # ── إعادة حساب attachments_complete ──
        total_attachments = form.attachments.count()
        min_docs = len(form.required_attachments) if form.required_attachments else 0
        form.attachments_complete = total_attachments >= max(min_docs, 1)
        form.save(update_fields=['attachments_complete'])

        # ── تسجيل الحدث ──
        FormEventLog.objects.create(
            form=form,
            action='updated',
            performed_by=request.user,
            notes=f'تم تحديث المرفقات — العدد الحالي: {total_attachments}'
        )

        return Response({
            'success': True,
            'message': f'تم تحديث المرفقات ({total_attachments} مرفق)',
            'attachments_complete': form.attachments_complete,
            'attachments_count': total_attachments,
        })

    @decorators.action(detail=True, methods=['get'])
    def checklist(self, request, pk=None):
        """جلب Checklist المرحلة الحالية"""
        form = get_object_or_404(StatusChangeForm, pk=pk)
        stage = request.query_params.get('stage', form.status)
        
        items = FormChecklist.objects.filter(form=form, stage=stage).order_by('order')
        serializer = FormChecklistSerializer(items, many=True)
        return Response(serializer.data)


class ChecklistViewSet(viewsets.ViewSet):
    """
    إدارة عناصر Checklist بشكل فردي
    """
    permission_classes = [IsAuthenticated]

    @decorators.action(detail=True, methods=['patch'])
    def toggle(self, request, pk=None):
        """تبديل حالة عنصر التحقق"""
        item = get_object_or_404(FormChecklist, pk=pk)
        
        is_checked = request.data.get('is_checked', True)
        
        item.is_checked = is_checked
        if is_checked:
            item.checked_by = request.user
            item.checked_at = timezone.now()
        else:
            item.checked_by = None
            item.checked_at = None
            
        item.save()
        
        # تسجيل حدث إذا اكتمل العنصر
        if is_checked:
            FormEventLog.objects.create(
                form=item.form,
                action='checklist_checked',
                performed_by=request.user,
                notes=f'تم التحقق من: {item.title}'
            )
            
        serializer = FormChecklistSerializer(item)
        return Response(serializer.data)
