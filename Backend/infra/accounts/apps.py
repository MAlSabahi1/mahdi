"""
Accounts App Configuration
═══════════════════════════
تطبيق إدارة الهوية والمستخدمين — Identity Infrastructure.
يجمع كل ما يتعلق بالمستخدم: الهوية، الجلسات، الأمان، المصادقة.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infra.accounts'
    label = 'accounts'
    verbose_name = _('إدارة المستخدمين')
