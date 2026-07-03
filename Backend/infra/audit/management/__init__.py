"""
Audit Management Commands
═════════════════════════════════
1. archive_old_logs  — أرشفة سجلات التدقيق القديمة (5+ سنوات)
2. cleanup_expired_logs — حذف السجلات المؤرشفة (10+ سنوات)

الاستخدام:
    python manage.py archive_old_logs --days=1825
    python manage.py cleanup_expired_logs --days=3650
    
Cron (يومياً):
    0 3 * * * cd /app && python manage.py archive_old_logs
    0 4 * * 0 cd /app && python manage.py cleanup_expired_logs
"""
