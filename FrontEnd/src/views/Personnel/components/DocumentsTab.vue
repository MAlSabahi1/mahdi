<template>
  <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4">
      <div>
        <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ $t('documents.title') }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ $t('documents.subtitle') }}</p>
      </div>
      <button 
        @click="showUploadModal = true"
        class="inline-flex items-center justify-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors"
      >
        <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        {{ $t('documents.upload_new') }}
      </button>
    </div>

    <!-- Documents Display -->
    <div v-if="person.documents && person.documents.length > 0">
      
      <!-- Timeline Events -->
      <div v-if="groupedDocuments.events.length > 0" class="mb-10">
        <div class="flex items-center gap-3 mb-6 border-b border-gray-100 pb-3 dark:border-gray-800">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h4 class="text-base font-bold text-gray-800 dark:text-gray-200">
            سجل الإجراءات والمرفقات المرتبطة
          </h4>
        </div>

        <div class="relative border-r-2 border-gray-100 dark:border-gray-800 pr-6 mr-4">
          <div v-for="(event, idx) in groupedDocuments.events" :key="idx" class="relative mb-8 last:mb-0">
            <!-- Timeline Node -->
            <div class="absolute -right-[33px] top-1 flex h-4 w-4 items-center justify-center rounded-full bg-white ring-4 ring-gray-50 dark:bg-gray-900 dark:ring-gray-800">
              <div class="h-2 w-2 rounded-full bg-brand-500 shadow-sm"></div>
            </div>
            
            <!-- Event Header -->
            <div class="mb-4 bg-gray-50/50 dark:bg-gray-800/30 rounded-xl p-3 border border-gray-100 dark:border-gray-800">
              <div class="flex flex-col gap-3">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div class="flex items-center gap-2 text-brand-700 dark:text-brand-400">
                    <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <h4 class="text-sm font-bold">{{ event.title }}</h4>
                  </div>
                  <div class="flex items-center gap-3 text-xs font-medium text-gray-500 bg-white dark:bg-gray-800 px-2.5 py-1 rounded-md shadow-theme-xs border border-gray-100 dark:border-gray-700">
                    <span class="flex items-center gap-1">
                      <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                      <span dir="ltr">{{ new Date(event.date).toLocaleDateString('ar-SA') }}</span>
                    </span>
                    <span class="text-gray-300 dark:text-gray-600">|</span>
                    <span class="flex items-center gap-1">
                      <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" /></svg>
                      <span>#{{ event.context_id }}</span>
                    </span>
                  </div>
                </div>

                <div class="flex flex-col gap-2" v-if="event.meta && Object.keys(event.meta).length > 0">
                  <div class="flex flex-wrap items-center gap-4 text-xs">
                    <div class="flex items-center gap-1.5 text-gray-600 dark:text-gray-400">
                      <span class="font-medium">المُنشئ:</span>
                      <span class="font-bold text-gray-900 dark:text-gray-200">{{ event.meta.submitted_by }}</span>
                    </div>
                    <div class="flex items-center gap-1.5 text-gray-600 dark:text-gray-400">
                      <span class="font-medium">حالة الطلب:</span>
                      <span class="font-bold text-gray-900 dark:text-gray-200">{{ event.meta.status }}</span>
                    </div>
                  </div>
                  
                  <div v-if="event.events && event.events.length > 0" class="mt-1 border-t border-gray-100 dark:border-gray-700/50 pt-2">
                    <details class="group">
                      <summary class="cursor-pointer text-xs font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400 flex items-center gap-1 list-none">
                        <svg class="h-3 w-3 transition-transform group-open:rotate-90" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
                        عرض مسار الموافقات ({{ event.events.length }} حركات)
                      </summary>
                      <div class="mt-2.5 flex flex-col gap-2 border-r-2 border-gray-200 dark:border-gray-700 pr-3 mr-1">
                        <div v-for="(ev, i) in event.events" :key="i" class="flex flex-col gap-0.5 text-[11px]">
                          <div class="flex items-center justify-between">
                            <span class="font-bold text-gray-800 dark:text-gray-200">{{ ev.performed_by }}</span>
                            <span class="text-gray-400" dir="ltr">{{ new Date(ev.date).toLocaleString('ar-SA', { hour12: true, month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</span>
                          </div>
                          <span class="text-gray-500 dark:text-gray-400">{{ ev.notes }}</span>
                        </div>
                      </div>
                    </details>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Event Documents -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <div v-for="doc in event.docs" :key="doc.id" class="group relative flex items-start gap-3 rounded-xl border border-gray-100 bg-white p-2.5 transition-all hover:border-brand-300 hover:shadow-theme-md dark:border-gray-800 dark:bg-gray-800/50 dark:hover:border-brand-700">
                
                <div class="h-16 w-16 shrink-0 rounded-lg overflow-hidden bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 flex items-center justify-center relative">
                  <img v-if="isImage(doc.file_url)" :src="getFullUrl(doc.file_url)" class="w-full h-full object-cover" alt="preview" />
                  <svg v-else class="h-6 w-6 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                  
                  <a :href="getFullUrl(doc.file_url)" target="_blank" class="absolute inset-0 bg-gray-900/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
                    <svg class="h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  </a>
                </div>

                <div class="flex-1 min-w-0 py-0.5">
                  <h4 class="truncate text-xs font-bold text-gray-900 dark:text-white" :title="getDocumentTypeTitle(doc.document_type_display)">{{ getDocumentTypeTitle(doc.document_type_display) }}</h4>
                  <p v-if="doc.description" class="mt-0.5 text-[11px] text-gray-500 dark:text-gray-400 line-clamp-2 leading-relaxed" :title="doc.description">{{ doc.description }}</p>
                  <p v-else class="mt-0.5 text-[11px] text-gray-400 dark:text-gray-500">بدون وصف إضافي</p>
                  <p v-if="doc.uploaded_by" class="mt-1 text-[10px] font-medium text-brand-600 dark:text-brand-400 flex items-center gap-1">
                    <svg class="h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                    مُرفق بواسطة: {{ doc.uploaded_by }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Basic Documents -->
      <div v-if="groupedDocuments.basic.length > 0">
        <h4 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-6 border-b border-gray-100 pb-2 dark:border-gray-800">
          الوثائق الأساسية والعامة
        </h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="doc in groupedDocuments.basic" :key="doc.id" class="group relative flex flex-col justify-between rounded-xl border border-gray-100 p-3 transition-all hover:border-brand-300 hover:shadow-theme-md dark:border-gray-800 dark:hover:border-brand-700 dark:bg-gray-800/50">
            
            <div class="w-full h-40 mb-3 rounded-lg overflow-hidden bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 flex items-center justify-center relative group-hover:border-brand-200 dark:group-hover:border-brand-600 transition-colors">
              <img v-if="isImage(doc.file_url)" :src="getFullUrl(doc.file_url)" class="w-full h-full object-cover" alt="preview" />
              <svg v-else class="h-10 w-10 text-gray-300 dark:text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
              
              <a :href="getFullUrl(doc.file_url)" target="_blank" class="absolute inset-0 bg-gray-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[2px]">
                <span class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white px-3 py-1.5 rounded-lg text-xs font-bold shadow-sm inline-flex items-center gap-1.5">
                  <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  {{ $t('documents.view') }}
                </span>
              </a>
            </div>

            <div class="flex-1 overflow-hidden text-center">
              <h4 class="truncate text-sm font-semibold text-gray-900 dark:text-white" :title="getDocumentTypeTitle(doc.document_type_display)">{{ getDocumentTypeTitle(doc.document_type_display) }}</h4>
              <p class="mt-1 truncate text-xs text-gray-500 dark:text-gray-400" dir="ltr" v-if="doc.description">{{ doc.description }}</p>
              <p class="mt-2 text-xs text-gray-400 dark:text-gray-500">{{ new Date(doc.created_at).toLocaleDateString('ar-SA') }}</p>
            </div>
          </div>
        </div>
      </div>
      
    </div>
    
    <div v-else class="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 py-12 text-center dark:border-gray-700">
      <div class="mb-4 rounded-full bg-gray-50 p-3 dark:bg-gray-800">
        <svg class="h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ $t('documents.no_documents') }}</p>
      <button @click="showUploadModal = true" class="mt-4 text-sm font-medium text-brand-600 hover:text-brand-500 dark:text-brand-400 dark:hover:text-brand-300">
        {{ $t('documents.upload_new') }}
      </button>
    </div>

    <!-- Modals -->
    <DocumentUploadModal 
      v-if="showUploadModal" 
      :person="person" 
      @close="showUploadModal = false"
      @uploaded="handleUploadSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import DocumentUploadModal from './DocumentUploadModal.vue'

const props = defineProps<{
  person: any
}>()

const emit = defineEmits(['update'])
const { t } = useI18n()

const showUploadModal = ref(false)

function getFullUrl(url: string) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  return `${baseUrl}${url}`
}

function isImage(url: string) {
  if (!url) return false
  const lowerUrl = url.toLowerCase()
  return lowerUrl.includes('.jpeg') || 
         lowerUrl.includes('.jpg') || 
         lowerUrl.includes('.gif') || 
         lowerUrl.includes('.png') || 
         lowerUrl.includes('.webp') || 
         lowerUrl.startsWith('blob:') || 
         lowerUrl.startsWith('data:image')
}

// ── Event Timeline Grouping ──
const groupedDocuments = computed(() => {
  const basic: any[] = []
  const events: Record<string, { title: string, date: string, context_id: string, docs: any[], meta: any, events: any[] }> = {}
  
  if (!props.person.documents) return { basic, events: [] }
  
  props.person.documents.forEach((doc: any) => {
    // If it lacks context or is marked general
    if (!doc.context_type || !doc.context_id || doc.context_type === 'General') {
      basic.push(doc)
    } else {
      const key = `${doc.context_type}_${doc.context_id}`
      if (!events[key]) {
        const meta = doc.context_meta || {}
        let cTitle = doc.context_title || getContextTitle(doc.context_type)
        
        // Force meaningful title for StatusChangeForm
        if (doc.context_type === 'StatusChangeForm' || cTitle.includes('إثبات حالة')) {
          if (meta.category && meta.category !== 'dynamic' && meta.category !== 'status_change') {
            const categoryMap: Record<string, string> = { 
              escort: 'مرافق / معيات', 
              martyr: 'شهيد', 
              death: 'وفاة طبيعية', 
              missing: 'مفقود', 
              desertion: 'فرار',
              retirement_age: 'بلوغ السن القانوني',
              medical_unfit: 'عدم لياقة صحية',
              end_of_service: 'إنهاء مدة',
              retired: 'محال للتقاعد',
              imprisoned: 'مسجون',
              study_leave: 'تفريغ دراسي',
              seconded: 'انتداب',
              returned_to_service: 'عائد للخدمة'
            }
            cTitle = `طلب إثبات حالة - ${categoryMap[meta.category.toLowerCase()] || meta.category}`
          } else {
             cTitle = 'طلب إجراء تغيير / إثبات حالة'
          }
        }
        
        events[key] = {
          title: cTitle,
          date: doc.created_at, // initial fallback date
          context_id: doc.context_id,
          meta: meta,
          events: doc.context_events || [],
          docs: []
        }
      }
      events[key].docs.push(doc)
    }
  })
  
  // Convert events dictionary to a sorted array (newest first)
  const sortedEvents = Object.values(events).sort((a, b) => {
    return new Date(b.date).getTime() - new Date(a.date).getTime()
  })
  
  return { basic, events: sortedEvents }
})

function getContextTitle(type: string) {
  const map: Record<string, string> = {
    'NationalIdUpdate': 'تعديل الرقم الوطني',
    'RankPromotion': 'قرار تسوية / ترقية رتبة',
    'PersonnelToOfficer': 'تسوية من فرد إلى ضابط',
    'NameCorrection': 'تصحيح الاسم أو اللقب',
    'StatusChange_Martyr': 'إثبات حالة: شهيد',
    'StatusChange_Missing': 'إثبات حالة: مفقود',
    'StatusChange_Death': 'إثبات حالة: وفاة طبيعية',
    'StatusChange_Desertion': 'إثبات حالة: فرار / غياب',
    'StatusChange_Retirement': 'إحالة على التقاعد',
    'Transfer': 'أمر نقل / تعديل إدارة',
    'ServiceRequest': 'إجراء خدمة (عام)',
    'SuggestedCorrection': 'طلب تصحيح بيانات',
    'StatusChangeForm': 'طلب إجراء تغيير / إثبات حالة',
    'RankSettlement': 'تسوية رتبة',
    'Retired': 'إحالة على التقاعد',
    'CorrectionRequestForm': 'نموذج طلب تصحيح',
    'UnifiedRequestForm': 'نموذج طلب موحد',
  }
  return map[type] || type
}

function getDocumentTypeTitle(type: string) {
  if (!type) return 'مستند غير معروف';
  const map: Record<string, string> = {
    'ministry_approval': 'موافقة الوزارة',
    'personal_attachment': 'مرفق شخصي',
    'appointment_ruling': 'قرار تعيين',
    'attorney_id': 'هوية الوكيل',
    'power_of_attorney': 'وكالة قانونية / شرعية',
    'heir_ruling': 'حصر إرث / فريضة',
    'certified_id': 'هوية مصدقة',
    'national_id_front': 'بطاقة وطنية - أمامي',
    'national_id_back': 'بطاقة وطنية - خلفي',
    'id_card': 'بطاقة هوية',
    'general_document': 'مستند عام',
    'medical_report': 'تقرير طبي',
    'operations_report': 'بلاغ عمليات',
    'police_report': 'بلاغ شرطة',
    'study_order': 'أمر دراسة / ابتعاث',
    'military_id': 'هوية عسكرية',
    'court_order': 'أمر قضائي / حكم',
    'service_certificate': 'شهادة خدمة',
    'birth_certificate': 'شهادة ميلاد',
    'death_certificate': 'شهادة وفاة',
    'marriage_certificate': 'عقد زواج',
    'family_book': 'دفتر عائلة',
    'residence_card': 'بطاقة سكن / إقامة',
    // New mappings
    'signed_form': 'الاستمارة الموقعة',
    'order_copy': 'نسخة التكليف / الأمر',
    'agent_id': 'هوية الوكيل',
    'personnel_id': 'هوية الفرد',
    'prosecution_memo': 'مذكرة النيابة',
    'ruling_copy': 'نسخة الحكم'
  }
  return map[type] || map[type.toLowerCase()] || type
}

function handleUploadSuccess(newDoc: any) {
  showUploadModal.value = false
  // Emitting to parent to update the person.documents array
  if (!props.person.documents) {
    props.person.documents = []
  }
  props.person.documents.unshift(newDoc) // add to top
  emit('update')
}


</script>
