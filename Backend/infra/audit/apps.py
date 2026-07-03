"""Audit App Configuration — نظام التدقيق المركزي."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infra.audit'
    label = 'audit'
    verbose_name = _('نظام التدقيق والمراقبة')

    def ready(self):
        pass
