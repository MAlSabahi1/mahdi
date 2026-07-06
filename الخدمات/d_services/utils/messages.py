from django.utils.translation import gettext_lazy as _


class Messages:
    
    LIST_SUCCESS = _('📋 تم جلب قائمة الطلبات بنجاح!')
    DETAIL_SUCCESS = _('📄 تم جلب تفاصيل الطلب بنجاح!')
    UPDATE_SUCCESS = _('✨ رائع! تم تحديث الطلب بنجاح')

    REQUEST_CREATED = _('🎉 تهانينا! تم إنشاء طلبك بنجاح')
    REQUEST_STARTED = _('🚀 انطلقنا! تم بدء معالجة طلبك')
    REQUEST_COMPLETED = _('🏆 مبروك! تم إكمال طلبك بنجاح')
    
    REQUEST_LOCKED = _('🔒 تم قفل الطلب بنجاح')
    REQUEST_UNLOCKED = _('🔓 رائع! تم فتح قفل الطلب')
    
    REQUEST_CANCELLED = _('🛑 تم إلغاء الطلب')
    REQUEST_REJECTED = _(' تم رفض الطلب')
    
    GRANT_ASSIGNED = _('💫 أخبار سارة! تم تعيين المنحة (قيد الانتظار)')
    GRANT_APPROVED = _('🎊 ممتاز! تمت الموافقة على المنحة')
    GRANT_CANCELLED = _('📝 تم إلغاء المنحة بنجاح')
    GRANT_REJECTED = _(' تم رفض المنحة')
    GRANT_UPDATED = _('📝 تم تحديث المنحة بنجاح')
    
    DISCOUNT_ADDED = _('🏷️ تم إضافة الخصم (قيد الانتظار)')
    DISCOUNT_APPROVED = _('✅ تمت الموافقة على الخصم بنجاح')
    DISCOUNT_UPDATED = _('📝 تم تحديث الخصم بنجاح')
    DISCOUNT_CANCELLED = _('🔄 تم إلغاء الخصم بنجاح')
    DISCOUNT_REJECTED = _(' تم رفض الخصم')
    
    STAGE_STARTED = _('🚀 تم بدء العمل على المرحلة')
    STAGE_COMPLETED = _('✅ تم إكمال المرحلة بنجاح')
    STAGE_APPROVED = _('👍 تمت الموافقة على المرحلة')
    STAGE_REJECTED = _(' تم رفض المرحلة')
    STAGE_RETURNED = _('↩️ تم إرجاع المرحلة')
    STAGE_ADVANCED = _('➡️ تم الانتقال للمرحلة التالية')
    
    HINT_GRANT_PENDING = _(' تحتاج موافقة لتفعيل المنحة')
    HINT_DISCOUNT_PENDING = _(' تحتاج موافقة لتفعيل الخصم')
    HINT_CONTACT_ADMIN = _(' تواصل مع مدير النظام')
    HINT_CHECK_STATUS = _(' تحقق من حالة الطلب')
    
    ERROR_NO_PERMISSION = _('⚠️ ليس لديك صلاحية تنفيذ هذا الإجراء')
    ERROR_LOCKED = _('⚠️ الطلب مقفول ولا يمكن تعديله')
    ERROR_INVALID_STATUS = _('⚠️ لا يمكن تنفيذ هذا الإجراء على الطلب الحالي')
    ERROR_NOT_FOUND = _('⚠️ العنصر غير موجود')
    ERROR_REQUIRED_FIELD = _('⚠️ الحقل مطلوب')
