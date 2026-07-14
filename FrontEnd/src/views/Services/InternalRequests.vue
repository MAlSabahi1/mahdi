<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="الطلبات الداخلية" />

    <div class="space-y-6 text-start" dir="rtl">

      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-blue-50 dark:bg-blue-500/10 rounded-xl text-blue-600 dark:text-blue-400">
              <UserCheck class="h-6 w-6" />
            </div>
            الطلبات الداخلية
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            تُعالج وتُعتمد بالكامل داخل المنظومة المحلية عبر سلسلة موافقات متدرجة.
          </p>
        </div>

        <!-- Active Stage Badge -->
        <div class="flex items-center gap-4 flex-shrink-0">
          <div v-if="activeStageFilter !== 'all'" class="flex items-center gap-2 bg-blue-50 dark:bg-blue-500/10 text-blue-700 dark:text-blue-300 text-xs font-bold px-4 py-2 rounded-xl border border-blue-200 dark:border-blue-500/20">
            <span class="h-1.5 w-1.5 rounded-full bg-blue-500 animate-pulse"></span>
            {{ stageLabels[activeStageFilter] || activeStageFilter }}
          </div>
        </div>
      </div>

      <!-- Stats Row -->
      <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <div v-for="stat in stats" :key="stat.label"
          class="rounded-2xl border p-4 shadow-theme-xs" :class="stat.cardClass">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-full" :class="stat.iconBgClass">
              <span :class="stat.dotClass" class="h-3 w-3 rounded-full"></span>
            </div>
            <div class="text-start">
              <p class="text-xs font-medium" :class="stat.labelColorClass">{{ stat.label }}</p>
              <h3 class="text-xl font-bold font-mono" :class="stat.valueColorClass">{{ stat.value }}</h3>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <DataTable
        :columns="columns"
        :data="filteredRequests"
        rowKey="id"
        :loading="loading"
        searchPlaceholder="بحث بالاسم أو رقم الطلب..."
        @search="val => searchText = val"
        @refresh="() => { /* Add refresh logic here if needed or re-fetch */ }"
        emptyTitle="لا توجد طلبات داخلية"
        emptyDescription="لا توجد طلبات داخلية بهذه المعايير"
        actionsWidth="200px"
      >
        <!-- Toolbar Actions: Filters -->
        <template #toolbar-actions>
          <div class="flex flex-wrap items-center gap-3">
            <!-- Stage Filter Tabs -->
            <div class="flex gap-1.5 flex-wrap">
              <button v-for="stage in stageOptions" :key="stage.value"
                @click="activeStageFilter = stage.value"
                :class="activeStageFilter === stage.value
                  ? 'bg-blue-600 text-white border-blue-500 shadow-md shadow-blue-500/20'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700'"
                class="px-3.5 py-2 text-[11px] font-bold rounded-lg border transition-all flex items-center gap-1.5 cursor-pointer">
                <span class="w-1.5 h-1.5 rounded-full" :class="stage.dot"></span>
                {{ stage.label }}
                <span v-if="stage.value !== 'all' && (stageCounts[stage.value] || 0) > 0"
                  :class="activeStageFilter === stage.value ? 'bg-white/20 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'"
                  class="rounded-md px-1.5 text-[9px] font-bold">
                  {{ stageCounts[stage.value] || 0 }}
                </span>
              </button>
            </div>

            <!-- Service Type Filter -->
            <div class="relative min-w-[160px]">
              <select v-model="filterServiceType"
                class="dark:bg-dark-900 h-10 w-full appearance-none rounded-lg border bg-transparent px-4 py-2 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option value="">جميع الأنواع</option>
                <option value="form">الاستمارات (إثبات حالة)</option>
                <option value="correction">تصحيحات البيانات</option>
                <option value="rank_settlement">الترقيات والتسويات</option>
                <option value="disciplinary">الجزاءات والانضباط</option>
                <option value="security">الأمان والوصول</option>
              </select>
            </div>
          </div>
        </template>

        <template #cell-id="{ row }">
          <template v-if="row.isCorrection">
            <button @click="showCorrectionDetails(row)" class="text-blue-600 hover:underline hover:text-blue-700 font-mono font-bold">
              #{{ String(row.rawId).padStart(5, '0') }}
            </button>
          </template>
          <template v-else>
            <RouterLink :to="`/services/forms/${row.id}`"
              class="text-blue-600 hover:underline hover:text-blue-700 font-mono font-bold">
              #{{ String(row.id).padStart(5, '0') }}
            </RouterLink>
          </template>
        </template>

        <template #cell-service_type="{ row }">
          <span class="inline-flex items-center gap-1.5 text-gray-800 dark:text-gray-200 font-bold">
            <span :class="serviceTypeColor(row.service_type)" class="h-1.5 w-1.5 rounded-full flex-shrink-0"></span>
            {{ row.form_type_display || row.form_type }}
          </span>
        </template>

        <template #cell-personnel="{ row }">
          <span class="text-gray-700 dark:text-gray-300">{{ row.personnel_name || '—' }}</span>
        </template>

        <template #cell-military_number="{ row }">
          <span class="font-mono text-gray-500 dark:text-gray-400 text-[11px]">{{ row.personnel_military_number || '—' }}</span>
        </template>

        <template #cell-attachments="{ row }">
          <button v-if="row.attachments_count > 0" @click="showAttachments(row)"
            class="inline-flex items-center gap-1 text-[10px] font-bold px-2.5 py-1 rounded-lg bg-brand-50 text-brand-600 hover:bg-brand-100 dark:bg-brand-500/10 dark:text-brand-400 border border-brand-200 dark:border-brand-500/20 transition-colors cursor-pointer">
            <Paperclip class="w-3 h-3" />
            {{ row.attachments_count }}
          </button>
          <span v-else class="text-[10px] text-gray-400">—</span>
        </template>

        <template #cell-status="{ row }">
          <span :class="stageColor(row.status)"
            class="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[10px] font-bold border">
            <span :class="stageDot(row.status)" class="h-1.5 w-1.5 rounded-full"></span>
            {{ stageLabels[row.status] || row.status }}
          </span>
        </template>

        <template #cell-date="{ row }">
          <span class="font-mono text-gray-500 dark:text-gray-400 text-[11px]">
            {{ row.submitted_at ? new Date(row.submitted_at).toLocaleDateString('en-GB') : '—' }}
          </span>
        </template>

        <template #actions="{ row }">
          <button v-if="canApprove(row)"
            @click="approveReq(row)"
            class="bg-success-600 hover:bg-success-700 text-white text-[10px] font-bold px-2.5 py-1.5 rounded-lg cursor-pointer transition-colors shadow-sm">
            اعتماد
          </button>
          <button v-if="canApprove(row)"
            @click="rejectReq(row)"
            class="bg-error-50 hover:bg-error-100 text-error-600 border border-error-200 dark:bg-error-500/10 dark:text-error-400 dark:border-error-500/20 text-[10px] font-bold px-2.5 py-1.5 rounded-lg cursor-pointer transition-colors">
            رفض
          </button>
          <template v-if="row.isCorrection">
            <button @click="showCorrectionDetails(row)"
              class="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-[10px] font-bold hover:underline px-1">
              التفاصيل
            </button>
          </template>
          <template v-else>
            <RouterLink :to="`/services/forms/${row.id}`"
              class="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-[10px] font-bold hover:underline px-1">
              التفاصيل
            </RouterLink>
          </template>
        </template>
      </DataTable>


    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import { UserCheck, Search, FileX, Paperclip } from 'lucide-vue-next'
import { useServicesStore } from '@/stores/services'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const columns = [
  { key: 'id', label: 'رقم الطلب' },
  { key: 'service_type', label: 'نوع الخدمة' },
  { key: 'personnel', label: 'الفرد' },
  { key: 'military_number', label: 'الرقم العسكري' },
  { key: 'attachments', label: 'المرفقات' },
  { key: 'status', label: 'المرحلة الحالية' },
  { key: 'date', label: 'تاريخ التقديم' },
]

const servicesStore = useServicesStore()
const authStore = useAuthStore()

const allRequests = ref<any[]>([])
const loading = ref(false)
const activeStageFilter = ref('all')
const filterServiceType = ref('')
const searchText = ref('')

// ── الحالات الداخلية ──────────────────────────────────
const stageLabels: Record<string, string> = {
  all:               'الكل',
  draft:             'مسودة',
  in_progress:       'قيد الإجراء',
  pending_services:  'عند رئيس قسم الخدمات',
  pending_hr:        'عند مدير إدارة القوى البشرية',
  pending_director:  'عند المدير العام للمحافظة',
  approved:          'معتمد نهائياً',
  rejected:          'مرفوض',
  returned:          'مُرجع للتعديل',
  cancelled:         'ملغى',
}

const stageOptions = [
  { value: 'all',              label: 'الكل',                            dot: 'bg-gray-400' },
  { value: 'pending_services', label: 'عند رئيس قسم الخدمات',       dot: 'bg-amber-500' },
  { value: 'pending_hr',       label: 'عند مدير إدارة القوى البشرية', dot: 'bg-blue-500'  },
  { value: 'pending_director', label: 'عند المدير العام للمحافظة',      dot: 'bg-purple-500'},
  { value: 'approved',         label: 'معتمدة',                          dot: 'bg-emerald-500'},
  { value: 'rejected',         label: 'مرفوضة',                          dot: 'bg-red-500'  },
]

// ── الإحصائيات ──────────────────────────────────────────
const stageCounts = computed(() => {
  const counts: Record<string, number> = {}
  for (const req of allRequests.value) {
    counts[req.status] = (counts[req.status] || 0) + 1
  }
  return counts
})

const stats = computed(() => [
  {
    label: 'إجمالي', value: allRequests.value.length,
    dotClass: 'bg-gray-400',
    cardClass: 'border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900',
    iconBgClass: 'bg-gray-100 dark:bg-gray-800',
    labelColorClass: 'text-gray-600 dark:text-gray-400',
    valueColorClass: 'text-gray-900 dark:text-white',
  },
  {
    label: 'عند رئيس الخدمات', value: stageCounts.value['pending_services'] || 0,
    dotClass: 'bg-amber-500',
    cardClass: 'border-warning-200 bg-warning-50 dark:border-warning-500/20 dark:bg-warning-500/5',
    iconBgClass: 'bg-warning-100 dark:bg-warning-500/20',
    labelColorClass: 'text-warning-700 dark:text-warning-400',
    valueColorClass: 'text-warning-900 dark:text-warning-300',
  },
  {
    label: 'عند مدير إدارة القوى البشرية', value: stageCounts.value['pending_hr'] || 0,
    dotClass: 'bg-blue-500',
    cardClass: 'border-blue-200 bg-blue-50 dark:border-blue-500/20 dark:bg-blue-500/5',
    iconBgClass: 'bg-blue-100 dark:bg-blue-500/20',
    labelColorClass: 'text-blue-700 dark:text-blue-400',
    valueColorClass: 'text-blue-900 dark:text-blue-300',
  },
  {
    label: 'عند المدير العام للمحافظة', value: stageCounts.value['pending_director'] || 0,
    dotClass: 'bg-purple-500',
    cardClass: 'border-purple-200 bg-purple-50 dark:border-purple-500/20 dark:bg-purple-500/5',
    iconBgClass: 'bg-purple-100 dark:bg-purple-500/20',
    labelColorClass: 'text-purple-700 dark:text-purple-400',
    valueColorClass: 'text-purple-900 dark:text-purple-300',
  },
  {
    label: 'معتمدة', value: stageCounts.value['approved'] || 0,
    dotClass: 'bg-emerald-500',
    cardClass: 'border-success-200 bg-success-50 dark:border-success-500/20 dark:bg-success-500/5',
    iconBgClass: 'bg-success-100 dark:bg-success-500/20',
    labelColorClass: 'text-success-700 dark:text-success-400',
    valueColorClass: 'text-success-900 dark:text-success-300',
  },
])

// ── الفلترة ──────────────────────────────────────────────
const filteredRequests = computed(() => {
  let list = allRequests.value
  if (activeStageFilter.value !== 'all') {
    list = list.filter(r => r.status === activeStageFilter.value)
  }
  if (filterServiceType.value) {
    list = list.filter(r => r.service_type === filterServiceType.value)
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

// ── ألوان ────────────────────────────────────────────────
function stageColor(status: string) {
  const m: Record<string, string> = {
    draft:             'bg-gray-100 text-gray-600 border-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700',
    in_progress:       'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20',
    pending_services:  'bg-warning-50 text-warning-700 border-warning-200 dark:bg-warning-500/10 dark:text-warning-400 dark:border-warning-500/20',
    pending_hr:        'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20',
    pending_director:  'bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-500/10 dark:text-purple-400 dark:border-purple-500/20',
    approved:          'bg-success-50 text-success-700 border-success-200 dark:bg-success-500/10 dark:text-success-400 dark:border-success-500/20',
    rejected:          'bg-error-50 text-error-700 border-error-200 dark:bg-error-500/10 dark:text-error-400 dark:border-error-500/20',
    returned:          'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-500/10 dark:text-orange-400 dark:border-orange-500/20',
  }
  return m[status] || 'bg-gray-100 text-gray-600 border-gray-200'
}

function stageDot(status: string) {
  const m: Record<string, string> = {
    draft: 'bg-gray-400', in_progress: 'bg-blue-500',
    pending_services: 'bg-amber-500', pending_hr: 'bg-blue-500',
    pending_director: 'bg-purple-500', approved: 'bg-emerald-500',
    rejected: 'bg-red-500', returned: 'bg-orange-500',
  }
  return m[status] || 'bg-gray-400'
}

function serviceTypeColor(type: string) {
  const m: Record<string, string> = {
    form:            'bg-blue-500',
    correction:      'bg-sky-500',
    rank_settlement: 'bg-indigo-500',
    disciplinary:    'bg-red-500',
    security:        'bg-gray-500',
  }
  return m[type] || 'bg-gray-400'
}

// ── صلاحية الاعتماد حسب دور المستخدم ──────────────────
function canApprove(req: any): boolean {
  if (req.status === 'approved' || req.status === 'rejected') return false
  if (authStore.isAdmin) return true
  const role = authStore.user?.authz_profile?.role_name || ''
  const roleCode = authStore.user?.authz_profile?.role_code || ''
  const pending = req.status
  if (pending === 'pending_services' && (roleCode === 'services_dept' || role.includes('الخدمات'))) return true
  if (pending === 'pending_hr'       && (roleCode === 'hr_director' || role.includes('القوى البشرية') || role.includes('مدير إدارة'))) return true
  if (pending === 'pending_director' && (roleCode === 'governor_general' || role.includes('المدير العام'))) return true
  if (pending === 'in_progress' || pending === 'draft') return false
  return false
}

// ── تحميل البيانات ──────────────────────────────────────
onMounted(async () => {
  loading.value = true
  try {
    const res = await servicesStore.fetchForms({ approval_type: 'internal' })
    const formsList = (res?.results || res || []).map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || '',
      service_type: f.service_type || 'form',
      attachments_count: f.attachments?.length || 0,
      attachments_list: f.attachments || [],
    }))

    const correctionsRes = await api.get('/personnel/corrections/')
    const correctionsList = (correctionsRes.data?.results || correctionsRes.data || [])
      .map((c: any) => ({
        id: `corr-${c.id}`,
        rawId: c.id,
        isCorrection: true,
        service_type: 'correction',
        form_type: c.correction_type,
        form_type_display: c.correction_type === 'national_id_correction' ? 'طلب تصحيح الرقم الوطني'
          : c.correction_type === 'military_number_correction' ? 'طلب تصحيح الرقم العسكري'
          : c.correction_type === 'name_correction' ? 'طلب تصحيح الاسم' : c.correction_type,
        personnel_name: c.personnel_name,
        personnel_military_number: c.personnel_military_number,
        status: c.status === 'pending' ? 'pending_services' : c.status,
        status_display: c.status_display,
        submitted_at: c.requested_at,
        notes: c.notes,
        old_value: c.old_value,
        new_value: c.new_value,
        attachments_count: c.documents?.length || 0,
        attachments_list: c.documents || [],
      }))

    allRequests.value = [...formsList, ...correctionsList]
  } catch (e) {
    console.error('Failed to fetch internal requests', e)
  } finally {
    loading.value = false
  }
})

// ── الإجراءات ────────────────────────────────────────────
async function approveReq(req: any) {
  const result = await Swal.fire({
    title: 'تأكيد الاعتماد',
    html: `<p class="text-sm text-gray-600">سيتم اعتماد الطلب <strong>#${String(req.isCorrection ? req.rawId : req.id).padStart(5,'0')}</strong> ونقله للمرحلة التالية.</p>`,
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتماد',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981',
  })
  if (result.isConfirmed) {
    try {
      if (req.isCorrection) {
        await api.post(`/personnel/corrections/${req.rawId}/approve/`)
        const idx = allRequests.value.findIndex(r => r.id === req.id)
        if (idx !== -1) {
          allRequests.value[idx].status = 'approved'
        }
      } else {
        await servicesStore.approveForm(req.id)
        const idx = allRequests.value.findIndex(r => r.id === req.id)
        if (idx !== -1) {
          const nextStage: Record<string, string> = {
            pending_services: 'pending_hr',
            pending_hr:       'pending_director',
            pending_director: 'approved',
            in_progress:      'approved',
          }
          allRequests.value[idx].status = nextStage[req.status] || 'approved'
        }
      }
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الاعتماد بنجاح', showConfirmButton: false, timer: 2500 })
    } catch (e: any) {
      Swal.fire({ icon: 'error', title: 'خطأ', text: e?.response?.data?.error || 'حدث خطأ أثناء الاعتماد' })
    }
  }
}

async function rejectReq(req: any) {
  const result = await Swal.fire({
    title: 'رفض الطلب',
    input: 'textarea',
    inputPlaceholder: 'اكتب سبب الرفض بوضوح...',
    inputAttributes: { dir: 'rtl', rows: '3' },
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444',
    inputValidator: (value) => !value ? 'يجب كتابة سبب الرفض' : undefined,
  })
  if (result.isConfirmed && result.value) {
    try {
      if (req.isCorrection) {
        await api.post(`/personnel/corrections/${req.rawId}/reject/`, { reason: result.value })
      } else {
        await servicesStore.rejectForm(req.id, result.value)
      }
      const idx = allRequests.value.findIndex(r => r.id === req.id)
      if (idx !== -1) allRequests.value[idx].status = 'rejected'
      Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض الطلب', showConfirmButton: false, timer: 2500 })
    } catch (e: any) {
      Swal.fire({ icon: 'error', title: 'خطأ', text: e?.response?.data?.error || 'حدث خطأ أثناء الرفض' })
    }
  }
}

function showAttachments(req: any) {
  const attachments = req.attachments_list || []
  if (attachments.length === 0) return

  const rows = attachments.map((att: any, idx: number) => {
    const docType = att.document_type || att.doc_type || 'مستند'
    const fileUrl = att.file || att.url || '#'
    return `
      <div class="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-xl mb-2">
        <div class="flex items-center gap-3">
          <span class="bg-brand-50 text-brand-600 font-bold text-[10px] w-7 h-7 rounded-lg flex items-center justify-center">${idx + 1}</span>
          <div>
            <p class="text-sm font-bold text-gray-800">${docType}</p>
            <p class="text-[10px] text-gray-400">ID: ${att.id || '—'}</p>
          </div>
        </div>
        <a href="${fileUrl}" target="_blank" class="text-[10px] font-bold text-brand-600 bg-brand-50 px-3 py-1.5 rounded-lg hover:bg-brand-100">معاينة</a>
      </div>
    `
  }).join('')

  Swal.fire({
    title: `المرفقات (${attachments.length})`,
    html: `<div class="text-right space-y-1 max-h-[400px] overflow-y-auto" dir="rtl">${rows}</div>`,
    width: 500,
    confirmButtonText: 'إغلاق',
    confirmButtonColor: '#3b82f6',
  })
}

function showCorrectionDetails(req: any) {
  Swal.fire({
    title: req.form_type_display,
    html: `
      <div class="text-right text-sm space-y-2" dir="rtl">
        <div><strong>الاسم:</strong> ${req.personnel_name}</div>
        <div><strong>الرقم العسكري:</strong> ${req.personnel_military_number}</div>
        <hr class="my-2 border-gray-200 dark:border-gray-700" />
        <div><strong>القيمة الحالية:</strong> <span class="text-red-600 font-mono">${req.old_value || '—'}</span></div>
        <div><strong>القيمة المقترحة:</strong> <span class="text-emerald-600 font-bold font-mono">${req.new_value || '—'}</span></div>
        <hr class="my-2 border-gray-200 dark:border-gray-700" />
        <div><strong>ملاحظات/السبب:</strong> ${req.notes || '—'}</div>
      </div>
    `,
    icon: 'info',
    confirmButtonText: 'إغلاق',
    confirmButtonColor: '#3b82f6'
  })
}
</script>
