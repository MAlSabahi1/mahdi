<template>
  <div class="workflow-tracker" dir="rtl">

    <!-- ══ بانر المسودة (لم يُقدَّم بعد) ══ -->
    <div v-if="status === 'draft'" class="mb-4 flex items-start gap-3 rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 dark:border-gray-700 dark:bg-gray-800/50">
      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
      </svg>
      <div>
        <p class="text-sm font-black text-gray-700 dark:text-gray-300">مسودة — في انتظار التقديم</p>
        <p class="mt-0.5 text-xs text-gray-500 dark:text-gray-400">
          الطلب لم يُقدَّم بعد لدورة الاعتماد. اضغط <strong>تقديم الطلب</strong> لبدء سير العمل.
        </p>
      </div>
    </div>

    <!-- ══ بانر الخدمة الخارجية ══ -->
    <div v-if="isExternal && status !== 'draft'" class="mb-4 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 dark:border-amber-800/50 dark:bg-amber-900/20">
      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <div>
        <p class="text-sm font-black text-amber-800 dark:text-amber-200">خدمة خارجية — تتطلب موافقة وزارية</p>
        <p class="mt-0.5 text-xs text-amber-700 dark:text-amber-300">
          يجب <strong>طباعة الاستمارة وإرسالها للوزارة</strong> ثم <strong>رفع مستند القرار الوزاري</strong> قبل الاعتماد النهائي.
        </p>
      </div>
    </div>

    <!-- ══ مسار داخلي ══ -->
    <div v-if="!isExternal && steps.length > 0" class="relative">
      <div class="flex items-start gap-0">
        <div
          v-for="(step, idx) in internalSteps"
          :key="idx"
          class="relative flex flex-1 flex-col items-center gap-2"
        >
          <!-- خط الوصل -->
          <div class="relative flex w-full items-center">
            <div class="flex-1 h-1 rounded-l-none"
              :class="idx === 0 ? 'opacity-0' : getLineClass(idx)" />
            <!-- دائرة المرحلة -->
            <div
              class="relative z-10 flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full border-2 transition-all duration-300"
              :class="getCircleClass(idx, step)"
            >
              <!-- مكتملة -->
              <svg v-if="isCompleted(idx)" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <!-- حالية -->
              <span v-else-if="isCurrent(idx)" class="h-2.5 w-2.5 rounded-full bg-current animate-pulse" />
              <!-- رفض -->
              <svg v-else-if="isRejected && isCurrent(idx)" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <!-- قادمة -->
              <span v-else class="text-[10px] font-black">{{ idx + 1 }}</span>
            </div>
            <div class="flex-1 h-1 rounded-r-none"
              :class="idx === internalSteps.length - 1 ? 'opacity-0' : getLineClass(idx + 1)" />
          </div>

          <!-- اسم المرحلة -->
          <p class="px-1 text-center text-[10px] font-bold leading-tight transition-colors"
            :class="getTextClass(idx)">
            {{ step }}
          </p>
        </div>
      </div>
    </div>

    <!-- ══ مسار خارجي ══ -->
    <div v-if="isExternal" class="relative">
      <div class="flex items-start gap-0">
        <div
          v-for="(step, idx) in externalSteps"
          :key="idx"
          class="relative flex flex-1 flex-col items-center gap-2"
        >
          <div class="relative flex w-full items-center">
            <div class="flex-1 h-1" :class="idx === 0 ? 'opacity-0' : getExternalLineClass(idx)" />
            <div
              class="relative z-10 flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full border-2 transition-all"
              :class="getExternalCircleClass(idx)"
            >
              <!-- إنشاء -->
              <svg v-if="idx === 0 && isExternalStepDone(0)" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="idx === 0" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              <!-- طباعة -->
              <svg v-else-if="idx === 1 && isExternalStepDone(1)" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="idx === 1" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
              </svg>
              <!-- قرار الوزارة -->
              <svg v-else-if="idx === 2 && isExternalStepDone(2)" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="idx === 2" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <!-- معتمد -->
              <svg v-else-if="idx === 3" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="flex-1 h-1" :class="idx === externalSteps.length - 1 ? 'opacity-0' : getExternalLineClass(idx + 1)" />
          </div>
          <p class="px-1 text-center text-[10px] font-bold leading-tight" :class="getExternalTextClass(idx)">
            {{ step.label }}
            <span v-if="step.required && !isExternalStepDone(idx)" class="block text-[9px] text-amber-600 font-medium mt-0.5">{{ step.hint }}</span>
          </p>
        </div>
      </div>
    </div>

    <!-- ══ شريط الحالة السفلي ══ -->
    <div v-if="status === 'rejected'" class="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 dark:border-red-800/50 dark:bg-red-900/20 flex items-center gap-2">
      <div class="h-2 w-2 rounded-full bg-red-500 flex-shrink-0" />
      <p class="text-xs font-bold text-red-700 dark:text-red-300">مرفوض — {{ rejectionReason || 'تم رفض المعاملة' }}</p>
    </div>
    <div v-else-if="status === 'returned'" class="mt-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 dark:border-amber-800/50 dark:bg-amber-900/20 flex items-center gap-2">
      <div class="h-2 w-2 rounded-full bg-amber-500 flex-shrink-0" />
      <p class="text-xs font-bold text-amber-700 dark:text-amber-300">مُرجع للتعديل — بانتظار تصحيح البيانات أو إضافة المرفقات</p>
    </div>
    <div v-else-if="status === 'approved'" class="mt-3 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 dark:border-emerald-800/50 dark:bg-emerald-900/20 flex items-center gap-2">
      <div class="h-2 w-2 rounded-full bg-emerald-500 flex-shrink-0" />
      <p class="text-xs font-bold text-emerald-700 dark:text-emerald-300">✓ معتمد نهائياً — تم تحديث سجل الفرد</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface ExternalStep { label: string; required?: boolean; hint?: string }

const props = defineProps<{
  steps: string[]         // all_steps من الـ API
  currentStepIndex: number
  status: string
  isExternal: boolean
  isPrinted: boolean
  hasMinistryDoc: boolean
  rejectionReason?: string
}>()

const isRejected = computed(() => props.status === 'rejected')
const isApproved = computed(() => props.status === 'approved')

// ══ داخلي ══
const internalSteps = computed(() => {
  const base = props.steps.length > 0 ? props.steps : ['رئيس قسم الخدمات', 'مدير إدارة القوى البشرية', 'المدير العام للمحافظة']
  return ['إنشاء الطلب', ...base, 'معتمد نهائياً']
})

const isCompleted = (idx: number) => {
  if (isApproved.value) return true
  // idx=0 = إنشاء → دائماً مكتمل إذا وجد الطلب
  if (idx === 0) return true
  const workflowIdx = idx - 1 // offset: 0=create, 1..N=steps, N+1=approved
  return workflowIdx < props.currentStepIndex
}

const isCurrent = (idx: number) => {
  if (isApproved.value) return idx === internalSteps.value.length - 1
  if (idx === 0) return props.status === 'draft'
  const workflowIdx = idx - 1
  return workflowIdx === props.currentStepIndex && !isRejected.value
}

const getCircleClass = (idx: number, _step: string) => {
  if (isApproved.value) return 'border-emerald-500 bg-emerald-500 text-white'
  if (isRejected.value && isCurrent(idx)) return 'border-red-500 bg-red-500 text-white'
  if (isCompleted(idx)) return 'border-emerald-500 bg-emerald-500 text-white'
  if (isCurrent(idx)) return 'border-blue-500 bg-blue-50 text-blue-600 dark:bg-blue-900/30 shadow-[0_0_12px_rgba(59,130,246,0.4)]'
  return 'border-gray-200 bg-white text-gray-400 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-500'
}

const getLineClass = (idx: number) => {
  if (isApproved.value) return 'bg-emerald-400'
  const workflowIdx = idx - 1
  if (workflowIdx < props.currentStepIndex) return 'bg-emerald-400'
  if (workflowIdx === props.currentStepIndex) return 'bg-gradient-to-l from-gray-200 to-emerald-400 dark:from-gray-700'
  return 'bg-gray-200 dark:bg-gray-700'
}

const getTextClass = (idx: number) => {
  if (isApproved.value) return 'text-emerald-700 dark:text-emerald-400'
  if (isRejected.value && isCurrent(idx)) return 'text-red-600 dark:text-red-400'
  if (isCompleted(idx)) return 'text-emerald-700 dark:text-emerald-400'
  if (isCurrent(idx)) return 'text-blue-700 dark:text-blue-400'
  return 'text-gray-400 dark:text-gray-500'
}

// ══ خارجي ══
const externalSteps = computed<ExternalStep[]>(() => [
  { label: 'إنشاء الطلب' },
  { label: 'طباعة وإرسال للوزارة', required: !props.isPrinted, hint: '⚠ يجب الطباعة أولاً' },
  { label: 'رفع قرار الوزارة', required: !props.hasMinistryDoc, hint: '⚠ يجب رفع المستند' },
  { label: 'معتمد نهائياً' },
])

const isExternalStepDone = (idx: number) => {
  if (isApproved.value) return true
  if (idx === 0) return props.status !== 'draft'
  if (idx === 1) return props.isPrinted
  if (idx === 2) return props.hasMinistryDoc
  return false
}

const getExternalLineClass = (idx: number) => {
  if (isApproved.value) return 'bg-emerald-400'
  if (isExternalStepDone(idx - 1)) return 'bg-emerald-400'
  return 'bg-gray-200 dark:bg-gray-700'
}

const getExternalCircleClass = (idx: number) => {
  if (isApproved.value && idx === 3) return 'border-emerald-500 bg-emerald-500 text-white'
  if (isExternalStepDone(idx)) return 'border-emerald-500 bg-emerald-500 text-white'
  // المرحلة الحالية
  const isCurrentExt = (idx === 1 && !props.isPrinted && props.status !== 'draft') ||
                       (idx === 2 && props.isPrinted && !props.hasMinistryDoc) ||
                       (idx === 0 && props.status === 'draft')
  if (isCurrentExt) return 'border-amber-500 bg-amber-50 text-amber-600 dark:bg-amber-900/30 shadow-[0_0_12px_rgba(245,158,11,0.4)]'
  return 'border-gray-200 bg-white text-gray-400 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-500'
}

const getExternalTextClass = (idx: number) => {
  if (isApproved.value) return 'text-emerald-700 dark:text-emerald-400'
  if (isExternalStepDone(idx)) return 'text-emerald-700 dark:text-emerald-400'
  const isCurrentExt = (idx === 1 && !props.isPrinted && props.status !== 'draft') ||
                       (idx === 2 && props.isPrinted && !props.hasMinistryDoc) ||
                       (idx === 0 && props.status === 'draft')
  if (isCurrentExt) return 'text-amber-700 dark:text-amber-400'
  return 'text-gray-400 dark:text-gray-500'
}
</script>
