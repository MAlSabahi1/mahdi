<template>
  <admin-layout>
    <div class="print:hidden">
      <PageBreadcrumb :pageTitle="'تفاصيل المعاملة رقم ' + (form?.id || '')" />
    </div>

    <div v-if="loading" class="flex justify-center items-center py-20 print:hidden">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
    </div>

    <div v-else-if="error || !form" class="bg-red-50 text-red-600 p-6 rounded-2xl text-center font-bold print:hidden">
      {{ error || 'لم يتم العثور على تفاصيل هذه المعاملة.' }}
      <div class="mt-4">
        <RouterLink to="/services/inbox" class="text-brand-600 underline">العودة لصندوق المعاملات</RouterLink>
      </div>
    </div>

    <div v-else class="space-y-6 text-start" dir="rtl">
      <!-- Header / Summary Card -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6 print:border-none print:shadow-none print:p-0">
        <div class="flex items-center gap-5">
          <div class="h-16 w-16 bg-gray-50 dark:bg-gray-800 rounded-2xl flex items-center justify-center border border-gray-100 dark:border-gray-700">
            <svg class="w-8 h-8 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-bold tracking-widest text-brand-500 uppercase bg-brand-50 dark:bg-brand-950/30 px-2 py-0.5 rounded border border-brand-100 dark:border-brand-900">
                TX-{{ form.id.toString().padStart(6, '0') }}
              </span>
              <span :class="getStatusColor(form.status)" class="text-[10px] font-bold px-2 py-0.5 rounded flex items-center gap-1">
                <span :class="getStatusDot(form.status)" class="h-1.5 w-1.5 rounded-full"></span>
                {{ getStatusLabel(form.status, form.current_step_name) }}
              </span>
            </div>
            <h1 class="text-xl font-black text-gray-900 dark:text-white">
              {{ form.form_type_display || form.form_type }}
            </h1>
            <p class="text-xs text-gray-500 mt-1">تاريخ التقديم: {{ new Date(form.submitted_at || form.created_at).toLocaleString('en-GB') }}</p>
          </div>
        </div>

        <div class="flex flex-wrap gap-2 w-full md:w-auto print:hidden">
          <button v-if="form.status === 'in_progress'" @click="approveForm" class="flex-1 md:flex-none bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2.5 rounded-xl transition-all shadow-lg shadow-emerald-500/20 text-sm flex items-center justify-center gap-2">
            اعتماد الطلب
          </button>
          <button v-if="form.status === 'in_progress'" @click="returnFormModal" class="flex-1 md:flex-none bg-amber-50 text-amber-600 hover:bg-amber-100 border border-amber-200 dark:bg-amber-950/20 dark:border-amber-900 font-bold px-6 py-2.5 rounded-xl transition-all text-sm flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"/></svg>
            إرجاع
          </button>
          <button v-if="form.status === 'in_progress'" @click="rejectForm" class="flex-1 md:flex-none bg-red-50 text-red-600 hover:bg-red-100 border border-red-200 dark:bg-red-950/20 dark:border-red-900 font-bold px-6 py-2.5 rounded-xl transition-all text-sm">
            رفض
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 print:block print:w-full">
        <!-- Main Content (Left / Right side depending on dir) -->
        <div class="lg:col-span-2 space-y-6 print:w-full print:block">
          <!-- Personnel Details -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              بيانات الفرد
            </h2>
            <div class="grid grid-cols-2 gap-4">
              <div class="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                <p class="text-[10px] text-gray-500 mb-1">الاسم الرباعي</p>
                <p class="text-sm font-bold text-gray-900 dark:text-white">{{ form.personnel?.full_name || '-' }}</p>
              </div>
              <div class="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                <p class="text-[10px] text-gray-500 mb-1">الرقم العسكري</p>
                <p class="text-sm font-bold font-mono text-gray-900 dark:text-white">{{ form.personnel?.military_number || '-' }}</p>
              </div>
              <div class="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                <p class="text-[10px] text-gray-500 mb-1">الرتبة الحالية</p>
                <p class="text-sm font-bold text-gray-900 dark:text-white">{{ form.personnel?.rank || '-' }}</p>
              </div>
              <div class="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                <p class="text-[10px] text-gray-500 mb-1">تاريخ النفاذ</p>
                <p class="text-sm font-bold font-mono text-gray-900 dark:text-white">{{ form.effective_date ? new Date(form.effective_date).toLocaleDateString('en-GB') : '-' }}</p>
              </div>
            </div>
          </div>

          <!-- Form Data -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              تفاصيل الاستمارة
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(value, key) in form.form_data" :key="key" class="p-3 border border-gray-100 dark:border-gray-800 rounded-xl">
                <p class="text-[10px] text-gray-500 mb-1 capitalize">{{ String(key).replace(/_/g, ' ') }}</p>
                <p class="text-sm font-bold text-gray-900 dark:text-white">{{ value || '-' }}</p>
              </div>
            </div>
            
            <div v-if="form.notes" class="mt-4 p-4 bg-amber-50 dark:bg-amber-950/20 text-amber-800 dark:text-amber-200 rounded-xl text-sm border border-amber-100 dark:border-amber-900">
              <p class="text-[10px] font-bold uppercase tracking-wider mb-1 opacity-70">ملاحظات إضافية</p>
              {{ form.notes }}
            </div>
            
            <div v-if="form.rejection_reason" class="mt-4 p-4 bg-red-50 dark:bg-red-950/20 text-red-800 dark:text-red-200 rounded-xl text-sm border border-red-100 dark:border-red-900">
              <p class="text-[10px] font-bold uppercase tracking-wider mb-1 opacity-70">سبب الرفض</p>
              {{ form.rejection_reason }}
            </div>
          </div>

          <!-- Attachments -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/></svg>
              المرفقات المدعمة
            </h2>
            <div v-if="form.attachments && form.attachments.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div v-for="att in form.attachments" :key="att.id" class="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer group">
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-brand-50 dark:bg-brand-950/30 text-brand-600 rounded-lg group-hover:bg-brand-100 transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-900 dark:text-white">{{ att.document_type || 'مستند مرفق' }}</p>
                    <p class="text-[10px] text-gray-500 font-mono">ID: {{ att.id }}</p>
                  </div>
                </div>
                <a :href="att.file" target="_blank" class="text-[10px] font-bold text-brand-600 bg-brand-50 dark:bg-brand-950/30 px-2.5 py-1 rounded-lg hover:bg-brand-100 transition-colors">
                  معاينة
                </a>
              </div>
            </div>
            <div v-else class="text-center py-6 text-sm text-gray-500 bg-gray-50 dark:bg-gray-800/30 rounded-xl border border-dashed border-gray-200 dark:border-gray-700">
              لا توجد مرفقات مرتبطة بهذه المعاملة.
            </div>
          </div>
          
          <!-- Notes Section -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
              الملاحظات والتعليقات
            </h2>
            
            <div class="space-y-4 mb-4 max-h-64 overflow-y-auto pr-2">
              <div v-if="notes.length === 0" class="text-center text-xs text-gray-500 py-4">
                لا توجد ملاحظات على هذه المعاملة حتى الآن.
              </div>
              <div v-for="note in notes" :key="note.id" class="bg-gray-50 dark:bg-gray-800/50 p-3 rounded-xl border border-gray-100 dark:border-gray-700">
                <div class="flex justify-between items-start mb-1">
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ note.created_by_name }}</span>
                  <span class="text-[10px] text-gray-500">{{ new Date(note.created_at).toLocaleString('en-GB') }}</span>
                </div>
                <p class="text-sm text-gray-700 dark:text-gray-300">{{ note.content }}</p>
              </div>
            </div>
            
            <div class="flex gap-2">
              <input v-model="newNote" type="text" placeholder="اكتب ملاحظة هنا..." class="flex-1 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" @keyup.enter="submitNote" />
              <button @click="submitNote" :disabled="!newNote.trim()" class="bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white px-4 py-2 rounded-xl text-sm font-bold transition-colors">
                إرسال
              </button>
            </div>
          </div>
        </div>

        <!-- Sidebar Timeline -->
        <div class="space-y-6 print:hidden">
        
          <!-- Checklist Section -->
          <div v-if="checklist.length > 0" class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              قائمة التحقق للمرحلة
            </h2>
            <div class="space-y-3">
              <label v-for="item in checklist" :key="item.id" class="flex items-center gap-3 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors">
                <input type="checkbox" :checked="item.is_checked" @change="toggleChecklist(item)" class="w-4 h-4 text-brand-600 rounded border-gray-300 focus:ring-brand-500" />
                <span class="text-sm text-gray-700 dark:text-gray-300 select-none" :class="{ 'line-through opacity-50': item.is_checked }">
                  {{ item.title }}
                  <span v-if="item.is_required" class="text-red-500 ml-1">*</span>
                </span>
              </label>
            </div>
          </div>
        
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-6">سجل الأحداث</h2>
            
            <div class="relative pl-4 space-y-6">
              <!-- Vertical Line -->
              <div class="absolute right-[11px] top-2 bottom-2 w-0.5 bg-gray-100 dark:bg-gray-800"></div>

              <div v-for="event in timeline" :key="event.id" class="relative flex items-start gap-4 pr-6 text-right">
                <span class="absolute right-0 top-1.5 h-6 w-6 rounded-full bg-brand-500 text-white flex items-center justify-center text-[10px] z-10 shadow-sm border border-white dark:border-gray-900">
                  <svg v-if="event.action === 'created' || event.action === 'submitted'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                  <svg v-else-if="event.action === 'approved' || event.action === 'checklist_checked'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                  <svg v-else-if="event.action === 'rejected'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                  <svg v-else-if="event.action === 'returned'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"/></svg>
                  <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
                </span>
                <div>
                  <p class="text-xs font-bold text-gray-900 dark:text-white">{{ event.action_display }}</p>
                  <p class="text-[10px] text-gray-500 mt-0.5">{{ event.performed_by_name || 'النظام' }}</p>
                  <p v-if="event.notes" class="text-[10px] text-gray-600 dark:text-gray-400 mt-1 bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">{{ event.notes }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Print Only Attachments Section -->
    <div class="hidden print:block w-full" v-if="form?.attachments?.length">
      <div v-for="(att, idx) in form.attachments" :key="'print-att-'+att.id" style="page-break-before: always; padding-top: 2cm;">
        <h3 class="text-xl font-bold text-center mb-6 text-gray-900 border-b-2 border-gray-800 pb-2 inline-block">
          مرفق ({{ Number(idx) + 1 }}): {{ att.document_type || 'مستند' }}
        </h3>
        <div class="flex justify-center w-full">
          <!-- Try to render as image. Note: If it's a PDF, browsers usually don't print the embedded object well, but this is standard for images -->
          <img v-if="att.file && !att.file.endsWith('.pdf')" :src="att.file" class="max-w-full max-h-[25cm] border border-gray-400 p-2 shadow-sm" alt="Attachment">
          <div v-else class="text-center p-10 border-2 border-dashed border-gray-400">
            <p class="font-bold text-gray-800 text-lg">هذا المرفق بصيغة PDF</p>
            <p class="text-sm text-gray-600">يرجى طباعته بشكل مستقل من النظام.</p>
            <p class="text-xs mt-4">{{ att.file }}</p>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()

const id = route.params.id as string
const form = ref<any>(null)
const loading = ref(true)
const error = ref('')

const timeline = ref<any[]>([])
const notes = ref<any[]>([])
const checklist = ref<any[]>([])
const newNote = ref('')

onMounted(async () => {
  if (!id) {
    error.value = 'رقم المعاملة مفقود.'
    loading.value = false
    return
  }
  await fetchFormDetails()
})

async function fetchFormDetails() {
  loading.value = true
  try {
    form.value = await servicesStore.fetchFormById(id)
    // Fetch extended data parallel
    const [t, n, c] = await Promise.all([
      servicesStore.fetchFormTimeline(id),
      servicesStore.fetchFormNotes(id),
      servicesStore.fetchFormChecklist(id, form.value.status)
    ])
    timeline.value = t
    notes.value = n
    checklist.value = c
    
    // Auto-trigger print if requested via query string
    if (route.query.print === 'true') {
      setTimeout(() => {
        window.print()
      }, 500)
    }
  } catch (err: any) {
    error.value = 'فشل جلب تفاصيل المعاملة.'
  } finally {
    loading.value = false
  }
}

async function submitNote() {
  if (!newNote.value.trim()) return
  try {
    const note = await servicesStore.addFormNote(id, newNote.value)
    notes.value.push(note)
    newNote.value = ''
    timeline.value = await servicesStore.fetchFormTimeline(id) // refresh timeline
  } catch (err: any) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'فشل إضافة الملاحظة', showConfirmButton: false, timer: 2000 })
  }
}

async function toggleChecklist(item: any) {
  try {
    item.is_checked = !item.is_checked
    await servicesStore.toggleChecklistItem(item.id, item.is_checked)
    timeline.value = await servicesStore.fetchFormTimeline(id) // refresh timeline
  } catch (err: any) {
    item.is_checked = !item.is_checked // revert on fail
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'فشل تحديث القائمة', showConfirmButton: false, timer: 2000 })
  }
}

async function approveForm() {
  if (!form.value) return

  Swal.fire({
    title: 'تأكيد الاعتماد؟',
    text: `سيتم الاعتماد وتمرير المعاملة.`,
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتماد',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await servicesStore.approveForm(form.value.id)
        Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة', showConfirmButton: false, timer: 2000 })
        fetchFormDetails() // refresh
      } catch (err: any) {
        Swal.fire({ icon: 'error', title: 'خطأ', text: err.response?.data?.error || 'حدث خطأ' })
      }
    }
  })
}

async function rejectForm() {
  if (!form.value) return
  Swal.fire({
    title: 'رفض المعاملة؟',
    text: `الرجاء كتابة سبب الرفض:`,
    input: 'text',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444'
  }).then(async (result) => {
    if (result.isConfirmed && result.value) {
      try {
        await servicesStore.rejectForm(form.value.id, result.value)
        Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض المعاملة', showConfirmButton: false, timer: 2000 })
        fetchFormDetails() // refresh
      } catch (err: any) {
        Swal.fire({ icon: 'error', title: 'خطأ', text: err.response?.data?.error || 'حدث خطأ' })
      }
    }
  })
}

async function returnFormModal() {
  if (!form.value) return
  
  const { value: formValues } = await Swal.fire({
    title: 'إرجاع المعاملة للتعديل',
    html:
      '<select id="swal-reason" class="swal2-select w-[80%] mx-auto mb-4" dir="rtl">' +
      '<option value="missing_attachments">نقص المرفقات</option>' +
      '<option value="incorrect_data">بيانات غير صحيحة</option>' +
      '<option value="incomplete_form">نموذج غير مكتمل</option>' +
      '<option value="other">أخرى</option>' +
      '</select>' +
      '<textarea id="swal-details" class="swal2-textarea w-[80%] mx-auto text-sm" placeholder="تفاصيل سبب الإرجاع..."></textarea>',
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'إرجاع المعاملة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#d97706',
    preConfirm: () => {
      return {
        reason: (document.getElementById('swal-reason') as HTMLSelectElement).value,
        details: (document.getElementById('swal-details') as HTMLTextAreaElement).value
      }
    }
  })

  if (formValues) {
    try {
      await servicesStore.returnForm(form.value.id, {
        reason: formValues.reason,
        details: formValues.details,
        to_status: 'returned' // or back to 'draft' or initial stage
      })
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم إرجاع المعاملة', showConfirmButton: false, timer: 2000 })
      fetchFormDetails()
    } catch (err: any) {
      Swal.fire({ icon: 'error', title: 'خطأ', text: err.response?.data?.error || 'حدث خطأ' })
    }
  }
}

function getStatusLabel(status: string, stepName?: string) {
  if (status === 'in_progress') return `بانتظار: ${stepName || 'المراجعة'}`
  const map: any = {
    'draft': 'مسودة',
    'approved': 'معتمد نهائياً',
    'rejected': 'مرفوض',
    'returned': 'مُرجع للتعديل'
  }
  return map[status] || status
}

function getStatusColor(status: string) {
  const colors: any = {
    'draft': 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    'pending_services': 'bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400',
    'pending_hr': 'bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400',
    'pending_director': 'bg-purple-50 text-purple-700 dark:bg-purple-950/20 dark:text-purple-400',
    'approved': 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/20 dark:text-emerald-400',
    'rejected': 'bg-red-50 text-red-700 dark:bg-red-950/20 dark:text-red-400',
    'returned': 'bg-orange-50 text-orange-700 dark:bg-orange-950/20 dark:text-orange-400',
  }
  return colors[status] || 'bg-gray-100 text-gray-600'
}

function getStatusDot(status: string) {
  const dots: any = {
    'draft': 'bg-gray-400',
    'pending_services': 'bg-amber-500',
    'pending_hr': 'bg-blue-500',
    'pending_director': 'bg-purple-500',
    'approved': 'bg-emerald-500',
    'rejected': 'bg-red-500',
    'returned': 'bg-orange-500',
  }
  return dots[status] || 'bg-gray-400'
}
</script>
