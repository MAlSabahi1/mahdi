<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="مركز المعاملات والمتابعة" />

    <div class="space-y-6 text-start" dir="rtl">

      <!-- Header -->
      <div class="relative overflow-hidden rounded-2xl border border-brand-200 dark:border-brand-900/40 bg-gradient-to-br from-brand-50 to-white dark:from-brand-950/10 dark:to-gray-900 p-6 shadow-sm">
        <div class="absolute -left-10 -top-10 w-40 h-40 bg-brand-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative flex items-center justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-brand-100 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 rounded-xl border border-brand-200/60 dark:border-brand-800">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">مركز المعاملات والمتابعة الموحد</h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">تقديم ومتابعة واعتماد جميع المعاملات والطلبات من مكان واحد.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-2 lg:grid-cols-5 gap-3">
        <div v-for="stat in stats" :key="stat.label"
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 shadow-sm">
          <p class="text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">{{ stat.label }}</p>
          <div class="flex items-center justify-between">
            <p class="text-lg font-black text-gray-900 dark:text-white font-mono">{{ stat.value }}</p>
            <span :class="stat.dot" class="h-2.5 w-2.5 rounded-full"></span>
          </div>
        </div>
      </div>

      <!-- Main Tabs -->
      <div class="flex gap-1.5 flex-wrap border-b border-gray-200 dark:border-gray-800 pb-0">
        <button v-for="tab in mainTabs" :key="tab.value" @click="setTab(tab.value)"
          :class="activeTab === tab.value
            ? 'text-brand-600 border-b-2 border-brand-600 dark:text-brand-400 dark:border-brand-400 bg-brand-50/50 dark:bg-brand-950/10'
            : 'text-gray-500 dark:text-gray-400 border-b-2 border-transparent hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800/50'"
          class="px-5 py-3 text-sm font-bold transition-all flex items-center gap-2 cursor-pointer rounded-t-lg">
          <component :is="tab.icon" class="w-4 h-4" />
          {{ tab.label }}
          <span v-if="tab.count > 0" class="bg-brand-100 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 text-[10px] font-black px-1.5 py-0.5 rounded-full">{{ tab.count }}</span>
        </button>
      </div>

      <!-- Tab Content -->
      <AllTab v-if="activeTab === 'all'" :rows="allRequests" :loading="loading" :currentStatus="filterStatus"
        @filter-status="filterStatus = $event" @approve="handleApprove" @reject="handleReject" />

      <InternalTab v-else-if="activeTab === 'internal'" :rows="internalRequests" :loading="loading"
        @approve="handleApproveInternal" @reject="handleRejectInternal" />

      <ExternalTab v-else-if="activeTab === 'external'" :rows="externalRequests" :loading="loading"
        @print="handlePrint" @register-approval="handleRegisterApproval" @reject="handleRejectExternal" />

      <TrackingTab v-else-if="activeTab === 'tracking'" :rows="allFormsRaw" :loading="loading" />
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { Inbox, Building2, Globe, GitBranch } from 'lucide-vue-next'
import { useServicesStore } from '@/stores/services'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'
import api from '@/lib/api'

import AllTab from './TransactionsHub/AllTab.vue'
import InternalTab from './TransactionsHub/InternalTab.vue'
import ExternalTab from './TransactionsHub/ExternalTab.vue'
import TrackingTab from './TransactionsHub/TrackingTab.vue'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()
const authStore = useAuthStore()

const activeTab = ref((route.query.tab as string) || 'all')
const filterStatus = ref('all')
const loading = ref(false)

const allFormsRaw = ref<any[]>([])
const allRequests = ref<any[]>([])
const internalRequests = ref<any[]>([])
const externalRequests = ref<any[]>([])

function setTab(tab: string) {
  activeTab.value = tab
  router.replace({ query: { ...route.query, tab } })
}

const stats = computed(() => {
  const all = allRequests.value
  return [
    { label: 'إجمالي المعاملات', value: all.length, dot: 'bg-gray-400' },
    { label: 'قيد الانتظار', value: all.filter(r => r.status === 'in_progress' || r.status === 'pending_services' || r.status === 'pending_hr' || r.status === 'pending_director').length, dot: 'bg-blue-500' },
    { label: 'معتمدة', value: all.filter(r => r.status === 'approved').length, dot: 'bg-emerald-500' },
    { label: 'مرفوضة', value: all.filter(r => r.status === 'rejected').length, dot: 'bg-red-500' },
    { label: 'خارجية معلقة', value: externalRequests.value.filter(r => r.status === 'in_progress').length, dot: 'bg-amber-500' },
  ]
})

const mainTabs = computed(() => [
  { value: 'all', label: 'كل المعاملات', icon: Inbox, count: allRequests.value.length },
  { value: 'internal', label: 'الداخلية', icon: Building2, count: internalRequests.value.length },
  { value: 'external', label: 'الخارجية', icon: Globe, count: externalRequests.value.length },
  { value: 'tracking', label: 'التتبع البصري', icon: GitBranch, count: 0 },
])

onMounted(() => fetchAll())

async function fetchAll() {
  loading.value = true
  try {
    // All forms
    const resAll = await servicesStore.fetchForms({})
    const formsList = (resAll?.results || resAll || []).map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || '',
    }))
    allFormsRaw.value = formsList
    allRequests.value = formsList

    // Internal
    const resInt = await servicesStore.fetchForms({ approval_type: 'internal' })
    const intForms = (resInt?.results || resInt || []).map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || '',
      service_type: f.service_type || 'form',
    }))
    // Add corrections to internal
    try {
      const corrRes = await api.get('/personnel/corrections/')
      const corrs = (corrRes.data?.results || corrRes.data || []).map((c: any) => ({
        id: `corr-${c.id}`, rawId: c.id, isCorrection: true, service_type: 'correction',
        form_type: c.correction_type,
        form_type_display: c.correction_type === 'national_id_correction' ? 'طلب تصحيح الرقم الوطني'
          : c.correction_type === 'military_number_correction' ? 'طلب تصحيح الرقم العسكري'
          : c.correction_type === 'name_correction' ? 'طلب تصحيح الاسم' : c.correction_type,
        personnel_name: c.personnel_name,
        personnel_military_number: c.personnel_military_number,
        status: c.status === 'pending' ? 'pending_services' : c.status,
        submitted_at: c.requested_at, old_value: c.old_value, new_value: c.new_value, notes: c.notes,
      }))
      internalRequests.value = [...intForms, ...corrs]
    } catch { internalRequests.value = intForms }

    // External
    const resExt = await servicesStore.fetchForms({ approval_type: 'external' })
    const extForms = (resExt?.results || resExt || []).map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || '',
    }))
    try {
      const corrRes2 = await api.get('/personnel/corrections/?type=name_correction')
      const extCorrs = (corrRes2.data?.results || corrRes2.data || []).map((c: any) => ({
        id: `corr-${c.id}`, rawId: c.id, isCorrection: true,
        form_type_display: 'طلب تصحيح الاسم (نموذج 23)',
        personnel_name: c.personnel_name, personnel_military_number: c.personnel_military_number,
        status: c.status === 'pending' ? 'in_progress' : c.status,
        submitted_at: c.requested_at, is_printed: c.is_printed,
        old_value: c.old_value, new_value: c.new_value,
        reason: c.notes || 'تصحيح الاسم بالكامل في السجلات العسكرية.',
      }))
      externalRequests.value = [...extForms, ...extCorrs]
    } catch { externalRequests.value = extForms }
  } catch (e) {
    console.error('Failed to fetch transactions', e)
  } finally {
    loading.value = false
  }
}

// ── All Tab Actions ──
async function handleApprove(tx: any) {
  const result = await Swal.fire({ title: 'اعتماد المعاملة؟', text: `الموافقة على المعاملة في مرحلة (${tx.current_step_name || 'الاعتماد'}).`, icon: 'success', showCancelButton: true, confirmButtonText: 'نعم، اعتماد', cancelButtonText: 'إلغاء', confirmButtonColor: '#10b981' })
  if (result.isConfirmed) {
    await servicesStore.approveForm(tx.id)
    fetchAll()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة', showConfirmButton: false, timer: 2000 })
  }
}

async function handleReject(tx: any) {
  const result = await Swal.fire({ title: 'رفض المعاملة؟', input: 'text', inputPlaceholder: 'سبب الرفض...', icon: 'warning', showCancelButton: true, confirmButtonText: 'تأكيد الرفض', cancelButtonText: 'إلغاء', confirmButtonColor: '#ef4444' })
  if (result.isConfirmed && result.value) {
    await servicesStore.rejectForm(tx.id, result.value)
    fetchAll()
    Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض المعاملة', showConfirmButton: false, timer: 2000 })
  }
}

// ── Internal Tab Actions ──
async function handleApproveInternal(req: any) {
  const result = await Swal.fire({ title: 'تأكيد الاعتماد', html: `<p class="text-sm text-gray-600">سيتم اعتماد الطلب <strong>#${String(req.isCorrection ? req.rawId : req.id).padStart(5,'0')}</strong> ونقله للمرحلة التالية.</p>`, icon: 'success', showCancelButton: true, confirmButtonText: 'نعم، اعتماد', cancelButtonText: 'إلغاء', confirmButtonColor: '#10b981' })
  if (result.isConfirmed) {
    try {
      if (req.isCorrection) { await api.post(`/personnel/corrections/${req.rawId}/approve/`) }
      else { await servicesStore.approveForm(req.id) }
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الاعتماد بنجاح', showConfirmButton: false, timer: 2500 })
      fetchAll()
    } catch (e: any) { Swal.fire({ icon: 'error', title: 'خطأ', text: e?.response?.data?.error || 'حدث خطأ' }) }
  }
}

async function handleRejectInternal(req: any) {
  const result = await Swal.fire({ title: 'رفض الطلب', input: 'textarea', inputPlaceholder: 'اكتب سبب الرفض...', inputAttributes: { dir: 'rtl' } as any, icon: 'warning', showCancelButton: true, confirmButtonText: 'تأكيد الرفض', cancelButtonText: 'إلغاء', confirmButtonColor: '#ef4444', inputValidator: (v) => !v ? 'يجب كتابة سبب الرفض' : undefined })
  if (result.isConfirmed && result.value) {
    try {
      if (req.isCorrection) { await api.post(`/personnel/corrections/${req.rawId}/reject/`, { reason: result.value }) }
      else { await servicesStore.rejectForm(req.id, result.value) }
      Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض الطلب', showConfirmButton: false, timer: 2500 })
      fetchAll()
    } catch (e: any) { Swal.fire({ icon: 'error', title: 'خطأ', text: e?.response?.data?.error || 'حدث خطأ' }) }
  }
}

// ── External Tab Actions ──
async function handlePrint(req: any) {
  try {
    if (req.isCorrection) {
      await api.post(`/personnel/corrections/${req.rawId}/mark_printed/`)
      window.open(`/services/print/model-23/${req.rawId}?personnelId=${req.personnel_military_number}&old_value=${req.old_value}&new_value=${req.new_value}&reason=${req.reason}`, '_blank')
    } else {
      await servicesStore.markFormPrinted(req.id)
      window.open(`/services/forms/${req.id}?print=true`, '_blank')
    }
    fetchAll()
  } catch (e: any) { Swal.fire('خطأ', e.response?.data?.error || 'حدث خطأ أثناء الطباعة', 'error') }
}

async function handleRegisterApproval(req: any) {
  const result = await Swal.fire({
    title: 'تسجيل موافقة الوزارة', html: `<div class="text-right" dir="rtl"><p class="text-xs text-gray-600 mb-3">يجب إرفاق ملف القرار/المذكرة الوزارية.</p><input type="file" id="ministry-doc" class="block w-full text-xs" accept=".pdf,.png,.jpg,.jpeg"></div>`,
    icon: 'info', showCancelButton: true, confirmButtonText: 'رفع واعتماد', cancelButtonText: 'إلغاء', confirmButtonColor: '#10b981', showLoaderOnConfirm: true,
    preConfirm: async () => {
      const fileInput = document.getElementById('ministry-doc') as HTMLInputElement
      if (!fileInput?.files?.length) { Swal.showValidationMessage('يجب اختيار ملف'); return false }
      const fd = new FormData(); fd.append('file', fileInput.files[0]); fd.append('document_type', 'ministry_approval')
      try {
        const uploadRes = await api.post('/storage/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
        const docId = uploadRes.data?.data?.id || uploadRes.data?.id
        if (!docId) throw new Error('فشل الحصول على معرّف المستند')
        if (req.isCorrection) { await api.post(`/personnel/corrections/${req.rawId}/approve/`, { approval_document_id: docId }) }
        else { await servicesStore.approveForm(req.id, { ministry_document_id: docId }) }
        return true
      } catch (e: any) { Swal.showValidationMessage(e.response?.data?.error || 'حدث خطأ'); return false }
    }
  })
  if (result.isConfirmed) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تسجيل موافقة الوزارة', showConfirmButton: false, timer: 2500 })
    fetchAll()
  }
}

async function handleRejectExternal(req: any) {
  const result = await Swal.fire({ title: 'رفض الطلب', input: 'text', inputPlaceholder: 'سبب الرفض...', icon: 'warning', showCancelButton: true, confirmButtonText: 'تأكيد الرفض', cancelButtonText: 'إلغاء', confirmButtonColor: '#ef4444', inputValidator: (v) => !v ? 'يجب كتابة سبب الرفض' : undefined })
  if (result.isConfirmed && result.value) {
    try {
      if (req.isCorrection) { await api.post(`/personnel/corrections/${req.rawId}/reject/`, { reason: result.value }) }
      else { await servicesStore.rejectForm(req.id, result.value) }
      Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض الطلب', showConfirmButton: false, timer: 2000 })
      fetchAll()
    } catch (e: any) { Swal.fire('خطأ', e.response?.data?.error || 'حدث خطأ', 'error') }
  }
}
</script>
