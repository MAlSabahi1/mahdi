<template>
  <div class="hidden print:block mb-4 relative">
    
    <!-- Top Header Columns -->
    <div class="grid grid-cols-3 gap-2 pt-4 px-6 items-start relative">
      
      <!-- Right: Arabic Info -->
      <div class="text-right space-y-1.5 leading-tight">
        <img src="/images/yemen_calligraphy_cropped.png" alt="الجمهورية اليمنية" class="h-10 w-auto inline-block mb-1 print:h-10" />
        <h3 class="font-bold text-[14pt] leading-tight font-sans text-gray-900">{{ issuerLine1 || 'وزارة الداخلية' }}</h3>
        
        <template v-if="issuerLine2 || issuerLine3">
          <h4 v-if="issuerLine2" class="font-bold text-[13pt] leading-tight font-sans text-gray-800">{{ issuerLine2 }}</h4>
          <h4 v-if="issuerLine3" class="font-bold text-[13pt] leading-tight font-sans text-gray-800">{{ issuerLine3 }}</h4>
        </template>
        <template v-else-if="isCentralAdmin">
          <h4 class="font-bold text-[13pt] leading-tight font-sans text-gray-800">قطاع الموارد البشرية</h4>
          <h4 class="font-bold text-[13pt] leading-tight font-sans text-gray-800">الإدارة العامة للقوى البشرية</h4>
        </template>
        <template v-else>
          <h4 class="font-bold text-[13pt] leading-tight font-sans text-gray-800">شرطة م / {{ governorateName }}</h4>
          <h4 class="font-bold text-[13pt] leading-tight font-sans text-gray-800">إدارة القوى البشرية</h4>
        </template>

        <!-- Document Info Box (Below Arabic Side - ONLY if bilingual) -->
        <div v-if="bilingual" class="text-[12pt] font-bold mt-4 font-sans space-y-1.5">
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الرقـــــــــــــم/</span>
            <span :class="{'tracking-widest': String(referenceNo).includes('...')}" class="text-blue-900">{{ referenceNo }}</span>
          </div>
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">التاريــــــــــــخ/</span>
            <span :class="{'tracking-widest': String(docDate).includes('...')}" class="text-blue-900">{{ docDate }}</span>
          </div>
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الموافـــــــــــق/</span>
            <span :class="{'tracking-widest': String(correspondingDate).includes('...')}" class="text-blue-900">{{ correspondingDate }}</span>
          </div>
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">المرفقـــــــــات/</span>
            <span :class="{'tracking-widest': String(attachments).includes('...')}" class="text-blue-900">{{ attachments }}</span>
          </div>
        </div>
      </div>

      <!-- Center: Emblem Image & Bismillah -->
      <div class="flex flex-col justify-center items-center pt-1">
        <img src="/images/bismillah_cropped.png" alt="بسم الله الرحمن الرحيم" class="h-[2.5rem] w-auto max-w-full object-contain print:h-[2.5rem] mb-0 relative z-10" />
        <img src="/images/logo/yemen_logo_clean.png" alt="شعار الجمهورية" class="h-[125px] w-auto object-contain print:h-[125px] -mt-3 relative z-0" />
      </div>

      <!-- Left: English Info (If Bilingual) -->
      <div v-if="bilingual" class="text-left space-y-1 pt-2" dir="ltr">
        <h2 class="font-bold text-[13pt] leading-tight tracking-wide font-serif text-gray-900">REPUBLIC OF YEMEN</h2>
        <h3 class="font-semibold text-[12pt] leading-tight font-serif text-gray-900">Ministry of Interior</h3>
        <h4 v-if="isCentralAdmin" class="font-semibold text-[11pt] leading-tight font-serif text-gray-800">Human Resources Sector</h4>
        <h4 v-else class="font-semibold text-[11pt] leading-tight font-serif text-gray-800">Police Department</h4>
      </div>

      <!-- Left: Document Info Box (If Arabic Only) -->
      <div v-else class="flex justify-end pt-2 pl-2 text-[12pt] font-bold font-sans" dir="rtl">
        <div class="space-y-1.5 leading-tight">
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الرقـــــــــــــم/</span>
            <span :class="{'tracking-widest': String(referenceNo).includes('...')}" class="text-blue-900">{{ referenceNo }}</span>
          </div>
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">التاريــــــــــــخ/</span>
            <span :class="{'tracking-widest': String(docDate).includes('...')}" class="text-blue-900">{{ docDate }}</span>
          </div>
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الموافـــــــــــق/</span>
            <span :class="{'tracking-widest': String(correspondingDate).includes('...')}" class="text-blue-900">{{ correspondingDate }}</span>
          </div>
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">المرفقـــــــــات/</span>
            <span :class="{'tracking-widest': String(attachments).includes('...')}" class="text-blue-900">{{ attachments }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Thick Separator Line -->
    <div class="px-2 -mt-4 relative z-10">
      <div class="w-full border-b-[3px] border-black mb-[2px]"></div>
      <div class="w-full border-b-[1.5px] border-black mb-4"></div>
      
      <!-- Security / Intelligence Badge (Breaks the lines) -->
      <div v-if="securityLevel && securityLevel !== 'NORMAL'" class="absolute top-[-9px] left-0 w-full flex justify-center pointer-events-none print:top-[-9px]">
        <div class="bg-white px-4 py-0 font-black text-[11pt] tracking-widest border-[2px] rounded-sm print:bg-white" 
             :style="`box-shadow: 0 0 0 4px white; border-color: ${currentSecurityColor}; color: ${currentSecurityColor};`">
          {{ currentSecurityText }}
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  referenceNo: { type: String, default: '........................' },
  docDate: { type: String, default: '' },
  correspondingDate: { type: String, default: '........................' },
  attachments: { type: String, default: '........................' },
  bilingual: { type: Boolean, default: false },
  securityLevel: { type: String, default: 'TOP_SECRET' },
  securityCustomText: { type: String, default: '' },
  securityCustomColor: { type: String, default: '#991b1b' },
  issuerLine1: { type: String, default: '' },
  issuerLine2: { type: String, default: '' },
  issuerLine3: { type: String, default: '' }
})

const securityLabelAr = computed(() => {
  switch (props.securityLevel) {
    case 'SECRET': return 'ســـــــــري'
    case 'TOP_SECRET': return 'ســـري للغايـــة'
    case 'URGENT': return 'عـــاجـــل فـــوراً'
    default: return ''
  }
})

const currentSecurityText = computed(() => {
  if (props.securityLevel === 'CUSTOM') return props.securityCustomText || 'مخصص'
  return securityLabelAr.value
})

const currentSecurityColor = computed(() => {
  if (props.securityLevel === 'CUSTOM') return props.securityCustomColor || '#991b1b'
  return '#991b1b' // Default red
})

const authStore = useAuthStore()

// Determine if the user is a central admin (Ministry level)
const isCentralAdmin = computed(() => {
  const user = authStore.user as any
  if (!user) return false
  if (user.is_superuser) return true
  
  const roleCode = user.role?.code || user.authz_profile?.role_code
  const supervisesAll = user.supervises_all || user.authz_profile?.supervises_all
  
  return roleCode === 'SYSTEM_ADMIN' || supervisesAll
})

// Extract the governorate name
const governorateName = computed(() => {
  const user = authStore.user as any
  if (!user) return '............'
  
  if (user.city) return user.city

  const roleName = user.role?.name || user.authz_profile?.role_name || ''
  const displayName = authStore.displayName || ''
  
  const textToParse = displayName.includes('أمن') || displayName.includes('محافظة') ? displayName : roleName
  
  if (textToParse) {
    if (textToParse.includes('محافظة')) {
      return textToParse.split('محافظة')[1].trim()
    } else if (textToParse.includes('أمن')) {
      return textToParse.split('أمن')[1].trim()
    }
    return textToParse
  }
  
  return '............'
})
</script>
