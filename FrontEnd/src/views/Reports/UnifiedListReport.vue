<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Top Action Bar -->
      <div class="flex flex-wrap items-center justify-between gap-4 print:hidden">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">{{ reportInfo.title }}</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ reportInfo.subtitle }}</p>
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

      <div class="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden printable-area print:border-none print:shadow-none print:bg-transparent">
        <div class="p-6 print:p-0">
          <!-- Header -->
          <report-header 
            :title="reportInfo.title" 
            :subtitle="reportInfo.subtitle" 
            :reportType="reportId"
          />

          <!-- Data Table -->
          <detailed-report-table 
            :columns="columns" 
            :data="reportData" 
            :loading="loading" 
          />
          
          <report-footer class="mt-8" />
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'
import DetailedReportTable from '@/components/reports/DetailedReportTable.vue'

const route = useRoute()
const reportData = ref([])
const loading = ref(false)

// Determine the report ID from the URL param
const reportId = computed(() => {
  const id = route.params.id as string
  return `report_${id}`
})

const reportDefinitions: Record<string, { title: string, subtitle: string, hideUnit?: boolean, dynamicCols: any[] }> = {
  'report_5': {
    title: 'كشف بالقوة غير العاملة مؤقتاً مرضى لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'hospital', label: 'اسم المستشفى' },
      { key: 'entry_date', label: 'تاريخ الدخول' },
      { key: 'medical_report', label: 'التقرير الطبي' }
    ]
  },
  'report_6': {
    title: 'كشف بالقوة غير العاملة مؤقتاً مرافقين لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير عاملة مؤقتاً',
    hideUnit: true,
    dynamicCols: [
      { key: 'order_source', label: 'مصدر الامر' },
      { key: 'escort_name', label: 'اسم الشخصية' },
      { key: 'escort_position', label: 'منصب الشخصية' },
      { label: 'مدة التفريغ', children: [
        { key: 'duration_from', label: 'من' },
        { key: 'duration_to', label: 'إلى' }
      ]}
    ]
  },
  'report_7': {
    title: 'كشف بالقوة غير العاملة مؤقتاً منتدبين لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير عاملة مؤقتاً',
    hideUnit: true,
    dynamicCols: [
      { key: 'order_source', label: 'مصدر الامر' },
      { key: 'delegate_to', label: 'جهة الانتداب' },
      { key: 'delegate_purpose', label: 'الغرض من الانتداب' },
      { label: 'مدة الانتداب', children: [
        { key: 'duration_from', label: 'من' },
        { key: 'duration_to', label: 'إلى' }
      ]}
    ]
  },
  'report_8': {
    title: 'كشف بالقوة غير العاملة مؤقتاً مفرغين للدراسة لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير عاملة مؤقتاً',
    hideUnit: true,
    dynamicCols: [
      { key: 'study_type', label: 'نوع الدراسة' },
      { key: 'study_location', label: 'جهة الدراسة' },
      { key: 'order_number', label: 'رقم قرار الايفاد' },
      { label: 'مدة الدراسة', children: [
        { key: 'duration_from', label: 'من' },
        { key: 'duration_to', label: 'إلى' }
      ]}
    ]
  },
  'report_9': {
    title: 'كشف بالقوة غير العاملة مؤقتاً سجناء لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير عاملة مؤقتاً',
    hideUnit: true,
    dynamicCols: [
      { key: 'case_type', label: 'نوع القضية' },
      { key: 'arrest_date', label: 'تاريخ التوقيف' },
      { key: 'verdict_type', label: 'نوع الحكم' },
      { label: 'مدة الحكم', children: [
        { key: 'duration_from', label: 'من' },
        { key: 'duration_to', label: 'إلى' }
      ]}
    ]
  },
  'report_10': {
    title: 'كشف بالقوة غير العاملة مؤقتاً إجازات لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'vacation_type', label: 'نوع الاجازة' },
      { key: 'order_source', label: 'مصدر الامر' },
      { label: 'مدة الاجازة', children: [
        { key: 'duration_from', label: 'من' },
        { key: 'duration_to', label: 'إلى' }
      ]}
    ]
  },
  'report_11': {
    title: 'كشف بالقوة غير العاملة مؤقتاً مفقودين لشهر ..... ٢٠٢م',
    subtitle: 'قوة غير العاملة مؤقتاً',
    dynamicCols: [
      { key: 'missing_date', label: 'تاريخ الفقدان' },
      { label: 'الاجراءات', children: [
        { key: 'procedures_status', label: 'مستكمل/غير مستكمل' }
      ]}
    ]
  }
}

const reportInfo = computed(() => reportDefinitions[reportId.value] || { title: 'غير معروف', subtitle: '', dynamicCols: [] })

const columns = computed(() => {
  const cols = [
    { key: 'index', label: 'م' },
    { key: 'rank', label: 'الرتبة' },
    { key: 'military_number', label: 'الرقم العسكري' },
    { key: 'full_name', label: 'الاسم' },
  ]
  if (!reportInfo.value.hideUnit) {
    cols.push({ key: 'unit', label: 'محل الخدمة' })
  }
  return [
    ...cols,
    ...reportInfo.value.dynamicCols,
    { key: 'notes', label: 'ملاحظات' }
  ]
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/temp-inactive/', {
      params: { report_id: reportId.value }
    })
    reportData.value = res.data.data || []
  } catch (error) {
    console.error(`Failed to fetch report ${reportId.value}`, error)
  } finally {
    loading.value = false
  }
}

watch(reportId, () => {
  fetchData()
})

onMounted(() => {
  fetchData()
})

const printReport = () => {
  window.print()
}
</script>
