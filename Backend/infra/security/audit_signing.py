"""
Audit Signing — التوقيع الرقمي لسجلات التدقيق
═══════════════════════════════════════════════════
⚠️  التوقيع أصبح مدمجاً في AuditLog.compute_signature() و AuditLog.verify()
    هذا الملف يُعيد تصدير الدوال للتوافق الخلفي.

    الاستخدام الجديد:
        from infra.audit.models import AuditLog
        log = AuditLog.objects.get(pk=1)
        log.verify()  # True/False
"""
import hmac
import hashlib
import json
from django.conf import settings


def _get_signing_key() -> bytes:
    """جلب مفتاح التوقيع."""
    key = getattr(settings, 'AUDIT_SIGNING_KEY', None) or settings.SECRET_KEY
    return key.encode('utf-8')


def _canonicalize(value) -> str:
    """تحويل القيمة إلى نص ثابت الترتيب."""
    if value is None:
        return 'null'
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True, ensure_ascii=False,
                         separators=(',', ':'))
    return str(value)


def compute_signature(audit_record) -> str:
    """
    حساب توقيع HMAC-SHA256 لسجل التدقيق.
    ⚠️ يُفضل استخدام: audit_record.compute_signature()
    """
    return audit_record.compute_signature()


def verify_signature(audit_record) -> bool:
    """
    التحقق من صحة توقيع سجل التدقيق.
    ⚠️ يُفضل استخدام: audit_record.verify()
    """
    return audit_record.verify()


def verify_all_signatures(queryset=None) -> dict:
    """التحقق من جميع توقيعات سجلات التدقيق."""
    from infra.audit.models import AuditLog

    if queryset is None:
        queryset = AuditLog.objects.all()

    result = {
        'total': 0,
        'valid': 0,
        'tampered': 0,
        'unsigned': 0,
        'tampered_ids': [],
    }

    for record in queryset.iterator():
        result['total'] += 1
        if not record.signature:
            result['unsigned'] += 1
        elif record.verify():
            result['valid'] += 1
        else:
            result['tampered'] += 1
            result['tampered_ids'].append(record.pk)

    return result
