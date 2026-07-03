<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.general_configs')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Development Alert -->
      <div class="rounded-2xl border border-blue-100 bg-blue-50/50 p-6 dark:border-blue-900/30 dark:bg-blue-950/20">
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shrink-0">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 3m0-3a2 2 0 110 3m-3.793-1.793l-1.414-1.414m1.414 1.414a2 2 0 112.828 2.828m-2.828-2.828a2 2 0 102.828 2.828" />
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
              تهيئة الرتب العسكرية والاختصارات
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تعريف قائمة الرتب المعتمدة (أفراد، ضباط، ضباط صف) وتحديد تسلسلها الهرمي والرموز المقابلة لها وصور شارات الرتب.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              تهيئة الحالات الوظيفية والخدمية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              تحديد حالات الخدمة (على رأس العمل، منتدب، شهيد، متوفى، متقاعد، هارب) والقواعد المالية والإدارية المترتبة على كل حالة.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              تهيئة الفئات والمستويات الوظيفية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              إضافة وتصنيف فئات الموظفين (فني، إداري، مقاتل، مهندس) لتمكين لوحات الإحصائيات من فرز القوات بدقة.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="rounded-xl border border-gray-100 p-5 dark:border-gray-800 bg-gray-50/40 dark:bg-gray-900/30">
            <h5 class="font-bold text-gray-800 dark:text-gray-200 mb-2 flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-blue-500"></span>
              تهيئة المسميات والمناصب القيادية
            </h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              إدخال المناصب الرسمية كـ ثوابت بالنظام (مدير عام، رئيس شعبة، قائد لواء، أخصائي أنظمة) للربط بهيكل الصلاحيات.
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
