<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity" @click="close"></div>

    <!-- Modal Panel -->
    <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white shadow-2xl transition-all dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
      
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-100 px-6 py-4 dark:border-gray-700">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-full bg-amber-50 text-amber-600 dark:bg-amber-500/10 dark:text-amber-500">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">طلب تصريح تصدير</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">النموذج محمي ويتطلب موافقة أمنية</p>
          </div>
        </div>
        <button @click="close" class="rounded-full p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-500 dark:hover:bg-gray-700 dark:hover:text-gray-300 transition-colors">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Body -->
      <div class="px-6 py-5">
        <p class="mb-4 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
          أنت على وشك طلب تصدير البيانات الخاصة بـ <span class="font-semibold text-brand-600 dark:text-brand-400">{{ reportName }}</span>.
          يرجى توضيح الغرض من هذا الطلب ليتم مراجعته واعتماده من قبل الإدارة المختصة.
        </p>
        
        <div class="space-y-1">
          <label class="block text-theme-sm font-medium text-gray-700 dark:text-gray-300">
            سبب التصدير المبرر <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="reason"
            rows="3"
            placeholder="مثال: لغرض المطابقة مع الإدارة المالية..."
            class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-theme-sm text-gray-900 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white dark:placeholder-gray-400"
            :class="{'border-red-300 focus:border-red-500 focus:ring-red-500': showError}"
          ></textarea>
          <p v-if="showError" class="text-xs text-red-500 mt-1">يجب كتابة سبب واضح للتصدير</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-end gap-3 border-t border-gray-100 bg-gray-50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
        <button
          @click="close"
          class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
        >
          إلغاء
        </button>
        <button
          @click="submit"
          :disabled="isSubmitting"
          class="flex items-center gap-2 rounded-lg bg-amber-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-amber-600 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg v-if="isSubmitting" class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
          {{ isSubmitting ? 'جاري إرسال الطلب...' : 'إرسال الطلب' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  isOpen: boolean
  reportName: string
}>()

const emit = defineEmits(['update:isOpen', 'submit'])

const reason = ref('')
const showError = ref(false)
const isSubmitting = ref(false)

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    reason.value = ''
    showError.value = false
    isSubmitting.value = false
  }
})

const close = () => {
  emit('update:isOpen', false)
}

const submit = async () => {
  if (!reason.value.trim()) {
    showError.value = true
    return
  }
  
  showError.value = false
  isSubmitting.value = true
  
  // Simulate network delay for realistic frontend feel
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  emit('submit', reason.value)
  close()
}
</script>
