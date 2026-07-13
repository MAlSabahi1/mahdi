<template>
  <div class="hidden print:flex flex-col w-full print:break-inside-avoid" :class="settings?.showLabels !== false ? 'mt-8' : ''" style="page-break-inside: avoid; break-inside: avoid; font-family: 'Arial', 'Tajawal', sans-serif;">
    
    <!-- DESIGN 1: Classic (With labels, dots, optional frame) -->
    <template v-if="settings?.showLabels !== false">
      <div v-if="computedSignatures.length > 0" :class="[
        settings?.showFrame !== false ? 'border-2 border-gray-900 rounded-xl p-4 mb-3' : 'pt-4 mb-3',
        'flex flex-row justify-between items-start text-[0.85rem] text-gray-900 text-center relative w-full',
        typography?.weight || 'font-bold'
      ]" :style="{ fontFamily: typography?.family || 'Arial, Tajawal, sans-serif', fontSize: getFontSize(typography?.size, 0.85), textDecoration: typography?.underline ? 'underline' : 'none' }">
        <!-- Frame Title -->
        <div v-if="settings?.showFrame !== false" class="absolute -top-3 right-6 bg-white px-2 text-[0.85rem] font-bold text-gray-900 print:bg-white" style="font-family: 'Arial', 'Tajawal', sans-serif;">التوقيعات والاعتمادات</div>
        
        <div v-for="(sig, index) in displaySignatures" :key="index" class="flex-1">
          <div class="w-full max-w-[220px] text-right" :class="getAlignmentClass(index, displaySignatures.length)">
            <p class="mb-2 font-bold whitespace-pre-wrap text-right">{{ sig.title }}</p>
            <div class="space-y-2 w-full text-right">
              <p class="flex items-center"><span class="w-12 text-right">الاسم</span> <span class="flex-1 text-right">{{ sig.name || '................................' }}</span></p>
              <p class="flex items-center"><span class="w-12 text-right">الرتبة</span> <span class="flex-1 text-right">{{ sig.rank || '................................' }}</span></p>
              <div class="flex items-center relative"><span class="w-12 text-right z-10 mt-1">التوقيع</span> 
                <div class="flex-1 text-right relative z-10">
                  <span class="leading-none">................................</span>
                  <!-- Official Seal Area -->
                  <div v-if="sig.showSeal" class="absolute bottom-[-10px] right-2 w-14 h-14 border-2 border-dashed border-gray-400 rounded-full flex items-center justify-center opacity-60 z-0 -rotate-12 pointer-events-none">
                    <span class="text-gray-400 text-[8px] font-black text-center leading-tight" style="font-family: 'Arial', sans-serif; text-decoration: none;">الختم<br>الرسمي</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- DESIGN 2: Plain (Completely separate, no frame, no dots) -->
    <template v-else>
      <div v-if="computedSignatures.length > 0" class="flex flex-row justify-between items-start pt-8 pb-4 w-full" :class="typography?.weight || 'font-bold'" :style="{ fontFamily: typography?.family || 'Arial, Tajawal, sans-serif', fontSize: getFontSize(typography?.size, 0.85), textDecoration: typography?.underline ? 'underline' : 'none', color: '#111827' }">
        <div v-for="(sig, index) in displaySignatures" :key="index" class="flex-1 flex flex-col gap-1 relative items-center text-center">
          <!-- Design 2: Free Text Style -->
          <template v-if="sig.freeText">
            <div class="ck-content signature-content text-[1.05em] leading-tight mt-2" v-html="sig.freeText"></div>
          </template>
          <div v-if="sig.showSeal" class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-16 h-16 border-2 border-dashed border-gray-400 rounded-full flex items-center justify-center opacity-60 z-0 -rotate-12 pointer-events-none" :class="index === 0 ? 'right-0 translate-x-0 left-auto' : index === displaySignatures.length - 1 ? 'left-0 translate-x-0 right-auto' : ''">
            <span class="text-gray-400 text-[8px] font-black text-center leading-tight" style="font-family: 'Arial', sans-serif; text-decoration: none;">الختم<br>الرسمي</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Security Tracking Footer & QR Code (Absolute Bottom) -->
    <div class="absolute bottom-2 left-8 right-8 flex items-center justify-between text-[7px] text-gray-500 font-medium border-t border-gray-400 pt-2 leading-relaxed z-50">
      <div class="space-y-0.5 text-right flex-1">
        <p>طُبع بواسطة: <span class="font-bold text-gray-800">{{ userName }}</span> | بتاريخ: <span class="font-bold text-gray-800" dir="ltr">{{ printDate }}</span></p>
        <p>المرجع (REF): <span class="font-bold text-gray-800 font-mono tracking-wider">{{ refId }}</span> <span class="text-gray-400 px-2">|</span> كود التوثيق (HASH): <span class="font-bold text-gray-700 font-mono tracking-widest text-[6px]">{{ secHash }}</span></p>
      </div>
      
      <!-- Functional QR Code (Cryptographic Token) -->
      <div class="flex items-center gap-2 pr-3 border-r border-gray-200 shrink-0">
        <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=1&data=${encodeURIComponent(offlineQrData)}`" class="h-[55px] w-[55px] min-w-[55px] min-h-[55px] object-contain grayscale shrink-0 opacity-90 mix-blend-multiply" alt="QR Code" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{
  signatures: any,
  settings?: any,
  typography?: any
}>()

const getFontSize = (size: number | undefined, defaultSize: number) => {
  if (!size) return `${defaultSize}rem`
  return `${size}rem`
}

const computedSignatures = computed(() => {
  if (Array.isArray(props.signatures)) {
    return props.signatures
  } else if (props.signatures) {
    // Migration for older formats
    return [
      { title: props.signatures.preparer?.title || '', rank: props.signatures.preparer?.rank || '', name: props.signatures.preparer?.name || '', showSeal: false },
      { title: props.signatures.reviewer?.title || '', rank: props.signatures.reviewer?.rank || '', name: props.signatures.reviewer?.name || '', showSeal: false },
      { title: props.signatures.approver?.title || '', rank: props.signatures.approver?.rank || '', name: props.signatures.approver?.name || '', showSeal: true }
    ]
  }
  return []
})

const displaySignatures = computed(() => {
  const sigs = [...computedSignatures.value]
  // Auto-fix loaded drafts: If the first item has the seal (Approver) and the last doesn't,
  // it means they are backwards. The approver should be on the left (last item).
  if (sigs.length > 1 && sigs[0]?.showSeal === true && sigs[sigs.length - 1]?.showSeal === false) {
    return sigs.reverse()
  }
  return sigs
})

const getAlignmentClass = (index: number, total: number) => {
  if (total === 1) return 'mx-auto'
  if (index === 0) return 'ml-auto mr-0' // Right side in RTL
  if (index === total - 1) return 'mr-auto ml-0' // Left side in RTL
  return 'mx-auto' // Center
}

const getTextAlignmentClass = (index: number, total: number) => {
  if (total === 1) return 'text-center'
  if (index === 0) return 'text-right'
  if (index === total - 1) return 'text-left'
  return 'text-center'
}

const authStore = useAuthStore()

const userName = computed(() => {
  return authStore.displayName || (authStore.user as any)?.full_name || 'مدير النظام'
})

const printDate = ref('')
const refId = ref('')
const secHash = ref('')

const offlineQrData = computed(() => {
  // TODO: [قيد التطوير] ميزة الباركود للاسترجاع الأرشيفي الداخلي.
  // تم وضع أساس الميزة الآن لتكون متوافقة مع أجهزة الفحص اليدوية (USB Barcode Scanners).
  // تقوم هذه الأجهزة بقراءة الباركود وكتابته كـ "نص مباشر" في خانة البحث في النظام المغلق.
  // لم تكتمل الميزة إلا الآن كقاعدة تصميم، وسيتم تفعيل دورة الاسترجاع في الـ Backend لاحقاً.
  return refId.value
})

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

<style>
/* CKEditor 5 Alignment & Font Fixes (Bulletproof) */
.ck-content .text-tiny { font-size: 0.7em !important; }
.ck-content .text-small { font-size: 0.85em !important; }
.ck-content .text-big { font-size: 1.4em !important; }
.ck-content .text-huge { font-size: 1.8em !important; }

.ck-content .text-align-left, .ck-content .text-left { text-align: left !important; display: block; }
.ck-content .text-align-center, .ck-content .text-center { text-align: center !important; display: block; }
.ck-content .text-align-right, .ck-content .text-right { text-align: right !important; display: block; }
.ck-content .text-align-justify, .ck-content .text-justify { text-align: justify !important; display: block; }

.signature-content p {
  width: 100% !important;
  margin: 0 !important;
  text-align: inherit;
}
.signature-content {
  text-align: center;
}
</style>
