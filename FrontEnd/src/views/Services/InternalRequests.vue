<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="الطلبات الداخلية" />

    <div class="space-y-6 text-start" dir="rtl">

      <!-- Header -->
      <div class="relative overflow-hidden rounded-2xl border border-blue-200 dark:border-blue-900/40 bg-gradient-to-br from-blue-50 to-white dark:from-blue-950/10 dark:to-gray-900 p-6 shadow-sm">
        <div class="absolute -left-10 -top-10 w-40 h-40 bg-blue-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative flex items-center justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-xl border border-blue-200/60 dark:border-blue-800">
              <UserCheck class="h-6 w-6" />
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">الطلبات الداخلية</h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                تُعالج وتُعتمد بالكامل داخل المنظومة المحلية عبر سلسلة موافقات متدرجة.
              </p>
            </div>
          </div>
          <!-- Active Stage Badge -->
          <div v-if="activeStageFilter !== 'all'" class="flex items-center gap-2 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-bold px-3 py-1.5 rounded-full border border-blue-200 dark:border-blue-800">
            <span class="h-1.5 w-1.5 rounded-full bg-blue-500 animate-pulse"></span>
            {{ stageLabels[activeStageFilter] || activeStageFilter }}
          </div>
        </div>
      </div>

      <!-- Stats Row -->
      <div class="grid grid-cols-2 lg:grid-cols-5 gap-3">
        <div v-for="stat in stats" :key="stat.label"
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 shadow-sm">
          <p class="text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">{{ stat.label }}</p>
          <div class="flex items-center justify-between">
            <p class="text-lg font-black text-gray-900 dark:text-white font-mono">{{ stat.value }}</p>
            <span :class="stat.dotClass" class="h-2.5 w-2.5 rounded-full"></span>
          </div>
        </div>
      </div>

      <!-- Filters Row -->
      <div class="flex flex-wrap gap-2 items-center">
        <!-- Stage Filter Tabs -->
        <div class="flex gap-1.5 flex-wrap">
          <button v-for="stage in stageOptions" :key="stage.value"
            @click="activeStageFilter = stage.value"
            :class="activeStageFilter === stage.value
              ? 'bg-blue-600 text-white border-blue-500 shadow-md shadow-blue-500/20'
              : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-800 hover:bg-gray-50'"
            class="px-3 py-1.5 text-[11px] font-bold rounded-lg border transition-all flex items-center gap-1.5 cursor-pointer">
            <span class="w-1.5 h-1.5 rounded-full" :class="stage.dot"></span>
            {{ stage.label }}
            <span v-if="stage.value !== 'all'" class="bg-white/30 text-white rounded px-1 text-[9px] font-black" :class="activeStageFilter === stage.value ? '' : 'hidden'">
              {{ stageCounts[stage.value] || 0 }}
            </span>
          </button>
        </div>

        <div class="flex-1"></div>

        <!-- Service Type Filter -->
        <select v-model="filterServiceType"
          class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 min-w-[140px]">
          <option value="">جميع الأنواع</option>
          <option value="correction">تصحيحات البيانات</option>
          <option value="rank_settlement">الترقيات والتسويات</option>
          <option value="disciplinary">الجزاءات والانضباط</option>
          <option value="security">الأمان والوصول</option>
        </select>

        <!-- Search -->
        <div class="relative">
          <Search class="absolute right-2.5 top-2 h-3.5 w-3.5 text-gray-400" />
          <input v-model="searchText" type="text" placeholder="بحث بالاسم أو رقم الطلب..."
            class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg py-2 pr-8 pl-3 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 w-48 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-450 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-4 py-3">رقم الطلب</th>
                <th class="px-4 py-3">نوع الخدمة</th>
                <th class="px-4 py-3">الفرد</th>
                <th class="px-4 py-3">الرقم العسكري</th>
                <th class="px-4 py-3">المرحلة الحالية</th>
                <th class="px-4 py-3">تاريخ التقديم</th>
                <th class="px-4 py-3 text-center w-[180px]">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-800/60">
              <tr v-if="loading">
                <td colspan="7" class="px-4 py-12 text-center text-gray-400">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </td>
              </tr>
              <tr v-else-if="filteredRequests.length === 0">
                <td colspan="7" class="px-4 py-12 text-center">
                  <div class="flex flex-col items-center gap-3 text-gray-400">
                    <FileX class="h-10 w-10 opacity-30" />
                    <p class="text-sm font-bold">لا توجد طلبات داخلية بهذه المعايير</p>
                  </div>
                </td>
              </tr>
              <tr v-for="req in filteredRequests" :key="req.id"
                class="hover:bg-blue-50/30 dark:hover:bg-blue-950/10 transition-colors group">
                <td class="px-4 py-3 font-mono font-bold">
                  <template v-if="req.isCorrection">
                    <button @click="showCorrectionDetails(req)" class="text-blue-600 hover:underline hover:text-blue-700">
                      #{{ String(req.rawId).padStart(5, '0') }}
                    </button>
                  </template>
                  <template v-else>
                    <RouterLink :to="`/services/forms/${req.id}`"
                      class="text-blue-600 hover:underline hover:text-blue-700">
                      #{{ String(req.id).padStart(5, '0') }}
                    </RouterLink>
                  </template>
                </td>
                <td class="px-4 py-3">
                  <span class="inline-flex items-center gap-1.5 text-gray-800 dark:text-gray-200 font-bold">
                    <span :class="serviceTypeColor(req.service_type)" class="h-1.5 w-1.5 rounded-full flex-shrink-0"></span>
                    {{ req.form_type_display || req.form_type }}
                  </span>
                </td>
                <td class="px-4 py-3 text-gray-700 dark:text-gray-300">{{ req.personnel_name || '—' }}</td>
                <td class="px-4 py-3 font-mono text-gray-500 text-[11px]">{{ req.personnel_military_number || '—' }}</td>
                <td class="px-4 py-3">
                  <span :class="stageColor(req.status)"
                    class="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[10px] font-bold border">
                    <span :class="stageDot(req.status)" class="h-1.5 w-1.5 rounded-full"></span>
                    {{ stageLabels[req.status] || req.status }}
                  </span>
                </td>
                <td class="px-4 py-3 font-mono text-gray-450 text-[11px]">
                  {{ req.submitted_at ? new Date(req.submitted_at).toLocaleDateString('en-GB') : '—' }}
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center justify-center gap-1.5">
                    <!-- Approve: only if current stage matches user role -->
                    <button v-if="canApprove(req)"
                      @click="approveReq(req)"
                      class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm">
                      اعتماد
                    </button>
                    <button v-if="canApprove(req)"
                      @click="rejectReq(req)"
                      class="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors">
                      رفض
                    </button>
                    <template v-if="req.isCorrection">
                      <button @click="showCorrectionDetails(req)"
                        class="text-blue-600 hover:text-blue-700 text-[10px] font-bold hover:underline px-1">
                        التفاصيل
                      </button>
                    </template>
                    <template v-else>
                      <RouterLink :to="`/services/forms/${req.id}`"
                        class="text-blue-600 hover:text-blue-700 text-[10px] font-bold hover:underline px-1">
                        التفاصيل
                      </RouterLink>
                    </template>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination Info -->
      <div v-if="!loading && allRequests.length > 0" class="text-xs text-gray-500 text-center">
        عرض {{ filteredRequests.length }} من {{ allRequests.length }} طلب
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { UserCheck, Search, FileX } from 'lucide-vue-next'
import { useServicesStore } from '@/stores/services'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'
import api from '@/lib/api'

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
  in_progress:       'قيد المراجعة',
  pending_services:  'عند رئيس الخدمات',
  pending_hr:        'عند مدير الموارد',
  pending_director:  'عند المدير العام',
  approved:          'معتمد نهائياً',
  rejected:          'مرفوض',
  returned:          'مُرجع للتعديل',
  cancelled:         'ملغى',
}

const stageOptions = [
  { value: 'all',              label: 'الكل',              dot: 'bg-gray-400' },
  { value: 'pending_services', label: 'عند رئيس الخدمات', dot: 'bg-amber-500' },
  { value: 'pending_hr',       label: 'عند مدير الموارد', dot: 'bg-blue-500'  },
  { value: 'pending_director', label: 'عند المدير العام',  dot: 'bg-purple-500'},
  { value: 'approved',         label: 'معتمدة',            dot: 'bg-emerald-500'},
  { value: 'rejected',         label: 'مرفوضة',            dot: 'bg-red-500'  },
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
  { label: 'إجمالي',            value: allRequests.value.length, dotClass: 'bg-gray-400' },
  { label: 'عند رئيس الخدمات', value: stageCounts.value['pending_services'] || 0, dotClass: 'bg-amber-500' },
  { label: 'عند مدير الموارد', value: stageCounts.value['pending_hr'] || 0,       dotClass: 'bg-blue-500'  },
  { label: 'عند المدير العام',  value: stageCounts.value['pending_director'] || 0, dotClass: 'bg-purple-500'},
  { label: 'معتمدة',            value: stageCounts.value['approved'] || 0,         dotClass: 'bg-emerald-500'},
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
    in_progress:       'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/20 dark:text-blue-400 dark:border-blue-900',
    pending_services:  'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/20 dark:text-amber-400 dark:border-amber-900',
    pending_hr:        'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/20 dark:text-blue-400 dark:border-blue-900',
    pending_director:  'bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/20 dark:text-purple-400 dark:border-purple-900',
    approved:          'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/20 dark:text-emerald-400 dark:border-emerald-900',
    rejected:          'bg-red-50 text-red-700 border-red-200 dark:bg-red-950/20 dark:text-red-400 dark:border-red-900',
    returned:          'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-950/20 dark:text-orange-400 dark:border-orange-900',
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
  const role = authStore.user?.authz_profile?.role_name || ''
  const pending = req.status
  if (pending === 'pending_services' && (role.includes('رئيس الخدمات') || authStore.isAdmin)) return true
  if (pending === 'pending_hr'       && (role.includes('مدير الموارد') || authStore.isAdmin)) return true
  if (pending === 'pending_director' && (role.includes('المدير العام') || authStore.isAdmin)) return true
  if ((pending === 'in_progress' || pending === 'draft') && authStore.isAdmin) return true
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
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || ''
    }))

    const correctionsRes = await api.get('/personnel/corrections/')
    const correctionsList = (correctionsRes.data?.results || correctionsRes.data || [])
      .filter((c: any) => c.correction_type === 'national_id_correction' || c.correction_type === 'military_number_correction')
      .map((c: any) => ({
        id: `corr-${c.id}`,
        rawId: c.id,
        isCorrection: true,
        service_type: 'correction',
        form_type: c.correction_type,
        form_type_display: c.correction_type === 'national_id_correction' ? 'طلب تصحيح الرقم الوطني' : 'طلب تصحيح الرقم العسكري',
        personnel_name: c.personnel_name,
        personnel_military_number: c.personnel_military_number,
        status: c.status === 'pending' ? 'pending_services' : c.status,
        status_display: c.status_display,
        submitted_at: c.requested_at,
        notes: c.notes,
        old_value: c.old_value,
        new_value: c.new_value
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
