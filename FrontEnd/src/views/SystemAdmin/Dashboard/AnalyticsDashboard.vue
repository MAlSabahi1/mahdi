<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.analytics_dashboard')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Filters Row -->
      <div class="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900 flex flex-col md:flex-row items-center gap-4">
        <div class="flex-1 flex items-center gap-2">
          <Filter class="w-5 h-5 text-gray-400" />
          <span class="font-bold text-gray-700 dark:text-gray-300">أدوات التحليل:</span>
        </div>
        <div class="flex items-center gap-3 w-full md:w-auto">
          <select class="form-select bg-gray-50 border-gray-200 dark:bg-gray-800 dark:border-gray-700 rounded-xl text-sm font-bold px-4 py-2 w-full md:w-48 cursor-pointer text-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500">
            <option value="all">جميع المحافظات</option>
            <option value="1">صنعاء</option>
            <option value="2">عدن</option>
            <option value="3">مأرب</option>
          </select>
          <select class="form-select bg-gray-50 border-gray-200 dark:bg-gray-800 dark:border-gray-700 rounded-xl text-sm font-bold px-4 py-2 w-full md:w-48 cursor-pointer text-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500">
            <option value="all">جميع القطاعات</option>
            <option value="1">الأمن العام</option>
            <option value="2">القوات الخاصة</option>
          </select>
          <button class="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-xl transition-colors shadow-sm cursor-pointer shrink-0">
            <Search class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Main Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Bar Chart: Force by Governorate -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <h3 class="font-bold text-gray-900 dark:text-white mb-4">التوزيع الجغرافي للقوات</h3>
          <div class="h-[300px] w-full" dir="ltr">
            <ClientOnly>
              <VueApexCharts 
                type="bar" 
                height="100%" 
                :options="barChartOptions" 
                :series="barChartSeries" 
              />
            </ClientOnly>
          </div>
        </div>

        <!-- Donut Chart: Status Distribution -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <h3 class="font-bold text-gray-900 dark:text-white mb-4">توزيع حالات الخدمة</h3>
          <div class="h-[300px] w-full flex items-center justify-center" dir="ltr">
            <ClientOnly>
              <VueApexCharts 
                type="donut" 
                height="100%" 
                :options="donutChartOptions" 
                :series="donutChartSeries" 
              />
            </ClientOnly>
          </div>
        </div>

        <!-- Radar Chart: Readiness -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <h3 class="font-bold text-gray-900 dark:text-white mb-4">مؤشر الجاهزية والتدريب بالقطاعات</h3>
          <div class="h-[350px] w-full flex items-center justify-center" dir="ltr">
            <ClientOnly>
              <VueApexCharts 
                type="radar" 
                height="100%" 
                :options="radarChartOptions" 
                :series="radarChartSeries" 
              />
            </ClientOnly>
          </div>
        </div>

        <!-- Horizontal Bar Chart: Ranks -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <h3 class="font-bold text-gray-900 dark:text-white mb-4">الهرم الرتبي (ضباط وأفراد)</h3>
          <div class="h-[350px] w-full" dir="ltr">
            <ClientOnly>
              <VueApexCharts 
                type="bar" 
                height="100%" 
                :options="horizontalBarOptions" 
                :series="horizontalBarSeries" 
              />
            </ClientOnly>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, defineComponent, h, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import VueApexCharts from 'vue3-apexcharts'
import { Filter, Search } from 'lucide-vue-next'
import api from '@/lib/api'

const { t } = useI18n()

// SSR Wrapper
const ClientOnly = defineComponent({
  setup(_, { slots }) {
    const isMounted = ref(false)
    onMounted(() => {
      isMounted.value = true
    })
    return () => (isMounted.value && slots.default ? slots.default() : h('div', { class: 'h-full w-full bg-gray-50 dark:bg-gray-800 animate-pulse rounded-xl' }))
  }
})

// Bar Chart (Trend/Growth instead of Geographical for now)
const barChartSeries = ref([
  { name: 'تسجيل جديد', data: [0, 0, 0, 0, 0] }
])
const barChartOptions = ref({
  chart: { type: 'bar', stacked: false, fontFamily: 'Tajawal, sans-serif', toolbar: { show: false }, background: 'transparent' },
  colors: ['#3b82f6'],
  plotOptions: { bar: { borderRadius: 4, horizontal: false, columnWidth: '40%' } },
  xaxis: {
    categories: ['-', '-', '-', '-', '-'],
    labels: { style: { fontFamily: 'Tajawal, sans-serif', colors: '#9ca3af' } }
  },
  yaxis: { labels: { style: { colors: '#9ca3af' } } },
  grid: { borderColor: 'rgba(156, 163, 175, 0.1)', strokeDashArray: 4 },
  dataLabels: { enabled: false },
  legend: { position: 'top', fontFamily: 'Tajawal, sans-serif', labels: { colors: '#6b7280' } }
})

// Donut Chart (Force Distribution)
const donutChartSeries = ref([10, 10, 10])
const donutChartOptions = ref({
  chart: { type: 'donut', fontFamily: 'Tajawal, sans-serif', background: 'transparent' },
  labels: ['-', '-', '-'],
  colors: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#6b7280', '#8b5cf6'],
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
        labels: {
          show: true,
          name: { show: true, fontSize: '14px', fontFamily: 'Tajawal, sans-serif' },
          value: { show: true, fontSize: '20px', fontWeight: 'bold', color: '#6b7280' },
          total: { show: true, label: 'الإجمالي', color: '#6b7280', fontSize: '14px', fontFamily: 'Tajawal, sans-serif' }
        }
      }
    }
  },
  dataLabels: { enabled: false },
  stroke: { show: true, colors: 'transparent' },
  legend: { position: 'bottom', fontFamily: 'Tajawal, sans-serif', labels: { colors: '#6b7280' } }
})

// Radar Chart (Readiness) - Static mock for now
const radarChartSeries = ref([
  { name: 'الأمن العام', data: [80, 90, 70, 85, 60] },
  { name: 'القوات الخاصة', data: [95, 85, 90, 80, 85] }
])
const radarChartOptions = ref({
  chart: { type: 'radar', fontFamily: 'Tajawal, sans-serif', toolbar: { show: false }, background: 'transparent' },
  labels: ['التسليح', 'التدريب البدني', 'الالتزام الإداري', 'الجاهزية الفنية', 'الاستجابة'],
  colors: ['#3b82f6', '#8b5cf6'],
  stroke: { width: 2 },
  fill: { opacity: 0.2 },
  markers: { size: 4 },
  yaxis: { show: false },
  xaxis: { labels: { style: { colors: '#6b7280', fontFamily: 'Tajawal, sans-serif' } } },
  legend: { position: 'bottom', fontFamily: 'Tajawal, sans-serif', labels: { colors: '#6b7280' } }
})

// Horizontal Bar (Ranks) - Static mock for now
const horizontalBarSeries = ref([{ name: 'العدد', data: [120, 300, 850, 1500, 3200, 6000] }])
const horizontalBarOptions = ref({
  chart: { type: 'bar', fontFamily: 'Tajawal, sans-serif', toolbar: { show: false }, background: 'transparent' },
  colors: ['#0ea5e9'],
  plotOptions: {
    bar: { borderRadius: 4, horizontal: true, barHeight: '50%' }
  },
  dataLabels: { enabled: true, textAnchor: 'start', style: { colors: ['#6b7280'] }, offsetX: 0 },
  xaxis: {
    categories: ['لواء', 'عميد', 'عقيد', 'مقدم', 'رائد', 'نقيب'],
    labels: { style: { colors: '#9ca3af' } }
  },
  yaxis: { labels: { style: { fontFamily: 'Tajawal, sans-serif', colors: '#6b7280' } } },
  grid: { borderColor: 'rgba(156, 163, 175, 0.1)', strokeDashArray: 4 },
})

const fetchAnalytics = async () => {
  try {
    const res = await api.get('/personnel/dashboard/analytics/')
    
    // Process Geographic Distribution (Bar Chart)
    const geographics = res.data.geographic_distribution || []
    if (geographics.length) {
      barChartSeries.value = [{ name: 'التعداد', data: geographics.map((g: any) => g.value) }]
      barChartOptions.value = {
        ...barChartOptions.value,
        xaxis: {
          ...barChartOptions.value.xaxis,
          categories: geographics.map((g: any) => g.name || 'غير محدد')
        }
      }
    }
    
    // Process Status Distribution (Donut Chart)
    const statuses = res.data.status_distribution || []
    if (statuses.length) {
      donutChartSeries.value = statuses.map((s: any) => s.value)
      donutChartOptions.value = {
        ...donutChartOptions.value,
        labels: statuses.map((s: any) => s.name || 'غير محدد')
      }
    }

    // Process Force Distribution (Radar Chart - map to one series for now)
    const forces = res.data.force_distribution || []
    if (forces.length) {
      radarChartSeries.value = [{ name: 'القوات', data: forces.map((f: any) => f.value) }]
      radarChartOptions.value = {
        ...radarChartOptions.value,
        labels: forces.map((f: any) => f.name || 'غير محدد')
      }
    }

    // Process Rank Distribution (Horizontal Bar)
    const ranks = res.data.rank_distribution || []
    if (ranks.length) {
      horizontalBarSeries.value = [{ name: 'العدد', data: ranks.map((r: any) => r.value) }]
      horizontalBarOptions.value = {
        ...horizontalBarOptions.value,
        xaxis: {
          ...horizontalBarOptions.value.xaxis,
          categories: ranks.map((r: any) => r.name || 'غير محدد')
        }
      }
    }
  } catch (error) {
    console.error('Error fetching analytics', error)
  }
}

onMounted(() => {
  fetchAnalytics()
})
</script>
