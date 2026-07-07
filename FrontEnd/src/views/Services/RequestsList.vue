<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="'قائمة طلبات: ' + (serviceTitle || filterType || 'جميع الخدمات')" />

    <div class="space-y-6 text-start" dir="rtl">

      <!-- Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-3">
          قائمة الطلبات
          <span v-if="filterType" class="text-[10px] bg-brand-50 text-brand-600 border border-brand-100 dark:bg-brand-950/30 dark:border-brand-900 px-3 py-1 rounded-full flex items-center gap-2">
            {{ serviceTitle || filterType }}
            <RouterLink to="/services/requests" class="hover:text-red-500 font-bold ml-1">×</RouterLink>
          </span>
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          جميع الطلبات التي قمت بتقديمها مع إمكانية البحث والتصفية حسب الحالة.
        </p>
      </div>

      <!-- Filters -->
      <div class="flex flex-wrap gap-2">
        <button v-for="f in statusFilters" :key="f.value" @click="filterStatus = f.value"
          :class="filterStatus === f.value ? 'bg-brand-600 text-white border-brand-500' : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800'"
          class="px-3 py-2 text-xs font-bold rounded-xl border transition-all cursor-pointer flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full" :class="f.dot"></span>
          {{ f.label }}
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 lg:grid-cols-6 gap-3">
        <div v-for="stat in requestStats" :key="stat.label"
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 shadow-sm">
          <p class="text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">{{ stat.label }}</p>
          <div class="flex items-center justify-between">
            <p class="text-lg font-black text-gray-900 dark:text-white font-mono">{{ stat.value }}</p>
            <span :class="stat.dotClass" class="h-2.5 w-2.5 rounded-full"></span>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-450 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-4 py-3">رقم الطلب</th>
                <th class="px-4 py-3">اسم الخدمة</th>
                <th class="px-4 py-3">مقدم الطلب</th>
                <th class="px-4 py-3">الحالة</th>
                <th class="px-4 py-3">تاريخ الإنشاء</th>
                <th class="px-4 py-3">آخر تحديث</th>
                <th class="px-4 py-3">الجهة الحالية</th>
                <th class="px-4 py-3 text-center w-[100px]">إجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr v-if="loading" >
                <td colspan="8" class="px-4 py-12 text-center text-gray-400">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600 mx-auto"></div>
                </td>
              </tr>
              <tr v-else-if="displayedRequests.length === 0">
                <td colspan="8" class="px-4 py-12 text-center text-gray-400 dark:text-gray-500">
                  لا توجد طلبات بهذه الحالة حالياً.
                </td>
              </tr>
              <tr v-for="req in displayedRequests" :key="req.id" class="hover:bg-gray-50/50 dark:hover:bg-gray-950/30">
                <td class="px-4 py-3 font-mono font-bold">
                  <RouterLink :to="`/services/forms/${req.id}`" class="text-brand-600 hover:underline">{{ req.id }}</RouterLink>
                </td>
                <td class="px-4 py-3 font-bold text-gray-800 dark:text-gray-200">{{ req.form_type_display || req.form_type }}</td>
                <td class="px-4 py-3">{{ req.personnel_name || '—' }}</td>
                <td class="px-4 py-3">
                  <span :class="getStatusColor(req.status)" class="inline-flex items-center gap-1 rounded px-2 py-0.5 text-[10px] font-bold">
                    <span :class="getStatusDot(req.status)" class="h-1.5 w-1.5 rounded-full"></span>
                    {{ getStatusLabel(req.status) }}
                  </span>
                </td>
                <td class="px-4 py-3 font-mono text-gray-450">{{ formatDate(req.created_at) }}</td>
                <td class="px-4 py-3 font-mono text-gray-450">{{ formatDate(req.updated_at) }}</td>
                <td class="px-4 py-3 text-gray-600 dark:text-gray-400">{{ req.current_step_name || '-' }}</td>
                <td class="px-4 py-3 text-center">
                  <RouterLink :to="`/services/forms/${req.id}`"
                    class="text-brand-600 hover:text-brand-700 text-[10px] font-bold hover:underline">
                    عرض التفاصيل
                  </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'

const route = useRoute()
const servicesStore = useServicesStore()
const filterType = ref(route.query.type as string || '')
const serviceTitle = ref('')
const filterStatus = ref('all')
const allRequests = ref<any[]>([])
const loading = ref(false)

const statusFilters = [
  { value: 'all', label: 'الكل', dot: 'bg-gray-400' },
  { value: 'draft', label: 'مسودة', dot: 'bg-gray-400' },
  { value: 'in_progress', label: 'قيد الانتظار', dot: 'bg-blue-500' },
  { value: 'approved', label: 'تمت الموافقة', dot: 'bg-emerald-500' },
  { value: 'executing', label: 'قيد التنفيذ', dot: 'bg-indigo-500' },
  { value: 'completed', label: 'مكتمل', dot: 'bg-teal-500' },
  { value: 'rejected', label: 'مرفوض', dot: 'bg-red-500' },
  { value: 'cancelled', label: 'ملغى', dot: 'bg-orange-500' },
]

const displayedRequests = computed(() => {
  if (filterStatus.value === 'all') return allRequests.value
  return allRequests.value.filter(r => r.status === filterStatus.value)
})

const requestStats = computed(() => {
  const r = allRequests.value
  return [
    { label: 'الكل', value: r.length, dotClass: 'bg-gray-400' },
    { label: 'قيد الانتظار', value: r.filter(x => x.status === 'in_progress').length, dotClass: 'bg-blue-500' },
    { label: 'تمت الموافقة', value: r.filter(x => x.status === 'approved').length, dotClass: 'bg-emerald-500' },
    { label: 'قيد التنفيذ', value: r.filter(x => x.status === 'executing').length, dotClass: 'bg-indigo-500' },
    { label: 'مرفوض', value: r.filter(x => x.status === 'rejected').length, dotClass: 'bg-red-500' },
    { label: 'ملغى', value: r.filter(x => x.status === 'cancelled').length, dotClass: 'bg-orange-500' },
  ]
})

onMounted(() => fetchData())
watch(() => route.query.type, (v) => { filterType.value = v as string || ''; fetchData() })

async function fetchData() {
  loading.value = true
  try {
    const q: any = {}
    if (filterType.value) q.type = filterType.value
    const res = await servicesStore.fetchForms(q)
    const formsList = res?.results || res || []
    allRequests.value = formsList.map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || ''
    }))
  } catch { /* ignore */ } finally { loading.value = false }
}

function formatDate(d: string) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-GB')
}

function getStatusLabel(s: string) {
  const m: any = { draft: 'مسودة', in_progress: 'قيد الانتظار', approved: 'تمت الموافقة', executing: 'قيد التنفيذ', completed: 'مكتمل', rejected: 'مرفوض', cancelled: 'ملغى', returned: 'مُرجع' }
  return m[s] || s
}

function getStatusColor(s: string) {
  const c: any = {
    draft: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    in_progress: 'bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400',
    approved: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/20 dark:text-emerald-400',
    executing: 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950/20 dark:text-indigo-400',
    completed: 'bg-teal-50 text-teal-700 dark:bg-teal-950/20 dark:text-teal-400',
    rejected: 'bg-red-50 text-red-700 dark:bg-red-950/20 dark:text-red-400',
    cancelled: 'bg-orange-50 text-orange-700 dark:bg-orange-950/20 dark:text-orange-400',
  }
  return c[s] || 'bg-gray-100 text-gray-600'
}

function getStatusDot(s: string) {
  const d: any = { draft: 'bg-gray-400', in_progress: 'bg-blue-500', approved: 'bg-emerald-500', executing: 'bg-indigo-500', completed: 'bg-teal-500', rejected: 'bg-red-500', cancelled: 'bg-orange-500' }
  return d[s] || 'bg-gray-400'
}
</script>
