<template>
  <admin-layout>
    <div class="space-y-6">
      
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('services.reconciliation_title') || 'مهام المطابقة (Reconciliation)' }}</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t('services.reconciliation_subtitle') || 'تتبع ومعالجة الاختلافات والتعارضات في البيانات المرفوعة.' }}
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="isModalOpen = true"
            class="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors"
          >
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            {{ $t('services.create_reconciliation') || 'إنشاء مهمة مطابقة جديدة' }}
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div v-if="servicesStore.loading && servicesStore.reconciliationTasks.length === 0" class="flex justify-center p-8">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="servicesStore.reconciliationTasks.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="mb-4 rounded-full bg-gray-50 p-4 dark:bg-gray-800 shadow-theme-xs">
            <svg class="h-10 w-10 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">لا توجد مهام مطابقة</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 text-center">لم يتم إنشاء أي مهام مطابقة حتى الآن.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-start">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">رقم المهمة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">اسم المهمة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">النوع</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الحالة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">بواسطة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">تاريخ الإنشاء</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="task in servicesStore.reconciliationTasks" :key="task.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td class="px-5 py-4 text-sm font-medium text-gray-900 dark:text-white">
                  #{{ task.id }}
                </td>
                <td class="px-5 py-4 text-sm text-gray-700 dark:text-gray-300">
                  {{ task.name }}
                </td>
                <td class="px-5 py-4">
                  <span class="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10 dark:bg-blue-500/10 dark:text-blue-400 dark:ring-blue-500/20">
                    {{ task.task_type === 'monthly_salary' ? 'راتب شهري' : task.task_type }}
                  </span>
                </td>
                <td class="px-5 py-4">
                  <span v-if="task.status === 'pending'" class="inline-flex items-center rounded-full bg-warning-50 px-2 py-1 text-xs font-medium text-warning-700 ring-1 ring-inset ring-warning-600/20 dark:bg-warning-500/10 dark:text-warning-400 dark:ring-warning-500/20">
                    <svg class="mr-1.5 h-2 w-2 text-warning-500 animate-pulse" fill="currentColor" viewBox="0 0 8 8"><circle cx="4" cy="4" r="3" /></svg>
                    قيد المعالجة
                  </span>
                  <span v-else-if="task.status === 'completed'" class="inline-flex items-center rounded-full bg-success-50 px-2 py-1 text-xs font-medium text-success-700 ring-1 ring-inset ring-success-600/20 dark:bg-success-500/10 dark:text-success-400 dark:ring-success-500/20">
                    <svg class="mr-1.5 h-2 w-2 text-success-500" fill="currentColor" viewBox="0 0 8 8"><circle cx="4" cy="4" r="3" /></svg>
                    مكتملة (بانتظار القرار)
                  </span>
                  <span v-else-if="task.status === 'resolved'" class="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10 dark:bg-gray-800 dark:text-gray-400 dark:ring-gray-700">
                    تم الحل
                  </span>
                </td>
                <td class="px-5 py-4 text-sm text-gray-700 dark:text-gray-300">
                  {{ task.created_by?.username || 'مدير النظام' }}
                </td>
                <td class="px-5 py-4 text-sm text-gray-500 dark:text-gray-400" dir="ltr">
                  {{ formatDate(task.created_at) }}
                </td>
                <td class="px-5 py-4">
                  <router-link 
                    v-if="task.status === 'completed'"
                    :to="`/services/reconciliation/${task.id}`" 
                    class="text-brand-600 hover:text-brand-900 dark:text-brand-400 dark:hover:text-brand-300 font-medium text-sm"
                  >
                    استعراض وحل
                  </router-link>
                  <span v-else-if="task.status === 'pending'" class="text-xs text-gray-400">جاري التحليل...</span>
                  <router-link 
                    v-else
                    :to="`/services/reconciliation/${task.id}`" 
                    class="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300 font-medium text-sm"
                  >
                    عرض التفاصيل
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 backdrop-blur-sm transition-opacity p-4">
      <div class="relative w-full max-w-lg transform overflow-hidden rounded-2xl bg-white text-start shadow-xl transition-all dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
        <div class="bg-white px-6 pb-4 pt-6 dark:bg-gray-900">
          <div class="flex items-start justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
            <div>
              <h3 class="text-xl font-bold leading-6 text-gray-900 dark:text-white">{{ $t('services.create_reconciliation') || 'إنشاء مهمة مطابقة جديدة' }}</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ $t('services.create_reconciliation_subtitle') || 'قم برفع الكشف الذي يحتوي على اختلافات ليقوم النظام بتحليله.' }}</p>
            </div>
            <button @click="isModalOpen = false" class="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 dark:hover:bg-gray-800 dark:hover:text-gray-300">
              <span class="sr-only">إغلاق</span>
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" /></svg>
            </button>
          </div>
          <div class="mt-4 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('services.task_name') || 'اسم المهمة' }} <span class="text-error-500">*</span></label>
              <input type="text" v-model="newTask.name" :placeholder="$t('services.task_name_placeholder') || 'مثال: مطابقة رواتب شهر مايو'" class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('services.task_type') || 'نوع المطابقة' }} <span class="text-error-500">*</span></label>
              <div class="relative">
                <select v-model="newTask.taskType" class="block w-full appearance-none rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
                  <option value="salary">{{ $t('services.monthly_salary') || 'راتب شهري' }}</option>
                  <option value="strength">{{ $t('services.strength_reconciliation') || 'مطابقة القوة' }}</option>
                  <option value="courses">{{ $t('services.courses_reconciliation') || 'مطابقة الدورات' }}</option>
                </select>
                <span class="pointer-events-none absolute inset-y-0 ltr:right-0 rtl:left-0 flex items-center px-4 text-gray-500">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                </span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('services.match_key') || 'مفتاح المطابقة' }} <span class="text-error-500">*</span></label>
              <div class="relative">
                <select v-model="newTask.keyField" class="block w-full appearance-none rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
                  <option value="military_number">{{ $t('services.military_number') || 'الرقم العسكري (أساسي)' }}</option>
                  <option value="national_id">{{ $t('services.national_id') || 'الرقم الوطني' }}</option>
                </select>
                <span class="pointer-events-none absolute inset-y-0 ltr:right-0 rtl:left-0 flex items-center px-4 text-gray-500">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                </span>
              </div>
              <p class="mt-1 text-xs text-gray-500">{{ $t('services.match_key_hint') || 'الحقل الذي سيتم من خلاله ربط سجل الإكسل بسجل الموظف في النظام.' }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('services.excel_file') || 'ملف الإكسل' }} <span class="text-error-500">*</span></label>
              <input type="file" @change="handleFileSelect" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" class="block w-full text-sm text-gray-500 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 dark:file:bg-brand-900/30 dark:file:text-brand-400 dark:text-gray-400">
            </div>
            
            <!-- Poller Progress -->
            <div v-if="poller.active" class="mt-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  <svg class="h-4 w-4 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                  {{ $t('services.processing_file') || 'جاري رفع ومعالجة الملف...' }}
                </span>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ $t('services.processing_hint') || 'الرجاء الانتظار، يقوم الخادم بمقارنة آلاف السجلات لاستخراج الاختلافات.' }}</p>
            </div>
            
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 dark:bg-gray-800/50 flex flex-col sm:flex-row justify-end gap-3">
          <button 
            @click="isModalOpen = false" 
            :disabled="poller.active"
            class="inline-flex w-full justify-center rounded-lg bg-white px-4 py-2 text-sm font-medium text-gray-900 shadow-theme-xs ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:w-auto dark:bg-gray-800 dark:text-white dark:ring-gray-700 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors"
          >
            {{ $t('common.cancel') || 'إلغاء' }}
          </button>
          <button 
            @click="submitTask" 
            :disabled="!isFormValid || poller.active"
            class="inline-flex w-full justify-center rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 sm:w-auto focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 disabled:opacity-50 transition-colors"
          >
            {{ $t('services.start_reconciliation') || 'بدء المطابقة' }}
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useServicesStore } from '@/stores/services'
import Swal from 'sweetalert2'

const router = useRouter()
const servicesStore = useServicesStore()

const isModalOpen = ref(false)
const newTask = ref({
  name: '',
  taskType: 'salary',
  keyField: 'military_number',
  file: null as File | null
})

const poller = ref({
  active: false,
  taskId: '',
  intervalId: null as any
})

const isFormValid = computed(() => {
  return newTask.value.name.trim() !== '' && newTask.value.file !== null
})

onMounted(() => {
  fetchTasks()
})

async function fetchTasks() {
  await servicesStore.fetchReconciliationTasks()
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    newTask.value.file = target.files[0]
  }
}

async function submitTask() {
  if (!isFormValid.value || !newTask.value.file) return
  
  try {
    const response = await servicesStore.createReconciliationTask(
      newTask.value.file,
      newTask.value.name,
      newTask.value.taskType,
      newTask.value.keyField
    )
    
    if (response.data && response.data.celery_task_id) {
      startPoller(response.data.celery_task_id, response.data.task_id)
    } else {
      Swal.fire('نجاح', 'تم إنشاء المهمة بنجاح', 'success')
      isModalOpen.value = false
      fetchTasks()
    }
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل إنشاء المهمة', 'error')
  }
}

function startPoller(celeryTaskId: string, dbTaskId: number) {
  poller.value.active = true
  poller.value.taskId = celeryTaskId
  
  poller.value.intervalId = setInterval(async () => {
    try {
      const res = await servicesStore.checkTaskStatus(celeryTaskId)
      if (res.data) {
        if (res.data.status === 'SUCCESS') {
          stopPoller()
          isModalOpen.value = false
          Swal.fire({
            title: 'اكتملت المطابقة!',
            text: 'تم استخراج الاختلافات، سيتم توجيهك الآن لحلها.',
            icon: 'success',
            confirmButtonText: 'حسناً',
            confirmButtonColor: '#10b981'
          }).then(() => {
            router.push(`/services/reconciliation/${dbTaskId}`)
          })
        } else if (res.data.status === 'FAILURE') {
          stopPoller()
          Swal.fire('خطأ أثناء التحليل', res.data.error || 'فشلت معالجة الملف السحابية', 'error')
        }
      }
    } catch (err) {
      // Ignore intermediate errors
    }
  }, 2000)
}

function stopPoller() {
  if (poller.value.intervalId) {
    clearInterval(poller.value.intervalId)
  }
  poller.value.active = false
}

function formatDate(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ar-EG', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>
