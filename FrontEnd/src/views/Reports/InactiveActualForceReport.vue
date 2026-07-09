<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Screen Header -->
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

      <!-- Print Content Wrapper -->
      <div class="printable-area print:block print:w-full print:absolute print:top-0 print:left-0 print:bg-white print:z-50">
        <!-- Print Header -->
        <report-header 
          :title="reportInfo.title" 
          :subtitle="reportInfo.subtitle" 
          :reportType="reportId"
        />

        <div class="mt-6">
          <detailed-report-table 
            :columns="columns" 
            :data="reportData" 
            :loading="loading" 
          />
        </div>
        
        <report-footer class="hidden print:block mt-8" />
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

const reportId = computed(() => route.params.id as string)

const reportInfo = computed(() => {
  if (reportId.value === '4b1') {
    return {
      title: 'ب - القوة العاملة الغير فعلية',
      subtitle: 'قوة متواجدة بدون عمل',
    }
  } else {
    return {
      title: 'ب - القوة العاملة الغير فعلية',
      subtitle: 'قوة الإحتياط',
    }
  }
})

const columns = [
  { key: 'index', label: 'م' },
  { key: 'rank', label: 'الرتبة' },
  { key: 'military_number', label: 'الرقم العسكري' },
  { key: 'full_name', label: 'الاسم' },
  { key: 'old_workplace', label: 'محل الخدمة السابق' },
  { key: 'old_service_type', label: 'نوع الخدمة السابقة' },
  { key: 'national_id', label: 'الرقم الوطني' },
  { key: 'qualification', label: 'المؤهل' },
  { key: 'notes', label: 'ملاحظات' }
]

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/audit-movement/', {
      params: { report_id: `report_${reportId.value}_mock` }
    }).catch(() => ({ data: { data: [] } }))
    
    reportData.value = res.data?.data || []
  } catch (error) {
    console.error(`Failed to fetch report`, error)
  } finally {
    loading.value = false
  }
}

const printReport = () => {
  window.print()
}

watch(reportId, () => {
  fetchData()
})

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* Inherits global print styles from main.css */
</style>
