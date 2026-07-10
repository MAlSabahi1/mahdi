<template>
  <div class="relative">
    <div class="flex items-center justify-between mb-1.5">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-400">
        {{ label }} <span v-if="required" class="text-error-500">*</span>
      </label>
      <div class="flex items-center gap-2">
        <button v-if="step >= 2 && !isEditing" type="button" @click="startEdit" class="text-xs text-brand-600 hover:underline">
          تعديل الرقم
        </button>
        <button v-if="isEditing && matchedValue" type="button" @click="cancelEdit" class="text-xs text-gray-500 hover:text-gray-700 hover:underline">
          تراجع
        </button>
        <span v-if="step === 3 && !isEditing" class="text-success-500 flex items-center text-xs font-bold bg-success-50 dark:bg-success-900/30 px-2 py-0.5 rounded">
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          متطابق
        </span>
      </div>
    </div>
    
    <!-- Step 1: Original Entry -->
    <div class="relative transition-all duration-300" :class="{'opacity-50 blur-[2px] pointer-events-none': step === 2}">
      <div class="flex justify-between gap-0.5 sm:gap-1 w-full" dir="ltr">
        <input v-for="(d, i) in 11" :key="'nid1-'+i" 
          ref="inputRefs1"
          v-model="digits1[i]"
          @input="onInput(1, i, $event)"
          @keydown="onKeydown(1, i, $event)"
          @paste="onPaste(1, $event)"
          @focus="($event.target as HTMLInputElement).select()"
          type="text" maxlength="1"
          class="flex-1 min-w-[18px] max-w-[34px] h-[38px] sm:h-[42px] text-center text-sm sm:text-base font-bold rounded-md border focus:ring-1 transition-colors p-0"
          :class="{
            'border-gray-300 focus:border-brand-500 focus:ring-brand-500/20 dark:bg-gray-900 dark:border-gray-700 dark:text-white': step !== 3 || isEditing,
            'border-success-500 bg-success-50 text-success-700 dark:border-success-500 dark:bg-success-900/20 dark:text-success-400': step === 3 && !isEditing,
            'pointer-events-none': (step === 3 && !isEditing) || step === 2
          }"
        />
      </div>
    </div>

    <!-- Step 2: Confirm Entry -->
    <div v-show="step === 2" class="mt-4 transition-all duration-300 relative">
      <label class="mb-1.5 block text-xs font-bold text-brand-600 dark:text-brand-400">
        تأكيد: يرجى التأكد من الرقم من البطاقة وإعادة كتابته:
      </label>
      <div class="flex justify-between gap-0.5 sm:gap-1 w-full" dir="ltr">
        <input v-for="(d, i) in 11" :key="'nid2-'+i" 
          ref="inputRefs2"
          v-model="digits2[i]"
          @input="onInput(2, i, $event)"
          @keydown="onKeydown(2, i, $event)"
          @paste.prevent
          @focus="($event.target as HTMLInputElement).select()"
          type="text" maxlength="1"
          class="flex-1 min-w-[18px] max-w-[34px] h-[38px] sm:h-[42px] text-center text-sm sm:text-base font-bold rounded-md border-2 border-brand-300 focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20 dark:bg-gray-900 dark:border-brand-700 dark:text-white transition-colors p-0"
          :class="{'border-error-500 dark:border-error-500 bg-error-50 dark:bg-error-900/20': shake}"
        />
      </div>
    </div>

    <!-- Messages -->
    <div class="mt-2 text-center min-h-[20px]">
      <p v-if="duplicateError" class="text-xs text-error-500 font-medium">{{ duplicateError }}</p>
      <p v-else-if="isValidating || isValidatingLocal" class="text-xs text-gray-500 flex items-center justify-center">
        <svg class="animate-spin h-3 w-3 mr-1" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>
        جاري الفحص السحابي...
      </p>
      <p v-else-if="localError || error" class="text-xs text-error-500 font-medium">{{ localError || error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, type PropType, onMounted } from 'vue'

const props = defineProps({
  modelValue: { type: String as PropType<string | null>, default: null },
  label: { type: String, default: 'الرقم الوطني' },
  required: { type: Boolean, default: true },
  error: { type: String, default: '' },
  duplicateError: { type: String, default: '' },
  isValidating: { type: Boolean, default: false },
  autofocus: { type: Boolean, default: false },
  checkDuplicateFn: { type: Function as PropType<(val: string) => Promise<string | null>>, default: null }
})

const emit = defineEmits(['update:modelValue', 'complete', 'mismatch'])

const step = ref(1) // 1: Entry, 2: Confirm, 3: Success
const isEditing = ref(false)
const matchedValue = ref<string | null>(null)

const digits1 = ref<string[]>(Array(11).fill(''))
const digits2 = ref<string[]>(Array(11).fill(''))
const inputRefs1 = ref<HTMLInputElement[]>([])
const inputRefs2 = ref<HTMLInputElement[]>([])
const shake = ref(false)
const localError = ref('')
const isValidatingLocal = ref(false)

onMounted(() => {
  if (props.autofocus && step.value === 1 && !props.modelValue) {
    nextTick(() => {
      inputRefs1.value[0]?.focus()
    })
  }
})

// Initialize if modelValue is passed
watch(() => props.modelValue, (newVal) => {
  if (newVal && newVal.length === 11 && step.value === 1) {
    matchedValue.value = newVal
    digits1.value = newVal.split('')
    digits2.value = newVal.split('')
    step.value = 3
    isEditing.value = false
  }
}, { immediate: true })

function onInput(s: 1 | 2, index: number, event: Event) {
  const target = event.target as HTMLInputElement
  const val = target.value.replace(/\D/g, '')
  
  const arr = s === 1 ? digits1.value : digits2.value
  arr[index] = val
  target.value = val

  if (val && index < 10) {
    const refs = s === 1 ? inputRefs1.value : inputRefs2.value
    refs[index + 1]?.focus()
  }

  checkCompletion(s)
}

function onKeydown(s: 1 | 2, index: number, event: KeyboardEvent) {
  const refs = s === 1 ? inputRefs1.value : inputRefs2.value
  
  if (event.key === 'Backspace') {
    const arr = s === 1 ? digits1.value : digits2.value
    if (!arr[index] && index > 0) {
      refs[index - 1]?.focus()
    }
  } else if (event.key === 'ArrowRight') {
    event.preventDefault()
    if (index < 10) refs[index + 1]?.focus()
  } else if (event.key === 'ArrowLeft') {
    event.preventDefault()
    if (index > 0) refs[index - 1]?.focus()
  }
}

function onPaste(s: 1, event: ClipboardEvent) {
  event.preventDefault()
  const paste = (event.clipboardData?.getData('text') || '').replace(/\D/g, '').slice(0, 11)
  if (!paste) return
  
  for (let i = 0; i < paste.length; i++) {
    digits1.value[i] = paste[i]
  }
  
  const focusIndex = paste.length < 11 ? paste.length : 10
  const refs = s === 1 ? inputRefs1.value : inputRefs2.value
  refs[focusIndex]?.focus()
  checkCompletion(s)
}

async function checkCompletion(s: 1 | 2) {
  if (s === 1) {
    if (digits1.value.every(d => d !== '')) {
      const v1 = digits1.value.join('')
      
      if (props.checkDuplicateFn) {
        isValidatingLocal.value = true
        const errorMsg = await props.checkDuplicateFn(v1)
        isValidatingLocal.value = false
        if (errorMsg) {
          localError.value = errorMsg
          return // Stop and do not go to step 2
        }
      }
      
      step.value = 2
      localError.value = ''
      nextTick(() => { inputRefs2.value[0]?.focus() })
    }
  } else if (s === 2) {
    if (digits2.value.every(d => d !== '')) {
      const v1 = digits1.value.join('')
      const v2 = digits2.value.join('')
      
      if (v1 === v2) {
        step.value = 3
        isEditing.value = false
        matchedValue.value = v1
        localError.value = ''
        emit('update:modelValue', v1)
        emit('complete', v1)
      } else {
        shake.value = true
        setTimeout(() => { shake.value = false }, 400)
        digits2.value = Array(11).fill('')
        inputRefs2.value[0]?.focus()
        localError.value = 'الرقم غير متطابق! لقد كتبت رقماً مختلفاً في التأكيد.'
        emit('mismatch')
      }
    }
  }
}

function startEdit() {
  isEditing.value = true
  step.value = 1
  digits2.value = Array(11).fill('')
  emit('update:modelValue', null)
  
  nextTick(() => { 
    const emptyIndex = digits1.value.findIndex(d => !d)
    const focusIndex = emptyIndex === -1 ? 10 : emptyIndex
    inputRefs1.value[focusIndex]?.focus() 
  })
}

function cancelEdit() {
  if (matchedValue.value) {
    digits1.value = matchedValue.value.split('')
    digits2.value = matchedValue.value.split('')
    step.value = 3
    isEditing.value = false
    localError.value = ''
    emit('update:modelValue', matchedValue.value)
  }
}
</script>
