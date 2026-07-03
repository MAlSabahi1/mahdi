"""
جسر لمهام Celery لتتوافق مع الاكتشاف التلقائي لـ Django
"""
from .application.tasks import process_legacy_import_task

__all__ = ['process_legacy_import_task']

