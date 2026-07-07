<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="الطلبات الخارجية" />

    <div class="space-y-6 text-start" dir="rtl">
      <!-- Header -->
      <div class="relative overflow-hidden rounded-2xl border border-amber-200 dark:border-amber-900/40 bg-gradient-to-br from-amber-50 to-white dark:from-amber-950/10 dark:to-gray-900 p-6 shadow-sm">
        <div class="absolute -left-10 -top-10 w-40 h-40 bg-amber-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative flex items-center justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 rounded-xl border border-amber-200/60 dark:border-amber-800">
              <ExternalLink class="h-6 w-6" />
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">الطلبات الخارجية (الوزارية)</h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 max-w-xl">
                الطلبات السيادية والاستمارات الرسمية التي يتم طباعتها وتجميعها لرفعها للوزارة شهرياً ثم تسجيل موافقتها الرسمية.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Workflow Timeline Steps -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm">
        <h3 class="text-xs font-bold text-gray-450 dark:text-gray-500 mb-4 flex items-center gap-1.5">
          <Info class="w-4 h-4 text-amber-500" />
          خطوات سير العمل الدورة الخارجية:
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
          <div v-for="(step, idx) in workflowSteps" :key="idx" 
            class="flex items-center gap-3 p-3 rounded-xl bg-gray-50 dark:bg-gray-800/40 border border-gray-100 dark:border-gray-800/80">
            <span class="w-7 h-7 rounded-full bg-amber-500 text-white flex items-center justify-center text-xs font-black shadow-sm flex-shrink-0">
              {{ idx + 1 }}
            </span>
            <div class="text-[11px] font-bold text-gray-700 dark:text-gray-300 leading-tight">
              {{ step }}
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Filters -->
      <div class="flex flex-wrap gap-2 items-center justify-between">
        <div class="flex gap-1.5 flex-wrap">
          <button v-for="tab in tabs" :key="tab.value"
            @click="activeTab = tab.value"
            :class="activeTab === tab.value
              ? 'bg-amber-600 text-white border-amber-500 shadow-md shadow-amber-500/20'
              : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-800 hover:bg-gray-50'"
            class="px-4 py-2 text-xs font-bold rounded-xl border transition-all flex items-center gap-2 cursor-pointer">
            <component :is="tab.icon" class="w-3.5 h-3.5" />
            {{ tab.label }}
            <span class="bg-black/20 text-white text-[9px] font-black px-1.5 py-0.5 rounded-full" v-if="tabCounts[tab.value] > 0">
              {{ tabCounts[tab.value] }}
            </span>
          </button>
        </div>

        <!-- Search -->
        <div class="relative">
          <Search class="absolute right-2.5 top-2.5 h-4 w-4 text-gray-400" />
          <input v-model="searchText" type="text" placeholder="بحث بالاسم أو الرقم العسكري..."
            class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg py-2 pr-9 pl-4 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 w-64 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500" />
        </div>
      </div>

      <!-- Table / list -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-450 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-4 py-3">رقم الطلب</th>
                <th class="px-4 py-3">نوع الخدمة</th>
                <th class="px-4 py-3">الفرد</th>
                <th class="px-4 py-3">الرقم العسكري</th>
                <th class="px-4 py-3">الحالة الحالية</th>
                <th class="px-4 py-3">تاريخ التقديم</th>
                <th class="px-4 py-3 text-center w-[230px]">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr v-if="loading">
                <td colspan="7" class="px-4 py-12 text-center text-gray-400">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-600 mx-auto"></div>
                </td>
              </tr>
              <tr v-else-if="displayedRequests.length === 0">
                <td colspan="7" class="px-4 py-12 text-center text-gray-400 dark:text-gray-500">
                  لا توجد طلبات خارجية في هذا التبويب حالياً.
                </td>
              </tr>
              <tr v-for="req in displayedRequests" :key="req.id" class="hover:bg-gray-50/50 dark:hover:bg-gray-950/30">
                <td class="px-4 py-3 font-mono font-bold">
                  <template v-if="req.isCorrection">
                    <RouterLink :to="`/services/print/model-23/${req.rawId}?personnelId=${req.personnel_military_number}&old_value=${req.old_value}&new_value=${req.new_value}&reason=${req.reason}`" class="text-amber-600 hover:underline">#{{ String(req.rawId).padStart(5, '0') }}</RouterLink>
                  </template>
                  <template v-else>
                    <RouterLink :to="`/services/forms/${req.id}`" class="text-amber-600 hover:underline">#{{ String(req.id).padStart(5, '0') }}</RouterLink>
                  </template>
                </td>
                <td class="px-4 py-3 font-bold text-gray-800 dark:text-gray-200">
                  {{ req.form_type_display || req.form_type }}
                </td>
                <td class="px-4 py-3">{{ req.personnel_name || '—' }}</td>
                <td class="px-4 py-3 font-mono">{{ req.personnel_military_number || '—' }}</td>
                <td class="px-4 py-3">
                  <span :class="getStatusStyle(req)" class="inline-flex items-center gap-1.5 rounded px-2 py-0.5 text-[10px] font-bold">
                    <span :class="getStatusDot(req)" class="h-1.5 w-1.5 rounded-full"></span>
                    {{ getStatusLabel(req) }}
                  </span>
                </td>
                <td class="px-4 py-3 font-mono text-gray-450">
                  {{ req.submitted_at ? new Date(req.submitted_at).toLocaleDateString('en-GB') : '-' }}
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center justify-center gap-1.5">
                    <!-- Step 1: Print -->
                    <button v-if="req.status === 'in_progress' && !req.is_printed" @click="printRequest(req)"
                      class="bg-amber-50 hover:bg-amber-100 text-amber-700 border border-amber-200 text-[10px] font-bold px-2 py-1 rounded-lg cursor-pointer transition-all flex items-center gap-1">
                      <Printer class="w-3 h-3" />
                      طباعة
                    </button>

                    <!-- Step 2: Register Ministry Approval -->
                    <button v-if="req.status === 'in_progress' && req.is_printed" @click="registerApproval(req)"
                      class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-all flex items-center gap-1 shadow-sm shadow-emerald-500/10">
                      <FileCheck class="w-3 h-3" />
                      موافقة الوزارة
                    </button>

                    <!-- Reject -->
                    <button v-if="req.status === 'in_progress'" @click="rejectRequest(req)"
                      class="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-[10px] font-bold px-2 py-1 rounded-lg cursor-pointer transition-all">
                      رفض
                    </button>

                    <template v-if="req.isCorrection">
                      <RouterLink :to="`/services/print/model-23/${req.rawId}?personnelId=${req.personnel_military_number}&old_value=${req.old_value}&new_value=${req.new_value}&reason=${req.reason}`"
                        class="text-gray-500 hover:text-gray-700 text-[10px] font-bold hover:underline px-1">
                        عرض
                      </RouterLink>
                    </template>
                    <template v-else>
                      <RouterLink :to="`/services/forms/${req.id}`"
                        class="text-gray-500 hover:text-gray-700 text-[10px] font-bold hover:underline px-1">
                        عرض
                      </RouterLink>
                    </template>
                  </div>
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
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { ExternalLink, Search, Printer, FileCheck, Info, FileClock, CheckCircle, XCircle } from 'lucide-vue-next'
import { useServicesStore } from '@/stores/services'
import Swal from 'sweetalert2'
import api from '@/lib/api'

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
  if (req.status === 'approved') return 'bg-emerald-50 text-emerald-700 border border-emerald-250 dark:bg-emerald-950/20 dark:text-emerald-400'
  if (req.status === 'rejected') return 'bg-red-50 text-red-700 border border-red-250 dark:bg-red-950/20 dark:text-red-400'
  return req.is_printed
    ? 'bg-blue-50 text-blue-700 border border-blue-250 dark:bg-blue-950/20 dark:text-blue-400'
    : 'bg-amber-50 text-amber-700 border border-amber-250 dark:bg-amber-950/20 dark:text-amber-400'
}

function getStatusDot(req: any) {
  if (req.status === 'approved') return 'bg-emerald-500'
  if (req.status === 'rejected') return 'bg-red-500'
  return req.is_printed ? 'bg-blue-500' : 'bg-amber-500'
}
</script>
