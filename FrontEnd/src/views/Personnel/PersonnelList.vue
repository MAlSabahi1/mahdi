<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('personnel.title') }}</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t('personnel.subtitle') }}
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="exportData"
            class="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
          >
            <svg class="h-4.5 w-4.5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ $t('common.export') || 'تصدير' }}
          </button>
          <RouterLink
            to="/personnel/create"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            {{ $t('personnel.add_personnel') }}
          </RouterLink>
        </div>
      </div>

      <!-- Filters & Search Section -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
        <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="relative w-full md:max-w-md">
            <div class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3">
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              @input="debouncedSearch"
              type="text"
              class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 ps-10 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:border-brand-500 dark:focus:ring-brand-500"
              :placeholder="$t('personnel.search_placeholder') || 'البحث بالرقم العسكري، الاسم، أو الرقم الوطني...'"
            >
          </div>
          <div class="flex items-center gap-3 w-full md:w-auto">
            <button
              @click="loadPersonnel(1)"
              class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors w-full md:w-auto"
            >
              {{ $t('common.refresh') || 'تحديث' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
        <div v-if="personnelStore.loading && personnelStore.records.length === 0" class="flex justify-center p-8">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>

        <div v-else-if="personnelStore.error" class="p-8 text-center text-error-500">
          {{ personnelStore.error }}
        </div>

        <div v-else-if="personnelStore.records.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="mb-4 rounded-full bg-gray-50 p-4 dark:bg-gray-800 shadow-theme-xs">
            <svg class="h-10 w-10 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('common.no_data') || 'لا توجد بيانات' }}</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 text-center max-w-sm">لم يتم العثور على أفراد يطابقون معايير البحث الحالية. يمكنك المحاولة بكلمات بحث مختلفة.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-start">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('personnel.military_number') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('personnel.full_name') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('personnel.org_job_section') || 'جهة العمل' }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.status') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('personnel.data_quality') || 'جودة البيانات' }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="person in personnelStore.records"
                :key="person.military_number"
                class="border-b border-gray-100 last:border-0 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
              >
                <!-- Military Number -->
                <td class="px-5 py-4">
                  <span class="font-mono text-sm font-semibold text-gray-900 dark:text-white">{{ person.military_number }}</span>
                  <span v-if="person.old_military_number" class="block text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    {{ $t('personnel.old_military_number_prefix') }} {{ person.old_military_number }}
                  </span>
                </td>
                
                <!-- Name & Rank -->
                <td class="px-5 py-4">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ person.full_name }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ person.rank_name || ($t('personnel.no_rank') || 'بدون رتبة') }}
                    <span v-if="person.pending_rank" class="text-warning-500" :title="$t('personnel.pending_promotion')">
                      ({{ $t('personnel.due_promotion') }} {{ person.pending_rank_name }})
                    </span>
                  </p>
                </td>
                
                <!-- Workplace -->
                <td class="px-5 py-4">
                  <p class="text-sm text-gray-700 dark:text-gray-300">
                    {{ person.branch_name || person.security_admin_name || ($t('personnel.unspecified') || 'غير محدد') }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ person.position_name || person.job_title_name || ($t('personnel.no_position') || 'بدون منصب') }}
                  </p>
                </td>
                
                <!-- Status -->
                <td class="px-5 py-4">
                  <span
                    class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium"
                    :class="getStatusColor(person.status_classification)"
                  >
                    <span class="h-1.5 w-1.5 rounded-full" :class="getStatusDotColor(person.status_classification)"></span>
                    {{ person.status_name || ($t('personnel.unspecified') || 'غير محدد') }}
                  </span>
                </td>
                
                <!-- Data Quality Score -->
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <div class="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700 min-w-[80px]">
                      <div 
                        class="h-2 rounded-full" 
                        :class="getQualityScoreColor(person.data_quality_score)"
                        :style="{ width: `${person.data_quality_score}%` }"
                      ></div>
                    </div>
                    <span class="text-xs font-medium" :class="getQualityScoreTextColor(person.data_quality_score)">
                      {{ person.data_quality_score }}%
                    </span>
                  </div>
                  <span v-if="!person.is_complete" class="text-[10px] text-error-500 mt-1 block">{{ $t('personnel.incomplete_data') || 'بيانات غير مكتملة' }}</span>
                </td>
                
                <!-- Actions -->
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <RouterLink
                      :to="`/personnel/${person.military_number}`"
                      class="rounded-lg p-2 text-brand-500 hover:bg-brand-50 dark:hover:bg-brand-500/10 transition-colors"
                      :title="$t('personnel.view_profile') || 'عرض الملف'"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                      </svg>
                    </RouterLink>
                    <RouterLink
                      :to="`/personnel/${person.military_number}/edit`"
                      class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200 transition-colors"
                      :title="$t('common.edit') || 'تعديل'"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </RouterLink>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="!personnelStore.loading && personnelStore.records.length > 0" class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <p class="text-sm text-gray-500 dark:text-gray-400 text-center sm:text-end">
            {{ $t('common.page') }} <span class="font-medium text-gray-900 dark:text-white">{{ personnelStore.currentPage }}</span> {{ $t('common.from') }} <span class="font-medium text-gray-900 dark:text-white">{{ personnelStore.totalPages }}</span>
            ({{ $t('common.total') }}: {{ personnelStore.totalCount }})
          </p>
          <div class="flex justify-center gap-2">
            <button
              :disabled="personnelStore.currentPage <= 1"
              @click="goToPage(personnelStore.currentPage - 1)"
              class="px-3 py-1.5 rounded-lg border border-gray-200 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
            >
              {{ $t('common.previous') || 'السابق' }}
            </button>
            <button
              :disabled="personnelStore.currentPage >= personnelStore.totalPages"
              @click="goToPage(personnelStore.currentPage + 1)"
              class="px-3 py-1.5 rounded-lg border border-gray-200 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
            >
              {{ $t('common.next') || 'التالي' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { usePersonnelStore } from '@/stores/personnel'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const personnelStore = usePersonnelStore()

const searchQuery = ref('')
let searchTimeout: ReturnType<typeof setTimeout> | null = null

function debouncedSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadPersonnel(1)
  }, 400)
}

function loadPersonnel(page = 1) {
  personnelStore.fetchPersonnel({
    search: searchQuery.value || undefined,
    page
  })
}

function goToPage(page: number) {
  if (page >= 1 && page <= personnelStore.totalPages) {
    loadPersonnel(page)
  }
}

async function exportData() {
  try {
    const params: any = {}
    if (searchQuery.value) params.search = searchQuery.value
    
    const response = await api.get('/personnel/export_csv/', {
      params,
      responseType: 'blob'
    })
    
    const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8;' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    a.download = 'personnel.csv'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)
    
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم التصدير بنجاح', showConfirmButton: false, timer: 2500 })
  } catch (err) {
    // Global error handler shows Swal automatically
  }
}

// Helper methods for styling
function getStatusColor(classification: string | null) {
  switch (classification) {
    case 'active': return 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400'
    case 'leave': return 'bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400'
    case 'absent': return 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
    case 'inactive': return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
    default: return 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400'
  }
}

function getStatusDotColor(classification: string | null) {
  switch (classification) {
    case 'active': return 'bg-success-500'
    case 'leave': return 'bg-warning-500'
    case 'absent': return 'bg-error-500'
    case 'inactive': return 'bg-gray-500'
    default: return 'bg-brand-500'
  }
}

function getQualityScoreColor(score: number) {
  if (score >= 80) return 'bg-success-500'
  if (score >= 50) return 'bg-warning-500'
  return 'bg-error-500'
}

function getQualityScoreTextColor(score: number) {
  if (score >= 80) return 'text-success-600 dark:text-success-400'
  if (score >= 50) return 'text-warning-600 dark:text-warning-400'
  return 'text-error-600 dark:text-error-400'
}

onMounted(() => {
  loadPersonnel()
})
</script>
