<template>
  <div class="grid grid-cols-4 w-full h-full text-center print-location-grid" style="grid-template-rows: auto 1fr; gap: 0;">
    <!-- Headers -->
    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none" style="background-color: #f3f4f6 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;">المحافظة</div>
    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none" style="background-color: #f3f4f6 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;">المديرية</div>
    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none" style="background-color: #f3f4f6 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;">العزلة</div>
    <div class="text-[8px] tracking-tighter font-normal border-b border-black py-0.5 print-bg-gray flex items-center justify-center leading-none" style="background-color: #f3f4f6 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;">القرية</div>
    
    <!-- Data -->
    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ locationObj.gov || '—' }}</div>
    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ locationObj.dist || '—' }}</div>
    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ locationObj.subDist || '—' }}</div>
    <div class="py-1 px-0.5 font-bold text-[9px] flex items-center justify-center leading-tight break-words whitespace-normal">{{ locationObj.village || '—' }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  locationObj: {
    gov?: string;
    dist?: string;
    subDist?: string;
    village?: string;
  }
}>()
</script>
