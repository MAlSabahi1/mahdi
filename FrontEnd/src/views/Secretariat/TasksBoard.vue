<template>
  <admin-layout>
    <div class="space-y-6">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('secretariat.tasks.title') }}</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ $t('secretariat.tasks.subtitle') }}</p>
        </div>
        <button class="flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-600 shadow-theme-xs">
          {{ $t('secretariat.tasks.add') }}
        </button>
      </div>

      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.tasks.task_title') }}</th>
                <th class="px-6 py-4 text-start text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.tasks.assigned_to') }}</th>
                <th class="px-6 py-4 text-start text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.tasks.status') }}</th>
                <th class="px-6 py-4 text-start text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.tasks.due_date') }}</th>
                <th class="px-6 py-4 text-start text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white dark:divide-gray-800 dark:bg-gray-900">
              <tr v-if="loading">
                <td colspan="5" class="px-6 py-8 text-center text-sm text-gray-500">{{ $t('common.loading') }}</td>
              </tr>
              <tr v-else-if="tasks.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-sm text-gray-500">{{ $t('common.no_data') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'

const { t } = useI18n()
const store = useSecretariatStore()
const loading = ref(true)
const tasks = ref([])

onMounted(async () => {
  try {
    const res = await store.fetchTasks()
    tasks.value = res.results || []
  } finally {
    loading.value = false
  }
})
</script>
