<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.system_telemetry')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <Activity class="w-7 h-7 text-blue-500" />
            تليمتري النظام والمهام
          </h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            مراقبة حية لصحة الخوادم والمهام الخلفية وقوائم الانتظار
          </p>
        </div>
        <button @click="fetchTelemetryData" class="bg-blue-50 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400 px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors border border-blue-200 dark:border-blue-800">
          <RefreshCw class="w-4 h-4" /> تحديث البيانات
        </button>
      </div>

      <!-- Live Resource Monitor Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- CPU Card -->
        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <div class="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
              <Cpu class="w-5 h-5" />
            </div>
            <span class="text-xs font-bold text-gray-500 dark:text-gray-400">Main Server</span>
          </div>
          <div>
            <div class="flex items-end gap-2 mb-1">
              <h3 class="text-3xl font-black text-gray-900 dark:text-white">{{ stats.cpu }}<span class="text-lg font-medium text-gray-500">%</span></h3>
              <span class="text-xs text-emerald-500 font-bold mb-1.5 flex items-center"><TrendingDown class="w-3 h-3 mr-0.5" /> 2.1%</span>
            </div>
            <p class="text-sm font-bold text-gray-600 dark:text-gray-400">استهلاك المعالج (CPU)</p>
          </div>
          <div class="mt-4 w-full bg-gray-100 dark:bg-gray-800 rounded-full h-1.5">
            <div class="bg-blue-500 h-1.5 rounded-full" :style="`width: ${stats.cpu}%`"></div>
          </div>
        </div>

        <!-- RAM Card -->
        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <div class="w-10 h-10 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
              <MemoryStick class="w-5 h-5" />
            </div>
            <span class="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-0.5 rounded">مستقر</span>
          </div>
          <div>
            <div class="flex items-end gap-2 mb-1">
              <h3 class="text-3xl font-black text-gray-900 dark:text-white">{{ stats.ram }}<span class="text-lg font-medium text-gray-500">GB</span></h3>
              <span class="text-xs text-gray-500 font-bold mb-1.5">/ {{ stats.ramTotal }}GB</span>
            </div>
            <p class="text-sm font-bold text-gray-600 dark:text-gray-400">الذاكرة العشوائية (RAM)</p>
          </div>
          <div class="mt-4 w-full bg-gray-100 dark:bg-gray-800 rounded-full h-1.5">
            <div class="bg-emerald-500 h-1.5 rounded-full" :style="`width: ${(stats.ram / stats.ramTotal) * 100}%`"></div>
          </div>
        </div>

        <!-- Storage Card -->
        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <div class="w-10 h-10 rounded-lg bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center text-amber-600 dark:text-amber-400">
              <HardDrive class="w-5 h-5" />
            </div>
          </div>
          <div>
            <div class="flex items-end gap-2 mb-1">
              <h3 class="text-3xl font-black text-gray-900 dark:text-white">{{ stats.storage }}<span class="text-lg font-medium text-gray-500">%</span></h3>
            </div>
            <p class="text-sm font-bold text-gray-600 dark:text-gray-400">مساحة التخزين (Storage)</p>
          </div>
          <div class="mt-4 w-full bg-gray-100 dark:bg-gray-800 rounded-full h-1.5">
            <div class="bg-amber-500 h-1.5 rounded-full" :style="`width: ${stats.storage}%`"></div>
          </div>
        </div>

        <!-- API Latency Card -->
        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <div class="w-10 h-10 rounded-lg bg-purple-50 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 dark:text-purple-400">
              <Zap class="w-5 h-5" />
            </div>
            <span class="text-xs font-bold text-gray-500 dark:text-gray-400">Avg. 1h</span>
          </div>
          <div>
            <div class="flex items-end gap-2 mb-1">
              <h3 class="text-3xl font-black text-gray-900 dark:text-white">{{ stats.latency }}<span class="text-lg font-medium text-gray-500">ms</span></h3>
            </div>
            <p class="text-sm font-bold text-gray-600 dark:text-gray-400">زمن استجابة النظام (Latency)</p>
          </div>
          <div class="mt-4 flex items-center gap-1 h-1.5">
            <div class="bg-purple-500 h-full rounded-full flex-1"></div>
            <div class="bg-purple-500 h-full rounded-full flex-1 opacity-70"></div>
            <div class="bg-purple-500 h-full rounded-full flex-1 opacity-40"></div>
            <div class="bg-gray-200 dark:bg-gray-700 h-full rounded-full flex-1"></div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Background Jobs Table (2/3 width) -->
        <div class="lg:col-span-2 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm overflow-hidden flex flex-col">
          <div class="p-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/20">
            <h3 class="font-bold text-gray-800 dark:text-gray-200 flex items-center gap-2">
              <Settings2 class="w-5 h-5 text-gray-400" />
              المهام الخلفية (Background Jobs)
            </h3>
          </div>
          <div class="flex-1">
            <DataTable
              :columns="jobColumns"
              :data="backgroundJobs"
              row-key="id"
              :search-placeholder="'ابحث عن مهمة...'"
            >
              <template #cell-status="{ row }">
                <span v-if="row.status === 'running'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
                  <Loader2 class="w-3 h-3 animate-spin" /> قيد التنفيذ
                </span>
                <span v-else-if="row.status === 'completed'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                  <CheckCircle class="w-3 h-3" /> اكتمل
                </span>
                <span v-else-if="row.status === 'failed'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 border border-red-200 dark:border-red-800">
                  <XCircle class="w-3 h-3" /> فشل
                </span>
                <span v-else class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400 border border-gray-200 dark:border-gray-700">
                  <Clock class="w-3 h-3" /> مجدول
                </span>
              </template>
              <template #cell-progress="{ row }">
                <div class="flex items-center gap-2">
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 min-w-[80px]">
                    <div class="h-1.5 rounded-full" 
                         :class="row.status === 'failed' ? 'bg-red-500' : 'bg-blue-500'" 
                         :style="`width: ${row.progress}%`"></div>
                  </div>
                  <span class="text-xs font-bold text-gray-500">{{ row.progress }}%</span>
                </div>
              </template>
            </DataTable>
          </div>
        </div>

        <!-- System Logs (1/3 width) -->
        <div class="bg-gray-900 rounded-2xl border border-gray-800 shadow-sm overflow-hidden flex flex-col relative text-gray-300">
          <div class="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-950">
            <h3 class="font-bold text-white flex items-center gap-2 text-sm">
              <Terminal class="w-4 h-4 text-emerald-400" />
              سجل أحداث النظام (Live Logs)
            </h3>
            <span class="flex h-2 w-2 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
          </div>
          <div class="p-4 font-mono text-xs overflow-y-auto max-h-[400px] flex-1 space-y-2">
            <div v-for="(log, idx) in systemLogs" :key="idx" class="flex gap-3 items-start hover:bg-gray-800/50 p-1 rounded">
              <span class="text-gray-500 shrink-0">{{ log.time }}</span>
              <span :class="{
                'text-emerald-400': log.level === 'INFO',
                'text-amber-400': log.level === 'WARN',
                'text-red-400': log.level === 'ERROR',
                'text-blue-400': log.level === 'DEBUG'
              }">[{{ log.level }}]</span>
              <span class="break-all">{{ log.message }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import api from '@/lib/api'
import { 
  Activity, RefreshCw, Cpu, MemoryStick, HardDrive, Zap, TrendingDown, 
  Settings2, Loader2, CheckCircle, XCircle, Clock, Terminal
} from 'lucide-vue-next'

const { t } = useI18n()

// System Stats
const stats = ref({
  cpu: 32,
  ram: 12.4,
  ramTotal: 32,
  storage: 68,
  latency: 124
})

const fetchTelemetryData = async () => {
  try {
    const res = await api.get('/telemetry/dashboard/')
    if (res.data?.success) {
      const db = res.data.data
      
      // Update basic mock stats with some randomness or logic based on data
      // For a real implementation, these would come directly from telemetry metrics if available.
      if (db.system_health) {
        stats.value.cpu = db.system_health.cpu_usage || Math.floor(Math.random() * 40) + 10
        stats.value.ram = db.system_health.ram_usage || 12.4
        stats.value.storage = db.system_health.storage_usage || 68
      }
      
      // We can also inject background jobs from celery if available
    }
  } catch (e) {
    console.error('Failed to fetch telemetry data', e)
  }
}

let intervalId: any = null

onMounted(() => {
  fetchTelemetryData()
  intervalId = setInterval(fetchTelemetryData, 10000) // Poll every 10 seconds
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

// Mock Data for Background Jobs
const jobColumns = ref([
  { key: 'id', label: '#', sortable: true },
  { key: 'name', label: 'اسم المهمة', sortable: true },
  { key: 'type', label: 'النوع', sortable: true },
  { key: 'status', label: 'الحالة', sortable: true },
  { key: 'progress', label: 'التقدم', sortable: false },
  { key: 'time', label: 'المدة الزمنية', sortable: true },
])

const backgroundJobs = ref([
  { id: 'JB-1042', name: 'استيراد كشف القوة (صنعاء)', type: 'استيراد بيانات', status: 'running', progress: 45, time: '02:14' },
  { id: 'JB-1041', name: 'أرشفة اللقطة الشهرية', type: 'نسخ احتياطي', status: 'completed', progress: 100, time: '05:30' },
  { id: 'JB-1040', name: 'تحديث مصفوفة الصلاحيات', type: 'أمان النظام', status: 'completed', progress: 100, time: '00:12' },
  { id: 'JB-1039', name: 'مزامنة رواتب الأفراد (مايو)', type: 'مزامنة مالية', status: 'failed', progress: 82, time: '14:20' },
  { id: 'JB-1038', name: 'توليد تقارير الانضباط', type: 'تقارير مجدولة', status: 'scheduled', progress: 0, time: '-' },
])

// Mock Data for System Logs
const systemLogs = ref([
  { time: '10:42:15', level: 'INFO', message: 'User admin@system.gov logged in successfully.' },
  { time: '10:41:03', level: 'INFO', message: 'Worker node-2 joined the cluster.' },
  { time: '10:39:55', level: 'WARN', message: 'High memory usage detected on Redis instance (85%).' },
  { time: '10:35:12', level: 'ERROR', message: 'Failed to connect to external API endpoint (timeout).' },
  { time: '10:30:00', level: 'INFO', message: 'Cron job "daily_backup" executed successfully.' },
  { time: '10:28:44', level: 'DEBUG', message: 'Cache cleared for permissions matrix.' },
  { time: '10:15:20', level: 'INFO', message: 'System startup sequence completed in 4.2s.' },
])

</script>
