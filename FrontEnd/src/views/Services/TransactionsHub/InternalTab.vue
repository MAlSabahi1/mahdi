<template>
  <div class="space-y-4">
    <!-- Stage Filters -->
    <div class="flex flex-wrap gap-2 items-center">
      <button v-for="stage in stageOptions" :key="stage.value"
        @click="activeStage = stage.value"
        :class="activeStage === stage.value
          ? 'bg-blue-600 text-white border-blue-500 shadow-md shadow-blue-500/20'
          : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-800 hover:bg-gray-50'"
        class="px-3 py-1.5 text-[11px] font-bold rounded-lg border transition-all flex items-center gap-1.5 cursor-pointer">
        <span class="w-1.5 h-1.5 rounded-full" :class="stage.dot"></span>
        {{ stage.label }}
        <span v-if="stage.value !== 'all' && stageCounts[stage.value]"
          :class="activeStage === stage.value ? 'bg-white/30 text-white' : 'bg-gray-100 dark:bg-gray-800 text-gray-500'"
          class="text-[9px] font-black px-1.5 py-0.5 rounded-full">
          {{ stageCounts[stage.value] }}
        </span>
      </button>
    </div>

    <!-- DataTable -->
    <DataTable
      :columns="columns"
      :data="filteredRows"
      row-key="id"
      :loading="loading"
      :has-actions="true"
      actions-width="180px"
      :current-page="1"
      :total-pages="1"
      :total-count="filteredRows.length"
      :page-size="filteredRows.length || 50"
      search-placeholder="بحث بالاسم أو رقم الطلب..."
      empty-title="لا توجد طلبات داخلية"
      empty-description="لا توجد طلبات داخلية بهذه المعايير."
      @search="searchText = $event"
      @refresh="$emit('refresh')"
    >
      <template #cell-id="{ row }">
        <RouterLink :to="row.isCorrection ? '#' : `/services/forms/${row.id}`" class="text-blue-600 hover:underline font-mono font-bold">
          #{{ String(row.isCorrection ? row.rawId : row.id).padStart(5, '0') }}
        </RouterLink>
      </template>

      <template #cell-form_type_display="{ row }">
        <span class="font-bold text-gray-800 dark:text-gray-200">
          {{ (row.form_type_display || row.form_type || '').replace('returned_to_service', 'عائد للخدمة') }}
        </span>
      </template>

      <template #cell-personnel_name="{ row }">
        <RouterLink v-if="row.personnel_military_number" :to="`/personnel/${row.personnel_military_number}`" class="text-brand-600 hover:underline font-bold text-xs">
          {{ row.personnel_name || '—' }}
        </RouterLink>
        <span v-else>{{ row.personnel_name || '—' }}</span>
      </template>

      <template #cell-personnel_military_number="{ row }">
        <span class="font-mono text-gray-500 text-[11px]">{{ row.personnel_military_number || '—' }}</span>
      </template>

      <template #cell-status="{ row }">
        <span :class="stageColor(row.status)"
          class="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[10px] font-bold border">
          <span :class="stageDot(row.status)" class="h-1.5 w-1.5 rounded-full"></span>
          {{ getDisplayStatus(row) }}
        </span>
      </template>

      <template #cell-submitted_at="{ row }">
        <span class="font-mono text-gray-450 text-[11px]">{{ row.submitted_at ? new Date(row.submitted_at).toLocaleDateString('en-GB') : '—' }}</span>
      </template>

      <template #actions="{ row }">
        <!-- زر تقديم المسودة -->
        <button v-if="row.status === 'draft' && !row.isCorrection" @click="$emit('submit-draft', row)"
          class="bg-blue-600 hover:bg-blue-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg>
          تقديم
        </button>
        <button v-if="canApprove(row)" @click="$emit('approve', row)"
          class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm">
          اعتماد
        </button>
        <button v-if="canApprove(row)" @click="$emit('reject', row)"
          class="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors">
          رفض
        </button>
        <RouterLink :to="`/services/forms/${row.id}`"
          class="text-blue-600 hover:text-blue-700 text-[10px] font-bold hover:underline px-1">
          التفاصيل
        </RouterLink>
      </template>
    </DataTable>
    <div v-if="!loading && rows.length > 0" class="text-xs text-gray-500 text-center">
      عرض {{ filteredRows.length }} من {{ rows.length }} طلب
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import DataTable from '@/components/tables/DataTable.vue'

const props = defineProps<{ rows: any[]; loading: boolean }>()
defineEmits<{
  (e: 'approve', req: any): void
  (e: 'reject', req: any): void
  (e: 'submit-draft', req: any): void
  (e: 'refresh'): void
}>()

const authStore = useAuthStore()
const activeStage = ref('all')
const searchText = ref('')

const stageLabels: Record<string, string> = {
  all: 'الكل',
  draft: 'مسودة',
  in_progress: 'قيد الإجراء',
  approved: 'معتمد نهائياً',
  rejected: 'مرفوض',
  returned: 'مُرجع للتعديل',
  // الحالات القديمة — توافق مع بيانات DB
  pending_services:  'عند رئيس قسم الخدمات',
  pending_hr:        'عند مدير إدارة القوى البشرية',
  pending_director:  'عند المدير العام للمحافظة',
}

// عرض ذكي: إذا كانت in_progress فأظهر اسم الخطوة الحالية من الابي
function getDisplayStatus(row: any): string {
  // الحالة التفصيلية: in_progress مع اسم الخطوة
  if (row.status === 'in_progress' && row.current_step_name) {
    const stepIdx = row.current_step_index != null ? ` (مرحلة ${row.current_step_index + 1})` : ''
    return `عند: ${row.current_step_name}${stepIdx}`
  }
  return stageLabels[row.status] || row.status
}

const columns = [
  { key: 'id', label: 'رقم الطلب', minWidth: '100px' },
  { key: 'form_type_display', label: 'نوع الخدمة', minWidth: '140px' },
  { key: 'personnel_name', label: 'الفرد', minWidth: '160px' },
  { key: 'personnel_military_number', label: 'الرقم العسكري', minWidth: '120px' },
  { key: 'status', label: 'المرحلة الحالية', minWidth: '170px' },
  { key: 'submitted_at', label: 'تاريخ التقديم', minWidth: '110px' },
]

const stageOptions = [
  { value: 'all', label: 'الكل', dot: 'bg-gray-400' },
  { value: 'in_progress', label: 'قيد المراجعة', dot: 'bg-blue-500' },
  { value: 'draft', label: 'مسودة', dot: 'bg-gray-400' },
  { value: 'approved', label: 'معتمدة', dot: 'bg-emerald-500' },
  { value: 'rejected', label: 'مرفوضة', dot: 'bg-red-500' },
  { value: 'returned', label: 'مُرجعة', dot: 'bg-orange-500' },
]

const stageCounts = computed(() => {
  const c: Record<string, number> = {}
  for (const r of props.rows) c[r.status] = (c[r.status] || 0) + 1
  return c
})

const filteredRows = computed(() => {
  let list = props.rows
  if (activeStage.value !== 'all') list = list.filter(r => r.status === activeStage.value)
  if (searchText.value.trim()) {
    const q = searchText.value.trim().toLowerCase()
    list = list.filter(r =>
      String(r.id).includes(q) || (r.personnel_name || '').toLowerCase().includes(q) ||
      (r.personnel_military_number || '').includes(q) || (r.form_type_display || '').toLowerCase().includes(q))
  }
  return list
})

// منطق الصلاحيات المعتمد على stage.code (المفتاح البرمجي الثابت) بدل مقارنة النص العربي
function canApprove(req: any): boolean {
  if (req.status === 'approved' || req.status === 'rejected') return false
  if (req.status === 'draft') return false  // لم يُقدّم بعد

  // المدير العام يعتمد في أي مرحلة
  if (authStore.isAdmin) return true

  const userRole = authStore.user?.authz_profile?.role_code
    || authStore.user?.authz_profile?.role_name
    || ''

  // استخدم stage.code إذا توفر — وإلا ارجع لـ current_step_name كبديل مؤقت
  const stepCode = req.current_step_code || ''
  const stepName = req.current_step_name || ''

  // ── مطابقة بالكود أولاً (آمن) ──
  if (stepCode) {
    if (stepCode === 'services_dept' && (userRole === 'services_dept' || userRole.includes('رئيس قسم الخدمات'))) return true
    if (stepCode === 'hr_director'   && (userRole === 'hr_director'   || userRole.includes('مدير إدارة')))           return true
    if (stepCode === 'governor_general' && (userRole === 'governor_general' || userRole.includes('مدير عام')))  return true
    // أي كود آخر غير معروف: لا تسمح بالاعتماد تلقائياً
    return false
  }

  // ── فول باك: مطابقة باسم الخطوة إذا لم يتوفر الكود ──
  if (stepName.includes('رئيس قسم الخدمات') || stepName.includes('الخدمات')) {
    return userRole.includes('رئيس') || userRole.includes('الخدمات')
  }
  if (stepName.includes('مدير إدارة') || stepName.includes('القوى البشرية')) {
    return userRole.includes('مدير') || userRole.includes('القوى')
  }
  if (stepName.includes('المدير العام') || stepName.includes('المحافظة')) {
    return userRole.includes('مدير عام') || userRole.includes('المحافظة')
  }

  // إذا لا يوجد اسم خطوة محدد: الطلب قيد الإجراء ولا توجد خطوة → المدير فقط
  return authStore.isAdmin
}

function stageColor(s: string) {
  const m: Record<string, string> = {
    draft: 'bg-gray-100 text-gray-600 border-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700',
    pending_services: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/20 dark:text-amber-400 dark:border-amber-900',
    pending_hr: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/20 dark:text-blue-400 dark:border-blue-900',
    pending_director: 'bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/20 dark:text-purple-400 dark:border-purple-900',
    approved: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/20 dark:text-emerald-400 dark:border-emerald-900',
    rejected: 'bg-red-50 text-red-700 border-red-200 dark:bg-red-950/20 dark:text-red-400 dark:border-red-900',
    in_progress: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/20 dark:text-blue-400 dark:border-blue-900',
  }
  return m[s] || 'bg-gray-100 text-gray-600 border-gray-200'
}

function stageDot(s: string) {
  const m: Record<string, string> = {
    draft: 'bg-gray-400', in_progress: 'bg-blue-500', pending_services: 'bg-amber-500',
    pending_hr: 'bg-blue-500', pending_director: 'bg-purple-500', approved: 'bg-emerald-500',
    rejected: 'bg-red-500', returned: 'bg-orange-500',
  }
  return m[s] || 'bg-gray-400'
}
</script>
