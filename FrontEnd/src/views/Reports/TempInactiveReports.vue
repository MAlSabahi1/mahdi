<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
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

const route = useRoute()
const reportData = ref([])
const loading = ref(false)

// Determine the report ID from the URL param
const reportId = computed(() => {
  const id = route.params.id as string
  return `report_${id}`
})

const reportDefinitions: Record<string, { title: string, subtitle: string, dynamicCols: any[] }> = {
  'report_5': {
    title: 'كشف المرضى المتواجدين في المستشفى',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'hospital', label: 'اسم المستشفى' },
      { key: 'entry_date', label: 'تاريخ الدخول' },
      { key: 'medical_report', label: 'التقرير الطبي' }
    ]
  },
  'report_6': {
    title: 'كشف بالقوة غير العاملة مؤقتاً (مرافقين)',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'escort_source', label: 'مصدر الأمر' },
      { key: 'escort_name', label: 'اسم الشخصية' },
      { key: 'duration_from', label: 'من تاريخ' },
      { key: 'duration_to', label: 'إلى تاريخ' }
    ]
  },
  'report_7': {
    title: 'كشف المنتدبين لدى جهات',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'delegate_to', label: 'جهة الانتداب' },
      { key: 'delegate_purpose', label: 'الغرض من الانتداب' },
      { key: 'duration_from', label: 'من تاريخ' },
      { key: 'duration_to', label: 'إلى تاريخ' }
    ]
  },
  'report_8': {
    title: 'كشف المفرغين للدراسة',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'study_type', label: 'نوع الدراسة' },
      { key: 'study_location', label: 'جهة الدراسة' },
      { key: 'duration_from', label: 'من تاريخ' },
      { key: 'duration_to', label: 'إلى تاريخ' }
    ]
  },
  'report_9': {
    title: 'كشف السجناء',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'case_type', label: 'نوع القضية' },
      { key: 'arrest_date', label: 'تاريخ التوقيف' },
      { key: 'verdict_type', label: 'نوع الحكم' },
      { key: 'duration_from', label: 'من تاريخ' },
      { key: 'duration_to', label: 'إلى تاريخ' }
    ]
  },
  'report_10': {
    title: 'كشف الإجازات الرسمية',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'vacation_type', label: 'نوع الإجازة' },
      { key: 'duration_from', label: 'من تاريخ' },
      { key: 'duration_to', label: 'إلى تاريخ' }
    ]
  },
  'report_11': {
    title: 'كشف المفقودين',
    subtitle: 'قوة غير عاملة مؤقتاً',
    dynamicCols: [
      { key: 'missing_date', label: 'تاريخ الفقدان' },
      { key: 'court_order', label: 'حكم شرعي بالفقدان' }
    ]
  }
}

const reportInfo = computed(() => reportDefinitions[reportId.value] || { title: 'غير معروف', subtitle: '', dynamicCols: [] })

const columns = computed(() => {
  return [
    { key: 'index', label: 'م' },
    { key: 'rank', label: 'الرتبة' },
    { key: 'full_name', label: 'الاسم الرباعي' },
    { key: 'military_number', label: 'الرقم العسكري' },
    { key: 'unit', label: 'الجهة/الإدارة' },
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
</script>
