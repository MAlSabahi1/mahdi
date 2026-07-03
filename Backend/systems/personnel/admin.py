"""
Personnel Admin - واجهة الإدارة للأفراد
═══════════════════════════════════════════
فلترة ديناميكية: عند اختيار إدارة أمن المحافظة →
  الإدارات المركزية / الفروع / شرطة المديريات تُفلتر عبر JavaScript.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    PersonnelMaster, RawDataImport, SuggestedCorrection,
    HistoricalMonthlyVariables
)
from core.models import CentralDepartment, Branch, DistrictPolice


@admin.register(PersonnelMaster)
class PersonnelMasterAdmin(admin.ModelAdmin):
    list_display = [
        'military_number', 'full_name', 'current_rank',
        'security_admin', 'central_department', 'current_status', 'is_complete',
        'is_data_clean', 'data_quality_score'
    ]
    search_fields = ['military_number', 'full_name', 'national_id']
    list_filter = [
        'security_admin', 'central_department',
        'current_status', 'current_rank',
        'is_complete', 'is_data_clean'
    ]
    # security_admin = select عادي (22 خيار فقط — لا يحتاج autocomplete)
    # central_department / branch / district_police = select عادي (يُفلتر بـ JS)
    autocomplete_fields = [
        'current_rank', 'current_status',
        'qualification', 'pending_rank',
    ]
    raw_id_fields = ['division', 'unit']
    readonly_fields = ['created_at', 'updated_at', 'age', 'service_years']

    class Media:
        js = ('personnel/js/org_filter.js',)

    fieldsets = (
        (_('الهوية'), {
            'fields': ('military_number', 'old_military_number', 'national_id', 'full_name')
        }),
        (_('البيانات الشخصية'), {
            'fields': ('birth_date', 'join_date', 'phone_number', 'qualification')
        }),
        (_('البيانات الحيوية'), {
            'fields': ('photo', 'fingerprint_hash'),
            'classes': ('collapse',)
        }),
        (_('الهيكل التنظيمي'), {
            'fields': ('security_admin', 'central_department', 'branch', 'district_police', 'division', 'unit'),
            'description': 'اختر إدارة أمن المحافظة أولاً ← ثم ستُفلتر الإدارات والفروع والمديريات تلقائياً.'
        }),
        (_('الحالة والرتبة'), {
            'fields': ('current_rank', 'current_status', 'force_classification')
        }),
        (_('التوصيف الوظيفي'), {
            'fields': ('job_title', 'category', 'position')
        }),
        (_('المرحلة 1.5 - معالجة البيانات'), {
            'fields': (
                'pending_rank',
                'is_data_clean', 'data_quality_score', 'notes'
            ),
            'classes': ('collapse',)
        }),
        (_('بيانات إضافية'), {
            'fields': (
                'expense_status', 'appointment_info',
                'decision_date', 'transfer_date',
            ),
            'classes': ('collapse',)
        }),
        (_('معلومات النظام'), {
            'fields': ('is_complete', 'created_at', 'updated_at', 'age', 'service_years'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """فلترة server-side عند التعديل (للتحميل الأولي)"""
        sa_id = request.POST.get('security_admin')

        if not sa_id and hasattr(request, 'resolver_match') and request.resolver_match:
            try:
                obj_id = request.resolver_match.kwargs.get('object_id')
                if obj_id:
                    obj = PersonnelMaster.objects.only('security_admin_id').get(pk=obj_id)
                    sa_id = obj.security_admin_id
            except Exception:
                pass

        if sa_id:
            if db_field.name == 'central_department':
                kwargs['queryset'] = CentralDepartment.objects.filter(
                    security_admin_id=sa_id
                ).order_by('order', 'name')
            elif db_field.name == 'branch':
                kwargs['queryset'] = Branch.objects.filter(
                    security_admin_id=sa_id
                ).order_by('order', 'name')
            elif db_field.name == 'district_police':
                kwargs['queryset'] = DistrictPolice.objects.filter(
                    security_admin_id=sa_id
                ).order_by('order', 'name')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(RawDataImport)
class RawDataImportAdmin(admin.ModelAdmin):
    list_display = ['row_index', 'import_batch_id', 'status', 'created_at']
    search_fields = ['import_batch_id', 'error_message']
    list_filter = ['status', 'import_batch_id', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('معلومات الصف'), {
            'fields': ('row_index', 'import_batch_id', 'status')
        }),
        (_('البيانات'), {
            'fields': ('raw_data', 'error_message')
        }),
        (_('التوقيت'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SuggestedCorrection)
class SuggestedCorrectionAdmin(admin.ModelAdmin):
    """
    واجهة إدارة اقتراحات التصحيح — للقراءة وإدارة النطاق فقط.
    ══════════════════════════════════════════════════════════
    ⚠️  قرارات الموافقة/الرفض تتم حصراً عبر API (PersonnelService).
    ⚠️  هذه الواجهة للمراقبة والتدقيق فقط.
    ══════════════════════════════════════════════════════════
    """
    list_display = [
        'personnel_link', 'correction_type', 'field_name',
        'old_value_short', 'new_value_short',
        'status_badge', 'has_document_icon',
        'requires_doc_icon', 'requested_by', 'requested_at',
        'security_admin',
    ]
    search_fields = [
        'personnel__military_number',
        'personnel__full_name',
        'old_value',
        'new_value',
        'requested_by__username',
    ]
    list_filter = [
        'correction_type',
        'status',
        'security_admin',
        ('requested_at', admin.DateFieldListFilter),
    ]
    date_hierarchy = 'requested_at'

    # ── جميع الحقول للقراءة فقط (لا تعديل من Admin) ──
    readonly_fields = [
        'personnel', 'security_admin',
        'correction_type', 'field_name',
        'old_value', 'new_value',
        'status', 'supporting_document_preview',
        'supporting_document',
        'requested_by', 'requested_at',
        'reviewed_by', 'reviewed_at',
        'rejection_reason',
        'created_at', 'updated_at',
        'requires_document', 'document_description',
    ]

    # لا توجد أي actions (منع الموافقة/الرفض من Admin)
    actions = None

    fieldsets = (
        (_('بيانات الفرد والتصحيح'), {
            'fields': (
                'personnel', 'security_admin',
                'correction_type', 'field_name', 'status',
            )
        }),
        (_('القيم (القديمة والجديدة)'), {
            'fields': ('old_value', 'new_value')
        }),
        (_('المستند الداعم'), {
            'fields': (
                'supporting_document',
                'supporting_document_preview',
                'requires_document',
                'document_description',
            ),
            'description': (
                '⚠️ تصحيح الاسم يتطلب نموذج 23 أو صورة البطاقة — '
                'وفق الدليل الإرشادي البند 8'
            ),
        }),
        (_('بيانات المراجعة'), {
            'fields': (
                'requested_by', 'requested_at',
                'reviewed_by', 'reviewed_at',
                'rejection_reason',
            )
        }),
        (_('معلومات النظام'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # ── منع أي تعديل كامل من Admin ──
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        """
        القراءة فقط — لا تعديل.
        السوبر يوزر يمكنه التصحيح الطارئ لـ rejection_reason فقط.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """لا حذف — السجلات التدقيقية دائمة."""
        return False

    def get_queryset(self, request):
        """
        فلترة النطاق الأمني:
        - السوبر يوزر يرى الكل.
        - باقي المستخدمين يرون نطاق إدارة الأمن الخاصة بهم فقط.
        - الأفراد المحذوفون ناعماً لا يظهرون.
        """
        qs = super().get_queryset(request).select_related(
            'personnel', 'security_admin',
            'requested_by', 'reviewed_by',
            'supporting_document',
        ).filter(
            personnel__is_deleted=False,
        )

        if request.user.is_superuser:
            return qs

        # فلترة حسب إدارة الأمن للمستخدم
        try:
            user_sa = request.user.userprofile.security_admin
            if user_sa:
                return qs.filter(security_admin=user_sa)
        except AttributeError:
            pass

        return qs.none()

    # ══ حقول مخصصة للعرض ══

    @admin.display(description=_('الفرد'), ordering='personnel__full_name')
    def personnel_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        if not obj.personnel:
            return '—'
        url = reverse(
            'admin:personnel_personnelmaster_change',
            args=[obj.personnel.military_number]
        )
        return format_html(
            '<a href="{}">{} — {}</a>',
            url,
            obj.personnel.military_number,
            obj.personnel.full_name,
        )

    @admin.display(description=_('الحالة'))
    def status_badge(self, obj):
        from django.utils.html import format_html
        colors = {
            'pending': '#f59e0b',
            'approved': '#10b981',
            'rejected': '#ef4444',
        }
        labels = {
            'pending': 'معلق',
            'approved': 'موافق',
            'rejected': 'مرفوض',
        }
        color = colors.get(obj.status, '#6b7280')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:4px;font-weight:bold">{}</span>',
            color, label,
        )

    @admin.display(description=_('القيمة القديمة'))
    def old_value_short(self, obj):
        v = obj.old_value or '—'
        return v[:50] + '...' if len(v) > 50 else v

    @admin.display(description=_('القيمة الجديدة'))
    def new_value_short(self, obj):
        v = obj.new_value or '—'
        return v[:50] + '...' if len(v) > 50 else v

    @admin.display(description=_('مرفق؟'), boolean=True)
    def has_document_icon(self, obj):
        return obj.supporting_document_id is not None

    @admin.display(description=_('إلزامي؟'), boolean=True)
    def requires_doc_icon(self, obj):
        return obj.requires_document

    @admin.display(description=_('معاينة المستند'))
    def supporting_document_preview(self, obj):
        from django.utils.html import format_html
        if not obj.supporting_document_id:
            return format_html(
                '<span style="color:#ef4444">⚠️ لا يوجد مستند مرفق</span>'
            )
        doc = obj.supporting_document
        label = getattr(doc, 'original_filename', None) or str(doc)
        return format_html(
            '<strong style="color:#10b981">✅ {}</strong>',
            label,
        )

    @admin.display(description=_('وصف المرفق المطلوب'))
    def document_description(self, obj):
        return obj.document_description or '—'

    class Media:
        css = {
            'all': ('admin/css/suggested_correction.css',)
        }



@admin.register(HistoricalMonthlyVariables)
class HistoricalMonthlyVariablesAdmin(admin.ModelAdmin):
    list_display = ['personnel', 'month', 'variable_value', 'source_column', 'created_at']
    search_fields = ['personnel__military_number', 'personnel__full_name', 'variable_value']
    list_filter = ['month', 'source_column', 'created_at']
    autocomplete_fields = ['personnel']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('معلومات المتغير'), {
            'fields': ('personnel', 'month', 'source_column')
        }),
        (_('القيمة'), {
            'fields': ('variable_value', 'notes')
        }),
        (_('التوقيت'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
