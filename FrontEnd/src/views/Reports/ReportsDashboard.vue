<template>
  <admin-layout>
    <div class="h-full bg-gray-50 dark:bg-gray-900 pb-20">
      
      <!-- Dashboard Header & Snapshot Button -->
      <div class="bg-white px-6 py-8 border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
        <div class="mx-auto max-w-7xl flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">وحدة التقارير والإحصائيات المركزية</h1>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              النماذج الرسمية المعتمدة (25 نموذجًا) المُجمّعة آلياً من قاعدة البيانات.
            </p>
          </div>
          
          <button
            @click="exportMonthlySnapshot"
            class="flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-brand-500/30 hover:bg-brand-700 hover:-translate-y-0.5 transition-all focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            تصدير اللقطة الشهرية الشاملة
          </button>
        </div>
      </div>

      <!-- Tabs Navigation -->
      <div class="sticky top-0 z-10 bg-gray-50/90 backdrop-blur-md border-b border-gray-200 dark:bg-gray-900/90 dark:border-gray-800 px-6">
        <div class="mx-auto max-w-7xl">
          <nav class="-mb-px flex gap-8 overflow-x-auto custom-scrollbar">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-brand-500 text-brand-600 dark:border-brand-400 dark:text-brand-400 font-bold'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:border-gray-600 dark:hover:text-gray-300 font-medium',
                'whitespace-nowrap border-b-2 py-4 px-4 text-sm font-medium transition-colors'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content (Cards Grid) -->
      <div class="mx-auto max-w-7xl px-6 py-8">
        
        <!-- Tab 1: Summaries -->
        <div v-show="activeTab === 'summaries'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ReportCard
            title="خلاصة القوة العاملة بحسب الرتبة"
            description="خلاصة عددية للقوة العاملة موزعة بحسب الرتب والجهات التنظيمية."
            reportType="خلاصة عددية"
            :totalRecords="12054"
            recordsLabel="فرد بالخدمة"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_1']?.status"
            @view="viewReport(1)"
            @request-export="requestExport('report_1', 'النموذج 1: خلاصة القوة العاملة بحسب الرتبة')"
            @download="downloadReport(requests['report_1'])"
          >
            <template #icon>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            </template>
          </ReportCard>

          <ReportCard
            title="خلاصة فئوية للقوة العاملة"
            description="خلاصة للفئات الوظيفية (تخصصي، ميداني، إداري، إلخ)."
            reportType="خلاصة فئوية"
            :totalRecords="84"
            recordsLabel="تصنيف"
            :isReady="true"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_2']?.status"
            @view="viewReport(2)"
            @request-export="requestExport('report_2', 'النموذج 2: خلاصة فئوية للقوة العاملة')"
            @download="downloadReport(requests['report_2'])"
          >
            <template #icon>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" /></svg>
            </template>
          </ReportCard>

          <ReportCard
            title="خلاصة القوة غير العاملة"
            description="خلاصة عددية للقوة غير العاملة بحسب الرتبة وأسباب عدم العمل."
            reportType="خلاصة عددية"
            :totalRecords="312"
            recordsLabel="فرد غير عامل"
            :isReady="true"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_3']?.status"
            @view="viewReport(3)"
            @request-export="requestExport('report_3', 'النموذج 3: خلاصة القوة غير العاملة')"
            @download="downloadReport(requests['report_3'])"
          >
            <template #icon>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
            </template>
          </ReportCard>
        </div>

        <!-- Tab 2: Active Force -->
        <div v-show="activeTab === 'active_force'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ReportCard
            title="كشف القوة العاملة فعليًا"
            description="الكشف التفصيلي الشامل لجميع الأفراد المتواجدين على رأس العمل."
            reportType="كشف تفصيلي"
            :totalRecords="12054"
            recordsLabel="فرد"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_4']?.status"
            @view="viewReport(4)"
            @request-export="requestExport('report_4', 'النموذج 4: كشف القوة العاملة فعليًا')"
            @download="downloadReport(requests['report_4'])"
          />
          <ReportCard
            title="ب1 - قوة متواجدة بدون عمل"
            description="كشف الأفراد التابعين للوحدة والمتواجدين بدون عمل."
            reportType="كشف تفصيلي"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_4b1']?.status"
            @view="viewReport('4b1')"
            @request-export="requestExport('report_4b1', 'النموذج 4ب1: متواجدة بدون عمل')"
            @download="downloadReport(requests['report_4b1'])"
          />
          <ReportCard
            title="ب2 - قوة الإحتياط"
            description="كشف الأفراد التابعين للوحدة في قوات الاحتياط."
            reportType="كشف تفصيلي"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_4b2']?.status"
            @view="viewReport('4b2')"
            @request-export="requestExport('report_4b2', 'النموذج 4ب2: قوة الاحتياط')"
            @download="downloadReport(requests['report_4b2'])"
          />
        </div>

        <!-- Tab 3: Temp Inactive Force -->
        <div v-show="activeTab === 'inactive_temp'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ReportCard
            title="كشف المرضى (مستشفى)"
            description="حصر الأفراد المتواجدين في المستشفى (قوة مؤقتاً غير عاملة)"
            reportType="النموذج (5)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_5']?.status"
            @view="viewReport(5)"
            @request-export="requestExport('report_5', 'النموذج 5: كشف المرضى')"
            @download="downloadReport(requests['report_5'])"
          />
          <ReportCard
            title="كشف المرافقين"
            description="حصر الأفراد المفرغين للمرافقة أو الحراسة لشخصيات"
            reportType="النموذج (6)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_6']?.status"
            @view="viewReport(6)"
            @request-export="requestExport('report_6', 'النموذج 6: كشف المرافقين')"
            @download="downloadReport(requests['report_6'])"
          />
          <ReportCard
            title="كشف المنتدبين"
            description="حصر الأفراد المنتدبين للعمل لدى جهات أخرى"
            reportType="النموذج (7)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_7']?.status"
            @view="viewReport(7)"
            @request-export="requestExport('report_7', 'النموذج 7: كشف المنتدبين')"
            @download="downloadReport(requests['report_7'])"
          />
          <ReportCard
            title="كشف الدارسين"
            description="حصر الأفراد المفرغين للدراسة الأكاديمية أو الدورات"
            reportType="النموذج (8)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_8']?.status"
            @view="viewReport(8)"
            @request-export="requestExport('report_8', 'النموذج 8: كشف الدارسين')"
            @download="downloadReport(requests['report_8'])"
          />
          <ReportCard
            title="كشف السجناء"
            description="حصر الأفراد الموقوفين أو المسجونين على ذمة قضايا"
            reportType="النموذج (9)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_9']?.status"
            @view="viewReport(9)"
            @request-export="requestExport('report_9', 'النموذج 9: كشف السجناء')"
            @download="downloadReport(requests['report_9'])"
          />
          <ReportCard
            title="كشف الإجازات"
            description="حصر الأفراد المتواجدين في إجازات رسمية مصرحة"
            reportType="النموذج (10)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_10']?.status"
            @view="viewReport(10)"
            @request-export="requestExport('report_10', 'النموذج 10: كشف الإجازات')"
            @download="downloadReport(requests['report_10'])"
          />
          <ReportCard
            title="كشف المفقودين"
            description="حصر الأفراد المفقودين (مؤقتاً)"
            reportType="النموذج (11)"
            :hasExportPermission="hasPermission"
            :exportRequestStatus="requests['report_11']?.status"
            @view="viewReport(11)"
            @request-export="requestExport('report_11', 'النموذج 11: كشف المفقودين')"
            @download="downloadReport(requests['report_11'])"
          />
        </div>

        <!-- Tab 4: Perm Inactive Force -->
        <div v-show="activeTab === 'inactive_perm'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ReportCard title="كشف كبار السن" description="بلوغ السن القانوني للتقاعد" reportType="النموذج (12)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_12']?.status" @view="viewReport(12)" @request-export="requestExport('report_12', 'النموذج 12: كبار السن')" @download="downloadReport(requests['report_12'])" />
          <ReportCard title="كشف إنهاء الخدمة" description="نهاية المدة القانونية" reportType="النموذج (13)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_13']?.status" @view="viewReport(13)" @request-export="requestExport('report_13', 'النموذج 13: إنهاء الخدمة')" @download="downloadReport(requests['report_13'])" />
          <ReportCard title="كشف مرشحين للتقاعد" description="مرشحين للتقاعد لأسباب مختلفة" reportType="النموذج (14)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_14']?.status" @view="viewReport(14)" @request-export="requestExport('report_14', 'النموذج 14: مرشحين تقاعد')" @download="downloadReport(requests['report_14'])" />
          <ReportCard title="كشف عدم اللياقة" description="أمراض وعجز طبي" reportType="النموذج (15)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_15']?.status" @view="viewReport(15)" @request-export="requestExport('report_15', 'النموذج 15: عدم لياقة')" @download="downloadReport(requests['report_15'])" />
          <ReportCard title="كشف شهداء ووفيات" description="الوفيات الطبيعية وشهداء الواجب" reportType="النموذج (16)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_16']?.status" @view="viewReport(16)" @request-export="requestExport('report_16', 'النموذج 16: شهداء ووفيات')" @download="downloadReport(requests['report_16'])" />
          <ReportCard title="كشف متقاعدين" description="القرار النهائي للتقاعد" reportType="النموذج (17)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_17']?.status" @view="viewReport(17)" @request-export="requestExport('report_17', 'النموذج 17: متقاعدين')" @download="downloadReport(requests['report_17'])" />
        </div>

        <!-- Tab 5: Audit and Movement -->
        <div v-show="activeTab === 'audit'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ReportCard title="الواصلين من الوزارة" description="حركة الواصلين خلال الشهر" reportType="النموذج (18)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_18']?.status" @view="viewReport(18)" @request-export="requestExport('report_18', 'النموذج 18: واصلين')" @download="downloadReport(requests['report_18'])" />
          <ReportCard title="العازمين للوزارة" description="حركة المغادرين إلى الوزارة" reportType="النموذج (19)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_19']?.status" @view="viewReport(19)" @request-export="requestExport('report_19', 'النموذج 19: عازمين')" @download="downloadReport(requests['report_19'])" />
          <ReportCard title="العازمين (مقارن)" description="كشف تفصيلي مقارن للمغادرين" reportType="النموذج (20)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_20']?.status" @view="viewReport(20)" @request-export="requestExport('report_20', 'النموذج 20: عازمين مقارن')" @download="downloadReport(requests['report_20'])" />
          <ReportCard title="انتداب للداخل" description="عاملين لدينا رواتبهم في جهات أخرى" reportType="النموذج (21)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_21']?.status" @view="viewReport(21)" @request-export="requestExport('report_21', 'النموذج 21: انتداب للداخل')" @download="downloadReport(requests['report_21'])" />
          <ReportCard title="انتداب للخارج" description="عاملين بالخارج رواتبهم لدينا" reportType="النموذج (22)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_22']?.status" @view="viewReport(22)" @request-export="requestExport('report_22', 'النموذج 22: انتداب للخارج')" @download="downloadReport(requests['report_22'])" />
          <ReportCard title="المطلوب تصحيحهم" description="كشف بأسماء المطلوب تصحيح أسمائهم" reportType="النموذج (23)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_23']?.status" @view="viewReport(23)" @request-export="requestExport('report_23', 'النموذج 23: تصحيح أسماء')" @download="downloadReport(requests['report_23'])" />
          <ReportCard title="الغياب المؤقت" description="مطلوب توقيف مرتباتهم" reportType="النموذج (24 أ)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_24a']?.status" @view="viewReport('24a')" @request-export="requestExport('report_24a', 'النموذج 24أ: الغياب المؤقت')" @download="downloadReport(requests['report_24a'])" />
          <ReportCard title="الفرار والغياب المستمر" description="انقطاع دائم وفرار" reportType="النموذج (24 ب)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_24b']?.status" @view="viewReport('24b')" @request-export="requestExport('report_24b', 'النموذج 24ب: الفرار')" @download="downloadReport(requests['report_24b'])" />
          <ReportCard title="الملتحقين بالعدوان" description="القائمة السوداء" reportType="النموذج (25)" :hasExportPermission="hasPermission" :exportRequestStatus="requests['report_25']?.status" @view="viewReport(25)" @request-export="requestExport('report_25', 'النموذج 25: ملتحقين بالعدوان')" @download="downloadReport(requests['report_25'])" />
        </div>

      </div>
    </div>

    <!-- Modals -->
    <ExportRequestModal 
      v-model:isOpen="isModalOpen" 
      :reportName="currentModalReportName" 
      @submit="handleExportSubmit"
    />
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportCard from '@/components/reports/ReportCard.vue'
import ExportRequestModal from '@/components/reports/ExportRequestModal.vue'

const router = useRouter()

// Temporary Auth Mock: Toggle this to test the Data Export Approval Workflow
const hasPermission = ref(false) 

const tabs = [
  { id: 'summaries', name: 'الخلاصات الإحصائية (1-3)' },
  { id: 'active_force', name: 'القوة العاملة (4-5)' },
  { id: 'inactive_temp', name: 'القوة غير العاملة مؤقتاً (6-11)' },
  { id: 'inactive_perm', name: 'القوة غير العاملة نهائياً (12-17)' },
  { id: 'audit', name: 'التدقيق وحركة القوة (18-25)' }
]

const activeTab = ref('summaries')

// Requests tracking state: mapping report_id -> ExportRequest object
const requests = ref<Record<string, any>>({})

// Modal state
const isModalOpen = ref(false)
const currentModalReportId = ref('')
const currentModalReportName = ref('')

import { onMounted } from 'vue'

const fetchRequests = async () => {
  try {
    const res = await api.get('/reports/export-requests/')
    // Handle both paginated and non-paginated responses
    const reqs = Array.isArray(res.data) ? res.data : (res.data.results || res.data.data || [])
    const map: Record<string, any> = {}
    // Get the latest request for each report
    reqs.forEach((r: any) => {
      // If we already have one, check if we should override. Usually we want the latest.
      map[r.report_id] = r
    })
    requests.value = map
  } catch (err) {
    console.error('Failed to fetch requests', err)
  }
}

onMounted(() => {
  fetchRequests()
})

const viewReport = (id: number | string) => {
  router.push(`/reports/view/${id}`)
}

const downloadReport = async (reqObj: any) => {
  if (reqObj && reqObj.status === 'APPROVED') {
    try {
      const url = `/reports/export-requests/${reqObj.id}/download/`
      const response = await api.get(url, { responseType: 'blob' })
      
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = `export_${reqObj.report_id}.xlsx`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    } catch (err) {
      console.error('Failed to download file', err)
      alert('فشل في تحميل الملف')
    }
  }
}

const requestExport = (reportId: string, reportName: string) => {
  currentModalReportId.value = reportId
  currentModalReportName.value = reportName
  isModalOpen.value = true
}

const handleExportSubmit = async (reason: string) => {
  try {
    const res = await api.post('/reports/export-requests/', {
      report_id: currentModalReportId.value,
      report_name: currentModalReportName.value,
      reason: reason
    })
    requests.value[currentModalReportId.value] = res.data
  } catch (error) {
    console.error('Failed to submit export request:', error)
    alert('حدث خطأ أثناء إرسال الطلب')
  }
}

const exportMonthlySnapshot = () => {
  if (!hasPermission.value) {
    requestExport('monthly_snapshot', 'الملف الرقمي الشهري الشامل (Excel)')
  } else {
    console.log('Exporting all sheets...')
  }
}
</script>
