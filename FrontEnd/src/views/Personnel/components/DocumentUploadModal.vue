<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-gray-900/50 transition-opacity" @click="$emit('close')"></div>

    <!-- Modal Panel -->
    <div class="relative w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-theme-xl dark:bg-gray-900 sm:my-8 transition-all">
      <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center">
        <div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('documents.upload_new') }}</h3>
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors">
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 py-6 space-y-6">
        <!-- Document Type Selector -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('documents.document_type') }} <span class="text-error-500">*</span></label>
          <div class="relative z-20 bg-transparent">
            <select 
              v-model="documentType"
              class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
            >
              <option value="" disabled>{{ $t('documents.select_type') }}</option>
              <option v-for="(label, key) in documentTypes" :key="key" :value="key" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ label }}</option>
            </select>
            <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
              <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </span>
          </div>
          <p v-if="errors.documentType" class="mt-1 text-xs text-error-500">{{ errors.documentType }}</p>
        </div>

        <!-- File Upload Area -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الوثيقة <span class="text-error-500">*</span></label>
          <div 
            class="mt-1 flex justify-center rounded-xl border-2 border-dashed px-6 py-8 transition-colors"
            :class="[
              isDragging ? 'border-brand-500 bg-brand-50 dark:bg-brand-500/10' : 'border-gray-300 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600',
              errors.file ? 'border-error-300 bg-error-50 dark:border-error-700 dark:bg-error-500/10' : ''
            ]"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <div class="text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="mt-4 flex text-sm leading-6 text-gray-600 dark:text-gray-400 justify-center">
                <label for="file-upload" class="relative cursor-pointer rounded-md bg-transparent font-semibold text-brand-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-brand-600 focus-within:ring-offset-2 hover:text-brand-500 dark:text-brand-400 dark:hover:text-brand-300">
                  <span>{{ $t('documents.drag_drop') }}</span>
                  <input id="file-upload" ref="fileInput" name="file-upload" type="file" class="sr-only" @change="handleFileSelect" accept=".pdf,.jpg,.jpeg,.png">
                </label>
              </div>
              <p class="text-xs leading-5 text-gray-500">{{ $t('documents.supported_formats') }}</p>
            </div>
          </div>
          
          <!-- Selected File Preview -->
          <div v-if="selectedFile" class="mt-3 flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 p-3 dark:border-gray-700 dark:bg-gray-800">
            <div class="flex items-center gap-3 overflow-hidden">
              <svg class="h-6 w-6 text-brand-500 shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span class="truncate text-sm font-medium text-gray-900 dark:text-white" dir="ltr">{{ selectedFile.name }}</span>
            </div>
            <button type="button" @click.stop="clearFile" class="text-gray-400 hover:text-error-500 transition-colors shrink-0">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p v-if="errors.file" class="mt-1 text-xs text-error-500">{{ errors.file }}</p>
        </div>
      </div>

      <div class="bg-gray-50 px-6 py-4 border-t border-gray-100 dark:bg-gray-800/50 dark:border-gray-800 flex justify-end gap-3 rounded-b-2xl">
        <button 
          @click="$emit('close')" 
          type="button" 
          class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
          :disabled="isSubmitting"
        >
          {{ $t('common.cancel') }}
        </button>
        <button 
          @click="submitUpload" 
          type="button" 
          class="inline-flex justify-center items-center gap-2 rounded-lg bg-brand-600 px-5 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors"
          :disabled="isSubmitting"
        >
          <svg v-if="isSubmitting" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isSubmitting ? $t('documents.uploading') : $t('documents.upload') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDocumentStore } from '@/stores/document'

const props = defineProps<{
  person: any
}>()

const emit = defineEmits(['close', 'uploaded'])
const { t } = useI18n()
const documentStore = useDocumentStore()

const documentType = ref('')
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isSubmitting = ref(false)

const errors = ref({
  documentType: '',
  file: ''
})

const documentTypes = computed(() => {
  return {
    'id_card': t('documents.types.id_card'),
    'passport': t('documents.types.passport'),
    'certificate': t('documents.types.certificate'),
    'decree': t('documents.types.decree'),
    'other': t('documents.types.other')
  }
})

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    validateAndSetFile(target.files[0])
  }
}

function handleDrop(event: DragEvent) {
  isDragging.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
    validateAndSetFile(event.dataTransfer.files[0])
  }
}

function validateAndSetFile(file: File) {
  errors.value.file = ''
  
  // Basic validation
  const validTypes = ['application/pdf', 'image/jpeg', 'image/png']
  if (!validTypes.includes(file.type)) {
    errors.value.file = 'عذراً، الصيغة غير مدعومة. يجب أن يكون الملف PDF أو صورة JPG/PNG.'
    return
  }
  
  if (file.size > 5 * 1024 * 1024) { // 5MB
    errors.value.file = 'حجم الملف يتجاوز الحد الأقصى (5MB).'
    return
  }
  
  selectedFile.value = file
}

function clearFile() {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

async function submitUpload() {
  // Validate
  errors.value.documentType = ''
  errors.value.file = ''
  let isValid = true
  
  if (!documentType.value) {
    errors.value.documentType = 'الرجاء اختيار نوع المرفق'
    isValid = false
  }
  
  if (!selectedFile.value) {
    errors.value.file = 'الرجاء اختيار ملف لرفعه'
    isValid = false
  }
  
  if (!isValid) return
  
  isSubmitting.value = true
  
  try {
    const typeDisplay = documentTypes.value[documentType.value as keyof typeof documentTypes.value]
    
    // Call the mock store action
    const newDoc = await documentStore.uploadDocument(
      props.person.military_number,
      selectedFile.value!,
      documentType.value,
      typeDisplay
    )
    
    emit('uploaded', newDoc)
  } catch (error) {
    console.error('Failed to upload document', error)
    errors.value.file = 'حدث خطأ أثناء الرفع، يرجى المحاولة لاحقاً.'
  } finally {
    isSubmitting.value = false
  }
}
</script>
