<template>
  <div class="hidden print:block mt-8 print:break-inside-avoid" style="page-break-inside: avoid; break-inside: avoid; font-family: 'Arial', 'Tajawal', sans-serif;">
    <div class="border-2 border-gray-900 rounded-xl p-4 grid grid-cols-3 gap-6 text-[0.85rem] font-bold text-gray-900 text-center relative mb-3">
      <!-- Frame Title -->
      <div class="absolute -top-3 right-6 bg-white px-2 text-[0.85rem] font-bold text-gray-900 print:bg-white">التوقيعات والاعتمادات</div>
      
      <!-- Right: Preparer -->
      <div class="space-y-3 flex flex-col items-start text-right">
        <p class="mb-2 font-bold whitespace-pre-wrap">{{ signatures.preparer.title }}</p>
        <div class="space-y-2 w-full max-w-[200px]">
          <p class="flex items-center"><span class="w-12 text-right">الاسم:</span> <span class="flex-1 text-right">{{ signatures.preparer.name || '................................' }}</span></p>
          <p class="flex items-center"><span class="w-12 text-right">الرتبة:</span> <span class="flex-1 text-right">{{ signatures.preparer.rank || '................................' }}</span></p>
          <p class="flex items-center"><span class="w-12 text-right">التوقيع:</span> <span class="flex-1 text-right">................................</span></p>
        </div>
      </div>
      
      <!-- Center: Reviewer -->
      <div class="space-y-3 flex flex-col items-center text-center">
        <p class="mb-2 font-bold whitespace-pre-wrap">{{ signatures.reviewer.title }}</p>
        <div class="space-y-2 w-full max-w-[200px]">
          <p class="flex items-center"><span class="w-12 text-right">الاسم:</span> <span class="flex-1 text-right">{{ signatures.reviewer.name || '................................' }}</span></p>
          <p class="flex items-center"><span class="w-12 text-right">الرتبة:</span> <span class="flex-1 text-right">{{ signatures.reviewer.rank || '................................' }}</span></p>
          <p class="flex items-center"><span class="w-12 text-right">التوقيع:</span> <span class="flex-1 text-right">................................</span></p>
        </div>
      </div>
      
      <!-- Left: Approver -->
      <div class="space-y-3 flex flex-col items-end text-right">
        <p class="mb-2 font-bold whitespace-pre-wrap">{{ signatures.approver.title }}</p>
        <div class="space-y-2 w-full max-w-[200px]">
          <p class="flex items-center"><span class="w-12 text-right">الاسم:</span> <span class="flex-1 text-right">{{ signatures.approver.name || '................................' }}</span></p>
          <p class="flex items-center"><span class="w-12 text-right">الرتبة:</span> <span class="flex-1 text-right">{{ signatures.approver.rank || '................................' }}</span></p>
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
        <p>طُبع بواسطة: <span class="font-bold text-gray-800">{{ userName }}</span> | بتاريخ: <span class="font-bold text-gray-800" dir="ltr">{{ printDate }}</span></p>
        <p>المرجع (REF): <span class="font-bold text-gray-800 font-mono tracking-wider">{{ refId }}</span> <span class="text-gray-400 px-2">|</span> كود التوثيق (HASH): <span class="font-bold text-gray-700 font-mono tracking-widest text-[6px]">{{ secHash }}</span></p>
      </div>
      
      <!-- Functional QR Code -->
      <div class="flex items-center gap-2 pr-4 border-r border-gray-300">
        <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://moi.gov.ye/verify/${refId}`" class="h-[65px] w-[65px] object-contain grayscale" alt="QR Code" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

defineProps<{
  signatures: {
    approver: { title: string, rank: string, name: string },
    reviewer: { title: string, rank: string, name: string },
    preparer: { title: string, rank: string, name: string }
  }
}>()

const authStore = useAuthStore()

const userName = computed(() => {
  return authStore.displayName || (authStore.user as any)?.full_name || 'مدير النظام'
})

const printDate = ref('')
const refId = ref('')
const secHash = ref('')

onMounted(() => {
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-GB', { year: 'numeric', month: '2-digit', day: '2-digit' }).split('/').reverse().join('/')
  const timeStr = now.toLocaleTimeString('ar-YE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  printDate.value = `${dateStr}، ${timeStr}`
  
  const randomStr = Math.random().toString(36).substring(2, 8).toUpperCase()
  refId.value = `MEMO-${randomStr}`
  
  // Generate a mock SHA-like security hash for the print
  const chars = '0123456789abcdef'
  let hash = ''
  for(let i=0; i<40; i++) hash += chars[Math.floor(Math.random() * chars.length)]
  secHash.value = hash
})
</script>
