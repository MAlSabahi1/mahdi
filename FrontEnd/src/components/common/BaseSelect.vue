<template>
  <div>
    <label v-if="label" class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
      {{ label }} <span v-if="required" class="text-error-500">*</span>
    </label>
    <div class="relative z-20 bg-transparent">
      <select
        v-model="internalValue"
        :disabled="disabled"
        :class="[
          'dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors dark:placeholder:text-white/30',
          error
            ? 'border-error-500 text-error-900 focus:border-error-500 focus:ring-error-500/20 dark:border-error-500 dark:text-error-400'
            : 'border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800',
          { 'text-gray-800 dark:text-white/90': internalValue }
        ]"
      >
        <option v-if="placeholder !== false" :value="null" disabled>
          {{ placeholder === true ? '...' : placeholder }}
        </option>
        
        <option
          v-for="(opt, index) in normalizedOptions"
          :key="index"
          :value="opt.value"
          class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
        >
          {{ opt.label }}
        </option>
        
        <slot></slot>
      </select>
      <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
        <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>
    </div>
    <p v-if="error && typeof error === 'string'" class="mt-1.5 text-xs text-error-500 font-medium">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  modelValue?: any
  label?: string
  options?: any[]
  valueKey?: string
  labelKey?: string
  placeholder?: string | boolean
  error?: string | boolean
  required?: boolean
  disabled?: boolean
}>(), {
  modelValue: null,
  options: () => [],
  valueKey: 'id',
  labelKey: 'name',
  placeholder: '...',
  required: false,
  disabled: false
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: any): void
}>()

const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const normalizedOptions = computed(() => {
  return props.options.map(opt => {
    if (typeof opt === 'object' && opt !== null) {
      return {
        label: opt[props.labelKey],
        value: opt[props.valueKey]
      }
    }
    return { label: opt, value: opt }
  })
})
</script>
