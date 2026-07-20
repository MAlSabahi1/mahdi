<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.alerts_center')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Stats Row -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="rounded-2xl border border-red-100 bg-red-50 p-5 dark:border-red-900/30 dark:bg-red-950/20 flex items-center justify-between">
          <div>
            <p class="text-sm font-bold text-red-600 dark:text-red-400">تنبيهات حرجة</p>
            <h3 class="text-3xl font-black text-red-700 dark:text-red-300 mt-1">{{ stats.critical_alerts }}</h3>
          </div>
          <div class="h-14 w-14 rounded-full bg-red-100 dark:bg-red-900/50 flex items-center justify-center text-red-600 dark:text-red-400">
            <AlertOctagon class="w-7 h-7 animate-pulse" />
          </div>
        </div>

        <div class="rounded-2xl border border-amber-100 bg-amber-50 p-5 dark:border-amber-900/30 dark:bg-amber-950/20 flex items-center justify-between">
          <div>
            <p class="text-sm font-bold text-amber-600 dark:text-amber-400">طلبات معلقة</p>
            <h3 class="text-3xl font-black text-amber-700 dark:text-amber-300 mt-1">{{ stats.pending_requests_count }}</h3>
          </div>
          <div class="h-14 w-14 rounded-full bg-amber-100 dark:bg-amber-900/50 flex items-center justify-center text-amber-600 dark:text-amber-400">
            <Clock class="w-7 h-7" />
          </div>
        </div>

        <div class="rounded-2xl border border-emerald-100 bg-emerald-50 p-5 dark:border-emerald-900/30 dark:bg-emerald-950/20 flex items-center justify-between">
          <div>
            <p class="text-sm font-bold text-emerald-600 dark:text-emerald-400">تمت المعالجة اليوم</p>
            <h3 class="text-3xl font-black text-emerald-700 dark:text-emerald-300 mt-1">{{ stats.processed_today }}</h3>
          </div>
          <div class="h-14 w-14 rounded-full bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
            <CheckCircle2 class="w-7 h-7" />
          </div>
        </div>
      </div>

      <!-- Main Layout -->
      <div class="rounded-2xl border border-gray-200 bg-white p-2 shadow-sm dark:border-gray-800 dark:bg-gray-900">
        <!-- Tabs -->
        <div class="flex items-center gap-2 border-b border-gray-100 dark:border-gray-800 p-4">
          <button 
            @click="activeTab = 'alerts'"
            class="px-5 py-2.5 rounded-xl font-bold text-sm transition-all flex items-center gap-2 cursor-pointer"
            :class="activeTab === 'alerts' ? 'bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400' : 'text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-800'"
          >
            <ShieldAlert class="w-4 h-4" />
            التنبيهات الأمنية والنظامية
            <span v-if="activeTab !== 'alerts' && alerts.length > 0" class="bg-red-100 text-red-600 dark:bg-red-900/50 dark:text-red-400 px-2 py-0.5 rounded-md text-[10px]">{{ alerts.length }}</span>
          </button>
          <button 
            @click="activeTab = 'requests'"
            class="px-5 py-2.5 rounded-xl font-bold text-sm transition-all flex items-center gap-2 cursor-pointer"
            :class="activeTab === 'requests' ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-800'"
          >
            <FileEdit class="w-4 h-4" />
            الطلبات الإدارية المعلقة
            <span v-if="activeTab !== 'requests' && requests.length > 0" class="bg-blue-100 text-blue-600 dark:bg-blue-900/50 dark:text-blue-400 px-2 py-0.5 rounded-md text-[10px]">{{ requests.length }}</span>
          </button>
        </div>

        <div class="p-4">
          <!-- Alerts Tab -->
          <div v-if="activeTab === 'alerts'" class="space-y-4">
            <div v-for="alert in alerts" :key="alert.id" class="rounded-xl border p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all"
                 :class="alert.severity === 'critical' ? 'border-red-200 bg-red-50/30 dark:border-red-900/50 dark:bg-red-900/10' : 'border-amber-200 bg-amber-50/30 dark:border-amber-900/50 dark:bg-amber-900/10'">
              <div class="flex items-start gap-4">
                <div class="mt-1 h-10 w-10 shrink-0 rounded-full flex items-center justify-center"
                     :class="alert.severity === 'critical' ? 'bg-red-100 text-red-600 dark:bg-red-900/50 dark:text-red-400' : 'bg-amber-100 text-amber-600 dark:bg-amber-900/50 dark:text-amber-400'">
                  <AlertOctagon v-if="alert.severity === 'critical'" class="w-5 h-5 animate-pulse" />
                  <AlertTriangle v-else class="w-5 h-5" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                    {{ alert.title }}
                    <span class="text-[10px] px-2 py-0.5 rounded-md font-mono" 
                          :class="alert.severity === 'critical' ? 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300'">
                      {{ alert.time }}
                    </span>
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">{{ alert.description }}</p>
                  <p class="text-xs text-gray-500 font-mono mt-2">Source IP: {{ alert.ip }} | User: {{ alert.user }}</p>
                </div>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button @click="handleAction('investigate', alert.id)" class="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-xl text-sm font-bold shadow-sm transition-all cursor-pointer">
                  تحقيق
                </button>
                <button @click="handleAction('dismiss', alert.id)" class="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-xl text-sm font-bold transition-all cursor-pointer">
                  تجاهل
                </button>
              </div>
            </div>
            <div v-if="alerts.length === 0" class="text-center py-12 text-gray-400 font-bold">
              لا توجد تنبيهات أمنية حالياً.
            </div>
          </div>

          <!-- Requests Tab -->
          <div v-if="activeTab === 'requests'" class="space-y-4">
            <div v-for="req in requests" :key="req.id" class="rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900/50 p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-blue-200 dark:hover:border-blue-900/50 transition-all">
              <div class="flex items-start gap-4">
                <div class="mt-1 h-10 w-10 shrink-0 rounded-full bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400 flex items-center justify-center">
                  <FileText class="w-5 h-5" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                    {{ req.title }}
                    <span class="text-[10px] px-2 py-0.5 rounded-md font-mono bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300">
                      {{ req.time }}
                    </span>
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">{{ req.description }}</p>
                  <p class="text-xs font-bold text-gray-500 mt-2">مقدم الطلب: <span class="text-blue-600 dark:text-blue-400">{{ req.requester }}</span> - {{ req.department }}</p>
                </div>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button @click="handleAction('approve', req.id)" class="px-4 py-2 bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 dark:bg-emerald-900/20 dark:border-emerald-800 dark:text-emerald-400 dark:hover:bg-emerald-900/40 rounded-xl text-sm font-bold shadow-sm transition-all cursor-pointer">
                  اعتماد
                </button>
                <button @click="handleAction('reject', req.id)" class="px-4 py-2 bg-red-50 border border-red-200 text-red-700 hover:bg-red-100 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/40 rounded-xl text-sm font-bold shadow-sm transition-all cursor-pointer">
                  رفض
                </button>
              </div>
            </div>
            <div v-if="requests.length === 0" class="text-center py-12 text-gray-400 font-bold">
              لا توجد طلبات معلقة حالياً.
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'
import { AlertOctagon, AlertTriangle, Clock, CheckCircle2, ShieldAlert, FileEdit, FileText } from 'lucide-vue-next'
import api from '@/lib/api'

import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()
const activeTab = ref('alerts')

const alerts = ref<any[]>([])
const requests = ref<any[]>([])
const stats = ref({
  critical_alerts: 0,
  pending_requests_count: 0,
  processed_today: 0
})

const fetchAlerts = async () => {
  try {
    const res = await api.get('/personnel/dashboard/alerts/')
    if (res.data.data_quality_alerts) {
      alerts.value = res.data.data_quality_alerts.map((a: any) => ({
        id: a.military_number,
        title: 'تدني جودة بيانات الفرد',
        description: `الاسم: ${a.full_name} | نسبة الجودة: ${a.data_quality_score}% — يتطلب تحديث البيانات أو استكمال المرفقات.`,
        severity: a.data_quality_score < 50 ? 'critical' : 'warning',
        time: 'مستمر',
        ip: 'فحص آلي',
        user: a.military_number
      }))
    }
    
    if (res.data.pending_requests) {
      requests.value = res.data.pending_requests.map((r: any) => ({
        id: r.id,
        title: r.title,
        description: r.description,
        time: new Date(r.time).toLocaleString(),
        requester: r.requester,
        department: r.department
      }))
    }
    
    if (res.data.stats) {
      stats.value = res.data.stats
    }
  } catch (error) {
    console.error('Error fetching alerts', error)
  }
}

onMounted(() => {
  fetchAlerts()
})

const handleAction = (action: string, id: number | string) => {
  let title = ''
  let text = ''
  let confirmColor = ''
  let icon: 'warning' | 'info' | 'success' | 'question' = 'question'

  if (action === 'approve') {
    title = 'هل أنت متأكد من اعتماد الطلب؟'
    text = 'سيتم تنفيذ الطلب وتوثيقه في سجل التدقيق فوراً.'
    confirmColor = '#10b981'
    icon = 'question'
  } else if (action === 'reject') {
    title = 'رفض الطلب'
    text = 'هل تريد رفض هذا الطلب وإرسال إشعار للمرسل؟'
    confirmColor = '#ef4444'
    icon = 'warning'
  } else if (action === 'investigate') {
    title = 'مراجعة السجل'
    text = 'سيتم توجيهك إلى شاشة الفرد لإكمال البيانات الناقصة. هل تود الانتقال الآن؟'
    confirmColor = '#3b82f6'
    icon = 'info'
  } else if (action === 'dismiss') {
    title = 'تجاهل التنبيه'
    text = 'هل أنت متأكد من تجاهل هذا التنبيه الأمني؟'
    confirmColor = '#6b7280'
    icon = 'warning'
  }

  Swal.fire({
    title,
    text,
    icon,
    showCancelButton: true,
    confirmButtonColor: confirmColor,
    cancelButtonColor: '#d1d5db',
    confirmButtonText: 'نعم، تأكيد',
    cancelButtonText: 'إلغاء'
  }).then((result) => {
    if (result.isConfirmed) {
      if (action === 'investigate') {
        router.push(`/personnel/${id}`)
        return
      }

      if (activeTab.value === 'alerts') {
        alerts.value = alerts.value.filter(a => a.id !== id)
      } else {
        requests.value = requests.value.filter(r => r.id !== id)
      }
      
      Swal.fire({
        title: 'تم الإجراء بنجاح',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false
      })
    }
  })
}
</script>
