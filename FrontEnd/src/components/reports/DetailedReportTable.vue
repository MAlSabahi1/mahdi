<template>
  <div class="bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden">
    <div class="overflow-x-auto max-h-[600px]">
      <table class="w-full text-right text-sm">
        <thead class="bg-slate-50 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 sticky top-0 shadow-sm z-10 print:text-black print:static">
          <!-- Row 1 -->
          <tr>
            <th 
              v-for="(col, idx) in columns" 
              :key="'h1-'+idx" 
              class="px-3 py-3.5 font-bold whitespace-nowrap bg-slate-50 dark:bg-slate-800 border-b border-l border-slate-200 dark:border-slate-700 text-center align-middle text-sm"
              :rowspan="col.children ? 1 : (hasNestedHeaders ? 2 : 1)"
              :colspan="col.children ? col.children.length : 1"
            >
              {{ col.label }}
            </th>
          </tr>
          <!-- Row 2 (Optional) -->
          <tr v-if="hasNestedHeaders">
            <template v-for="(col, idx) in columns" :key="'h2-outer-'+idx">
              <th 
                v-if="col.children"
                v-for="(child, cIdx) in col.children" 
                :key="'h2-inner-'+cIdx"
                class="px-3 py-2 text-xs font-bold whitespace-nowrap bg-slate-100 dark:bg-slate-800/70 border-b border-l border-slate-200 dark:border-slate-700 text-center"
              >
                {{ child.label }}
              </th>
            </template>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
          <tr v-for="(row, rIdx) in data" :key="row.index || rIdx" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors border-b border-slate-200 dark:border-slate-700">
            <td v-for="col in flatColumns" :key="col.key" class="px-3 py-2.5 whitespace-nowrap text-center border-l border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300">
              <template v-if="col.key === 'index'">
                <span class="font-bold text-slate-500 dark:text-slate-400 font-mono">{{ row[col.key] || (rIdx + 1) }}</span>
              </template>
              <template v-else-if="col.key === 'full_name'">
                <span class="font-bold text-slate-900 dark:text-white">{{ row[col.key] }}</span>
              </template>
              <template v-else-if="col.key === 'rank'">
                <span class="inline-flex items-center rounded-md bg-slate-100 px-2.5 py-1 text-xs font-bold text-slate-800 dark:bg-slate-800 dark:text-slate-200 ring-1 ring-inset ring-slate-600/10 print:ring-0 print:bg-transparent print:p-0">
                  {{ row[col.key] }}
                </span>
              </template>
              <template v-else-if="col.key === 'military_number' || col.key === 'national_id'">
                <span class="font-mono">{{ row[col.key] || '-' }}</span>
              </template>
              <template v-else>
                {{ row[col.key] || '-' }}
              </template>
            </td>
          </tr>
          <tr v-if="data.length === 0 && !loading">
            <td :colspan="flatColumns.length" class="px-6 py-12 text-center text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-3 print:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              لا توجد بيانات مطابقة
            </td>
          </tr>
          <tr v-if="loading">
            <td :colspan="flatColumns.length" class="px-6 py-12 text-center text-gray-500">
              <svg class="animate-spin mx-auto h-8 w-8 text-brand-500 mb-3 print:hidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              جاري تحميل البيانات...
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="!loading && data.length > 0" class="bg-slate-50 dark:bg-slate-800/80 px-5 py-4 border-t border-slate-200 dark:border-slate-700 flex justify-between items-center text-sm font-medium text-slate-600 dark:text-slate-400 print:hidden">
      <span>إجمالي الأفراد المعروضين: <strong class="text-slate-900 dark:text-white text-base">{{ data.length }}</strong></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  columns: any[]
  data: any[]
  loading: boolean
}>()

const hasNestedHeaders = computed(() => {
  return props.columns.some(col => col.children && col.children.length > 0)
})

const flatColumns = computed(() => {
  const result: any[] = []
  props.columns.forEach(col => {
    if (col.children && col.children.length > 0) {
      result.push(...col.children)
    } else {
      result.push(col)
    }
  })
  return result
})
</script>

<style scoped>
@media print {
  @page {
    size: A4 landscape !important;
    margin: 0.5cm !important;
  }
  body * {
    visibility: hidden;
  }
  .printable-area, .printable-area * {
    visibility: visible;
  }
  .printable-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    border: none !important;
    box-shadow: none !important;
  }
  /* Perfect Print Grid */
  :deep(table) {
    width: 100% !important;
    border-collapse: collapse !important;
    border: 2px solid black !important;
  }
  :deep(th), :deep(td) {
    padding: 4px 4px !important;
    font-size: 11px !important;
    border: 1px solid black !important;
    color: black !important;
  }
  :deep(th) {
    background-color: #f3f4f6 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  :deep(tr) {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
  :deep(thead) {
    display: table-header-group !important;
  }
}
</style>
