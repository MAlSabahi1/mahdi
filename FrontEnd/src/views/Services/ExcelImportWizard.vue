<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="معالج الاستيراد الجماعي وتتبع مهام Celery" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          معالج الاستيراد الجماعي وتتبع مهام Celery (Excel Import Wizard)
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          رفع كشوفات المديريات المعدلة واستيرادها آلياً عبر محرك الخلفية. تتبع حالة المعالجة ومطابقة السجلات أولاً بأول.
        </p>
      </div>

      <!-- Import Progress Stepper -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4 max-w-3xl mx-auto">
          <div v-for="step in steps" :key="step.number" class="flex items-center gap-3">
            <span 
              :class="[
                currentStep === step.number 
                  ? 'bg-brand-600 text-white' 
                  : currentStep > step.number 
                    ? 'bg-emerald-500 text-white' 
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-400'
              ]"
              class="h-8 w-8 rounded-full flex items-center justify-center font-bold text-xs shadow-theme-xs transition-colors"
            >
              {{ currentStep > step.number ? '✓' : step.number }}
            </span>
            <div class="text-right">
              <h4 class="text-xs font-black text-gray-800 dark:text-gray-200">{{ step.title }}</h4>
              <p class="text-[9px] text-gray-400">{{ step.desc }}</p>
            </div>
            <!-- Arrow divider -->
            <div v-if="step.number < 4" class="hidden md:block h-px w-10 bg-gray-200 dark:bg-gray-800 mr-4"></div>
          </div>
        </div>
      </div>

      <!-- Wizard Views Container -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs min-h-[300px] flex flex-col justify-between">
        
        <!-- Step 1: Upload File -->
        <div v-if="currentStep === 1" class="space-y-6 flex-1 flex flex-col justify-center items-center py-6">
          <div class="w-full max-w-lg border-2 border-dashed border-gray-300 dark:border-gray-800 rounded-2xl p-8 text-center bg-gray-50/50 dark:bg-gray-950/20 hover:bg-gray-50 dark:hover:bg-gray-950/40 transition-colors relative">
            <input type="file" @change="handleFileChange" accept=".xlsx,.xls,.csv" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
            <span class="p-3 bg-brand-50 dark:bg-brand-950/40 text-brand-600 dark:text-brand-400 rounded-xl inline-block mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </span>
            <h3 class="text-xs font-black text-gray-800 dark:text-gray-200">اسحب كشف الإكسل المعدل وأفلته هنا</h3>
            <p class="text-[10px] text-gray-400 mt-1">يدعم التنسيقات .xlsx, .xls, .csv حتى حجم 20 ميجابايت</p>
          </div>
          <div v-if="selectedFile" class="text-xs font-bold text-brand-650 bg-brand-50/50 dark:bg-brand-950/20 px-4 py-2 rounded-lg">
            الملف المختار: {{ selectedFile.name }} ({{ (selectedFile.size / 1024).toFixed(1) }} KB)
          </div>
        </div>

        <!-- Step 2: Structure Validation -->
        <div v-if="currentStep === 2" class="space-y-4 flex-1">
          <h3 class="text-sm font-black text-gray-800 dark:text-gray-200">مطابقة هيكل الكشف المستورد</h3>
          <p class="text-[10px] text-gray-400">يجري فحص الأعمدة الحيوية لمطابقة القواعد التنظيمية والمالية الأساسية في الباك اند.</p>

          <div class="border border-gray-100 dark:border-gray-850 rounded-xl overflow-hidden text-xs">
            <table class="w-full text-right border-collapse">
              <thead>
                <tr class="bg-gray-50 dark:bg-gray-950 text-gray-500 font-bold border-b border-gray-150 dark:border-gray-800">
                  <th class="p-3">اسم العمود بالكشف</th>
                  <th class="p-3">حالة المطابقة الفنية</th>
                  <th class="p-3">النوع المتوقع</th>
                  <th class="p-3">التحقق الهيكلي</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-150 dark:divide-gray-850 text-gray-700 dark:text-gray-300">
                <tr>
                  <td class="p-3 font-mono font-bold">military_number</td>
                  <td class="p-3 text-emerald-500 font-bold">متطابق ✓</td>
                  <td class="p-3 font-mono text-[10px] text-gray-400">Integer (7-digits)</td>
                  <td class="p-3">الرقم العسكري (مفتاح أساسي مقفل)</td>
                </tr>
                <tr>
                  <td class="p-3 font-mono font-bold">full_name</td>
                  <td class="p-3 text-emerald-500 font-bold">متطابق ✓</td>
                  <td class="p-3 font-mono text-[10px] text-gray-400">String (max 255)</td>
                  <td class="p-3">الاسم الكامل المطابق للهوية</td>
                </tr>
                <tr>
                  <td class="p-3 font-mono font-bold">base_salary</td>
                  <td class="p-3 text-emerald-500 font-bold">متطابق ✓</td>
                  <td class="p-3 font-mono text-[10px] text-gray-400">Decimal (10,2)</td>
                  <td class="p-3">الراتب الأساسي المعتمد</td>
                </tr>
                <tr>
                  <td class="p-3 font-mono font-bold">absent_days</td>
                  <td class="p-3 text-emerald-500 font-bold">متطابق ✓</td>
                  <td class="p-3 font-mono text-[10px] text-gray-400">Integer</td>
                  <td class="p-3">أيام الغياب الفعلي (مسموح بالتعديل)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Step 3: Celery AsyncTask Tracker -->
        <div v-if="currentStep === 3" class="space-y-6 flex-1 flex flex-col justify-center items-center py-6">
          <div class="w-full max-w-md space-y-4">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-gray-500">معرف المهمة (Celery Task ID):</span>
              <span class="font-mono text-gray-400">celery-task-{{ Math.random().toString(36).substr(2, 9) }}</span>
            </div>
            
            <div class="h-3 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
              <div 
                class="h-full bg-brand-600 rounded-full transition-all duration-300"
                :style="{ width: `${celeryProgress}%` }"
              ></div>
            </div>

            <div class="flex justify-between items-center text-xs">
              <span class="text-brand-650 font-bold">جاري المعالجة غير المتزامنة وتحديث السجلات...</span>
              <span class="font-bold text-gray-900 dark:text-white">{{ celeryProgress }}%</span>
            </div>

            <!-- Stats updates -->
            <div class="grid grid-cols-3 gap-2 text-center text-[10px] pt-3">
              <div class="bg-gray-50 dark:bg-gray-950 p-2.5 rounded-lg border border-gray-100 dark:border-gray-850">
                <span class="block text-gray-400">إجمالي السجلات</span>
                <span class="text-xs font-bold text-gray-800 dark:text-gray-200">500</span>
              </div>
              <div class="bg-emerald-50/50 dark:bg-emerald-950/20 p-2.5 rounded-lg border border-emerald-100/30">
                <span class="block text-emerald-500">السجلات السليمة</span>
                <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400">{{ Math.floor((celeryProgress/100) * 480) }}</span>
              </div>
              <div class="bg-red-50/50 dark:bg-red-950/20 p-2.5 rounded-lg border border-red-100/30">
                <span class="block text-red-500">المرفوضات المحتملة</span>
                <span class="text-xs font-bold text-red-600 dark:text-red-400">{{ Math.floor((celeryProgress/100) * 20) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 4: Import Summary & Rejections -->
        <div v-if="currentStep === 4" class="space-y-4 flex-1">
          <div class="p-4 bg-emerald-50/60 dark:bg-emerald-950/10 border border-emerald-100 dark:border-emerald-900/30 rounded-xl flex items-center gap-3">
            <span class="p-2 bg-emerald-100 text-emerald-650 dark:bg-emerald-950/30 dark:text-emerald-450 rounded-lg shrink-0">
              ✓
            </span>
            <div class="text-right">
              <h4 class="text-xs font-bold text-emerald-800 dark:text-emerald-400">اكتملت المهمة بنجاح</h4>
              <p class="text-[10px] text-emerald-700/80 dark:text-emerald-400/80 mt-0.5">تم استيراد كافة السجلات المطابقة بنجاح وترحيلها لبيئة المراجعة (Staging).</p>
            </div>
          </div>

          <div class="grid grid-cols-4 gap-4 text-center">
            <div class="bg-gray-50 dark:bg-gray-950 p-3 rounded-xl border border-gray-150 dark:border-gray-800">
              <span class="block text-[10px] text-gray-400 mb-1">السجلات المعالجة</span>
              <span class="text-base font-black text-gray-900 dark:text-white">500</span>
            </div>
            <div class="bg-emerald-50 dark:bg-emerald-950/20 p-3 rounded-xl border border-emerald-100 dark:border-emerald-900/20">
              <span class="block text-[10px] text-emerald-650 mb-1">المستوردة (Staging)</span>
              <span class="text-base font-black text-emerald-600 dark:text-emerald-400">480</span>
            </div>
            <div class="bg-red-50 dark:bg-red-950/20 p-3 rounded-xl border border-red-100 dark:border-red-900/20">
              <span class="block text-[10px] text-red-650 mb-1">المرفوضة</span>
              <span class="text-base font-black text-red-600 dark:text-red-400">20</span>
            </div>
            <div class="bg-brand-50 dark:bg-brand-950/20 p-3 rounded-xl border border-brand-100 dark:border-brand-900/20">
              <span class="block text-[10px] text-brand-650 mb-1">معدل الدقة فني %</span>
              <span class="text-base font-black text-brand-600 dark:text-brand-400">96%</span>
            </div>
          </div>

          <div class="pt-2 text-right">
            <RouterLink to="/services/rejections" class="text-xs font-bold text-red-600 hover:underline">
              ← استعراض وتنزيل قائمة المرفوضات الاستثنائية لمعالجتها
            </RouterLink>
          </div>
        </div>

        <!-- Wizard Navigation Footer -->
        <div class="flex justify-between items-center border-t border-gray-150 dark:border-gray-800 pt-4 mt-6">
          <button 
            :disabled="currentStep === 1 || currentStep === 3"
            @click="prevStep"
            class="px-4 py-1.5 text-xs font-bold border border-gray-200 dark:border-gray-850 hover:bg-gray-50 dark:hover:bg-gray-900 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            السابق
          </button>
          
          <button 
            v-if="currentStep < 4"
            :disabled="currentStep === 1 && !selectedFile"
            @click="nextStep"
            class="px-4 py-1.5 text-xs font-bold bg-brand-600 text-white hover:bg-brand-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {{ currentStep === 3 ? 'جاري المعالجة...' : 'التالي' }}
          </button>
          
          <button 
            v-else
            @click="resetWizard"
            class="px-4 py-1.5 text-xs font-bold bg-brand-600 text-white hover:bg-brand-700 rounded-lg cursor-pointer"
          >
            تحميل كشف جديد
          </button>
        </div>

      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

const currentStep = ref(1)
const selectedFile = ref<File | null>(null)
const celeryProgress = ref(0)

const steps = [
  { number: 1, title: 'رفع الكشف المالي', desc: 'تحميل ملف Excel أو CSV' },
  { number: 2, title: 'فحص البنية والمطابقة', desc: 'مطابقة حقول الجدول فني' },
  { number: 3, title: 'معالجة Celery', desc: 'معالجة السجلات في الخلفية' },
  { number: 4, title: 'التقرير والملخص', desc: 'المستورد والمرفوض نهائي' }
]

function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

function nextStep() {
  if (currentStep.value === 2) {
    currentStep.value = 3
    simulateCeleryTask()
  } else if (currentStep.value < 4) {
    currentStep.value++
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

function resetWizard() {
  currentStep.value = 1
  selectedFile.value = null
  celeryProgress.value = 0
}

function simulateCeleryTask() {
  celeryProgress.value = 0
  const interval = setInterval(() => {
    if (celeryProgress.value >= 100) {
      clearInterval(interval)
      currentStep.value = 4
    } else {
      celeryProgress.value += 10
    }
  }, 400)
}
</script>
