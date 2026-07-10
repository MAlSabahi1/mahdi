<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t?.('personnel.title') || 'شؤون الأفراد'" />

    <div class="space-y-5 text-start">

      <!-- ═══════════════════════════════════════════════════════ -->
      <!-- Stats + Add Button Row                                  -->
      <!-- ═══════════════════════════════════════════════════════ -->
      <div class="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4">
        <!-- Stats Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 flex-1 w-full">
          <div class="rounded-xl border border-gray-200 bg-white p-3.5 dark:border-gray-800 dark:bg-white/[0.03]">
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-50 dark:bg-brand-500/10">
                <svg class="h-4.5 w-4.5 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p class="text-theme-xs text-gray-500 dark:text-gray-400">{{ $t?.('personnel.total') || 'الإجمالي' }}</p>
                <p class="text-base font-bold text-gray-900 dark:text-white">{{ personnelStore.totalCount }}</p>
              </div>
            </div>
          </div>
          <div class="rounded-xl border border-gray-200 bg-white p-3.5 dark:border-gray-800 dark:bg-white/[0.03]">
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-success-50 dark:bg-success-500/10">
                <svg class="h-4.5 w-4.5 text-success-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-theme-xs text-gray-500 dark:text-gray-400">{{ $t?.('personnel.active') || 'موجود' }}</p>
                <p class="text-base font-bold text-success-600 dark:text-success-400">{{ activeCount }}</p>
              </div>
            </div>
          </div>
          <div class="rounded-xl border border-gray-200 bg-white p-3.5 dark:border-gray-800 dark:bg-white/[0.03]">
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-warning-50 dark:bg-warning-500/10">
                <svg class="h-4.5 w-4.5 text-warning-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div>
                <p class="text-theme-xs text-gray-500 dark:text-gray-400">{{ $t?.('personnel.incomplete') || 'بيانات ناقصة' }}</p>
                <p class="text-base font-bold text-warning-600 dark:text-warning-400">{{ incompleteCount }}</p>
              </div>
            </div>
          </div>
          <div class="rounded-xl border border-gray-200 bg-white p-3.5 dark:border-gray-800 dark:bg-white/[0.03]">
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-error-50 dark:bg-error-500/10">
                <svg class="h-4.5 w-4.5 text-error-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>
              </div>
              <div>
                <p class="text-theme-xs text-gray-500 dark:text-gray-400">{{ $t?.('personnel.inactive') || 'غير موجود' }}</p>
                <p class="text-base font-bold text-error-600 dark:text-error-400">{{ inactiveCount }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Button moved to DataTable toolbar -->
      </div>

      <!-- ═══════════════════════════════════════════════════════ -->
      <!-- DataTable Component                                     -->
      <!-- ═══════════════════════════════════════════════════════ -->
      <DataTable
        :columns="tableColumns"
        :data="personnelStore.records"
        row-key="military_number"
        :loading="personnelStore.loading"
        :error="personnelStore.error"
        :current-page="personnelStore.currentPage"
        :total-pages="personnelStore.totalPages"
        :total-count="personnelStore.totalCount"
        :page-size="pageSize"
        :has-actions="true"
        actions-width="90px"
        :has-filters="true"
        :active-filter-count="activeFilterCount"
        :search-placeholder="$t?.('personnel.search_placeholder') || 'بحث بالاسم، الرقم العسكري...'"
        :loading-text="$t?.('common.loading_data') || 'جاري تحميل السجل الموحد...'"
        :empty-title="$t?.('common.empty_registry') || 'السجل فارغ'"
        :empty-description="$t?.('common.empty_registry_desc') || 'لم يتم العثور على أفراد يطابقون معايير البحث الحالية.'"
        @search="onSearch"
        @refresh="loadPersonnel(personnelStore.currentPage)"
        @export="exportData"
        @change-page="goToPage"
        @change-page-size="changePageSize"
      >
        <!-- ── Toolbar Actions Slot ──────────────────────────── -->
        <template #toolbar-actions>
          <RouterLink
            to="/personnel/create"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-theme-sm font-bold text-white shadow-theme-xs hover:bg-brand-600 hover:shadow-theme-sm hover:-translate-y-0.5 transition-all duration-200 ease-in-out cursor-pointer whitespace-nowrap shrink-0"
          >
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            {{ $t?.('personnel.add_personnel') || 'إضافة منتسب' }}
          </RouterLink>
        </template>

        <!-- ── Filters Slot ──────────────────────────────────── -->
        <template #filters>
          <div class="p-5">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <BaseSelect
                v-model="filters.current_rank"
                :label="$t?.('personnel.military_rank') || 'الرتبة العسكرية'"
                :placeholder="$t?.('personnel.all_ranks') || 'جميع الرتب'"
                :options="coreStore.ranks"
              />
              <BaseSelect
                v-model="filters.current_status"
                :label="$t?.('personnel.employment_status') || 'الحالة الوظيفية'"
                :placeholder="$t?.('personnel.all_statuses') || 'جميع الحالات'"
                :options="coreStore.statuses"
              />
              <BaseSelect
                v-model="filters.governorate"
                :label="$t?.('personnel.governorate') || 'المحافظة'"
                :placeholder="$t?.('personnel.all_governorates') || 'جميع المحافظات'"
                :options="coreStore.governorates"
              />
            </div>
            <div class="mt-4 flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-800">
              <span v-if="hasActiveFilters" class="text-theme-xs text-brand-600 dark:text-brand-400 font-medium">
                {{ activeFilterCount }} {{ $t?.('personnel.active_filters') || 'فلتر نشط' }}
              </span>
              <span v-else></span>
              <div class="flex items-center gap-2">
                <button @click="clearFilters" class="rounded-lg px-4 py-2 text-theme-sm font-medium text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 transition-colors cursor-pointer">
                  {{ $t?.('common.clear_all') || 'مسح الكل' }}
                </button>
                <button @click="loadPersonnel(1)" class="rounded-lg bg-brand-500 px-5 py-2 text-theme-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer">
                  {{ $t?.('common.apply') || 'تطبيق' }}
                </button>
              </div>
            </div>
          </div>
        </template>

        <!-- ── Empty Action Slot ─────────────────────────────── -->
        <template #empty-action>
          <RouterLink
            to="/personnel/create"
            class="mt-4 rounded-lg bg-brand-500 px-4 py-2 text-theme-sm font-medium text-white hover:bg-brand-600 transition-colors"
          >
            {{ $t?.('personnel.add_first_personnel') || 'إضافة أول منتسب' }}
          </RouterLink>
        </template>

        <!-- ── Actions Column ────────────────────────────────── -->
        <template #actions="{ row }">
          <RouterLink
            :to="`/personnel/${row.military_number}`"
            class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors cursor-pointer p-1"
            :title="$t?.('common.view') || 'عرض'"
          >
            <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </RouterLink>
          <RouterLink
            :to="`/personnel/${row.military_number}/edit`"
            class="text-gray-400 hover:text-blue-600 dark:text-gray-500 dark:hover:text-blue-400 transition-colors cursor-pointer p-1"
            :title="$t?.('common.edit') || 'تعديل'"
          >
            <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </RouterLink>
          <button
            class="text-gray-400 hover:text-error-600 dark:text-gray-500 dark:hover:text-error-400 transition-colors cursor-pointer p-1"
            :title="$t?.('common.delete') || 'حذف'"
          >
            <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </template>

        <!-- ── Custom Cell: Serial ────────────────────────────── -->
        <template #cell-serial="{ index }">
          <p class="text-gray-500 text-theme-sm dark:text-gray-400 font-mono text-center">
            {{ (personnelStore.currentPage - 1) * pageSize + index + 1 }}
          </p>
        </template>

        <!-- ── Custom Cell: Full Name ────────────────────────── -->
        <template #cell-full_name="{ row }">
          <div class="flex items-center gap-3">
            <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-50 text-brand-600 font-bold text-theme-xs dark:bg-brand-500/10 dark:text-brand-400">
              {{ row.full_name ? row.full_name.charAt(0) : 'ف' }}
            </div>
            <div>
              <span class="block font-medium text-gray-800 text-theme-sm dark:text-white/90">{{ row.full_name }}</span>
              <span v-if="row.rank_name" class="block text-gray-500 text-theme-xs dark:text-gray-400">{{ row.rank_name }}</span>
            </div>
          </div>
        </template>

        <!-- ── Custom Cell: Military Number ──────────────────── -->
        <template #cell-military_number="{ value }">
          <p class="text-gray-500 text-theme-sm dark:text-gray-400 font-mono">{{ value }}</p>
        </template>

        <!-- ── Custom Cell: Sub Administration ───────────────── -->
        <template #cell-sub_administration="{ row }">
          <p class="text-gray-800 text-theme-sm dark:text-white/90 font-medium">
            <template v-if="row.central_department_name">
              {{ row.central_department_name }}
            </template>
            <template v-else-if="row.branch_name">
              {{ row.branch_name }}
            </template>
            <template v-else-if="row.district_police_name">
              {{ row.district_police_name }}
            </template>
            <template v-else>
              <span class="text-gray-400">—</span>
            </template>
          </p>
        </template>

        <!-- ── Custom Cell: Division ─────────────────────────── -->
        <template #cell-division_name="{ row }">
          <p class="text-gray-800 text-theme-sm dark:text-white/90 font-medium">
            <template v-if="row.division_name">
              {{ row.division_name }}
            </template>
            <template v-else>
              <span class="text-gray-400">—</span>
            </template>
          </p>
        </template>

        <!-- ── Custom Cell: National ID ──────────────────────── -->
        <template #cell-national_id="{ value }">
          <p class="text-gray-500 text-theme-sm dark:text-gray-400 font-mono">{{ value || '—' }}</p>
        </template>

        <!-- ── Custom Cell: Phone ────────────────────────────── -->
        <template #cell-phone_number="{ value }">
          <p class="text-gray-500 text-theme-sm dark:text-gray-400 font-mono">{{ value || '—' }}</p>
        </template>

        <!-- ── Custom Cell: Rank ─────────────────────────────── -->
        <template #cell-rank_name="{ value }">
          <p class="text-gray-800 text-theme-sm dark:text-white/90 font-medium">{{ value || $t?.('personnel.no_rank') || 'بدون رتبة' }}</p>
        </template>

        <!-- ── Custom Cell: Status Classification ────────────── -->
        <template #cell-status_classification="{ row }">
          <p class="text-gray-800 text-theme-sm dark:text-white/90 font-medium">
            {{ row.status_classification_display || 'غير متوفر' }}
          </p>
        </template>

        <!-- ── Custom Cell: Quality Score ─────────────────────── -->
        <template #cell-data_quality_score="{ value }">
          <div class="flex items-center gap-2">
            <div class="h-1.5 w-14 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-500"
                :class="getQualityBarColor(value)"
                :style="{ width: value + '%' }"
              ></div>
            </div>
            <span class="text-theme-xs font-semibold" :class="getQualityTextColor(value)">{{ value }}%</span>
          </div>
        </template>

        <!-- ── Custom Cell: Join Date ─────────────────────────── -->
        <template #cell-join_date="{ value }">
          <p class="text-gray-500 text-theme-sm dark:text-gray-400 font-mono">{{ value || '—' }}</p>
        </template>

        <!-- ── Custom Cell: Expense Status ───────────────────── -->
        <template #cell-expense_status="{ row }">
          <p class="text-gray-800 text-theme-sm dark:text-white/90 font-medium">
            {{ row.expense_status_display || 'غير متوفر' }}
          </p>
        </template>
      </DataTable>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import BaseSelect from '@/components/common/BaseSelect.vue'
import type { DataTableColumn } from '@/components/tables/DataTable.vue'
import { usePersonnelStore } from '@/stores/personnel'
import { useCoreStore } from '@/stores/core'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const { t } = useI18n()
const personnelStore = usePersonnelStore()
const coreStore = useCoreStore()

const pageSize = ref(50)
const searchText = ref('')

// ── Table Column Definitions ───────────────────────────────
const tableColumns = computed<DataTableColumn[]>(() => [
  { key: 'serial', label: 'م' },
  { key: 'rank_name', label: t('personnel.rank') || 'الرتبة' },
  { key: 'military_number', label: t('personnel.military_number') || 'الرقم العسكري' },
  { key: 'national_id', label: t('personnel.national_id') || 'الرقم الوطني' },
  { key: 'full_name', label: t('personnel.full_name') || 'الاسم الكامل' },
  { key: 'security_admin_name', label: t('personnel.administration') || 'الوحدة' },
  { key: 'sub_administration', label: 'السرية / الإدارة / المديرية' },
  { key: 'division_name', label: 'القسم_فرع السرية' },
  { key: 'unit_name', label: t('personnel.unit') || 'الوحدة التابعة' },
  { key: 'position_name', label: t('personnel.position') || 'المنصب' },
  { key: 'job_title_name', label: t('personnel.job_title') || 'المسمى الوظيفي' },
  { key: 'category_name', label: t('personnel.category') || 'الفئة' },
  { key: 'status_classification', label: t('personnel.classification') || 'الحالة' },
  { key: 'status_name', label: t('personnel.status_type') || 'نوع الحالة' },
  { key: 'force_classification_name', label: t('personnel.force_classification') || 'تصنيف القوة' },
  { key: 'qualification_name', label: t('personnel.qualification') || 'المؤهل' },
  { key: 'phone_number', label: t('personnel.phone_number') || 'رقم الهاتف' },
  // باقي الأعمدة
  { key: 'old_military_number', label: t('personnel.old_military_number') || 'الرقم العسكري القديم' },
  { key: 'expense_status', label: t('personnel.expense_status') || 'حالة النفقات' },
  { key: 'appointment_info', label: t('personnel.appointment_info') || 'معلومات التعيين' },
  { key: 'data_quality_score', label: t('personnel.quality') || 'الجودة' },
  { key: 'join_date', label: t('personnel.join_date') || 'تاريخ الالتحاق' },
])


// ── Filters ────────────────────────────────────────────────
const filters = ref({
  current_rank: null as number | string | null,
  current_status: null as number | string | null,
  governorate: null as number | string | null
})

const hasActiveFilters = computed(() =>
  filters.value.current_rank !== null ||
  filters.value.current_status !== null ||
  filters.value.governorate !== null
)

const activeFilterCount = computed(() => {
  let count = 0
  if (filters.value.current_rank !== null) count++
  if (filters.value.current_status !== null) count++
  if (filters.value.governorate !== null) count++
  return count
})

function clearFilters() {
  filters.value = { current_rank: null, current_status: null, governorate: null }
  loadPersonnel(1)
}

// ── Stats ──────────────────────────────────────────────────
const activeCount = computed(() =>
  personnelStore.records.filter(p => p.status_classification === 'active').length
)
const inactiveCount = computed(() =>
  personnelStore.records.filter(p => p.status_classification !== 'active').length
)
const incompleteCount = computed(() =>
  personnelStore.records.filter(p => p.data_quality_score < 80).length
)

// ── Data Loading ───────────────────────────────────────────
function loadPersonnel(page = 1) {
  personnelStore.fetchPersonnel({
    search: searchText.value || undefined,
    current_rank: filters.value.current_rank || undefined,
    current_status: filters.value.current_status || undefined,
    governorate: filters.value.governorate || undefined,
    page
  })
}

function onSearch(query: string) {
  searchText.value = query
  loadPersonnel(1)
}

function goToPage(page: number) {
  if (page >= 1 && page <= personnelStore.totalPages) {
    loadPersonnel(page)
  }
}

function changePageSize(size: number) {
  pageSize.value = size
  loadPersonnel(1)
}

// ── Export ──────────────────────────────────────────────────
async function exportData() {
  try {
    const params: any = {}
    if (filters.value.current_rank) params.current_rank = filters.value.current_rank
    if (filters.value.current_status) params.current_status = filters.value.current_status
    if (filters.value.governorate) params.governorate = filters.value.governorate

    const response = await api.get('/personnel/export_csv/', {
      params,
      responseType: 'blob'
    })

    const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8;' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'personnel.csv'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('common.export_success') || 'تم التصدير بنجاح', showConfirmButton: false, timer: 2500 })
  } catch (err) {
    console.error('Export failed:', err)
  }
}

// ── Quality Helpers ────────────────────────────────────────
function getQualityTextColor(score: number) {
  if (score >= 80) return 'text-success-600 dark:text-success-400'
  if (score >= 50) return 'text-warning-600 dark:text-warning-400'
  return 'text-error-600 dark:text-error-400'
}

function getQualityBarColor(score: number) {
  if (score >= 80) return 'bg-success-500'
  if (score >= 50) return 'bg-warning-500'
  return 'bg-error-500'
}

// ── Lifecycle ──────────────────────────────────────────────
onMounted(() => {
  if (coreStore.ranks.length === 0) {
    coreStore.fetchAllReferences()
  }
  loadPersonnel()
})
</script>
