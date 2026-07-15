<template>
  <div class="print:hidden bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 flex flex-wrap items-center justify-between gap-4 transition-all duration-300 hover:shadow-md">
    <div class="flex items-center gap-3">
      <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-900/30 dark:text-brand-400">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <div>
        <label for="month-picker" class="block text-sm font-semibold text-gray-700 dark:text-gray-200">
          استعراض السجلات حسب الشهر
        </label>
        <p class="text-xs text-gray-500 dark:text-gray-400">حدد شهراً لعرض المتغيرات التي حدثت خلاله</p>
      </div>
    </div>
    
    <div class="flex items-center gap-3">
      <div class="relative">
        <input 
          id="month-picker"
          type="month" 
          :value="modelValue"
          @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value); $emit('change')"
          class="block w-48 rounded-lg border-gray-300 bg-gray-50 py-2.5 px-4 text-sm font-medium text-gray-900 shadow-sm focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-200 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-brand-400 dark:focus:bg-gray-800 dark:focus:ring-brand-800 transition-colors cursor-pointer"
        />
      </div>
      
      <button 
        v-if="modelValue" 
        @click="$emit('update:modelValue', ''); $emit('change')" 
        class="group relative flex h-10 items-center justify-center gap-2 rounded-lg border border-red-200 bg-red-50 px-4 text-sm font-medium text-red-600 transition-all hover:border-red-300 hover:bg-red-100 hover:text-red-700 dark:border-red-900/50 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/40 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1"
        title="إلغاء الفلترة وعرض كافة السجلات"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        مسح الفلتر
      </button>
      
      <div v-else class="flex h-10 items-center px-4 rounded-lg bg-gray-100 text-sm font-medium text-gray-500 dark:bg-gray-800 dark:text-gray-400">
        يتم عرض الكشف التراكمي
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
}>()

defineEmits(['update:modelValue', 'change'])
</script>
