  <template>
    <component :is="isEmbedded ? 'div' : AdminLayout">
      <div :class="isEmbedded ? 'embedded-report-view' : 'standalone-report-page space-y-6 pb-20 print:pb-0 print:space-y-0'">
        <!-- Screen Header -->
        <div v-if="!isEmbedded" class="flex flex-wrap items-center justify-between gap-4 print:hidden">
          <div>
            <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">{{ reportInfo.title }}</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ reportInfo.subtitle }}</p>
          </div>
          
          <month-filter 
            v-model="selectedMonth" 
            @change="fetchData" 
          />

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
        <div :class="isEmbedded ? '' : 'rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden printable-area print:overflow-visible print:border-none print:shadow-none print:bg-transparent'">
          <div :class="isEmbedded ? 'p-0' : 'p-6 print:p-0'">
            <!-- Print Header -->
            <report-header 
              :title="reportInfo.title" 
              :subtitle="reportInfo.subtitle" 
              :reportType="reportId"
              :selectedMonth="selectedMonth"
            />

            <!-- Sub-Tabs for report_24 (Absence and AWOL) -->
            <div v-if="!isEmbedded && (reportId === 'report_24a' || reportId === 'report_24b')" class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-2 flex gap-2 w-max print:hidden mb-4">
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
            
            <report-footer class="mt-8" />
          </div>
        </div>
      </div>
    </component>
  </template>

  <script setup lang="ts">
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import api from '@/lib/api'
  import AdminLayout from '@/components/layout/AdminLayout.vue'
  import ReportHeader from '@/components/reports/ReportHeader.vue'
  import ReportFooter from '@/components/reports/ReportFooter.vue'
  import DetailedReportTable from '@/components/reports/DetailedReportTable.vue'
  import MonthFilter from '@/components/reports/MonthFilter.vue'

  const props = withDefaults(defineProps<{
    isEmbedded?: boolean
    reportIdProp?: string
    monthProp?: string
  }>(), {
    isEmbedded: false,
    reportIdProp: '',
    monthProp: ''
  })

  const route = useRoute()
  const reportData = ref([])
  const loading = ref(false)
  const selectedMonth = ref('')

  const reportId = computed(() => {
    if (props.reportIdProp) return `report_${props.reportIdProp}`
    const id = route.params.id as string
    return `report_${id}`
  })

  const reportDefinitions: Record<string, { title: string, subtitle: string, fullCols: any[] }> = {
    'report_19': {
      title: 'كشف العازمين من الوحدة إلى الوزارة',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'الرتبة' },
        { key: 'military_number', label: 'الرقم العسكري' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'old_workplace', label: 'محل الخدمة السابق' },
        { key: 'old_service_type', label: 'نوع الخدمة' },
        { key: 'new_directed_workplace', label: 'محل الخدمة الحالي' },
        { key: 'new_service_type', label: 'نوع الخدمة' },
        { key: 'transfer_date', label: 'تاريخ النقل' },
        { key: 'transfer_reason', label: 'سبب النقل' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_20': {
      title: 'كشف العازمين من الوحدة إلى الوزارة (التفصيلي المقارن)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'الرتبة' },
        { key: 'military_number', label: 'الرقم العسكري' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'old_workplace', label: 'محل الخدمة السابق' },
        { key: 'old_service_type', label: 'نوع الخدمة السابقة' },
        { key: 'new_directed_workplace', label: 'محل الخدمة الموجه إليه' },
        { key: 'new_service_type', label: 'نوع الخدمة الجديدة' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_21': {
      title: 'كشف العاملين لدينا ومرتباتهم في جهات أخرى (انتداب للداخل)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'الرتبة' },
        { key: 'military_number', label: 'الرقم العسكري' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'current_workplace', label: 'محل الخدمة' },
        { key: 'actual_service_type', label: 'نوع الخدمة' },
        { key: 'salary_source', label: 'جهة المرتب' },
        { key: 'start_date', label: 'تاريخ المباشرة' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_22': {
      title: 'كشف العاملين في جهات أخرى ومرتباتهم لدينا (انتداب للخارج)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'الرتبة' },
        { key: 'military_number', label: 'الرقم العسكري' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'old_workplace', label: 'محل الخدمة السابق' },
        { key: 'old_service_type', label: 'نوع الخدمة' },
        { key: 'transfer_date', label: 'تاريخ النقل' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_23': {
      title: 'كشف بأسماء المطلوب تصحيح أسماؤهم (كشف المطابقة)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'الرتبة' },
        { key: 'military_number', label: 'الرقم العسكري' },
        { key: 'full_name', label: 'الاسم الصحيح' },
        { key: 'wrong_name', label: 'الاسم الخطأ' },
        { key: 'correction_target', label: 'المطلوب تصحيحه' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_24a': {
      title: 'كشف الغياب المطلوب توقيف مرتباتهم (انقطاع مؤقت)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'رتبة' },
        { key: 'military_number', label: 'رقم عسكري' },
        { key: 'national_id', label: 'الرقم الوطني' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'stop_reason', label: 'سبب التوقيف' },
        { key: 'absence_days', label: 'عدد أيام الغياب' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_24b': {
      title: 'كشف الغياب المستمر (الفرار والانقطاع الدائم)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'رتبة' },
        { key: 'military_number', label: 'رقم عسكري' },
        { key: 'national_id', label: 'الرقم الوطني' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'stop_reason', label: 'سبب التوقيف' },
        { key: 'continuous_absence_duration', label: 'مدة الغياب' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    },
    'report_25': {
      title: 'كشف الملتحقين بالعدوان (القائمة السوداء)',
      subtitle: 'حركة التنقلات والتدقيق',
      fullCols: [
        { key: 'index', label: 'م' },
        { key: 'rank', label: 'رتبة' },
        { key: 'military_number', label: 'رقم عسكري' },
        { key: 'national_id', label: 'الرقم الوطني' },
        { key: 'full_name', label: 'الاسم' },
        { key: 'reporter_entity', label: 'جهة البلاغ' },
        { key: 'taken_procedures', label: 'الإجراءات المتخذة' },
        { key: 'notes', label: 'ملاحظات' }
      ]
    }
  }

  const reportInfo = computed(() => reportDefinitions[reportId.value] || { title: 'غير معروف', subtitle: '', fullCols: [] })

  const columns = computed(() => reportInfo.value.fullCols)

  const fetchData = async () => {
    loading.value = true
    try {
      const res = await api.get('/reports/detailed-reports/audit-movement/', {
        params: { 
          report_id: reportId.value,
          month: selectedMonth.value || undefined
        }
      })
      
      let data = res.data.data || []
      
      // معالجة خاصة لبيانات كشف المطابقة (تصحيح الأسماء) لتنظيف الملاحظات وعكس الاسم الصحيح/الخطأ
      if (reportId.value === 'report_23') {
        data = data.map((item: any) => {
          let rawNotes = item.notes || item.reason || ''
          let target = '—'
          let notes = rawNotes
          
          if (typeof rawNotes === 'string') {
            const targetMatch = rawNotes.match(/المطلوب تصحيح[هة]:\s*([\s\S]*?)(?=\s*المبررات:|$)/)
            if (targetMatch && targetMatch[1]) {
              target = targetMatch[1].trim()
              const reasonMatch = rawNotes.match(/المبررات:\s*([\s\S]*)/)
              notes = reasonMatch && reasonMatch[1] ? reasonMatch[1].trim() : '—'
            }
          }
          
          if (target === '—') {
            target = item.correction_target || item.field_name || item.correction_type || 'تحديث بيانات'
          }
          
          return {
            ...item,
            full_name: item.correct_name || item.new_value || item.full_name || '', // الاسم الصحيح (الجديد المعتمد)
            wrong_name: item.wrong_name || item.old_value || item.full_name || '', // الاسم الخطأ (القديم)
            correction_target: target,
            notes: notes
          }
        })
      }
      
      reportData.value = data
    } catch (error) {
      console.error(`Failed to fetch report ${reportId.value}`, error)
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

  watch(() => props.monthProp, (newVal) => {
    selectedMonth.value = newVal || ''
    fetchData()
  })

  onMounted(() => {
    if (props.monthProp) {
      selectedMonth.value = props.monthProp
    }
    fetchData()
  })
  </script>

  <style>
  @media print {
    @page standalone-landscape-page {
      size: A4 landscape;
      margin: 0 !important;
    }
    
    body:has(.standalone-report-page) {
      page: standalone-landscape-page !important;
      background-color: white !important;
      margin: 0 !important;
      padding: 0 !important;
    }
    
    body:has(.standalone-report-page) .standalone-report-page {
      width: 29.7cm !important;
      height: auto !important;
      min-height: 21cm !important;
      position: absolute !important;
      left: 0 !important;
      top: 0 !important;
      z-index: 9999 !important;
      background: white !important;
      box-sizing: border-box !important;
      padding: 0.5cm !important;
    }

    body:has(.standalone-report-page) * {
      visibility: hidden;
    }

    body:has(.standalone-report-page) .standalone-report-page,
    body:has(.standalone-report-page) .standalone-report-page * {
      visibility: visible;
    }
  }
  </style>
