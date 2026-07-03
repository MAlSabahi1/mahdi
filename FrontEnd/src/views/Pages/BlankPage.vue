<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div
      class="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12"
    >
      <div class="mx-auto w-full max-w-[630px] text-center">
        <div class="mb-6 flex justify-center text-brand-500">
          <svg class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6V4m0 2a2 2 0 100 3m0-3a2 2 0 110 3m-3.793-1.793l-1.414-1.414m1.414 1.414a2 2 0 112.828 2.828m-2.828-2.828a2 2 0 102.828 2.828M17.364 5.636l-1.414 1.414m1.414-1.414a2 2 0 11-2.829 2.829m2.829-2.829a2 2 0 10-2.829 2.829M5.636 17.364l1.414-1.414m-1.414 1.414a2 2 0 112.829-2.829m-2.829 2.829a2 2 0 102.829-2.829M12 12l.01 0m0 0a2 2 0 10-.01 0M12 18v2m0-2a2 2 0 100-3m0 3a2 2 0 110-3m3.793 1.793l1.414 1.414m-1.414-1.414a2 2 0 11-2.828-2.828m2.828 2.828a2 2 0 10-2.828-2.828M5.636 5.636l1.414 1.414m-1.414-1.414a2 2 0 112.829 2.829m-2.829-2.829a2 2 0 10-2.829 2.829" />
          </svg>
        </div>

        <h3
          class="mb-4 font-semibold text-gray-800 text-theme-xl dark:text-white/90 sm:text-2xl"
        >
          {{ $t('blank_page.card_title') }}
        </h3>

        <p class="text-sm text-gray-500 dark:text-gray-400 sm:text-base leading-relaxed">
          {{ $t('blank_page.description') }}
        </p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";

const { t } = useI18n();
const currentPageTitle = computed(() => t("blank_page.title"));
</script>

<style></style>
