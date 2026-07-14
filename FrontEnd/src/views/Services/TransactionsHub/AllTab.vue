<template>
  <div class="space-y-4">
    <!-- Status Filters -->
    <div class="flex flex-wrap gap-2">
      <button v-for="f in statusFilters" :key="f.value" @click="$emit('filter-status', f.value)"
        :class="currentStatus === f.value ? 'bg-brand-600 text-white border-brand-500' : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800'"
        class="px-3 py-2 text-xs font-bold rounded-xl border transition-all cursor-pointer flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full" :class="f.dot"></span>
        {{ f.label }}
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
      empty-title="لا توجد طلبات"
      empty-description="لا توجد طلبات بهذه الحالة حالياً."
      @search="onSearch"
      @refresh="$emit('refresh')"
    >
      <template #cell-id="{ row }">
        <RouterLink :to="`/services/forms/${row.isCorrection ? row.rawId : row.id}`" class="text-brand-600 hover:underline font-mono font-bold">
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

      <template #cell-status="{ row }">
        <!-- مسودة: مؤشر بياني خاص -->
        <div v-if="row.status === 'draft'" class="flex items-center gap-2">
          <span class="inline-flex items-center gap-1 bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 text-[10px] font-bold px-2 py-0.5 rounded border border-gray-200 dark:border-gray-700">
            <span class="w-1.5 h-1.5 rounded-full bg-gray-400"></span>
            مسودة — بانتظار التقديم
          </span>
        </div>
        <!-- in_progress: شريط المراحل -->
        <div v-else-if="row.status === 'in_progress' && row.all_steps && row.all_steps.length > 0" class="w-full min-w-[160px]">
          <div class="flex items-center gap-1 mb-1.5 justify-between">
            <span class="text-[10px] font-bold text-gray-700 dark:text-gray-300">
              مرحلة {{ row.current_step_index + 1 }} / {{ row.all_steps.length }}
            </span>
            <span class="text-[9px] text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-400 px-1.5 py-0.5 rounded font-bold">
              {{ row.current_step_name }}
            </span>
          </div>
          <div class="flex items-center gap-1 w-full">
            <div v-for="(step, idx) in row.all_steps" :key="idx"
              class="h-1.5 flex-1 rounded-full transition-colors duration-300"
              :class="[
                idx < row.current_step_index ? 'bg-emerald-500' :
                idx === row.current_step_index ? 'bg-blue-500 animate-pulse' : 'bg-gray-200 dark:bg-gray-700'
              ]"></div>
          </div>
        </div>
        <!-- غير ذلك -->
        <span v-else :class="getStatusColor(row.status)" class="inline-flex items-center gap-1 rounded px-2 py-0.5 text-[10px] font-bold">
          <span :class="getStatusDot(row.status)" class="h-1.5 w-1.5 rounded-full"></span>
          {{ getStatusLabel(row.status) }}
        </span>
      </template>

      <template #cell-created_at="{ row }">
        <span class="font-mono text-gray-450 text-xs">{{ formatDate(row.created_at || row.submitted_at) }}</span>
      </template>

      <template #cell-updated_at="{ row }">
        <span class="font-mono text-gray-450 text-xs">{{ formatDate(row.updated_at) }}</span>
      </template>

      <template #actions="{ row }">
        <!-- زر تقديم المسودة -->
        <button v-if="row.status === 'draft'" @click="$emit('submit-draft', row)"
          class="bg-blue-600 hover:bg-blue-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg>
          تقديم
        </button>
        <!-- اعتماد/رفض في_progress -->
        <button v-if="row.status === 'in_progress'" @click="$emit('approve', row)"
          class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm">
          اعتماد
        </button>
        <button v-if="row.status === 'in_progress'" @click="$emit('reject', row)"
          class="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors">
          رفض
        </button>
        <RouterLink :to="`/services/forms/${row.isCorrection ? row.rawId : row.id}`"
          class="text-brand-600 hover:text-brand-700 text-[10px] font-bold hover:underline px-1">
          التفاصيل
        </RouterLink>
      </template>
    </DataTable>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import DataTable from '@/components/tables/DataTable.vue'

const props = defineProps<{
  rows: any[]
  loading: boolean
  currentStatus: string
}>()

defineEmits<{
  (e: 'filter-status', v: string): void
  (e: 'approve', req: any): void
  (e: 'reject', req: any): void
  (e: 'submit-draft', req: any): void
  (e: 'refresh'): void
}>()

const searchQuery = ref('')

const columns = [
  { key: 'id', label: 'رقم الطلب', minWidth: '100px' },
  { key: 'form_type_display', label: 'نوع الخدمة', minWidth: '140px' },
  { key: 'personnel_name', label: 'مقدم الطلب', minWidth: '160px' },
  { key: 'status', label: 'الحالة', minWidth: '180px' },
  { key: 'created_at', label: 'تاريخ الإنشاء', minWidth: '110px' },
  { key: 'updated_at', label: 'آخر تحديث', minWidth: '110px' },
]

const statusFilters = [
  { value: 'all', label: 'الكل', dot: 'bg-gray-400' },
  { value: 'draft', label: 'مسودة', dot: 'bg-gray-400' },
  { value: 'in_progress', label: 'قيد الانتظار', dot: 'bg-blue-500' },
  { value: 'approved', label: 'تمت الموافقة', dot: 'bg-emerald-500' },
  { value: 'executing', label: 'قيد التنفيذ', dot: 'bg-indigo-500' },
  { value: 'completed', label: 'مكتمل', dot: 'bg-teal-500' },
  { value: 'rejected', label: 'مرفوض', dot: 'bg-red-500' },
]

const filteredRows = computed(() => {
  let list = props.rows
  if (props.currentStatus !== 'all') list = list.filter(r => r.status === props.currentStatus)
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter(r =>
      String(r.id).includes(q) || (r.personnel_name || '').toLowerCase().includes(q) ||
      (r.form_type_display || '').toLowerCase().includes(q))
  }
  return list
})

function onSearch(q: string) { searchQuery.value = q }

function formatDate(d: string) { return d ? new Date(d).toLocaleDateString('en-GB') : '-' }

function getStatusLabel(s: string) {
  const m: any = {
    draft: 'مسودة',
    in_progress: 'قيد الإجراء',
    approved: 'معتمد نهائياً',
    executing: 'قيد التنفيذ',
    completed: 'مكتمل',
    rejected: 'مرفوض',
    cancelled: 'ملغى',
    returned: 'مُرجع للتعديل',
    // الحالات القديمة — للتوافق مع البيانات الموجودة في DB
    pending_services: 'عند رئيس قسم الخدمات',
    pending_hr: 'عند مدير إدارة القوى البشرية',
    pending_director: 'عند المدير العام للمحافظة',
  }
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
    pending_services: 'bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400',
    pending_hr: 'bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400',
    pending_director: 'bg-purple-50 text-purple-700 dark:bg-purple-950/20 dark:text-purple-400',
  }
  return c[s] || 'bg-gray-100 text-gray-600'
}

function getStatusDot(s: string) {
  const d: any = { draft: 'bg-gray-400', in_progress: 'bg-blue-500', approved: 'bg-emerald-500', executing: 'bg-indigo-500', completed: 'bg-teal-500', rejected: 'bg-red-500', pending_services: 'bg-amber-500', pending_hr: 'bg-blue-500', pending_director: 'bg-purple-500' }
  return d[s] || 'bg-gray-400'
}
</script>
