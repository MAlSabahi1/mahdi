from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'version', 'uploaded_by', 'created_at', 'integrity_badge']
    search_fields = ['description', 'file_hash']
    list_filter = ['version', 'created_at']
    readonly_fields = ['file_hash', 'created_at', 'updated_at']
    
    def integrity_badge(self, obj):
        if obj.verify_integrity():
            return format_html('<span style="color: green;">✓ سليم</span>')
        return format_html('<span style="color: red;">✗ معطوب</span>')
    integrity_badge.short_description = _('سلامة الملف')
