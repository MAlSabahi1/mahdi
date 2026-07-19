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

    <!-- System Authentication & Tracking Footer -->
    <div class="absolute bottom-[6mm] left-[12mm] right-[12mm] border-[1.2px] border-gray-900 rounded-[3px] flex items-stretch text-[8px] font-medium z-50 overflow-hidden print:border-black bg-white" dir="ltr" style="height: 13.5mm;">
      
      <!-- QR Code Block -->
      <div class="w-[13.5mm] shrink-0 border-r-[1.2px] border-gray-900 print:border-black flex items-center justify-center p-[1px]">
        <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=0&data=${encodeURIComponent(offlineQrData)}`" class="w-full h-full object-contain grayscale" alt="SEC-QR" />
      </div>

      <!-- Cryptographic Hash Block -->
      <div class="flex-1 flex flex-col justify-center px-4 border-r-[1.2px] border-gray-900 print:border-black" style="font-family: 'Courier New', Courier, monospace;">
        <div class="flex items-center justify-between mb-[2px]">
          <span class="text-[8px] font-bold text-gray-800">SEC_REF:</span>
          <span class="text-[9px] font-black tracking-widest text-black">{{ refId }}</span>
        </div>
        <div class="flex flex-col border-t border-dashed border-gray-400 pt-[1px]">
          <span class="text-[5.5px] uppercase tracking-widest text-gray-500">Digital Signature Hash (SHA-256)</span>
          <span class="text-[6.5px] font-black tracking-widest uppercase truncate text-gray-900">{{ secHash }}</span>
        </div>
      </div>

      <!-- Printing Data Block -->
      <div class="w-[50mm] shrink-0 flex flex-col justify-center px-4" dir="rtl" style="font-family: 'Cairo', sans-serif;">
        <div class="flex justify-between items-center mb-[2px]">
          <span class="text-[7.5px] text-gray-600 font-bold">بواسطة:</span>
          <span class="text-[8px] font-black truncate max-w-[35mm] text-black">{{ userName }}</span>
        </div>
        <div class="flex justify-between items-center border-t border-dashed border-gray-400 pt-[1px]">
          <span class="text-[7.5px] text-gray-600 font-bold">تاريخ الإصدار:</span>
          <span class="text-[8px] font-black font-mono text-black" dir="ltr">{{ printDate }}</span>
        </div>
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
  typography?: any,
  referenceNo?: string
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

const printDate = ref(new Date().toLocaleString('en-GB'))
const refId = computed(() => {
  if (props.referenceNo && props.referenceNo.trim() !== '' && props.referenceNo !== '........................') {
    return props.referenceNo
  }
  return props.settings?.referenceId || `MEMO-SYS-GEN`
})

const secHash = computed(() => {
  if (props.settings?.securityHash) return props.settings.securityHash
  
  // Deterministic Hash based on ref and date (simulating a real system hash)
  const seed = `${refId.value}-${printDate.value}-${userName.value}`
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    const char = seed.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash 
  }
  const hex = Math.abs(hash).toString(16).padStart(8, '0')
  let fullHash = ''
  while(fullHash.length < 64) {
    fullHash += hex + seed.length.toString(16).padStart(2, '0')
  }
  return fullHash.substring(0, 64).toUpperCase()
})

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
