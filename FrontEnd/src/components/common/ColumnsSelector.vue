<template>
  <div class="relative">
    <button
      @click="isOpen = !isOpen"
      class="flex h-10 w-10 items-center justify-center rounded-xl border border-gray-200 bg-white text-gray-400 hover:bg-gray-50 hover:text-gray-600 shadow-sm transition-all dark:border-gray-800 dark:bg-gray-950 dark:text-gray-500 cursor-pointer"
      title="تحديد الأعمدة الظاهرة"
    >
      <svg class="h-5 w-5 stroke-[1.8]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      </svg>
    </button>

    <!-- Backdrop to close dropdown -->
    <div v-if="isOpen" @click="isOpen = false" class="fixed inset-0 z-40"></div>

    <!-- Columns Selection Dropdown Menu -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-56 rounded-2xl border border-gray-150 bg-white p-3 shadow-lg z-50 dark:border-gray-800 dark:bg-gray-900 text-right"
    >
      <div class="text-xs font-bold text-gray-400 mb-2 select-none px-2">الأعمدة المعروضة</div>
      <div class="space-y-1 max-h-64 overflow-y-auto pr-1">
        <label
          v-for="col in columns"
          :key="col.key"
          class="flex items-center justify-start gap-2.5 px-2.5 py-1.5 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg cursor-pointer select-none transition-colors"
        >
          <input
            type="checkbox"
            v-model="col.visible"
            class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-800"
          />
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ col.name }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Column {
  key: string
  name: string
  visible: boolean
}

defineProps<{
  columns: Column[]
}>()

const isOpen = ref(false)
</script>
