<template>
  <admin-layout>
    <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4 print:hidden">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">خلاصة فئوية للقوة العاملة</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">تقرير إحصائي لعدد الأفراد النشطين موزعاً بحسب الفئة والجهات</p>
      </div>
      <div class="flex gap-2">
        <button @click="printReport" class="flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
          طباعة
        </button>
      </div>
    </div>

    <!-- Levels Tabs (Hidden in print) -->
    <div class="flex overflow-x-auto border-b border-gray-200 dark:border-gray-800 no-scrollbar print:hidden">
      <nav class="-mb-px flex gap-8">
        <button
          v-for="level in levels"
          :key="level.id"
          @click="currentLevel = level.id"
          :class="[
            currentLevel === level.id
              ? 'border-brand-500 text-brand-600 dark:text-brand-400'
              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:border-gray-700',
            'whitespace-nowrap border-b-2 py-4 px-4 text-sm font-medium transition-colors'
          ]"
        >
          {{ level.name }}
        </button>
      </nav>
    </div>

    <!-- Report Container -->
    <div class="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden printable-area print:border-none print:shadow-none print:bg-transparent">
      <div class="p-6 print:p-0">
        <!-- Official Print Header -->
        <ReportHeader title="خلاصة فئوية للقوة العاملة" />

        <ReportTable 
          :data="filteredReportData" 
          :loading="loading"
          loadingText="جاري تجميع البيانات..."
          emptyTitle="لا توجد بيانات"
          emptyDescription="لا توجد بيانات متاحة لهذا المستوى."
          
          :showRefresh="true"
          :showExport="true"
          :showPrint="true"
          :showSearch="true"
          searchPlaceholder="بحث في الوحدات والجهات..."
          v-model:searchQuery="searchQuery"
          @refresh="fetchReport"
          @export="exportExcel"
          @print="printReport"
        >
          <!-- Table Header -->
          <template #header>
            <tr class="border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
              <th rowspan="2" class="w-40 min-w-[160px] px-4 py-3 border-l border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 align-middle text-center font-bold">
                {{ currentLevel === 'all' ? 'السرية' : currentLevelName }}
              </th>
              <th :colspan="categories.length" class="px-4 py-2 border-l border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 align-middle text-center font-bold">
                تصنيف الوظائف
              </th>
              <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 align-middle text-center font-bold">
                الإجمالي
              </th>
            </tr>
            <tr class="border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
              <th v-for="cat in categories" :key="cat" class="px-4 py-2 border-l border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 align-middle text-center font-bold">
                {{ cat }}
              </th>
            </tr>
          </template>

          <!-- Table Body -->
          <template #body>
            <tr v-for="(row, idx) in filteredReportData" :key="idx" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors border-b border-gray-200 dark:border-gray-700">
              <td class="px-4 py-3 font-medium text-right bg-gray-50 dark:bg-gray-800/30 border-l border-gray-200 dark:border-gray-700 break-words">{{ row.unit_name }}</td>
              <td v-for="cat in categories" :key="cat" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700" :class="{'text-gray-300 dark:text-gray-700': !row.categories[cat]}">
                {{ row.categories[cat] || '-' }}
              </td>
              <td class="px-4 py-3 font-bold bg-gray-50 dark:bg-gray-800/50 border-l border-gray-200 dark:border-gray-700">{{ row.total }}</td>
            </tr>
          </template>

          <!-- Table Footer (Totals) -->
          <template #footer>
            <tr class="border-t-2 border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 print:text-black">
              <td class="px-4 py-3 text-right font-bold border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">الإجمالي الكلي</td>
              <td v-for="cat in categories" :key="cat" class="px-2 py-3 text-center font-bold border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">{{ grandTotals[cat] || '-' }}</td>
              <td class="px-4 py-3 text-center font-black text-lg border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">{{ overallTotal }}</td>
            </tr>
          </template>
        </ReportTable>
        
        <!-- Official Print Footer -->
        <ReportFooter />
      </div>
    </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportTable from '@/components/tables/ReportTable.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'

// Categories from backend data or fixed
const categories = ref<string[]>([])

const levels = [
  { id: 'all', name: 'الكل' },
  { id: 'central', name: 'الإدارات المركزية' },
  { id: 'branch', name: 'الفروع' },
  { id: 'district', name: 'شرطات المديريات' },
]

const currentLevel = ref('all')
const currentLevelName = computed(() => levels.find(l => l.id === currentLevel.value)?.name || '')

const loading = ref(false)
const reportData = ref<any[]>([])
const grandTotals = ref<Record<string, number>>({})
const searchQuery = ref('')

const filteredReportData = computed(() => {
  if (!searchQuery.value) return reportData.value
  const query = searchQuery.value.toLowerCase()
  return reportData.value.filter(row => 
    row.unit_name.toLowerCase().includes(query)
  )
})

const overallTotal = computed(() => {
  return reportData.value.reduce((acc, row) => acc + row.total, 0)
})

// Fetch Data
const fetchReport = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/categorical-summary/', {
      params: { level: currentLevel.value }
    })
    reportData.value = res.data.data
    grandTotals.value = res.data.totals
    
    // Extract unique categories from data but keep standard ones
    const standardCats = ['إدارية', 'ميدانية', 'فنية', 'تخصصية', 'حرفية']
    const cats = new Set<string>(standardCats)
    
    reportData.value.forEach(row => {
      Object.keys(row.categories).forEach(c => cats.add(c))
    })
    
    // Sort standard categories first, then others
    categories.value = Array.from(cats).sort((a, b) => {
      const idxA = standardCats.indexOf(a)
      const idxB = standardCats.indexOf(b)
      if (idxA !== -1 && idxB !== -1) return idxA - idxB
      if (idxA !== -1) return -1
      if (idxB !== -1) return 1
      return a.localeCompare(b)
    })
  } catch (error) {
    console.error('Error fetching report:', error)
  } finally {
    loading.value = false
  }
}

watch(currentLevel, fetchReport)

onMounted(() => {
  fetchReport()
})

// Print
const printReport = () => {
  window.print()
}

// Export to Excel (Placeholder)
const exportExcel = () => {
  alert('ميزة التصدير لملف إكسل سيتم تفعيلها قريباً')
}
</script>

<style scoped>
@media print {
  @page {
    size: A4 portrait;
    margin: 0.5cm;
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
    padding: 6px 4px !important;
    font-size: 13px !important;
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
  :deep(tfoot) {
    display: table-row-group !important;
  }
}
.bg-group-1 {
  background-color: rgba(243, 244, 246, 0.5);
}
.dark .bg-group-1 {
  background-color: rgba(31, 41, 55, 0.5);
}
</style>
