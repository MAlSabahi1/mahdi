import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useValidationStore = defineStore('validation', () => {
  // Store errors as field -> string[]
  const fieldErrors = ref<Record<string, string[]>>({})

  // Set errors from API response
  function setErrors(errors: Record<string, any>) {
    const newErrors: Record<string, string[]> = {}
    
    const extractFieldErrors = (obj: any, prefix = '') => {
      if (typeof obj === 'string') {
        // Handle python dict string
        if (obj.startsWith('{') && obj.endsWith('}')) {
          try {
            const clean = obj.replace(/\[|\]|'|"/g, '').replace(/\{|\}/g, '')
            clean.split(',').forEach(part => {
              const subparts = part.split(':')
              if (subparts.length > 1) {
                const key = subparts[0].trim()
                const msg = subparts[1].trim()
                if (!newErrors[key]) newErrors[key] = []
                newErrors[key].push(msg)
              }
            })
          } catch (e) {
            // fallback
          }
        }
      } else if (typeof obj === 'object' && obj !== null) {
        for (const [key, value] of Object.entries(obj)) {
          if (Array.isArray(value)) {
             if (!newErrors[key]) newErrors[key] = []
             value.forEach(v => {
                if (typeof v === 'string') newErrors[key].push(v)
             })
          } else if (typeof value === 'string') {
             if (!newErrors[key]) newErrors[key] = []
             newErrors[key].push(value)
          } else if (typeof value === 'object') {
             extractFieldErrors(value, key)
          }
        }
      }
    }
    
    extractFieldErrors(errors)
    fieldErrors.value = newErrors
  }

  // Add a specific error manually (e.g. for client-side validation)
  function addFieldError(field: string, message: string) {
    if (!fieldErrors.value[field]) {
      fieldErrors.value[field] = []
    }
    if (!fieldErrors.value[field].includes(message)) {
      fieldErrors.value[field].push(message)
    }
  }

  // Clear specific field error
  function clearFieldError(field: string) {
    if (fieldErrors.value[field]) {
      delete fieldErrors.value[field]
    }
  }

  // Clear all errors
  function clearAllErrors() {
    fieldErrors.value = {}
  }

  return {
    fieldErrors,
    setErrors,
    addFieldError,
    clearFieldError,
    clearAllErrors
  }
})

/**
 * Global helper to validate all required fields inside a container.
 * Automatically adds errors to the store so v-field-error picks them up.
 */
export function validateFormFields(containerSelector = 'form, .space-y-6, main'): boolean {
  try {
    const store = useValidationStore()
    const container = document.querySelector(containerSelector)
    if (!container) return true

    let isValid = true
    const requiredElements = container.querySelectorAll('[data-field-name][required]')

    requiredElements.forEach((el: any) => {
      const fieldName = el.dataset.fieldName
      if (!el.value || el.value.trim() === '') {
        store.addFieldError(fieldName, 'الحقل مطلوب')
        isValid = false
      }
    })

    return isValid
  } catch {
    return true
  }
}
