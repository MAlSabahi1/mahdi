<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تصدير التقارير الرسمية والإحصائيات" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          تصدير التقارير الرسمية (Official Reports Center)
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          توليد وطباعة التقارير الإحصائية والبيانية الرسمية المعمدة من الوزارة، وتصديرها بصيغ PDF مهيأة للطباعة المباشرة.
        </p>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Parameters Selection -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-1 space-y-4">
          <h3 class="text-xs font-black text-gray-900 dark:text-white mb-2">1. إعدادات ومعايير التقرير</h3>
          
          <div>
            <label class="block text-[11px] font-bold text-gray-500 mb-1.5">اختر نموذج التقرير الرسمي</label>
            <select v-model="selectedTemplate" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option value="">اختر قالباً...</option>
              <option value="strength">تقرير القوة الفعلية والموجود البشري</option>
              <option value="promotions">تقرير حركة الترقيات العسكرية الفصلية</option>
              <option value="deductions">خلاصة الخصومات والعقوبات المالية الشهرية</option>
              <option value="qualification">توزيع القوة البشرية حسب المؤهلات العلمية</option>
            </select>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-gray-500 mb-1.5">التصنيف الإداري</label>
            <select class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option>كل الوحدات والإدارات</option>
              <option>الإدارة العامة للأفراد</option>
              <option>الإدارة العامة للضباط</option>
              <option>ديوان عام الوزارة</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-[11px] font-bold text-gray-500 mb-1.5">من تاريخ</label>
              <input type="date" value="2026-06-01" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 mb-1.5">إلى تاريخ</label>
              <input type="date" value="2026-06-30" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300" />
            </div>
          </div>

          <div class="pt-2">
            <button
              @click="generateReport"
              :disabled="!selectedTemplate"
              class="w-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-black py-2.5 rounded-lg transition-colors cursor-pointer shadow-theme-xs"
            >
              توليد التقرير المعمد
            </button>
          </div>
        </div>

        <!-- Preview Placeholders / Layout Preview -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-2 flex flex-col justify-between min-h-[350px]">
          <div class="flex justify-between items-center border-b border-gray-150 dark:border-gray-800 pb-3">
            <h3 class="text-xs font-black text-gray-900 dark:text-white">2. معاينة شكل التقرير الرسمي</h3>
            <span class="text-[9px] bg-gray-50 dark:bg-gray-950 text-gray-400 border border-gray-150 dark:border-gray-800 px-2 py-0.5 rounded font-mono">PDF Standard Layout</span>
          </div>

          <div class="flex-1 flex flex-col items-center justify-center py-8">
            <div class="text-center max-w-sm space-y-3">
              <span class="p-3 bg-gray-50 dark:bg-gray-900 border border-gray-150 dark:border-gray-800 text-gray-400 rounded-2xl inline-block">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </span>
              <h4 class="text-xs font-black text-gray-800 dark:text-gray-200">
                {{ selectedTemplate ? 'معاينة التقرير جاهزة للتوليد' : 'حدد نموذج التقرير من القائمة الجانبية للمعاينة' }}
              </h4>
              <p class="text-[10px] text-gray-450 leading-relaxed">
                تقوم خوادم الطباعة في الباك اند ببناء وتوليد التقرير بتنسيق رسمي ومستند موحد يحتوي على الشعار الرسمي والختم وتوقيع اللجان المعمدة.
              </p>
            </div>
          </div>

          <div v-if="selectedTemplate" class="border-t border-gray-150 dark:border-gray-800 pt-3 flex justify-end gap-2">
            <button class="bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:bg-gray-200 text-gray-700 dark:text-gray-300 text-[10px] font-bold px-4 py-2 rounded-lg cursor-pointer">
              معاينة على الشاشة
            </button>
            <button class="bg-brand-650 hover:bg-brand-700 text-white text-[10px] font-bold px-4 py-2 rounded-lg cursor-pointer">
              تحميل PDF المعمد
            </button>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'

const selectedTemplate = ref('')

function generateReport() {
  if (!selectedTemplate.value) return
  
  Swal.fire({
    title: 'جاري توليد التقرير الرسمي...',
    html: 'يجري تجميع البيانات من خوادم النظام وإعداد التنسيق التلقائي لـ PDF...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading()
      setTimeout(() => {
        Swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'success',
          title: 'اكتمل توليد التقرير بنجاح',
          showConfirmButton: false,
          timer: 3000
        })
      }, 1500)
    }
  })
}
</script>
