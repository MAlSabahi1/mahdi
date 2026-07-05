<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('personnel.profile_search.title') || 'الملف الكامل للمنتسب'" />

    <div class="space-y-6">
      
      <!-- Page Info Card -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs flex flex-col sm:flex-row sm:items-center gap-4 relative overflow-hidden">
        <!-- Subtle decorative background element -->
        <div class="absolute -left-6 -top-6 w-24 h-24 rounded-full bg-brand-50 dark:bg-brand-500/5 blur-2xl pointer-events-none"></div>
        
        <div class="relative z-10 h-12 w-12 rounded-xl bg-brand-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400 flex items-center justify-center shrink-0 border border-brand-100 dark:border-brand-500/20">
          <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 21h7a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v11m0 5l4.879-4.879m0 0a3 3 0 104.243-4.242 3 3 0 00-4.243 4.242z" />
          </svg>
        </div>
        <div class="relative z-10">
          <h2 class="text-lg font-bold text-gray-900 dark:text-white">
            {{ $t('personnel.profile_search.heading') || 'الاستعلام الشامل للمنتسبين' }}
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1 max-w-3xl">
            {{ $t('personnel.profile_search.description') || 'يتيح لك هذا القسم البحث عن أي منتسب للوصول السريع إلى تفاصيل ملفه الشامل، بما في ذلك بيانات الخدمة الأساسية، الترقيات، والتسويات.' }}
          </p>
        </div>
      </div>
      
      <!-- Data Table Area -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs">
        <BasicTable
          :columns="tableColumns"
          :data="results"
          row-key="military_number"
          :loading="loading"
          :has-actions="true"
          actions-width="150px"
          :empty-title="searchQuery ? ($t('common.no_results') || 'لم يتم العثور على نتائج') : ($t('personnel.profile_search.heading') || 'الاستعلام الشامل للمنتسبين')"
          :empty-description="searchQuery ? ($t('personnel.profile_search.no_match') || 'لا يوجد منتسب يطابق معايير البحث الحالية.') : ($t('personnel.profile_search.search_prompt') || 'يرجى إدخال اسم أو رقم المنتسب في شريط البحث أعلاه للبحث في السجلات.')"
        >
          <!-- Table Header Toolbar -->
          <template #header>
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 w-full mb-2">
              <div class="relative w-full sm:max-w-md shrink-0">
                <div class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3">
                  <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  v-model="searchQuery"
                  type="text"
                  :placeholder="$t('personnel.profile_search.search_placeholder') || 'بحث بالاسم، الرقم العسكري...'"
                  class="w-full h-10 rounded-lg border border-gray-300 bg-gray-50 py-2 ps-9 pe-20 text-theme-sm text-gray-900 placeholder-gray-400 focus:border-brand-300 focus:bg-white focus:ring-2 focus:ring-brand-500/10 focus:outline-none dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500 transition-all"
                  @keyup.enter="handleSearch(1)"
                />
                <button 
                  @click="handleSearch(1)"
                  class="absolute end-1 top-1 bottom-1 px-4 rounded-md bg-brand-600 text-white text-xs font-medium hover:bg-brand-700 transition-colors cursor-pointer flex items-center justify-center min-w-[60px]"
                >
                  <span v-if="!loading">{{ $t('common.search') || 'بحث' }}</span>
                  <svg v-else class="h-3.5 w-3.5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                </button>
              </div>
            </div>
          </template>

          <template #cell-military_number="{ row }">
            <span class="font-medium text-gray-900 dark:text-white">{{ row.military_number }}</span>
          </template>

          <template #cell-full_name="{ row }">
            <span class="font-bold text-sm text-gray-900 dark:text-white">{{ row.full_name }}</span>
          </template>

          <template #cell-rank_name="{ row }">
            <span class="inline-block px-2.5 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-md text-xs font-medium border border-gray-200 dark:border-gray-700">
              {{ row.rank_name || $t('personnel.unspecified') || 'غير محدد' }}
            </span>
          </template>
          
          <template #cell-classification="{ row }">
            <span class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold" :class="getClassificationColor(row.classification)">
              {{ getClassificationName(row.classification) }}
            </span>
          </template>

          <template #actions="{ row }">
            <button @click="viewProfile(row.military_number)" class="inline-flex items-center gap-1.5 rounded-lg bg-brand-50 text-brand-700 px-3 py-1.5 text-xs font-medium hover:bg-brand-100 dark:bg-brand-500/10 dark:text-brand-400 dark:hover:bg-brand-500/20 transition-colors cursor-pointer">
              <span>{{ $t('personnel.view_profile') || 'عرض الملف' }}</span>
              <svg class="h-3.5 w-3.5 rtl:-scale-x-100" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </template>

          <template #footer>
            <TablePagination
              v-if="!loading && totalResults > 0"
              :currentPage="currentPage"
              :totalPages="totalPages"
              :totalCount="totalResults"
              :pageSize="pageSize"
              :visiblePages="computedVisiblePages"
              @change-page="handleSearch"
            />
          </template>
        </BasicTable>

      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import BasicTable from '@/components/tables/BasicTable.vue'
import TablePagination from '@/components/common/TablePagination.vue'
import { usePersonnelStore } from '@/stores/personnel'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const personnelStore = usePersonnelStore()

const searchQuery = ref('')
const loading = ref(false)
const results = ref<any[]>([])

const totalResults = ref(0)
const totalPages = ref(1)
const currentPage = ref(1)
const pageSize = ref(15)

const tableColumns = computed(() => [
  { key: 'military_number', label: t('personnel.military_number') || 'الرقم العسكري' },
  { key: 'full_name', label: t('personnel.full_name') || 'الاسم الكامل' },
  { key: 'rank_name', label: t('personnel.rank') || 'الرتبة', class: 'text-center', tdClass: 'text-center' },
  { key: 'classification', label: t('personnel.status_classification') || 'حالة الدوام', class: 'text-center', tdClass: 'text-center' }
])

const computedVisiblePages = computed((): (number | string)[] => {
  const total = totalPages.value || 1
  const current = currentPage.value || 1
  const pages: (number | string)[] = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

async function handleSearch(page: number = 1) {
  if (!searchQuery.value.trim()) {
    results.value = []
    totalResults.value = 0
    return
  }

  loading.value = true
  try {
    await personnelStore.fetchPersonnel({
      search: searchQuery.value,
      page: page
    })
    results.value = personnelStore.records || []
    totalResults.value = personnelStore.totalCount || 0
    totalPages.value = personnelStore.totalPages || 1
    currentPage.value = page
    pageSize.value = 10
  } catch (error) {
    console.error('Error searching personnel:', error)
  } finally {
    loading.value = false
  }
}

function viewProfile(militaryNumber: string) {
  router.push(`/personnel/${militaryNumber}`)
}

function getClassificationColor(classification: string | undefined) {
  switch (classification) {
    case 'active': return 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400'
    case 'leave': return 'bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400'
    case 'absent': return 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
    case 'inactive': return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
    default: return 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400'
  }
}

function getClassificationName(classification: string | undefined) {
  switch (classification) {
    case 'active': return t('personnel.status_types.active') || 'مداوم'
    case 'leave': return t('personnel.status_types.leave') || 'إجازة'
    case 'absent': return t('personnel.status_types.absent') || 'غائب'
    case 'inactive': return t('personnel.status_types.inactive') || 'غير نشط'
    default: return t('personnel.unspecified') || 'غير محدد'
  }
}
</script>
