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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">تحديث الرقم الوطني (آمن)</h3>
            <p class="text-xs text-gray-500 mt-0.5">يرجى توخي الدقة وإرفاق صور واضحة للبطاقة</p>
          </div>
        </div>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors">
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 py-6 space-y-6 max-h-[70vh] overflow-y-auto">
        
        <!-- Error Banner -->
        <div v-if="globalError" class="flex items-start gap-3 rounded-lg border border-error-200 bg-error-50 p-3 dark:border-error-500/30 dark:bg-error-500/10">
          <svg class="h-5 w-5 text-error-600 dark:text-error-400 shrink-0 mt-0.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <p class="text-sm text-error-700 dark:text-error-300">{{ globalError }}</p>
        </div>

        <!-- National ID Inputs -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الرقم الوطني الجديد <span class="text-error-500">*</span></label>
            <input 
              v-model="nationalId" 
              type="text" 
              maxlength="11" 
              class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:text-white dark:focus:border-brand-500" 
              :class="{'border-error-500 focus:border-error-500': errors.nationalId}"
              placeholder="مثال: 01010101010"
              @input="validateInputs"
            >
            <p v-if="errors.nationalId" class="mt-1 text-xs text-error-500">{{ errors.nationalId }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">تأكيد الرقم الوطني <span class="text-error-500">*</span></label>
            <input 
              v-model="confirmNationalId" 
              type="text" 
              maxlength="11" 
              class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:text-white dark:focus:border-brand-500" 
              :class="{'border-error-500 focus:border-error-500': errors.confirmNationalId}"
              placeholder="أعد إدخال الرقم..."
              @input="validateInputs"
            >
            <p v-if="errors.confirmNationalId" class="mt-1 text-xs text-error-500">{{ errors.confirmNationalId }}</p>
          </div>
        </div>

        <hr class="border-gray-100 dark:border-gray-800">

        <!-- File Uploads -->
        <div class="space-y-4">
          <h4 class="text-sm font-bold text-gray-900 dark:text-white">المرفقات الإلزامية</h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Front Image -->
            <div>
              <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">صورة البطاقة (الوجه الأمامي) <span class="text-error-500">*</span></label>
              <div 
                class="mt-1 flex justify-center rounded-xl border-2 border-dashed px-4 py-5 transition-colors cursor-pointer"
                :class="[
                  frontFile ? 'border-success-500 bg-success-50 dark:bg-success-500/10' : 'border-gray-300 dark:border-gray-700 hover:border-gray-400',
                  errors.frontFile ? 'border-error-300 bg-error-50 dark:border-error-700' : ''
                ]"
                @click="triggerFrontFile"
              >
                <div class="text-center">
                  <svg v-if="frontFile" class="mx-auto h-8 w-8 text-success-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-else class="mx-auto h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p class="mt-2 text-xs font-medium text-gray-900 dark:text-white truncate max-w-[150px]">
                    {{ frontFile ? frontFile.name : 'اضغط للرفع' }}
                  </p>
                </div>
                <input ref="frontInput" type="file" class="hidden" accept="image/jpeg,image/png,application/pdf" @change="e => handleFileSelect(e, 'front')">
              </div>
              <p v-if="errors.frontFile" class="mt-1 text-xs text-error-500">{{ errors.frontFile }}</p>
            </div>

            <!-- Back Image -->
            <div>
              <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">صورة البطاقة (الوجه الخلفي) <span class="text-error-500">*</span></label>
              <div 
                class="mt-1 flex justify-center rounded-xl border-2 border-dashed px-4 py-5 transition-colors cursor-pointer"
                :class="[
                  backFile ? 'border-success-500 bg-success-50 dark:bg-success-500/10' : 'border-gray-300 dark:border-gray-700 hover:border-gray-400',
                  errors.backFile ? 'border-error-300 bg-error-50 dark:border-error-700' : ''
                ]"
                @click="triggerBackFile"
              >
                <div class="text-center">
                  <svg v-if="backFile" class="mx-auto h-8 w-8 text-success-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-else class="mx-auto h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p class="mt-2 text-xs font-medium text-gray-900 dark:text-white truncate max-w-[150px]">
                    {{ backFile ? backFile.name : 'اضغط للرفع' }}
                  </p>
                </div>
                <input ref="backInput" type="file" class="hidden" accept="image/jpeg,image/png,application/pdf" @change="e => handleFileSelect(e, 'back')">
              </div>
              <p v-if="errors.backFile" class="mt-1 text-xs text-error-500">{{ errors.backFile }}</p>
            </div>
          </div>
        </div>

      </div>

      <div class="bg-gray-50 px-6 py-4 border-t border-gray-100 dark:bg-gray-800/50 dark:border-gray-800 flex justify-between items-center rounded-b-2xl">
        <p class="text-xs text-gray-500 hidden sm:block">هذا الإجراء سيقوم بتحديث السجل وإرفاق الوثائق</p>
        <div class="flex gap-3 w-full sm:w-auto justify-end">
          <button 
            @click="closeModal" 
            type="button" 
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
            :disabled="isSubmitting"
          >
            إلغاء
          </button>
          <button 
            @click="submitUpdate" 
            type="button" 
            class="inline-flex justify-center items-center gap-2 rounded-lg bg-brand-600 px-5 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
            :disabled="isSubmitting"
          >
            <svg v-if="isSubmitting" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ isSubmitting ? 'جاري التحديث...' : 'تحديث واعتماد' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDocumentStore } from '@/stores/document'
import { usePersonnelStore } from '@/stores/personnel'

const props = defineProps<{
  militaryNumber: string
}>()

const emit = defineEmits(['close', 'success'])

const documentStore = useDocumentStore()
const personnelStore = usePersonnelStore()

const nationalId = ref('')
const confirmNationalId = ref('')
const frontFile = ref<File | null>(null)
const backFile = ref<File | null>(null)

const frontInput = ref<HTMLInputElement | null>(null)
const backInput = ref<HTMLInputElement | null>(null)

const isSubmitting = ref(false)
const globalError = ref('')
const errors = ref({
  nationalId: '',
  confirmNationalId: '',
  frontFile: '',
  backFile: ''
})

function closeModal() {
  if (!isSubmitting.value) {
    emit('close')
  }
}

function triggerFrontFile() {
  frontInput.value?.click()
}

function triggerBackFile() {
  backInput.value?.click()
}

function handleFileSelect(event: Event, side: 'front' | 'back') {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    
    // Basic validation
    const validTypes = ['application/pdf', 'image/jpeg', 'image/png']
    if (!validTypes.includes(file.type)) {
      if (side === 'front') errors.value.frontFile = 'الصيغة غير مدعومة'
      if (side === 'back') errors.value.backFile = 'الصيغة غير مدعومة'
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      if (side === 'front') errors.value.frontFile = 'حجم الملف يتجاوز 5MB'
      if (side === 'back') errors.value.backFile = 'حجم الملف يتجاوز 5MB'
      return
    }

    if (side === 'front') {
      frontFile.value = file
      errors.value.frontFile = ''
    } else {
      backFile.value = file
      errors.value.backFile = ''
    }
  }
}

function validateInputs(): boolean {
  let isValid = true
  errors.value = { nationalId: '', confirmNationalId: '', frontFile: '', backFile: '' }
  globalError.value = ''

  if (!nationalId.value || nationalId.value.length < 11 || !/^\d+$/.test(nationalId.value)) {
    errors.value.nationalId = 'الرقم الوطني يجب أن يتكون من 11 رقماً'
    isValid = false
  }

  if (nationalId.value !== confirmNationalId.value) {
    errors.value.confirmNationalId = 'الرقمان غير متطابقين'
    isValid = false
  }

  if (!frontFile.value) {
    errors.value.frontFile = 'يجب إرفاق صورة البطاقة من الأمام'
    isValid = false
  }

  if (!backFile.value) {
    errors.value.backFile = 'يجب إرفاق صورة البطاقة من الخلف'
    isValid = false
  }

  return isValid
}

async function submitUpdate() {
  if (!validateInputs()) return

  isSubmitting.value = true
  try {
    // 1. Check if national ID already exists first (to prevent uploading files unnecessarily)
    const checkResult = await personnelStore.checkNationalId(nationalId.value)
    if (checkResult.exists) {
      errors.value.nationalId = 'هذا الرقم الوطني مسجل مسبقاً في النظام'
      isSubmitting.value = false
      return
    }

    // 2. Upload Documents
    // Using id_card document type
    const [frontDoc, backDoc] = await Promise.all([
      documentStore.uploadDocument(props.militaryNumber, frontFile.value!, 'id_card', 'بطاقة شخصية (أمام)'),
      documentStore.uploadDocument(props.militaryNumber, backFile.value!, 'id_card', 'بطاقة شخصية (خلف)')
    ])

    const documentIds = [frontDoc.id, backDoc.id]

    // 3. Call update endpoint
    await personnelStore.updateNationalId(props.militaryNumber, nationalId.value, documentIds)

    // Emit success
    emit('success')
  } catch (error: any) {
    globalError.value = personnelStore.error || error.message || 'فشل التحديث. الرجاء المحاولة مرة أخرى.'
  } finally {
    isSubmitting.value = false
  }
}
</script>
