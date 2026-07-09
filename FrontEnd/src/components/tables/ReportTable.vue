<template>
  <div class="relative overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 print:border-none print:rounded-none print:bg-transparent">
    
    <!-- ─── Report Toolbar ─────────────────────────────── -->
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 px-5 py-4 border-b border-slate-200 dark:border-slate-800 print:hidden">
      <!-- Left Side: Title / Custom Tools -->
      <div class="flex-1 w-full md:w-auto">
        <slot name="toolbar-left"></slot>
      </div>

      <!-- Right Side (RTL): Search & Actions -->
      <div class="flex flex-wrap sm:flex-nowrap items-center gap-3 w-full md:w-auto">
        
        <!-- Search Input -->
        <div class="relative w-full sm:max-w-xs shrink-0" v-if="showSearch">
          <div class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3">
            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            :value="searchQuery"
            @input="$emit('update:searchQuery', ($event.target as HTMLInputElement).value)"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full h-10 rounded-lg border border-slate-300 bg-slate-50 py-2 ps-9 pe-8 text-theme-sm text-slate-900 placeholder-slate-400 focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-500/10 focus:outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:placeholder-slate-500 dark:focus:border-slate-500/40 dark:focus:bg-slate-900 transition-all"
          />
          <button
            v-if="searchQuery"
            @click="$emit('update:searchQuery', '')"
            class="absolute inset-y-0 end-0 flex items-center pe-2.5 text-gray-400 hover:text-gray-600 cursor-pointer"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Actions Group -->
        <div class="flex flex-wrap items-center gap-2 shrink-0">
          <!-- Refresh -->
          <button
            v-if="showRefresh"
            @click="$emit('refresh')"
            :class="[
              'flex h-10 w-10 items-center justify-center rounded-lg border shadow-theme-xs transition-all duration-200 ease-in-out cursor-pointer hover:shadow-theme-sm hover:-translate-y-0.5',
              loading
                ? 'border-brand-200 bg-brand-50 text-brand-500 dark:border-brand-500/30 dark:bg-brand-500/10'
                : 'border-slate-200 bg-white text-slate-500 hover:bg-slate-100 hover:text-slate-800 hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-300 dark:hover:border-slate-700'
            ]"
            title="تحديث"
          >
            <svg :class="['h-5 w-5', loading && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          <!-- Export -->
          <button
            v-if="showExport"
            @click="$emit('export')"
            class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-theme-xs hover:bg-brand-50 hover:text-brand-600 hover:border-brand-200 hover:shadow-theme-sm hover:-translate-y-0.5 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-brand-500/10 dark:hover:text-brand-400 dark:hover:border-brand-500/30 transition-all duration-200 ease-in-out cursor-pointer"
            title="تصدير (Excel / CSV)"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>

          <!-- Print -->
          <button
            v-if="showPrint"
            @click="$emit('print')"
            class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-theme-xs hover:bg-brand-50 hover:text-brand-600 hover:border-brand-200 hover:shadow-theme-sm hover:-translate-y-0.5 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-brand-500/10 dark:hover:text-brand-400 dark:hover:border-brand-500/30 transition-all duration-200 ease-in-out cursor-pointer"
            title="طباعة"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading overlay -->
    <div v-if="loading && data && data.length > 0" class="absolute inset-0 z-10 bg-white/60 dark:bg-gray-900/60 flex items-center justify-center backdrop-blur-[1px]">
      <svg class="h-6 w-6 animate-spin text-brand-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full w-full text-center border-collapse report-table">
        <thead class="bg-gray-50 dark:bg-gray-900/50 text-gray-500 dark:text-gray-400">
          <slot name="header"></slot>
        </thead>

        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-if="loading && (!data || data.length === 0)">
            <td class="px-5 py-20 text-center" colspan="100%">
              <div class="flex flex-col items-center justify-center">
                <svg class="mb-3 h-8 w-8 animate-spin text-brand-500" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-theme-sm font-medium text-gray-500 dark:text-gray-400">{{ loadingText }}</span>
              </div>
            </td>
          </tr>

          <tr v-else-if="!data || data.length === 0">
            <td class="px-5 py-20 text-center" colspan="100%">
              <div class="flex flex-col items-center justify-center">
                <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                  <svg class="h-7 w-7 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                </div>
                <h3 class="text-theme-sm font-semibold text-gray-900 dark:text-white">{{ emptyTitle }}</h3>
                <p class="mt-1 text-theme-xs text-gray-500 dark:text-gray-400 max-w-sm">{{ emptyDescription }}</p>
              </div>
            </td>
          </tr>

          <template v-else>
            <slot name="body"></slot>
          </template>
        </tbody>

        <tfoot v-if="$slots.footer" class="bg-slate-50 dark:bg-slate-900/50">
          <slot name="footer"></slot>
        </tfoot>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  data: any[]
  loading?: boolean
  loadingText?: string
  emptyTitle?: string
  emptyDescription?: string
  
  // Toolbar controls
  searchQuery?: string
  searchPlaceholder?: string
  showSearch?: boolean
  showRefresh?: boolean
  showExport?: boolean
  showPrint?: boolean
}>(), {
  loading: false,
  loadingText: 'جاري التحميل...',
  emptyTitle: 'لا توجد بيانات',
  emptyDescription: 'الجدول فارغ.',
  searchQuery: '',
  searchPlaceholder: 'بحث...',
  showSearch: false,
  showRefresh: false,
  showExport: false,
  showPrint: false
})

defineEmits(['update:searchQuery', 'refresh', 'export', 'print'])
</script>

