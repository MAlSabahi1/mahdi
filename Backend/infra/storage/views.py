"""
Document Upload Views — رفع المرفقات الآمن
═══════════════════════════════════════════
Endpoint مركزي لرفع أي ملف في النظام.
الأمان مدمج في Document.save() عبر FileValidationService.
"""
from rest_framework import status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from infra.storage.models import Document
from core.models.audit import AuditLog
from systems.personnel.models import PersonnelMaster


# ═══════════════════════════════════════════════════
# Serializer
# ═══════════════════════════════════════════════════

class DocumentUploadSerializer(serializers.ModelSerializer):
    """مسلسل رفع المرفقات"""
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'file', 'file_url', 'original_filename', 'mime_type', 'size', 'file_hash',
            'document_type', 'description',
            'related_field', 'context_type', 'context_id',
            'source_method',
            'personnel', 'status', 'version',
            'uploaded_by', 'created_at',
        ]
        read_only_fields = [
            'id', 'file_hash', 'original_filename', 'mime_type', 'size', 'status', 'version',
            'uploaded_by', 'created_at',
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class DocumentListSerializer(serializers.ModelSerializer):
    """مسلسل عرض المرفقات (خفيف)"""
    file_url = serializers.SerializerMethodField()
    uploaded_by_name = serializers.CharField(
        source='uploaded_by.username', read_only=True, default=None
    )
    document_type_display = serializers.CharField(
        source='get_document_type_display', read_only=True
    )
    
    class Meta:
        model = Document
        fields = [
            'id', 'file_url', 'original_filename', 'mime_type', 'size', 'file_hash',
            'document_type', 'document_type_display',
            'description',
            'related_field', 'context_type', 'context_id',
            'source_method',
            'personnel', 'status', 'version',
            'uploaded_by', 'uploaded_by_name',
            'created_at',
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


# ═══════════════════════════════════════════════════
# Views
# ═══════════════════════════════════════════════════

class DocumentUploadView(APIView):
    """
    رفع مرفق جديد — الأمان مضمّن في Document.save():
    - فحص Magic Bytes + امتداد + حجم
    - إعادة تسمية بـ UUID
    - حساب hash SHA-256
    
    POST /api/v1/services/documents/upload/
    Content-Type: multipart/form-data
    Body: file + document_type + description (اختياري) + personnel (اختياري)
    
    Response: { id, file_url, file_hash, document_type, status }
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'success': False, 'error': 'لم يتم رفع ملف'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        document_type = request.data.get('document_type', 'other')
        description = request.data.get('description', '')
        personnel_id = request.data.get('personnel')
        related_field = request.data.get('related_field')  # مثل: national_id, current_rank
        context_type = request.data.get('context_type')    # مثل: SuggestedCorrection
        context_id = request.data.get('context_id')        # مثل: 42
        source_method = request.data.get('source_method', 'upload')  # upload/scanner/camera
        
        # جلب الفرد إن وُجد
        personnel_obj = None
        if personnel_id:
            try:
                personnel_obj = PersonnelMaster.objects.get(
                    military_number=str(personnel_id).zfill(7)
                )
            except PersonnelMaster.DoesNotExist:
                return Response(
                    {'success': False, 'error': 'الفرد غير موجود'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            # الأمان يحدث تلقائياً في Document.save()
            doc = Document(
                file=file,
                document_type=document_type,
                description=description,
                related_field=related_field,
                context_type=context_type,
                context_id=context_id,
                source_method=source_method,
                personnel=personnel_obj,
                uploaded_by=request.user,
                status=request.data.get('status', 'temp'),
            )
            doc.save()  # ← هنا يحدث: FileValidation + UUID rename + hash
            
            serializer = DocumentUploadSerializer(doc, context={'request': request})
            return Response({
                'success': True,
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PersonnelDocumentsView(APIView):
    """
    عرض مرفقات فرد معين.
    
    GET /api/v1/services/documents/personnel/<military_number>/
    GET /api/v1/services/documents/personnel/<military_number>/?type=national_id_front
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, military_number):
        try:
            personnel = PersonnelMaster.objects.get(military_number=military_number)
        except PersonnelMaster.DoesNotExist:
            return Response(
                {'success': False, 'error': 'الفرد غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        qs = Document.objects.filter(
            personnel=personnel,
            status='committed',
        ).order_by('-created_at')
        
        # فلتر حسب النوع (اختياري)
        doc_type = request.query_params.get('type')
        if doc_type:
            qs = qs.filter(document_type=doc_type)
        
        # فلتر حسب الحقل المرتبط (اختياري)
        field = request.query_params.get('field')
        if field:
            qs = qs.filter(related_field=field)
        
        serializer = DocumentListSerializer(
            qs, many=True, context={'request': request}
        )
        
        return Response({
            'success': True,
            'count': qs.count(),
            'data': serializer.data,
        })


class DocumentReplaceView(APIView):
    """
    استبدال مرفق (بدون حذف — سياسة عدم الحذف).
    المرفق القديم يُؤرشف + المرفق الجديد يُنشأ بنسخة أعلى.
    
    POST /api/v1/services/documents/<id>/replace/
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        try:
            old_doc = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response(
                {'success': False, 'error': 'المرفق غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # التحقق من الملكية
        if old_doc.uploaded_by and old_doc.uploaded_by != request.user:
            if not request.user.is_superuser:
                return Response(
                    {'success': False, 'error': 'لا تملك صلاحية استبدال هذا المرفق'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'success': False, 'error': 'لم يتم رفع الملف البديل'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.db import transaction
        
        with transaction.atomic():
            # أرشفة القديم
            old_doc.status = 'archived'
            old_doc.save(update_fields=['status'])
            
            # إنشاء الجديد بنسخة أعلى — يرث السياق من القديم
            new_doc = Document(
                file=file,
                document_type=old_doc.document_type,
                description=old_doc.description,
                related_field=old_doc.related_field,
                context_type=old_doc.context_type,
                context_id=old_doc.context_id,
                source_method=request.data.get('source_method', old_doc.source_method),
                personnel=old_doc.personnel,
                uploaded_by=request.user,
                version=old_doc.version + 1,
                status='committed',
            )
            new_doc.save()
            
            # تسجيل التدقيق
            AuditLog.objects.create(
                user=request.user,
                action='UPDATE',
                model_name='Document',
                object_id=str(old_doc.pk),
                old_data={
                    'version': old_doc.version,
                    'file_hash': old_doc.file_hash,
                },
                new_data={
                    'new_document_id': new_doc.pk,
                    'version': new_doc.version,
                    'file_hash': new_doc.file_hash,
                },
            )
        
        serializer = DocumentUploadSerializer(new_doc, context={'request': request})
        return Response({
            'success': True,
            'message': 'تم استبدال المرفق بنجاح (المرفق القديم تم أرشفته)',
            'data': serializer.data,
        })


class AttachmentRequirementsView(APIView):
    """
    جلب متطلبات المرفقات لعملية محددة.
    الفرونت اند يستدعي هذا قبل عرض نافذة الرفع.
    
    GET /api/v1/storage/requirements/?action_key=SuggestedCorrection:name_correction
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        from core.services.document_enforcement import DocumentEnforcementService
        from infra.storage.models import Document
        
        action_key = request.query_params.get('action_key')
        service = DocumentEnforcementService()
        
        if not action_key:
            return Response({
                'success': True,
                'data': service.rules
            })
            
        if action_key not in service.rules:
            return Response({
                'success': False,
                'error': 'العملية غير موجودة في قاموس القواعد'
            }, status=404)
            
        rule = service.rules[action_key]
        doc_choices = dict(Document.DOCUMENT_TYPE_CHOICES)
        
        # إضافة الأسماء المترجمة للمتطلبات
        for req in rule.get('required_documents', []):
            req['label'] = str(doc_choices.get(req['type'], req['type']))
            
        return Response({
            'success': True,
            'data': rule
        })


class ValidateAttachmentsView(APIView):
    """
    التحقق من اكتمال المرفقات قبل تنفيذ العملية (تستخدم للتأكد من الفرونت اند قبل الإرسال النهائي).
    
    POST /api/v1/storage/validate/
    Body: {
        "action_key": "SuggestedCorrection:name_correction",
        "context_id": "50",
        "personnel_id": "1234567"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        from core.services.document_enforcement import DocumentEnforcementService
        from django.core.exceptions import ValidationError
        
        action_key = request.data.get('action_key')
        context_id = request.data.get('context_id')
        personnel_id = request.data.get('personnel_id')
        
        if not action_key or not context_id:
            return Response(
                {'success': False, 'error': 'action_key و context_id مطلوبة'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        service = DocumentEnforcementService()
        
        try:
            service.validate_action_documents(action_key, context_id, personnel_id)
            return Response({
                'success': True,
                'valid': True,
                'message': 'جميع المرفقات المطلوبة متوفرة'
            })
        except ValidationError as e:
            return Response({
                'success': True,
                'valid': False,
                'errors': e.message_dict if hasattr(e, 'message_dict') else e.messages
            })
