<template>
  <div class="rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03] relative z-10 overflow-visible">

    <!-- ─── DataTable Toolbar ─────────────────────────────── -->
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 px-5 py-4 border-b border-gray-200 dark:border-gray-800 print:hidden">

      <!-- Right Side (RTL): Search & Tools -->
      <div class="flex flex-wrap sm:flex-nowrap items-center gap-3 w-full md:w-auto md:flex-1">
        
        <!-- Column Visibility (Eye) -->
        <div class="order-2 sm:order-1 shrink-0">
          <ColumnsSelector :columns="internalColumns" />
        </div>

        <!-- Inline Search -->
        <div class="relative w-full sm:max-w-xs shrink-0 order-1 sm:order-2">
          <div class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3">
            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            v-model="searchQuery"
            @input="onSearchInput"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full h-10 rounded-lg border border-gray-300 bg-gray-50 py-2 ps-9 pe-8 text-theme-sm text-gray-900 placeholder-gray-400 focus:border-brand-300 focus:bg-white focus:ring-2 focus:ring-brand-500/10 focus:outline-none dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500 dark:focus:border-brand-500/40 dark:focus:bg-gray-900 transition-all"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''; onSearchInput()"
            class="absolute inset-y-0 end-0 flex items-center pe-2.5 text-gray-400 hover:text-gray-600 cursor-pointer"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Action Buttons Group -->
        <div class="flex flex-wrap items-center gap-2 shrink-0 order-3">

          <!-- Refresh -->
          <button
            @click="$emit('refresh')"
            :class="[
              'flex h-10 w-10 items-center justify-center rounded-lg border shadow-theme-xs transition-all duration-200 ease-in-out cursor-pointer shrink-0 hover:shadow-theme-sm hover:-translate-y-0.5',
              loading
                ? 'border-brand-200 bg-brand-50 text-brand-500 dark:border-brand-500/30 dark:bg-brand-500/10'
                : 'border-gray-200 bg-white text-gray-500 hover:bg-brand-50 hover:text-brand-600 hover:border-brand-200 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-brand-500/10 dark:hover:text-brand-400 dark:hover:border-brand-500/30'
            ]"
            :title="$t?.('common.refresh') || 'تحديث'"
          >
            <svg :class="['h-5 w-5', loading && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          <!-- Filter Toggle -->
          <button
            v-if="hasFilters"
            @click="filtersVisible = !filtersVisible"
            :class="[
              'flex h-10 w-10 items-center justify-center rounded-lg border shadow-theme-xs transition-all duration-200 ease-in-out cursor-pointer relative shrink-0 hover:shadow-theme-sm hover:-translate-y-0.5',
              filtersVisible || activeFilterCount > 0
                ? 'border-brand-300 bg-brand-50 text-brand-600 dark:border-brand-500/30 dark:bg-brand-500/10 dark:text-brand-400'
                : 'border-gray-200 bg-white text-gray-500 hover:bg-brand-50 hover:text-brand-600 hover:border-brand-200 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-brand-500/10 dark:hover:text-brand-400 dark:hover:border-brand-500/30'
            ]"
            :title="$t?.('common.filter') || 'تصفية'"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            <span
              v-if="activeFilterCount > 0"
              class="absolute -top-1.5 -left-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-brand-500 text-[9px] font-bold text-white ring-2 ring-white dark:ring-gray-900 shadow-sm"
            >
              {{ activeFilterCount }}
            </span>
          </button>

          <!-- Export -->
          <button
            @click="$emit('export')"
            class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-theme-xs hover:bg-brand-50 hover:text-brand-600 hover:border-brand-200 hover:shadow-theme-sm hover:-translate-y-0.5 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-brand-500/10 dark:hover:text-brand-400 dark:hover:border-brand-500/30 transition-all duration-200 ease-in-out cursor-pointer shrink-0"
            :title="$t?.('common.export_csv') || 'تصدير CSV'"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>

          <!-- Print -->
          <button
            @click="handlePrint"
            class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-theme-xs hover:bg-brand-50 hover:text-brand-600 hover:border-brand-200 hover:shadow-theme-sm hover:-translate-y-0.5 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-brand-500/10 dark:hover:text-brand-400 dark:hover:border-brand-500/30 transition-all duration-200 ease-in-out cursor-pointer shrink-0"
            :title="$t?.('common.print_table') || 'طباعة الجدول'"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Left Side (RTL): Toolbar Actions Slot (e.g. Add Button) -->
      <div class="flex items-center gap-2 w-full md:w-auto shrink-0 justify-start sm:justify-end">
        <slot name="toolbar-actions" />
      </div>
    </div>

    <!-- ─── Collapsible Filters Panel ─────────────────────── -->
    <transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="max-h-0 opacity-0"
      enter-to-class="max-h-[500px] opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="max-h-[500px] opacity-100"
      leave-to-class="max-h-0 opacity-0"
    >
      <div v-if="filtersVisible && hasFilters" class="overflow-hidden border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-950/30">
        <slot name="filters" />
      </div>
    </transition>

    <!-- ─── Loading State ─────────────────────────────────── -->
    <div v-if="loading && data.length === 0" class="flex flex-col items-center justify-center py-20">
      <svg class="h-8 w-8 animate-spin text-brand-500 mb-3" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
      <span class="text-theme-sm font-medium text-gray-500 dark:text-gray-400">{{ loadingText || $t?.('common.loading_data') || 'جاري تحميل البيانات...' }}</span>
    </div>

    <!-- ─── Error State ───────────────────────────────────── -->
    <div v-else-if="error" class="flex flex-col items-center justify-center py-20 px-4">
      <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-error-50 dark:bg-error-500/10">
        <svg class="h-6 w-6 text-error-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-theme-sm font-semibold text-error-600 dark:text-error-400 text-center">{{ error }}</p>
      <button @click="$emit('refresh')" class="mt-3 text-theme-xs text-brand-500 hover:text-brand-600 font-medium cursor-pointer">{{ $t?.('common.retry') || 'إعادة المحاولة' }}</button>
    </div>

    <!-- ─── Empty State ───────────────────────────────────── -->
    <div v-else-if="data.length === 0" class="flex flex-col items-center justify-center py-20 px-4">
      <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
        <svg class="h-7 w-7 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <h3 class="text-theme-sm font-semibold text-gray-900 dark:text-white">{{ emptyTitle || $t?.('common.no_data') || 'لا توجد بيانات' }}</h3>
      <p class="mt-1 text-theme-xs text-gray-500 dark:text-gray-400 text-center max-w-sm">{{ emptyDescription || $t?.('common.no_data_desc') || 'لا توجد بيانات متاحة لعرضها في هذا الجدول.' }}</p>
      <slot name="empty-action" />
    </div>

    <!-- ─── Data Table ────────────────────────────────────── -->
    <template v-else>
      <!-- Loading overlay for subsequent fetches -->
      <div v-if="loading" class="relative">
        <div class="absolute inset-0 z-10 bg-white/60 dark:bg-gray-900/60 flex items-center justify-center backdrop-blur-[1px]">
          <svg class="h-6 w-6 animate-spin text-brand-500" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
      </div>

      <div ref="tableContainerRef" class="max-w-full overflow-x-auto print:overflow-visible print:max-w-none custom-scrollbar">
        <table class="min-w-full print:w-full print:table-fixed">
          <!-- Print column widths -->
          <colgroup class="hidden print:table-column-group">
            <col
              v-for="col in columns"
              :key="'cg-' + col.key"
              :style="{ width: col.printWidth || 'auto' }"
            />
          </colgroup>
          <thead>
            <!-- Group Headers Row -->
            <tr v-if="columnGroups && columnGroups.length > 0" class="border-b border-gray-200 dark:border-gray-700 print:border-black print:border-2">
              <template v-for="(group, gi) in columnGroups" :key="gi">
                <th
                  v-if="visibleColsInGroup(group.keys) > 0"
                  :colspan="visibleColsInGroup(group.keys)"
                  :class="[
                    'border-e border-gray-200 dark:border-gray-700 text-center px-4 py-2.5 print:px-1 print:py-1 print:text-[10px] print:border-black print:border',
                    group.highlighted ? 'bg-brand-50/40 dark:bg-brand-500/5' : ''
                  ]"
                >
                  <p :class="['font-semibold text-theme-xs', group.highlighted ? 'text-brand-700 dark:text-brand-400' : 'text-gray-600 dark:text-gray-400']">{{ group.label }}</p>
                </th>
              </template>
              <!-- Actions Group -->
              <th v-if="hasActions" class="md:sticky md:end-0 z-20 bg-slate-50 dark:bg-slate-900 border-s border-gray-200 dark:border-gray-700 px-4 py-2.5 text-center" :style="{ width: actionsWidth }">
                <p class="font-semibold text-gray-600 text-theme-xs dark:text-gray-400">{{ $t?.('common.operations') || 'العمليات' }}</p>
              </th>
            </tr>

            <!-- Column Headers Row -->
            <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 print:border-black print:border-2">
              <template v-for="col in columns" :key="col.key">
                <th
                  v-if="isColVisible(col.key)"
                  :class="['border-e border-gray-200 dark:border-gray-700 px-5 py-3 text-start whitespace-nowrap print:whitespace-normal print:break-words print:p-0.5 print:text-[6px] print:leading-tight print:border-black print:border', col.class || '']"
                  :style="{ minWidth: col.minWidth || 'auto' }"
                >
                  <div class="flex items-center justify-between gap-2 cursor-pointer group">
                    <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300 transition-colors print:text-[7px] print:leading-tight print:whitespace-normal print:break-words">{{ col.label }}</p>
                    <svg class="h-3 w-3 text-gray-400 opacity-50 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                    </svg>
                  </div>
                </th>
              </template>
              <!-- Actions Header -->
              <th v-if="hasActions" class="md:sticky md:end-0 z-20 bg-slate-50 dark:bg-slate-900 border-s border-gray-200 dark:border-gray-700 px-4 py-3 text-center md:shadow-[0_0_8px_rgba(0,0,0,0.05)] dark:md:shadow-[0_0_8px_rgba(0,0,0,0.3)]" :style="{ width: actionsWidth }">
                <p class="font-medium text-gray-500 text-theme-xs dark:text-gray-400">{{ $t?.('common.actions') || 'إجراءات' }}</p>
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr
              v-for="(row, index) in data"
              :key="row[rowKey]"
              class="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group print:border-black print:border"
            >
              <!-- Data Columns -->
              <template v-for="col in columns" :key="col.key">
                <td
                  v-if="isColVisible(col.key)"
                  :class="['border-e border-gray-200 dark:border-gray-700 px-5 py-4 max-w-[150px] sm:max-w-[250px] truncate print:max-w-none print:whitespace-normal print:break-words print:overflow-visible print:text-wrap print:p-0.5 print:border-black print:border', col.tdClass || '']"
                  :title="row[col.key] ? String(row[col.key]) : ''"
                >
                  <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]" :index="index">
                    <p class="text-gray-500 text-theme-sm dark:text-gray-400 truncate print:whitespace-normal print:break-words print:overflow-visible print:text-wrap print:text-[7px] print:leading-tight">{{ row[col.key] ?? '—' }}</p>
                  </slot>
                </td>
              </template>

              <!-- Pinned Actions -->
              <td v-if="hasActions" class="md:sticky md:end-0 z-10 bg-slate-50 dark:bg-slate-900 group-hover:bg-slate-100 dark:group-hover:bg-slate-800 border-s border-gray-200 dark:border-gray-700 px-4 py-3 text-center transition-colors md:shadow-[0_0_8px_rgba(0,0,0,0.05)] dark:md:shadow-[0_0_8px_rgba(0,0,0,0.3)]" :style="{ width: actionsWidth }">
                <div class="flex items-center justify-center gap-1.5">
                  <slot name="actions" :row="row" />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="print:hidden">
        <TablePagination
          :currentPage="currentPage"
          :totalPages="totalPages"
          :totalCount="totalCount"
          :pageSize="pageSize"
          :visiblePages="computedVisiblePages"
          @change-page="(p: number) => $emit('change-page', p)"
          @change-page-size="(s: number) => $emit('change-page-size', s)"
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import ColumnsSelector from '@/components/common/ColumnsSelector.vue'
import TablePagination from '@/components/common/TablePagination.vue'

// ── Types ──────────────────────────────────────────────────
export interface DataTableColumn {
  key: string
  label: string
  minWidth?: string
  printWidth?: string
  class?: string
  tdClass?: string
}

export interface DataTableColumnGroup {
  label: string
  keys: string[]
  highlighted?: boolean
}

// ── Props ──────────────────────────────────────────────────
const props = withDefaults(defineProps<{
  columns: DataTableColumn[]
  columnGroups?: DataTableColumnGroup[]
  data: any[]
  rowKey: string
  loading?: boolean
  error?: string | null
  currentPage?: number
  totalPages?: number
  totalCount?: number
  pageSize?: number
  hasActions?: boolean
  actionsWidth?: string
  hasFilters?: boolean
  activeFilterCount?: number
  searchPlaceholder?: string
  loadingText?: string
  emptyTitle?: string
  emptyDescription?: string
}>(), {
  loading: false,
  error: null,
  currentPage: 1,
  totalPages: 1,
  totalCount: 0,
  pageSize: 50,
  hasActions: true,
  actionsWidth: '100px',
  hasFilters: false,
  activeFilterCount: 0,
  searchPlaceholder: 'بحث...',
  loadingText: 'جاري التحميل...',
  emptyTitle: 'لا توجد بيانات',
  emptyDescription: 'لم يتم العثور على نتائج مطابقة.',
})

// ── Events ─────────────────────────────────────────────────
const emit = defineEmits<{
  (e: 'search', query: string): void
  (e: 'refresh'): void
  (e: 'export'): void
  (e: 'change-page', page: number): void
  (e: 'change-page-size', size: number): void
}>()

// ── State ──────────────────────────────────────────────────
const searchQuery = ref('')
const filtersVisible = ref(false)
const tableContainerRef = ref<HTMLElement | null>(null)

// ── Column Visibility (internal reactive list for ColumnsSelector) ──
const internalColumns = reactive(
  props.columns.map(c => ({ key: c.key, name: c.label, visible: true }))
)

// Sync when parent columns change
watch(() => props.columns, (newCols) => {
  // Add new columns
  for (const col of newCols) {
    const existing = internalColumns.find(c => c.key === col.key)
    if (!existing) {
      internalColumns.push({ key: col.key, name: col.label, visible: true })
    }
  }
}, { deep: true })

function isColVisible(key: string): boolean {
  const col = internalColumns.find(c => c.key === key)
  return col ? col.visible : true
}

function visibleColsInGroup(keys: string[]): number {
  return keys.filter(k => isColVisible(k)).length
}

// ── Search ─────────────────────────────────────────────────
let searchTimer: any = null
function onSearchInput() {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    emit('search', searchQuery.value)
  }, 400)
}

// ── Pagination ─────────────────────────────────────────────
const computedVisiblePages = computed((): (number | string)[] => {
  const total = props.totalPages
  const current = props.currentPage
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

// ── Print (table only) ────────────────────────────────────
function handlePrint() {
  const container = tableContainerRef.value
  if (!container) return
  const table = container.querySelector('table')
  if (!table) return

  const printWin = window.open('', '_blank', 'width=1100,height=700')
  if (!printWin) return

  // Clone the table
  const clone = table.cloneNode(true) as HTMLElement
  
  // Remove the Actions column completely
  clone.querySelectorAll('[class*="sticky"]').forEach(el => el.remove())

  // Gather all stylesheets and inline styles to match the exact design
  const styles = Array.from(document.querySelectorAll('style, link[rel="stylesheet"]'))
    .map(el => el.outerHTML)
    .join('\n')

  printWin.document.write(`<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>طباعة الجدول</title>
${styles}
<style>
  @page { size: landscape; margin: 10mm; }
  body { background: white !important; padding: 20px; }
  /* Ensure SVGs or small elements render well */
  table { width: 100%; border-collapse: collapse; }
  @media print { 
    body { padding: 0; } 
    /* Force background colors to print */
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  }
</style>
</head>
<body class="bg-white text-gray-900">
  <div class="overflow-hidden border border-gray-200 rounded-xl">
    ${clone.outerHTML}
  </div>
</body>
</html>`)
  printWin.document.close()
  
  // Wait a little bit for styles to be applied before printing
  setTimeout(() => { 
    printWin.print()
    printWin.close() 
  }, 500)
}

// ── Expose for parent ──────────────────────────────────────
defineExpose({ isColVisible, filtersVisible })
</script>
