<template>
  <div
    class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-[#f8fafc] dark:bg-gray-950"
  >
    <!-- Page size selector & Totals -->
    <div class="flex flex-wrap items-center gap-4 order-2 md:order-1">
      <!-- Page Size -->
      <div class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
        <span>عرض:</span>
        <select
          :value="pageSize"
          @change="$emit('change-page-size', Number(($event.target as HTMLSelectElement).value))"
          class="rounded-lg border border-gray-300 bg-white px-2 py-1 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 focus:outline-none"
        >
          <option :value="10">10</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>

      <!-- Total count -->
      <div class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
        <svg class="h-4.5 w-4.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <span>الإجمالي: <strong class="text-gray-800 dark:text-gray-200">{{ totalCount }}</strong> عناصر</span>
      </div>
    </div>

    <!-- Pagination controls -->
    <div class="flex flex-wrap items-center gap-3 order-1 md:order-2">
      <!-- Text: Page X of Y -->
      <span class="text-sm text-gray-500 dark:text-gray-400">
        الصفحة {{ currentPage }} من {{ totalPages }}
      </span>

      <!-- Page navigation buttons -->
      <div class="flex items-center gap-1">
        <!-- First Page -->
        <button
          @click="$emit('change-page', 1)"
          :disabled="currentPage === 1"
          class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 hover:bg-gray-50 disabled:opacity-40 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 cursor-pointer"
        >
          |&lt;
        </button>

        <!-- Previous -->
        <button
          @click="$emit('change-page', currentPage - 1)"
          :disabled="currentPage === 1"
          class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 hover:bg-gray-50 disabled:opacity-40 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 cursor-pointer"
        >
          &lt;
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
              'flex h-8 w-8 items-center justify-center rounded-lg text-sm font-semibold transition-all cursor-pointer',
              currentPage === p
                ? 'bg-blue-100 text-blue-700 font-bold dark:bg-blue-900/30 dark:text-blue-400'
                : 'text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-800'
            ]"
          >
            {{ p }}
          </button>
        </template>

        <!-- Next -->
        <button
          @click="$emit('change-page', currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 hover:bg-gray-50 disabled:opacity-40 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 cursor-pointer"
        >
          &gt;
        </button>
        <!-- Last Page -->
        <button
          @click="$emit('change-page', totalPages)"
          :disabled="currentPage === totalPages"
          class="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 hover:bg-gray-50 disabled:opacity-40 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 cursor-pointer"
        >
          &gt;|
        </button>
      </div>
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
