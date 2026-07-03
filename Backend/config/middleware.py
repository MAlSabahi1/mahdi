"""
Governorate Middleware
لإدارة تعدد المحافظات (Multi-Tenancy) في الواجهة الخلفية
"""
from threading import local

_thread_locals = local()

def get_current_governorate():
    """الحصول على معرف المحافظة الحالية من الذاكرة المحلية للـ Thread"""
    return getattr(_thread_locals, 'governorate_id', None)

class GovernorateMiddleware:
    """
    يقرأ المحافظة الحالية للمستخدم من ملفه ويخزنها في مساحة Thread
    لاستخدامها لاحقاً في فلترة البيانات دون الحاجة لتمرير request لكل مكان
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                profile = getattr(request.user, 'profile', None)
                if profile:
                    _thread_locals.governorate_id = profile.governorate_id
                else:
                    _thread_locals.governorate_id = None
            except Exception:
                _thread_locals.governorate_id = None
        else:
            _thread_locals.governorate_id = None

        response = self.get_response(request)
        
        # تنظيف الذاكرة بعد الاستجابة لمنع تسرب البيانات بين الطلبات
        if hasattr(_thread_locals, 'governorate_id'):
            del _thread_locals.governorate_id
            
        return response
