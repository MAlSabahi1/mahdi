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
      selectable
      v-model:selectedRowKeys="selectedIds"
      @search="searchText = $event"
      @refresh="$emit('refresh')"
    >
      <template #toolbar-actions>
        <div v-if="selectedIds.length > 0" class="flex gap-2">
          <!-- Bulk Print Corrections -->
          <button @click="handleBulkPrint"
            class="bg-brand-600 hover:bg-brand-700 text-white text-[11px] font-bold px-4 py-2 rounded-lg cursor-pointer shadow-sm flex items-center gap-1.5 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
            خيارات الطباعة للطلبات المحددة ({{ selectedIds.length }})
          </button>
          <!-- Bulk Register Approval -->
          <button @click="handleBulkRegisterApproval"
            class="bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold px-4 py-2 rounded-lg cursor-pointer shadow-sm flex items-center gap-1.5 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
            رفع الموافقة للطلبات المحددة ({{ selectedIds.length }})
          </button>
        </div>
      </template>
      <template #cell-id="{ row }">
        <RouterLink :to="row.isCorrection ? '#' : `/services/forms/${row.id}`" class="text-brand-600 hover:underline font-mono font-bold">
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
          {{ stageLabels[row.status] || row.status }}
        </span>
      </template>

      <template #cell-submitted_at="{ row }">
        <span class="font-mono text-gray-450 text-[11px]">{{ row.submitted_at ? new Date(row.submitted_at).toLocaleDateString('en-GB') : '—' }}</span>
      </template>
      
      <template #cell-is_printed="{ row }">
        <div class="flex flex-col gap-1">
          <!-- الخطوة 1: الطباعة -->
          <span class="flex items-center gap-1.5 text-[10px] font-bold"
            :class="row.is_printed ? 'text-emerald-600' : 'text-gray-400'">
            <span class="flex items-center justify-center w-3.5 h-3.5 rounded-full border text-white"
              :class="row.is_printed ? 'bg-emerald-500 border-emerald-500' : 'border-gray-300'">
              <svg v-if="row.is_printed" class="w-2 h-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
            </span>
            {{ row.is_printed ? 'تمت الطباعة' : 'لم يطبع بعد' }}
          </span>
          <!-- الخطوة 2: مرفق الوزارة -->
          <span class="flex items-center gap-1.5 text-[10px] font-bold"
            :class="row.ministry_approval_doc_id ? 'text-emerald-600' : (row.is_printed ? 'text-amber-600' : 'text-gray-300')">
            <span class="flex items-center justify-center w-3.5 h-3.5 rounded-full border text-white"
              :class="row.ministry_approval_doc_id ? 'bg-emerald-500 border-emerald-500' : (row.is_printed ? 'border-amber-400' : 'border-gray-300')">
              <svg v-if="row.ministry_approval_doc_id" class="w-2 h-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
            </span>
            {{ row.ministry_approval_doc_id ? 'مرفق الوزارة ✓' : 'بانتظار مرفق الوزارة' }}
          </span>
          <!-- الخطوة 3: الاعتماد النهائي -->
          <span class="flex items-center gap-1.5 text-[10px] font-bold"
            :class="row.status === 'approved' ? 'text-emerald-600' : 'text-gray-300'">
            <span class="flex items-center justify-center w-3.5 h-3.5 rounded-full border text-white"
              :class="row.status === 'approved' ? 'bg-emerald-500 border-emerald-500' : 'border-gray-300'">
              <svg v-if="row.status === 'approved'" class="w-2 h-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
            </span>
            {{ row.status === 'approved' ? 'معتمد نهائياً' : 'الاعتماد النهائي' }}
          </span>
        </div>
      </template>

      <template #actions="{ row }">
        <!-- زر الطباعة — متاح دائماً قبل الاعتماد النهائي -->
        <button v-if="canPrint(row)" @click="$emit('print', row)"
          class="bg-blue-50 hover:bg-blue-100 text-blue-600 border border-blue-200 text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
          {{ row.is_printed ? 'إعادة طباعة' : 'طباعة' }}
        </button>
        <!-- رفع مرفق الوزارة — فقط بعد الطباعة وقبل الاعتماد -->
        <button v-if="canRegisterApproval(row)" @click="$emit('register-approval', row)"
          class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors shadow-sm flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
          رفع موافقة الوزارة
        </button>
        <!-- تنبيه: يجب طباعة أولاً -->
        <span v-if="!row.is_printed && row.status === 'in_progress'"
          class="text-[9px] text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded font-bold">
          ⚠️ اطبع أولاً
        </span>
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
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/auth'
import DataTable from '@/components/tables/DataTable.vue'
import api from '@/lib/api'
import { useRouter } from 'vue-router'

const props = defineProps<{ rows: any[]; loading: boolean }>()
const emit = defineEmits<{ (e: 'print', req: any): void; (e: 'register-approval', req: any): void; (e: 'bulk-register-approval', req: any[]): void; (e: 'reject', req: any): void; (e: 'refresh'): void }>()

const router = useRouter()
const authStore = useAuthStore()
const activeStage = ref('all')
const searchText = ref('')
const selectedIds = ref<(string | number)[]>([])

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

// === Bulk Actions ===

function handleBulkPrint() {
  if (!selectedIds.value.length) return
  
  const selectedRows = props.rows.filter(r => selectedIds.value.includes(r.id) && r.isCorrection)
  if (!selectedRows.length) return
  
  const rawIds = selectedRows.map(r => r.rawId).join(',')
  router.push(`/services/corrections/${rawIds}/print`)
}

function handleBulkRegisterApproval() {
  if (!selectedIds.value.length) return
  
  const selectedRows = props.rows.filter(r => selectedIds.value.includes(r.id))
  if (!selectedRows.length) return
  
  // التحقق من أن جميع الطلبات جاهزة للاعتماد
  const unreadyRows = selectedRows.filter(r => !canRegisterApproval(r))
  if (unreadyRows.length > 0) {
    Swal.fire({
      icon: 'warning',
      title: 'طلبات غير جاهزة',
      text: `هناك ${unreadyRows.length} طلبات محددة غير جاهزة للاعتماد (إما أنها غير مطبوعة أو تم البت فيها مسبقاً). يرجى تحديد الطلبات الجاهزة فقط.`
    })
    return
  }

  emit('bulk-register-approval', selectedRows)
}
</script>
