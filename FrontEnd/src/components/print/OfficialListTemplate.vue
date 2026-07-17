<template>
  <div class="print-list-container relative">
    <!-- Removed outer-border and extra padding so the table stretches naturally -->
    <div class="h-full flex flex-col relative z-10 p-2">
      
      <!-- Report Header Slot (Expects ReportHeader.vue usually) -->
      <slot name="header"></slot>

      <!-- Document Title -->
      <div v-if="title" class="text-center mt-4 mb-4 flex justify-center items-center w-full print:hidden">
        <div class="border border-gray-500 bg-gray-100 rounded px-6 py-1.5">
          <h2 class="text-[18px] font-black text-black leading-tight tracking-tight" style="font-family: 'Cairo', sans-serif !important;">
            {{ title }}
          </h2>
        </div>
      </div>

      <!-- Main Content / Table Slot -->
      <div class="flex-grow w-full relative">
        <slot name="body"></slot>
      </div>

      <!-- Footer Slot (Expects ReportFooter.vue usually) -->
      <div class="mt-6">
        <slot name="footer"></slot>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
}>()
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');

.print-list-container {
  width: 297mm;
  min-height: 210mm; 
  background: white;
  margin: 0 auto;
  box-sizing: border-box;
  color: #000;
  padding: 10px;
  font-family: 'Cairo', sans-serif;
}

.outer-border {
  border: 1.5px solid #000;
  outline: 3px solid #000;
  outline-offset: -4px;
}
</style>

<style>
@media print {
  @page landscape-page {
    size: A4 landscape;
    margin: 0; 
  }
  
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
    height: auto !important;
  }
  
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }

  .print-list-container {
    page: landscape-page;
    width: 100% !important; 
    height: auto !important; 
    margin: 0 auto !important;
    padding: 0 !important;
    box-shadow: none !important;
    box-sizing: border-box !important;
    page-break-before: always;
    page-break-after: always;
    page-break-inside: avoid;
  }

  .print-list-container:last-child {
    page-break-after: auto;
  }
}
</style>
