<template>
  <button
    :class="[
      'inline-flex items-center justify-center font-medium gap-2 rounded-lg transition-colors focus:outline-hidden focus:ring-2 focus:ring-brand-500 focus:ring-offset-2',
      sizeClasses[size],
      variantClasses[variant],
      customClass,
      { 'cursor-not-allowed opacity-50': disabled || loading },
    ]"
    @click="$emit('click', $event)"
    :disabled="disabled || loading"
    :type="type"
  >
    <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
    </svg>
    <span v-else-if="startIcon" class="flex items-center">
      <component :is="startIcon" />
    </span>
    <slot></slot>
    <span v-if="endIcon" class="flex items-center">
      <component :is="endIcon" />
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface ButtonProps {
  size?: 'sm' | 'md' | 'lg'
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'outline' | 'ghost'
  type?: 'button' | 'submit' | 'reset'
  startIcon?: object
  endIcon?: object
  customClass?: string
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<ButtonProps>(), {
  size: 'md',
  variant: 'primary',
  type: 'button',
  customClass: '',
  disabled: false,
  loading: false,
})

defineEmits(['click'])

const sizeClasses = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-5 py-2.5 text-sm',
  lg: 'px-6 py-3.5 text-base',
}

const variantClasses = {
  primary: 'bg-brand-600 text-white shadow-theme-xs hover:bg-brand-500 disabled:bg-brand-300',
  secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700',
  success: 'bg-success-600 text-white shadow-theme-xs hover:bg-success-500 disabled:bg-success-300',
  danger: 'bg-error-600 text-white shadow-theme-xs hover:bg-error-500 disabled:bg-error-300',
  outline: 'border border-gray-300 bg-white text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700',
  ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800',
}
</script>
