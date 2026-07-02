<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.analytics_dashboard')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Development Alert -->
      <div class="rounded-2xl border border-blue-100 bg-blue-50/50 p-6 dark:border-blue-900/30 dark:bg-blue-950/20">
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shrink-0">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-bold text-blue-950 dark:text-blue-200">الشاشة قيد التطوير والتهيئة</h4>
            <p class="text-sm text-blue-700/80 dark:text-blue-300/80 mt-1">
              <strong>تنبيه هام جداً:</strong> إن كافة الميزات والخصائص والبيانات المذكورة في هذه الشاشة هي <strong>مقترحات وتصاميم توجيهية فقط</strong>، ويتم تطويعها وتخصيصها بدقة تامة طبقاً لمتطلبات وتفاصيل النظام الإنتاجي الفعلية.
            </p>
          </div>
        </div>
      </div>

      <!-- Main Layout -->
      <div class="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-white/[0.03]">
        <div class="mb-6 border-b border-gray-150 dark:border-gray-800 pb-4">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">طبيعة ودور هذه الشاشة في النظام:</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-2 leading-relaxed">
            هي <strong>الشاشة الجامعة</strong> التي تعرض الإحصائيات الكلية العميقة والخرائط التحليلية لكامل قاعدة البيانات (مثل: إجمالي القوة البشرية، نسبة الضباط للأفراد، أعداد الأفراد الموزعين على المحافظات، وحجم القوات في كل قطاع وإدارة). تمنح الإدارة العليا نظرة عامة وشاملة على النظام بأكمله ومراقبة تكامل الأنظمة.
          </p>
        </div>

        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">الوظائف والخصائص المقترحة للتطوير المستقبلية:</h3>
        
        <div class="grid gap-6 md:grid-cols-2">
          <!-- Card 1 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              الإحصائيات الكلية العميقة
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              عرض إجمالي القوة البشرية المفصلة، نسب توزيع الضباط إلى الأفراد، توزيع الرتب على مستوى القطاعات المختلفة.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              التوزيع الجغرافي والإداري للقوات
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              مخططات بيانية دائرية وخرائط تفاعلية توضح تركيز أعداد الأفراد في كل محافظة أو إدارة أو فرع إقليمي بشكل لحظي.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              مقارنة وتكامل نشاط الفروع
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تحليل دورات الكشوفات وتدفق المراسلات ومعدلات تسليم البيانات الشهرية بين المحافظات لقياس الكفاءة الكلية.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              استعلامات مخصصة للإدارة العليا
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تصفية وتقاطعات متعددة للبيانات (فرز برتبة معينة + محافظة معينة + حالة الخدمة) وتصدير النتائج فوراً.
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
