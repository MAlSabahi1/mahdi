<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <div class="flex flex-wrap items-center justify-between gap-4 print:hidden">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">كشف بالقوة غير العاملة عدم اللياقة (أمراض ومشوهين)</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">نموذج رقم (١٥)</p>
        </div>
        <div class="flex gap-2">
          <button @click="printReport" class="flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
            طباعة
          </button>
        </div>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden printable-area print:border-none print:shadow-none print:bg-transparent">
        <div class="p-6 print:p-0">
          <ReportHeader title="كشف بالقوة غير العاملة عدم اللياقة (أمراض ومشوهين)" />

          <ReportTable 
            :data="filteredReportData" 
            :loading="loading"
            loadingText="جاري تجميع البيانات..."
            emptyTitle="لا توجد بيانات مطابقة"
            emptyDescription="لا يوجد حالات عدم لياقة مسجلة."
            
            :showRefresh="true"
            :showExport="true"
            :showPrint="true"
            :showSearch="true"
            searchPlaceholder="بحث بالاسم أو الرقم العسكري..."
            v-model:searchQuery="searchQuery"
            @refresh="fetchData"
            @export="exportExcel"
            @print="printReport"
          >
            <template #header>
              <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800">
                <th rowspan="2" class="px-2 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center w-12">م</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">الرتبة</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">الرقم العسكري</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">الاسم</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">نوع المرض</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">نسبة العجز</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">تاريخ وقوعها</th>
                <th rowspan="2" class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-center">مصدر القرار</th>
                <th colspan="2" class="px-4 py-2 border-b border-l border-gray-200 dark:border-gray-700 font-bold text-center bg-blue-50/50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300">حالة وقوعها</th>
                <th rowspan="2" class="px-4 py-3 font-bold text-center">ملاحظات</th>
              </tr>
              <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
                <th class="px-3 py-2 border-l border-gray-200 dark:border-gray-700 text-sm font-semibold text-center w-24">أثناء الواجب</th>
                <th class="px-3 py-2 border-l border-gray-200 dark:border-gray-700 text-sm font-semibold text-center w-24">طبيعية</th>
              </tr>
            </template>

            <template #body>
              <tr v-for="(row, idx) in filteredReportData" :key="row.index" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors border-b border-gray-200 dark:border-gray-700">
                <td class="px-2 py-3 text-center border-l border-gray-200 dark:border-gray-700 font-mono text-gray-500">{{ row.index }}</td>
                <td class="px-4 py-3 text-center border-l border-gray-200 dark:border-gray-700">
                  <span class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 dark:bg-gray-800 dark:text-gray-300 ring-1 ring-inset ring-gray-600/10">{{ row.rank }}</span>
                </td>
                <td class="px-4 py-3 text-center border-l border-gray-200 dark:border-gray-700 font-mono">{{ row.military_number }}</td>
                <td class="px-4 py-3 font-bold text-right border-l border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">{{ row.full_name }}</td>
                <td class="px-4 py-3 text-center border-l border-gray-200 dark:border-gray-700">{{ row.disease_type || '-' }}</td>
                <td class="px-4 py-3 text-center border-l border-gray-200 dark:border-gray-700 font-mono">{{ row.disability_ratio || '-' }}</td>
                <td class="px-4 py-3 text-center border-l border-gray-200 dark:border-gray-700 font-mono">{{ row.incident_date || '-' }}</td>
                <td class="px-4 py-3 text-center border-l border-gray-200 dark:border-gray-700">{{ row.medical_source || '-' }}</td>
                
                <td class="px-3 py-3 text-center border-l border-gray-200 dark:border-gray-700">
                  <span v-if="row.incident_type?.includes('واجب')">✔</span>
                </td>
                <td class="px-3 py-3 text-center border-l border-gray-200 dark:border-gray-700">
                  <span v-if="row.incident_type?.includes('طبيع')">✔</span>
                </td>
                
                <td class="px-4 py-3 text-right text-gray-600 dark:text-gray-400 text-sm">{{ row.notes || '-' }}</td>
              </tr>
            </template>
          </ReportTable>
          
          <div class="mt-8 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700 print:border-none print:bg-transparent">
            <h4 class="font-bold text-gray-800 dark:text-white mb-2 text-lg print:text-black flex items-center gap-2">
              <span class="bg-red-600 text-white px-3 py-1 rounded-full text-sm print:border print:border-black print:text-black print:bg-white">توضيح</span>
            </h4>
            <ul class="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300 print:text-black">
              <li><strong>نوع المرض:</strong> حالة الفرد بحسب القرار الطبي.</li>
              <li><strong>نسبة العجز:</strong> النسبة المئوية للعجز بحسب القرار الطبي.</li>
              <li><strong>مصدر القرار:</strong> جهة إصدار القرار الطبي.</li>
              <li><strong>حالة وقوعها:</strong> وقوع الحالة أثناء الواجب أم طبيعية.</li>
            </ul>
          </div>
          
          <ReportFooter />
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportTable from '@/components/tables/ReportTable.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'

const reportData = ref<any[]>([])
const loading = ref(false)
const searchQuery = ref('')

const filteredReportData = computed(() => {
  if (!searchQuery.value) return reportData.value
  const query = searchQuery.value.toLowerCase()
  return reportData.value.filter(row => 
    row.full_name?.toLowerCase().includes(query) || 
    row.military_number?.toLowerCase().includes(query)
  )
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/perm-inactive/', {
      params: { report_id: 'report_15' }
    })
    reportData.value = res.data.data || []
  } catch (error) {
    console.error('Failed to fetch report 15', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

const printReport = () => {
  window.print()
}

const exportExcel = () => {
  alert('ميزة التصدير لملف إكسل سيتم تفعيلها قريباً')
}
</script>

<style scoped>
@media print {
  @page {
    size: A4 landscape;
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
