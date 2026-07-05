<template>
  <div class="relative overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    
    <!-- Header / Title Slot (Optional) -->
    <div v-if="$slots.header" class="px-5 py-4 border-b border-gray-200 dark:border-gray-800">
      <slot name="header"></slot>
    </div>

    <!-- Loading overlay for subsequent fetches -->
    <div v-if="loading && data && data.length > 0" class="absolute inset-0 z-10 bg-white/60 dark:bg-gray-900/60 flex items-center justify-center backdrop-blur-[1px]">
      <svg class="h-6 w-6 animate-spin text-brand-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full w-full text-start border-collapse">
        <thead>
          <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
            <template v-for="col in columns" :key="col.key">
              <th
                :class="['border-e border-gray-200 dark:border-gray-700 px-5 py-3 text-start whitespace-nowrap last:border-e-0', col.class || '']"
                :style="{ minWidth: col.minWidth || 'auto' }"
                @click="col.sortable !== false ? toggleSort(col.key) : null"
              >
                <div :class="['flex items-center gap-2', col.sortable !== false ? 'cursor-pointer group justify-between' : '']">
                  <slot :name="`header-${col.key}`" :col="col">
                    <p :class="['font-medium text-theme-xs transition-colors', col.sortable !== false ? 'text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300' : 'text-gray-500 dark:text-gray-400']">{{ col.label }}</p>
                  </slot>
                  <svg v-if="col.sortable !== false" :class="['h-3 w-3 transition-opacity', sortCol === col.key ? 'text-brand-500 opacity-100' : 'text-gray-400 opacity-0 group-hover:opacity-50']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path v-if="sortCol !== col.key || sortAsc" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 15l-4 4-4-4m0-6l4-4 4 4" />
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
          <tr v-if="loading && (!data || data.length === 0)">
            <td :colspan="hasActions ? columns.length + 1 : columns.length" class="px-5 py-20 text-center">
              <div class="flex flex-col items-center justify-center">
                <svg class="mb-3 h-8 w-8 animate-spin text-brand-500" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-theme-sm font-medium text-gray-500 dark:text-gray-400">{{ loadingText }}</span>
              </div>
            </td>
          </tr>

          <tr v-else-if="!data || data.length === 0">
            <td :colspan="hasActions ? columns.length + 1 : columns.length" class="px-5 py-20 text-center">
              <div class="flex flex-col items-center justify-center">
                <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                  <svg class="h-7 w-7 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                </div>
                <h3 class="text-theme-sm font-semibold text-gray-900 dark:text-white">{{ emptyTitle }}</h3>
                <p class="mt-1 text-theme-xs text-gray-500 dark:text-gray-400 max-w-sm">{{ emptyDescription }}</p>
              </div>
            </td>
          </tr>

          <template v-else>
            <tr
              v-for="row in displayData"
              :key="row[rowKey]"
              class="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
            >
              <!-- Data Columns -->
              <template v-for="col in columns" :key="col.key">
                <td
                  :class="['border-e border-gray-200 dark:border-gray-700 px-5 py-4 max-w-[150px] sm:max-w-[250px] truncate last:border-e-0', col.tdClass || '']"
                  :title="row[col.key] ? String(row[col.key]) : ''"
                >
                  <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                    <p class="text-gray-500 text-theme-sm dark:text-gray-400 truncate">{{ row[col.key] ?? '—' }}</p>
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
          </template>
        </tbody>
      </table>
    </div>

    <!-- Footer Slot -->
    <div v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

export interface BasicTableColumn {
  key: string
  label: string
  class?: string
  tdClass?: string
  minWidth?: string
  sortable?: boolean
}

const props = withDefaults(defineProps<{
  columns: BasicTableColumn[]
  data: any[]
  rowKey?: string
  loading?: boolean
  hasActions?: boolean
  actionsWidth?: string
  loadingText?: string
  emptyTitle?: string
  emptyDescription?: string
}>(), {
  rowKey: 'id',
  loading: false,
  hasActions: false,
  actionsWidth: '100px',
  loadingText: 'جاري التحميل...',
  emptyTitle: 'لا توجد بيانات',
  emptyDescription: 'الجدول فارغ.'
})

const sortCol = ref('')
const sortAsc = ref(true)

function toggleSort(key: string) {
  if (sortCol.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortCol.value = key
    sortAsc.value = true
  }
}

const displayData = computed(() => {
  if (!sortCol.value) return props.data
  return [...props.data].sort((a, b) => {
    const valA = a[sortCol.value]
    const valB = b[sortCol.value]
    if (valA === valB) return 0
    if (valA == null) return sortAsc.value ? 1 : -1
    if (valB == null) return sortAsc.value ? -1 : 1
    
    if (typeof valA === 'string' && typeof valB === 'string') {
      return sortAsc.value ? valA.localeCompare(valB) : valB.localeCompare(valA)
    }
    return sortAsc.value ? (valA > valB ? 1 : -1) : (valA > valB ? -1 : 1)
  })
})
</script>
