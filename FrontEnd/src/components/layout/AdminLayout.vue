<template>
  <div class="min-h-screen xl:flex print:block print:min-h-0 print:bg-white">
    <app-sidebar class="print:hidden" />
    <Backdrop class="print:hidden" />
    <div
      class="flex-1 transition-all duration-300 ease-in-out print:!ms-0 print:block"
      :class="[isExpanded || isHovered ? 'lg:ms-[290px]' : 'lg:ms-[90px]']"
    >
      <app-header class="print:hidden" />
      <div class="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6 space-y-5 print:p-0 print:m-0 print:space-y-0 print:max-w-none print:w-full">
        <!-- Prototype Notice Banner for Users & Permissions System -->
        <div 
          v-if="systemStore.currentSystem === 'users_permissions'"
          class="flex items-start gap-3 p-4 rounded-2xl border border-amber-200 bg-amber-50/50 dark:border-amber-900/30 dark:bg-amber-950/20 text-start"
          dir="rtl"
        >
          <div class="text-amber-600 dark:text-amber-400 shrink-0 mt-0.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h4 class="text-xs font-black text-amber-800 dark:text-amber-300">
              تنبيه التطوير والنمذجة الأولية
            </h4>
            <p class="text-[11px] text-amber-700 dark:text-amber-400 mt-1 leading-relaxed">
              تنويه: نظام الصلاحيات والتحقق المتقدم قيد التطوير الكامل حالياً. كافة الشاشات والوحدات المعروضة في هذا القسم هي نماذج أولية (Prototypes/Drafts) لغرض محاكاة الواجهات وتصميم تجربة المستخدم، وليست النسخة النهائية المكتملة.
            </p>
          </div>
        </div>

        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
import { useSidebar } from '@/composables/useSidebar'
import Backdrop from './Backdrop.vue'
import { useSystemStore } from '@/stores/system'

const { isExpanded, isHovered } = useSidebar()
const systemStore = useSystemStore()
</script>
