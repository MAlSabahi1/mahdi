from django.apps import AppConfig


class SecurityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infra.security'
    label = 'security'
    verbose_name = 'الأمان والصلاحيات'
    
    def ready(self):
        import infra.security.signals  # noqa: F401
