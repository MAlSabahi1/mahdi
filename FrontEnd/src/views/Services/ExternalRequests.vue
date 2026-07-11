<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="الطلبات الخارجية" />

    <div class="space-y-6 text-start" dir="rtl">

      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-warning-50 dark:bg-warning-500/10 rounded-xl text-warning-600 dark:text-warning-400">
              <ExternalLink class="h-6 w-6" />
            </div>
            الطلبات الخارجية (الوزارية)
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            الطلبات السيادية والاستمارات الرسمية التي يتم طباعتها وتجميعها لرفعها للوزارة شهرياً ثم تسجيل موافقتها الرسمية.
          </p>
        </div>

        <!-- Live Counters -->
        <div class="flex gap-4 flex-shrink-0 flex-wrap">
          <div v-for="stat in headerStats" :key="stat.label" class="rounded-2xl border p-4 shadow-theme-xs text-center min-w-[110px]"
            :class="stat.borderClass">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full" :class="stat.iconClass">
                <component :is="stat.icon" class="h-5 w-5" />
              </div>
              <div class="text-start">
                <p class="text-xs font-medium" :class="stat.labelClass">{{ stat.label }}</p>
                <h3 class="text-xl font-bold" :class="stat.valueClass">{{ stat.value }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Workflow Timeline Steps -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-4 dark:border-gray-800 dark:bg-gray-800/40 flex items-center gap-3">
          <Info class="w-4.5 h-4.5 text-warning-500" />
          <span class="text-xs font-bold text-gray-700 dark:text-gray-300">خطوات سير العمل للدورة الخارجية:</span>
        </div>
        <div class="p-5">
          <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
            <div v-for="(step, idx) in workflowSteps" :key="idx" 
              class="flex items-center gap-3 p-3 rounded-xl bg-gray-50 dark:bg-gray-800/40 border border-gray-100 dark:border-gray-800">
              <span class="w-8 h-8 rounded-lg bg-warning-500 text-white flex items-center justify-center text-xs font-bold shadow-sm flex-shrink-0">
                {{ idx + 1 }}
              </span>
              <div class="text-[11px] font-bold text-gray-700 dark:text-gray-300 leading-tight">
                {{ step }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <DataTable
        :columns="columns"
        :data="displayedRequests"
        rowKey="id"
        :loading="loading"
        searchPlaceholder="بحث بالاسم أو الرقم العسكري..."
        @search="val => searchText = val"
        @refresh="fetchRequests"
        emptyTitle="لا توجد طلبات خارجية"
        emptyDescription="لا توجد طلبات خارجية في هذا التبويب حالياً"
        actionsWidth="230px"
      >
        <!-- Toolbar Actions: Tabs -->
        <template #toolbar-actions>
          <div class="flex gap-1.5 flex-wrap">
            <button v-for="tab in tabs" :key="tab.value"
              @click="activeTab = tab.value"
              :class="activeTab === tab.value
                ? 'bg-warning-600 text-white border-warning-500 shadow-md shadow-warning-500/20'
                : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700'"
              class="px-4 py-2.5 text-xs font-bold rounded-lg border transition-all flex items-center gap-2 cursor-pointer">
              <component :is="tab.icon" class="w-3.5 h-3.5" />
              {{ tab.label }}
              <span v-if="tabCounts[tab.value] > 0"
                :class="activeTab === tab.value ? 'bg-white/20 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'"
                class="text-[9px] font-bold px-1.5 py-0.5 rounded-md">
                {{ tabCounts[tab.value] }}
              </span>
            </button>
          </div>
        </template>

        <template #cell-id="{ row }">
          <template v-if="row.isCorrection">
            <RouterLink :to="`/services/print/model-23/${row.rawId}?personnelId=${row.personnel_military_number}&old_value=${row.old_value}&new_value=${row.new_value}&reason=${row.reason}`" class="text-warning-600 hover:underline font-mono font-bold">#{{ String(row.rawId).padStart(5, '0') }}</RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="`/services/forms/${row.id}`" class="text-warning-600 hover:underline font-mono font-bold">#{{ String(row.id).padStart(5, '0') }}</RouterLink>
          </template>
        </template>

        <template #cell-service_type="{ row }">
          <span class="font-bold text-gray-800 dark:text-gray-200">{{ row.form_type_display || row.form_type }}</span>
        </template>

        <template #cell-personnel="{ row }">
          <span class="text-gray-600 dark:text-gray-300">{{ row.personnel_name || '—' }}</span>
        </template>

        <template #cell-military_number="{ row }">
          <span class="font-mono text-gray-500 dark:text-gray-400">{{ row.personnel_military_number || '—' }}</span>
        </template>

        <template #cell-status="{ row }">
          <span :class="getStatusStyle(row)" class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[10px] font-bold border">
            <span :class="getStatusDot(row)" class="h-1.5 w-1.5 rounded-full"></span>
            {{ getStatusLabel(row) }}
          </span>
        </template>

        <template #cell-date="{ row }">
          <span class="font-mono text-gray-500 dark:text-gray-400 text-[11px]">{{ row.submitted_at ? new Date(row.submitted_at).toLocaleDateString('en-GB') : '-' }}</span>
        </template>

        <template #actions="{ row }">
          <button v-if="row.status === 'in_progress' && !row.is_printed" @click="printRequest(row)"
            class="bg-warning-50 hover:bg-warning-100 text-warning-700 border border-warning-200 dark:bg-warning-500/10 dark:text-warning-400 dark:border-warning-500/20 text-[10px] font-bold px-2.5 py-1.5 rounded-lg cursor-pointer transition-all flex items-center gap-1">
            <Printer class="w-3 h-3" />
            طباعة
          </button>

          <button v-if="row.status === 'in_progress' && row.is_printed" @click="registerApproval(row)"
            class="bg-success-600 hover:bg-success-700 text-white text-[10px] font-bold px-2.5 py-1.5 rounded-lg cursor-pointer transition-all flex items-center gap-1 shadow-sm">
            <FileCheck class="w-3 h-3" />
            موافقة الوزارة
          </button>

          <button v-if="row.status === 'in_progress'" @click="rejectRequest(row)"
            class="bg-error-50 hover:bg-error-100 text-error-600 border border-error-200 dark:bg-error-500/10 dark:text-error-400 dark:border-error-500/20 text-[10px] font-bold px-2.5 py-1.5 rounded-lg cursor-pointer transition-all">
            رفض
          </button>

          <template v-if="row.isCorrection">
            <RouterLink :to="`/services/print/model-23/${row.rawId}?personnelId=${row.personnel_military_number}&old_value=${row.old_value}&new_value=${row.new_value}&reason=${row.reason}`"
              class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-[10px] font-bold hover:underline px-1">
              عرض
            </RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="`/services/forms/${row.id}`"
              class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-[10px] font-bold hover:underline px-1">
              عرض
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
import { ExternalLink, Search, Printer, FileCheck, Info, FileClock, CheckCircle, XCircle } from 'lucide-vue-next'
import { useServicesStore } from '@/stores/services'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const columns = [
  { key: 'id', label: 'رقم الطلب' },
  { key: 'service_type', label: 'نوع الخدمة' },
  { key: 'personnel', label: 'الفرد' },
  { key: 'military_number', label: 'الرقم العسكري' },
  { key: 'status', label: 'الحالة الحالية' },
  { key: 'date', label: 'تاريخ التقديم' },
]

const servicesStore = useServicesStore()
const allRequests = ref<any[]>([])
const activeTab = ref('needs_print')
const searchText = ref('')
const loading = ref(false)

const workflowSteps = [
  'تقديم الطلب بالنظام',
  'طباعة الاستمارة الرسمية',
  'الرفع للوزارة بالدورة الشهرية',
  'موافقة / قرار الوزارة',
  'تسجيل المذكرة والاعتماد النهائي'
]

const tabs = [
  { value: 'needs_print', label: 'بحاجة لطباعة', icon: Printer },
  { value: 'pending_ministry', label: 'بانتظار الوزارة', icon: FileClock },
  { value: 'approved', label: 'معتمدة نهائياً', icon: CheckCircle },
  { value: 'rejected', label: 'مرفوضة', icon: XCircle }
]

// Tab Counts
const tabCounts = computed<Record<string, number>>(() => {
  return {
    needs_print: allRequests.value.filter(r => r.status === 'in_progress' && !r.is_printed).length,
    pending_ministry: allRequests.value.filter(r => r.status === 'in_progress' && r.is_printed).length,
    approved: allRequests.value.filter(r => r.status === 'approved').length,
    rejected: allRequests.value.filter(r => r.status === 'rejected').length
  }
})

// Header Stats
const headerStats = computed(() => [
  {
    label: 'بحاجة لطباعة', value: tabCounts.value.needs_print, icon: Printer,
    borderClass: 'border-warning-200 bg-warning-50 dark:border-warning-500/20 dark:bg-warning-500/5',
    iconClass: 'bg-warning-100 text-warning-600 dark:bg-warning-500/20 dark:text-warning-400',
    labelClass: 'text-warning-700 dark:text-warning-400',
    valueClass: 'text-warning-900 dark:text-warning-300',
  },
  {
    label: 'بانتظار الوزارة', value: tabCounts.value.pending_ministry, icon: FileClock,
    borderClass: 'border-blue-200 bg-blue-50 dark:border-blue-500/20 dark:bg-blue-500/5',
    iconClass: 'bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400',
    labelClass: 'text-blue-700 dark:text-blue-400',
    valueClass: 'text-blue-900 dark:text-blue-300',
  },
  {
    label: 'معتمدة', value: tabCounts.value.approved, icon: CheckCircle,
    borderClass: 'border-success-200 bg-success-50 dark:border-success-500/20 dark:bg-success-500/5',
    iconClass: 'bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400',
    labelClass: 'text-success-700 dark:text-success-400',
    valueClass: 'text-success-900 dark:text-success-300',
  },
])

// Filtered Requests
const displayedRequests = computed(() => {
  let list = allRequests.value

  // Status/Printed Tabs Filter
  if (activeTab.value === 'needs_print') {
    list = list.filter(r => r.status === 'in_progress' && !r.is_printed)
  } else if (activeTab.value === 'pending_ministry') {
    list = list.filter(r => r.status === 'in_progress' && r.is_printed)
  } else if (activeTab.value === 'approved') {
    list = list.filter(r => r.status === 'approved')
  } else if (activeTab.value === 'rejected') {
    list = list.filter(r => r.status === 'rejected')
  }

  // Search Filter
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

onMounted(async () => {
  await fetchRequests()
})

async function fetchRequests() {
  loading.value = true
  try {
    const formsRes = await servicesStore.fetchForms({ approval_type: 'external' })
    const formsList = (formsRes?.results || formsRes || []).map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || ''
    }))
    
    const correctionsRes = await api.get('/personnel/corrections/?type=name_correction')
    const correctionsList = (correctionsRes.data?.results || correctionsRes.data || []).map((c: any) => ({
      id: `corr-${c.id}`,
      rawId: c.id,
      isCorrection: true,
      form_type: c.correction_type,
      form_type_display: 'طلب تصحيح الاسم (نموذج 23)',
      personnel_name: c.personnel_name,
      personnel_military_number: c.personnel_military_number,
      status: c.status === 'pending' ? 'in_progress' : c.status,
      status_display: c.status_display,
      submitted_at: c.requested_at,
      is_printed: c.is_printed,
      old_value: c.old_value,
      new_value: c.new_value,
      notes: c.notes,
      reason: c.notes || 'تصحيح الاسم بالكامل في السجلات العسكرية.'
    }))
    
    allRequests.value = [...formsList, ...correctionsList]
  } catch (e) {
    console.error('Failed to fetch external requests', e)
  } finally {
    loading.value = false
  }
}

async function printRequest(req: any) {
  try {
    if (req.isCorrection) {
      await api.post(`/personnel/corrections/${req.rawId}/mark_printed/`)
      req.is_printed = true
      window.open(`/services/print/model-23/${req.rawId}?personnelId=${req.personnel_military_number}&old_value=${req.old_value}&new_value=${req.new_value}&reason=${req.reason}`, '_blank')
    } else {
      await servicesStore.markFormPrinted(req.id)
      req.is_printed = true
      window.open(`/services/forms/${req.id}?print=true`, '_blank')
    }
    await fetchRequests() // Refresh state
  } catch (e: any) {
    Swal.fire('خطأ', e.response?.data?.error || 'حدث خطأ أثناء طباعة الطلب', 'error')
  }
}

async function registerApproval(req: any) {
  const result = await Swal.fire({
    title: 'تسجيل موافقة الوزارة والاعتماد',
    html: `
      <div class="text-right" dir="rtl">
        <p class="text-xs text-gray-600 mb-3">يجب إرفاق ملف القرار/المذكرة الوزارية الرسمي الوارد من الوزارة لإكمال الاعتماد.</p>
        <input type="file" id="ministry-doc" class="block w-full text-xs text-gray-500 file:ml-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100" accept=".pdf,.png,.jpg,.jpeg">
      </div>
    `,
    icon: 'info',
    showCancelButton: true,
    confirmButtonText: 'رفع واعتماد الطلب',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      const fileInput = document.getElementById('ministry-doc') as HTMLInputElement
      if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        Swal.showValidationMessage('يجب اختيار ملف المذكرة/القرار أولاً')
        return false
      }
      const file = fileInput.files[0]
      const fd = new FormData()
      fd.append('file', file)
      fd.append('document_type', 'ministry_approval')

      try {
        const uploadRes = await api.post('/storage/upload/', fd, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        const docId = uploadRes.data?.data?.id || uploadRes.data?.id
        if (!docId) throw new Error('فشل الحصول على معرّف المستند المرفوع')

        if (req.isCorrection) {
          await api.post(`/personnel/corrections/${req.rawId}/approve/`, { approval_document_id: docId })
        } else {
          await servicesStore.approveForm(req.id, { ministry_document_id: docId })
        }
        return true
      } catch (e: any) {
        Swal.showValidationMessage(e.response?.data?.error || 'حدث خطأ أثناء الرفع أو اعتماد الطلب')
        return false
      }
    }
  })

  if (result.isConfirmed) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تسجيل موافقة الوزارة واعتماد الطلب', showConfirmButton: false, timer: 2500 })
    await fetchRequests()
  }
}

async function rejectRequest(req: any) {
  const result = await Swal.fire({
    title: 'رفض الطلب',
    input: 'text',
    inputPlaceholder: 'سبب الرفض الموجه من الوزارة...',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444',
    inputValidator: (value) => !value ? 'يجب كتابة سبب الرفض' : undefined
  })

  if (result.isConfirmed && result.value) {
    try {
      if (req.isCorrection) {
        await api.post(`/personnel/corrections/${req.rawId}/reject/`, { reason: result.value })
      } else {
        await servicesStore.rejectForm(req.id, result.value)
      }
      Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم تسجيل رفض الطلب', showConfirmButton: false, timer: 2000 })
      await fetchRequests()
    } catch (e: any) {
      Swal.fire('خطأ', e.response?.data?.error || 'حدث خطأ أثناء الرفض', 'error')
    }
  }
}

function getStatusLabel(req: any) {
  if (req.status === 'approved') return 'معتمد نهائياً'
  if (req.status === 'rejected') return 'مرفوض'
  return req.is_printed ? 'بانتظار الوزارة (مطبوع)' : 'بانتظار الطباعة'
}

function getStatusStyle(req: any) {
  if (req.status === 'approved') return 'bg-success-50 text-success-700 border-success-200 dark:bg-success-500/10 dark:text-success-400 dark:border-success-500/20'
  if (req.status === 'rejected') return 'bg-error-50 text-error-700 border-error-200 dark:bg-error-500/10 dark:text-error-400 dark:border-error-500/20'
  return req.is_printed
    ? 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20'
    : 'bg-warning-50 text-warning-700 border-warning-200 dark:bg-warning-500/10 dark:text-warning-400 dark:border-warning-500/20'
}

function getStatusDot(req: any) {
  if (req.status === 'approved') return 'bg-success-500'
  if (req.status === 'rejected') return 'bg-error-500'
  return req.is_printed ? 'bg-blue-500' : 'bg-warning-500'
}
</script>
