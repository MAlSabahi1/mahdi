import type { DirectiveBinding, ObjectDirective } from 'vue'
import { useValidationStore } from '@/stores/validation'

function getStore() {
  try {
    return useValidationStore()
  } catch {
    return null
  }
}

export const fieldError: ObjectDirective = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const store = getStore()
    if (!store) return

    const fieldName = binding.value
    if (!fieldName) return
    
    // Attach to element dataset for global validation scans
    el.dataset.fieldName = fieldName

    let errorElement: HTMLElement | null = null

    const inputHandler = () => {
      store.clearFieldError(fieldName)
    }
    el.addEventListener('input', inputHandler)
    el.addEventListener('change', inputHandler)

    const updateErrorState = () => {
      const errors = store.fieldErrors[fieldName]
      
      if (errors && errors.length > 0) {
        // Add error styles
        el.classList.add('border-error-500', 'focus:border-error-500', 'focus:ring-error-500/20', 'dark:border-error-500')
        el.classList.remove('border-gray-300', 'dark:border-gray-700', 'focus:border-brand-500')
        
        if (!errorElement) {
          errorElement = document.createElement('p')
          errorElement.className = 'mt-1.5 text-xs font-medium text-error-500 dark:text-error-400 field-error-msg'
          if (el.parentNode) {
            el.parentNode.insertBefore(errorElement, el.nextSibling)
          }
        }
        errorElement.innerText = errors[0]
      } else {
        // Restore normal styles
        el.classList.remove('border-error-500', 'focus:border-error-500', 'focus:ring-error-500/20', 'dark:border-error-500')
        el.classList.add('border-gray-300', 'dark:border-gray-700')
        
        if (errorElement) {
          errorElement.remove()
          errorElement = null
        }
      }
    }

    const unsubscribe = store.$subscribe(() => {
      updateErrorState()
    })

    ;(el as any)._cleanup = () => {
      el.removeEventListener('input', inputHandler)
      el.removeEventListener('change', inputHandler)
      unsubscribe()
      if (errorElement) errorElement.remove()
    }
    
    updateErrorState()
  },
  
  unmounted(el: HTMLElement) {
    if ((el as any)._cleanup) {
      (el as any)._cleanup()
    }
  }
}
