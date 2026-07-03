<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تتبع سير الموافقات والاعتمادات الجارية" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          تتبع سير الموافقات (Workflow Tracker)
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          لوحة تتبع بصرية لمراحل تدقيق واعتماد المعاملات الجارية عبر الهيكل القيادي وسلسلة الموافقات المشتركة.
        </p>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Active Tracked Transactions -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-1 space-y-4">
          <h3 class="text-xs font-black text-gray-900 dark:text-white mb-2">المعاملات النشطة تحت التتبع</h3>
          
          <div class="space-y-2.5">
            <div 
              v-for="tx in activeWorkflows" 
              :key="tx.id"
              @click="selectedWorkflow = tx"
              :class="[
                selectedWorkflow.id === tx.id 
                  ? 'border-brand-500 bg-brand-50/50 dark:bg-brand-950/20' 
                  : 'border-gray-150 dark:border-gray-800 hover:bg-gray-50/30'
              ]"
              class="p-3 border rounded-xl cursor-pointer transition-all flex flex-col gap-1.5"
            >
              <div class="flex justify-between items-center">
                <span class="font-mono text-[10px] font-bold text-gray-400">{{ tx.txNumber }}</span>
                <span class="text-[9px] font-bold bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400 px-2 py-0.5 rounded">
                  قيد المراجعة
                </span>
              </div>
              <h4 class="text-xs font-black text-gray-800 dark:text-gray-200">{{ tx.title }}</h4>
              <p class="text-[9px] text-gray-450">{{ tx.governorate }} • آخر إجراء: {{ tx.lastAction }}</p>
            </div>
          </div>
        </div>

        <!-- Workflow Visual Timeline -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs lg:col-span-2 space-y-5">
          <div class="flex justify-between items-center border-b border-gray-150 dark:border-gray-800 pb-3">
            <div>
              <h3 class="text-xs font-black text-gray-900 dark:text-white">تفاصيل مسار الموافقات التتابعي</h3>
              <p class="text-[9px] text-gray-400 mt-0.5">تتبع مراحل التدقيق من المنشئ (Maker) وصولاً للاعتماد النهائي والمطابقة.</p>
            </div>
            <span class="text-[9px] bg-brand-50 dark:bg-brand-950/40 text-brand-650 dark:text-brand-400 font-mono px-2 py-0.5 rounded font-bold">
              {{ selectedWorkflow.txNumber }}
            </span>
          </div>

          <!-- Vertical Timeline Steps -->
          <div class="relative pl-6 space-y-6">
            <!-- Timeline vertical line -->
            <div class="absolute right-[15px] top-2 bottom-2 w-0.5 bg-gray-200 dark:bg-gray-800"></div>

            <div 
              v-for="(step, idx) in selectedWorkflow.steps" 
              :key="idx" 
              class="relative flex items-start gap-4 pr-8 text-right"
            >
              <!-- Timeline Dot -->
              <span 
                :class="[
                  step.status === 'completed' 
                    ? 'bg-emerald-500 text-white' 
                    : step.status === 'current' 
                      ? 'bg-amber-500 text-white border-4 border-amber-100 dark:border-amber-950' 
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-400'
                ]"
                class="absolute right-0 top-0.5 h-8 w-8 rounded-full flex items-center justify-center font-bold text-xs shadow-theme-xs z-10 transition-colors"
              >
                <span v-if="step.status === 'completed'">✓</span>
                <span v-else-if="step.status === 'current'">●</span>
                <span v-else>{{ idx + 1 }}</span>
              </span>

              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <h4 class="text-xs font-black text-gray-800 dark:text-gray-200">{{ step.title }}</h4>
                  <span 
                    :class="[
                      step.status === 'completed' 
                        ? 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20' 
                        : step.status === 'current' 
                          ? 'text-amber-600 bg-amber-50 dark:bg-amber-950/20' 
                          : 'text-gray-400 bg-gray-50 dark:bg-gray-900'
                    ]"
                    class="text-[9px] font-bold px-1.5 py-0.5 rounded"
                  >
                    {{ step.status === 'completed' ? 'معتمد' : step.status === 'current' ? 'جارٍ التدقيق' : 'انتظار' }}
                  </span>
                </div>
                <p class="text-[10px] text-gray-400 leading-relaxed">{{ step.desc }}</p>
                <p v-if="step.timestamp" class="text-[9px] text-gray-400 font-mono mt-0.5">تاريخ الإجراء: {{ step.timestamp }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

interface WorkflowStep {
  title: string
  desc: string
  status: 'completed' | 'current' | 'pending'
  timestamp?: string
}

interface Workflow {
  id: number
  txNumber: string
  title: string
  governorate: string
  lastAction: string
  steps: WorkflowStep[]
}

const activeWorkflows = ref<Workflow[]>([
  {
    id: 1,
    txNumber: 'TX-2026-0089',
    title: 'طلب تسوية رتبة عسكرية (كرت 01)',
    governorate: 'عدن',
    lastAction: 'اعتماد شؤون الأفراد بالفرع',
    steps: [
      { title: 'إنشاء الطلب ورفع المرفقات', desc: 'تم إنشاء المعاملة ورفع شهادات تسوية الرتب العسكرية للباك اند.', status: 'completed', timestamp: '2026-07-01 09:12' },
      { title: 'تدقيق شؤون الأفراد والضباط بالمديرية', desc: 'مراجعة ومطابقة الملف المرفوع وتأكيد التوزيع الوظيفي.', status: 'completed', timestamp: '2026-07-02 11:30' },
      { title: 'اعتماد الإدارة العامة لشؤون الموظفين (ديوان الوزارة)', desc: 'يجري التحقق من السجل العسكري الموحد وقواعد البيانات المتقاطعة.', status: 'current' },
      { title: 'المصادقة المالية والمطابقة النهائية', desc: 'تحديث الراتب الأساسي والبدلات في كشوفات الصرف وإقفال الكرت.', status: 'pending' }
    ]
  },
  {
    id: 2,
    txNumber: 'TX-2026-0092',
    title: 'طلب علاوة رتبة جديدة (كرت 02)',
    governorate: 'تعز',
    lastAction: 'رفع الاستمارات والمرفقات',
    steps: [
      { title: 'إنشاء الطلب ورفع المرفقات', desc: 'تم إدراج طلب علاوة الرتبة الجديدة بالملف المالي.', status: 'completed', timestamp: '2026-07-02 14:00' },
      { title: 'تدقيق شؤون الأفراد والضباط بالمديرية', desc: 'مراجعة المرفقات المالية وتحديد الراتب الأساسي والبدلة الحالية.', status: 'current' },
      { title: 'اعتماد الإدارة العامة لشؤون الموظفين (ديوان الوزارة)', desc: 'مراجعة الأثر الرجعي المالي والتسويات.', status: 'pending' },
      { title: 'المصادقة المالية والمطابقة النهائية', desc: 'صرف الفروق المالية وإدراجها بكشف الشهر القادم.', status: 'pending' }
    ]
  }
])

const selectedWorkflow = ref<Workflow>(activeWorkflows.value[0])
</script>
