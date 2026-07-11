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
      actions-width="220px"
      :current-page="1"
      :total-pages="1"
      :total-count="filteredRows.length"
      :page-size="filteredRows.length || 50"
      search-placeholder="بحث بالاسم أو رقم الطلب..."
      empty-title="لا توجد طلبات خارجية"
      empty-description="لا توجد طلبات خارجية بهذه المعايير."
      @search="searchText = $event"
      @refresh="$emit('refresh')"
    >
      <template #cell-id="{ row }">
        <RouterLink :to="row.isCorrection ? '#' : `/services/forms/${row.id}`" class="text-brand-600 hover:underline font-mono font-bold">
          #{{ String(row.isCorrection ? row.rawId : row.id).padStart(5, '0') }}
        </RouterLink>
      </template>

      <template #cell-form_type_display="{ row }">
        <span class="font-bold text-gray-800 dark:text-gray-200">{{ row.form_type_display || row.form_type }}</span>
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
          {{ stageLabels[row.status] || row.status }}
        </span>
      </template>

      <template #cell-submitted_at="{ row }">
        <span class="font-mono text-gray-450 text-[11px]">{{ row.submitted_at ? new Date(row.submitted_at).toLocaleDateString('en-GB') : '—' }}</span>
      </template>
      
      <template #cell-is_printed="{ row }">
        <span v-if="row.is_printed" class="text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 px-2 py-0.5 rounded text-[10px] font-bold border border-emerald-100 dark:border-emerald-900">
          تمت الطباعة
        </span>
        <span v-else class="text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded text-[10px] font-bold border border-gray-200 dark:border-gray-700">
          لم يطبع
        </span>
      </template>

      <template #actions="{ row }">
        <button v-if="canPrint(row)" @click="$emit('print', row)"
          class="bg-blue-50 hover:bg-blue-100 text-blue-600 border border-blue-200 text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
          طباعة
        </button>
        <button v-if="canRegisterApproval(row)" @click="$emit('register-approval', row)"
          class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm">
          موافقة الوزارة
        </button>
        <button v-if="canReject(row)" @click="$emit('reject', row)"
          class="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors">
          رفض
        </button>
        <RouterLink :to="`/services/forms/${row.id}`" v-if="!row.isCorrection"
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
defineEmits<{ (e: 'print', req: any): void; (e: 'register-approval', req: any): void; (e: 'reject', req: any): void; (e: 'refresh'): void }>()

const authStore = useAuthStore()
const activeStage = ref('all')
const searchText = ref('')

const stageLabels: Record<string, string> = {
  all: 'الكل', in_progress: 'معلق بالوزارة', approved: 'معتمد (تمت الموافقة)',
  rejected: 'مرفوض', pending: 'قيد الانتظار'
}

const columns = [
  { key: 'id', label: 'رقم الطلب', minWidth: '100px' },
  { key: 'form_type_display', label: 'نوع الخدمة', minWidth: '140px' },
  { key: 'personnel_name', label: 'الفرد', minWidth: '160px' },
  { key: 'personnel_military_number', label: 'الرقم العسكري', minWidth: '120px' },
  { key: 'status', label: 'المرحلة الحالية', minWidth: '130px' },
  { key: 'is_printed', label: 'حالة الطباعة', minWidth: '100px' },
  { key: 'submitted_at', label: 'تاريخ التقديم', minWidth: '110px' },
]

const stageOptions = [
  { value: 'all', label: 'الكل', dot: 'bg-gray-400' },
  { value: 'in_progress', label: 'معلق بالوزارة', dot: 'bg-amber-500' },
  { value: 'approved', label: 'معتمدة', dot: 'bg-emerald-500' },
  { value: 'rejected', label: 'مرفوضة', dot: 'bg-red-500' },
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

function canPrint(req: any) {
  if (req.status === 'approved' || req.status === 'rejected') return false
  return authStore.isAdmin || authStore.user?.authz_profile?.role_name?.includes('سكرتارية')
}

function canRegisterApproval(req: any) {
  if (req.status === 'approved' || req.status === 'rejected') return false
  return req.is_printed && (authStore.isAdmin || authStore.user?.authz_profile?.role_name?.includes('سكرتارية'))
}

function canReject(req: any) {
  if (req.status === 'approved' || req.status === 'rejected') return false
  return authStore.isAdmin || authStore.user?.authz_profile?.role_name?.includes('سكرتارية')
}

function stageColor(s: string) {
  const m: Record<string, string> = {
    in_progress: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/20 dark:text-amber-400 dark:border-amber-900',
    pending: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/20 dark:text-blue-400 dark:border-blue-900',
    approved: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/20 dark:text-emerald-400 dark:border-emerald-900',
    rejected: 'bg-red-50 text-red-700 border-red-200 dark:bg-red-950/20 dark:text-red-400 dark:border-red-900',
  }
  return m[s] || 'bg-gray-100 text-gray-600 border-gray-200'
}

function stageDot(s: string) {
  const m: Record<string, string> = {
    in_progress: 'bg-amber-500', pending: 'bg-blue-500', approved: 'bg-emerald-500', rejected: 'bg-red-500',
  }
  return m[s] || 'bg-gray-400'
}
</script>
