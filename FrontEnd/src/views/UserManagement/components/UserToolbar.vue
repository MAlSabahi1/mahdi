<template>
  <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
    <!-- Right side: View, Search, Filter, Refresh, Settings -->
    <div class="flex flex-wrap items-center gap-2 order-2 lg:order-1">
      <!-- Eye button & Columns selection Dropdown (Extracted Component) -->
      <ColumnsSelector :columns="columns" />

      <!-- Search Input -->
      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="ابحث..."
          class="h-10 w-full rounded-xl border border-gray-200 bg-white pr-10 pl-4 text-sm text-gray-850 placeholder:text-gray-400/80 focus:border-blue-500 focus:bg-white focus:outline-none dark:border-gray-800 dark:bg-gray-950 dark:text-white/90"
        />
        <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-gray-400">
          <svg class="h-4.5 w-4.5 stroke-[1.5]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <!-- Filter button -->
      <button
        @click="showFiltersPanel = !showFiltersPanel"
        :class="[
          'flex h-10 w-10 items-center justify-center rounded-xl border shadow-xs transition-colors cursor-pointer',
          filterActive !== null
            ? 'border-blue-200 bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400'
            : 'border-gray-200 bg-white text-gray-400 hover:bg-gray-50 hover:text-gray-600 dark:border-gray-800 dark:bg-gray-950 dark:text-gray-500 dark:hover:bg-gray-900'
        ]"
        title="تصفية النشاط"
      >
        <svg class="h-5 w-5 stroke-[1.5]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 8.293A1 1 0 013 7.586V4z" />
        </svg>
      </button>

      <!-- Refresh button -->
      <button
        @click="$emit('refresh')"
        class="flex h-10 w-10 items-center justify-center rounded-xl border border-gray-200 bg-white text-gray-400 hover:bg-gray-50 hover:text-gray-600 shadow-xs transition-colors dark:border-gray-800 dark:bg-gray-950 dark:text-gray-500 dark:hover:bg-gray-900 cursor-pointer"
        title="تحديث البيانات"
      >
        <svg class="h-5 w-5 stroke-[1.8]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
        </svg>
      </button>

      <!-- Settings button -->
      <button
        class="flex h-10 w-10 items-center justify-center rounded-xl border border-blue-100 bg-blue-50/60 text-blue-500 hover:bg-blue-100 hover:text-blue-600 transition-colors dark:bg-blue-500/10 dark:border-blue-500/20 dark:text-blue-400 dark:hover:bg-blue-500/20 cursor-pointer"
        title="إعدادات الجدول"
      >
        <svg class="h-5 w-5 stroke-[1.8]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.43l-1.003.828c-.293.241-.438.613-.43.992a7.723 7.723 0 010 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.43l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.991l-1.004-.827a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.645-.869l.214-1.28z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>
    </div>

    <!-- Left side: Add New User button -->
    <div class="order-1 lg:order-2 flex justify-end">
      <button
        @click="$emit('add-new')"
        class="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 transition-colors cursor-pointer"
      >
        <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        إضافة جديد
      </button>
    </div>
  </div>

  <!-- Optional Filters panel toggle -->
  <div v-if="showFiltersPanel" class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900 transition-all mt-4">
    <div class="flex flex-wrap gap-2">
      <button
        @click="filterActive = null; $emit('filter-changed')"
        :class="[
          'rounded-lg px-4 py-2 text-sm font-medium transition-colors cursor-pointer',
          filterActive === null
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
        ]"
      >
        الكل
      </button>
      <button
        @click="filterActive = true; $emit('filter-changed')"
        :class="[
          'rounded-lg px-4 py-2 text-sm font-medium transition-colors cursor-pointer',
          filterActive === true
            ? 'bg-green-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
        ]"
      >
        الحسابات المفعلة
      </button>
      <button
        @click="filterActive = false; $emit('filter-changed')"
        :class="[
          'rounded-lg px-4 py-2 text-sm font-medium transition-colors cursor-pointer',
          filterActive === false
            ? 'bg-red-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
        ]"
      >
        الحسابات المعطلة
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import ColumnsSelector from '@/components/common/ColumnsSelector.vue'

defineProps<{
  columns: any[]
}>()

defineEmits<{
  (e: 'refresh'): void
  (e: 'add-new'): void
  (e: 'filter-changed'): void
}>()

const searchQuery = defineModel<string>('searchQuery', { required: true })
const filterActive = defineModel<boolean | null>('filterActive', { required: true })
const showFiltersPanel = defineModel<boolean>('showFiltersPanel', { required: true })
</script>
