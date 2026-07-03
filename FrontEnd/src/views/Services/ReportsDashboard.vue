<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('services.reports_title') || 'التقارير والإقفال الشهري'" />
    <div class="space-y-6">
      
      <!-- Danger Zone: Close Month -->
      <div class="flex justify-end">
        <button 
          @click="handleCloseMonth"
          :disabled="servicesStore.loading"
          class="flex items-center gap-2 rounded-lg bg-error-600 px-5 py-2 text-sm font-bold text-white shadow-theme-xs hover:bg-error-500 focus:outline-none focus:ring-2 focus:ring-error-500 focus:ring-offset-2 transition-colors disabled:opacity-50 cursor-pointer"
        >
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          {{ $t('services.close_month') || 'إقفال الشهر الحالي' }}
        </button>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        
        <!-- Reports Generator Card (Left Side) -->
        <div class="lg:col-span-1 space-y-6">
          <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
            <div class="border-b border-gray-100 bg-gray-50/50 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/50 flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-100 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400">
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">توليد التقارير الختامية</h3>
              </div>
            </div>
            
            <div class="p-6 space-y-5 flex-1">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نوع التقرير <span class="text-error-500">*</span></label>
                <div class="relative">
                  <select v-model="reportForm.templateId" class="block w-full appearance-none rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
                    <option value="" disabled>اختر التقرير</option>
                    <option v-for="tpl in servicesStore.reportTemplates" :key="tpl.id" :value="tpl.id">{{ tpl.name }}</option>
                  </select>
                  <span class="pointer-events-none absolute inset-y-0 ltr:right-0 rtl:left-0 flex items-center px-4 text-gray-500">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">صيغة الملف <span class="text-error-500">*</span></label>
                <div class="flex gap-4 mt-2">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="reportForm.format" value="pdf" class="h-4 w-4 text-brand-600 border-gray-300 focus:ring-brand-500">
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">PDF</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="reportForm.format" value="excel" class="h-4 w-4 text-success-600 border-gray-300 focus:ring-success-500">
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Excel</span>
                  </label>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">تصفية بالشهر</label>
                <input type="month" v-model="reportForm.month" class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500" />
              </div>
              
              <div class="pt-4 mt-auto">
                <button 
                  @click="handleGenerateReport" 
                  :disabled="!reportForm.templateId || isGenerating"
                  class="w-full flex justify-center items-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
                >
                  <svg v-if="isGenerating" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                  <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                  توليد التقرير
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Compliance Table (Right Side) -->
        <div class="lg:col-span-2">
          <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden h-full flex flex-col">
            <div class="border-b border-gray-100 bg-gray-50/50 px-6 py-4 dark:border-gray-800 dark:bg-gray-800/50 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-gray-900 dark:text-white">حالة امتثال المديريات</h3>
                  <p class="text-xs text-gray-500 dark:text-gray-400">تتبع من التزم بالتسليم في الوقت المحدد.</p>
                </div>
              </div>
              <div>
                <input type="month" v-model="complianceMonth" @change="fetchCompliance" class="block rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white" />
              </div>
            </div>
            
            <div class="flex-1 overflow-x-auto">
              <table class="w-full text-start h-full">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                    <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">المديرية / الإدارة</th>
                    <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">حالة التسليم</th>
                    <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">نسبة التعديل</th>
                    <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">تاريخ التسليم</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
                  <tr v-if="servicesStore.loading && servicesStore.complianceRecords.length === 0">
                    <td colspan="4" class="px-5 py-12 text-center">
                      <svg class="h-8 w-8 animate-spin mx-auto text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                    </td>
                  </tr>
                  <tr v-else-if="servicesStore.complianceRecords.length === 0">
                    <td colspan="4" class="px-5 py-12 text-center text-gray-500">لا توجد بيانات لهذا الشهر.</td>
                  </tr>
                  <tr v-for="record in servicesStore.complianceRecords" :key="record.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                    <td class="px-5 py-3 text-sm font-bold text-gray-900 dark:text-white">
                      {{ record.central_department?.name || 'غير معروف' }}
                    </td>
                    <td class="px-5 py-3">
                      <span v-if="record.status === 'compliant'" class="inline-flex items-center rounded-full bg-success-50 px-2 py-1 text-xs font-medium text-success-700 ring-1 ring-inset ring-success-600/20 dark:bg-success-500/10 dark:text-success-400 dark:ring-success-500/20">
                        سلم بالوقت
                      </span>
                      <span v-else-if="record.status === 'late'" class="inline-flex items-center rounded-full bg-warning-50 px-2 py-1 text-xs font-medium text-warning-700 ring-1 ring-inset ring-warning-600/20 dark:bg-warning-500/10 dark:text-warning-400 dark:ring-warning-500/20">
                        تأخير
                      </span>
                      <span v-else class="inline-flex items-center rounded-full bg-error-50 px-2 py-1 text-xs font-medium text-error-700 ring-1 ring-inset ring-error-600/20 dark:bg-error-500/10 dark:text-error-400 dark:ring-error-500/20">
                        لم يسلم
                      </span>
                    </td>
                    <td class="px-5 py-3 text-sm text-gray-700 dark:text-gray-300">
                      {{ record.change_percentage || '0' }}%
                    </td>
                    <td class="px-5 py-3 text-sm text-gray-500 dark:text-gray-400" dir="ltr">
                      {{ record.submission_date ? formatDate(record.submission_date) : '-' }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'
import Swal from 'sweetalert2'

const servicesStore = useServicesStore()

const complianceMonth = ref('')
const isGenerating = ref(false)

const reportForm = ref({
  templateId: '',
  format: 'pdf',
  month: ''
})

onMounted(async () => {
  // Set current month as default for compliance
  const now = new Date()
  const monthStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  complianceMonth.value = monthStr
  
  await fetchCompliance()
  await servicesStore.fetchReportTemplates()
})

async function fetchCompliance() {
  await servicesStore.fetchCompliance(complianceMonth.value)
}

async function handleGenerateReport() {
  if (!reportForm.value.templateId) return
  
  isGenerating.value = true
  try {
    const filters = reportForm.value.month ? { month: reportForm.value.month } : {}
    await servicesStore.generateReport(Number(reportForm.value.templateId), reportForm.value.format, filters)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تحميل التقرير', showConfirmButton: false, timer: 3000 })
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل توليد التقرير', 'error')
  } finally {
    isGenerating.value = false
  }
}

async function handleCloseMonth() {
  const result = await Swal.fire({
    title: 'تأكيد إقفال الشهر؟',
    text: "تحذير: إقفال الشهر سيمنع أي تعديلات إضافية على كشوفات الشهر الحالي وسيقوم بحفظها كنسخة مؤرشفة نهائية. هذا الإجراء لا يمكن التراجع عنه بسهولة.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'نعم، إقفال الشهر',
    cancelButtonText: 'إلغاء'
  })

  if (result.isConfirmed) {
    try {
      await servicesStore.closeMonth()
      Swal.fire(
        'تم الإقفال!',
        'تم إقفال الشهر بنجاح وأرشفة الكشوفات.',
        'success'
      )
    } catch (err: any) {
      Swal.fire('خطأ', servicesStore.error || 'فشل الإقفال', 'error')
    }
  }
}

function formatDate(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ar-EG', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric'
  }).format(date)
}
</script>
