"""
Services Admin - واجهة الإدارة للخدمات
═══════════════════════════════════════
⚠️ AuditLog admin moved to audit/admin.py
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from systems.services.models import (
    ServiceEventLog,
    StagingRecord, ReconciliationTask, MonthlySnapshot,
    ExportLog, RejectionLog, DirectorateCompliance,
    CustomFormTemplate, CustomReportTemplate
)


@admin.register(ServiceEventLog)
class ServiceEventLogAdmin(admin.ModelAdmin):
    list_display = [
        'personnel', 'field_name', 'service_month',
        'event_date', 'created_by', 'created_at'
    ]
    search_fields = ['personnel__military_number', 'personnel__full_name', 'field_name']
    list_filter = ['service_month', 'field_name', 'event_date']
    date_hierarchy = 'event_date'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('personnel', 'order_document', 'created_by')

    # ==========================================
    # IMMUTABLE LEDGER LOCKDOWN (READ-ONLY)
    # ==========================================
    def get_readonly_fields(self, request, obj=None):
        """جميع الحقول للقراءة فقط دائماً"""
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        """يمنع الإضافة اليدوية تماماً"""
        return False

    def has_change_permission(self, request, obj=None):
        """يمنع التعديل تماماً"""
        return False

    def has_delete_permission(self, request, obj=None):
        """يمنع الحذف تماماً"""
        return False




@admin.register(StagingRecord)
class StagingRecordAdmin(admin.ModelAdmin):
    list_display = [
        'personnel', 'status', 'severity', 'requires_document',
        'name_mismatch', 'rank_mismatch', 'reviewed_by', 'created_at'
    ]
    search_fields = ['personnel__military_number', 'personnel__full_name']
    list_filter = ['status', 'severity', 'requires_document', 'created_at']
    autocomplete_fields = ['personnel', 'reviewed_by']
    readonly_fields = ['created_at', 'updated_at', 'upload_batch_id']
    
    fieldsets = (
        (_('معلومات الفرد'), {
            'fields': ('personnel', 'upload_batch_id')
        }),
        (_('التغيير المقترح'), {
            'fields': ('proposed_change', 'notes', 'severity', 'requires_document')
        }),
        (_('التنبيهات'), {
            'fields': ('name_mismatch', 'rank_mismatch', 'national_id_mismatch'),
            'classes': ('collapse',)
        }),
        (_('المراجعة'), {
            'fields': ('status', 'reviewed_by', 'reviewed_at')
        }),
        (_('التوقيت'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('personnel', 'reviewed_by')


@admin.register(ReconciliationTask)
class ReconciliationTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_type', 'status', 'created_by', 'created_at']
    search_fields = ['name']
    list_filter = ['task_type', 'status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MonthlySnapshot)
class MonthlySnapshotAdmin(admin.ModelAdmin):
    list_display = ['service_month', 'locked', 'created_at']
    search_fields = ['service_month']
    list_filter = ['locked', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'data', 'service_month', 'security_admin', 'central_department']
    actions = ['unlock_snapshots', 'lock_snapshots']

    @admin.action(description=_('🔓 كسر إقفال الشهور المحددة (يسجل أمنياً)'))
    def unlock_snapshots(self, request, queryset):
        from infra.audit.models import AuditLog
        unlocked_count = 0
        for snapshot in queryset.filter(locked=True):
            snapshot.locked = False
            snapshot.save(update_fields=['locked'])
            unlocked_count += 1
            AuditLog.objects.create(
                user=request.user,
                action='UNLOCK',
                model_name='MonthlySnapshot',
                object_id=str(snapshot.id),
                old_data={'locked': True},
                new_data={'locked': False, 'reason': 'Manual Unlock via Admin Actions'}
            )
        self.message_user(request, f'تم كسر إقفال {unlocked_count} شهر بنجاح، وتم تسجيل الحدث في دفتر التدقيق.')

    @admin.action(description=_('🔒 إقفال الشهور المحددة'))
    def lock_snapshots(self, request, queryset):
        from infra.audit.models import AuditLog
        locked_count = 0
        for snapshot in queryset.filter(locked=False):
            snapshot.locked = True
            snapshot.save(update_fields=['locked'])
            locked_count += 1
            AuditLog.objects.create(
                user=request.user,
                action='LOCK',
                model_name='MonthlySnapshot',
                object_id=str(snapshot.id),
                old_data={'locked': False},
                new_data={'locked': True, 'reason': 'Manual Lock via Admin Actions'}
            )
        self.message_user(request, f'تم إقفال {locked_count} شهر بنجاح.')

    def has_delete_permission(self, request, obj=None):
        if obj and obj.locked:
            return False
        return super().has_delete_permission(request, obj)



@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    list_display = [
        'export_id_short', 'central_department', 'service_month',
        'exported_by', 'status', 'created_at'
    ]
    search_fields = ['export_id', 'central_department__name']
    list_filter = ['status', 'service_month', 'created_at']
    autocomplete_fields = ['central_department', 'exported_by']
    readonly_fields = ['export_id', 'file_hash', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('معلومات التصدير'), {
            'fields': ('export_id', 'central_department', 'service_month', 'exported_by')
        }),
        (_('الأمان'), {
            'fields': ('file_hash', 'row_uuids', 'editable_columns')
        }),
        (_('الحالة'), {
            'fields': ('status',)
        }),
        (_('التوقيت'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def export_id_short(self, obj):
        return str(obj.export_id)[:8]
    export_id_short.short_description = _('معرف التصدير')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('central_department', 'exported_by')


@admin.register(RejectionLog)
class RejectionLogAdmin(admin.ModelAdmin):
    list_display = [
        'personnel', 'central_department', 'service_month',
        'proposed_status', 'rejected_by', 'rejected_at'
    ]
    search_fields = [
        'personnel__military_number', 'personnel__full_name',
        'central_department__name', 'rejection_reason'
    ]
    list_filter = ['central_department', 'service_month', 'rejected_at']
    autocomplete_fields = ['staging_record', 'central_department', 'personnel', 'rejected_by']
    readonly_fields = ['rejected_at', 'created_at', 'updated_at']
    date_hierarchy = 'rejected_at'
    
    fieldsets = (
        (_('معلومات الرفض'), {
            'fields': ('staging_record', 'personnel', 'central_department', 'service_month')
        }),
        (_('التفاصيل'), {
            'fields': ('proposed_status', 'rejection_reason')
        }),
        (_('المراجعة'), {
            'fields': ('rejected_by', 'rejected_at')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('personnel', 'central_department', 'rejected_by', 'staging_record')


@admin.register(DirectorateCompliance)
class DirectorateComplianceAdmin(admin.ModelAdmin):
    list_display = [
        'central_department', 'service_month', 'quality_score_badge',
        'error_count', 'rejected_changes_count', 'late_days',
        'submitted_at'
    ]
    search_fields = ['central_department__name', 'service_month']
    list_filter = ['service_month', 'quality_score', 'late_days']
    autocomplete_fields = ['central_department']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('معلومات الإدارة'), {
            'fields': ('central_department', 'service_month', 'submitted_at')
        }),
        (_('الإحصائيات'), {
            'fields': ('error_count', 'rejected_changes_count', 'late_days')
        }),
        (_('الجودة'), {
            'fields': ('quality_score',)
        }),
    )
    
    def quality_score_badge(self, obj):
        if obj.quality_score >= 90:
            color = 'green'
            icon = '✓'
        elif obj.quality_score >= 70:
            color = 'orange'
            icon = '⚠'
        else:
            color = 'red'
            icon = '✗'
        return format_html(
            '<span style="color: {};">{} {}%</span>',
            color, icon, obj.quality_score
        )
    quality_score_badge.short_description = _('درجة الجودة')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('central_department')


@admin.register(CustomFormTemplate)
class CustomFormTemplateAdmin(admin.ModelAdmin):
    list_display = ['form_type', 'label', 'target_status', 'is_active', 'created_at']
    search_fields = ['form_type', 'label', 'target_status']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (_('التعريف'), {
            'fields': ('form_type', 'label', 'target_status', 'description')
        }),
        (_('الحقول'), {
            'fields': ('fields',),
            'description': _('JSON: [{"key":"...", "label":"...", "type":"text|date|select", "required":true}]')
        }),
        (_('المرفقات'), {
            'fields': ('attachments', 'min_documents', 'max_documents'),
        }),
        (_('الحالة'), {
            'fields': ('is_active', 'created_by')
        }),
    )


@admin.register(CustomReportTemplate)
class CustomReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['model_number', 'title', 'report_type', 'category', 'is_active', 'created_at']
    search_fields = ['title', 'category']
    list_filter = ['report_type', 'is_active', 'category']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (_('التعريف'), {
            'fields': ('model_number', 'title', 'report_type')
        }),
        (_('التصنيف'), {
            'fields': ('category', 'parent_section', 'sub_section')
        }),
        (_('الأعمدة والفلترة'), {
            'fields': ('columns', 'base_filter'),
            'description': _('JSON للأعمدة والفلتر')
        }),
        (_('الحالة'), {
            'fields': ('is_active', 'created_by')
        }),
    )
