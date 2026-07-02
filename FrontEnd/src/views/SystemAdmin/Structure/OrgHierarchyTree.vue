<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.org_tree')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Development Alert -->
      <div class="rounded-2xl border border-blue-100 bg-blue-50/50 p-6 dark:border-blue-900/30 dark:bg-blue-950/20">
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shrink-0">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
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
              شجرة القيادة والتشكيلات الإدارية والقتالية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تمثيل هرمي شامل للرتب العسكرية والقطاعات وتوزيع القوات والمجموعات التشغيلية في هيكل تنظيمي واحد موحد.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              إدارة المناصب الشاغرة والقيادية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              رصد وتوزيع أصحاب المناصب القيادية (مثل القادة ومساعديهم) والتنبيه التلقائي في حال شغور منصب أو حدوث تداخل في التكليفات.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              حصر وتوزيع القوة حسب السلاح والتخصص
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تصنيف وتوزيع أعداد الأفراد والمستويات في الشجرة بناءً على تخصصاتهم الفنية (مثل الاتصالات، الإمداد والتموين، العمليات).
            </p>
          </div>

          <!-- Card 4 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              محاكاة إعادة الهيكلة والتنظيم
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              وضع مسودة تعديل على الهيكل ومحاكاة تأثيرها قبل تطبيقها فعلياً على قاعدة بيانات الإنتاج لضمان سلامة سير العمل.
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
