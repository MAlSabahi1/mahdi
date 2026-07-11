<template>
  <div class="hidden print:flex flex-col mb-6">
    <!-- Header Frame -->
    <div class="border-2 border-gray-900 rounded-xl p-4 pt-5 pb-3 flex justify-between items-center text-sm font-bold text-gray-900 relative">
      
      <!-- Right: Logo/Republic Info -->
      <div class="text-right w-1/3 space-y-1 pr-2 leading-tight">
        <p class="text-base">الجمهورية اليمنية</p>
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
      <div class="text-center w-1/3 flex flex-col justify-center items-center gap-2">
        <h1 class="text-lg font-bold text-gray-900" style="font-family: 'Amiri', 'Traditional Arabic', 'KFGQPC Uthman Taha Naskh', serif;">بسم الله الرحمن الرحيم</h1>
        <img src="/images/logo/yemen_logo_clean.png" alt="شعار الجمهورية" class="h-32 w-auto max-w-full object-contain print:h-32" />
      </div>
      
      <!-- Left: Document Info -->
      <div class="w-1/3 flex justify-end pl-2">
        <div class="space-y-1 text-base leading-tight">
          <div class="flex items-center gap-1">
            <span class="w-16 text-right font-bold">الرقم:</span>
            <span class="text-right tracking-widest">(....................)</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="w-16 text-right font-bold">التاريخ:</span>
            <span class="text-right">{{ formattedDate }}</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="w-16 text-right font-bold">المرفقات:</span>
            <span class="text-right tracking-widest">(....................)</span>
          </div>
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
