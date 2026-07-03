"""
Initial Seed Views - واجهات الاستيراد التأسيسي الصارم
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from systems.services.application.services.initial_import_service import (
    StrictInitialImportService, StrictImportError
)
from systems.services.api.serializers.initial_seed_serializers import (
    InitialSeedValidateSerializer, InitialSeedCommitSerializer, InitialSeedPreviewSerializer,
    InitialSeedValidateJsonSerializer, InitialSeedCommitJsonSerializer
)
from infra.audit.models import AuditLog


class InitialSeedViewSet(viewsets.ViewSet):
    """
    محرك الاستيراد التأسيسي الصارم
    لا يقبل إلا البيانات المطابقة 100% لقاعدة البيانات
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="معاينة ملف التأسيس",
        description="قراءة أسماء الأعمدة وأول 10 صفوف من الملف لغرض الربط اليدوي في الواجهة.",
        request=InitialSeedPreviewSerializer,
        responses={
            200: OpenApiResponse(description="أسماء الأعمدة وأول 10 صفوف"),
            400: OpenApiResponse(description="خطأ في قراءة الملف")
        },
        tags=['initial-seed']
    )
    @action(detail=False, methods=['post'])
    def preview(self, request):
        serializer = InitialSeedPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data['file']
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            return Response(
                {"success": False, "message": "يجب أن يكون الملف بصيغة Excel"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            service = StrictInitialImportService()
            preview_data = service.extract_preview(uploaded_file.read())
            return Response({"success": True, "data": preview_data})
        except StrictImportError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"حدث خطأ غير متوقع أثناء المعاينة: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="فحص ملف التأسيس",
        description="رفع ملف التأسيس ليقوم النظام بفحصه بصرامة وإرجاع تقرير بالأخطاء لتعديلها.",
        request=InitialSeedValidateSerializer,
        responses={
            200: OpenApiResponse(description="نتيجة الفحص (ناجح أو قائمة بالأخطاء)"),
            400: OpenApiResponse(description="خطأ في الملف")
        },
        tags=['initial-seed']
    )
    @action(detail=False, methods=['post'])
    def validate(self, request):
        serializer = InitialSeedValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data['file']
        mapping = serializer.validated_data.get('mapping')

        import json
        if isinstance(mapping, str):
            try:
                mapping = json.loads(mapping)
            except:
                mapping = None

        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            return Response(
                {"success": False, "message": "يجب أن يكون الملف بصيغة Excel"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            service = StrictInitialImportService()
            # 1. Parse file into list of dicts
            rows_data = service.parse_file_to_dicts(uploaded_file.read(), column_mapping=mapping)
            # 2. Validate data
            report = service.validate_data(rows_data)
            # 3. Attach full parsed data for frontend inline editing
            report['all_rows'] = rows_data
            
            # تسجيل الحدث
            AuditLog.objects.create(
                user=request.user,
                action='VALIDATE_SEED',
                model_name='PersonnelMaster',
                object_id='Bulk',
                old_data={},
                new_data={'report_summary': {'total': report['total_rows'], 'errors': report['error_count']}},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return Response({"success": True, "data": report})
            
        except StrictImportError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"حدث خطأ غير متوقع: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="اعتماد ملف التأسيس",
        description="حفظ البيانات بعد التأكد من خلوها من الأخطاء.",
        request=InitialSeedCommitSerializer,
        responses={
            200: OpenApiResponse(description="نجاح الحفظ وإنشاء السجلات"),
            400: OpenApiResponse(description="يوجد أخطاء في الملف ويجب فحصها")
        },
        tags=['initial-seed']
    )
    @action(detail=False, methods=['post'])
    def commit(self, request):
        serializer = InitialSeedCommitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data['file']
        batch_id = serializer.validated_data.get('batch_id')
        mapping = serializer.validated_data.get('mapping')

        import json
        if isinstance(mapping, str):
            try:
                mapping = json.loads(mapping)
            except:
                mapping = None
        
        file_content = uploaded_file.read()
        service = StrictInitialImportService()
        
        try:
            # يجب إعادة الفحص لضمان أن المستخدم لم يرفع ملفاً خاطئاً للاعتماد مباشرة
            report = service.validate_file(file_content, column_mapping=mapping)
            if not report['is_valid']:
                return Response({
                    "success": False, 
                    "message": "الملف يحتوي على أخطاء. الرجاء استخدام مسار validate أولاً.",
                    "data": report
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # الاعتماد والحفظ
            stats = service.commit_file(file_content, batch_id, column_mapping=mapping)
            
            AuditLog.objects.create(
                user=request.user,
                action='COMMIT_SEED',
                model_name='PersonnelMaster',
                object_id='Bulk',
                old_data={},
                new_data={'stats': stats},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return Response({
                "success": True,
                "message": "تم الاستيراد التأسيسي بنجاح",
                "data": stats
            })
            
        except StrictImportError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"حدث خطأ أثناء الحفظ: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="فحص بيانات التأسيس (JSON)",
        description="فحص البيانات المرسلة كقائمة JSON من شبكة الواجهة وتحديد الأخطاء.",
        request=InitialSeedValidateJsonSerializer,
        responses={
            200: OpenApiResponse(description="نتيجة الفحص (ناجح أو قائمة بالأخطاء)"),
            400: OpenApiResponse(description="خطأ في البيانات")
        },
        tags=['initial-seed']
    )
    @action(detail=False, methods=['post'], url_path='validate-json')
    def validate_json(self, request):
        serializer = InitialSeedValidateJsonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        rows_data = serializer.validated_data['data']
        
        try:
            service = StrictInitialImportService()
            report = service.validate_data(rows_data)
            return Response({"success": True, "data": report})
        except StrictImportError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"حدث خطأ غير متوقع: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="اعتماد بيانات التأسيس (JSON)",
        description="حفظ البيانات بشكل نهائي بعد الفحص بنجاح بدون الحاجة للملف.",
        request=InitialSeedCommitJsonSerializer,
        responses={
            200: OpenApiResponse(description="نجاح الحفظ وإنشاء السجلات"),
            400: OpenApiResponse(description="يوجد أخطاء ويجب إعادة الفحص")
        },
        tags=['initial-seed']
    )
    @action(detail=False, methods=['post'], url_path='commit-json')
    def commit_json(self, request):
        serializer = InitialSeedCommitJsonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        rows_data = serializer.validated_data['data']
        batch_id = serializer.validated_data.get('batch_id')
        
        service = StrictInitialImportService()
        
        try:
            # يجب إعادة الفحص لضمان أن البيانات المرسلة سليمة
            report = service.validate_data(rows_data)
            if not report['is_valid']:
                return Response({
                    "success": False, 
                    "message": "البيانات تحتوي على أخطاء. الرجاء الإصلاح وإعادة المحاولة.",
                    "data": report
                }, status=status.HTTP_400_BAD_REQUEST)
                
            stats = service.commit_data(rows_data, batch_id)
            
            AuditLog.objects.create(
                user=request.user,
                action='COMMIT_SEED',
                model_name='PersonnelMaster',
                object_id='BulkJSON',
                old_data={},
                new_data={'stats': stats},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return Response({
                "success": True,
                "message": "تم الاستيراد التأسيسي بنجاح",
                "data": stats
            })
            
        except StrictImportError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"حدث خطأ أثناء الحفظ: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
