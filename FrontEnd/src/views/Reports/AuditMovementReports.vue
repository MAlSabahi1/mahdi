<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Header -->
      <report-header 
        :title="reportInfo.title" 
        :subtitle="reportInfo.subtitle" 
        :reportType="reportId"
      />

      <!-- Sub-Tabs for report_24 (Absence and AWOL) -->
      <div v-if="reportId === 'report_24a' || reportId === 'report_24b'" class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-2 flex gap-2 w-max">
        <router-link 
          :to="{ name: 'AuditMovementReports', params: { id: '24a' } }"
          class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="reportId === 'report_24a' ? 'bg-brand-50 text-brand-600 dark:bg-brand-900/30 dark:text-brand-400' : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-800'"
        >
          (أ) غياب مؤقت
        </router-link>
        <router-link 
          :to="{ name: 'AuditMovementReports', params: { id: '24b' } }"
          class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="reportId === 'report_24b' ? 'bg-brand-50 text-brand-600 dark:bg-brand-900/30 dark:text-brand-400' : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-800'"
        >
          (ب) غياب مستمر (فرار)
        </router-link>
      </div>

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

const reportId = computed(() => {
  const id = route.params.id as string
  return `report_${id}`
})

const reportDefinitions: Record<string, { title: string, subtitle: string, dynamicCols: any[] }> = {
  'report_18': {
    title: 'كشف الواصلين من الوزارة خلال الشهر',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'new_workplace', label: 'محل الخدمة الجديد لدينا' },
      { key: 'arrived_from', label: 'الجهة الواصل منها' },
      { key: 'start_date', label: 'تاريخ مباشرة العمل لدينا' }
    ]
  },
  'report_19': {
    title: 'كشف العازمين من الوحدة إلى الوزارة',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'old_workplace', label: 'محل الخدمة السابق لدينا' },
      { key: 'old_service_type', label: 'نوع الخدمة السابقة' },
      { key: 'transfer_date', label: 'تاريخ النقل الفعلي' },
      { key: 'transfer_reason', label: 'سبب النقل' }
    ]
  },
  'report_20': {
    title: 'كشف العازمين من الوحدة إلى الوزارة (التفصيلي المقارن)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'old_workplace', label: 'محل الخدمة السابق' },
      { key: 'old_service_type', label: 'نوع الخدمة السابقة' },
      { key: 'new_directed_workplace', label: 'محل الخدمة الموجه إليه' },
      { key: 'new_service_type', label: 'نوع الخدمة الجديدة' }
    ]
  },
  'report_21': {
    title: 'كشف العاملين لدينا ومرتباتهم في جهات أخرى (انتداب للداخل)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'current_workplace', label: 'محل الخدمة الحالي لدينا' },
      { key: 'actual_service_type', label: 'نوع الخدمة والعمل الفعلي' },
      { key: 'salary_source', label: 'جهة صرف المرتب' },
      { key: 'start_date', label: 'تاريخ مباشرة العمل لدينا' }
    ]
  },
  'report_22': {
    title: 'كشف العاملين في جهات أخرى ومرتباتهم لدينا (انتداب للخارج)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'old_workplace', label: 'محل الخدمة السابق لدينا' },
      { key: 'old_service_type', label: 'نوع الخدمة السابقة' },
      { key: 'transfer_date', label: 'تاريخ النقل للجهة الخارجية' },
      { key: 'external_delegate_target', label: 'الجهة الخارجية المنتدب إليها' }
    ]
  },
  'report_23': {
    title: 'كشف بأسماء المطلوب تصحيح أسماؤهم (كشف المطابقة)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'national_id', label: 'الرقم الوطني' },
      { key: 'full_name', label: 'الاسم الصحيح (حسب البطاقة)' },
      { key: 'wrong_name', label: 'الاسم الخطأ (حسب الكشف)' },
      { key: 'correction_target', label: 'المطلوب تصحيحه' }
    ]
  },
  'report_24a': {
    title: 'كشف الغياب - مطلوب توقيف مرتباتهم (انقطاع مؤقت)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'national_id', label: 'الرقم الوطني' },
      { key: 'stop_reason', label: 'سبب التوقيف/الانقطاع' },
      { key: 'absence_days', label: 'عدد أيام الغياب' }
    ]
  },
  'report_24b': {
    title: 'كشف الغياب المستمر (الفرار والانقطاع الدائم)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'national_id', label: 'الرقم الوطني' },
      { key: 'stop_reason', label: 'سبب التوقيف' },
      { key: 'continuous_absence_duration', label: 'مدة الغياب المستمر' }
    ]
  },
  'report_25': {
    title: 'كشف الملتحقين بالعدوان (القائمة السوداء)',
    subtitle: 'حركة التنقلات والتدقيق',
    dynamicCols: [
      { key: 'national_id', label: 'الرقم الوطني' },
      { key: 'reporter_entity', label: 'جهة البلاغ الأمنية' },
      { key: 'taken_procedures', label: 'الإجراءات المتخذة' }
    ]
  }
}

const reportInfo = computed(() => reportDefinitions[reportId.value] || { title: 'غير معروف', subtitle: '', dynamicCols: [] })

const columns = computed(() => {
  const baseCols = [
    { key: 'index', label: 'م' },
    { key: 'rank', label: 'الرتبة' },
    { key: 'military_number', label: 'الرقم العسكري' }
  ]
  
  // report_23 overrides full_name position
  if (reportId.value !== 'report_23') {
    baseCols.push({ key: 'full_name', label: 'الاسم' })
  }

  return [
    ...baseCols,
    ...reportInfo.value.dynamicCols,
    { key: 'notes', label: 'ملاحظات' }
  ]
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/audit-movement/', {
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
