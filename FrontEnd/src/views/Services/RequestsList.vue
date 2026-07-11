<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="'قائمة طلبات: ' + (serviceTitle || filterType || 'جميع الخدمات')" />

    <div class="space-y-6 text-start" dir="rtl">

      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            قائمة الطلبات
            <span v-if="filterType" class="text-[10px] bg-brand-50 text-brand-600 border border-brand-100 dark:bg-brand-500/10 dark:border-brand-500/20 px-3 py-1 rounded-full flex items-center gap-2 font-bold">
              {{ serviceTitle || filterType }}
              <RouterLink to="/services/requests" class="hover:text-error-500 font-bold ml-1">×</RouterLink>
            </span>
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            جميع الطلبات التي قمت بتقديمها مع إمكانية البحث والتصفية حسب الحالة.
          </p>
        </div>
      </div>

      <!-- Data Table -->
      <DataTable
        :columns="columns"
        :data="displayedRequests"
        rowKey="id"
        :loading="loading"
        searchPlaceholder="بحث برقم الطلب أو اسم مقدم الطلب..."
        @search="val => searchText = val"
        @refresh="fetchData"
        emptyTitle="لا توجد طلبات"
        emptyDescription="لا توجد طلبات بهذه الحالة حالياً"
        actionsWidth="120px"
      >
        <!-- Toolbar Actions: Filters -->
        <template #toolbar-actions>
          <div class="flex flex-wrap gap-2">
            <button v-for="f in statusFilters" :key="f.value" @click="filterStatus = f.value"
              :class="filterStatus === f.value ? 'bg-brand-600 text-white border-brand-500 shadow-md shadow-brand-500/20' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700'"
              class="px-3.5 py-2 text-[11px] font-bold rounded-lg border transition-all cursor-pointer flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full" :class="f.dot"></span>
              {{ f.label }}
            </button>
          </div>
        </template>

        <template #cell-id="{ row }">
          <RouterLink :to="`/services/forms/${row.id}`" class="text-brand-600 hover:underline font-mono font-bold">#{{ String(row.id).padStart(5, '0') }}</RouterLink>
        </template>

        <template #cell-form_type="{ row }">
          <span class="font-bold text-gray-800 dark:text-gray-200">{{ row.form_type_display || row.form_type }}</span>
        </template>

        <template #cell-personnel="{ row }">
          <span class="text-gray-600 dark:text-gray-300">{{ row.personnel_name || '—' }}</span>
        </template>

        <template #cell-status="{ row }">
          <span :class="getStatusColor(row.status)" class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[10px] font-bold border">
            <span :class="getStatusDot(row.status)" class="h-1.5 w-1.5 rounded-full"></span>
            {{ getStatusLabel(row.status) }}
          </span>
        </template>

        <template #cell-created_at="{ row }">
          <span class="font-mono text-gray-500 dark:text-gray-400 text-[11px]">{{ formatDate(row.created_at) }}</span>
        </template>

        <template #cell-updated_at="{ row }">
          <span class="font-mono text-gray-500 dark:text-gray-400 text-[11px]">{{ formatDate(row.updated_at) }}</span>
        </template>

        <template #cell-current_step="{ row }">
          <span class="text-gray-600 dark:text-gray-400">{{ row.current_step_name || '-' }}</span>
        </template>

        <template #actions="{ row }">
          <RouterLink :to="`/services/forms/${row.id}`"
            class="inline-flex items-center gap-1.5 text-[10px] font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 dark:bg-brand-500/10 dark:hover:bg-brand-500/20 border border-brand-200/30 dark:border-brand-500/20 px-3 py-1.5 rounded-lg transition-all">
            عرض التفاصيل
          </RouterLink>
        </template>
      </DataTable>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import { useServicesStore } from '@/stores/services'

const columns = [
  { key: 'id', label: 'رقم الطلب' },
  { key: 'form_type', label: 'اسم الخدمة' },
  { key: 'personnel', label: 'مقدم الطلب' },
  { key: 'status', label: 'الحالة' },
  { key: 'created_at', label: 'تاريخ الإنشاء' },
  { key: 'updated_at', label: 'آخر تحديث' },
  { key: 'current_step', label: 'الجهة الحالية' },
]

const route = useRoute()
const servicesStore = useServicesStore()
const filterType = ref(route.query.type as string || '')
const serviceTitle = ref('')
const filterStatus = ref('all')
const searchText = ref('')
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
  let list = allRequests.value
  if (filterStatus.value !== 'all') {
    list = list.filter(r => r.status === filterStatus.value)
  }
  if (searchText.value.trim()) {
    const q = searchText.value.trim().toLowerCase()
    list = list.filter(r => 
      String(r.id).includes(q) ||
      (r.personnel_name || '').toLowerCase().includes(q) ||
      (r.personnel_military_number || '').includes(q) ||
      (r.form_type_display || r.form_type || '').toLowerCase().includes(q)
    )
  }
  return list
})

const requestStats = computed(() => {
  const r = allRequests.value
  return [
    {
      label: 'الكل', value: r.length, dotClass: 'bg-gray-400',
      cardClass: 'border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900',
      iconBgClass: 'bg-gray-100 dark:bg-gray-800',
      labelColorClass: 'text-gray-600 dark:text-gray-400',
      valueColorClass: 'text-gray-900 dark:text-white',
    },
    {
      label: 'قيد الانتظار', value: r.filter(x => x.status === 'in_progress').length, dotClass: 'bg-blue-500',
      cardClass: 'border-blue-200 bg-blue-50 dark:border-blue-500/20 dark:bg-blue-500/5',
      iconBgClass: 'bg-blue-100 dark:bg-blue-500/20',
      labelColorClass: 'text-blue-700 dark:text-blue-400',
      valueColorClass: 'text-blue-900 dark:text-blue-300',
    },
    {
      label: 'تمت الموافقة', value: r.filter(x => x.status === 'approved').length, dotClass: 'bg-emerald-500',
      cardClass: 'border-success-200 bg-success-50 dark:border-success-500/20 dark:bg-success-500/5',
      iconBgClass: 'bg-success-100 dark:bg-success-500/20',
      labelColorClass: 'text-success-700 dark:text-success-400',
      valueColorClass: 'text-success-900 dark:text-success-300',
    },
    {
      label: 'قيد التنفيذ', value: r.filter(x => x.status === 'executing').length, dotClass: 'bg-indigo-500',
      cardClass: 'border-indigo-200 bg-indigo-50 dark:border-indigo-500/20 dark:bg-indigo-500/5',
      iconBgClass: 'bg-indigo-100 dark:bg-indigo-500/20',
      labelColorClass: 'text-indigo-700 dark:text-indigo-400',
      valueColorClass: 'text-indigo-900 dark:text-indigo-300',
    },
    {
      label: 'مرفوض', value: r.filter(x => x.status === 'rejected').length, dotClass: 'bg-red-500',
      cardClass: 'border-error-200 bg-error-50 dark:border-error-500/20 dark:bg-error-500/5',
      iconBgClass: 'bg-error-100 dark:bg-error-500/20',
      labelColorClass: 'text-error-700 dark:text-error-400',
      valueColorClass: 'text-error-900 dark:text-error-300',
    },
    {
      label: 'ملغى', value: r.filter(x => x.status === 'cancelled').length, dotClass: 'bg-orange-500',
      cardClass: 'border-orange-200 bg-orange-50 dark:border-orange-500/20 dark:bg-orange-500/5',
      iconBgClass: 'bg-orange-100 dark:bg-orange-500/20',
      labelColorClass: 'text-orange-700 dark:text-orange-400',
      valueColorClass: 'text-orange-900 dark:text-orange-300',
    },
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
    draft: 'bg-gray-100 text-gray-600 border-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700',
    in_progress: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20',
    approved: 'bg-success-50 text-success-700 border-success-200 dark:bg-success-500/10 dark:text-success-400 dark:border-success-500/20',
    executing: 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-500/10 dark:text-indigo-400 dark:border-indigo-500/20',
    completed: 'bg-teal-50 text-teal-700 border-teal-200 dark:bg-teal-500/10 dark:text-teal-400 dark:border-teal-500/20',
    rejected: 'bg-error-50 text-error-700 border-error-200 dark:bg-error-500/10 dark:text-error-400 dark:border-error-500/20',
    cancelled: 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-500/10 dark:text-orange-400 dark:border-orange-500/20',
  }
  return c[s] || 'bg-gray-100 text-gray-600 border-gray-200'
}

function getStatusDot(s: string) {
  const d: any = { draft: 'bg-gray-400', in_progress: 'bg-blue-500', approved: 'bg-emerald-500', executing: 'bg-indigo-500', completed: 'bg-teal-500', rejected: 'bg-red-500', cancelled: 'bg-orange-500' }
  return d[s] || 'bg-gray-400'
}
</script>
