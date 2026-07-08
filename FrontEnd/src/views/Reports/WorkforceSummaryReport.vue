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
        <button @click="printReport" class="flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
          طباعة
        </button>
      </div>
    </div>

    <!-- Levels Tabs -->
    <div class="flex overflow-x-auto border-b border-gray-200 dark:border-gray-800 no-scrollbar print:hidden">
      <nav class="-mb-px flex space-x-8 rtl:space-x-reverse">
        <button
          v-for="level in levels"
          :key="level.id"
          @click="currentLevel = level.id"
          :class="[
            currentLevel === level.id
              ? 'border-brand-500 text-brand-600 dark:text-brand-400'
              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:border-gray-700',
            'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors'
          ]"
        >
          {{ level.name }}
        </button>
      </nav>
    </div>

    <!-- Report Container -->
    <div class="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden printable-area print:border-none print:shadow-none print:bg-transparent">
      <div class="p-4 md:p-6 print:p-0">
        <!-- Official Print Header -->
        <ReportHeader title="خلاصة القوة العاملة بحسب الرتبة" />
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
            <tr>
              <th rowspan="2" class="w-48 font-bold">الرتبة / {{ currentLevelName }}</th>
              <th :colspan="officerRanks.length" class="font-bold bg-group-1">الضباط</th>
              <th :colspan="ncoRanks.length" class="font-bold bg-group-2">الأفراد</th>
              <th rowspan="2" class="font-bold bg-gray-100 dark:bg-gray-800">الإجمالي</th>
            </tr>
            <tr>
              <th v-for="rank in officerRanks" :key="rank" class="w-12 text-xs bg-group-1">{{ rank }}</th>
              <th v-for="rank in ncoRanks" :key="rank" class="w-12 text-xs bg-group-2">{{ rank }}</th>
            </tr>
          </template>

          <!-- Table Body -->
          <template #body>
            <tr v-for="(row, idx) in filteredReportData" :key="idx">
              <td class="font-medium text-right bg-gray-50 dark:bg-gray-800/30">{{ row.unit_name }}</td>
              <td v-for="rank in officerRanks" :key="rank" :class="{'text-gray-400 dark:text-gray-600': !row.ranks[rank]}">
                {{ row.ranks[rank] || '' }}
              </td>
              <td v-for="rank in ncoRanks" :key="rank" :class="{'text-gray-400 dark:text-gray-600': !row.ranks[rank]}">
                {{ row.ranks[rank] || '' }}
              </td>
              <td class="font-bold bg-gray-50 dark:bg-gray-800/50">{{ row.total }}</td>
            </tr>
          </template>

          <!-- Table Footer -->
          <template #footer>
            <tr>
              <td class="text-right">الإجمالي الكلي</td>
              <td v-for="rank in officerRanks" :key="rank">{{ grandTotals[rank] || '' }}</td>
              <td v-for="rank in ncoRanks" :key="rank">{{ grandTotals[rank] || '' }}</td>
              <td class="text-brand-600 dark:text-brand-400">{{ overallTotal }}</td>
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
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportTable from '@/components/tables/ReportTable.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'

// Ranks Arrays based on the physical paper
const officerRanks = ['عميد', 'عقيد', 'مقدم', 'رائد', 'نقيب', 'ملازم أول', 'ملازم ثاني']
const ncoRanks = ['مساعد ١', 'مساعد ٢', 'مساعد', 'رقيب ١', 'رقيب ٢', 'عريف', 'جندي', 'حارس', 'مدني']
const totalColumns = computed(() => officerRanks.length + ncoRanks.length + 2)

// Levels
const levels = [
  { id: 'central', name: 'الإدارات المركزية (ديوان)' },
  { id: 'branch', name: 'الفروع الميدانية' },
  { id: 'district', name: 'أمن المديريات' },
  { id: 'security_admin', name: 'الإدارات الأمنية (المحافظات)' },
]

const currentLevel = ref('central')
const currentLevelName = computed(() => {
  const lvl = levels.find(l => l.id === currentLevel.value)
  return lvl ? lvl.name.split(' ')[0] + ' ' + (lvl.name.split(' ')[1] || '') : 'الجهة'
})

// State
const loading = ref(true)
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
    const res = await api.get('/personnel/reports/workforce-summary/', {
      params: { level: currentLevel.value }
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
  alert('ميزة التصدير لملف إكسل سيتم تفعيلها قريباً')
}
</script>

<style scoped>
@media print {
  @page {
    size: A4 portrait;
    margin: 1cm;
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
}
</style>
