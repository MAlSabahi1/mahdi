<template>
  <div class="hidden print:flex flex-col mb-6 border-b-2 border-gray-900 pb-4">
    <div class="flex justify-between items-center text-sm font-bold text-gray-900">
      
      <!-- Right: Logo/Republic Info -->
      <div class="text-right w-1/3 space-y-1 pr-2 leading-tight">
        <p class="text-base">الجمهورية اليمنية</p>
        <p class="text-base">وزارة الداخلية</p>
        <p>وكيل قطاع الموارد البشرية</p>
        <p>الإدارة العامة للقوى البشرية</p>
        <p>لجنة بناء الامتدادات</p>
      </div>
      
      <!-- Center: Emblem Image -->
      <div class="text-center w-1/3 flex justify-center">
        <!-- Assuming logoBase.svg is the republic emblem -->
        <img src="/images/logo/logoBase.svg" alt="شعار الجمهورية" class="h-24 w-24 object-contain" style="filter: grayscale(100%);" />
      </div>
      
      <!-- Left: Document Info -->
      <div class="text-left w-1/3 space-y-2 pl-2 leading-tight" dir="rtl">
        <div class="flex justify-start">
          <span class="w-16">الرقم:</span>
          <span>(....................)</span>
        </div>
        <div class="flex justify-start">
          <span class="w-16">التاريخ:</span>
          <span>{{ formattedDate }}</span>
        </div>
        <div class="flex justify-start">
          <span class="w-16">المرفقات:</span>
          <span>(....................)</span>
        </div>
      </div>
      
    </div>

    <!-- Center Title -->
    <div class="mt-6 text-center">
      <h2 class="text-xl font-bold text-gray-900 border-b border-gray-900 inline-block pb-1 px-4">
        {{ title }} لشهر ( {{ currentMonth }} ) {{ currentYear }}م
      </h2>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

defineProps<{
  title: string
}>()

const dateObj = new Date()
const arabicMonths = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
const currentMonth = arabicMonths[dateObj.getMonth()]
const currentYear = dateObj.getFullYear()

const formattedDate = computed(() => {
  const d = String(dateObj.getDate()).padStart(2, '0')
  const m = String(dateObj.getMonth() + 1).padStart(2, '0')
  return `${d} / ${m} / ${currentYear} م`
})
</script>
