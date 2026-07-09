<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.stats_dashboard')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Top Stats Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Stat Card 1 -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900 flex items-center justify-between group hover:border-blue-500/30 transition-colors">
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">إجمالي القوة البشرية</p>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1">14,250</h3>
            <div class="flex items-center gap-1 text-xs text-emerald-600 mt-2 font-bold">
              <TrendingUp class="w-3 h-3" />
              <span>+2.4% هذا الشهر</span>
            </div>
          </div>
          <div class="h-12 w-12 rounded-xl bg-blue-50 text-blue-600 dark:bg-blue-950/30 dark:text-blue-400 flex items-center justify-center transition-transform group-hover:scale-110">
            <Users class="w-6 h-6" />
          </div>
        </div>

        <!-- Stat Card 2 -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900 flex items-center justify-between group hover:border-emerald-500/30 transition-colors">
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">المستخدمين النشطين (الآن)</p>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1">842</h3>
            <div class="flex items-center gap-1 text-xs text-emerald-600 mt-2 font-bold">
              <Zap class="w-3 h-3" />
              <span>أداء مستقر</span>
            </div>
          </div>
          <div class="h-12 w-12 rounded-xl bg-emerald-50 text-emerald-600 dark:bg-emerald-950/30 dark:text-emerald-400 flex items-center justify-center transition-transform group-hover:scale-110">
            <Activity class="w-6 h-6" />
          </div>
        </div>

        <!-- Stat Card 3 -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900 flex items-center justify-between group hover:border-purple-500/30 transition-colors">
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">معدل معالجة البيانات</p>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1">1.2K/s</h3>
            <div class="flex items-center gap-1 text-xs text-emerald-600 mt-2 font-bold">
              <TrendingUp class="w-3 h-3" />
              <span>+14% استجابة</span>
            </div>
          </div>
          <div class="h-12 w-12 rounded-xl bg-purple-50 text-purple-600 dark:bg-purple-950/30 dark:text-purple-400 flex items-center justify-center transition-transform group-hover:scale-110">
            <Server class="w-6 h-6" />
          </div>
        </div>

        <!-- Stat Card 4 -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900 flex items-center justify-between group hover:border-amber-500/30 transition-colors">
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">التنبيهات الأمنية المعلقة</p>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1">14</h3>
            <div class="flex items-center gap-1 text-xs text-amber-600 mt-2 font-bold">
              <AlertTriangle class="w-3 h-3" />
              <span>تحتاج مراجعة</span>
            </div>
          </div>
          <div class="h-12 w-12 rounded-xl bg-amber-50 text-amber-600 dark:bg-amber-950/30 dark:text-amber-400 flex items-center justify-center transition-transform group-hover:scale-110">
            <ShieldAlert class="w-6 h-6" />
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Area Chart: System Activity -->
        <div class="lg:col-span-2 rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-gray-900 dark:text-white">نشاط النظام خلال 30 يوم</h3>
            <button class="text-sm font-bold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 dark:bg-blue-900/20 dark:hover:bg-blue-900/40 px-3 py-1.5 rounded-lg transition-colors cursor-pointer">
              تصدير التقرير
            </button>
          </div>
          <div class="h-[300px] w-full" dir="ltr">
            <ClientOnly>
              <VueApexCharts 
                type="area" 
                height="100%" 
                :options="areaChartOptions" 
                :series="areaChartSeries" 
              />
            </ClientOnly>
          </div>
        </div>

        <!-- Radial Chart: Storage & Resources -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <h3 class="font-bold text-gray-900 dark:text-white mb-4">استهلاك الموارد السحابية</h3>
          <div class="h-[250px] w-full flex items-center justify-center" dir="ltr">
            <ClientOnly>
              <VueApexCharts 
                type="radialBar" 
                height="100%" 
                :options="radialChartOptions" 
                :series="radialChartSeries" 
              />
            </ClientOnly>
          </div>
          <div class="mt-4 space-y-3">
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                <span class="w-3 h-3 rounded-full bg-blue-500"></span>
                قاعدة البيانات
              </div>
              <span class="font-bold text-gray-900 dark:text-white">78%</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
                مساحة الملفات
              </div>
              <span class="font-bold text-gray-900 dark:text-white">45%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity List -->
      <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
        <h3 class="font-bold text-gray-900 dark:text-white mb-6">أحدث الأنشطة الحساسة</h3>
        <div class="space-y-4">
          <div v-for="i in 4" :key="i" class="flex items-start gap-4 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors border border-transparent hover:border-gray-100 dark:hover:border-gray-800 cursor-pointer">
            <div class="h-10 w-10 shrink-0 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <User class="w-5 h-5 text-gray-500 dark:text-gray-400" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-bold text-gray-900 dark:text-white">تعديل بيانات رتبة عسكرية (ترقية)</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 truncate">تم بواسطة: أحمد محمد عبدالله - إدارة الموارد البشرية</p>
            </div>
            <div class="text-xs font-mono text-gray-400 shrink-0">منذ 10 دقائق</div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, defineComponent, h, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import VueApexCharts from 'vue3-apexcharts'
import { Users, Activity, TrendingUp, Zap, Server, ShieldAlert, AlertTriangle, User } from 'lucide-vue-next'

const { t } = useI18n()

// Wrapper to prevent SSR issues with ApexCharts if any, though standard SPA works fine.
const ClientOnly = defineComponent({
  setup(_, { slots }) {
    const isMounted = ref(false)
    onMounted(() => {
      isMounted.value = true
    })
    return () => (isMounted.value && slots.default ? slots.default() : h('div', { class: 'h-full w-full bg-gray-50 dark:bg-gray-800 animate-pulse rounded-xl' }))
  }
})

// Chart Data: System Activity (Area)
const areaChartSeries = ref([
  { name: 'عمليات الإدخال', data: [31, 40, 28, 51, 42, 109, 100] },
  { name: 'عمليات الاستعلام', data: [11, 32, 45, 32, 34, 52, 41] }
])

const areaChartOptions = ref({
  chart: { 
    type: 'area', 
    fontFamily: 'Tajawal, sans-serif',
    toolbar: { show: false },
    zoom: { enabled: false },
    background: 'transparent'
  },
  colors: ['#3b82f6', '#10b981'],
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  fill: {
    type: 'gradient',
    gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0.05, stops: [0, 90, 100] }
  },
  xaxis: {
    categories: ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
    axisBorder: { show: false },
    axisTicks: { show: false },
    labels: {
      style: { colors: '#9ca3af', fontFamily: 'Tajawal, sans-serif' }
    }
  },
  yaxis: { 
    show: false 
  },
  grid: {
    borderColor: 'rgba(156, 163, 175, 0.1)',
    strokeDashArray: 4,
    xaxis: { lines: { show: true } },
    yaxis: { lines: { show: true } }
  },
  theme: {
    mode: 'light' // Can be made dynamic later
  },
  legend: { 
    position: 'top', 
    horizontalAlign: 'right',
    fontFamily: 'Tajawal, sans-serif',
    labels: { colors: '#6b7280' }
  }
})

// Chart Data: Storage (RadialBar)
const radialChartSeries = ref([78, 45])
const radialChartOptions = ref({
  chart: { 
    type: 'radialBar', 
    fontFamily: 'Tajawal, sans-serif',
    background: 'transparent'
  },
  colors: ['#3b82f6', '#10b981'],
  plotOptions: {
    radialBar: {
      hollow: { size: '45%' },
      track: { background: 'rgba(156, 163, 175, 0.1)', margin: 8 },
      dataLabels: {
        name: { fontSize: '14px', fontWeight: 'bold', color: '#6b7280' },
        value: { fontSize: '24px', fontWeight: '900', color: '#111827' },
        total: {
          show: true,
          label: 'الإجمالي',
          color: '#6b7280',
          formatter: function () {
            return '61.5%'
          }
        }
      }
    }
  },
  labels: ['قاعدة البيانات', 'مساحة الملفات'],
  stroke: { lineCap: 'round' }
})
</script>
