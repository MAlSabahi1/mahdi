"""
Personnel Serializers - مسلسلات إدارة الأفراد
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from systems.personnel.models import PersonnelMaster, SuggestedCorrection, HistoricalMonthlyVariables, RankSettlement
from systems.services.models import ServiceEventLog
from core.api.serializers import (
    RankSerializer, ServiceStatusSerializer,
    QualificationSerializer,
)


@extend_schema_serializer(component_name='PersonnelList')
class PersonnelListSerializer(serializers.ModelSerializer):
    """مسلسل مختصر لعرض القائمة (جدول)"""
    rank_name = serializers.CharField(source='current_rank.name', read_only=True)
    status_name = serializers.CharField(
        source='current_status.name', read_only=True
    )
    status_classification = serializers.CharField(
        source='current_status.classification', read_only=True
    )
    status_classification_display = serializers.CharField(
        source='current_status.get_classification_display', read_only=True
    )
    expense_status_display = serializers.CharField(
        source='get_expense_status_display', read_only=True
    )
    # الهيكل التنظيمي الأمني
    security_admin_name = serializers.CharField(
        source='security_admin.name', read_only=True, default=None
    )
    central_department_name = serializers.CharField(
        source='central_department.name', read_only=True, default=None
    )
    branch_name = serializers.CharField(
        source='branch.name', read_only=True, default=None
    )
    district_police_name = serializers.CharField(
        source='district_police.name', read_only=True, default=None
    )
    division_name = serializers.CharField(
        source='division.name', read_only=True, default=None
    )
    unit_name = serializers.CharField(
        source='unit.name', read_only=True, default=None
    )

    # حقول إضافية
    pending_rank_name = serializers.CharField(
        source='pending_rank.name', read_only=True, default=None
    )
    category_name = serializers.CharField(
        source='category.name', read_only=True, default=None
    )
    job_title_name = serializers.CharField(
        source='job_title.name', read_only=True, default=None
    )
    position_name = serializers.CharField(
        source='position.name', read_only=True, default=None
    )
    force_classification_name = serializers.CharField(
        source='force_classification.name', read_only=True, default=None
    )
    qualification_name = serializers.CharField(
        source='qualification.name', read_only=True, default=None
    )
    birth_gov_id = serializers.IntegerField(source='birth_governorate_id', read_only=True)
    birth_district_id = serializers.IntegerField(read_only=True)
    birth_sub_district_id = serializers.IntegerField(read_only=True)
    birth_village_id = serializers.IntegerField(read_only=True)
    residence_gov_id = serializers.IntegerField(source='residence_governorate_id', read_only=True)
    residence_district_id = serializers.IntegerField(read_only=True)
    residence_sub_district_id = serializers.IntegerField(read_only=True)
    residence_village_id = serializers.IntegerField(read_only=True)
    has_pending_correction = serializers.SerializerMethodField()
    military_number_type = serializers.DictField(read_only=True)
    national_id_status = serializers.CharField(read_only=True)
    national_id_status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = PersonnelMaster
        fields = [
            'military_number', 'old_military_number',
            'military_number_type',
            'full_name',
            'national_id', 'national_id_status', 'national_id_status_display',
            'current_rank', 'rank_name',
            'pending_rank', 'pending_rank_name',
            'current_status', 'status_name', 'status_classification', 'status_classification_display',
            # الهيكل التنظيمي الأمني
            'security_admin', 'security_admin_name',
            'central_department', 'central_department_name',
            'branch', 'branch_name',
            'district_police', 'district_police_name',
            'division', 'division_name',
            'unit', 'unit_name',
            # التوصيف الوظيفي
            'category', 'category_name',
            'job_title', 'job_title_name',
            'position', 'position_name',
            'force_classification', 'force_classification_name',
            'qualification', 'qualification_name',
            # بيانات أخرى
            'phone_number', 'birth_date', 'join_date',
            'birth_gov_id', 'birth_district_id', 'birth_sub_district_id', 'birth_village_id',
            'residence_gov_id', 'residence_district_id', 'residence_sub_district_id', 'residence_village_id',
            'id_issue_date', 'id_issue_place',
            'expense_status', 'expense_status_display', 'appointment_info', 'notes',
            'is_complete', 'is_data_clean', 'data_quality_score',
            'has_pending_correction',
            'updated_at',
        ]
    
    def get_has_pending_correction(self, obj):
        return obj.suggested_corrections.filter(status='pending').exists()


@extend_schema_serializer(component_name='PersonnelDetail')
class PersonnelDetailSerializer(serializers.ModelSerializer):
    """مسلسل تفصيلي: كل البيانات + آخر أحداث"""
    rank = RankSerializer(source='current_rank', read_only=True)
    status = ServiceStatusSerializer(
        source='current_status', read_only=True
    )
    qualification_detail = QualificationSerializer(
        source='qualification', read_only=True
    )
    expense_status_display = serializers.CharField(
        source='get_expense_status_display', read_only=True
    )
    geo_location_name = serializers.CharField(
        source='geo_location.name_ar', read_only=True, default=None
    )
    # الهيكل التنظيمي الأمني
    security_admin_name = serializers.CharField(
        source='security_admin.name', read_only=True, default=None
    )
    central_department_name = serializers.CharField(
        source='central_department.name', read_only=True, default=None
    )
    branch_name = serializers.CharField(
        source='branch.name', read_only=True, default=None
    )
    district_police_name = serializers.CharField(
        source='district_police.name', read_only=True, default=None
    )
    division_name = serializers.CharField(
        source='division.name', read_only=True, default=None
    )
    unit_name = serializers.CharField(
        source='unit.name', read_only=True, default=None
    )
    pending_rank_name = serializers.CharField(
        source='pending_rank.name', read_only=True, default=None
    )
    category_name = serializers.CharField(
        source='category.name', read_only=True, default=None
    )
    job_title_name = serializers.CharField(
        source='job_title.name', read_only=True, default=None
    )
    position_name = serializers.CharField(
        source='position.name', read_only=True, default=None
    )
    force_classification_name = serializers.CharField(
        source='force_classification.name', read_only=True, default=None
    )
    qualification_name = serializers.CharField(
        source='qualification.name', read_only=True, default=None
    )
    birth_gov_id = serializers.IntegerField(source='birth_governorate_id', read_only=True)
    birth_district_id = serializers.IntegerField(read_only=True)
    birth_sub_district_id = serializers.IntegerField(read_only=True)
    birth_village_id = serializers.IntegerField(read_only=True)
    residence_gov_id = serializers.IntegerField(source='residence_governorate_id', read_only=True)
    residence_district_id = serializers.IntegerField(read_only=True)
    residence_sub_district_id = serializers.IntegerField(read_only=True)
    residence_village_id = serializers.IntegerField(read_only=True)
    # بيانات محسوبة
    age = serializers.IntegerField(read_only=True)
    service_years = serializers.IntegerField(read_only=True)
    recent_events = serializers.SerializerMethodField()
    pending_corrections = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    military_number_type = serializers.DictField(read_only=True)
    national_id_status = serializers.CharField(read_only=True)
    national_id_status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = PersonnelMaster
        fields = [
            'military_number', 'old_military_number',
            'military_number_type',
            'national_id',
            'national_id_status', 'national_id_status_display',
            'full_name', 'birth_date', 'join_date', 'phone_number',
            'age', 'service_years',
            # الحالة
            'current_rank', 'rank', 'pending_rank', 'pending_rank_name',
            'current_status', 'status',
            # الهيكل التنظيمي الأمني
            'security_admin', 'security_admin_name',
            'central_department', 'central_department_name',
            'branch', 'branch_name',
            'district_police', 'district_police_name',
            'division', 'division_name',
            'unit', 'unit_name',

            # التوصيف الوظيفي
            'category', 'category_name',
            'job_title', 'job_title_name',
            'position', 'position_name',
            'force_classification', 'force_classification_name',
            # بيانات أخرى
            'qualification', 'qualification_detail', 'qualification_name',
            'birth_gov_id', 'birth_district_id', 'birth_sub_district_id', 'birth_village_id',
            'residence_gov_id', 'residence_district_id', 'residence_sub_district_id', 'residence_village_id',
            'id_issue_date', 'id_issue_place',
            'geo_location', 'geo_location_name',
            'photo', 'fingerprint_hash',
            'expense_status', 'expense_status_display', 'appointment_info',
            'is_complete', 'is_data_clean',
            'data_quality_score', 'notes',
            'recent_events', 'pending_corrections', 'documents',
            'created_at', 'updated_at',
        ]
    
    def get_recent_events(self, obj):
        events = ServiceEventLog.objects.filter(
            personnel=obj
        ).select_related('order_document').order_by('-event_date')[:24]
        return ServiceEventLogSerializer(events, many=True).data
    
    def get_pending_corrections(self, obj):
        corrections = obj.suggested_corrections.filter(status='pending')
        return SuggestedCorrectionSerializer(corrections, many=True).data
    
    def get_documents(self, obj):
        """المرفقات المثبّتة المرتبطة بالفرد (صور بطاقة، قرارات ترقية، إلخ)"""
        from infra.storage.models import Document
        docs = Document.objects.filter(
            personnel=obj,
            status='committed',
        ).order_by('-created_at')[:20]
        return [
            {
                'id': d.id,
                'document_type': d.document_type,
                'document_type_display': d.get_document_type_display(),
                'description': d.description,
                'related_field': d.related_field,
                'source_method': d.source_method,
                'file_url': d.file.url if d.file else None,
                'file_hash': d.file_hash,
                'version': d.version,
                'created_at': d.created_at.isoformat() if d.created_at else None,
            }
            for d in docs
        ]


class PersonnelCreateSerializer(serializers.ModelSerializer):
    """إنشاء فرد جديد"""
    
    class Meta:
        model = PersonnelMaster
        fields = [
            'military_number', 'national_id', 'full_name',
            'birth_date', 'join_date', 'phone_number',
            'current_rank', 'current_status',
            'security_admin', 'central_department', 'branch',
            'district_police', 'division', 'unit',

            'category', 'job_title', 'position', 'force_classification',
            'qualification', 'geo_location', 'expense_status', 'notes',
            
            # البيانات الجغرافية وتفاصيل الهوية الجديدة
            'birth_governorate', 'birth_district', 'birth_sub_district', 'birth_village',
            'residence_governorate', 'residence_district', 'residence_sub_district', 'residence_village',
            'id_issue_date', 'id_issue_place',
        ]
        extra_kwargs = {
            'notes': {'allow_null': True, 'allow_blank': True, 'required': False},
            'birth_date': {'allow_null': True, 'required': False},
            'qualification': {'allow_null': True, 'required': False},
            'geo_location': {'allow_null': True, 'required': False},
            'expense_status': {'allow_null': True, 'allow_blank': True, 'required': False},
            'id_issue_place': {'allow_null': True, 'allow_blank': True, 'required': False},
        }
    
    def validate_military_number(self, value):
        if len(value) != 7 or not value.isdigit():
            raise serializers.ValidationError(
                'الرقم العسكري يجب أن يكون 7 أرقام'
            )
        if PersonnelMaster.objects.filter(military_number=value).exists():
            raise serializers.ValidationError('الرقم العسكري مستخدم بالفعل')
        return value
    
    def validate_national_id(self, value):
        if value and PersonnelMaster.objects.filter(national_id=value).exists():
            raise serializers.ValidationError(
                'الرقم الوطني مستخدم بالفعل لموظف آخر. إذا كنت متأكداً من صحة الرقم، يرجى تقديم "طلب تصحيح" عبر شاشة إدارة البيانات أو مراجعة إدارة الموارد لحل النزاع.'
            )
        return value

    def validate(self, data):
        birth_date = data.get('birth_date')
        join_date = data.get('join_date')
        
        if birth_date and join_date:
            age_at_join = join_date.year - birth_date.year - ((join_date.month, join_date.day) < (birth_date.month, birth_date.day))
            if age_at_join < 18:
                raise serializers.ValidationError(
                    {'birth_date': 'تاريخ الميلاد غير صالح: يجب أن يكون عمر الفرد 18 عاماً على الأقل عند تاريخ التجنيد.'}
                )
                
        id_issue_date = data.get('id_issue_date')
        if id_issue_date:
            from datetime import date
            if id_issue_date > date.today():
                raise serializers.ValidationError(
                    {'id_issue_date': 'لا يمكن أن يكون تاريخ إصدار البطاقة في المستقبل.'}
                )
            if birth_date and id_issue_date <= birth_date:
                raise serializers.ValidationError(
                    {'id_issue_date': 'تاريخ إصدار البطاقة يجب أن يكون بعد تاريخ الميلاد.'}
                )
                
        return super().validate(data) if hasattr(super(), 'validate') else data


class PersonnelUpdateSerializer(serializers.ModelSerializer):
    """تحديث بيانات فرد"""
    expense_status = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    
    class Meta:
        model = PersonnelMaster
        fields = [
            'full_name', 'national_id', 'birth_date', 'join_date',
            'phone_number', 'current_rank', 'current_status',
            'security_admin', 'central_department', 'branch',
            'district_police', 'division', 'unit',
            'category', 'job_title', 'position', 'force_classification',
            'qualification', 'geo_location', 'expense_status',
            'pending_rank', 'is_complete', 'notes',
            
            # البيانات الجغرافية وتفاصيل الهوية الجديدة
            'birth_governorate', 'birth_district', 'birth_sub_district', 'birth_village',
            'residence_governorate', 'residence_district', 'residence_sub_district', 'residence_village',
            'id_issue_date', 'id_issue_place',
        ]
        extra_kwargs = {
            'notes': {'allow_null': True, 'allow_blank': True, 'required': False},
            'birth_date': {'allow_null': True, 'required': False},
            'qualification': {'allow_null': True, 'required': False},
            'geo_location': {'allow_null': True, 'required': False},
            'expense_status': {'allow_null': True, 'allow_blank': True, 'required': False},
            'id_issue_place': {'allow_null': True, 'allow_blank': True, 'required': False},
            # السماح بـ null/blank للحقول الجغرافية أثناء PATCH
            'birth_governorate': {'allow_null': True, 'required': False},
            'birth_district': {'allow_null': True, 'required': False},
            'birth_sub_district': {'allow_null': True, 'required': False},
            'birth_village': {'allow_null': True, 'required': False},
            'residence_governorate': {'allow_null': True, 'required': False},
            'residence_district': {'allow_null': True, 'required': False},
            'residence_sub_district': {'allow_null': True, 'required': False},
            'residence_village': {'allow_null': True, 'required': False},
            'id_issue_date': {'allow_null': True, 'required': False},
        }
    
    def validate_national_id(self, value):
        instance = self.instance
        user = self.context.get('request').user if self.context.get('request') else None
        
        # إذا تم تغيير الرقم الوطني ولم يكن المستخدم سوبر أدمن، يتم الرفض
        if instance and instance.national_id != value:
            if user and not user.is_superuser:
                raise serializers.ValidationError(
                    'لا يمكن تعديل الرقم الوطني مباشرة. يرجى تقديم "طلب تصحيح" مع إرفاق الوثائق الثبوتية.'
                )
        
        if instance and PersonnelMaster.objects.filter(
            national_id=value
        ).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError('الرقم الوطني مستخدم بالفعل لموظف آخر')
        return value

    def validate(self, data):
        instance = self.instance

        # ── حماية الحقول الجغرافية: لا تكتب null فوق قيمة موجودة في قاعدة البيانات ──
        # هذا يحمي البيانات الجغرافية المحفوظة من الضياع عند إرسال null من الفرونت
        GEO_FIELDS = [
            'birth_governorate', 'birth_district', 'birth_sub_district', 'birth_village',
            'residence_governorate', 'residence_district', 'residence_sub_district', 'residence_village',
        ]
        if instance and self.partial:
            for field in GEO_FIELDS:
                if field in data and data[field] is None:
                    existing_val = getattr(instance, f'{field}_id', None)
                    if existing_val is not None:
                        # Don't overwrite existing value with null
                        del data[field]

        birth_date = data.get('birth_date', getattr(instance, 'birth_date', None))
        join_date = data.get('join_date', getattr(instance, 'join_date', None))
        
        if birth_date and join_date:
            age_at_join = join_date.year - birth_date.year - ((join_date.month, join_date.day) < (birth_date.month, birth_date.day))
            if age_at_join < 18:
                raise serializers.ValidationError(
                    {'birth_date': 'تاريخ الميلاد غير صالح: يجب أن يكون عمر الفرد 18 عاماً على الأقل عند تاريخ التجنيد.'}
                )
                
        id_issue_date = data.get('id_issue_date')
        if id_issue_date:
            from datetime import date
            if id_issue_date > date.today():
                raise serializers.ValidationError(
                    {'id_issue_date': 'لا يمكن أن يكون تاريخ إصدار البطاقة في المستقبل.'}
                )
            
            # Since birth_date might not be in data if it wasn't updated, check instance too
            final_birth_date = birth_date or (instance.birth_date if instance else None)
            if final_birth_date and id_issue_date <= final_birth_date:
                raise serializers.ValidationError(
                    {'id_issue_date': 'تاريخ إصدار البطاقة يجب أن يكون بعد تاريخ الميلاد.'}
                )
                
        return super().validate(data) if hasattr(super(), 'validate') else data


# ============================================================================
# Supporting Serializers
# ============================================================================

class ServiceEventLogSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True, default=None
    )
    
    class Meta:
        model = ServiceEventLog
        fields = [
            'id', 'event_date', 'service_month',
            'field_name', 'old_value', 'new_value',
            'order_document', 'created_by', 'created_by_name',
            'created_at',
        ]


class SuggestedCorrectionSerializer(serializers.ModelSerializer):
    """
    مسلسل متكامل لاقتراحات التصحيح (SuggestedCorrection).

    ─── للمطور ────────────────────────────────────────────────────
    • حقول القراءة فقط: id, status, requested_by, reviewed_by,
      requested_at, reviewed_at, approval_document
    • عند الإنشاء (POST) يُرسَل: personnel (رقم عسكري), correction_type,
      field_name, old_value, new_value, supporting_document, notes,
      metadata (اختياري), linked_correction (اختياري)
    • التحقق من المرفقات يتم هنا في validate() حسب نوع التصحيح
    ────────────────────────────────────────────────────────────────
    """
    # ── حقول مقروءة للعرض ──
    personnel_name = serializers.CharField(
        source='personnel.full_name', read_only=True, default=None
    )
    personnel_military_number = serializers.CharField(
        source='personnel.military_number', read_only=True, default=None
    )
    personnel_rank = serializers.CharField(
        source='personnel.current_rank.name', read_only=True, default=None
    )
    personnel_department = serializers.CharField(
        source='personnel.central_department.name', read_only=True, default=None
    )
    requested_by_name = serializers.CharField(
        source='requested_by.username', read_only=True, default=None
    )
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.username', read_only=True, default=None
    )
    correction_type_display = serializers.CharField(
        source='get_correction_type_display', read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )
    # معلومات المذكرة الوزارية (فقط بعد الموافقة)
    approval_document_url = serializers.SerializerMethodField()

    # ── الحقل الذي يقبل الرقم العسكري كـ write_only للإنشاء ──
    # (personnel FK يقبل PK لكن الفرونت يرسل الرقم العسكري)
    personnel_military_number_input = serializers.CharField(
        write_only=True, required=False,
        help_text='الرقم العسكري للفرد — بديل عن personnel (FK)'
    )

    class Meta:
        model = SuggestedCorrection
        fields = [
            # تعريف الطلب
            'id', 'correction_type', 'correction_type_display',
            'field_name', 'old_value', 'new_value',
            # الفرد
            'personnel', 'personnel_military_number_input',
            'personnel_name', 'personnel_military_number',
            'personnel_rank', 'personnel_department',
            # الحالة
            'status', 'status_display', 'is_printed',
            # المرفقات
            'supporting_document',       # وثيقة الطلب (بطاقة / نموذج 23)
            'approval_document',         # مذكرة الوزارة (تُملأ عند الموافقة)
            'approval_document_url',
            # التواصل الداخلي والبيانات المرنة
            'notes', 'metadata', 'linked_correction',
            # التدقيق (للقراءة فقط)
            'requested_by', 'requested_by_name', 'requested_at',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at',
            'rejection_reason',
        ]
        read_only_fields = [
            'id', 'status', 'requested_by', 'requested_at',
            'reviewed_by', 'reviewed_at', 'rejection_reason',
            'approval_document',         # تُملأ فقط عبر approve_batch
        ]

    def get_approval_document_url(self, obj):
        """رابط تحميل المذكرة الوزارية المرفقة عند الموافقة"""
        if obj.approval_document and obj.approval_document.file:
            return obj.approval_document.file.url
        return None

    def validate_personnel(self, value):
        """يمنع إنشاء طلب لفرد محذوف"""
        if value and value.is_deleted:
            raise serializers.ValidationError(
                'لا يمكن إنشاء طلب تصحيح لفرد محذوف من النظام.'
            )
        return value

    def validate(self, data):
        """
        التحقق الشامل حسب نوع التصحيح:

        name_correction         → supporting_document إلزامي
        national_id_correction  → يُتحقق في Service Layer حسب الدور
                                  (رئيس خدمات: مباشر | موظف: يطلب موافقة)
        military_number_correction → supporting_document إلزامي
        """
        correction_type = data.get('correction_type')
        supporting_doc = data.get('supporting_document')

        # الحصول على متطلبات هذا النوع من DOCUMENT_REQUIREMENTS
        req = SuggestedCorrection.DOCUMENT_REQUIREMENTS.get(correction_type, {})

        if req.get('required') and not supporting_doc:
            raise serializers.ValidationError({
                'supporting_document': (
                    f'هذا النوع من التصحيح ({correction_type}) يتطلب مرفقاً داعماً: '
                    f'{req.get("description", "")}'
                )
            })

        # حل personnel من الرقم العسكري إذا أُرسل كـ input
        military_input = data.pop('personnel_military_number_input', None)
        if military_input and not data.get('personnel'):
            mil = str(military_input).zfill(7)
            try:
                data['personnel'] = PersonnelMaster.objects.get(military_number=mil)
            except PersonnelMaster.DoesNotExist:
                raise serializers.ValidationError({
                    'personnel_military_number_input': f'الفرد برقم {mil} غير موجود.'
                })

        if not data.get('personnel'):
            raise serializers.ValidationError({
                'personnel': 'يجب تحديد الفرد (personnel أو personnel_military_number_input).'
            })

        # منع تكرار الطلبات المعلقة لنفس الفرد ونفس الحقل
        personnel = data.get('personnel')
        field_name = data.get('field_name')
        if personnel and field_name:
            exists_pending = SuggestedCorrection.objects.filter(
                personnel=personnel,
                field_name=field_name,
                status='pending'
            ).exists()
            if exists_pending:
                raise serializers.ValidationError({
                    'field_name': 'يوجد بالفعل طلب تصحيح معلق (قيد الانتظار) لنفس هذا الحقل لهذا الفرد. لا يمكن تقديم طلب آخر حتى يتم البت في الطلب الحالي.'
                })

        return data

    def create(self, validated_data):
        """
        يُسجّل تلقائياً requested_by من الطلب.
        يمرر البيانات لـ full_clean() قبل الحفظ لضمان قواعد النموذج.
        """
        request = self.context.get('request')
        validated_data['requested_by'] = request.user if request else None

        instance = SuggestedCorrection(**validated_data)
        instance.full_clean()   # تُطبَّق قواعد clean() على النموذج
        instance.save()
        return instance




class HistoricalMonthlyVariablesSerializer(serializers.ModelSerializer):
    variable_type_name = serializers.CharField(
        source='variable_type.name', read_only=True, default=None
    )
    variable_type_code = serializers.CharField(
        source='variable_type.code', read_only=True, default=None
    )
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True, default=None
    )
    source_display = serializers.CharField(
        source='get_source_display', read_only=True
    )

    class Meta:
        model = HistoricalMonthlyVariables
        fields = [
            'id', 'personnel', 'month',
            'variable_type', 'variable_type_name', 'variable_type_code',
            'variable_value', 'source', 'source_display',
            'source_column', 'notes',
            'created_by', 'created_by_name',
            'created_at',
        ]
        read_only_fields = ['created_at']


class PersonnelHistorySerializer(serializers.Serializer):
    """تاريخ الفرد من Shadow Table"""
    history_id = serializers.IntegerField()
    history_action = serializers.CharField()
    history_user = serializers.CharField()
    history_timestamp = serializers.DateTimeField()
    history_version = serializers.IntegerField()
    military_number = serializers.CharField()
    full_name = serializers.CharField()
    national_id = serializers.CharField(allow_null=True)
    directorate_id = serializers.IntegerField(allow_null=True)
    current_rank_id = serializers.IntegerField(allow_null=True)
    current_status_id = serializers.IntegerField(allow_null=True)


# ============================================================================
# RankSettlement Serializer — طلبات تسوية الرتب
# ============================================================================

class RankSettlementSerializer(serializers.ModelSerializer):
    """مسلسل طلبات تسوية الرتب"""
    personnel_name = serializers.CharField(
        source='personnel.full_name', read_only=True
    )
    personnel_military_number = serializers.CharField(
        source='personnel.military_number', read_only=True
    )
    from_rank_name = serializers.CharField(
        source='from_rank.name', read_only=True
    )
    to_rank_name = serializers.CharField(
        source='to_rank.name', read_only=True
    )
    requested_by_name = serializers.CharField(
        source='requested_by.username', read_only=True, default=None
    )
    applied_by_name = serializers.CharField(
        source='applied_by.username', read_only=True, default=None
    )
    
    class Meta:
        model = RankSettlement
        fields = [
            'id', 'personnel', 'personnel_name', 'personnel_military_number',
            'settlement_type',
            'from_rank', 'from_rank_name',
            'to_rank', 'to_rank_name',
            'new_military_number',
            'decision_number', 'decision_date',
            'supporting_document',
            'batch_reference',
            'status',
            'requested_by', 'requested_by_name',
            'applied_by', 'applied_by_name', 'applied_at',
            'rejection_reason', 'notes',
            'created_at',
        ]
        read_only_fields = [
            'id', 'status', 'requested_by', 'applied_by',
            'applied_at', 'rejection_reason', 'created_at',
        ]
    
    def validate(self, data):
        """تحقق شامل — يكمل clean() على المودل"""
        settlement_type = data.get('settlement_type')
        new_mil = data.get('new_military_number')
        from_rank = data.get('from_rank')
        to_rank = data.get('to_rank')
        
        # التحقق من اتجاه الرتبة حسب نوع التسوية
        if from_rank and to_rank:
            if from_rank == to_rank:
                raise serializers.ValidationError(
                    {'to_rank': 'الرتبة المطلوبة لا يمكن أن تكون نفس الرتبة الحالية.'}
                )
            
            if settlement_type == 'demotion':
                # التخفيض: الرتبة المطلوبة يجب أن تكون أقل (order أكبر)
                if to_rank.order <= from_rank.order:
                    raise serializers.ValidationError(
                        {'to_rank': 'التخفيض يتطلب اختيار رتبة أقل من الحالية.'}
                    )
            else:
                # الترقية: الرتبة المطلوبة يجب أن تكون أعلى (order أقل)
                if to_rank.order > from_rank.order:
                    raise serializers.ValidationError(
                        {'to_rank': 'الترقية يجب أن تكون لرتبة أعلى.'}
                    )
        
        # فرد→ضابط يتطلب رقم يبدأ بـ 60
        if settlement_type == 'personnel_to_officer':
            if not new_mil:
                raise serializers.ValidationError(
                    {'new_military_number': 'تسوية فرد إلى ضابط تتطلب رقماً عسكرياً جديداً.'}
                )
            if not new_mil.startswith('60'):
                raise serializers.ValidationError(
                    {'new_military_number': 'الرقم العسكري الجديد للضابط يجب أن يبدأ بـ 60.'}
                )
            if PersonnelMaster.objects.filter(military_number=new_mil).exists():
                raise serializers.ValidationError(
                    {'new_military_number': 'الرقم العسكري الجديد مستخدم بالفعل.'}
                )
        
        # ترقية ضمن نفس الصنف أو تخفيض — لا يتطلب رقم جديد
        if settlement_type in ('same_class_promotion', 'demotion') and new_mil:
            raise serializers.ValidationError(
                {'new_military_number': 'هذا النوع من التسوية لا يتطلب رقماً عسكرياً جديداً.'}
            )
        
        return data


class ActiveVariableUpsertSerializer(serializers.Serializer):
    """يستقبل البيانات من الواجهة لتحديث أو إنشاء المتغير الشهري مباشرة"""
    military_number = serializers.CharField()
    month = serializers.CharField()
    value = serializers.CharField(allow_blank=True)


class PersonnelActiveVariableSerializer(serializers.ModelSerializer):
    """يعرض بيانات الفرد الأساسية مع قيمة المتغير للشهر المطلوب (يُحسب ديناميكياً)"""
    current_variable = serializers.SerializerMethodField()
    current_rank_name = serializers.CharField(source='current_rank.name', read_only=True, default='')
    central_department_name = serializers.CharField(source='central_department.name', read_only=True, default='')

    class Meta:
        model = PersonnelMaster
        fields = [
            'military_number', 
            'full_name', 
            'current_rank_name', 
            'central_department_name',
            'current_variable'
        ]

    def get_current_variable(self, obj):
        variables = getattr(obj, 'prefetched_active_variables', [])
        if variables:
            return variables[0].variable_value
        return None
