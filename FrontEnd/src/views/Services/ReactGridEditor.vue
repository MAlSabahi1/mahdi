<template>
  <admin-layout>
    <!-- Embedded React AG Grid Spreadsheet App -->
    <div class="h-[calc(100vh-100px)] w-full overflow-hidden text-start rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-xs bg-white dark:bg-gray-900" dir="rtl">
      <iframe 
        src="http://127.0.0.1:5176/" 
        class="w-full h-full border-0"
        allowfullscreen
        allow="fullscreen"
        title="تعديل الخدمات (Excel)"
      ></iframe>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layout/AdminLayout.vue'
</script>

<style scoped>
iframe {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
