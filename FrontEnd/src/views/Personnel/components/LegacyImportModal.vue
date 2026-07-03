<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-gray-900/50 transition-opacity" @click="closeModal"></div>

    <!-- Modal Panel -->
    <div class="relative w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-theme-xl dark:bg-gray-900 sm:my-8 transition-all">
      <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand-100 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">استيراد البيانات التاريخية</h3>
            <p class="text-xs text-gray-500 mt-0.5">رفع كشوفات إكسل (Excel) لإدراج الأفراد دفعة واحدة</p>
          </div>
        </div>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors">
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 py-6 space-y-6">
        
        <!-- Important Alert -->
        <div class="flex items-start gap-3 rounded-lg border border-warning-200 bg-warning-50 p-4 dark:border-warning-500/30 dark:bg-warning-500/10">
          <svg class="h-5 w-5 text-warning-600 dark:text-warning-400 shrink-0 mt-0.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h4 class="text-sm font-bold text-warning-800 dark:text-warning-300">ملاحظة هامة</h4>
            <p class="text-xs text-warning-700 dark:text-warning-400 mt-1 leading-relaxed">
              هذه العملية ستأخذ وقتاً لمعالجة الملف في الخلفية. استخدم خيار <b>(التجربة Dry Run)</b> أولاً للتأكد من خلو الملف من الأخطاء كالأرقام الوطنية المكررة أو الحقول الناقصة.
            </p>
          </div>
        </div>

        <!-- Dry Run Toggle -->
        <div class="flex items-center justify-between rounded-xl border border-gray-200 p-4 dark:border-gray-800">
          <div>
            <span class="block text-sm font-bold text-gray-900 dark:text-white">وضع التجربة والفحص (Dry Run)</span>
            <span class="block text-xs text-gray-500 mt-1">إذا كان مفعّلاً، سيقوم النظام بمحاكاة الإدراج واكتشاف الأخطاء بدون حفظ فعلي.</span>
          </div>
          <button 
            type="button" 
            class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2"
            :class="dryRun ? 'bg-brand-600' : 'bg-gray-200 dark:bg-gray-700'"
            @click="dryRun = !dryRun"
          >
            <span class="sr-only">استخدام وضع التجربة</span>
            <span 
              aria-hidden="true" 
              class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
              :class="dryRun ? 'ltr:translate-x-5 rtl:-translate-x-5' : 'translate-x-0'"
            ></span>
          </button>
        </div>

        <!-- File Upload Area -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">ملف البيانات <span class="text-error-500">*</span></label>
          <div 
            class="mt-1 flex justify-center rounded-xl border-2 border-dashed px-6 py-8 transition-colors cursor-pointer"
            :class="[
              isDragging ? 'border-brand-500 bg-brand-50 dark:bg-brand-500/10' : 'border-gray-300 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600',
              errors.file ? 'border-error-300 bg-error-50 dark:border-error-700 dark:bg-error-500/10' : '',
              selectedFile ? 'border-success-500 bg-success-50 dark:border-success-500/50 dark:bg-success-500/10' : ''
            ]"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <div class="text-center">
              <svg v-if="selectedFile" class="mx-auto h-12 w-12 text-success-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              
              <div class="mt-4 flex text-sm leading-6 text-gray-600 dark:text-gray-400 justify-center">
                <span v-if="selectedFile" class="font-bold text-gray-900 dark:text-white">{{ selectedFile.name }}</span>
                <span v-else class="font-medium text-brand-600 dark:text-brand-400">اضغط لرفع الملف أو اسحبه هنا</span>
              </div>
              <p v-if="!selectedFile" class="text-xs leading-5 text-gray-500 mt-1">XLSX, XLS, CSV حتى 50MB</p>
            </div>
            <input ref="fileInput" type="file" class="hidden" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" @change="handleFileSelect">
          </div>
          <p v-if="errors.file" class="mt-1 text-xs text-error-500">{{ errors.file }}</p>
        </div>

        <div v-if="globalError" class="text-sm text-error-600 dark:text-error-400 text-center font-medium">{{ globalError }}</div>
      </div>

      <div class="bg-gray-50 px-6 py-4 border-t border-gray-100 dark:bg-gray-800/50 dark:border-gray-800 flex justify-end gap-3 rounded-b-2xl">
        <button 
          @click="closeModal" 
          type="button" 
          class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
          :disabled="isSubmitting"
        >
          إلغاء
        </button>
        <button 
          @click="submitUpload" 
          type="button" 
          class="inline-flex justify-center items-center gap-2 rounded-lg px-5 py-2 text-sm font-medium text-white shadow-theme-xs focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors disabled:opacity-50"
          :class="dryRun ? 'bg-gray-800 hover:bg-gray-700 focus:ring-gray-800' : 'bg-brand-600 hover:bg-brand-500 focus:ring-brand-500'"
          :disabled="isSubmitting"
        >
          <svg v-if="isSubmitting" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isSubmitting ? 'جاري الإرسال...' : (dryRun ? 'بدء التجربة (Dry Run)' : 'استيراد فعلي') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { usePersonnelStore } from '@/stores/personnel'

const emit = defineEmits(['close', 'success'])
const personnelStore = usePersonnelStore()

const dryRun = ref(true) // Default to true for safety
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const isSubmitting = ref(false)
const globalError = ref('')
const errors = ref({
  file: ''
})

function closeModal() {
  if (!isSubmitting.value) {
    emit('close')
  }
}

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
  
  // Basic validation for Excel/CSV
  const validTypes = [
    'text/csv', 
    'application/vnd.ms-excel', 
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ]
  
  if (!validTypes.includes(file.type) && !file.name.match(/\.(csv|xls|xlsx)$/i)) {
    errors.value.file = 'عذراً، الصيغة غير مدعومة. يجب أن يكون الملف إكسل أو CSV.'
    return
  }
  
  if (file.size > 50 * 1024 * 1024) { // 50MB
    errors.value.file = 'حجم الملف يتجاوز الحد الأقصى (50MB).'
    return
  }
  
  selectedFile.value = file
}

async function submitUpload() {
  errors.value.file = ''
  globalError.value = ''
  
  if (!selectedFile.value) {
    errors.value.file = 'الرجاء اختيار ملف لرفعه'
    return
  }
  
  isSubmitting.value = true
  
  try {
    const result = await personnelStore.importLegacyData(selectedFile.value, dryRun.value)
    emit('success', { result, dryRun: dryRun.value })
  } catch (error: any) {
    globalError.value = personnelStore.error || error.message || 'حدث خطأ أثناء رفع الملف'
  } finally {
    isSubmitting.value = false
  }
}
</script>
