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

    <!-- Documents Grid -->
    <div v-if="person.documents && person.documents.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="doc in person.documents" :key="doc.id" class="group relative flex flex-col justify-between rounded-xl border border-gray-100 p-4 transition-all hover:border-brand-300 hover:shadow-theme-md dark:border-gray-800 dark:hover:border-brand-700 dark:bg-gray-800/50">
        
        <div class="flex items-start gap-4">
          <!-- Icon -->
          <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-gray-50 text-gray-500 dark:bg-gray-800 dark:text-gray-400">
            <svg v-if="isImage(doc.file_url)" class="h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <svg v-else class="h-6 w-6 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          
          <div class="flex-1 overflow-hidden">
            <h4 class="truncate text-sm font-semibold text-gray-900 dark:text-white" :title="doc.document_type_display">
              {{ doc.document_type_display }}
            </h4>
            <p class="mt-1 truncate text-xs text-gray-500 dark:text-gray-400" dir="ltr">{{ doc.file_name || 'document_file' }}</p>
            <p class="mt-2 text-xs text-gray-400 dark:text-gray-500">{{ new Date(doc.created_at).toLocaleDateString('ar-SA') }}</p>
          </div>
        </div>

        <!-- Actions (visible on hover) -->
        <div class="mt-4 flex items-center gap-2 border-t border-gray-100 pt-3 dark:border-gray-800">
          <a :href="doc.file_url" target="_blank" class="flex-1 inline-flex justify-center items-center gap-1.5 rounded-lg bg-gray-50 px-2 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
            <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            {{ $t('documents.view') }}
          </a>
          <button @click="confirmDelete(doc)" class="inline-flex justify-center items-center rounded-lg bg-error-50 px-2.5 py-1.5 text-xs font-medium text-error-700 hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors" :title="$t('common.delete')">
            <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
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
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import DocumentUploadModal from './DocumentUploadModal.vue'

const props = defineProps<{
  person: any
}>()

const emit = defineEmits(['update'])
const { t } = useI18n()

const showUploadModal = ref(false)

function isImage(url: string) {
  if (!url) return false
  return url.match(/\.(jpeg|jpg|gif|png|blob)$/) != null || url.startsWith('blob:')
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

function confirmDelete(doc: any) {
  if (confirm(t('documents.delete_confirm_text'))) {
    // Mock delete logic
    const index = props.person.documents.findIndex((d: any) => d.id === doc.id)
    if (index !== -1) {
      props.person.documents.splice(index, 1)
      emit('update')
    }
  }
}
</script>
