from rest_framework import serializers
from ..models import (
    Correspondence, Task, Circular, CorrespondenceAttachment,
    MeetingMinutes, DocumentWorkRequest, InventoryItem, InventoryRequest,
    Custody, AttendanceLog, FinancialAllocation, Expense, CorrespondenceReferral
)
from systems.personnel.models import PersonnelMaster
from core.models import SecurityAdministration

class CorrespondenceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrespondenceAttachment
        fields = '__all__'

class CorrespondenceReferralSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    referred_by_name = serializers.CharField(source='referred_by.get_full_name', read_only=True)
    referred_to_name = serializers.CharField(source='referred_to.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    correspondence_subject = serializers.CharField(source='correspondence.subject', read_only=True)

    class Meta:
        model = CorrespondenceReferral
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin', 'referred_by')

class CorrespondenceReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Correspondence
        fields = ('id', 'reference_number', 'subject', 'date', 'status')

class CorrespondenceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    confidentiality_level_display = serializers.CharField(source='get_confidentiality_level_display', read_only=True)
    urgency_level_display = serializers.CharField(source='get_urgency_level_display', read_only=True)
    attachments = CorrespondenceAttachmentSerializer(many=True, read_only=True)
    referrals = CorrespondenceReferralSerializer(many=True, read_only=True)
    replies = CorrespondenceReplySerializer(many=True, read_only=True)
    qr_code_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Correspondence
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/secretariat/correspondences/track/{obj.tracking_token}/")
        return f"/secretariat/correspondences/track/{obj.tracking_token}/"

class TaskSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    related_correspondence_subject = serializers.CharField(source='related_correspondence.subject', read_only=True)
    related_correspondence_reference = serializers.CharField(source='related_correspondence.reference_number', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class CircularSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)

    class Meta:
        model = Circular
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class MeetingMinutesSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    attendees_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MeetingMinutes
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

    def get_attendees_details(self, obj):
        return [
            {"id": p.id, "full_name": p.full_name, "military_number": p.military_number}
            for p in obj.attendees.all()
        ]

class DocumentWorkRequestSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.full_name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DocumentWorkRequest
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class InventoryItemSerializer(serializers.ModelSerializer):
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ('security_admin',)

class InventoryRequestSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.full_name', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_code = serializers.CharField(source='item.code', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = InventoryRequest
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class CustodySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Custody
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class AttendanceLogSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_military_number = serializers.CharField(source='employee.military_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AttendanceLog
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

class ExpenseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    allocation_month = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

    def get_allocation_month(self, obj):
        return obj.allocation.month.strftime('%Y-%m') if obj.allocation else None

class FinancialAllocationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    security_admin_name = serializers.CharField(source='security_admin.name', read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    total_spent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FinancialAllocation
        fields = '__all__'
        read_only_fields = ('created_by', 'security_admin')

    def get_total_spent(self, obj):
        from django.db.models import Sum
        result = obj.expenses.aggregate(total=Sum('amount'))
        return result['total'] or 0.00
