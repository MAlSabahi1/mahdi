<template>
  <div class="mb-5">
    <nav class="flex">
      <ol class="flex items-center gap-2.5 text-sm text-gray-500 dark:text-gray-400">
        <!-- 1. Home Icon -->
        <li class="flex items-center">
          <router-link
            to="/"
            class="flex items-center text-gray-500 hover:text-brand-600 dark:text-gray-400 dark:hover:text-brand-400 transition-colors"
          >
            <svg class="h-4.5 w-4.5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </router-link>
        </li>

        <!-- Separator -->
        <li class="flex items-center">
          <svg class="h-3 w-3 text-gray-400 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </li>

        <!-- 2. Home Page Link (الرئيسية) -->
        <li class="flex items-center">
          <router-link
            to="/"
            class="font-medium text-gray-600 hover:text-brand-600 dark:text-gray-400 dark:hover:text-brand-400 transition-colors"
          >
            {{ $t('nav.home') || 'الرئيسية' }}
          </router-link>
        </li>

        <!-- Separator (if pageTitle exists) -->
        <li v-if="pageTitle" class="flex items-center">
          <svg class="h-3 w-3 text-gray-400 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </li>

        <!-- 3. Current Page Title (Blue Pill Badge) -->
        <li v-if="pageTitle" class="flex items-center">
          <span class="inline-flex items-center rounded-lg bg-blue-50 px-3 py-1.5 text-sm font-bold text-blue-700 dark:bg-blue-950/40 dark:text-blue-400">
            {{ pageTitle }}
          </span>
        </li>
      </ol>
    </nav>
  </div>
</template>

<script setup lang="ts">
interface BreadcrumbProps {
  pageTitle: string
}

defineProps<BreadcrumbProps>()
</script>
