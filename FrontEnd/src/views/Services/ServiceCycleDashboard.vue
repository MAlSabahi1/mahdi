<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('services.dashboard_title') || 'إدارة الكشوفات والخدمات'" />
    <div class="space-y-6">

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        
        <!-- Export Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
          <div class="border-b border-gray-100 bg-gray-50/50 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/50 flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-100 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('services.export_monthly_sheet') || 'تصدير كشوفة شهرية' }}</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ $t('services.export_subtitle') || 'تحميل ملف الإكسل الأصلي للتعديل عليه خارجياً' }}</p>
            </div>
          </div>
          
          <div class="p-6 space-y-5 flex-1 flex flex-col">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('personnel.governorate') || 'المديرية / الإدارة' }} <span class="text-error-500">*</span></label>
              <div class="relative">
                <select v-model="exportData.directorateId" class="block w-full appearance-none rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500">
                  <option value="">{{ $t('services.select_directorate') || 'اختر المديرية' }}</option>
                  <option v-for="dept in coreStore.centralDepartments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                </select>
                <span class="pointer-events-none absolute inset-y-0 ltr:right-0 rtl:left-0 flex items-center px-4 text-gray-500">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                </span>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('services.service_month') || 'شهر الخدمة' }} <span class="text-error-500">*</span></label>
              <input type="month" v-model="exportData.month" class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500" />
            </div>
            
            <div class="pt-4 mt-auto">
              <button 
                @click="handleExport" 
                :disabled="!exportData.directorateId || !exportData.month || isExporting"
                class="w-full flex justify-center items-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
              >
                <svg v-if="isExporting" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                {{ isExporting ? ($t('services.exporting') || 'جاري التجهيز والتحميل...') : ($t('services.export_sheet') || 'تصدير الكشوفة') }}
              </button>
            </div>
          </div>
        </div>

        <!-- Import Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
          <div class="border-b border-gray-100 bg-gray-50/50 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/50 flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('services.import_modified_sheet') || 'استيراد كشوفة معدلة' }}</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ $t('services.import_subtitle') || 'رفع الإكسل لإرسال التعديلات إلى شاشة (المراجعة)' }}</p>
            </div>
          </div>
          
          <div class="p-6 flex-1 flex flex-col">
            
            <div v-if="importTask.active" class="flex-1 flex flex-col items-center justify-center text-center space-y-4 py-8">
              <svg class="h-12 w-12 text-brand-500 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <div>
                <h4 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('services.processing_file') || 'جاري معالجة الملف السحابية...' }}</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ $t('services.processing_subtitle') || 'يتم الآن قراءة السجلات ومطابقتها، يرجى الانتظار وعدم إغلاق الصفحة.' }}</p>
              </div>
              
              <!-- Progress Bar -->
              <div class="w-full max-w-xs mt-4">
                <div class="flex justify-between text-xs font-medium mb-1">
                  <span class="text-gray-700 dark:text-gray-300">{{ $t('services.progress') || 'التقدم' }}</span>
                  <span class="text-brand-600 dark:text-brand-400">{{ importTask.progress }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700 overflow-hidden">
                  <div class="bg-brand-600 h-2 rounded-full transition-all duration-300" :style="{ width: `${importTask.progress}%` }"></div>
                </div>
              </div>
            </div>
            
            <div v-else class="flex-1 flex flex-col">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('services.select_file') || 'اختر ملف الإكسل' }} <span class="text-error-500">*</span></label>
              
              <div 
                class="flex-1 flex justify-center rounded-xl border-2 border-dashed transition-colors cursor-pointer items-center min-h-[160px]"
                :class="[
                  isDragging ? 'border-brand-500 bg-brand-50 dark:bg-brand-500/10 dark:border-brand-500' : 'border-gray-300 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600 hover:bg-gray-50/50 dark:hover:bg-gray-800/30',
                  selectedFile ? 'border-success-500 bg-success-50/50 dark:border-success-500/30 dark:bg-success-500/5' : ''
                ]"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
              >
                <div class="text-center w-full px-6 py-6">
                  <svg class="mx-auto h-12 w-12 text-gray-300 dark:text-gray-600 mb-3" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" :class="{ 'text-success-400 dark:text-success-500': selectedFile }">
                    <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clip-rule="evenodd" />
                  </svg>
                  <div class="flex text-sm leading-6 text-gray-600 dark:text-gray-400 justify-center">
                    <label for="file-upload" class="relative cursor-pointer rounded-md font-semibold text-brand-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-brand-600 focus-within:ring-offset-2 hover:text-brand-500 dark:text-brand-400 dark:hover:text-brand-300">
                      <span>{{ selectedFile ? 'تغيير الملف' : ($t('services.upload_file') || 'رفع ملف') }}</span>
                      <input id="file-upload" name="file-upload" type="file" class="sr-only" accept=".xlsx, .xls" @change="handleFileSelect">
                    </label>
                    <p class="pl-1 pe-1" v-if="!selectedFile">{{ $t('services.drag_drop') || 'أو اسحب وأفلت هنا' }}</p>
                  </div>
                  <p class="text-xs leading-5 text-gray-500 mt-1">XLSX, XLS {{ $t('services.max_size') || 'حتى 10MB' }}</p>
                </div>
              </div>
              
              <div v-if="selectedFile" class="mt-3 flex items-center justify-between p-3 rounded-lg bg-success-50 border border-success-100 dark:bg-success-500/10 dark:border-success-500/20 shadow-theme-xs">
                <div class="flex items-center gap-2">
                  <svg class="h-5 w-5 text-success-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  <span class="text-sm font-medium text-success-700 dark:text-success-400" dir="ltr">{{ selectedFile.name }}</span>
                </div>
                <button @click="selectedFile = null" class="text-gray-400 hover:text-error-500 transition-colors">
                  <span class="sr-only">إزالة الملف</span>
                  <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" /></svg>
                </button>
              </div>
              
              <div class="pt-4 mt-auto">
                <button 
                  @click="handleImport" 
                  :disabled="!selectedFile || isImporting"
                  class="w-full flex justify-center items-center gap-2 rounded-lg bg-success-600 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-success-500 focus:outline-none focus:ring-2 focus:ring-success-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
                >
                  <svg v-if="isImporting" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  {{ $t('services.start_import') || 'بدء الاستيراد والمعالجة' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'
import { useCoreStore } from '@/stores/core'
import Swal from 'sweetalert2'

const router = useRouter()
const servicesStore = useServicesStore()
const coreStore = useCoreStore()

// --- Export State ---
const isExporting = ref(false)
const exportData = ref({
  directorateId: '',
  month: '' // format: YYYY-MM
})

// --- Import State ---
const isImporting = ref(false)
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)

const importTask = ref({
  active: false,
  taskId: '',
  progress: 0,
  intervalId: null as any
})

onMounted(async () => {
  // Ensure we have directorates to choose from
  if (coreStore.centralDepartments.length === 0) {
    await coreStore.fetchAllReferences()
  }
})

// --- Export Logic ---
async function handleExport() {
  if (!exportData.value.directorateId || !exportData.value.month) return
  
  isExporting.value = true
  try {
    await servicesStore.exportSheet(Number(exportData.value.directorateId), exportData.value.month)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تصدير الكشوفة بنجاح', showConfirmButton: false, timer: 3000 })
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل عملية التصدير', 'error')
  } finally {
    isExporting.value = false
  }
}

// --- Import Logic ---
function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    validateAndSetFile(target.files[0])
  }
}

function handleDrop(event: DragEvent) {
  isDragging.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
    validateAndSetFile(event.dataTransfer.files[0])
  }
}

function validateAndSetFile(file: File) {
  const validTypes = [
    'text/csv', 
    'application/vnd.ms-excel', 
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ]
  
  if (!validTypes.includes(file.type) && !file.name.match(/\.(csv|xls|xlsx)$/i)) {
    Swal.fire('خطأ', 'الصيغة غير مدعومة. الرجاء رفع ملف إكسل', 'error')
    return
  }
  
  if (file.size > 50 * 1024 * 1024) {
    Swal.fire('خطأ', 'حجم الملف يتجاوز الحد الأقصى 50MB', 'error')
    return
  }
  
  selectedFile.value = file
}

async function handleImport() {
  if (!selectedFile.value) return
  
  isImporting.value = true
  try {
    const response = await servicesStore.importSheet(selectedFile.value)
    
    // Check if it's async (Celery task)
    if (response.async && response.task_id) {
      startTaskPoller(response.task_id)
    } else {
      // Sync processing completed instantly
      const responseData = response.data || response;
      const errorCount = responseData.errors ? responseData.errors.length : 0;
      const changesCount = responseData.stats ? responseData.stats.changes_detected : 0;

      if (errorCount > 0 && changesCount === 0) {
          Swal.fire({
            title: 'لم يتم اعتماد أي تغييرات',
            text: `يحتوي الملف على أخطاء تمنع استيراده. يرجى مراجعة الملف الأصلي. (${errorCount} أخطاء)`,
            icon: 'error',
          });
          selectedFile.value = null;
          return;
      } else if (errorCount > 0) {
          Swal.fire({
            title: 'تم الاستيراد جزئياً',
            text: `تم اكتشاف ${changesCount} تعديلات، ولكن يوجد ${errorCount} أخطاء في بعض الصفوف.`,
            icon: 'warning',
            confirmButtonText: 'الذهاب للاعتمادات',
            confirmButtonColor: '#f59e0b'
          }).then(() => {
            router.push('/services/staging')
          })
      } else if (changesCount === 0) {
          Swal.fire({
            title: 'لا توجد تغييرات',
            text: 'الملف مطابق تماماً للبيانات الحالية، لم يتم اكتشاف أي تعديلات.',
            icon: 'info',
          });
      } else {
          Swal.fire({
            title: 'تم الاستيراد بنجاح',
            text: `تم رفع الملف واكتشاف ${changesCount} تعديلات بنجاح. سيتم توجيهك الآن لمراجعتها.`,
            icon: 'success',
            confirmButtonText: 'الذهاب للاعتمادات',
            confirmButtonColor: '#10b981'
          }).then(() => {
            router.push('/services/staging')
          })
      }
      selectedFile.value = null
    }
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل عملية الاستيراد', 'error')
  } finally {
    isImporting.value = false
  }
}

function startTaskPoller(taskId: string) {
  importTask.value = {
    active: true,
    taskId,
    progress: 0,
    intervalId: setInterval(checkStatus, 2000)
  }
}

async function checkStatus() {
  if (!importTask.value.active) return
  
  try {
    const res = await servicesStore.checkTaskStatus(importTask.value.taskId)
    
    if (res.data) {
      if (res.data.status === 'PROGRESS') {
        importTask.value.progress = res.data.progress || 10 // just fake progress if needed
      } 
      else if (res.data.status === 'SUCCESS') {
        stopPoller()
        Swal.fire({
          title: 'اكتملت المعالجة السحابية!',
          text: 'تم تجهيز التعديلات. سيتم توجيهك الآن لمراجعتها.',
          icon: 'success',
          confirmButtonText: 'الذهاب للاعتمادات',
          confirmButtonColor: '#10b981'
        }).then(() => {
          router.push('/services/staging')
        })
        selectedFile.value = null
      } 
      else if (res.data.status === 'FAILURE') {
        stopPoller()
        Swal.fire('خطأ سحابي', res.data.error || 'فشلت معالجة الملف', 'error')
      }
    }
  } catch (err) {
    // silently fail and retry next tick unless it keeps failing
  }
}

function stopPoller() {
  if (importTask.value.intervalId) {
    clearInterval(importTask.value.intervalId)
  }
  importTask.value.active = false
  importTask.value.progress = 0
}
</script>
