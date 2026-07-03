<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.geo_tree')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Development Alert -->
      <div class="rounded-2xl border border-blue-100 bg-blue-50/50 p-6 dark:border-blue-900/30 dark:bg-blue-950/20">
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shrink-0">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
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
              استعراض الشجرة الجغرافية العسكرية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              عرض هرمي تفاعلي للشجرة الجغرافية التي تبدأ من مستوى الجمهورية والمحافظات وصولاً للمديريات والعزل والمربعات الأمنية.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              التحكم في النطاقات بالسحب والإفلات
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              توفير واجهة تفاعلية تمكن المدراء من سحب وإعادة هيكلة وتوزيع التبعية الجغرافية لبعض المراكز الأمنية بسهولة وسلاسة.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              تأثير التغييرات على القوى البشرية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              عرض إحصائيات سريعة بجانب كل عقدة في الشجرة الجغرافية توضح أعداد الأفراد المسجلين فيها وتحديثها تلقائياً عند النقل.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              تدقيق التغيرات الجغرافية التاريخية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              الاحتفاظ بسجل تاريخي للتعديلات الجغرافية مثل فصل مديريات أو استحداث مراكز جديدة للرجوع إليها في أي وقت.
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
