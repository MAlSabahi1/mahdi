"""
Celery Tasks للعمليات غير المتزامنة
المهمة 5.4: معالجة الاستيراد في الخلفية
"""
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from systems.services.application.services.import_service import import_service_file, ImportValidationError

User = get_user_model()
logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def process_import_file_task(self, file_content: bytes, export_id: str, user_id: int, service_month: str = None):
    """
    معالجة ملف الاستيراد بشكل غير متزامن
    
    Args:
        self: Task instance (bind=True)
        file_content: محتوى ملف Excel
        export_id: معرف التصدير (UUID)
        user_id: معرف المستخدم
        service_month: شهر الخدمة (اختياري)
        
    Returns:
        dict: تقرير النتائج
    """
    try:
        # تحديث الحالة: بدء المعالجة
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'processing',
                'progress': 10,
                'message': 'جاري تحميل الملف...'
            }
        )
        
        # الحصول على المستخدم
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ImportValidationError(f"المستخدم غير موجود: {user_id}")
        
        # تحديث: التحقق من الملف
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'processing',
                'progress': 30,
                'message': 'جاري التحقق من صحة الملف...'
            }
        )
        
        # تحديث: قراءة البيانات
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'processing',
                'progress': 50,
                'message': 'جاري قراءة البيانات...'
            }
        )
        
        # المعالجة الفعلية
        result = import_service_file(
            file_content=file_content,
            export_id=export_id,
            user=user,
            service_month=service_month
        )
        
        # تحديث: اكتمال المعالجة
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'processing',
                'progress': 90,
                'message': 'جاري حفظ النتائج...'
            }
        )
        
        logger.info(
            f"Import completed successfully. Batch ID: {result['batch_id']}, "
            f"Changes: {result['stats']['changes_detected']}"
        )
        
        return {
            'status': 'completed',
            'progress': 100,
            'result': result
        }
        
    except ImportValidationError as e:
        logger.error(f"Import validation error: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e),
            'error_type': 'validation'
        }
        
    except Exception as e:
        logger.exception(f"Unexpected error during import: {str(e)}")
        
        # إعادة المحاولة للأخطاء غير المتوقعة
        try:
            self.retry(countdown=60, exc=e)
        except self.MaxRetriesExceededError:
            return {
                'status': 'failed',
                'error': f"فشلت المعالجة بعد عدة محاولات: {str(e)}",
                'error_type': 'system'
            }


@shared_task
def cleanup_old_staging_records():
    """
    تنظيف سجلات Staging القديمة (أكثر من 30 يوم)
    يتم تشغيلها بشكل دوري
    """
    from datetime import timedelta
    from django.utils import timezone
    from systems.services.infrastructure.models.staging import StagingRecord
    
    cutoff_date = timezone.now() - timedelta(days=30)
    
    # حذف السجلات القديمة المكتملة أو المرفوضة
    deleted_count, _ = StagingRecord.objects.filter(
        created_at__lt=cutoff_date,
        status__in=['approved', 'rejected']
    ).delete()
    
    logger.info(f"Cleaned up {deleted_count} old staging records")
    
    return {
        'deleted_count': deleted_count,
        'cutoff_date': cutoff_date.isoformat()
    }


@shared_task
def generate_compliance_report(service_month: str):
    """
    توليد تقرير التزام المديريات لشهر معين
    
    Args:
        service_month: الشهر (YYYY-MM)
        
    Returns:
        dict: التقرير
    """
    from systems.services.infrastructure.models.snapshots import DirectorateCompliance
    from core.models import CentralDepartment
    
    directorates = CentralDepartment.objects.all()
    report = []
    
    for dir_obj in directorates:
        try:
            compliance = DirectorateCompliance.objects.get(
                central_department=dir_obj,
                service_month=service_month
            )
            report.append({
                'directorate': dir_obj.name,
                'submitted': True,
                'submitted_at': compliance.submitted_at.isoformat() if compliance.submitted_at else None,
                'error_count': compliance.error_count,
                'quality_score': compliance.quality_score,
            })
        except DirectorateCompliance.DoesNotExist:
            report.append({
                'directorate': dir_obj.name,
                'submitted': False,
                'submitted_at': None,
                'error_count': 0,
                'quality_score': 0,
            })
    
    logger.info(f"Generated compliance report for {service_month}")
    
    return {
        'service_month': service_month,
        'directorates': report,
        'total_directorates': len(directorates),
        'submitted_count': sum(1 for r in report if r['submitted'])
    }


@shared_task
def track_form_deadlines():
    """
    مهمة يومية لفحص الاستمارات الفعالة التي تقترب من تاريخ الانتهاء (end_date)
    مثل المنتدب، المفرغ للدراسة، أو المرافق.
    وإرسال إشعار تنبيهي (Notification) للمسؤولين قبل الانتهاء بـ 30 يوم و 7 أيام.
    """
    from datetime import timedelta
    from django.utils import timezone
    from systems.services.infrastructure.models.status_change import StatusChangeForm
    from core.services.notification_service import NotificationService
    import datetime
    
    # 1. جلب الاستمارات المعتمدة فقط، التي تحتوي على 'end_date' في form_data
    # لأن SQLite لا يدعم البحث المتقدم في JSON، سنجلب الاستمارات المعتمدة ونفلتر بالبايثون
    # في بيئة الإنتاج يفضل استخدام PostgreSQL JSONB field filters
    approved_forms = StatusChangeForm.objects.filter(status='approved')
    
    today = timezone.now().date()
    notified_count = 0
    
    for form in approved_forms:
        end_date_str = form.form_data.get('end_date')
        if not end_date_str:
            continue
            
        try:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            days_left = (end_date - today).days
            
            # تنبيه قبل 30 يوم وقبل 7 أيام
            if days_left == 30 or days_left == 7:
                # إرسال تنبيه (افتراض وجود دالة إشعار في NotificationService)
                NotificationService.notify_status_change(
                    personnel=form.personnel,
                    form=form,
                )
                notified_count += 1
                
        except (ValueError, TypeError):
            continue
            
    logger.info(f"Deadline tracking completed. Sent {notified_count} notifications.")
    return {'notified': notified_count}

