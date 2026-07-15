<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Toolbar for filtering -->
      <month-filter 
        v-model="selectedMonth" 
        @change="fetchData" 
      />

      <!-- Header -->
      <report-header 
        :title="reportInfo.title" 
        :subtitle="reportInfo.subtitle" 
        :reportType="reportId"
        :selectedMonth="selectedMonth"
      />

      <!-- Data Table -->
      <detailed-report-table 
        :columns="columns" 
        :data="reportData" 
        :loading="loading" 
      />
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import DetailedReportTable from '@/components/reports/DetailedReportTable.vue'
import MonthFilter from '@/components/reports/MonthFilter.vue'

const route = useRoute()
const reportData = ref([])
const loading = ref(false)
const selectedMonth = ref('')

const reportId = computed(() => {
  const id = route.params.id as string
  return `report_${id}`
})

const reportDefinitions: Record<string, { title: string, subtitle: string, dynamicCols: any[] }> = {
  'report_12': {
    title: 'كشف كبار السن (بلوغ السن القانوني للتقاعد)',
    subtitle: 'قوة غير عاملة نهائياً',
    dynamicCols: [
      { key: 'birth_date', label: 'تاريخ الميلاد' },
      { key: 'join_date', label: 'تاريخ الالتحاق' },
      { key: 'personal_request', label: 'الإجراءات (طلب شخصي)' }
    ]
  },
  'report_13': {
    title: 'كشف إنهاء الخدمة (نهاية المدة القانونية)',
    subtitle: 'قوة غير عاملة نهائياً',
    dynamicCols: [
      { key: 'birth_date', label: 'تاريخ الميلاد' },
      { key: 'join_date', label: 'تاريخ الالتحاق' },
      { key: 'total_years', label: 'إجمالي سنوات الخدمة' },
      { key: 'person_request', label: 'الإجراءات (طلب المذكور)' }
    ]
  },
  'report_14': {
    title: 'كشف مرشحين للتقاعد',
    subtitle: 'قوة غير عاملة نهائياً',
    dynamicCols: [
      { key: 'reason', label: 'نوع الحالة (السبب)' },
      { key: 'birth_date', label: 'تاريخ الميلاد' },
      { key: 'join_date', label: 'تاريخ الالتحاق' },
      { key: 'procedures', label: 'الإجراءات' }
    ]
  },
  'report_15': {
    title: 'كشف عدم اللياقة (أمراض وعجز طبي)',
    subtitle: 'قوة غير عاملة نهائياً',
    dynamicCols: [
      { key: 'disease_type', label: 'نوع المرض' },
      { key: 'disability_ratio', label: 'نسبة العجز %' },
      { key: 'incident_date', label: 'تاريخ وقوعها' },
      { key: 'medical_source', label: 'مصدر القرار الطبي' },
      { key: 'incident_type', label: 'حالة العجز' } // طبيعية أم أثناء الواجب
    ]
  },
  'report_16': {
    title: 'كشف شهداء ووفيات',
    subtitle: 'قوة غير عاملة نهائياً',
    dynamicCols: [
      { key: 'case_type', label: 'نوع الحالة (شهيد/متوفى)' },
      { key: 'death_date', label: 'تاريخ الوفاة/الاستشهاد' },
      { key: 'incident_type', label: 'حالة وقوعها' } // طبيعية أم أثناء الواجب
    ]
  },
  'report_17': {
    title: 'كشف متقاعدين (القرار النهائي)',
    subtitle: 'قوة غير عاملة نهائياً',
    dynamicCols: [
      { key: 'birth_date', label: 'تاريخ الميلاد' },
      { key: 'join_date', label: 'تاريخ الالتحاق' },
      { key: 'decision_number', label: 'رقم القرار الوزاري' },
      { key: 'decision_date', label: 'تاريخ صدور القرار' }
    ]
  }
}

const reportInfo = computed(() => reportDefinitions[reportId.value] || { title: 'غير معروف', subtitle: '', dynamicCols: [] })

const columns = computed(() => {
  return [
    { key: 'index', label: 'م' },
    { key: 'rank', label: 'الرتبة' },
    { key: 'military_number', label: 'الرقم العسكري' },
    { key: 'full_name', label: 'الاسم الرباعي' },
    ...reportInfo.value.dynamicCols,
    { key: 'notes', label: 'ملاحظات' }
  ]
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/perm-inactive/', {
      params: { 
        report_id: reportId.value,
        month: selectedMonth.value || undefined
      }
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
</script>
