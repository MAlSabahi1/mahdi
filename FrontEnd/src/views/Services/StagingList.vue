<template>
  <admin-layout>
    <div class="space-y-6">
      
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('services.staging_title') || 'مراجعة الاعتمادات (Staging)' }}</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t('services.staging_subtitle') || 'مراجعة التعديلات المقترحة القادمة من كشوفات الإكسل المستوردة للموافقة عليها أو رفضها.' }}
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="fetchData"
            class="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
          >
            <svg class="h-4.5 w-4.5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ $t('common.refresh') || 'تحديث' }}
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 text-gray-500 dark:bg-gray-800 dark:text-gray-400">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">إجمالي التغييرات</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ servicesStore.stagingStats.total }}</h3>
            </div>
          </div>
        </div>

        <div class="rounded-2xl border border-warning-200 bg-warning-50 p-5 shadow-theme-sm dark:border-warning-500/20 dark:bg-warning-500/5">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-warning-100 text-warning-600 dark:bg-warning-500/20 dark:text-warning-400">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-warning-700 dark:text-warning-400">قيد الانتظار</p>
              <h3 class="text-2xl font-bold text-warning-900 dark:text-warning-300">{{ servicesStore.stagingStats.pending }}</h3>
            </div>
          </div>
        </div>

        <div class="rounded-2xl border border-success-200 bg-success-50 p-5 shadow-theme-sm dark:border-success-500/20 dark:bg-success-500/5">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-success-700 dark:text-success-400">تم الموافقة</p>
              <h3 class="text-2xl font-bold text-success-900 dark:text-success-300">{{ servicesStore.stagingStats.approved }}</h3>
            </div>
          </div>
        </div>

        <div class="rounded-2xl border border-error-200 bg-error-50 p-5 shadow-theme-sm dark:border-error-500/20 dark:bg-error-500/5">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-error-100 text-error-600 dark:bg-error-500/20 dark:text-error-400">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-error-700 dark:text-error-400">مرفوضة</p>
              <h3 class="text-2xl font-bold text-error-900 dark:text-error-300">{{ servicesStore.stagingStats.rejected }}</h3>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters & Actions -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-3 w-full md:w-auto">
          <div class="relative w-full md:w-48">
            <select v-model="filters.status" @change="fetchData" class="block w-full appearance-none rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
              <option value="pending">{{ $t('services.status_pending') || 'قيد الانتظار' }}</option>
              <option value="approved">{{ $t('services.status_approved') || 'تم الموافقة' }}</option>
              <option value="rejected">{{ $t('services.status_rejected') || 'مرفوضة' }}</option>
              <option value="">{{ $t('services.all') || 'الكل' }}</option>
            </select>
            <span class="pointer-events-none absolute inset-y-0 ltr:right-0 rtl:left-0 flex items-center px-4 text-gray-500">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
            </span>
          </div>
          
          <div class="relative w-full md:w-48">
            <select v-model="filters.severity" @change="fetchData" class="block w-full appearance-none rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
              <option value="">{{ $t('services.all_severities') || 'كل المستويات' }}</option>
              <option value="high">{{ $t('services.high_severity') || 'عالي الخطورة' }}</option>
              <option value="medium">{{ $t('services.medium_severity') || 'متوسط الخطورة' }}</option>
              <option value="low">{{ $t('services.low_severity') || 'منخفض الخطورة' }}</option>
            </select>
            <span class="pointer-events-none absolute inset-y-0 ltr:right-0 rtl:left-0 flex items-center px-4 text-gray-500">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
            </span>
          </div>
        </div>
        
        <div class="flex items-center gap-3 w-full md:w-auto" v-if="selectedIds.length > 0 && filters.status === 'pending'">
          <span class="text-sm font-medium text-brand-600 dark:text-brand-400">{{ selectedIds.length }} محدد</span>
          <button @click="handleBulkApprove" class="rounded-lg bg-success-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-success-700 transition-colors shadow-theme-xs">
            موافقة على المحدد
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
        <div v-if="servicesStore.loading && servicesStore.stagingRecords.length === 0" class="flex justify-center p-8">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="servicesStore.stagingRecords.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="mb-4 rounded-full bg-gray-50 p-4 dark:bg-gray-800 shadow-theme-xs">
            <svg class="h-10 w-10 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">لا توجد تعديلات</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 text-center">لا توجد أي سجلات مطابقة للفلاتر المحددة حالياً.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-start">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                <th v-if="filters.status === 'pending'" class="px-5 py-3 w-12">
                  <div class="flex items-center">
                    <input type="checkbox" @change="toggleAll" :checked="isAllSelected" class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700">
                  </div>
                </th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الفرد</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الحقل المعدل</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">التغيير</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الخطورة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الحالة</th>
                <th v-if="filters.status === 'pending'" class="px-5 py-3 text-end text-sm font-medium text-gray-500 dark:text-gray-400">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="record in servicesStore.stagingRecords" :key="record.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td v-if="filters.status === 'pending'" class="px-5 py-4">
                  <div class="flex items-center">
                    <input type="checkbox" v-model="selectedIds" :value="record.id" class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700">
                  </div>
                </td>
                <td class="px-5 py-4">
                  <div class="flex flex-col">
                    <span class="text-sm font-bold text-gray-900 dark:text-white">{{ record.personnel.full_name }}</span>
                    <span class="text-xs text-gray-500 dark:text-gray-400 font-mono">{{ record.personnel.military_number }}</span>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ formatFieldName(record.field_name) }}</span>
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2 text-sm">
                    <span class="text-error-600 dark:text-error-400 line-through bg-error-50 dark:bg-error-500/10 px-2 py-0.5 rounded">{{ record.old_value || 'فارغ' }}</span>
                    <svg class="h-4 w-4 text-gray-400 ltr:rotate-0 rtl:rotate-180" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                    <span class="text-success-600 dark:text-success-400 font-medium bg-success-50 dark:bg-success-500/10 px-2 py-0.5 rounded">{{ record.new_value || 'فارغ' }}</span>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <span 
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                    :class="{
                      'bg-error-100 text-error-800 dark:bg-error-500/20 dark:text-error-400': record.severity === 'high',
                      'bg-warning-100 text-warning-800 dark:bg-warning-500/20 dark:text-warning-400': record.severity === 'medium',
                      'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300': record.severity === 'low'
                    }"
                  >
                    {{ formatSeverity(record.severity) }}
                  </span>
                </td>
                <td class="px-5 py-4">
                  <span 
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                    :class="{
                      'bg-warning-100 text-warning-800 dark:bg-warning-500/20 dark:text-warning-400': record.status === 'pending',
                      'bg-success-100 text-success-800 dark:bg-success-500/20 dark:text-success-400': record.status === 'approved',
                      'bg-error-100 text-error-800 dark:bg-error-500/20 dark:text-error-400': record.status === 'rejected'
                    }"
                  >
                    {{ formatStatus(record.status) }}
                  </span>
                </td>
                <td v-if="filters.status === 'pending'" class="px-5 py-4 text-end">
                  <div class="flex items-center justify-end gap-2">
                    <button @click="handleApprove(record.id)" class="text-success-600 hover:text-success-900 dark:text-success-400 dark:hover:text-success-300 bg-success-50 dark:bg-success-500/10 hover:bg-success-100 dark:hover:bg-success-500/20 p-1.5 rounded-lg transition-colors" title="موافقة">
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                    <button @click="openRejectModal(record.id)" class="text-error-600 hover:text-error-900 dark:text-error-400 dark:hover:text-error-300 bg-error-50 dark:bg-error-500/10 hover:bg-error-100 dark:hover:bg-error-500/20 p-1.5 rounded-lg transition-colors" title="رفض">
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div v-if="servicesStore.totalPages > 1" class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-900 sm:px-6 rounded-b-2xl">
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
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useServicesStore } from '@/stores/services'
import Swal from 'sweetalert2'

const servicesStore = useServicesStore()

const filters = ref({
  status: 'pending',
  severity: '',
  search: ''
})

const selectedIds = ref<number[]>([])

const isAllSelected = computed(() => {
  if (servicesStore.stagingRecords.length === 0) return false
  return selectedIds.value.length === servicesStore.stagingRecords.length
})

function toggleAll(event: Event) {
  const isChecked = (event.target as HTMLInputElement).checked
  if (isChecked) {
    selectedIds.value = servicesStore.stagingRecords.map(r => r.id)
  } else {
    selectedIds.value = []
  }
}

async function fetchData(page: number = 1) {
  selectedIds.value = []
  await Promise.all([
    servicesStore.fetchStagingStats(),
    servicesStore.fetchStagingRecords(page, filters.value)
  ])
}

function changePage(page: number) {
  fetchData(page)
}

function formatFieldName(field: string): string {
  const map: Record<string, string> = {
    'current_rank': 'الرتبة',
    'current_status': 'الحالة',
    'full_name': 'الاسم الكامل',
    'military_number': 'الرقم العسكري'
  }
  return map[field] || field
}

function formatSeverity(severity: string): string {
  const map: Record<string, string> = {
    'low': 'منخفض',
    'medium': 'متوسط',
    'high': 'عالي الخطورة'
  }
  return map[severity] || severity
}

function formatStatus(status: string): string {
  const map: Record<string, string> = {
    'pending': 'قيد الانتظار',
    'approved': 'مقبول',
    'rejected': 'مرفوض'
  }
  return map[status] || status
}

async function handleApprove(id: number) {
  try {
    await servicesStore.approveStaging(id)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تمت الموافقة بنجاح', showConfirmButton: false, timer: 3000 })
    fetchData(servicesStore.currentPage)
  } catch (err) {
    Swal.fire('خطأ', 'فشل الموافقة على التعديل', 'error')
  }
}

async function openRejectModal(id: number) {
  const { value: reason } = await Swal.fire({
    title: 'رفض التعديل المقترح',
    input: 'textarea',
    inputLabel: 'يرجى كتابة سبب الرفض',
    inputPlaceholder: 'أدخل السبب هنا...',
    showCancelButton: true,
    confirmButtonText: 'رفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444'
  })

  if (reason) {
    try {
      await servicesStore.rejectStaging(id, reason)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم رفض التعديل', showConfirmButton: false, timer: 3000 })
      fetchData(servicesStore.currentPage)
    } catch (err) {
      Swal.fire('خطأ', 'فشل عملية الرفض', 'error')
    }
  }
}

async function handleBulkApprove() {
  if (selectedIds.value.length === 0) return
  
  const result = await Swal.fire({
    title: 'موافقة جماعية',
    text: `هل أنت متأكد من الموافقة على ${selectedIds.value.length} تعديلات دفعة واحدة؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'نعم، موافقة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981'
  })

  if (result.isConfirmed) {
    try {
      await servicesStore.bulkApproveStaging(selectedIds.value)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تمت الموافقة الجماعية بنجاح', showConfirmButton: false, timer: 3000 })
      fetchData(servicesStore.currentPage)
    } catch (err) {
      Swal.fire('خطأ', 'فشلت الموافقة الجماعية', 'error')
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>
