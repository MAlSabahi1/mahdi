<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Header -->
      <report-header 
        title="كشف القوة العاملة فعلياً" 
        subtitle="يعرض القوة العاملة النشطة والمنتظمة في الدوام" 
        reportType="report_4"
      />

      <!-- Filters -->
      <div class="bg-white dark:bg-gray-900 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
        <div class="flex items-center gap-4">
          <div class="w-64">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">تصفية حسب المستوى:</label>
            <select 
              v-model="selectedLevel" 
              @change="fetchData"
              class="w-full rounded-lg border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
            >
              <option value="all">كل المستويات (الجمهورية)</option>
              <option value="central">الإدارات المركزية (ديوان)</option>
              <option value="branch">الفروع الميدانية</option>
              <option value="district">أمن المديريات</option>
            </select>
          </div>
        </div>
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
import { ref, onMounted } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import DetailedReportTable from '@/components/reports/DetailedReportTable.vue'

const selectedLevel = ref('all')
const reportData = ref([])
const loading = ref(false)

const columns = [
  { key: 'index', label: 'م' },
  { key: 'rank', label: 'الرتبة' },
  { key: 'full_name', label: 'الاسم الرباعي' },
  { key: 'military_number', label: 'الرقم العسكري' },
  { key: 'unit', label: 'الجهة' },
  { key: 'position', label: 'المنصب/العمل الحالي' },
  { key: 'notes', label: 'ملاحظات' }
]

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/active-force/', {
      params: { level: selectedLevel.value }
    })
    reportData.value = res.data.data || []
  } catch (error) {
    console.error('Failed to fetch active force report', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>
