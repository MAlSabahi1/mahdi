<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="واجهة تقديم الطلب الموحدة" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Premium Under Development banner -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-3xl p-12 text-center shadow-theme-xs max-w-2xl mx-auto space-y-5">
        
        <span class="p-4 bg-brand-50 text-brand-650 dark:bg-brand-950/40 dark:text-brand-400 rounded-2xl inline-block shadow-theme-xs">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </span>

        <div class="space-y-2">
          <h2 class="text-lg font-black text-gray-900 dark:text-white">
            واجهة تقديم الطلب الموحدة
          </h2>
          <p class="text-xs text-gray-400 font-bold">
            (النموذج المرن ورفع المرفقات الإلزامية)
          </p>
        </div>

        <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed max-w-md mx-auto">
          يجري حالياً دمج وضبط محرك الحقول المرنة والتحقق الأمني من سلامة المرفقات وصيغها لمنع الاختراقات وهندسة الثغرات. سيتم إطلاق الواجهة فور الانتهاء من مراجعة خيارات الرفع المشفرة.
        </p>

        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400 text-[10px] font-bold">
          <span class="h-1.5 w-1.5 rounded-full bg-amber-500 animate-pulse"></span>
          قيد التطوير والربط البرمجي
        </div>

        <div class="pt-4 border-t border-gray-100 dark:border-gray-850">
          <RouterLink 
            to="/services/directory" 
            class="text-xs font-bold text-brand-600 hover:underline"
          >
            ← العودة لدليل كروت الخدمات المعتمدة
          </RouterLink>
        </div>

      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
</script>
