<template>
  <admin-layout>
    <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4 print:hidden">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">خلاصة القوة العاملة بحسب الرتبة</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">تقرير إحصائي لعدد الأفراد النشطين موزعاً بحسب الرتب والجهات</p>
      </div>
      <div class="flex gap-2">
        
        <button @click="$router.push('/reports')" class="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700 transition-all focus:outline-none print:hidden">
          <svg class="h-4.5 w-4.5 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          عودة للوحة التقارير
        </button>
        <button @click="printReport" class="flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
          طباعة
        </button>
      </div>
    </div>

    <!-- Levels Tabs -->
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

    <!-- Filters Panel -->
    <month-filter 
      v-model="selectedMonth" 
      @change="fetchReport" 
    />

    <!-- Report Container -->
    <div class="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden printable-area print:border-2 print:border-black print:p-4 print:shadow-none print:bg-transparent">
      <div class="p-4 md:p-6 print:p-0">
        <!-- Official Print Header -->
        <ReportHeader 
          title="خلاصة القوة العاملة بحسب الرتبة" 
          :selectedMonth="selectedMonth" 
        />
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
            <tr class="border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 print:text-black">
              <th rowspan="2" class="w-40 p-0 border-l border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 relative align-middle overflow-hidden print:border-black print:border-2">
                <svg class="absolute inset-0 w-full h-full text-gray-400 dark:text-gray-600 print:text-black" preserveAspectRatio="none" viewBox="0 0 100 100">
                  <line x1="0" y1="0" x2="100" y2="100" stroke="currentColor" stroke-width="1.5"></line>
                </svg>
                <div class="relative w-full h-full min-h-[70px]">
                  <span class="absolute top-2 right-2 text-sm font-bold text-gray-700 dark:text-gray-300 print:text-black max-w-[70%] text-right leading-tight">{{ currentLevel === 'all' ? 'السرية' : currentLevelName }}</span>
                  <span class="absolute bottom-2 left-2 text-sm font-bold text-gray-900 dark:text-gray-100 print:text-black">الرتبة</span>
                </div>
              </th>
              <th :colspan="officerRanks.length" class="px-2 py-2 border-b border-l border-gray-200 dark:border-gray-700 font-bold bg-gray-100 dark:bg-gray-800 print:border-black print:border-2">الضباط</th>
              <th :colspan="ncoRanks.length" class="px-2 py-2 border-b border-l border-gray-200 dark:border-gray-700 font-bold bg-gray-100 dark:bg-gray-800 print:border-black print:border-2">الأفراد</th>
              <th rowspan="2" class="px-2 py-2 border-b border-gray-200 dark:border-gray-700 font-bold align-middle bg-gray-100 dark:bg-gray-800 print:border-black print:border-2">الإجمالي</th>
            </tr>
            <tr class="border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 print:text-black">
              <th v-for="rank in officerRanks" :key="rank" class="min-w-[40px] px-1 py-2 border-l border-gray-200 dark:border-gray-700 text-xs font-semibold bg-gray-50 dark:bg-gray-800/50 print:border-black print:border-2">{{ rank }}</th>
              <th v-for="rank in ncoRanks" :key="rank" class="min-w-[40px] px-1 py-2 border-l border-gray-200 dark:border-gray-700 text-xs font-semibold bg-gray-50 dark:bg-gray-800/50 print:border-black print:border-2">{{ rank }}</th>
            </tr>
          </template>

          <!-- Table Body -->
          <template #body>
            <tr v-for="(row, idx) in filteredReportData" :key="idx" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors border-b border-gray-200 dark:border-gray-700 print:border-black print:border-2 text-gray-900 dark:text-gray-100 print:text-black">
              <td class="px-2 py-2 font-bold text-right border-l border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/30 break-words print:border-black print:border-2">{{ row.unit_name }}</td>
              <td v-for="rank in officerRanks" :key="rank" class="px-1 py-2 text-center border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2" :class="{'text-gray-300 dark:text-gray-700 print:text-transparent': !row.ranks[rank]}">
                {{ row.ranks[rank] || '-' }}
              </td>
              <td v-for="rank in ncoRanks" :key="rank" class="px-1 py-2 text-center border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2" :class="{'text-gray-300 dark:text-gray-700 print:text-transparent': !row.ranks[rank]}">
                {{ row.ranks[rank] || '-' }}
              </td>
              <td class="px-2 py-2 font-bold text-center border-l border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 print:border-black print:border-2">{{ row.total }}</td>
            </tr>
          </template>

          <!-- Table Footer -->
          <template #footer>
            <tr class="border-t-2 border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 print:text-black">
              <td class="px-2 py-3 text-right font-bold border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">الإجمالي الكلي</td>
              <td v-for="rank in officerRanks" :key="rank" class="px-1 py-3 text-center font-bold border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">{{ grandTotals[rank] || '-' }}</td>
              <td v-for="rank in ncoRanks" :key="rank" class="px-1 py-3 text-center font-bold border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">{{ grandTotals[rank] || '-' }}</td>
              <td class="px-2 py-3 text-center font-black text-lg border-l border-gray-200 dark:border-gray-700 print:border-black print:border-2">{{ overallTotal }}</td>
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
import { ref, computed, watch, onMounted } from 'vue'
import { exportToCSV } from "@/utils/export"
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportTable from '@/components/tables/ReportTable.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'
import MonthFilter from '@/components/reports/MonthFilter.vue'

// Ranks Arrays based on the physical paper
const officerRanks = ['عميد', 'عقيد', 'مقدم', 'رائد', 'نقيب', 'ملازم أول', 'ملازم ثاني']
const ncoRanks = ['مساعد 1', 'مساعد 2', 'مساعد', 'رقيب 1', 'رقيب 2', 'عريف', 'جندي', 'حارس', 'مدني']
const totalColumns = computed(() => officerRanks.length + ncoRanks.length + 2)

// Levels
const levels = [
  { id: 'all', name: 'الكل' },
  { id: 'central', name: 'الإدارات المركزية' },
  { id: 'branch', name: 'الفروع' },
  { id: 'district', name: 'شرطات المديريات' },
]

const currentLevel = ref('all')
const currentLevelName = computed(() => {
  const lvl = levels.find(l => l.id === currentLevel.value)
  return lvl ? lvl.name.split(' ')[0] + ' ' + (lvl.name.split(' ')[1] || '') : 'الجهة'
})

// State
const loading = ref(true)
const reportData = ref<any[]>([])
const grandTotals = ref<Record<string, number>>({})
const searchQuery = ref('')
const selectedMonth = ref('')

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
    const res = await api.get('/personnel/reports/workforce-summary/', {
      params: { 
        level: currentLevel.value,
        month: selectedMonth.value || undefined
      }
    })
    reportData.value = res.data.data
    grandTotals.value = res.data.totals
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
  exportToCSV([], reportData.value, 'WorkforceSummaryReport_Export.csv')
}
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
    box-shadow: none !important;
  }
  /* Perfect Print Grid */
  :deep(table) {
    width: 100% !important;
    border-collapse: collapse !important;
    border: 2px solid black !important;
  }
  :deep(th), :deep(td) {
    padding: 2px 2px !important;
    font-size: 10px !important;
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
</style>
