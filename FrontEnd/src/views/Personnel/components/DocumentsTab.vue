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
        <h4 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-6 border-b border-gray-100 pb-2 dark:border-gray-800">
          سجل أحداث المرفقات (Timeline)
        </h4>
        <div class="relative border-r-2 border-brand-100 dark:border-brand-900 pr-6 mr-3">
          
          <div v-for="(event, idx) in groupedDocuments.events" :key="idx" class="relative mb-10 last:mb-0">
            <!-- Timeline Node -->
            <div class="absolute -right-[31px] top-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-white ring-4 ring-brand-50 dark:bg-gray-900 dark:ring-brand-500/20">
              <div class="h-2 w-2 rounded-full bg-brand-500"></div>
            </div>
            
            <!-- Event Header -->
            <div class="mb-4">
              <h4 class="text-base font-bold text-gray-900 dark:text-white">{{ event.title }}</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                تاريخ الإجراء: <span dir="ltr">{{ new Date(event.date).toLocaleDateString('ar-SA') }}</span> | مرجع: #{{ event.context_id }}
              </p>
            </div>
            
            <!-- Event Documents -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
              <div v-for="doc in event.docs" :key="doc.id" class="group relative flex flex-col justify-between rounded-xl border border-gray-100 p-3 transition-all hover:border-brand-300 hover:shadow-theme-md dark:border-gray-800 dark:hover:border-brand-700 dark:bg-gray-800/50">
                
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
                  <h4 class="truncate text-sm font-semibold text-gray-900 dark:text-white" :title="doc.document_type_display">{{ doc.document_type_display }}</h4>
                  <p class="mt-1 truncate text-xs text-gray-500 dark:text-gray-400" dir="ltr" v-if="doc.description">{{ doc.description }}</p>
                  <p class="mt-2 text-xs text-gray-400 dark:text-gray-500">{{ new Date(doc.created_at).toLocaleDateString('ar-SA') }}</p>
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
              <h4 class="truncate text-sm font-semibold text-gray-900 dark:text-white" :title="doc.document_type_display">{{ doc.document_type_display }}</h4>
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
  const events: Record<string, { title: string, date: string, context_id: string, docs: any[] }> = {}
  
  if (!props.person.documents) return { basic, events: [] }
  
  props.person.documents.forEach((doc: any) => {
    // If it lacks context or is marked general
    if (!doc.context_type || !doc.context_id || doc.context_type === 'General') {
      basic.push(doc)
    } else {
      const key = `${doc.context_type}_${doc.context_id}`
      if (!events[key]) {
        events[key] = {
          title: getContextTitle(doc.context_type),
          date: doc.created_at, // initial fallback date
          context_id: doc.context_id,
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
  }
  return map[type] || type
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
