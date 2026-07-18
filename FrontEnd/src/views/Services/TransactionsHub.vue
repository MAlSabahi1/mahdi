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
        @filter-status="filterStatus = $event" @approve="handleApprove" @reject="handleReject"
        @submit-draft="handleSubmitDraft" />

      <InternalTab v-else-if="activeTab === 'internal'" :rows="internalRequests" :loading="loading"
        @approve="handleApproveInternal" @reject="handleRejectInternal"
        @submit-draft="handleSubmitDraft" @print="handlePrint" />

      <ExternalTab v-else-if="activeTab === 'external'" :rows="externalRequests" :loading="loading"
        @print="handlePrint" @register-approval="handleRegisterApproval" @bulk-register-approval="handleBulkRegisterApproval" @reject="handleRejectExternal" />

      <TrackingTab v-else-if="activeTab === 'tracking'" :rows="allFormsRaw" :loading="loading" />
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onActivated, onUnmounted, watch } from 'vue'
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

onMounted(() => {
  fetchAll()

  // ─── BroadcastChannel: تحديث فوري عند إتمام الطباعة من أي تبويب ───
  let bc: BroadcastChannel | null = null
  try {
    bc = new BroadcastChannel('print_status_channel')
    bc.onmessage = (event) => {
      if (event.data?.type === 'PRINTED') {
        // تحديث الصف المعني فوراً بدون انتظار الخادم
        const printedId = Number(event.data.id)
        const idx = externalRequests.value.findIndex(r => r.rawId === printedId || r.id === printedId)
        if (idx !== -1) {
          externalRequests.value[idx] = { ...externalRequests.value[idx], is_printed: true }
        }
        // ثم تحديث من الخادم في الخلفية للتأكيد
        fetchExternalCorrections()
      }
    }
  } catch (_) { /* المتصفح لا يدعم BroadcastChannel */ }

  // إعادة جلب البيانات عند عودة المستخدم للتبويب (بعد طباعة في تبويب آخر)
  const onVisible = () => {
    if (document.visibilityState === 'visible') {
      fetchExternalCorrections()
    }
  }
  document.addEventListener('visibilitychange', onVisible)
  onUnmounted(() => {
    document.removeEventListener('visibilitychange', onVisible)
    bc?.close()
  })
})
// تحديث عند التنقل بين الصفحات (Vue Router keep-alive)
onActivated(() => fetchExternalCorrections())

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
      const corrRes = await api.get('/personnel/corrections/?page_size=500')
      const corrs = (corrRes.data?.results || corrRes.data || [])
        .filter((c: any) => !['name_correction', 'military_number_swap', 'military_number_correction'].includes(c.correction_type))
        .map((c: any) => ({
        id: `corr-${c.id}`, rawId: c.id, isCorrection: true, service_type: 'correction',
        form_type: c.correction_type,
        form_type_display: c.correction_type === 'national_id_correction' ? 'طلب تصحيح الرقم الوطني'
          : c.correction_type === 'data_correction' ? 'تصحيح بيانات عامة' : c.correction_type,
        personnel_name: c.personnel_name,
        personnel_military_number: c.personnel_military_number,
        status: c.status === 'pending' ? 'pending_services' : c.status,
        submitted_at: c.requested_at, old_value: c.old_value, new_value: c.new_value, notes: c.notes,
        is_printed: c.is_printed || false,
      }))
      internalRequests.value = [...intForms, ...corrs]
    } catch { internalRequests.value = intForms }

    // External - fetch all name corrections
    await fetchExternalCorrections()

  } catch (e) {
    console.error('Failed to fetch transactions', e)
  } finally {
    loading.value = false
  }
}

// دالة مخصصة لجلب طلبات التصحيح الخارجية فقط (أسرع)
async function fetchExternalCorrections() {
  try {
    const resExt = await servicesStore.fetchForms({ approval_type: 'external', _t: Date.now() })
    const extForms = (resExt?.results || resExt || []).map((f: any) => ({
      ...f,
      personnel_name: f.personnel?.full_name || f.personnel_name || '',
      personnel_military_number: f.personnel?.military_number || f.personnel_military_number || '',
    }))
    const corrRes2 = await api.get(`/personnel/corrections/?page_size=500&_t=${Date.now()}`)
    const extCorrs = (corrRes2.data?.results || corrRes2.data || [])
      .filter((c: any) => ['name_correction', 'military_number_swap', 'military_number_correction'].includes(c.correction_type))
      .map((c: any) => ({
      id: `corr-${c.id}`, rawId: c.id, isCorrection: true,
      form_type_display: c.correction_type === 'name_correction' ? 'طلب تصحيح الاسم (نموذج 23)' 
        : c.correction_type === 'military_number_swap' ? 'طلب التبديل المترابط للأرقام العسكرية' 
        : 'طلب تصحيح الرقم العسكري',
      personnel_name: c.personnel_name, personnel_military_number: c.personnel_military_number,
      status: c.status === 'pending' ? 'in_progress' : c.status,
      submitted_at: c.requested_at, is_printed: c.is_printed || false,
      old_value: c.old_value, new_value: c.new_value,
      reason: c.notes || (c.correction_type === 'name_correction' ? 'تصحيح الاسم بالكامل في السجلات العسكرية.' : ''),
      ministry_approval_doc_id: c.approval_document,
    }))
    
    // حفظ الحالة المحلية للطباعة لتجنب فقدانها إذا رجعت استجابة قديمة من السيرفر (Race condition)
    const existingMap = new Map(externalRequests.value.map(r => [r.rawId || r.id, r]))
    
    externalRequests.value = [...extForms, ...extCorrs].map(newReq => {
      const existing = existingMap.get(newReq.rawId || newReq.id)
      if (existing && existing.is_printed && !newReq.is_printed) {
        newReq.is_printed = true
      }
      return newReq
    })
  } catch { /* keep current state */ }
}

// ── Submit Draft ──
async function handleSubmitDraft(tx: any) {
  const result = await Swal.fire({
    title: 'تقديم الطلب',
    html: `<div class="text-right" dir="rtl">
      <p class="text-sm text-gray-600 mb-2">سيتم تقديم المعاملة <b class="font-mono text-blue-600">#${String(tx.id).padStart(5,'0')}</b> وبدء دورة الاعتماد.</p>
      <p class="text-xs text-amber-600 bg-amber-50 px-3 py-2 rounded-lg border border-amber-100">⚠️ بعد التقديم لا يمكن تعديل بيانات الطلب.</p>
    </div>`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'نعم، قدّم الطلب',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#2563eb',
    reverseButtons: true
  })
  if (!result.isConfirmed) return
  try {
    await servicesStore.submitForm(tx.id)
    Swal.fire({
      toast: true, position: 'top-end', icon: 'success',
      title: '✅ تم تقديم الطلب وبدأ سير العمل',
      showConfirmButton: false, timer: 3000
    })
    fetchAll()
  } catch (e: any) {
    const msg = e?.response?.data?.error || 'حدث خطأ أثناء التقديم'
    Swal.fire({ icon: 'error', title: 'فشل التقديم', text: msg })
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
  const stepLabel = req.current_step_name ? `المرحلة الحالية: <b>${req.current_step_name}</b>` : ''
  const result = await Swal.fire({
    title: 'تأكيد الاعتماد',
    html: `<div class="text-right" dir="rtl">
      <p class="text-sm text-gray-600 mb-2">سيتم اعتماد الطلب <b class="font-mono text-blue-600">#${String(req.isCorrection ? req.rawId : req.id).padStart(5,'0')}</b> ونقله للمرحلة التالية.</p>
      ${stepLabel ? `<p class="text-xs text-gray-500">${stepLabel}</p>` : ''}
    </div>`,
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتماد وتمرير',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981'
  })
  if (result.isConfirmed) {
    try {
      let res: any
      if (req.isCorrection) {
        res = await api.post(`/personnel/corrections/${req.rawId}/approve/`)
      } else {
        res = await servicesStore.approveForm(req.id)
      }
      const msg = res?.data?.message || res?.message || 'تم الاعتماد بنجاح'
      const isFinal = res?.data?.is_final ?? res?.is_final ?? false
      Swal.fire({
        toast: true, position: 'top-end', icon: 'success',
        title: isFinal ? '✅ تم الاعتماد النهائي' : `✅ ${msg}`,
        showConfirmButton: false, timer: 3000
      })
      fetchAll()
    } catch (e: any) {
      let errorMsg = e?.response?.data?.error || 'حدث خطأ'

      if (errorMsg.includes('يجب إرفاق الاستمارة الموقعة')) {
        return promptSignedDocInternal(req)
      }

      if (e?.response?.data && typeof e.response.data === 'object' && !e.response.data.error) {
        errorMsg = Object.values(e.response.data).flat().join('\n')
      }
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
  }
}

async function promptSignedDocInternal(req: any) {
  const result = await Swal.fire({
    title: 'إرفاق الاستمارة الموقعة',
    html: `<div class="text-right" dir="rtl">
             <div id="swal-upload-wrapper" class="p-4 border border-dashed rounded-xl transition-colors border-gray-300 dark:border-gray-700 text-right">
               <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                 <div>
                   <p class="font-bold text-sm flex items-center gap-2 text-gray-900 dark:text-white">
                     الاستمارة الموقعة ورقياً من المدير العام <span class="text-red-500">*</span>
                     <span id="swal-upload-badge" class="hidden text-emerald-600 text-[10px] bg-emerald-100 dark:bg-emerald-900/50 px-2 py-0.5 rounded font-bold border border-emerald-200 dark:border-emerald-800">✓ تم الرفع</span>
                   </p>
                   <p class="text-xs text-gray-400 mt-1">صيغ مدعومة: PDF, JPG, PNG (الحد الأقصى 5MB)</p>
                   <p id="swal-file-name" class="hidden text-xs text-emerald-600 mt-1.5 font-mono bg-white dark:bg-gray-900 inline-block px-2 py-1 rounded border border-emerald-100 dark:border-emerald-900/30"></p>
                 </div>
                 <div class="flex items-center gap-3 self-end sm:self-auto">
                   <label id="swal-upload-btn" for="signed-doc-internal" class="cursor-pointer bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 text-xs font-bold px-4 py-2.5 rounded-lg transition-colors shadow-sm">
                     اختيار ملف
                   </label>
                   <input id="signed-doc-internal" type="file" class="hidden" accept=".pdf,.jpg,.jpeg,.png" onchange="
                     const w = document.getElementById('swal-upload-wrapper');
                     const b = document.getElementById('swal-upload-badge');
                     const n = document.getElementById('swal-file-name');
                     const btn = document.getElementById('swal-upload-btn');
                     if(this.files && this.files[0]) {
                       w.classList.remove('border-gray-300', 'dark:border-gray-700');
                       w.classList.add('border-emerald-400', 'bg-emerald-50/50', 'dark:bg-emerald-950/20');
                       b.style.display = 'inline-block';
                       n.style.display = 'inline-block';
                       n.innerText = this.files[0].name;
                       btn.innerText = 'تغيير الملف';
                     } else {
                       w.classList.add('border-gray-300', 'dark:border-gray-700');
                       w.classList.remove('border-emerald-400', 'bg-emerald-50/50', 'dark:bg-emerald-950/20');
                       b.style.display = 'none';
                       n.style.display = 'none';
                       btn.innerText = 'اختيار ملف';
                     }
                   ">
                 </div>
               </div>
             </div>
           </div>`,
    icon: 'info', showCancelButton: true, confirmButtonText: 'رفع واعتماد', cancelButtonText: 'إلغاء', confirmButtonColor: '#10b981', showLoaderOnConfirm: true,
    preConfirm: async () => {
      const fileInput = document.getElementById('signed-doc-internal') as HTMLInputElement
      if (!fileInput?.files?.length) { Swal.showValidationMessage('يجب اختيار ملف'); return false }
      const fd = new FormData()
      fd.append('file', fileInput.files[0])
      fd.append('document_type', 'signed_form')
      try {
        const uploadRes = await api.post('/storage/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
        const docId = uploadRes.data?.data?.id || uploadRes.data?.id
        if (!docId) throw new Error('فشل الحصول على معرّف المستند')
        return docId
      } catch (e: any) {
        Swal.showValidationMessage(e.response?.data?.error || 'حدث خطأ أثناء رفع الملف')
        return false
      }
    }
  })
  
  if (result.isConfirmed && result.value) {
    try {
      if (req.isCorrection) {
        await api.post(`/personnel/corrections/${req.rawId}/approve/`, { signed_document_id: result.value })
      } else {
        await servicesStore.approveForm(req.id, { signed_document_id: result.value })
      }
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الاعتماد النهائي بنجاح', showConfirmButton: false, timer: 3000 })
      fetchAll()
    } catch (e: any) {
      let errorMsg = e?.response?.data?.error || 'حدث خطأ'
      if (e?.response?.data && typeof e.response.data === 'object' && !e.response.data.error) {
        errorMsg = Object.values(e.response.data).flat().join('\n')
      }
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
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
    } catch (e: any) {
      let errorMsg = e?.response?.data?.error || 'حدث خطأ'
      if (e?.response?.data && typeof e.response.data === 'object' && !e.response.data.error) {
        errorMsg = Object.values(e.response.data).flat().join('\n')
      }
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
  }
}

// ── External Tab Actions ──
async function handlePrint(req: any) {
  try {
    if (req.isCorrection) {
      // خطوة 1: سجل الطباعة في الخادم أولاً وانتظر النتيجة
      try { 
        await api.post(`/personnel/corrections/${req.rawId}/mark_printed/`) 
      } catch (err) { 
        console.warn('[print] mark_printed failed:', err) 
      }

      // خطوة 2: تحديث فوري للحالة المحلية
      const idx = externalRequests.value.findIndex(r => r.rawId === req.rawId)
      if (idx !== -1) {
        externalRequests.value[idx] = { ...externalRequests.value[idx], is_printed: true }
      }

      // خطوة 3: تحديث من الخادم لضمان تزامن البيانات
      fetchExternalCorrections()

      // خطوة 4: فتح صفحة الطباعة
      const routeUrl = router.resolve(`/services/corrections/${req.rawId}/print`).href
      window.open(routeUrl, '_blank')
    } else {
      // الخدمات العادية → منشئ المذكرات الرسمية مع بيانات مُعبأة تلقائياً
      try { await servicesStore.markFormPrinted(req.id) } catch (_) { /* لا نوقف الطباعة */ }

      // ── بناء draft المذكرة من بيانات المعاملة ──
      const personnelName = req.personnel_name || req.personnel?.full_name || ''
      const militaryNumber = req.personnel_military_number || req.personnel?.military_number || ''
      const formType = req.form_type_display || req.form_type || ''
      const txNumber = `TX-${String(req.id).padStart(6, '0')}`
      const today = new Date()
      const dateStr = today.toLocaleDateString('ar-YE', { year: 'numeric', month: '2-digit', day: '2-digit' })

      let memoDraft = {
        documentType: 'PERSONNEL_MEMO',
        securityLevel: 'NORMAL',
        referenceNo: txNumber,
        docDate: dateStr,
        correspondingDate: '',
        attachments: 'نموذج إثبات حالة',
        bilingual: false,
        issuerLine1: '',
        issuerLine2: '',
        issuerLine3: '',
        addressees: [
          { prefix: 'الأخ /', name: 'المدير العام للمحافظة', suffix: 'المحترم' }
        ],
        involvedPersonnel: [
          {
            militaryId: militaryNumber,
            rank: req.personnel?.rank_display || '',
            name: personnelName,
            nationalId: '',
            status: formType,
            workplace: '',
            serviceLocation: '',
            notes: '',
          }
        ],
        subject: `بخصوص طلب إثبات حالة (${formType}) — ${personnelName}`,
        body: `<p>نحيط سيادتكم علماً بأنه تم اعتماد طلب إثبات حالة (${formType}) للمنتسب المذكور أعلاه.</p><p>رقم المعاملة: <strong>${txNumber}</strong></p><p>نأمل التكرم بالاطلاع واتخاذ اللازم.</p>`,
        conclusion: '<p>والله الموفق ،،،</p>',
        signatures: [
          { title: 'رئيس قسم الخدمات', rank: '', name: '', showSeal: false },
          { title: 'مدير إدارة القوى البشرية', rank: '', name: '', showSeal: true },
        ],
        signatureSettings: { showLabels: true, showFrame: true },
        visibleColumns: {
          militaryId: true, rank: true, nationalId: false,
          status: true, workplace: false, serviceLocation: false,
          jobTitle: false, position: false, qualification: false,
          joinDate: false, commencementDate: false, phone: false,
          clarification: false, notes: true,
        },
        typography: {
          addressee:  { family: 'Cairo', size: 1.1, weight: 'font-bold', underline: true },
          greeting:   { family: 'Cairo', size: 1.0, weight: 'font-bold', underline: true },
          subject:    { family: 'Cairo', size: 1.15, weight: 'font-black', underline: true },
          body:       { family: 'Cairo', size: 1.0, weight: 'font-normal', underline: false },
          conclusionSeparator: { family: 'Cairo', size: 1.1, weight: 'font-bold', underline: true },
          conclusionBody: { family: 'Cairo', size: 1.0, weight: 'font-normal', underline: false },
          signatures: { family: 'Cairo', size: 0.95, weight: 'font-bold', underline: false },
        },
      }

                // Try to load any generic template or just fallback to default
          const tplStr = localStorage.getItem('memo_template_WORK_COMMENCEMENT') || localStorage.getItem('memo_template_ATTENTION_NOTICE');
          if (tplStr && (req?.form_type === 'work_commencement' || req?.form_type === 'attention_notice')) {
            try {
              const tpl = JSON.parse(tplStr);
              memoDraft = { ...memoDraft, ...tpl, referenceNo: memoDraft.referenceNo, docDate: memoDraft.docDate, involvedPersonnel: [] };
            } catch(e) {}
          }
          localStorage.setItem('official_memo_draft', JSON.stringify(memoDraft))
      window.open('/admin/documents/memo-preview', '_blank')
    }
    fetchAll()
  } catch (e: any) { Swal.fire('خطأ', e.response?.data?.error || 'حدث خطأ أثناء الطباعة', 'error') }
}

async function handleRegisterApproval(req: any) {
  const result = await Swal.fire({
    title: 'تسجيل موافقة الوزارة', 
    html: `
      <div class="text-right" dir="rtl">
        <div class="bg-blue-50 border border-blue-100 rounded-xl p-4 mb-4">
          <div class="flex items-start gap-3">
            <div class="bg-blue-100 p-2 rounded-lg text-blue-600 mt-0.5 shrink-0">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
            <div>
              <h4 class="text-sm font-bold text-blue-900 mb-1">القرار / المذكرة الوزارية</h4>
              <p class="text-xs text-blue-700 leading-relaxed">يجب إرفاق ملف القرار أو المذكرة الوزارية. سيتم ربط هذا الملف بالمعاملة كوثيقة اعتماد نهائية.</p>
            </div>
          </div>
        </div>
        <div class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:bg-gray-50 transition-colors relative group overflow-hidden">
          <div class="pointer-events-none">
            <svg class="w-8 h-8 text-gray-400 group-hover:text-brand-500 transition-colors mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            <span class="text-sm font-bold text-brand-600 mb-1 block">اضغط هنا لاختيار الملف</span>
            <span class="text-[11px] text-gray-500 block">PDF, PNG, JPG</span>
          </div>
          <input type="file" id="ministry-doc" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept=".pdf,.png,.jpg,.jpeg" onchange="document.getElementById('file-name').textContent = this.files[0]?.name || ''">
          <div id="file-name" class="mt-3 text-[11px] font-bold text-gray-700 bg-gray-200 py-1 px-3 rounded-md inline-block max-w-full truncate empty:hidden"></div>
        </div>
      </div>
    `,
    customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-xl text-sm font-bold px-6', cancelButton: 'rounded-xl text-sm font-bold px-6' },
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

async function handleBulkRegisterApproval(rows: any[]) {
  const result = await Swal.fire({
    title: `تسجيل موافقة الوزارة لـ ${rows.length} طلبات`, 
    html: `
      <div class="text-right" dir="rtl">
        <div class="bg-emerald-50 border border-emerald-100 rounded-xl p-4 mb-4">
          <div class="flex items-start gap-3">
            <div class="bg-emerald-100 p-2 rounded-lg text-emerald-600 mt-0.5 shrink-0">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            </div>
            <div>
              <h4 class="text-sm font-bold text-emerald-900 mb-1">تطبيق المذكرة على الجميع</h4>
              <p class="text-[11px] text-emerald-700 leading-relaxed font-bold">الملف الذي ستقوم برفعه الآن سيتم اعتماده كوثيقة رسمية لجميع الطلبات المحددة وعددها (${rows.length}).</p>
            </div>
          </div>
        </div>
        <div class="border-2 border-dashed border-emerald-300 bg-white rounded-xl p-6 text-center hover:bg-emerald-50/50 transition-colors relative group overflow-hidden">
          <div class="pointer-events-none">
            <svg class="w-8 h-8 text-emerald-400 group-hover:text-emerald-500 transition-colors mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
            <span class="text-sm font-bold text-emerald-600 mb-1 block">اضغط هنا لاختيار الملف</span>
            <span class="text-[11px] text-gray-500 block">PDF, PNG, JPG</span>
          </div>
          <input type="file" id="bulk-ministry-doc" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept=".pdf,.png,.jpg,.jpeg" onchange="document.getElementById('bulk-file-name').textContent = this.files[0]?.name || ''">
          <div id="bulk-file-name" class="mt-3 text-[11px] font-bold text-emerald-800 bg-emerald-100 py-1 px-3 rounded-md inline-block max-w-full truncate empty:hidden"></div>
        </div>
      </div>
    `,
    customClass: { popup: 'rounded-2xl border-t-4 border-t-emerald-500', confirmButton: 'rounded-xl text-sm font-bold px-6', cancelButton: 'rounded-xl text-sm font-bold px-6' },
    icon: 'info', showCancelButton: true, confirmButtonText: 'رفع واعتماد الجميع', cancelButtonText: 'إلغاء', confirmButtonColor: '#10b981', showLoaderOnConfirm: true,
    preConfirm: async () => {
      const fileInput = document.getElementById('bulk-ministry-doc') as HTMLInputElement
      if (!fileInput?.files?.length) { Swal.showValidationMessage('يجب اختيار ملف'); return false }
      const fd = new FormData(); fd.append('file', fileInput.files[0]); fd.append('document_type', 'ministry_approval')
      try {
        // 1. رفع المرفق مرة واحدة
        const uploadRes = await api.post('/storage/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
        const docId = uploadRes.data?.data?.id || uploadRes.data?.id
        if (!docId) throw new Error('فشل الحصول على معرّف المستند')
        
        // 2. فصل الطلبات
        const correctionIds = rows.filter(r => r.isCorrection).map(r => r.rawId)
        const regularForms = rows.filter(r => !r.isCorrection)
        
        const promises = []
        
        // الاعتماد الجماعي للتصحيحات في الخادم
        if (correctionIds.length > 0) {
          promises.push(api.post('/personnel/corrections/approve_batch/', {
            correction_ids: correctionIds,
            memo_document_id: docId
          }))
        }
        
        // الاعتماد الفردي للطلبات العادية
        for (const req of regularForms) {
          promises.push(servicesStore.approveForm(req.id, { ministry_document_id: docId }))
        }
        
        await Promise.all(promises)
        return true
      } catch (e: any) { Swal.showValidationMessage(e.response?.data?.error || 'حدث خطأ أثناء الاعتماد الجماعي'); return false }
    }
  })
  
  if (result.isConfirmed) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد جميع الطلبات المحددة بنجاح', showConfirmButton: false, timer: 3000 })
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
    } catch (e: any) {
      let errorMsg = e?.response?.data?.error || 'حدث خطأ'
      if (e?.response?.data && typeof e.response.data === 'object' && !e.response.data.error) {
        errorMsg = Object.values(e.response.data).flat().join('\n')
      }
      Swal.fire('خطأ', errorMsg, 'error')
    }
  }
}
</script>
