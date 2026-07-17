<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
      <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-800 flex items-center gap-3 bg-gray-50/50 dark:bg-gray-800/20">
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-50 text-purple-600 dark:bg-purple-500/10 dark:text-purple-400">
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
        </div>
        <h3 class="text-base font-bold text-gray-900 dark:text-white">سجل المتغيرات الشهرية</h3>
      </div>
      
      <div v-if="person.monthly_variables && person.monthly_variables.length > 0" class="overflow-x-auto">
        <table class="w-full text-start text-sm text-gray-600 dark:text-gray-400">
          <thead class="bg-gray-50 dark:bg-gray-800/50 text-xs uppercase font-bold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">
            <tr>
              <th scope="col" class="px-6 py-4">الشهر (الاستحقاق)</th>
              <th scope="col" class="px-6 py-4">نوع المتغير</th>
              <th scope="col" class="px-6 py-4">القيمة / الملاحظة</th>
              <th scope="col" class="px-6 py-4">المصدر</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr v-for="variable in person.monthly_variables" :key="variable.id" class="hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors">
              <td class="px-6 py-4 font-bold text-gray-900 dark:text-white whitespace-nowrap">
                {{ variable.month }}
              </td>
              <td class="px-6 py-4 font-medium text-gray-700 dark:text-gray-300">
                {{ variable.variable_type_name || 'متغير وارد من كشف' }}
              </td>
              <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400 border border-brand-100 dark:border-brand-900/50">
                  {{ variable.variable_value }}
                </span>
                <p v-if="variable.notes" class="mt-1 text-xs text-gray-500">{{ variable.notes }}</p>
              </td>
              <td class="px-6 py-4 text-xs text-gray-500 dark:text-gray-400">
                {{ variable.source_display || variable.source_column }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center py-16">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-50 dark:bg-gray-800 mb-4 text-gray-400">
          <svg class="h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <h4 class="text-base font-bold text-gray-900 dark:text-white mb-1">لا توجد متغيرات شهرية</h4>
        <p class="text-sm text-gray-500 dark:text-gray-400">لم يتم تسجيل أي متغيرات تاريخية أو شهرية لهذا الفرد.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  person: any
}>()
</script>
