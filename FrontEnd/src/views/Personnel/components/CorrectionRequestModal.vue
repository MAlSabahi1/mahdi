<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 p-4">
    <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl w-full max-w-lg overflow-hidden border border-gray-100 dark:border-gray-800">
      
      <!-- Modal Header -->
      <div class="flex justify-between items-center px-6 py-4 border-b border-gray-100 dark:border-gray-800">
        <div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('corrections.modal_title') }}</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ $t('corrections.modal_subtitle') }}</p>
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-5">
        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('corrections.field') }} <span class="text-error-500">*</span></label>
          <div class="relative z-20 bg-transparent">
            <select v-model="form.field" v-field-error="'field'" @change="updateOldValue" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
              <option value="" disabled>{{ $t('corrections.select_field') }}</option>
              <option v-for="field in editableFields" :key="field.key" :value="field.key" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">
                {{ $t(`corrections.fields.${field.key}`) }}
              </option>
            </select>
            <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
              <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </span>
          </div>
        </div>

        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('corrections.old_value') }}</label>
          <input v-model="form.old_value" v-field-error="'old_value'" type="text" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 shadow-theme-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-not-allowed">
        </div>

        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('corrections.new_value') }} <span class="text-error-500">*</span></label>
          <input v-model="form.new_value" v-field-error="'new_value'" type="text" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
        </div>

        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('corrections.reason') }} <span class="text-error-500">*</span></label>
          <textarea v-model="form.reason" v-field-error="'reason'" rows="3" :placeholder="$t('corrections.reason_placeholder')" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500"></textarea>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="flex justify-end gap-3 px-6 py-4 bg-gray-50 border-t border-gray-100 dark:bg-gray-800/50 dark:border-gray-800">
        <button @click="$emit('close')" class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700">
          {{ $t('common.cancel') }}
        </button>
        <button @click="submit" :disabled="!isFormValid || loading" class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 disabled:opacity-50">
          <svg v-if="loading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ $t('corrections.submit') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useCorrectionStore } from '@/stores/correction'
import { PersonnelRecord } from '@/stores/personnel'

const props = defineProps<{
  person: PersonnelRecord
}>()

const emit = defineEmits(['close', 'submitted'])

const store = useCorrectionStore()
const loading = ref(false)

const editableFields = [
  { key: 'full_name', prop: 'full_name' },
  { key: 'national_id', prop: 'national_id' },
  { key: 'birth_date', prop: 'birth_date' },
  { key: 'qualification', prop: 'qualification_name' },
  { key: 'current_rank', prop: 'rank_name' },
  { key: 'job_title', prop: 'job_title_name' },
]

const form = reactive({
  field: '',
  old_value: '',
  new_value: '',
  reason: ''
})

const isFormValid = computed(() => {
  return form.field && form.new_value.trim() && form.reason.trim()
})

function updateOldValue() {
  const fieldMap = editableFields.find(f => f.key === form.field)
  if (fieldMap) {
    const val = (props.person as any)[fieldMap.prop]
    form.old_value = val ? String(val) : ''
  } else {
    form.old_value = ''
  }
}

async function submit() {
  if (!isFormValid.value) return
  
  loading.value = true
  try {
    await store.submitCorrection({
      military_number: props.person.military_number,
      field: form.field,
      old_value: form.old_value,
      new_value: form.new_value,
      reason: form.reason
    })
    emit('submitted')
  } catch (err) {
    // Error handled globally via interceptor
  } finally {
    loading.value = false
  }
}
</script>
