<template>
  <div class="hidden print:block mt-8 pt-6">
    <div class="grid grid-cols-3 gap-8 text-sm font-bold text-gray-900 text-center">
      
      <!-- Right: Preparer -->
      <div class="space-y-6">
        <p class="mb-4">إعداد (قسم الخدمات)</p>
        <div class="space-y-4 flex flex-col items-start pr-8">
          <p class="flex w-full justify-between"><span class="w-16 text-right">الاسم:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
          <p class="flex w-full justify-between"><span class="w-16 text-right">الرتبة:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
          <p class="flex w-full justify-between"><span class="w-16 text-right">التوقيع:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
        </div>
      </div>
      
      <!-- Center: Reviewer -->
      <div class="space-y-6">
        <p class="mb-4">مراجعة (مدير إدارة القوى البشرية)</p>
        <div class="space-y-4 flex flex-col items-start pl-4 pr-4">
          <p class="flex w-full justify-between"><span class="w-16 text-right">الاسم:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
          <p class="flex w-full justify-between"><span class="w-16 text-right">الرتبة:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
          <p class="flex w-full justify-between"><span class="w-16 text-right">التوقيع:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
        </div>
      </div>
      
      <!-- Left: Approver -->
      <div class="space-y-6">
        <p class="mb-4">اعتماد (مدير عام شرطة المحافظة/الوحدة)</p>
        <div class="space-y-4 flex flex-col items-start pl-8">
          <p class="flex w-full justify-between"><span class="w-16 text-right">الاسم:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
          <p class="flex w-full justify-between"><span class="w-16 text-right">الرتبة:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
          <p class="flex w-full justify-between"><span class="w-16 text-right">التوقيع:</span> <span class="flex-1 text-right pr-2">.....................................</span></p>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
// Component doesn't require props for now as it's static structure based on جداول.md
</script>
