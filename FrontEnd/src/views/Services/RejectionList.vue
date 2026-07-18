<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('services.rejections_title') || 'سجل المرفوضات (Rejections)'" />
    <div class="space-y-6">
      
      <!-- Header Section -->
      <div class="flex justify-end">
        <BaseButton 
          @click="handleExport"
          :disabled="!filters.central_department || !filters.service_month || isExporting"
          :loading="isExporting"
          variant="primary"
          size="sm"
          title="اختر المديرية والشهر لتصدير التقرير"
        >
          <svg v-if="!isExporting" class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          {{ $t('services.export_report') || 'تصدير التقرير' }}
        </BaseButton>
      </div>

      <!-- Filters Section -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <BaseSelect
              v-model="filters.central_department"
              :label="$t('personnel.governorate') || 'المديرية / الإدارة'"
              :options="coreStore.centralDepartments"
              valueKey="id"
              labelKey="name"
              :placeholder="$t('services.all') || 'الكل'"
              @update:modelValue="fetchData(1)"
            />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('services.service_month') || 'شهر الخدمة' }}</label>
            <div class="relative z-20 bg-transparent">
              <input type="month" v-model="filters.service_month" @change="fetchData(1)" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors dark:placeholder:text-white/30 border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 [&::-webkit-calendar-picker-indicator]:opacity-0 [&::-webkit-calendar-picker-indicator]:absolute [&::-webkit-calendar-picker-indicator]:w-full [&::-webkit-calendar-picker-indicator]:h-full [&::-webkit-calendar-picker-indicator]:cursor-pointer [&::-webkit-calendar-picker-indicator]:inset-0">
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="h-5 w-5 stroke-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </span>
            </div>
          </div>
          <div class="flex items-end">
            <BaseButton @click="resetFilters" variant="outline" size="md" customClass="w-full md:w-auto h-11">
              إعادة ضبط الفرز
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div v-if="servicesStore.loading && servicesStore.rejectionsRecords.length === 0" class="flex justify-center p-8">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="servicesStore.rejectionsRecords.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="mb-4 rounded-full bg-gray-50 p-4 dark:bg-gray-800 shadow-theme-xs">
            <svg class="h-10 w-10 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">لا توجد سجلات مرفوضة</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 text-center">لا توجد أي مرفوضات مطابقة للفلاتر المحددة حالياً.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-start">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الفرد</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الشهر</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">سبب الرفض</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">بواسطة (المدير)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">تاريخ الرفض</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="record in servicesStore.rejectionsRecords" :key="record.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td class="px-5 py-4">
                  <div class="flex flex-col">
                    <span class="text-sm font-bold text-gray-900 dark:text-white">{{ record.personnel?.full_name || 'غير معروف' }}</span>
                    <span class="text-xs text-gray-500 dark:text-gray-400 font-mono">{{ record.personnel?.military_number || '-' }}</span>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ record.service_month || '-' }}</span>
                </td>
                <td class="px-5 py-4 max-w-xs">
                  <div class="text-sm text-error-700 dark:text-error-400 bg-error-50 dark:bg-error-500/10 p-2 rounded border border-error-100 dark:border-error-500/20">
                    {{ record.rejection_reason }}
                  </div>
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <div class="flex h-8 w-8 items-center justify-center rounded-full bg-brand-100 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400 text-xs font-bold">
                      {{ record.rejected_by?.username?.substring(0,2).toUpperCase() || 'AD' }}
                    </div>
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ record.rejected_by?.username || 'مدير النظام' }}</span>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <span class="text-sm text-gray-500 dark:text-gray-400" dir="ltr">{{ formatDate(record.rejected_at) }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div v-if="servicesStore.totalPages > 1" class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-900 sm:px-6">
          <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700 dark:text-gray-400">
                عرض <span class="font-medium">{{ ((servicesStore.currentPage - 1) * 20) + 1 }}</span> إلى <span class="font-medium">{{ Math.min(servicesStore.currentPage * 20, servicesStore.totalCount) }}</span> من أصل <span class="font-medium">{{ servicesStore.totalCount }}</span>
              </p>
            </div>
            <div>
              <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm rtl:space-x-reverse" aria-label="Pagination">
                <button @click="changePage(servicesStore.currentPage - 1)" :disabled="servicesStore.currentPage === 1" class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 dark:ring-gray-700 dark:hover:bg-gray-800">
                  <span class="sr-only">السابق</span>
                  <svg class="h-5 w-5 rtl:rotate-180" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clip-rule="evenodd" /></svg>
                </button>
                <button v-for="p in servicesStore.totalPages" :key="p" @click="changePage(p)" :class="[p === servicesStore.currentPage ? 'relative z-10 inline-flex items-center bg-brand-600 px-4 py-2 text-sm font-semibold text-white focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600' : 'relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 dark:text-gray-300 dark:ring-gray-700 dark:hover:bg-gray-800']">
                  {{ p }}
                </button>
                <button @click="changePage(servicesStore.currentPage + 1)" :disabled="servicesStore.currentPage === servicesStore.totalPages" class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 dark:ring-gray-700 dark:hover:bg-gray-800">
                  <span class="sr-only">التالي</span>
                  <svg class="h-5 w-5 rtl:rotate-180" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" /></svg>
                </button>
              </nav>
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
import BaseSelect from '@/components/common/BaseSelect.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useServicesStore } from '@/stores/services'
import { useCoreStore } from '@/stores/core'
import Swal from 'sweetalert2'

const servicesStore = useServicesStore()
const coreStore = useCoreStore()

const filters = ref({
  central_department: null as string | number | null,
  service_month: ''
})

const isExporting = ref(false)

onMounted(async () => {
  if (coreStore.centralDepartments.length === 0) {
    await coreStore.fetchAllReferences()
  }
  fetchData()
})

async function fetchData(page: number = 1) {
  await servicesStore.fetchRejections(page, filters.value)
}

function changePage(page: number) {
  fetchData(page)
}

function resetFilters() {
  filters.value = {
    central_department: null,
    service_month: ''
  }
  fetchData(1)
}

async function handleExport() {
  if (!filters.value.central_department || !filters.value.service_month) {
    Swal.fire('تنبيه', 'يجب اختيار المديرية والشهر لتصدير التقرير', 'warning')
    return
  }
  
  isExporting.value = true
  try {
    await servicesStore.exportRejections(String(filters.value.central_department), filters.value.service_month)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تصدير التقرير بنجاح', showConfirmButton: false, timer: 3000 })
  } catch (err: any) {
    Swal.fire('خطأ', 'فشل تصدير التقرير', 'error')
  } finally {
    isExporting.value = false
  }
}

function formatDate(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ar-EG', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>
