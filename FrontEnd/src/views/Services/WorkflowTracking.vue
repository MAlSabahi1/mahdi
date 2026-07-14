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
                selectedWorkflow?.id === tx.id 
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
        <div v-if="selectedWorkflow" class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs lg:col-span-2 space-y-5">
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
        <div v-else class="lg:col-span-2 flex justify-center items-center h-64 text-gray-400 font-bold bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm">
          لا توجد معاملات نشطة للتتبع.
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'

const servicesStore = useServicesStore()

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

const activeWorkflows = ref<Workflow[]>([])
const selectedWorkflow = ref<Workflow | null>(null)

onMounted(async () => {
  await servicesStore.fetchForms()
  
  // Filter out drafts and maybe rejected?
  const forms = servicesStore.forms.filter((f: any) => f.status !== 'draft')
  
  activeWorkflows.value = forms.map((form: any) => {
    // Determine steps based on status and timestamps
    
    // Step 1: Submission
    const s1: WorkflowStep = {
      title: 'إنشاء الطلب',
      desc: 'تم إنشاء المعاملة ورفع المرفقات.',
      status: form.submitted_at ? 'completed' : 'pending',
      timestamp: form.submitted_at ? new Date(form.submitted_at).toLocaleString('en-GB') : undefined
    }

    // Step 2: Services Approval
    const s2: WorkflowStep = {
      title: 'تدقيق قسم الخدمات',
      desc: 'مراجعة أولية ومطابقة المرفقات للطلب.',
      status: form.services_approved_at ? 'completed' : (form.status === 'pending_services' ? 'current' : 'pending'),
      timestamp: form.services_approved_at ? new Date(form.services_approved_at).toLocaleString('en-GB') : undefined
    }

    // Step 3: HR Director Approval
    const s3: WorkflowStep = {
      title: 'اعتماد مدير إدارة القوى البشرية',
      desc: 'تدقيق الأثر الوظيفي والمالي للمنتسب.',
      status: form.hr_approved_at ? 'completed' : (form.status === 'pending_hr' ? 'current' : 'pending'),
      timestamp: form.hr_approved_at ? new Date(form.hr_approved_at).toLocaleString('en-GB') : undefined
    }

    // Step 4: Director Approval
    const s4: WorkflowStep = {
      title: 'اعتماد المدير العام للمحافظة',
      desc: 'مصادقة المدير العام وتطبيق الأثر على السجل.',
      status: form.status === 'approved' ? 'completed' : (form.status === 'pending_director' ? 'current' : 'pending'),
      timestamp: form.director_approved_at ? new Date(form.director_approved_at).toLocaleString('en-GB') : undefined
    }
    
    // Last action mapping
    const actionMap: any = {
      'pending_services': 'عند رئيس قسم الخدمات',
      'pending_hr': 'عند مدير إدارة القوى البشرية',
      'pending_director': 'عند المدير العام للمحافظة',
      'approved': 'معتمد نهائياً',
      'rejected': 'مرفوض',
      'returned': 'مُرجع للتعديل',
      'in_progress': 'قيد الإجراء',
    }

    return {
      id: form.id,
      txNumber: `TX-${form.id.toString().padStart(6, '0')}`,
      title: form.form_type,
      governorate: form.personnel_details?.full_name || form.personnel,
      lastAction: actionMap[form.status] || form.status,
      steps: [s1, s2, s3, s4]
    }
  })

  if (activeWorkflows.value.length > 0) {
    selectedWorkflow.value = activeWorkflows.value[0]
  }
})
</script>
