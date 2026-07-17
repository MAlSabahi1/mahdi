<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8" dir="rtl">

    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-xl border border-gray-200">
      
      <div class="text-center">
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-brand-100 mb-4">
          <svg class="h-8 w-8 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900">
          طباعة الخدمة وإصدار المذكرات
        </h2>
        <p class="mt-2 text-sm text-gray-500">
          اختر كيف تريد التعامل مع طلب التصحيح (CORR-{{ String(correction?.id || '').padStart(5, '0') }})
        </p>
      </div>

      <div class="mt-8 space-y-4">
        
        <!-- الزر 1: إنشاء المذكرة في المنشئ الاحترافي -->
        <button @click="handleCreateMemo"
          class="group relative w-full flex justify-center py-4 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-gradient-to-r from-brand-600 to-brand-800 hover:from-brand-700 hover:to-brand-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-all shadow-lg overflow-hidden">
          <span class="absolute left-0 inset-y-0 flex items-center pl-3">
            <svg class="h-5 w-5 text-brand-300 group-hover:text-brand-200 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </span>
          الانتقال إلى مذكرة التغطية
        </button>

        <!-- الزر 2: طباعة الكشف (نموذج 23) -->
        <button @click="handlePrintList"
          class="group relative w-full flex justify-center py-4 px-4 border-2 border-emerald-500 text-sm font-bold rounded-xl text-emerald-700 bg-emerald-50 hover:bg-emerald-100 hover:border-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all shadow-sm">
          <span class="absolute left-0 inset-y-0 flex items-center pl-3">
            <svg class="h-5 w-5 text-emerald-500 group-hover:text-emerald-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
          </span>
          طباعة الكشف الرسمي (نموذج 23)
        </button>

        <!-- زر الرجوع -->
        <button @click="$router.back()"
          class="w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-all mt-4 shadow-theme-xs">
          إلغاء والعودة للخلف
        </button>
      </div>

    </div>

    <!-- iframe مخفي لطباعة الكشف -->
    <iframe 
      ref="listIframe" 
      class="hidden" 
      style="width:0;height:0;border:none;position:absolute;"
    ></iframe>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCorrectionStore } from '@/stores/correction'

const route = useRoute()
const router = useRouter()
const correctionStore = useCorrectionStore()

const id = route.params.id as string
const correction = ref<any>(null)
const loading = ref(true)
const error = ref('')
const listIframe = ref<HTMLIFrameElement | null>(null)

onMounted(async () => {
  if (!id) {
    error.value = 'رقم الكشف مفقود'
    loading.value = false
    return
  }
  try {
    correction.value = await correctionStore.fetchCorrectionById(id)
  } catch (e: any) {
    error.value = 'فشل تحميل بيانات الكشف'
  } finally {
    loading.value = false
  }
})

// === إنشاء المذكرة وربطها مع المنشئ الاحترافي ===
function handleCreateMemo() {
  if (!correction.value) return
  
  const corr = correction.value
  let target = '—'
  let rawNotes = corr.notes || corr.reason || ''
  let notes = rawNotes
  
  if (typeof rawNotes === 'string') {
    const targetMatch = rawNotes.match(/المطلوب تصحيح[هة]:\s*([\s\S]*?)(?=\s*المبررات:|$)/)
    if (targetMatch && targetMatch[1]) {
      target = targetMatch[1].trim()
    }
  }
  
  if (target === '—') {
    if (corr.field_name === 'full_name' || corr.correction_type === 'name_correction') target = 'تصحيح الاسم'
    else if (corr.field_name === 'national_id' || corr.correction_type === 'national_id_correction') target = 'تصحيح الرقم الوطني'
    else if (corr.field_name === 'military_number' || corr.correction_type === 'military_number_correction') target = 'تصحيح الرقم العسكري'
    else target = corr.field_name || corr.correction_type || 'تحديث بيانات'
  }

  // تجهيز بيانات الفرد
  
  let cleanedNotes = rawNotes;
  if (cleanedNotes.includes('المبررات:')) {
    cleanedNotes = cleanedNotes.split('المبررات:')[1].trim();
  } else if (cleanedNotes.includes('المطلوب تصحيحه:')) {
    cleanedNotes = cleanedNotes.split('المطلوب تصحيحه:')[0].trim() || cleanedNotes;
  }


  const personnel = [{
    militaryId: corr.military_number || corr.personnel_military_number || '',
    rank: corr.rank || corr.personnel_rank || '',
    name: corr.full_name || corr.personnel_name || corr.old_value || '',
    wrongName: corr.full_name || corr.personnel_name || corr.old_value || '',
    correctName: corr.new_value || corr.correct_name || '',
    correctionTarget: target,
    notes: cleanedNotes,
    nationalId: '', status: '', jobTitle: '', position: '', qualification: '', joinDate: '', workplace: '', serviceLocation: '', commencementDate: '', phone: '', clarification: '', secondaryNotes: ''
  }]

  // البحث عن القالب المحفوظ أو إنشاء مسودة جديدة
  let presets = []
  try {
    presets = JSON.parse(localStorage.getItem('memoTypographyPresets') || '[]')
  } catch (e) {}

  const TEMPLATE_NAME = 'قالب مذكرة تصحيح البيانات (افتراضي النظام)'
  let templateIndex = presets.findIndex((p: any) => p.name === TEMPLATE_NAME)
  let draft: any = {}

  if (templateIndex >= 0 && presets[templateIndex].fullTemplate) {
    // استخدام القالب المحفوظ مسبقاً
    draft = JSON.parse(JSON.stringify(presets[templateIndex].fullTemplate))
    draft.involvedPersonnel = personnel
    draft.referenceNo = 'CORR-' + String(corr.id).padStart(5, '0')
    draft.linkedForms = [{ id: corr.id, type: 'CORRECTION' }]
  } else {
    // مسودة افتراضية أولية
    draft = {
      documentType: 'CORRECTION',
      includeTable: false,
      subject: 'طلب تصحيح بيانات منتسب',
      referenceNo: 'CORR-' + String(corr.id).padStart(5, '0'),
      addressees: [
        { prefix: 'الأخ /', type: 'TEXT', entityId: null, name: 'المدير العام للمحافظة', suffix: 'المحترم' }
      ],
      involvedPersonnel: personnel,
      visibleColumns: {
        militaryId: true, rank: true, name: true, correctName: true, correctionTarget: true,
        nationalId: false, status: false, jobTitle: false, position: false, qualification: false, joinDate: false, workplace: false, serviceLocation: false, commencementDate: false, phone: false, clarification: false, notes: false, wrongName: false
      },
      body: `<p style="text-align: justify;">نحيط سيادتكم علماً بأنه ورد إلينا طلب تصحيح بيانات للمنتسب الموضح أدناه.</p>`,
      conclusion: `<p style="text-align: justify;">نرفق لكم الأوليات والمرفقات الثبوتية مع <strong>(كشف المطابقة — نموذج 23)</strong> للمطابقة، وذلك لاتخاذ الإجراءات اللازمة بحسب النظام والمصادقة على التصحيح المطلوب.</p>`,
      signatures: [
        { 
          title: 'مدير إدارة القوى البشرية', 
          rank: '', name: '', showSeal: false, 
          freeText: '<p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 14px; color: #1a202c;"><strong>الرتبة /</strong></span></p><p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 14px; color: #1a202c;"><strong>الاسم /</strong></span></p><p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 16px; color: #000000;"><strong>مدير إدارة القوى البشرية</strong></span></p><p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 12px; color: #4a5568;">التوقيع /</span></p>' 
        },
        { 
          title: 'المدير العام لإدارة أمن مأرب', 
          rank: '', name: '', showSeal: true, 
          freeText: '<p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 14px; color: #1a202c;"><strong>الرتبة /</strong></span></p><p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 14px; color: #1a202c;"><strong>الاسم /</strong></span></p><p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 16px; color: #000000;"><strong>المدير العام لإدارة أمن مأرب</strong></span></p><p class="text-align-center"><span style="font-family:\'Arial\', sans-serif; font-size: 12px; color: #4a5568;">التوقيع /</span></p>' 
        }
      ],
      signatureSettings: { showFrame: false, showLabels: false },
      linkedForms: [{ id: corr.id, type: 'CORRECTION' }]
    }
    
    // إنشاء القالب الافتراضي في النظام
    presets.push({
      name: TEMPLATE_NAME,
      fullTemplate: JSON.parse(JSON.stringify(draft))
    })
    templateIndex = presets.length - 1
    localStorage.setItem('memoTypographyPresets', JSON.stringify(presets))
  }

  // حفظ مسار التعديل
  localStorage.setItem('official_memo_edit_index', templateIndex.toString())
  localStorage.setItem('official_memo_draft', JSON.stringify(draft))
  router.push('/admin/documents/memo-builder')
}

// === طباعة الكشف عبر iframe ===
function handlePrintList() {
  const iframe = listIframe.value
  if (!iframe) return

  iframe.src = '/reports/view/23'
  
  iframe.onload = () => {
    setTimeout(() => {
      try {
        iframe.contentWindow?.print()
      } catch (e) {
        window.open('/reports/view/23', '_blank')
      }
    }, 1500)
  }
}
</script>
