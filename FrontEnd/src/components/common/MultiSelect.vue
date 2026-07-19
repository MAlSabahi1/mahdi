<template>
  <div class="relative">
    <!-- Backdrop to close dropdown -->
    <div v-if="isOpen" @click="isOpen = false" class="fixed inset-0 z-40"></div>
    
    <!-- Select Button -->
    <button 
      type="button"
      @click="isOpen = !isOpen"
      :disabled="disabled"
      class="relative z-10 flex h-11 w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <span class="truncate">
        {{ displayText }}
      </span>
      <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 20 20" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" />
      </svg>
    </button>
    
    <!-- Dropdown Menu -->
    <div v-if="isOpen" class="absolute z-50 mt-1 max-h-60 w-full overflow-y-auto rounded-xl border border-gray-200 bg-white p-2 shadow-lg dark:border-gray-700 dark:bg-gray-800">
      <div class="space-y-1">
        <!-- Select All Option -->
        <label v-if="options.length > 0" class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
          <input 
            type="checkbox" 
            :checked="isAllSelected" 
            @change="toggleAll" 
            class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" 
          />
          <span class="text-sm font-bold text-gray-900 dark:text-gray-100">تحديد الكل</span>
        </label>
        <div v-if="options.length > 0" class="h-px bg-gray-100 dark:bg-gray-700 my-1"></div>
        
        <!-- Individual Items -->
        <label v-for="opt in options" :key="opt[valueKey]" class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
          <input 
            type="checkbox" 
            :value="opt[valueKey]" 
            v-model="internalValue" 
            class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" 
          />
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ opt[labelKey] }}</span>
        </label>
        
        <!-- Empty State -->
        <div v-if="!options || options.length === 0" class="px-3 py-2 text-sm text-gray-500 dark:text-gray-400 text-center">
          لا توجد بيانات
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'الكل'
  },
  disabledPlaceholder: {
    type: String,
    default: 'اختر...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  valueKey: {
    type: String,
    default: 'id'
  },
  labelKey: {
    type: String,
    default: 'name'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)

const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isAllSelected = computed(() => {
  return (props.options?.length || 0) > 0 && (internalValue.value?.length || 0) === (props.options?.length || 0)
})

const displayText = computed(() => {
  if (props.disabled) return props.disabledPlaceholder
  if (!internalValue.value || internalValue.value.length === 0) return props.placeholder
  if (isAllSelected.value) return 'الكل'
  return `محدد (${internalValue.value.length})`
})

const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked && props.options) {
    internalValue.value = props.options.map((opt: any) => opt[props.valueKey])
  } else {
    internalValue.value = []
  }
}
</script>
