<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.alerts_center')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Development Alert -->
      <div class="rounded-2xl border border-blue-100 bg-blue-50/50 p-6 dark:border-blue-900/30 dark:bg-blue-950/20">
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shrink-0">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-bold text-blue-950 dark:text-blue-200">الشاشة قيد التطوير والتهيئة</h4>
            <p class="text-sm text-blue-700/80 dark:text-blue-300/80 mt-1">
              ملاحظة: هذه الشاشة مصممة كـ هيكل أساسي واقتراح تنظيمي. سيتم ربطها بالخلفية وتخصيصها بالكامل بما يتوافق مع متطلبات النظام الإنتاجي النهائية.
            </p>
          </div>
        </div>
      </div>

      <!-- Main Layout -->
      <div class="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-white/[0.03]">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6">الوظائف والخصائص المقترحة للتطوير المستقبلي:</h3>
        
        <div class="grid gap-6 md:grid-cols-2">
          <!-- Card 1 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              إدارة التنبيهات الفورية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تلقي الإشعارات الفورية عن العمليات الحساسة مثل حذف الحسابات، تغيير كلمات مرور المدراء، أو تعديل البيانات المالية الحرجة.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              مركز الطلبات المعلقة للأنظمة
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تجميع كافة الطلبات التي تحتاج إلى موافقة المدير العام (مثل طلبات التسوية المعلقة، طلبات التعديل خارج الصلاحية).
            </p>
          </div>

          <!-- Card 3 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              التحذيرات الأمنيةTelemetry
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              رصد أي محاولات دخول غير مصرح بها أو عمليات تكرار طلبات مشبوهة، مع ربطها تلقائياً بمركز الاستجابة السريع وجدار الحماية.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              قواعد الإشعارات والبريد
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              إعداد من يستقبل الرسائل القصيرة (SMS) أو رسائل البريد الإلكتروني عند حدوث حالات طوارئ في النظام أو انقطاع في خوادم المهام الخلفية.
            </p>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";

const { t } = useI18n();
</script>
