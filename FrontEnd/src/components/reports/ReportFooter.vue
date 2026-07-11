<template>
  <div class="hidden print:block mt-8 print:break-inside-avoid" style="page-break-inside: avoid; break-inside: avoid;">
    <div class="border-2 border-gray-900 rounded-xl p-4 grid grid-cols-3 gap-6 text-xs font-bold text-gray-900 text-center relative mb-3">
      <!-- Frame Title -->
      <div class="absolute -top-3 right-6 bg-white px-2 text-xs font-bold text-gray-900 print:bg-white">التوقيعات والاعتمادات</div>
      
      <!-- Right: Preparer -->
      <div class="space-y-3 flex flex-col items-start text-right">
        <p class="mb-2 font-bold">إعداد (قسم الخدمات)</p>
        <div class="space-y-2 w-full max-w-[200px]">
          <p class="flex items-center"><span class="w-12 text-right">الاسم:</span> <span class="flex-1 text-right">................................</span></p>
          <p class="flex items-center"><span class="w-12 text-right">الرتبة:</span> <span class="flex-1 text-right">................................</span></p>
          <p class="flex items-center"><span class="w-12 text-right">التوقيع:</span> <span class="flex-1 text-right">................................</span></p>
        </div>
      </div>
      
      <!-- Center: Reviewer -->
      <div class="space-y-3 flex flex-col items-center">
        <p class="mb-2 font-bold">مراجعة (مدير إدارة القوى البشرية)</p>
        <div class="space-y-2 w-full max-w-[200px]">
          <p class="flex items-center"><span class="w-12 text-right">الاسم:</span> <span class="flex-1 text-right">................................</span></p>
          <p class="flex items-center"><span class="w-12 text-right">الرتبة:</span> <span class="flex-1 text-right">................................</span></p>
          <p class="flex items-center"><span class="w-12 text-right">التوقيع:</span> <span class="flex-1 text-right">................................</span></p>
        </div>
      </div>
      
      <!-- Left: Approver -->
      <div class="space-y-3 flex flex-col items-end text-right">
        <p class="mb-2 font-bold">اعتماد (مدير عام شرطة المحافظة/الوحدة)</p>
        <div class="space-y-2 w-full max-w-[200px]">
          <p class="flex items-center"><span class="w-12 text-right">الاسم:</span> <span class="flex-1 text-right">................................</span></p>
          <p class="flex items-center"><span class="w-12 text-right">الرتبة:</span> <span class="flex-1 text-right">................................</span></p>
          <div class="flex items-center relative"><span class="w-12 text-right z-10 mt-1">التوقيع:</span> 
            <div class="flex-1 text-right relative z-10">
              <span class="leading-none">................................</span>
              <!-- Official Seal Area (Close to Signature) -->
              <div class="absolute bottom-[-10px] right-2 w-14 h-14 border-2 border-dashed border-gray-400 rounded-full flex items-center justify-center opacity-60 z-0 -rotate-12 pointer-events-none">
                <span class="text-gray-400 text-[8px] font-black text-center leading-tight">الختم<br>الرسمي</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Security Tracking Footer & QR Code -->
    <div class="flex items-center justify-between text-[7px] text-gray-500 font-medium border-t border-gray-400 pt-2 mt-4 leading-relaxed">
      <div class="space-y-0.5 text-right flex-1">
        <p>طُبع بواسطة: <span class="font-bold text-gray-800">مدير النظام</span> | بتاريخ: <span class="font-bold text-gray-800" dir="ltr">{{ printDate }}</span></p>
        <p>المرجع (REF): <span class="font-bold text-gray-800 font-mono tracking-wider">{{ refId }}</span></p>
      </div>
      
      <!-- QR Code Representation -->
      <div class="flex items-center gap-2 pr-4 border-r border-gray-300">
        <svg class="h-10 w-10 text-gray-900" viewBox="0 0 33 33" fill="currentColor" shape-rendering="crispEdges">
          <path d="M0 0h9v9H0zM2 2v5h5V2zM24 0h9v9h-9zM26 2v5h5V2zM0 24h9v9H0zM2 26v5h5v-5zM12 0h2v2h-2zM16 0h5v2h-5zM22 0h1v2h-1zM10 2h2v3h-2zM14 2h1v1h-1zM16 3h2v2h-2zM20 3h1v2h-1zM10 6h3v2h-3zM14 5h1v1h-1zM17 6h5v2h-5zM12 9h2v2h-2zM15 9h1v3h-1zM17 9h2v1h-2zM20 9h3v1h-3zM25 10h2v2h-2zM28 10h5v1h-5zM0 10h2v1H0zM3 10h2v2H3zM6 10h2v3H6zM9 10h2v2H9zM12 12h2v2h-2zM17 11h2v3h-2zM21 11h2v1h-2zM27 12h2v1h-2zM31 12h2v2h-2zM0 12h1v3H0zM2 13h2v1H2zM9 13h2v1H9zM20 13h1v3h-1zM23 13h3v2h-3zM29 14h2v2h-2zM4 14h1v1H4zM6 14h1v3H6zM8 15h3v2H8zM12 15h1v1h-1zM14 15h2v3h-2zM18 15h1v2h-1zM27 15h1v2h-1zM32 15h1v3h-1zM1 16h2v2H1zM4 16h1v2H4zM12 17h1v1h-1zM17 17h1v3h-1zM20 17h2v2h-2zM23 16h2v1h-2zM26 18h2v2h-2zM29 17h2v1h-2zM7 18h1v3H7zM9 18h2v1H9zM12 19h4v2h-4zM19 19h1v1h-1zM22 18h3v1h-3zM28 19h1v3h-1zM31 19h2v1h-2zM0 20h2v2H0zM3 20h3v1H3zM9 20h2v2H9zM17 21h2v1h-2zM20 20h1v2h-1zM23 20h1v1h-1zM25 21h2v2h-2zM30 21h3v2h-3zM2 23h2v1H2zM5 22h3v2H5zM11 22h2v1h-2zM14 21h2v2h-2zM18 23h3v1h-3zM22 22h2v1h-2zM25 24h1v1h-1zM27 24h5v2h-5zM10 24h3v1h-3zM14 24h2v2h-2zM17 25h1v1h-1zM19 25h2v2h-2zM22 24h2v3h-2zM25 26h1v3h-1zM28 27h2v2h-2zM31 26h2v1h-2zM10 26h1v2h-1zM12 27h2v2h-2zM15 26h1v2h-1zM17 27h2v2h-2zM20 28h1v3h-1zM22 28h1v1h-1zM27 28h1v1h-1zM32 28h1v2h-1zM10 29h2v2h-2zM13 30h1v3h-1zM15 29h2v1h-2zM18 30h1v3h-1zM22 30h2v1h-2zM25 30h2v3h-2zM29 31h3v2h-3zM10 32h2v1h-2zM15 31h2v2h-2zM21 32h3v1h-3z" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const printDate = ref('')
const refId = ref('')

onMounted(() => {
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-GB', { year: 'numeric', month: '2-digit', day: '2-digit' }).split('/').reverse().join('/')
  const timeStr = now.toLocaleTimeString('ar-YE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  printDate.value = `${dateStr}، ${timeStr}`
  
  const randomStr = Math.random().toString(36).substring(2, 8).toUpperCase()
  refId.value = `DOC-HR-${randomStr}`
})
</script>
