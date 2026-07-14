<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Toolbar & Page Header -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 print:hidden">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-slate-100 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
            <svg class="h-8 w-8 text-slate-700 dark:text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">تصدير الخدمات والكشوفات الشهرية</h2>
            <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">تصدير كشوفات الإجراءات والخدمات الشهرية وتحديد الأعمدة المراد عرضها</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button @click="$router.push('/reports')" class="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700 transition-all focus:outline-none">
            <svg class="h-4.5 w-4.5 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            عودة للوحة التقارير
          </button>
        </div>
      </div>

      <!-- Filters Panel -->
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 print:hidden">
        <div class="flex flex-col md:flex-row items-end gap-4">
          <div class="w-full md:w-1/4">
            <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الشهر:</label>
            <select 
              v-model="selectedMonth" 
              class="w-full rounded-lg border-gray-300 bg-gray-50 px-3.5 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-colors"
            >
              <option value="">كل الأشهر</option>
              <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
            </select>
          </div>
          <div class="w-full md:w-1/4">
            <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">السنة:</label>
            <select 
              v-model="selectedYear" 
              class="w-full rounded-lg border-gray-300 bg-gray-50 px-3.5 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-colors"
            >
              <option value="">كل السنوات</option>
              <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>
          <div class="w-full md:w-1/4">
            <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">حالة الطلب:</label>
            <select 
              v-model="selectedStatus" 
              class="w-full rounded-lg border-gray-300 bg-gray-50 px-3.5 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-colors"
            >
              <option value="all">الكل</option>
              <option value="draft">مسودة</option>
              <option value="pending">قيد المراجعة</option>
              <option value="approved">معتمد نهائياً</option>
              <option value="rejected">مرفوض</option>
              <option value="committed">منفذ في النظام</option>
            </select>
          </div>
          <div class="w-full md:w-1/4">
            <button @click="fetchData" class="w-full flex items-center justify-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-bold text-white shadow-sm hover:bg-brand-700 transition-all">
              <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              تطبيق الفلتر
            </button>
          </div>
        </div>
      </div>

      <!-- Unified DataTable Component -->
      <div class="print:border-none print:shadow-none print:bg-transparent">
        
        <!-- Official Print Header (Hidden in Screen, Visible in Print) -->
        <div class="hidden print:block mb-6 w-full">
          <report-header 
            :title="`الكشف الشهري للخدمات والإجراءات - شهر ${selectedMonth || '-'} / ${selectedYear || '-'}`" 
            :subtitle="`البيانات المستخرجة للإجراءات وتعديلات الحالة - حالة الطلبات: ${getStatusLabel(selectedStatus)}`" 
            reportType="report_4"
          />
        </div>

        <DataTable
          class="printable-area"
          :columns="columns"
          :data="filteredData"
          rowKey="index"
          :loading="loading"
          :hasActions="false"
          :hasFilters="false"
          :pageSize="50"
          searchPlaceholder="بحث في المخرجات..."
          emptyTitle="لا توجد بيانات مصدرة"
          emptyDescription="لا توجد إجراءات أو خدمات تطابق معايير البحث المحددة."
          @search="(q) => searchQuery = q"
          @refresh="fetchData"
          @export="exportExcel"
        />

        <!-- Official Print Footer -->
        <div class="mt-8 hidden print:block w-full">
          <report-footer />
        </div>

      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import DataTable from '@/components/tables/DataTable.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'

const currentYear = new Date().getFullYear()
const availableYears = [currentYear, currentYear - 1, currentYear - 2, currentYear - 3]

const selectedMonth = ref<number | ''>(new Date().getMonth() + 1)
const selectedYear = ref<number | ''>(currentYear)
const selectedStatus = ref('all')
const searchQuery = ref('')
const loading = ref(false)
const reportData = ref<any[]>([])

const columns = [
  { key: 'index', label: 'م' },
  { key: 'rank', label: 'الرتبة' },
  { key: 'military_number', label: 'الرقم العسكري' },
  { key: 'full_name', label: 'الاسم' },
  { key: 'unit', label: 'محل الخدمة' },
  { key: 'service_type', label: 'نوع الإجراء' },
  { key: 'status', label: 'الحالة' },
  { key: 'created_at', label: 'تاريخ الإجراء' },
  { key: 'submitted_by', label: 'الرافع / المُنشئ' }
]

const getStatusLabel = (val: string) => {
  const map: Record<string, string> = {
    'all': 'الكل',
    'draft': 'مسودة',
    'pending': 'قيد المراجعة',
    'approved': 'معتمد نهائياً',
    'rejected': 'مرفوض',
    'committed': 'منفذ في النظام'
  }
  return map[val] || val
}

const filteredData = computed(() => {
  if (!searchQuery.value) return reportData.value
  const q = searchQuery.value.toLowerCase()
  return reportData.value.filter(item => 
    item.full_name?.toLowerCase().includes(q) ||
    item.military_number?.includes(q) ||
    item.service_type?.toLowerCase().includes(q)
  )
})

const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (selectedMonth.value) params.month = selectedMonth.value
    if (selectedYear.value) params.year = selectedYear.value
    if (selectedStatus.value !== 'all') params.status = selectedStatus.value

    const res = await api.get('/reports/detailed-reports/monthly-services/', { params })
    // Format date in client
    reportData.value = (res.data.data || []).map((item: any) => ({
      ...item,
      created_at: item.created_at ? new Date(item.created_at).toLocaleDateString('ar-SA') : '-'
    }))
  } catch (error) {
    console.error('Failed to fetch monthly services report', error)
  } finally {
    loading.value = false
  }
}

const exportExcel = () => {
  alert('ميزة التصدير إلى إكسل قيد التطوير حالياً وسيتم إطلاقها ضمن نظام التصدير المركزي الموحد.')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
@media print {
  @page {
    size: A4 landscape;
    margin: 0;
  }
  body > *:not(#app) { display: none !important; }
  html, body, #app, main, .admin-layout-content {
    height: auto !important;
    min-height: auto !important;
    overflow: visible !important;
    position: static !important;
  }
  .print\:hidden {
    display: none !important;
  }
  .printable-area {
    display: block !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 10mm !important;
  }
  /* Force custom table styling inside DataTable for printing */
  :deep(.printable-area table) {
    border: 2px solid #000 !important;
    width: 100% !important;
  }
  :deep(.printable-area th), :deep(.printable-area td) {
    border: 1px solid #000 !important;
    color: #000 !important;
  }
  :deep(.printable-area th) {
    background-color: #f3f4f6 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
</style>
