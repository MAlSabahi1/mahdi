<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('nav.dashboard') || 'لوحة التحكم'" />
    <div class="grid grid-cols-12 gap-4 md:gap-6">
      <div class="col-span-12">
        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
          <h2 class="text-xl font-bold text-gray-800 dark:text-white/90">
            Welcome to your Dashboard
          </h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            This is a clean slate. Start building your amazing application!
          </p>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script>
import AdminLayout from '../components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

export default {
  components: {
    AdminLayout,
    PageBreadcrumb,
  },
  name: 'Ecommerce',
}
</script>
