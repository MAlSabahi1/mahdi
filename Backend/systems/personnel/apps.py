from django.apps import AppConfig


class PersonnelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'systems.personnel'
    label = 'personnel'
    verbose_name = 'إدارة الأفراد'

    def ready(self):
        """تسجيل الـ Signals عند تهيئة التطبيق"""
        import systems.personnel.signals  # noqa: F401 — تفعيل الإشارات
