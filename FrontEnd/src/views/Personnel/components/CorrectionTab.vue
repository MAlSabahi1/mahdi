<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('corrections.title') }}</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ $t('corrections.subtitle') }}</p>
      </div>
      <button @click="showModal = true" class="flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors">
        <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        {{ $t('corrections.new_request') }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="flex justify-center p-8">
      <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
    </div>

    <!-- Empty State -->
    <div v-else-if="requests.length === 0" class="rounded-xl border border-dashed border-gray-300 p-12 text-center dark:border-gray-700">
      <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
        <svg class="h-6 w-6 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="mt-4 text-sm font-medium text-gray-900 dark:text-white">{{ $t('corrections.no_requests') }}</h3>
    </div>

    <!-- Requests List -->
    <div v-else class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-start text-sm">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
              <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('corrections.requested_at') }}</th>
              <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('corrections.field') }}</th>
              <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('corrections.old_value') }}</th>
              <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('corrections.new_value') }}</th>
              <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="req in requests" :key="req.id" class="border-b border-gray-100 last:border-0 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
              <td class="px-5 py-4 whitespace-nowrap">{{ formatDate(req.requested_at) }}</td>
              <td class="px-5 py-4 whitespace-nowrap font-medium">{{ $t(`corrections.fields.${req.field}`) }}</td>
              <td class="px-5 py-4 whitespace-nowrap text-gray-500 line-through">{{ req.old_value || '-' }}</td>
              <td class="px-5 py-4 whitespace-nowrap text-brand-600 dark:text-brand-400 font-medium">{{ req.new_value }}</td>
              <td class="px-5 py-4 whitespace-nowrap">
                <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="getStatusClass(req.status)">
                  {{ getStatusText(req.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <CorrectionRequestModal
      v-if="showModal"
      :person="person"
      @close="showModal = false"
      @submitted="onSubmitted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCorrectionStore } from '@/stores/correction'
import type { PersonnelRecord } from '@/stores/personnel'
import CorrectionRequestModal from './CorrectionRequestModal.vue'

const props = defineProps<{
  person: PersonnelRecord
}>()

const { t } = useI18n()
const store = useCorrectionStore()
const showModal = ref(false)

const requests = computed(() => store.corrections.filter(c => c.military_number === props.person.military_number))

onMounted(() => {
  store.fetchCorrections(props.person.military_number)
})

function onSubmitted() {
  showModal.value = false
  // fetchCorrections logic is already handled (unshifted in store)
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-GB') // e.g., 28/06/2026
}

function getStatusClass(status: string) {
  const s = (status || '').toLowerCase()
  if (s === 'approved') return 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400'
  if (s === 'rejected') return 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
  return 'bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400'
}

function getStatusText(status: string) {
  const s = (status || '').toLowerCase()
  if (s === 'approved') return t('corrections.status_approved')
  if (s === 'rejected') return t('corrections.status_rejected')
  return t('corrections.status_pending')
}
</script>
