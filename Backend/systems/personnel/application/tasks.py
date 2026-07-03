import os
from celery import shared_task
from django.core.management import call_command
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_legacy_import_task(self, file_path, dry_run=True):
    """
    معالجة ملفات الإكسل الخام (Legacy Data) في الخلفية باستخدام Celery.
    تقوم بتشغيل أمر الإدارة import_legacy_data.
    """
    try:
        self.update_state(state='PROGRESS', meta={'progress': 10, 'status': 'بدء قراءة الملف...'})
        logger.info(f"Starting legacy import task for file {file_path}. Dry-run: {dry_run}")
        
        # إعداد المعاملات
        args = [file_path]
        kwargs = {}
        if dry_run:
            kwargs['dry_run'] = True

        # تشغيل الأمر (مخرجات الأمر سيتم تسجيلها/تجاهلها في الخلفية)
        call_command('import_legacy_data', *args, **kwargs)

        self.update_state(state='SUCCESS', meta={'progress': 100, 'status': 'تم الاستيراد/الفحص بنجاح'})
        
        return {"status": "success", "dry_run": dry_run, "message": "اكتمل بنجاح"}

    except Exception as e:
        logger.error(f"Error in legacy import task: {e}")
        self.update_state(state='FAILURE', meta={'progress': 0, 'status': f'حدث خطأ: {str(e)}'})
        raise e
    finally:
        # تنظيف الملف الخارجي دائماً لتجنب استنزاف المساحة
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                logger.error(f"Failed to remove temp file {file_path}: {cleanup_error}")
