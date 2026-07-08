<template>
  <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
    <div class="overflow-x-auto max-h-[600px]">
      <table class="w-full text-right text-sm">
        <thead class="bg-brand-50/50 dark:bg-gray-800/50 text-gray-700 dark:text-gray-300 sticky top-0 shadow-sm z-10">
          <tr>
            <th v-for="col in columns" :key="col.key" class="px-4 py-3 font-semibold whitespace-nowrap bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
          <tr v-for="row in data" :key="row.index" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
            <td v-for="col in columns" :key="col.key" class="px-4 py-3 whitespace-nowrap">
              <template v-if="col.key === 'index'">
                <span class="font-mono text-gray-500">{{ row[col.key] }}</span>
              </template>
              <template v-else-if="col.key === 'full_name'">
                <span class="font-bold text-gray-900 dark:text-white">{{ row[col.key] }}</span>
              </template>
              <template v-else-if="col.key === 'rank'">
                <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 ring-1 ring-inset ring-blue-700/10">
                  {{ row[col.key] }}
                </span>
              </template>
              <template v-else>
                {{ row[col.key] || '-' }}
              </template>
            </td>
          </tr>
          <tr v-if="data.length === 0 && !loading">
            <td :colspan="columns.length" class="px-6 py-12 text-center text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              لا توجد بيانات مطابقة
            </td>
          </tr>
          <tr v-if="loading">
            <td :colspan="columns.length" class="px-6 py-12 text-center text-gray-500">
              <svg class="animate-spin mx-auto h-8 w-8 text-brand-500 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              جاري تحميل البيانات...
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="!loading && data.length > 0" class="bg-gray-50 dark:bg-gray-800/80 px-4 py-3 border-t border-gray-200 dark:border-gray-700 flex justify-between items-center text-sm text-gray-600 dark:text-gray-400">
      <span>إجمالي الأفراد المعروضين: <strong class="text-gray-900 dark:text-white">{{ data.length }}</strong></span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  columns: { key: string, label: string }[]
  data: any[]
  loading: boolean
}>()
</script>
