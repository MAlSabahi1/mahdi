<template>
  <div class="group relative flex flex-col overflow-hidden rounded-xl border border-gray-200 bg-white shadow-theme-sm transition-all hover:shadow-theme-md dark:border-gray-700 dark:bg-gray-800 dark:shadow-none">
    
    <!-- Header: Icon & Count -->
    <div class="flex items-center justify-between border-b border-gray-100 p-5 dark:border-gray-700">
      <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400 group-hover:scale-110 transition-transform">
        <slot name="icon">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </slot>
      </div>
      <div class="text-left rtl:text-left">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalRecords }}</div>
        <div class="text-xs font-medium text-gray-500 dark:text-gray-400">{{ recordsLabel }}</div>
      </div>
    </div>

    <!-- Body: Title & Desc -->
    <div class="flex-1 p-5">
      <div class="mb-1 inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-[10px] font-medium text-gray-800 dark:bg-gray-700 dark:text-gray-200">
        {{ reportType }}
      </div>
      <h3 class="mb-2 text-lg font-bold text-gray-900 dark:text-white">{{ title }}</h3>
      <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2" :title="description">{{ description }}</p>
    </div>

    <!-- Footer: Filter & Actions -->
    <div class="border-t border-gray-100 bg-gray-50/50 p-4 dark:border-gray-700 dark:bg-gray-800/30">
      <div class="mb-4">
        <label class="mb-1.5 block text-xs font-medium text-gray-700 dark:text-gray-300">فلترة المستوي:</label>
        <select
          v-model="selectedLevel"
          @change="$emit('update:level', selectedLevel)"
          class="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-theme-sm text-gray-900 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white"
        >
          <option value="all">جميع المستويات</option>
          <option value="central">الإدارات المركزية</option>
          <option value="branch">الفروع الميدانية</option>
          <option value="district">أمن المديريات</option>
        </select>
      </div>

      <div class="flex items-center justify-between gap-2">
        <button
          @click="$emit('view')"
          class="flex flex-1 items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 hover:text-brand-600 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          عرض
        </button>

        <template v-if="hasExportPermission">
          <button
            @click="$emit('export')"
            class="flex flex-1 items-center justify-center gap-2 rounded-lg bg-green-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            تصدير الكشف
          </button>
        </template>
        <template v-else>
          <button
            v-if="!exportRequestStatus || exportRequestStatus === 'REJECTED' || exportRequestStatus === 'EXPIRED'"
            @click="$emit('request-export')"
            class="flex flex-1 items-center justify-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            طلب التصدير
          </button>
          
          <button
            v-else-if="exportRequestStatus === 'APPROVED'"
            @click="$emit('download')"
            class="flex flex-1 items-center justify-center gap-2 rounded-lg bg-green-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors animate-pulse-once"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            تحميل الإكسل
          </button>

          <button
            v-else
            disabled
            class="flex flex-1 items-center justify-center gap-2 rounded-lg bg-amber-100 px-4 py-2.5 text-sm font-medium text-amber-700 shadow-sm cursor-not-allowed dark:bg-amber-900/30 dark:text-amber-400 border border-amber-200 dark:border-amber-800"
          >
            <svg class="h-4 w-4 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            قيد الانتظار...
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(defineProps<{
  title: string
  description: string
  reportType: string
  totalRecords?: number | string
  recordsLabel?: string
  hasExportPermission?: boolean
  exportRequestStatus?: string
  initialLevel?: string
}>(), {
  recordsLabel: 'سجل',
  hasExportPermission: false,
  exportRequestStatus: undefined,
  initialLevel: 'all'
})

const emit = defineEmits(['view', 'export', 'request-export', 'update:level', 'download'])

const selectedLevel = ref(props.initialLevel)
</script>
