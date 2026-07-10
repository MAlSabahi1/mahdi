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

@shared_task(bind=True)
def auto_snapshot_task(self):
    """
    مهمة خلفية لأخذ اللقطات الشهرية تلقائياً بناءً على إعدادات النظام.
    """
    try:
        from infra.security.models import SystemSetting
        from django.utils import timezone
        from django.db import transaction
        from django.core.serializers.json import DjangoJSONEncoder
        from django.forms.models import model_to_dict
        import json
        from systems.personnel.models import PersonnelMaster, MonthlySnapshot
        from django.contrib.auth import get_user_model

        setting = SystemSetting.get_value('snapshot_schedule_config')
        if not setting or not setting.get('enabled'):
            logger.info("Auto snapshot is disabled or not configured.")
            return {"status": "skipped", "message": "Auto snapshot disabled"}
        
        schedule_day = int(setting.get('schedule_day', 28))
        
        now = timezone.localtime()
        if now.day != schedule_day:
            return {"status": "skipped", "message": "Not the scheduled day"}
        
        current_month = now.strftime('%Y-%m')
        
        if MonthlySnapshot.objects.filter(snapshot_date=current_month).exists():
            return {"status": "skipped", "message": f"Snapshot for {current_month} already exists."}

        logger.info(f"Starting automatic snapshot generation for {current_month}")

        User = get_user_model()
        system_user = User.objects.filter(is_superuser=True).first()

        active_personnel = PersonnelMaster.objects.all()
        snapshot_records = []
        
        with transaction.atomic():
            for p in active_personnel:
                p_dict = model_to_dict(p)
                from django.db.models.fields.files import FieldFile
                for key, value in p_dict.items():
                    if isinstance(value, FieldFile):
                        p_dict[key] = value.name if value else None
                
                p_json_string = json.dumps(p_dict, cls=DjangoJSONEncoder)
                p_json = json.loads(p_json_string)
                
                unit_name = "غير محدد"
                if getattr(p, 'central_department', None):
                    unit_name = p.central_department.name
                elif getattr(p, 'branch', None):
                    unit_name = p.branch.name
                elif getattr(p, 'district_police', None):
                    unit_name = p.district_police.name
                    
                snapshot = MonthlySnapshot(
                    personnel=p,
                    snapshot_date=current_month,
                    rank=p.current_rank.name if getattr(p, 'current_rank', None) else None,
                    status_name=p.current_status.name if getattr(p, 'current_status', None) else None,
                    unit_name=unit_name,
                    snapshot_data=p_json,
                    created_by=system_user
                )
                snapshot_records.append(snapshot)
                
            MonthlySnapshot.objects.bulk_create(snapshot_records)
            
        logger.info(f"Successfully created auto snapshot for {current_month} with {len(snapshot_records)} records.")
        return {"status": "success", "month": current_month, "total_records": len(snapshot_records)}

    except Exception as e:
        logger.error(f"Error in auto_snapshot_task: {e}")
        self.update_state(state='FAILURE', meta={'status': str(e)})
        raise e
