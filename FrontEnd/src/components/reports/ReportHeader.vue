<template>
  <div class="hidden print:flex flex-col mb-2">
    <!-- Header Frame -->
    <div class="border-2 border-gray-900 rounded-xl p-3 pt-3 pb-0 flex justify-between items-start text-sm font-bold text-gray-900 relative">
      
      <!-- Right: Logo/Republic Info -->
      <div class="text-right w-1/3 space-y-1 pr-2 leading-tight">
        <img src="/images/yemen_calligraphy_cropped.png" alt="الجمهورية اليمنية" class="h-8 w-auto inline-block mb-1 print:h-8" />
        <p class="text-base">وزارة الداخلية</p>
        
        <template v-if="isCentralAdmin">
          <p>وكيل قطاع الموارد البشرية</p>
          <p>الإدارة العامة للقوى البشرية</p>
          <p>لجنة بناء الامتدادات</p>
        </template>
        
        <template v-else>
          <p>شرطة م / {{ governorateName }}</p>
          <p>إدارة القوى البشرية</p>
        </template>
      </div>
      
      <!-- Center: Emblem Image & Bismillah -->
      <div class="text-center w-1/3 flex flex-col justify-center items-center">
        <img src="/images/bismillah_cropped.png" alt="بسم الله الرحمن الرحيم" class="h-7 w-auto max-w-full object-contain print:h-7 mb-1 scale-[1.15] relative z-20" />
        <img src="/images/logo/yemen_logo_clean.png" alt="شعار الجمهورية" class="h-auto max-h-[5.5rem] w-auto max-w-full object-contain print:max-h-[5.5rem] scale-[1.35] origin-top -translate-y-2 relative z-10" />
      </div>
      
      <!-- Left: Document Info -->
      <div class="w-1/3 flex justify-end pl-2 pt-1">
        <div class="space-y-1 text-base leading-tight font-bold">
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الـرقـــــــــم/</span>
            <span class="tracking-widest">........................</span>
          </div>
          
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">التاريــــــــخ/</span>
            <span>{{ formattedDate }}</span>
          </div>
          
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الــمـوافـــــق/</span>
            <span class="tracking-widest">........................</span>
          </div>
          
          <div class="flex items-center">
            <span class="w-[5.5rem] text-right">الـمـرفـقــــات/</span>
            <span class="tracking-widest">........................</span>
          </div>
        </div>
      </div>
      
    </div>

    <!-- Center Title -->
    <div class="mt-4 text-center">
      <h2 class="text-xl font-bold text-gray-900 border-b border-gray-900 inline-block pb-1 px-4">
        {{ title }} لشهر ( {{ displayMonth }} ) {{ displayYear }}م
      </h2>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

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

// Extract the governorate name from the role (e.g. "مدير أمن محافظة مأرب") or fallback to city
const governorateName = computed(() => {
  const user = authStore.user as any
  if (!user) return '............'
  
  if (user.city) return user.city

  const roleName = user.role?.name || user.authz_profile?.role_name || ''
  const displayName = authStore.displayName || ''
  
  // Clean up common prefixes from either roleName or displayName
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

const props = defineProps<{
  title: string
  selectedMonth?: string
}>()

const dateObj = new Date()
const arabicMonths = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']

const displayMonth = computed(() => {
  if (props.selectedMonth) {
    const parts = props.selectedMonth.split('-')
    if (parts.length === 2) {
      const m = parseInt(parts[1], 10) - 1
      if (m >= 0 && m < 12) return arabicMonths[m]
    }
  }
  return arabicMonths[dateObj.getMonth()]
})

const displayYear = computed(() => {
  if (props.selectedMonth) {
    const parts = props.selectedMonth.split('-')
    if (parts.length === 2) {
      return parts[0]
    }
  }
  return dateObj.getFullYear()
})

const formattedDate = computed(() => {
  const currentYear = dateObj.getFullYear()
  const d = String(dateObj.getDate()).padStart(2, '0')
  const m = String(dateObj.getMonth() + 1).padStart(2, '0')
  return `${d} / ${m} / ${currentYear} م`
})
</script>
