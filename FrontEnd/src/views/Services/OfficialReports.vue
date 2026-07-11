<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تصدير التقارير الرسمية والإحصائيات" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            تصدير التقارير الرسمية والإحصائيات
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            توليد وطباعة التقارير الإحصائية والبيانية الرسمية المعتمدة من الوزارة، وتصديرها بصيغ PDF مهيأة للطباعة المباشرة.
          </p>
        </div>

        <!-- Live Counters -->
        <div class="flex gap-5 flex-shrink-0">
          <div class="rounded-2xl border border-blue-200 bg-blue-50 p-4 shadow-theme-xs dark:border-blue-500/20 dark:bg-blue-500/5 text-center min-w-[120px]">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              </div>
              <div class="text-start">
                <p class="text-xs font-medium text-blue-700 dark:text-blue-400">قوالب متاحة</p>
                <h3 class="text-xl font-bold text-blue-900 dark:text-blue-300">4</h3>
              </div>
            </div>
          </div>
          <div class="rounded-2xl border border-warning-200 bg-warning-50 p-4 shadow-theme-xs dark:border-warning-500/20 dark:bg-warning-500/5 text-center min-w-[120px]">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-warning-100 text-warning-600 dark:bg-warning-500/20 dark:text-warning-400">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
              </div>
              <div class="text-start">
                <p class="text-xs font-medium text-warning-700 dark:text-warning-400">صيغة الإخراج</p>
                <h3 class="text-xl font-bold text-warning-900 dark:text-warning-300">PDF</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Parameters Selection Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden lg:col-span-1 flex flex-col">
          <!-- Card Header -->
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400 border border-indigo-100 dark:border-indigo-500/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-bold text-gray-900 dark:text-white">إعدادات ومعايير التقرير</h3>
              <p class="text-[10px] font-medium text-gray-500 dark:text-gray-400 mt-0.5">حدد النموذج والنطاق الزمني والتصنيف الإداري</p>
            </div>
          </div>

          <!-- Card Body -->
          <div class="p-6 space-y-5 flex-1 flex flex-col">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                نموذج التقرير الرسمي <span class="text-error-500">*</span>
              </label>
              <div class="relative">
                <select v-model="selectedTemplate" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent px-4 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">اختر قالباً...</option>
                  <option value="strength">تقرير القوة الفعلية والموجود البشري</option>
                  <option value="promotions">تقرير حركة الترقيات العسكرية الفصلية</option>
                  <option value="deductions">خلاصة الخصومات والعقوبات المالية الشهرية</option>
                  <option value="qualification">توزيع القوة البشرية حسب المؤهلات العلمية</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="h-4 w-4 stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                </span>
              </div>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                التصنيف الإداري
              </label>
              <div class="relative">
                <select v-model="selectedDepartment" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent px-4 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="all">كل الوحدات والإدارات</option>
                  <option value="personnel">الإدارة العامة للأفراد</option>
                  <option value="officers">الإدارة العامة للضباط</option>
                  <option value="ministry">ديوان عام الوزارة</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="h-4 w-4 stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                </span>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                  من تاريخ
                </label>
                <div class="relative">
                  <input type="date" v-model="dateFrom" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent px-4 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800" />
                </div>
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                  إلى تاريخ
                </label>
                <div class="relative">
                  <input type="date" v-model="dateTo" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent px-4 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800" />
                </div>
              </div>
            </div>

            <div class="pt-4 mt-auto">
              <BaseButton 
                @click="generateReport"
                :disabled="!selectedTemplate"
                variant="primary"
                size="lg"
                customClass="w-full rounded-xl font-bold"
              >
                <svg v-if="!isGenerating" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {{ isGenerating ? 'جاري توليد التقرير...' : 'توليد التقرير المعتمد' }}
              </BaseButton>
            </div>
          </div>
        </div>

        <!-- Preview Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden lg:col-span-2 flex flex-col min-h-[420px]">
          <!-- Card Header -->
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex items-center justify-between gap-4">
            <div class="flex items-center gap-4">
              <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-500/30">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <div>
                <h3 class="text-sm font-bold text-gray-900 dark:text-white">معاينة شكل التقرير الرسمي</h3>
                <p class="text-[10px] font-medium text-gray-500 dark:text-gray-400 mt-0.5">المخرجات النهائية بنمط الطباعة الموحد</p>
              </div>
            </div>
            <span class="flex items-center gap-1.5 text-[10px] font-bold text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-gray-800 px-3 py-1.5 rounded-lg font-mono flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              PDF Standard Layout
            </span>
          </div>

          <!-- Preview Body -->
          <div class="flex-1 flex flex-col items-center justify-center p-8">
            <!-- Empty State -->
            <transition name="fade" mode="out-in">
              <div v-if="!selectedTemplate" class="text-center max-w-sm space-y-4" key="empty">
                <div class="flex h-20 w-20 items-center justify-center rounded-2xl bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 mx-auto">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <h4 class="text-sm font-bold text-gray-600 dark:text-gray-300">حدد نموذج التقرير للمعاينة</h4>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 leading-relaxed">
                    اختر نموذج التقرير المطلوب من لوحة الإعدادات الجانبية لتظهر المعاينة هنا.
                  </p>
                </div>
              </div>

              <!-- Template Selected State -->
              <div v-else class="text-center max-w-md space-y-5 w-full" key="ready">
                <div class="flex h-20 w-20 items-center justify-center rounded-2xl bg-brand-50 dark:bg-brand-500/10 text-brand-500 dark:text-brand-400 mx-auto">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 class="text-sm font-bold text-gray-800 dark:text-gray-200">معاينة التقرير جاهزة للتوليد</h4>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 leading-relaxed">
                    تقوم خوادم الطباعة ببناء وتوليد التقرير بتنسيق رسمي ومستند موحد يحتوي على الشعار الرسمي والختم وتوقيع اللجان المعتمدة.
                  </p>
                </div>

                <!-- Selected Template Info Card -->
                <div class="bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700 rounded-xl p-4 text-start mx-auto max-w-sm">
                  <div class="flex items-center gap-3">
                    <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-50 dark:bg-brand-500/10 text-brand-500 dark:text-brand-400 flex-shrink-0">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase">النموذج المحدد</p>
                      <p class="text-xs font-bold text-gray-800 dark:text-gray-200 mt-0.5">{{ templateLabels[selectedTemplate] || selectedTemplate }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Preview Footer Actions -->
          <div v-if="selectedTemplate" class="border-t border-gray-100 dark:border-gray-800 px-6 py-4 flex justify-end gap-3">
            <BaseButton variant="outline" size="sm" customClass="rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              معاينة على الشاشة
            </BaseButton>
            <BaseButton variant="primary" size="sm" customClass="rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              تحميل PDF المعتمد
            </BaseButton>
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
import BaseButton from '@/components/common/BaseButton.vue'
import Swal from 'sweetalert2'

const selectedTemplate = ref('')
const selectedDepartment = ref('all')
const dateFrom = ref('2026-06-01')
const dateTo = ref('2026-06-30')
const isGenerating = ref(false)

const templateLabels: Record<string, string> = {
  strength: 'تقرير القوة الفعلية والموجود البشري',
  promotions: 'تقرير حركة الترقيات العسكرية الفصلية',
  deductions: 'خلاصة الخصومات والعقوبات المالية الشهرية',
  qualification: 'توزيع القوة البشرية حسب المؤهلات العلمية',
}

function generateReport() {
  if (!selectedTemplate.value) return
  isGenerating.value = true
  
  Swal.fire({
    title: 'جاري توليد التقرير الرسمي...',
    html: 'يجري تجميع البيانات من خوادم النظام وإعداد التنسيق التلقائي لـ PDF...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading()
      setTimeout(() => {
        isGenerating.value = false
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
