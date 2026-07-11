<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('services.dashboard_title') || 'إدارة الكشوفات والخدمات'" />
    
    <div class="pb-12" dir="rtl">
      
      <!-- Premium Page Header -->
      <div class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            لوحة تحكم الكشوفات والخدمات
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            المنصة المركزية لإدارة وتصدير واستيراد الكشوفات الدورية (الإكسل). يمكنك سحب بيانات الشهر وتعديلها خارجياً ثم إعادة رفعها لمطابقتها وإصدار تسويات.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 xl:grid-cols-2">
        
        <!-- Export Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col group transition-all hover:shadow-theme-sm">
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400 border border-brand-100 dark:border-brand-500/30 group-hover:scale-110 transition-transform duration-300">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('services.export_monthly_sheet') || 'تصدير كشوفة شهرية' }}</h3>
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mt-1">{{ $t('services.export_subtitle') || 'تحميل ملف الإكسل الأصلي للتعديل عليه خارجياً' }}</p>
            </div>
          </div>
          
          <div class="p-6 md:p-8 space-y-6 flex-1 flex flex-col bg-white dark:bg-gray-900">
            <BaseSelect
              v-model="exportData.directorateId"
              :label="$t('personnel.governorate') || 'المديرية / الإدارة'"
              :required="true"
              :options="coreStore.centralDepartments"
              valueKey="id"
              labelKey="name"
              :placeholder="$t('services.select_directorate') || 'اختر المديرية'"
            />
            
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                {{ $t('services.service_month') || 'شهر الخدمة' }} <span class="text-error-500">*</span>
              </label>
              <div class="relative z-20 bg-transparent">
                <input type="month" v-model="exportData.month" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors dark:placeholder:text-white/30 border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 [&::-webkit-calendar-picker-indicator]:opacity-0 [&::-webkit-calendar-picker-indicator]:absolute [&::-webkit-calendar-picker-indicator]:w-full [&::-webkit-calendar-picker-indicator]:h-full [&::-webkit-calendar-picker-indicator]:cursor-pointer [&::-webkit-calendar-picker-indicator]:inset-0" />
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="h-5 w-5 stroke-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </span>
              </div>
            </div>
            
            <div class="pt-6 mt-auto">
              <BaseButton 
                @click="handleExport" 
                :disabled="!exportData.directorateId || !exportData.month || isExporting"
                :loading="isExporting"
                variant="primary"
                size="lg"
                customClass="w-full rounded-xl font-bold"
              >
                <svg v-if="!isExporting" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                {{ isExporting ? ($t('services.exporting') || 'جاري التجهيز والتحميل...') : ($t('services.export_sheet') || 'تصدير الكشوفة') }}
              </BaseButton>
            </div>
          </div>
        </div>

        <!-- Import Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col group transition-all hover:shadow-theme-sm">
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-success-50 text-success-600 dark:bg-success-500/20 dark:text-success-400 border border-success-100 dark:border-success-500/30 group-hover:scale-110 transition-transform duration-300">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('services.import_modified_sheet') || 'استيراد كشوفة معدلة' }}</h3>
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mt-1">{{ $t('services.import_subtitle') || 'رفع الإكسل لإرسال التعديلات إلى شاشة (المراجعة)' }}</p>
            </div>
          </div>
          
          <div class="p-6 md:p-8 flex-1 flex flex-col bg-white dark:bg-gray-900">
            
            <transition name="fade-slide" mode="out-in">
              <div v-if="importTask.active" class="flex-1 flex flex-col items-center justify-center text-center space-y-5 py-8" key="processing">
                <div class="relative w-20 h-20 flex items-center justify-center">
                  <div class="absolute inset-0 border-4 border-gray-100 dark:border-gray-800 rounded-full"></div>
                  <div class="absolute inset-0 border-4 border-success-500 rounded-full border-t-transparent animate-spin"></div>
                  <svg class="h-8 w-8 text-success-500 absolute" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                </div>
                <div>
                  <h4 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('services.processing_file') || 'جاري معالجة الملف السحابية...' }}</h4>
                  <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mt-2">{{ $t('services.processing_subtitle') || 'يتم الآن قراءة السجلات ومطابقتها، يرجى الانتظار وعدم إغلاق الصفحة.' }}</p>
                </div>
                
                <!-- Clean Progress Bar -->
                <div class="w-full max-w-sm mt-6 space-y-2">
                  <div class="flex justify-between text-sm font-bold px-1">
                    <span class="text-success-600 dark:text-success-400">{{ $t('services.progress') || 'التقدم الفعلي' }}</span>
                    <span class="text-gray-900 dark:text-white font-mono">{{ importTask.progress }}%</span>
                  </div>
                  <div class="h-3 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden shadow-inner">
                    <div 
                      class="h-full bg-success-500 rounded-full transition-all duration-300 relative overflow-hidden" 
                      :style="{ width: `${importTask.progress}%` }"
                    >
                      <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-else class="flex-1 flex flex-col" key="upload">
                <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">{{ $t('services.select_file') || 'اختر ملف الإكسل' }} <span class="text-error-500">*</span></label>
                
                <div class="flex items-center justify-center w-full mb-4">
                  <label 
                    for="file-upload" 
                    class="flex flex-col items-center justify-center w-full h-[220px] border-2 border-dashed rounded-xl cursor-pointer transition-all duration-200"
                    :class="[
                      isDragging ? 'border-success-500 bg-success-50 dark:bg-success-500/10 dark:border-success-500' : 'border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 hover:border-gray-400 dark:hover:border-gray-500',
                      selectedFile ? 'border-success-500 bg-success-50/50 dark:border-success-500/30 dark:bg-success-500/5' : ''
                    ]"
                    @dragover.prevent="isDragging = true"
                    @dragleave.prevent="isDragging = false"
                    @drop.prevent="handleDrop"
                  >
                    <div class="flex flex-col items-center justify-center pt-5 pb-6">
                      <div class="w-16 h-16 mb-4 rounded-full flex items-center justify-center transition-colors"
                           :class="selectedFile ? 'bg-success-100 text-success-600 dark:bg-success-900/60 dark:text-success-400 ring-4 ring-success-50 dark:ring-success-900/20' : 'text-gray-400 bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700'">
                        <svg v-if="!selectedFile" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                      </div>
                      
                      <div v-if="!selectedFile" class="text-center px-4">
                        <p class="mb-2 text-sm font-bold text-gray-900 dark:text-white">اضغط لرفع الكشف أو قم بإفلاته هنا</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed max-w-[200px] mx-auto">XLSX, XLS {{ $t('services.max_size') || 'حتى 10MB' }}</p>
                      </div>
                      
                      <div v-else class="text-center animate-fade-in-up">
                        <p class="text-sm font-bold text-success-600 dark:text-success-400" dir="ltr">{{ selectedFile.name }}</p>
                        <p class="mt-2 inline-flex items-center gap-2 px-3 py-1 bg-white dark:bg-gray-800 rounded-lg text-xs font-medium text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 shadow-theme-xs">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                          حجم الملف: {{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB
                        </p>
                      </div>
                    </div>
                    <input id="file-upload" type="file" class="hidden" @change="handleFileSelect" accept=".xlsx, .xls" />
                  </label>
                </div>
                
                <div v-if="selectedFile" class="mb-4 flex items-center justify-end">
                  <button @click="selectedFile = null" class="text-xs font-bold text-error-500 hover:text-error-600 flex items-center gap-1 transition-colors px-2 py-1 rounded-md hover:bg-error-50 dark:hover:bg-error-500/10">
                    <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" /></svg>
                    إزالة الملف
                  </button>
                </div>
                
                <div class="pt-2 mt-auto">
                  <BaseButton 
                    @click="handleImport" 
                    :disabled="!selectedFile || isImporting"
                    :loading="isImporting"
                    variant="success"
                    size="lg"
                    customClass="w-full rounded-xl font-bold"
                  >
                    <svg v-if="!isImporting" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    {{ $t('services.start_import') || 'بدء الاستيراد والمعالجة' }}
                  </BaseButton>
                </div>
              </div>
            </transition>
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
import BaseSelect from '@/components/common/BaseSelect.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useServicesStore } from '@/stores/services'
import { useCoreStore } from '@/stores/core'
import Swal from 'sweetalert2'

const router = useRouter()
const servicesStore = useServicesStore()
const coreStore = useCoreStore()

// --- Export State ---
const isExporting = ref(false)
const exportData = ref({
  directorateId: null as number | string | null,
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
