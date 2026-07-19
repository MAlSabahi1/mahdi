<template>
  <div class="min-h-screen bg-gray-100 print:bg-white" dir="rtl">

    <!-- شريط الأدوات (لا يُطبع) -->
    <div class="print:hidden sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm px-6 py-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="$router.back()" class="flex items-center gap-2 text-sm font-bold text-gray-600 hover:text-gray-900 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
          العودة للمعاملة
        </button>
        <span class="text-gray-300">|</span>
        <h1 class="text-sm font-black text-gray-900">معاينة الطباعة الرسمية</h1>
        <span v-if="form" class="text-xs font-mono text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
          TX-{{ String(form.id).padStart(6, '0') }}
        </span>
      </div>
      <div class="flex items-center gap-2">
        <span v-if="form?.is_printed" class="flex items-center gap-1.5 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
          تمت الطباعة مسبقاً
        </span>
        
        <label class="flex items-center gap-2 text-sm font-bold text-gray-700 cursor-pointer bg-gray-50 border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-100 transition-colors">
          <input type="checkbox" v-model="printWithAttachments" class="w-4 h-4 text-brand-600 rounded border-gray-300 focus:ring-brand-500">
          طباعة المرفقات
        </label>
        <button @click="handlePrint"
          class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold px-5 py-2 rounded-lg transition-all shadow-md shadow-blue-500/20">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
          </svg>
          طباعة الاستمارة
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-32 print:hidden">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
      <p class="text-gray-500 text-sm font-medium">جاري تحميل الاستمارة...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error || !form" class="max-w-lg mx-auto mt-20 p-8 bg-red-50 border border-red-200 rounded-2xl text-center print:hidden">
      <svg class="w-12 h-12 mx-auto text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
      </svg>
      <p class="font-bold text-red-700">{{ error || 'لم يتم العثور على بيانات المعاملة' }}</p>
      <button @click="$router.back()" class="mt-4 text-sm text-red-600 underline">العودة</button>
    </div>

    <!-- نموذج الطباعة والمرفقات -->
    <div v-else class="print-bundle-container" id="print-area">
      <!-- الاستمارة -->
      <div class="max-w-[21cm] mx-auto my-6 print:my-0 shadow-xl print:shadow-none form-page-container">
        <StatusChangePrintForm :form="form" />
      </div>

      <!-- المرفقات -->
      <template v-if="printWithAttachments && form.attachments && form.attachments.length > 0">
        <div v-for="(att, aIdx) in form.attachments" :key="'att-'+aIdx" class="max-w-[21cm] min-h-[29.7cm] mx-auto my-6 print:my-0 bg-white shadow-xl print:shadow-none relative overflow-hidden flex flex-col justify-center items-center print-page-break p-8">
          <!-- Header for attachment context -->
          <div class="w-full flex justify-between items-center mb-4 pb-2 border-b border-gray-300 font-cairo text-sm text-gray-700">
            <div>
              <span class="text-gray-500">نوع الوثيقة:</span>
              <span class="mr-1 font-bold">{{ translateAttachmentType(att) }}</span>
            </div>
            <div>
              <span class="text-gray-500">تخص الموظف:</span>
              <span class="mr-1 font-bold">{{ form.personnel?.full_name || form.full_name || 'غير محدد' }}</span>
            </div>
          </div>
          
          <template v-if="!resolveAttachmentUrl(att).toLowerCase().endsWith('.pdf')">
            <img v-show="!att._imageError" :src="resolveAttachmentUrl(att)" @error="att._imageError = resolveAttachmentUrl(att)" class="max-w-full max-h-[90%] object-contain rounded-lg shadow-sm" alt="مرفق" />
            <div v-if="att._imageError" class="text-center p-8 bg-red-50 border-2 border-red-200 border-dashed rounded-xl w-full max-w-2xl mt-4">
              <p class="font-bold text-red-700 text-lg mb-2">فشل تحميل الصورة</p>
              <p class="text-gray-700 text-sm dir-ltr font-mono bg-white p-2 border rounded shadow-inner break-all">{{ att._imageError }}</p>
            </div>
          </template>
          <template v-else>
            <div class="text-center p-10 border-2 border-dashed border-gray-400 bg-gray-50 rounded-xl my-auto w-full max-w-2xl">
              <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
              </svg>
              <p class="font-bold text-gray-800 text-2xl mb-2">هذا المرفق بصيغة PDF</p>
              <p class="text-gray-600 text-lg mb-4">النظام لا يمكنه دمج ملفات PDF داخل حزمة الطباعة المباشرة.</p>
              <a :href="resolveAttachmentUrl(att)" target="_blank" class="text-brand-600 font-bold underline text-lg">اضغط هنا لفتح وطباعة المرفق بشكل مستقل</a>
            </div>
          </template>
          
          <!-- Footer for attachment context -->
          <div class="w-full text-center mt-auto pt-4 text-xs text-gray-500 font-mono tracking-wider">
            REF: ATT-{{ form.id }}-{{ aIdx }} | {{ new Date().toLocaleString('en-GB') }}
          </div>
        </div>
      </template>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import StatusChangePrintForm from './StatusChangePrintForm.vue'
import { useServicesStore } from '@/stores/services'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()

const id = route.params.id as string
const form = ref<any>(null)
const loading = ref(true)
const error = ref('')
const printWithAttachments = ref(true)

onMounted(async () => {
  if (!id) {
    error.value = 'رقم المعاملة مفقود'
    loading.value = false
    return
  }
  try {
    form.value = await servicesStore.fetchFormById(id)
  } catch (e: any) {
    error.value = 'فشل تحميل بيانات المعاملة'
  } finally {
    loading.value = false
  }
})

function translateAttachmentType(att: any) {
  const key = att.document_type_display || att.document_type || att.label || att.name || att.title || ''
  if (!key) return 'مرفق إضافي'
  const normalizedKey = String(key).toLowerCase().trim()
  const map: Record<string, string> = {
    attorney_id: 'هوية الوكيل',
    power_of_attorney: 'وكالة شرعية',
    legal_power_of_attorney: 'وكالة شرعية',
    'legal power of attorney': 'وكالة شرعية',
    photo: 'صورة شخصية',
    id_card: 'هوية شخصية',
    birth_certificate: 'شهادة ميلاد',
    death_certificate: 'شهادة وفاة',
    medical_report: 'تقرير طبي',
    'national id front': 'الوجه الأمامي للهوية الوطنية',
    'national_id_front': 'الوجه الأمامي للهوية الوطنية',
    'national id back': 'الوجه الخلفي للهوية الوطنية',
    'national_id_back': 'الوجه الخلفي للهوية الوطنية',
    memo: 'مذكرة',
    court_ruling: 'حكم محكمة',
    'court ruling': 'حكم محكمة',
    appointment_ruling: 'حكم تنصيب',
    'appointment ruling': 'حكم تنصيب',
    heir_ruling: 'انحصار ورثة',
    'heir ruling': 'انحصار ورثة',
    order_copy: 'نسخة من أمر التكليف',
    'order copy': 'نسخة من أمر التكليف',
    assignment_order: 'أمر التكليف',
    'assignment order': 'أمر التكليف',
    operations_report: 'بلاغ العمليات',
    'operations report': 'بلاغ العمليات',
    study_order: 'نسخة من أمر التفرغ الدراسي',
    'study order': 'نسخة من أمر التفرغ الدراسي',
    certified_id: 'نسخة من البطاقة العسكرية/الشخصية',
    'certified id': 'نسخة من البطاقة العسكرية/الشخصية',
    personal_request: 'الطلب الشخصي',
    'personal request': 'الطلب الشخصي',
    approval_document: 'مذكرة الاعتماد',
    'approval document': 'مذكرة الاعتماد',
    ministry_approval: 'موافقة الوزارة',
    'ministry approval': 'موافقة الوزارة',
    agent_id: 'هوية الوكيل',
    'agent id': 'هوية الوكيل',
    personnel_id: 'صورة الهوية',
    'personnel id': 'صورة الهوية',
    secondment_order: 'نسخة من الأمر',
    'secondment order': 'نسخة من الأمر',
    ruling_copy: 'نسخة من الحكم',
    'ruling copy': 'نسخة من الحكم',
    legal_ruling: 'حكم شرعي بالفقدان',
    'legal ruling': 'حكم شرعي بالفقدان',
    newspaper_ad: 'إعلان الجريدة',
    'newspaper ad': 'إعلان الجريدة',
    original_medical_decision: 'القرار الطبي الأصل',
    recent_photo: 'صورة حديثة'
  }
  return map[normalizedKey] || String(key).replace(/_/g, ' ')
}

function resolveAttachmentUrl(att: any) {
  let url = att.file || att.file_url || att.url || att.document_path || ''
  if (!url) return ''
  
  // Fix Docker internal hostnames resolving to broken images in browser
  if (url.startsWith('http://backend:') || url.startsWith('http://api:')) {
    try {
      const urlObj = new URL(url)
      url = `http://127.0.0.1:8000${urlObj.pathname}${urlObj.search}`
    } catch(e) {}
  }
  
  if (url.startsWith('http')) return url
  
  // إذا كان المسار خاماً قادماً من قاعدة البيانات ولا يحتوي على /media/ (مثل documents/2026/...)
  if (!url.startsWith('/media') && !url.startsWith('/api') && !url.startsWith('/')) {
    url = '/media/' + url
  } else if (url.startsWith('/') && !url.startsWith('/media') && !url.startsWith('/api')) {
    url = '/media' + url
  }
  
  if (!url.startsWith('/')) url = '/' + url
  
  const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'
  const baseUrl = apiUrl.split('/api')[0] || 'http://127.0.0.1:8000'
  return `${baseUrl}${url}`
}

async function handlePrint() {
  if (!form.value) return
  try {
    await servicesStore.markFormPrinted(form.value.id)
    form.value.is_printed = true
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تسجيل الطباعة', showConfirmButton: false, timer: 1500 })
  } catch (_) {
    // continue even if API fails
  }
  setTimeout(() => window.print(), 300)
}
</script>

<style>
@media print {
  @page {
    size: A4 portrait;
    margin: 0;
  }
  
  .print-page-break {
    page-break-before: always;
    break-before: page;
  }
  
  .form-page-container {
    width: 21cm !important;
    min-height: 29.7cm !important;
    background: white;
  }
}
</style>
