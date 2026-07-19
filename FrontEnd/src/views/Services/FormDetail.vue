<template>
  <admin-layout>
    <div class="print:hidden mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <h1 class="text-3xl font-black text-gray-800 tracking-tight flex items-center gap-3">
        ملف المعاملة 
        <span class="text-gray-500 font-mono text-2xl">#{{ form?.id || '' }}</span>
      </h1>
      
      <!-- Action Buttons - Formal Style -->
      <div v-if="form" class="flex flex-wrap gap-2">
        <button @click="printForm"
          class="bg-white text-gray-800 border border-gray-300 hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-200 dark:hover:bg-gray-700 font-bold px-5 py-2 rounded-sm transition-all text-sm shadow-sm flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
          طباعة الاستمارة
        </button>

        <button v-if="form.is_external && form.is_printed && !form.ministry_approval_doc_id && canApprove"
          @click="() => promptMinistryDoc()"
          class="bg-gray-800 hover:bg-black text-white font-bold px-5 py-2 rounded-sm transition-all text-sm shadow-sm flex items-center gap-2">
          رفع مستند الوزارة
        </button>

        <button v-if="canApprove" @click="rejectForm"
          class="bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 font-bold px-5 py-2 rounded-sm transition-all text-sm shadow-sm flex items-center gap-2">
          رفض
        </button>

        <button v-if="canApprove" @click="returnFormModal"
          class="bg-amber-50 text-amber-700 border border-amber-200 hover:bg-amber-100 font-bold px-5 py-2 rounded-sm transition-all text-sm shadow-sm flex items-center gap-2">
          إرجاع للتعديل
        </button>

        <button v-if="canApprove"
          @click="approveForm()"
          :disabled="form.is_external && (!form.is_printed || !form.ministry_approval_doc_id)"
          class="bg-emerald-700 hover:bg-emerald-800 disabled:bg-gray-400 text-white font-bold px-8 py-2 rounded-sm transition-all shadow-sm text-sm flex items-center gap-2">
          اعتماد الطلب
        </button>

        <button v-if="form && form.status === 'draft'" @click="submitDraft"
          class="bg-blue-700 hover:bg-blue-800 text-white font-bold px-8 py-2 rounded-sm transition-all shadow-sm text-sm flex items-center gap-2">
          تقديم الطلب النهائي
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-20 print:hidden">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-800"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error || !form" class="bg-red-50 border border-red-200 text-red-700 p-6 text-center font-bold print:hidden">
      {{ error || 'لم يتم العثور على تفاصيل هذه المعاملة.' }}
    </div>

    <!-- Main Content: Formal Layout -->
    <div v-else class="space-y-6 text-start" dir="rtl">
      
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 print:block print:w-full">
        <!-- Main Document Area (3/4 width) -->
        <div class="lg:col-span-3 space-y-6 print:w-full print:block">
          
          <!-- Structured Document Container -->
          <div class="bg-white dark:bg-gray-900 border-2 border-gray-300 dark:border-gray-700 shadow-sm print:border-none print:shadow-none p-8">
            <!-- Document Header -->
            <div class="border-b-2 border-gray-800 dark:border-gray-600 pb-4 mb-6 flex justify-between items-end">
              <div>
                <h2 class="text-2xl font-black text-gray-900 dark:text-white uppercase mb-1">
                  {{ (form.form_type_display || form.form_type || '').replace('returned_to_service', 'عائد للخدمة') }}
                </h2>
                <p class="text-sm font-bold text-gray-500">
                  تاريخ الإنشاء: {{ new Date(form.submitted_at || form.created_at).toLocaleString('en-GB') }}
                </p>
              </div>
              <div class="text-left">
                <div class="inline-block border-2 border-gray-800 dark:border-gray-600 px-4 py-2 font-bold text-sm bg-gray-50 dark:bg-gray-800">
                  الحالة: <span :class="getStatusTextColor(form.status)">{{ getStatusLabel(form.status, form.current_step_name) }}</span>
                </div>
              </div>
            </div>

            <!-- Personnel Details -->
            <div class="mb-8">
              <h3 class="text-lg font-black bg-gray-100 dark:bg-gray-800 border-y border-gray-300 dark:border-gray-600 px-4 py-2 mb-4">أولاً: بيانات مقدم الطلب</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-px bg-gray-300 dark:bg-gray-600 border border-gray-300 dark:border-gray-600">
                <div v-for="(detail, index) in personnelDetails" :key="index" class="bg-white dark:bg-gray-900 p-3">
                  <span class="block text-xs font-bold text-gray-500 mb-1">{{ detail.label }}</span>
                  <span class="block text-sm font-black text-gray-900 dark:text-gray-100" :class="{'font-mono': detail.isMono}">{{ detail.value || '—' }}</span>
                </div>
              </div>
              <div class="mt-2 text-left print:hidden">
                <RouterLink v-if="form.personnel?.military_number || form.personnel_military_number"
                  :to="`/personnel/${form.personnel?.military_number || form.personnel_military_number}`"
                  class="text-xs font-bold text-blue-700 hover:underline">
                  >> عرض الملف العسكري الشامل
                </RouterLink>
              </div>
            </div>

            <!-- Form Specific Details (The real info) -->
            <div class="mb-8">
              <h3 class="text-lg font-black bg-gray-100 dark:bg-gray-800 border-y border-gray-300 dark:border-gray-600 px-4 py-2 mb-4">ثانياً: البيانات المدخلة في الاستمارة</h3>
              
              <!-- Use actual form_data, unfiltered except for truly empty object -->
              <div v-if="form.form_data && Object.keys(form.form_data).length > 0" class="border border-gray-300 dark:border-gray-600">
                <table class="w-full text-right text-sm">
                  <tbody class="divide-y divide-gray-300 dark:divide-gray-600">
                    <tr v-for="(value, key) in form.form_data" :key="String(key)" 
                        class="bg-white hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800/50 transition-colors border-b border-gray-200 dark:border-gray-700">
                      <td class="w-1/3 px-4 py-3 text-xs font-bold text-gray-700 dark:text-gray-300 border-l border-gray-300 dark:border-gray-600 align-top bg-gray-100 dark:bg-gray-800 w-48">
                        {{ translateField(String(key)) }}
                      </td>
                      <td class="px-4 py-3 text-sm font-bold text-gray-900 dark:text-gray-100">
                        {{ formatFieldValue(String(key), value) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-sm font-bold text-gray-500 bg-gray-50 p-6 text-center border border-gray-300">
                لا توجد بيانات إضافية مدخلة في هذه الاستمارة.
              </div>
            </div>

            <!-- Notes & Rejections -->
            <div v-if="form.notes || form.rejection_reason" class="mb-8">
              <h3 class="text-lg font-black bg-gray-100 dark:bg-gray-800 border-y border-gray-300 dark:border-gray-600 px-4 py-2 mb-4">ثالثاً: الملاحظات والقرارات</h3>
              <div class="space-y-4">
                <div v-if="form.notes" class="border-2 border-blue-200 bg-blue-50 p-4">
                  <p class="text-xs font-black uppercase text-blue-800 mb-1">ملاحظات الطلب الأساسية:</p>
                  <p class="font-bold text-sm text-gray-900">{{ form.notes }}</p>
                </div>
                <div v-if="form.rejection_reason" class="border-2 border-red-200 bg-red-50 p-4">
                  <p class="text-xs font-black uppercase text-red-800 mb-1">سبب الرفض / الإرجاع:</p>
                  <p class="font-bold text-sm text-gray-900">{{ form.rejection_reason }}</p>
                </div>
              </div>
            </div>

            <!-- Attachments Summary -->
            <div class="mb-8 print:hidden">
              <h3 class="text-lg font-black bg-gray-100 dark:bg-gray-800 border-y border-gray-300 dark:border-gray-600 px-4 py-2 mb-4">رابعاً: الوثائق والمرفقات</h3>
              <div v-if="form.attachments && form.attachments.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="att in form.attachments" :key="att.id" class="flex items-center justify-between p-3 border border-gray-300 bg-gray-50 hover:bg-gray-100">
                  <div class="flex items-center gap-3">
                    <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/></svg>
                    <div>
                      <p class="text-sm font-bold text-gray-900">{{ translateField(att.document_type || 'مستند مرفق') }}</p>
                    </div>
                  </div>
                  <a :href="att.file" target="_blank" class="text-xs font-bold text-gray-700 bg-white border border-gray-300 px-3 py-1.5 hover:bg-gray-200">
                    استعراض الملف
                  </a>
                </div>
              </div>
              <div v-else class="text-sm font-bold text-gray-500 border border-gray-300 p-4 text-center bg-gray-50">
                لا توجد مرفقات.
              </div>
            </div>

            <ReportFooter />
          </div>
        </div>

        <!-- Sidebar Area (1/4 width) -->
        <div class="space-y-6 print:hidden">
          
          <!-- Workflow Progress -->
          <div class="bg-white border border-gray-300 shadow-sm p-5">
            <h3 class="text-sm font-black border-b-2 border-gray-800 pb-2 mb-4">مسار سير العمل</h3>
            <WorkflowProgressBar
              :steps="form.all_steps || []"
              :current-step-index="form.current_step_index ?? -1"
              :status="form.status"
              :is-external="!!form.is_external"
              :is-printed="!!form.is_printed"
              :has-ministry-doc="!!form.ministry_approval_doc_id"
              :rejection-reason="form.rejection_reason"
            />
          </div>

          <!-- History Timeline -->
          <div class="bg-white border border-gray-300 shadow-sm p-5">
            <h3 class="text-sm font-black border-b-2 border-gray-800 pb-2 mb-4">سجل الحركات</h3>
            <div class="relative pl-2 pr-4 space-y-6">
              <div class="absolute right-[11px] top-2 bottom-2 w-px bg-gray-200"></div>
              <div v-for="event in timeline" :key="event.id" class="relative flex items-start gap-4 pr-5 text-right">
                <span class="absolute right-[-4px] top-1.5 h-3 w-3 rounded-full border-2 border-white z-10"
                      :class="{
                        'bg-emerald-500': event.action === 'approved', 
                        'bg-blue-500': event.action === 'submitted', 
                        'bg-red-500': event.action === 'rejected', 
                        'bg-amber-500': event.action === 'returned', 
                        'bg-gray-400': !['approved', 'submitted', 'rejected', 'returned'].includes(event.action)
                      }"></span>
                <div class="w-full">
                  <p class="text-xs font-black text-gray-900" :class="{
                    'text-emerald-700': event.action === 'approved', 
                    'text-blue-700': event.action === 'submitted',
                    'text-red-700': event.action === 'rejected',
                    'text-amber-700': event.action === 'returned'
                  }">{{ event.action_display || event.action }}</p>
                  <p class="text-[10px] text-gray-500 mb-1.5 font-mono">{{ new Date(event.created_at).toLocaleString('en-GB') }} | <span class="font-bold font-sans text-gray-700">{{ event.performed_by_name || 'النظام التلقائي' }}</span></p>
                  <div v-if="event.notes" class="text-[11px] font-bold text-gray-800 bg-gray-50 p-2.5 border-r-2 mt-1 leading-relaxed"
                       :class="{
                         'border-emerald-300': event.action === 'approved',
                         'border-blue-300': event.action === 'submitted',
                         'border-red-300': event.action === 'rejected',
                         'border-amber-300': event.action === 'returned',
                         'border-gray-300': !['approved', 'submitted', 'rejected', 'returned'].includes(event.action)
                       }">
                    {{ formatEventNote(event.notes) }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Requirements Checklist -->
          <div v-if="checklist.length > 0" class="bg-white border border-gray-300 shadow-sm p-5">
            <h3 class="text-sm font-black border-b-2 border-gray-800 pb-2 mb-4">متطلبات المرحلة</h3>
            <div class="space-y-2">
              <label v-for="item in checklist" :key="item.id" class="flex items-start gap-3 p-2 bg-gray-50 border border-gray-200 cursor-pointer hover:bg-gray-100">
                <input type="checkbox" :checked="item.is_checked" @change="toggleChecklist(item)" class="mt-1 border-gray-400 text-gray-800 focus:ring-gray-800" />
                <span class="text-xs font-bold text-gray-800" :class="{ 'line-through text-gray-400': item.is_checked }">
                  {{ item.title }} <span v-if="item.is_required" class="text-red-600">*</span>
                </span>
              </label>
            </div>
          </div>

          <!-- Internal Chat -->
          <div class="bg-white border border-gray-300 shadow-sm flex flex-col h-[400px]">
            <div class="p-4 border-b border-gray-200">
              <h3 class="text-sm font-black">المراسلات الداخلية</h3>
            </div>
            <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
              <div v-if="notes.length === 0" class="text-center text-xs text-gray-500 mt-10">
                لا توجد مراسلات.
              </div>
              <div v-for="note in notes" :key="note.id" class="bg-white p-3 border border-gray-200 shadow-sm">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-[10px] font-bold text-gray-800">{{ note.created_by_name }}</span>
                  <span class="text-[9px] text-gray-500 font-mono">{{ new Date(note.created_at).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) }}</span>
                </div>
                <p class="text-xs text-gray-900">{{ note.content }}</p>
              </div>
            </div>
            <div class="p-3 border-t border-gray-200 bg-white flex gap-2">
              <input v-model="newNote" type="text" placeholder="اكتب ملاحظة..." class="flex-1 border border-gray-300 px-2 py-1.5 text-xs focus:ring-gray-800 focus:border-gray-800" @keyup.enter="submitNote" />
              <button @click="submitNote" :disabled="!newNote.trim()" class="bg-gray-800 text-white px-3 py-1.5 text-xs font-bold disabled:opacity-50">إرسال</button>
            </div>
          </div>

        </div>
      </div>
    </div>
    
    <!-- Print Only Attachments Section -->
    <div class="hidden print:block w-full" v-if="form?.attachments?.length">
      <div v-for="(att, idx) in form.attachments" :key="'print-att-'+att.id" style="page-break-before: always; padding-top: 2cm;">
        <h3 class="text-xl font-bold text-center mb-6 text-gray-900 border-b-2 border-gray-800 pb-2 inline-block">
          مرفق ({{ Number(idx) + 1 }}): {{ translateField(att.document_type || 'مستند') }}
        </h3>
        <div class="flex justify-center w-full">
          <img v-if="att.file && !att.file.endsWith('.pdf')" :src="att.file" class="max-w-full max-h-[25cm] border border-gray-400 p-2 shadow-sm" alt="Attachment">
          <div v-else class="text-center p-10 border-2 border-dashed border-gray-400">
            <p class="font-bold text-gray-800 text-lg">هذا المرفق بصيغة PDF</p>
            <p class="text-sm text-gray-600">يرجى طباعته بشكل مستقل من النظام.</p>
            <p class="text-xs mt-4 font-mono">{{ att.file }}</p>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'
import WorkflowProgressBar from '@/components/services/WorkflowProgressBar.vue'
import { useServicesStore } from '@/stores/services'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()
const authStore = useAuthStore()

const id = route.params.id as string
const form = ref<any>(null)
const loading = ref(true)
const error = ref('')

const timeline = ref<any[]>([])
const notes = ref<any[]>([])
const checklist = ref<any[]>([])
const newNote = ref('')

// Dictionary to translate raw database keys to official Arabic terms
const fieldTranslations: Record<string, string> = {
  rank: 'الرتبة',
  unit: 'الوحدة / اللواء',
  company: 'السرية / الكتيبة',
  category: 'التصنيف',
  full_name: 'الاسم الكامل',
  'full name': 'الاسم الكامل',
  id_issuer: 'جهة إصدار الهوية',
  'id issuer': 'جهة إصدار الهوية',
  birth_place: 'محل الميلاد',
  'birth place': 'محل الميلاد',
  national_id: 'الرقم الوطني / الهوية',
  'national id': 'الرقم الوطني / الهوية',
  id_issue_date: 'تاريخ إصدار الهوية',
  'id issue date': 'تاريخ إصدار الهوية',
  martyrdom_date: 'تاريخ الاستشهاد',
  'martyrdom date': 'تاريخ الاستشهاد',
  martyrdom_cause: 'سبب الاستشهاد',
  'martyrdom cause': 'سبب الاستشهاد',
  military_number: 'الرقم العسكري',
  'military number': 'الرقم العسكري',
  current_residence: 'مقر السكن الحالي',
  'current residence': 'مقر السكن الحالي',
  martyrdom_location: 'مكان الاستشهاد / الجبهة',
  'martyrdom location': 'مكان الاستشهاد / الجبهة',
  occurrence_context: 'سياق الواقعة',
  'occurrence context': 'سياق الواقعة',
  assignment_order: 'أمر التكليف',
  'assignment order': 'أمر التكليف',
  operations_report: 'بلاغ العمليات',
  'operations report': 'بلاغ العمليات',
  appointment_ruling: 'حكم تنصيب',
  attorney_id: 'هوية الوكيل',
  national_id_front: 'صورة الهوية الوطنية (وجه)',
  power_of_attorney: 'وكالة شرعية',
  heir_ruling: 'انحصار ورثة',
  death_certificate: 'شهادة وفاة',
  // New translations added for missing form data
  'end date': 'تاريخ الانتهاء',
  end_date: 'تاريخ الانتهاء',
  'start date': 'تاريخ البدء',
  start_date: 'تاريخ البدء',
  'order source': 'جهة التكليف',
  order_source: 'جهة التكليف',
  'dignitary name': 'اسم الشخصية',
  dignitary_name: 'اسم الشخصية',
  'dignitary position': 'منصب الشخصية',
  dignitary_position: 'منصب الشخصية',
  'certified id': 'هوية معتمدة',
  certified_id: 'هوية معتمدة'
}

function translateField(key: string) {
  const normalizedKey = String(key).toLowerCase()
  return fieldTranslations[normalizedKey] || String(key).replace(/_/g, ' ')
}

function formatFieldValue(key: string, value: any) {
  if (value === null || value === '' || value === undefined || value === '-') return '—'
  // Format standard date strings (YYYY-MM-DD)
  if (typeof value === 'string' && value.match(/^\d{4}-\d{2}-\d{2}$/)) {
    return new Date(value).toLocaleDateString('en-GB')
  }
  return value
}

const personnelDetails = computed(() => {
  if (!form.value) return []
  const p = form.value.personnel || {}
  
  const details = [
    { label: 'الاسم الرباعي', value: p.full_name || form.value.personnel_name },
    { label: 'الرقم العسكري', value: p.military_number || form.value.personnel_military_number, isMono: true },
    { label: 'الرتبة الحالية', value: p.rank || form.value.personnel_rank || p.rank_name || p.current_rank?.name },
  ]
  
  const qual = p.qualification_name || p.qualification_detail?.name
  if (qual && qual !== '—') details.push({ label: 'المؤهل العلمي', value: qual })
  
  if (p.expense_status_display && p.expense_status_display !== '—') {
    details.push({ label: 'حالة النفقات', value: p.expense_status_display })
  }
  
  if (form.value.effective_date) {
    details.push({ label: 'تاريخ النفاذ', value: new Date(form.value.effective_date).toLocaleDateString('en-GB'), isMono: true })
  }
  
  return details
})

function formatEventNote(note: string) {
  if (!note) return ''
  let cleaned = note
  // Clean up repetitive backend strings
  cleaned = cleaned.replace(/^[✓✅]\s*اعتماد(?: نهائي)?\s*(?:—\s*)?بواسطة:\s*[\w\d]+\s*(?:—|\.|-)?\s*/gi, '')
  cleaned = cleaned.replace(/^✓\s*اعتماد بواسطة:\s*[\w\d]+\s*—\s*/gi, '')
  cleaned = cleaned.replace(/^تمت طباعة الاستمارة بواسطة\s*[\w\d]+/gi, 'تمت طباعة الاستمارة بنجاح')
  cleaned = cleaned.replace(/^تم تقديم الطلب — /gi, 'تم تقديم الطلب: ')
  return cleaned
}

onMounted(async () => {
  if (!id) {
    error.value = 'رقم المعاملة مفقود.'
    loading.value = false
    return
  }
  await fetchFormDetails()
})

const canApprove = computed(() => {
  if (!form.value) return false
  const st = form.value.status
  if (st === 'approved' || st === 'rejected') return false
  if (authStore.isAdmin) return true
  const role = authStore.user?.authz_profile?.role_name || ''
  const roleCode = authStore.user?.authz_profile?.role_code || ''
  // الحالات القديمة — للتوافق
  if (st === 'pending_services' && (roleCode === 'services_dept' || role.includes('الخدمات'))) return true
  if (st === 'pending_hr' && (roleCode === 'hr_director' || role.includes('القوى البشرية') || role.includes('مدير إدارة'))) return true
  if (st === 'pending_director' && (roleCode === 'governor_general' || role.includes('المدير العام'))) return true
  // الحالة الجديدة in_progress — تعتمد على stage.code
  if (st === 'in_progress') {
    const stepCode = form.value.current_step_code || ''
    if (stepCode === 'services_dept' && (roleCode === 'services_dept' || role.includes('الخدمات'))) return true
    if (stepCode === 'hr_director' && (roleCode === 'hr_director' || role.includes('القوى') || role.includes('مدير إدارة'))) return true
    if (stepCode === 'governor_general' && (roleCode === 'governor_general' || role.includes('المدير العام'))) return true
  }
  return false
})

// Filter out empty form fields (null, undefined, "-", empty string)
const filteredFormData = computed(() => {
  if (!form.value?.form_data) return {}
  const filtered: Record<string, any> = {}
  for (const [key, value] of Object.entries(form.value.form_data)) {
    if (value !== null && value !== undefined && value !== '' && value !== '-') {
      filtered[key] = value
    }
  }
  return filtered
})

async function fetchFormDetails() {
  loading.value = true
  try {
    form.value = await servicesStore.fetchFormById(id)
    const [t, n, c] = await Promise.all([
      servicesStore.fetchFormTimeline(id),
      servicesStore.fetchFormNotes(id),
      servicesStore.fetchFormChecklist(id, form.value.status)
    ])
    timeline.value = t
    notes.value = n
    checklist.value = c
    
    if (route.query.print === 'true') {
      setTimeout(() => { window.print() }, 500)
    }
  } catch (err: any) {
    error.value = 'فشل جلب تفاصيل المعاملة. قد تكون محذوفة أو غير متوفرة.'
  } finally {
    loading.value = false
  }
}

async function printForm() {
  if (!form.value) return
  window.open(router.resolve(`/services/forms/${form.value.id}/print`).href, '_blank')
}
async function submitNote() {
  if (!newNote.value.trim()) return
  try {
    const note = await servicesStore.addFormNote(id, newNote.value)
    notes.value.unshift(note) // Add to top for chat style
    newNote.value = ''
    timeline.value = await servicesStore.fetchFormTimeline(id)
  } catch (err: any) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'فشل إرسال الرسالة', showConfirmButton: false, timer: 2000 })
  }
}

async function toggleChecklist(item: any) {
  try {
    item.is_checked = !item.is_checked
    await servicesStore.toggleChecklistItem(item.id, item.is_checked)
    timeline.value = await servicesStore.fetchFormTimeline(id)
  } catch (err: any) {
    item.is_checked = !item.is_checked
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'فشل التحديث', showConfirmButton: false, timer: 2000 })
  }
}

async function approveForm(ministryDocId?: number) {
  if (!form.value) return

  if (ministryDocId) {
    try {
      await servicesStore.approveForm(form.value.id, { ministry_document_id: ministryDocId })
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة بنجاح', showConfirmButton: false, timer: 2000 })
      fetchFormDetails()
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'حدث خطأ أثناء اعتماد المعاملة'
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
    return
  }

  Swal.fire({
    title: 'تأكيد الاعتماد؟',
    text: `سيتم الاعتماد وتمرير المعاملة للمرحلة التالية. هل أنت متأكد؟`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتمد المعاملة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#059669', // emerald-600
    reverseButtons: true
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await servicesStore.approveForm(form.value.id)
        Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة بنجاح', showConfirmButton: false, timer: 2000 })
        fetchFormDetails()
      } catch (err: any) {
        let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء اعتماد المعاملة'
        
        if (errorMsg.includes('يجب إرفاق مستند موافقة الوزارة') || errorMsg.includes('مستند موافقة')) {
          return promptMinistryDoc('ministry_document_id', 'تسجيل موافقة الوزارة', 'يجب إرفاق ملف القرار/المذكرة الوزارية.', 'ministry_approval')
        }
        
        if (errorMsg.includes('يجب إرفاق الاستمارة الموقعة')) {
          return promptMinistryDoc('signed_document_id', 'إرفاق الاستمارة الموقعة', 'يجب إرفاق الاستمارة الموقعة ورقياً من المدير العام.', 'signed_form')
        }

        if (err.response?.data && typeof err.response.data === 'object' && !err.response.data.error) {
          errorMsg = Object.values(err.response.data).flat().join('\n')
        }
        Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
      }
    }
  })
}

async function promptMinistryDoc(payloadKey = 'ministry_document_id', title = 'تسجيل موافقة الوزارة', subtitle = 'يجب إرفاق ملف القرار/المذكرة الوزارية.', docType = 'ministry_approval') {
  const result = await Swal.fire({
    title: title,
    html: `<div class="text-right" dir="rtl">
             <div id="swal-upload-wrapper" class="p-4 border border-dashed rounded-xl transition-colors border-gray-300 dark:border-gray-700 text-right">
               <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                 <div>
                   <p class="font-bold text-sm flex items-center gap-2 text-gray-900 dark:text-white">
                     المستند المرفق <span class="text-red-500">*</span>
                     <span id="swal-upload-badge" class="hidden text-emerald-600 text-[10px] bg-emerald-100 dark:bg-emerald-900/50 px-2 py-0.5 rounded font-bold border border-emerald-200 dark:border-emerald-800">✓ تم الرفع</span>
                   </p>
                   <p class="text-xs text-gray-400 mt-1">صيغ مدعومة: PDF, JPG, PNG (الحد الأقصى 5MB)</p>
                   <p id="swal-file-name" class="hidden text-xs text-emerald-600 mt-1.5 font-mono bg-white dark:bg-gray-900 inline-block px-2 py-1 rounded border border-emerald-100 dark:border-emerald-900/30"></p>
                 </div>
                 <div class="flex items-center gap-3 self-end sm:self-auto">
                   <label id="swal-upload-btn" for="ministry-doc" class="cursor-pointer bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 text-xs font-bold px-4 py-2.5 rounded-lg transition-colors shadow-sm">
                     اختيار ملف
                   </label>
                   <input id="ministry-doc" type="file" class="hidden" accept=".pdf,.jpg,.jpeg,.png" onchange="
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
      const fileInput = document.getElementById('ministry-doc') as HTMLInputElement
      if (!fileInput?.files?.length) { Swal.showValidationMessage('يجب اختيار ملف'); return false }
      const fd = new FormData()
      fd.append('file', fileInput.files[0])
      fd.append('document_type', docType)
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
     if (payloadKey === 'ministry_document_id') {
         approveForm(result.value)
     } else {
         // بالنسبة للمستند الداخلي
         try {
             await servicesStore.approveForm(form.value.id, { [payloadKey]: result.value })
             Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الاعتماد بنجاح', showConfirmButton: false, timer: 2000 })
             fetchFormDetails()
         } catch (err: any) {
             const errorMsg = err.response?.data?.error || 'حدث خطأ أثناء الاعتماد'
             Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
         }
     }
  }
}

async function submitDraft() {
  if (!form.value) return
  Swal.fire({
    title: 'تقديم الطلب',
    text: `هل أنت متأكد من تقديم هذا الطلب نهائياً وبدء دورة الاعتماد؟`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'نعم، قدم الطلب',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#2563eb',
    reverseButtons: true
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await api.post(`/service-cycle/forms/${form.value.id}/submit/`)
        Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تقديم الطلب بنجاح', showConfirmButton: false, timer: 2000 })
        fetchFormDetails()
      } catch (err: any) {
        Swal.fire({ icon: 'error', title: 'فشل التقديم', text: err.response?.data?.error || 'حدث خطأ أثناء التقديم' })
      }
    }
  })
}

async function rejectForm() {
  if (!form.value) return
  Swal.fire({
    title: 'رفض المعاملة نهائياً',
    text: `الرجاء كتابة سبب الرفض بوضوح:`,
    input: 'text',
    icon: 'error',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#dc2626', // red-600
    reverseButtons: true,
    inputValidator: (val) => !val ? 'يجب إدخال سبب الرفض!' : undefined
  }).then(async (result) => {
    if (result.isConfirmed && result.value) {
      try {
        await servicesStore.rejectForm(form.value.id, result.value)
        Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض المعاملة', showConfirmButton: false, timer: 2000 })
        fetchFormDetails()
      } catch (err: any) {
        let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء الرفض'
        if (err.response?.data && typeof err.response.data === 'object' && !err.response.data.error) {
          errorMsg = Object.values(err.response.data).flat().join('\n')
        }
        Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
      }
    }
  })
}

async function returnFormModal() {
  if (!form.value) return
  const { value: formValues } = await Swal.fire({
    title: 'إرجاع المعاملة للتعديل',
    html:
      '<div class="text-right space-y-4">' +
      '<div><label class="block text-sm font-bold mb-1">سبب الإرجاع الرئيسي:</label>' +
      '<select id="swal-reason" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none">' +
      '<option value="missing_attachments">نقص وثائق أو مرفقات داعمة</option>' +
      '<option value="incorrect_data">بيانات الاستمارة غير صحيحة أو متضاربة</option>' +
      '<option value="incomplete_form">متطلبات المعاملة غير مكتملة</option>' +
      '<option value="other">أسباب أخرى</option>' +
      '</select></div>' +
      '<div><label class="block text-sm font-bold mb-1">تفاصيل وملاحظات للمنشئ:</label>' +
      '<textarea id="swal-details" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none h-24" placeholder="اكتب الملاحظات بدقة ليقوم المنشئ بتعديلها..."></textarea></div>' +
      '</div>',
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'إرجاع المعاملة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#d97706', // amber-600
    reverseButtons: true,
    preConfirm: () => {
      const details = (document.getElementById('swal-details') as HTMLTextAreaElement).value
      if (!details) {
        Swal.showValidationMessage('الرجاء كتابة تفاصيل الملاحظات')
      }
      return {
        reason: (document.getElementById('swal-reason') as HTMLSelectElement).value,
        details: details
      }
    }
  })

  if (formValues) {
    try {
      await servicesStore.returnForm(form.value.id, {
        reason: formValues.reason,
        details: formValues.details,
        to_status: 'returned'
      })
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم إرجاع المعاملة للتعديل', showConfirmButton: false, timer: 2000 })
      fetchFormDetails()
    } catch (err: any) {
      let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء الإرجاع'
      if (err.response?.data && typeof err.response.data === 'object' && !err.response.data.error) {
        errorMsg = Object.values(err.response.data).flat().join('\n')
      }
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
  }
}

function getStatusLabel(status: string, stepName?: string) {
  const map: Record<string, string> = {
    'draft': 'مسودة',
    'approved': 'معتمد نهائياً',
    'rejected': 'مرفوض',
    'returned': 'مُرجع للتعديل',
    'pending_services': 'عند: رئيس قسم الخدمات',
    'pending_hr': 'عند: مدير إدارة القوى البشرية',
    'pending_director': 'عند: المدير العام للمحافظة',
    'in_progress': `عند: ${stepName || 'قيد الإجراء'}`,
  }
  return map[status] || status
}

function getStatusTextColor(status: string) {
  const colors: Record<string, string> = {
    'draft': 'text-gray-600 dark:text-gray-400',
    'pending_services': 'text-amber-600 dark:text-amber-400',
    'pending_hr': 'text-blue-600 dark:text-blue-400',
    'pending_director': 'text-purple-600 dark:text-purple-400',
    'in_progress': 'text-indigo-600 dark:text-indigo-400',
    'approved': 'text-emerald-600 dark:text-emerald-400',
    'rejected': 'text-red-600 dark:text-red-400',
    'returned': 'text-orange-600 dark:text-orange-400',
  }
  return colors[status] || 'text-gray-600'
}

function getStatusDot(status: string) {
  const dots: Record<string, string> = {
    'draft': 'bg-gray-400',
    'pending_services': 'bg-amber-500',
    'pending_hr': 'bg-blue-500',
    'pending_director': 'bg-purple-500',
    'in_progress': 'bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)]',
    'approved': 'bg-emerald-500',
    'rejected': 'bg-red-500',
    'returned': 'bg-orange-500',
  }
  return dots[status] || 'bg-gray-400'
}
</script>
