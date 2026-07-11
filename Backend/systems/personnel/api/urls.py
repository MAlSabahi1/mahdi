"""
Personnel URLs - مسارات API الأفراد
═══════════════════════════════════════════════

📌 ملاحظات لمطوّر الفرونت إند:
────────────────────────────────────

🔷 GET /api/v1/personnel/
   قائمة الأفراد (فلترة + بحث + pagination)
   Filters: ?directorate=1&current_rank=3&current_status=2&governorate=1
   Search: ?search=أحمد
   Ordering: ?ordering=-military_number

🔷 GET /api/v1/personnel/{military_number}/
   تفاصيل فرد (كل الحقول + properties محسوبة)

🔷 POST /api/v1/personnel/
   إنشاء فرد جديد (يتطلب صلاحية edit_personnel_basic)

🔷 PUT/PATCH /api/v1/personnel/{military_number}/
   تحديث بيانات (صلاحيات ABAC)

🔷 GET /api/v1/personnel/check-national-id/?value=01234567890&exclude=7348799
   ← فحص فوري للرقم الوطني (استخدمه أثناء الكتابة - debounce 300ms)
   ← يُرجع: { valid_format, exists, owner? }
   ⚠️ Frontend: أضف confirm dialog عند exists=true

🔷 POST /api/v1/personnel/{military_number}/update-national-id/
   ← Body: { "national_id": "01234567890", "document_ids": [5, 6] }
   ← المسؤول (مدير/رئيس خدمات): تحديث مباشر
   ← المستخدم العادي: ينشئ طلب تصحيح
   ⚠️ Frontend: يجب رفع صورة البطاقة (أمام + خلف) قبل الإرسال
   ⚠️ Frontend: أضف إدخال مزدوج (كتابة الرقم مرتين للتأكد)

🔷 GET /api/v1/personnel/corrections/
   قائمة طلبات التصحيح

🔷 POST /api/v1/personnel/corrections/bulk-create/
   ← رفع تصحيحات أسماء جماعية (نموذج 23)
   ← Body: { "corrections": [{"military_number": "7348799", "new_name": "..."}] }

🔷 POST /api/v1/personnel/corrections/{id}/approve/
   ← موافقة على طلب تصحيح فردي (يتطلب document أو document_ids)

🔷 POST /api/v1/personnel/corrections/{id}/reject/
   ← رفض طلب تصحيح

🔷 GET /api/v1/personnel/corrections/needs-correction/
   ← قائمة الأفراد الذين لديهم corrected_name (بانتظار التصحيح)

🔷 GET/POST /api/v1/personnel/rank-settlements/
   ← إنشاء طلب تسوية رتبة (ترقية ضمن صنف / فرد→ضابط / تخفيض)
   ← settlement_type: same_class_promotion | personnel_to_officer | demotion

🔷 POST /api/v1/personnel/rank-settlements/{id}/apply/
   ← تطبيق التسوية فعلياً على الفرد

🔷 POST /api/v1/personnel/rank-settlements/{id}/reject/
   ← رفض طلب التسوية

📌 ملاحظات سلوك الترابط الذكي (Position↔JobTitle↔Category):
────────────────────────────────────────────────────────────
1. عند اختيار job_title → category تتعبأ تلقائياً (Backend: save() auto-fill)
2. عند اختيار position → تحقق من allowed_categories (Backend: clean() validation)
3. لا يمكن تغيير job_title أثناء وجود منصب (Backend: clean() يمنع)
4. ⚠️ Frontend: عطّل حقل job_title عندما position مختار
5. ⚠️ Frontend: عند اختيار job_title أولاً → فلتر المناصب المتوافقة
6. ⚠️ Frontend: category = readonly (تتحدد تلقائياً — لا تسمح بالتعديل اليدوي)
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views.reports_views import WorkforceSummaryReportView, HierarchicalWorkforceView

router = DefaultRouter()
router.register(r'corrections', views.SuggestedCorrectionViewSet, basename='suggested-corrections')
router.register(r'rank-settlements', views.RankSettlementViewSet, basename='rank-settlements')
router.register(r'', views.PersonnelViewSet, basename='personnel')

urlpatterns = [
    path('reports/workforce-summary/', WorkforceSummaryReportView.as_view(), name='reports-workforce-summary'),
    path('reports/hierarchical-workforce/', HierarchicalWorkforceView.as_view(), name='reports-hierarchical-workforce'),
    path('legacy-import/', views.LegacyImportView.as_view(), name='legacy-import'),
    path('rank-settlement/', views.RankSettlementView.as_view(), name='rank-settlement'),
    path('check-national-id/', views.CheckNationalIdView.as_view(), name='check-national-id'),
    path('<str:military_number>/update-national-id/', views.UpdateNationalIdView.as_view(), name='update-national-id'),
    path('schema/', views.PersonnelViewSet.as_view({'get': 'schema'}), name='personnel-schema'),
    path('', include(router.urls)),
]
