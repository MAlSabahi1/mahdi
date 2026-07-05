<template>
  <div
    class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-white dark:bg-gray-900/50"
  >
    <!-- Text: Showing X to Y of Z entries -->
    <div class="text-sm text-gray-500 dark:text-gray-400 order-2 md:order-1 font-medium">
      {{ $t?.('common.showing') || 'Showing' }} {{ (currentPage - 1) * pageSize + 1 }} {{ $t?.('common.to') || 'to' }} {{ Math.min(currentPage * pageSize, totalCount) }} {{ $t?.('common.of') || 'of' }} {{ totalCount }} {{ $t?.('common.entries') || 'entries' }}
    </div>

    <!-- Pagination controls -->
    <div class="flex items-center gap-1 order-1 md:order-2">
      <!-- Previous -->
      <button
        @click="$emit('change-page', currentPage - 1)"
        :disabled="currentPage === 1"
        class="flex h-9 px-3 items-center justify-center rounded-md border border-gray-200 bg-white text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-40 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-pointer"
      >
        {{ $t?.('common.previous') || 'Previous' }}
      </button>

      <!-- Page Numbers -->
      <template v-for="(p, i) in visiblePages" :key="i">
        <span
          v-if="p === '...'"
          class="px-2 text-gray-400"
        >
          ...
        </span>
        <button
          v-else
          @click="$emit('change-page', Number(p))"
          :class="[
            'flex h-9 w-9 items-center justify-center rounded-md text-sm font-semibold transition-all cursor-pointer',
            currentPage === p
              ? 'bg-blue-50 text-blue-600 font-bold dark:bg-blue-900/30 dark:text-blue-400'
              : 'text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-800 border border-transparent hover:border-gray-200 dark:hover:border-gray-700'
          ]"
        >
          {{ p }}
        </button>
      </template>

      <!-- Next -->
      <button
        @click="$emit('change-page', currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="flex h-9 px-3 items-center justify-center rounded-md border border-gray-200 bg-white text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-40 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-pointer"
      >
        {{ $t?.('common.next') || 'Next' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  currentPage: number
  totalPages: number
  totalCount: number
  pageSize: number
  visiblePages: (number | string)[]
}>()

defineEmits<{
  (e: 'change-page', page: number): void
  (e: 'change-page-size', size: number): void
}>()
</script>
