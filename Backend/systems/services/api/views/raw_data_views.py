"""
Raw Data Standardized Views
واجهات API البيانات الخام المعاد تنظيمها
"""
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from systems.personnel.models import PersonnelMaster, SuggestedCorrection, HistoricalMonthlyVariables
from systems.services.models import ServiceEventLog
from infra.audit.models import AuditLog
from systems.services.api.serializers.raw_data_serializers import (
    RawDataStandardizedSerializer,
    HistoricalMonthlyVariableSerializer,
    ApplyCorrectionSerializer,
    RejectCorrectionSerializer,
    BulkApplyCorrectionSerializer,
    BulkRejectCorrectionSerializer,
    DirectUpdatePersonnelSerializer,
    RawDataStatisticsSerializer,
)
from core.pagination import DynamicPageSizePagination
from core.base_views import BaseReadOnlyViewSet


@extend_schema_view(
    list=extend_schema(
        summary='قائمة البيانات الخام المعاد تنظيمها',
        description='عرض جميع بيانات الأفراد بعد التنظيم مع القيم الأصلية والاقتراحات',
        tags=['raw-data'],
        parameters=[
            OpenApiParameter('search', str, description='بحث في الاسم أو الرقم العسكري أو الرقم الوطني'),
            OpenApiParameter('geo_location', int, description='تصفية حسب الموقع الجغرافي'),
            OpenApiParameter('security_admin', int, description='تصفية حسب الإدارة الأمنية'),
            OpenApiParameter('division', int, description='تصفية حسب القسم'),
            OpenApiParameter('unit', int, description='تصفية حسب الوحدة'),
            OpenApiParameter('current_rank', int, description='تصفية حسب الرتبة'),
            OpenApiParameter('current_status', int, description='تصفية حسب الحالة الخدمية'),
            OpenApiParameter('national_id_status', str, description='تصفية حسب حالة الرقم الوطني'),
            OpenApiParameter('has_pending_corrections', bool, description='فقط الذين لديهم اقتراحات معلقة'),
            OpenApiParameter('is_data_clean', bool, description='تصفية حسب نظافة البيانات'),
        ]
    ),
    retrieve=extend_schema(
        summary='تفاصيل فرد',
        description='عرض تفاصيل فرد مع جميع البيانات الأصلية والاقتراحات',
        tags=['raw-data']
    ),
)
class RawDataStandardizedViewSet(BaseReadOnlyViewSet):
    """
    واجهة البيانات الخام المعاد تنظيمها
    - عرض البيانات بعد التنظيم
    - مقارنة القيم الأصلية مع الموحدة
    - إدارة الاقتراحات المعلقة
    """
    serializer_class = RawDataStandardizedSerializer
    pagination_class = DynamicPageSizePagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        جلب البيانات مع العلاقات المطلوبة
        """
        queryset = PersonnelMaster.objects.select_related(
            'current_rank',
            'current_status',
            'pending_rank',
            'geo_location',
            'security_admin',
            'division',
            'unit',
            'qualification',
        ).prefetch_related(
            Prefetch(
                'suggested_corrections',
                queryset=SuggestedCorrection.objects.filter(status='pending')
            ),
            'monthly_variables'
        )
        
        # التصفية
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(military_number__icontains=search) |
                Q(full_name__icontains=search) |
                Q(national_id__icontains=search)
            )
        
        # تصفية حسب الهيكل التنظيمي
        geo_location = self.request.query_params.get('geo_location')
        if geo_location:
            queryset = queryset.filter(geo_location_id=geo_location)
        
        security_admin = self.request.query_params.get('security_admin')
        if security_admin:
            queryset = queryset.filter(security_admin_id=security_admin)
        
        division = self.request.query_params.get('division')
        if division:
            queryset = queryset.filter(division_id=division)
        
        unit = self.request.query_params.get('unit')
        if unit:
            queryset = queryset.filter(unit_id=unit)
        
        # تصفية حسب الرتبة والحالة
        current_rank = self.request.query_params.get('current_rank')
        if current_rank:
            queryset = queryset.filter(current_rank_id=current_rank)
        
        current_status = self.request.query_params.get('current_status')
        if current_status:
            queryset = queryset.filter(current_status_id=current_status)
        
        # تصفية حسب حالة الرقم الوطني (محسوبة عبر DB queries)
        national_id_status = self.request.query_params.get('national_id_status')
        if national_id_status:
            if national_id_status == 'missing':
                queryset = queryset.filter(
                    Q(national_id__isnull=True) | Q(national_id='')
                )
            elif national_id_status == 'invalid_format':
                queryset = queryset.exclude(
                    Q(national_id__isnull=True) | Q(national_id='')
                ).exclude(national_id__regex=r'^\d+$')
            elif national_id_status == 'invalid_length':
                queryset = queryset.filter(
                    national_id__regex=r'^\d+$'
                ).exclude(national_id__regex=r'^\d{11}$')
            elif national_id_status == 'valid':
                queryset = queryset.filter(national_id__regex=r'^\d{11}$')
        
        # تصفية حسب وجود اقتراحات معلقة
        has_pending = self.request.query_params.get('has_pending_corrections')
        if has_pending == 'true':
            queryset = queryset.annotate(
                pending_count=Count('suggested_corrections', filter=Q(suggested_corrections__status='pending'))
            ).filter(pending_count__gt=0)
        
        # تصفية حسب نظافة البيانات
        is_clean = self.request.query_params.get('is_data_clean')
        if is_clean is not None:
            queryset = queryset.filter(is_data_clean=is_clean == 'true')
        
        return queryset.order_by('-updated_at')
    
    @extend_schema(
        summary='المتغيرات الشهرية لفرد',
        description='عرض جميع المتغيرات الشهرية التاريخية لفرد معين',
        tags=['raw-data'],
        responses={200: HistoricalMonthlyVariableSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def monthly_variables(self, request, pk=None):
        """عرض المتغيرات الشهرية"""
        personnel = self.get_object()
        variables = personnel.monthly_variables.all().order_by('-month')
        serializer = HistoricalMonthlyVariableSerializer(variables, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @extend_schema(
        summary='تعديل مباشر لبيانات الفرد',
        description='تعديل البيانات الأساسية للفرد مباشرة من مساحة عمل التحقق',
        tags=['raw-data'],
        request=DirectUpdatePersonnelSerializer,
    )
    @action(detail=True, methods=['patch'])
    def direct_update(self, request, pk=None):
        """تعديل مباشر للبيانات"""
        personnel = self.get_object()
        serializer = DirectUpdatePersonnelSerializer(personnel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # حفظ القيم القديمة للتدقيق
        old_data = {}
        for field in serializer.validated_data.keys():
            old_data[field] = getattr(personnel, field, None)
            
        serializer.save()
        
        # سجل تدقيق للتعديل المباشر
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=str(personnel.id),
            old_data=old_data,
            new_data=serializer.validated_data,
            ip_address=request.META.get('REMOTE_ADDR'),
            timestamp=timezone.now()
        )
        
        # إعادة البيانات المحدثة
        updated_serializer = self.get_serializer(personnel)
        return Response({
            'success': True,
            'message': 'تم تحديث البيانات بنجاح',
            'data': updated_serializer.data
        })
        
    @extend_schema(
        summary='إحصائيات المعالجة',
        description='جلب إحصائيات حية عن حالة البيانات وصحتها',
        tags=['raw-data'],
        responses={200: RawDataStatisticsSerializer}
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """إحصائيات المعالجة الحية"""
        qs = PersonnelMaster.objects.all()
        total_records = qs.count()
        clean_records = qs.filter(is_data_clean=True).count()
        
        # الأخطاء: إما لديه اقتراحات معلقة، أو بيانات غير نظيفة
        error_records = qs.filter(
            Q(is_data_clean=False) |
            Q(suggested_corrections__status='pending')
        ).distinct().count()
        
        # التحذيرات (مثلاً بدون رقم هاتف لكن لا يمنع الاعتماد)
        warning_records = qs.filter(
            is_data_clean=True,
            phone_number__isnull=True
        ).count()
        
        clean_percentage = (clean_records / total_records * 100) if total_records > 0 else 0
        
        stats = {
            'total_records': total_records,
            'clean_records': clean_records,
            'clean_percentage': round(clean_percentage, 1),
            'error_records': error_records,
            'warning_records': warning_records
        }
        
        serializer = RawDataStatisticsSerializer(stats)
        return Response({
            'success': True,
            'data': serializer.data
        })

    
    @extend_schema(
        summary='تطبيق تصحيح',
        description='تطبيق اقتراح تصحيح معلق على بيانات الفرد',
        tags=['raw-data'],
        request=ApplyCorrectionSerializer,
    )
    @action(detail=True, methods=['post'])
    def apply_correction(self, request, pk=None):
        """تطبيق تصحيح واحد"""
        personnel = self.get_object()
        serializer = ApplyCorrectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        correction_id = serializer.validated_data['correction_id']
        notes = serializer.validated_data.get('notes', '')
        
        try:
            correction = SuggestedCorrection.objects.get(
                id=correction_id,
                personnel=personnel,
                status='pending'
            )
        except SuggestedCorrection.DoesNotExist:
            return Response({
                'success': False,
                'message': 'الاقتراح غير موجود أو تم معالجته مسبقاً'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # تطبيق التصحيح حسب النوع
        old_value = getattr(personnel, correction.field_name, None)
        
        try:
            # تحديث الحقل
            setattr(personnel, correction.field_name, correction.new_value)
            personnel.save()
            
            # تحديث حالة الاقتراح
            correction.status = 'approved'
            correction.reviewed_by = request.user
            correction.reviewed_at = timezone.now()
            correction.save()
            
            # إنشاء سجل حدث
            ServiceEventLog.objects.create(
                personnel=personnel,
                security_admin=personnel.security_admin,
                event_date=timezone.now().date(),
                service_month=timezone.now().strftime('%Y-%m'),
                field_name=correction.field_name,
                old_value=str(old_value) if old_value else '',
                new_value=correction.new_value,
                order_document=correction.supporting_document,
                created_by=request.user
            )
            
            # سجل تدقيق
            AuditLog.objects.create(
                user=request.user,
                action='APPROVE',
                model_name='SuggestedCorrection',
                object_id=str(correction.id),
                old_data={'status': 'pending'},
                new_data={'status': 'approved', 'field': correction.field_name},
                ip_address=request.META.get('REMOTE_ADDR'),
                timestamp=timezone.now()
            )
            
            return Response({
                'success': True,
                'message': 'تم تطبيق التصحيح بنجاح'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'فشل تطبيق التصحيح: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary='رفض تصحيح',
        description='رفض اقتراح تصحيح معلق',
        tags=['raw-data'],
        request=RejectCorrectionSerializer,
    )
    @action(detail=True, methods=['post'])
    def reject_correction(self, request, pk=None):
        """رفض تصحيح واحد"""
        personnel = self.get_object()
        serializer = RejectCorrectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        correction_id = serializer.validated_data['correction_id']
        rejection_reason = serializer.validated_data['rejection_reason']
        
        try:
            correction = SuggestedCorrection.objects.get(
                id=correction_id,
                personnel=personnel,
                status='pending'
            )
        except SuggestedCorrection.DoesNotExist:
            return Response({
                'success': False,
                'message': 'الاقتراح غير موجود أو تم معالجته مسبقاً'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # رفض الاقتراح
        correction.status = 'rejected'
        correction.reviewed_by = request.user
        correction.reviewed_at = timezone.now()
        correction.rejection_reason = rejection_reason
        correction.save()
        
        # سجل تدقيق
        AuditLog.objects.create(
            user=request.user,
            action='REJECT',
            model_name='SuggestedCorrection',
            object_id=str(correction.id),
            old_data={'status': 'pending'},
            new_data={'status': 'rejected', 'reason': rejection_reason},
            ip_address=request.META.get('REMOTE_ADDR'),
            timestamp=timezone.now()
        )
        
        return Response({
            'success': True,
            'message': 'تم رفض التصحيح'
        })
    
    @extend_schema(
        summary='تطبيق تصحيحات متعددة',
        description='تطبيق عدة اقتراحات تصحيح دفعة واحدة',
        tags=['raw-data'],
        request=BulkApplyCorrectionSerializer,
    )
    @action(detail=False, methods=['post'])
    def bulk_apply(self, request):
        """تطبيق تصحيحات متعددة"""
        serializer = BulkApplyCorrectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        correction_ids = serializer.validated_data['correction_ids']
        notes = serializer.validated_data.get('notes', '')
        
        corrections = SuggestedCorrection.objects.filter(
            id__in=correction_ids,
            status='pending'
        ).select_related('personnel', 'personnel__security_admin')
        
        success_count = 0
        failed_count = 0
        errors = []
        
        for correction in corrections:
            try:
                personnel = correction.personnel
                old_value = getattr(personnel, correction.field_name, None)
                
                # تحديث الحقل
                setattr(personnel, correction.field_name, correction.new_value)
                personnel.save()
                
                # تحديث حالة الاقتراح
                correction.status = 'approved'
                correction.reviewed_by = request.user
                correction.reviewed_at = timezone.now()
                correction.save()
                
                # إنشاء سجل حدث
                ServiceEventLog.objects.create(
                    personnel=personnel,
                    security_admin=personnel.security_admin,
                    event_date=timezone.now().date(),
                    service_month=timezone.now().strftime('%Y-%m'),
                    field_name=correction.field_name,
                    old_value=str(old_value) if old_value else '',
                    new_value=correction.new_value,
                    order_document=correction.supporting_document,
                    created_by=request.user
                )
                
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append({
                    'correction_id': correction.id,
                    'error': str(e)
                })
        
        return Response({
            'success': True,
            'message': f'تم تطبيق {success_count} تصحيح بنجاح، فشل {failed_count}',
            'success_count': success_count,
            'failed_count': failed_count,
            'errors': errors
        })
    
    @extend_schema(
        summary='رفض تصحيحات متعددة',
        description='رفض عدة اقتراحات تصحيح دفعة واحدة',
        tags=['raw-data'],
        request=BulkRejectCorrectionSerializer,
    )
    @action(detail=False, methods=['post'])
    def bulk_reject(self, request):
        """رفض تصحيحات متعددة"""
        serializer = BulkRejectCorrectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        correction_ids = serializer.validated_data['correction_ids']
        rejection_reason = serializer.validated_data['rejection_reason']
        
        updated = SuggestedCorrection.objects.filter(
            id__in=correction_ids,
            status='pending'
        ).update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
            rejection_reason=rejection_reason
        )
        
        return Response({
            'success': True,
            'message': f'تم رفض {updated} تصحيح',
            'count': updated
        })
    
    @extend_schema(
        summary='إحصائيات البيانات الخام',
        description='عرض إحصائيات عامة عن البيانات الخام',
        tags=['raw-data'],
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """إحصائيات البيانات الخام"""
        queryset = self.get_queryset()
        
        stats = {
            'total_personnel': queryset.count(),
            'with_pending_corrections': queryset.annotate(
                pending_count=Count('suggested_corrections', filter=Q(suggested_corrections__status='pending'))
            ).filter(pending_count__gt=0).count(),
            'clean_data': queryset.filter(is_data_clean=True).count(),
            'complete_data': queryset.filter(is_complete=True).count(),
            'by_national_id_status': {},
            'by_classification': {},
        }
        
        # حسب حالة الرقم الوطني (محسوبة عبر DB queries)
        nid_missing = queryset.filter(
            Q(national_id__isnull=True) | Q(national_id='')
        ).count()
        nid_invalid_format = queryset.exclude(
            Q(national_id__isnull=True) | Q(national_id='')
        ).exclude(national_id__regex=r'^\d+$').count()
        nid_invalid_length = queryset.filter(
            national_id__regex=r'^\d+$'
        ).exclude(national_id__regex=r'^\d{11}$').count()
        nid_valid = queryset.filter(national_id__regex=r'^\d{11}$').count()
        
        stats['by_national_id_status'] = {
            'صحيح': nid_valid,
            'ناقص': nid_missing,
            'صيغة غير صحيحة': nid_invalid_format,
            'طول غير صحيح': nid_invalid_length,
        }
        
        # حسب تصنيف الحالة الخدمية
        from django.db.models import Count as DjangoCount
        classifications = queryset.values(
            'current_status__classification'
        ).annotate(
            count=DjangoCount('military_number')
        )
        
        for item in classifications:
            classification = item['current_status__classification']
            if classification:
                stats['by_classification'][classification] = item['count']
        
        return Response({
            'success': True,
            'data': stats
        })
