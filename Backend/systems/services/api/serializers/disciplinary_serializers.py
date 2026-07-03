"""
Disciplinary Serializers — وحدة الجزاءات والانضباط
════════════════════════════════════════════════════
يغطي الـ 3 نماذج:
  - DisciplinaryAction       → الجزاءات والإجراءات
  - AbsenceRecord            → سجل الغيابات
  - DisciplinaryCouncilVerdict → أحكام المجلس التأديبي
"""
from rest_framework import serializers
from systems.services.infrastructure.models.disciplinary import (
    DisciplinaryAction,
    AbsenceRecord,
    DisciplinaryCouncilVerdict,
)


# ══════════════════════════════════════════════════════════════════════════════
# 1. DisciplinaryAction — الجزاءات
# ══════════════════════════════════════════════════════════════════════════════

class DisciplinaryActionListSerializer(serializers.ModelSerializer):
    """قائمة مختصرة — للـ ListView"""
    personnel_name           = serializers.CharField(source='personnel.full_name',          read_only=True)
    personnel_military_number= serializers.CharField(source='personnel.military_number',     read_only=True)
    personnel_rank           = serializers.CharField(source='personnel.current_rank.name',   read_only=True)
    action_type_display      = serializers.CharField(source='get_action_type_display',       read_only=True)
    source_type_display      = serializers.CharField(source='get_source_type_display',       read_only=True)
    status_display           = serializers.CharField(source='get_status_display',            read_only=True)
    security_admin_name      = serializers.CharField(source='security_admin.name',           read_only=True)

    class Meta:
        model  = DisciplinaryAction
        fields = [
            'id',
            'personnel', 'personnel_name', 'personnel_military_number', 'personnel_rank',
            'security_admin', 'security_admin_name',
            'action_type', 'action_type_display',
            'source_type', 'source_type_display',
            'issued_by_name', 'decision_ref',
            'issued_date', 'effective_date', 'duration_days',
            'status', 'status_display',
            'ministry_notified', 'ministry_notified_at', 'ministry_sent_batch',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DisciplinaryActionDetailSerializer(serializers.ModelSerializer):
    """تفاصيل كاملة — للـ RetrieveView"""
    personnel_name           = serializers.CharField(source='personnel.full_name',          read_only=True)
    personnel_military_number= serializers.CharField(source='personnel.military_number',     read_only=True)
    personnel_rank           = serializers.CharField(source='personnel.current_rank.name',   read_only=True)
    action_type_display      = serializers.CharField(source='get_action_type_display',       read_only=True)
    source_type_display      = serializers.CharField(source='get_source_type_display',       read_only=True)
    status_display           = serializers.CharField(source='get_status_display',            read_only=True)
    security_admin_name      = serializers.CharField(source='security_admin.name',           read_only=True)
    created_by_name          = serializers.CharField(source='created_by.get_full_name',      read_only=True)
    attachments              = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return list(obj.attachments.values('id', 'document_type', 'original_filename', 'file', 'created_at'))

    class Meta:
        model  = DisciplinaryAction
        fields = [
            'id',
            'personnel', 'personnel_name', 'personnel_military_number', 'personnel_rank',
            'security_admin', 'security_admin_name',
            'action_type', 'action_type_display',
            'source_type', 'source_type_display',
            'issued_by_name', 'decision_ref',
            'issued_date', 'effective_date', 'duration_days',
            'description', 'status', 'status_display',
            'ministry_notified', 'ministry_notified_at', 'ministry_sent_batch',
            'attachments',
            'created_by', 'created_by_name', 'notes',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DisciplinaryActionCreateSerializer(serializers.ModelSerializer):
    """
    إنشاء جزاء جديد.
    الحقل document_ids يُمرَّر بشكل منفصل ويُعالَج في الـ View.
    """
    document_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        help_text='قائمة معرفات المرفقات المرتبطة بهذا الجزاء',
    )

    class Meta:
        model  = DisciplinaryAction
        fields = [
            'personnel', 'security_admin',
            'action_type', 'source_type',
            'issued_by_name', 'decision_ref',
            'issued_date', 'effective_date', 'duration_days',
            'description', 'status', 'notes',
            'document_ids',
        ]

    def validate(self, attrs):
        # إلزامية المدة للإيقاف والحبس
        action_type   = attrs.get('action_type')
        duration_days = attrs.get('duration_days')
        if action_type in (
            DisciplinaryAction.ActionType.SUSPENSION,
            DisciplinaryAction.ActionType.DETENTION,
        ) and not duration_days:
            raise serializers.ValidationError({
                'duration_days': 'المدة بالأيام إلزامية لجزاء الإيقاف والحبس العسكري.'
            })

        # تاريخ السريان بعد تاريخ الصدور
        issued    = attrs.get('issued_date')
        effective = attrs.get('effective_date')
        if issued and effective and effective < issued:
            raise serializers.ValidationError({
                'effective_date': 'تاريخ السريان لا يمكن أن يسبق تاريخ صدور الجزاء.'
            })
        return attrs


class DisciplinaryActionUpdateStatusSerializer(serializers.Serializer):
    """تعديل حالة الجزاء فقط (قيد التنفيذ / منفذ / ملغى)"""
    status = serializers.ChoiceField(choices=DisciplinaryAction.Status.choices)
    notes  = serializers.CharField(required=False, allow_blank=True)


class NotifyMinistrySerializer(serializers.Serializer):
    """تأكيد إبلاغ الإدارة العامة"""
    ministry_sent_batch = serializers.CharField(
        required=False, allow_blank=True,
        help_text='رقم دفعة الإرسال — يُربط برفع الخدمات الشهرية',
    )


# ══════════════════════════════════════════════════════════════════════════════
# 2. AbsenceRecord — سجل الغيابات
# ══════════════════════════════════════════════════════════════════════════════

class AbsenceRecordListSerializer(serializers.ModelSerializer):
    """قائمة مختصرة"""
    personnel_name           = serializers.CharField(source='personnel.full_name',        read_only=True)
    personnel_military_number= serializers.CharField(source='personnel.military_number',   read_only=True)
    absence_type_display     = serializers.CharField(source='get_absence_type_display',    read_only=True)
    source_display           = serializers.CharField(source='get_source_display',          read_only=True)
    status_display           = serializers.CharField(source='get_status_display',          read_only=True)
    duration_days            = serializers.IntegerField(read_only=True)
    security_admin_name      = serializers.CharField(source='security_admin.name',         read_only=True)

    class Meta:
        model  = AbsenceRecord
        fields = [
            'id',
            'personnel', 'personnel_name', 'personnel_military_number',
            'security_admin', 'security_admin_name',
            'absence_type', 'absence_type_display',
            'from_date', 'to_date', 'duration_days',
            'source', 'source_display',
            'reported_by_unit',
            'status', 'status_display',
            'ministry_notified',
            'linked_action',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'duration_days']


class AbsenceRecordDetailSerializer(serializers.ModelSerializer):
    """تفاصيل كاملة"""
    personnel_name           = serializers.CharField(source='personnel.full_name',        read_only=True)
    personnel_military_number= serializers.CharField(source='personnel.military_number',   read_only=True)
    personnel_rank           = serializers.CharField(source='personnel.current_rank.name', read_only=True)
    absence_type_display     = serializers.CharField(source='get_absence_type_display',    read_only=True)
    source_display           = serializers.CharField(source='get_source_display',          read_only=True)
    status_display           = serializers.CharField(source='get_status_display',          read_only=True)
    duration_days            = serializers.IntegerField(read_only=True)
    security_admin_name      = serializers.CharField(source='security_admin.name',         read_only=True)
    created_by_name          = serializers.CharField(source='created_by.get_full_name',    read_only=True)
    linked_action_display    = serializers.SerializerMethodField()

    def get_linked_action_display(self, obj):
        if obj.linked_action:
            return {
                'id': obj.linked_action.id,
                'action_type': obj.linked_action.get_action_type_display(),
                'issued_date': obj.linked_action.issued_date,
                'status': obj.linked_action.get_status_display(),
            }
        return None

    class Meta:
        model  = AbsenceRecord
        fields = [
            'id',
            'personnel', 'personnel_name', 'personnel_military_number', 'personnel_rank',
            'security_admin', 'security_admin_name',
            'absence_type', 'absence_type_display',
            'from_date', 'to_date', 'duration_days',
            'reported_by_unit',
            'source', 'source_display',
            'status', 'status_display',
            'ministry_notified', 'ministry_notified_at', 'ministry_sent_batch',
            'linked_action', 'linked_action_display',
            'created_by', 'created_by_name', 'notes',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'duration_days']


class AbsenceRecordCreateSerializer(serializers.ModelSerializer):
    """إنشاء سجل غياب"""

    class Meta:
        model  = AbsenceRecord
        fields = [
            'personnel', 'security_admin',
            'absence_type', 'from_date', 'to_date',
            'reported_by_unit', 'source', 'notes',
        ]

    def validate(self, attrs):
        from_date = attrs.get('from_date')
        to_date   = attrs.get('to_date')
        if from_date and to_date and to_date < from_date:
            raise serializers.ValidationError({
                'to_date': 'تاريخ الانتهاء لا يمكن أن يسبق تاريخ البداية.'
            })
        return attrs


class AbsenceCloseSerializer(serializers.Serializer):
    """إغلاق سجل الغياب — عاد الفرد للعمل"""
    to_date = serializers.DateField(help_text='تاريخ العودة الفعلي')
    notes   = serializers.CharField(required=False, allow_blank=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. DisciplinaryCouncilVerdict — أحكام المجلس التأديبي
# ══════════════════════════════════════════════════════════════════════════════

class VerdictListSerializer(serializers.ModelSerializer):
    """قائمة مختصرة"""
    personnel_name           = serializers.CharField(source='personnel.full_name',        read_only=True)
    personnel_military_number= serializers.CharField(source='personnel.military_number',   read_only=True)
    verdict_type_display     = serializers.CharField(source='get_verdict_type_display',    read_only=True)
    status_display           = serializers.CharField(source='get_status_display',          read_only=True)
    security_admin_name      = serializers.CharField(source='security_admin.name',         read_only=True)

    class Meta:
        model  = DisciplinaryCouncilVerdict
        fields = [
            'id',
            'personnel', 'personnel_name', 'personnel_military_number',
            'security_admin', 'security_admin_name',
            'verdict_ref', 'verdict_date',
            'verdict_type', 'verdict_type_display',
            'status', 'status_display',
            'ministry_sent_at', 'ministry_sent_batch',
            'linked_action',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class VerdictDetailSerializer(serializers.ModelSerializer):
    """تفاصيل كاملة"""
    personnel_name           = serializers.CharField(source='personnel.full_name',        read_only=True)
    personnel_military_number= serializers.CharField(source='personnel.military_number',   read_only=True)
    personnel_rank           = serializers.CharField(source='personnel.current_rank.name', read_only=True)
    verdict_type_display     = serializers.CharField(source='get_verdict_type_display',    read_only=True)
    status_display           = serializers.CharField(source='get_status_display',          read_only=True)
    security_admin_name      = serializers.CharField(source='security_admin.name',         read_only=True)
    created_by_name          = serializers.CharField(source='created_by.get_full_name',    read_only=True)
    attachments              = serializers.SerializerMethodField()
    linked_action_display    = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return list(obj.attachments.values('id', 'document_type', 'original_filename', 'file', 'created_at'))

    def get_linked_action_display(self, obj):
        if obj.linked_action:
            return {
                'id': obj.linked_action.id,
                'action_type': obj.linked_action.get_action_type_display(),
                'issued_date': obj.linked_action.issued_date,
                'status': obj.linked_action.get_status_display(),
            }
        return None

    class Meta:
        model  = DisciplinaryCouncilVerdict
        fields = [
            'id',
            'personnel', 'personnel_name', 'personnel_military_number', 'personnel_rank',
            'security_admin', 'security_admin_name',
            'verdict_ref', 'verdict_date',
            'verdict_type', 'verdict_type_display',
            'verdict_details', 'status', 'status_display',
            'ministry_sent_at', 'ministry_sent_batch',
            'linked_action', 'linked_action_display',
            'attachments',
            'created_by', 'created_by_name', 'notes',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VerdictCreateSerializer(serializers.ModelSerializer):
    """
    تسجيل حكم تأديبي جديد.
    document_ids تُمرَّر منفصلة وتُعالَج في الـ View.
    """
    document_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        help_text='قائمة معرفات نسخ الحكم المرفقة',
    )

    class Meta:
        model  = DisciplinaryCouncilVerdict
        fields = [
            'personnel', 'security_admin',
            'verdict_ref', 'verdict_date',
            'verdict_type', 'verdict_details',
            'linked_action', 'notes',
            'document_ids',
        ]


class VerdictSendToMinistrySerializer(serializers.Serializer):
    """تأكيد إرسال الحكم للإدارة العامة"""
    ministry_sent_batch = serializers.CharField(
        required=False, allow_blank=True,
        help_text='رقم دفعة الإرسال — اتركه فارغاً إذا أُرسِل منفرداً',
    )
