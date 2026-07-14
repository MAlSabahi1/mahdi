<template>
  <div class="print-container min-h-screen bg-gray-100 dark:bg-gray-900 py-8" dir="rtl">
    <!-- Action buttons (Hidden in print) -->
    <div class="max-w-[21cm] mx-auto mb-4 flex justify-between items-center no-print">
      <button @click="goBack" class="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg font-bold hover:bg-gray-300 transition-colors">
        العودة
      </button>
      <button @click="printDocument" class="bg-brand-600 text-white px-6 py-2 rounded-lg font-bold shadow-lg hover:bg-brand-700 transition-colors flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
        طباعة النموذج
      </button>
    </div>

    <!-- The A4 Print Page -->
    <div class="a4-page bg-white mx-auto shadow-2xl relative overflow-hidden" id="print-area">
      <!-- Watermark (optional) -->
      <div class="absolute inset-0 flex items-center justify-center opacity-[0.03] pointer-events-none">
        <img src="/images/logo/logo.svg" alt="watermark" class="w-96 h-96 grayscale" onerror="this.style.display='none'">
      </div>

      <div class="relative z-10 p-12 h-full flex flex-col">
        <!-- Header -->
        <header class="flex justify-between items-start border-b-2 border-gray-800 pb-6 mb-8">
          <div class="text-right font-bold text-gray-800 leading-relaxed text-sm">
            <p>الجمهورية اليمنية</p>
            <p>وزارة الداخلية</p>
            <p>إدارة شؤون الأفراد والخدمات</p>
            <p>القوى البشرية الأمنية</p>
          </div>
          <div class="text-center">
            <div class="w-20 h-20 mx-auto border-2 border-gray-800 rounded-full flex items-center justify-center mb-2">
              <span class="text-xs font-bold text-gray-500">شعار الجمهورية</span>
            </div>
          </div>
          <div class="text-left font-bold text-gray-800 leading-relaxed text-sm">
            <p>التاريخ: {{ currentDate }}</p>
            <p>الموافق: {{ currentHijriDate }} هـ</p>
            <p>رقم المعاملة: {{ requestData?.id || '..........' }}</p>
            <p>المرفقات: (   ) نموذج 23</p>
          </div>
        </header>

        <!-- Title -->
        <div class="text-center mb-10">
          <h1 class="text-2xl font-black text-gray-900 border-2 border-gray-800 inline-block px-8 py-3 rounded-lg bg-gray-50">
            نموذج رقم (23) - طلب تصحيح الاسم الأساسي
          </h1>
        </div>

        <!-- Section 1: Personnel Info -->
        <section class="mb-8">
          <h2 class="text-lg font-bold text-gray-800 mb-4 bg-gray-100 py-2 px-4 border-r-4 border-gray-800">
            أولاً: البيانات الأساسية للفرد
          </h2>
          <div class="grid grid-cols-2 gap-x-8 gap-y-6 px-4">
            <div class="flex items-end border-b border-gray-300 pb-1">
              <span class="font-bold text-gray-700 w-32 shrink-0">الرقم العسكري:</span>
              <span class="font-bold text-lg text-gray-900">{{ personnelData?.military_number || '....................' }}</span>
            </div>
            <div class="flex items-end border-b border-gray-300 pb-1">
              <span class="font-bold text-gray-700 w-32 shrink-0">الرتبة:</span>
              <span class="font-bold text-lg text-gray-900">{{ personnelData?.current_rank_display || '....................' }}</span>
            </div>
            <div class="flex items-end border-b border-gray-300 pb-1">
              <span class="font-bold text-gray-700 w-32 shrink-0">الإدارة / الوحدة:</span>
              <span class="font-bold text-lg text-gray-900">{{ personnelData?.unit_display || personnelData?.central_department_display || '....................' }}</span>
            </div>
            <div class="flex items-end border-b border-gray-300 pb-1">
              <span class="font-bold text-gray-700 w-32 shrink-0">تاريخ الالتحاق:</span>
              <span class="font-bold text-lg text-gray-900">{{ personnelData?.join_date || '....................' }}</span>
            </div>
          </div>
        </section>

        <!-- Section 2: Correction Details -->
        <section class="mb-10">
          <h2 class="text-lg font-bold text-gray-800 mb-4 bg-gray-100 py-2 px-4 border-r-4 border-gray-800">
            ثانياً: تفاصيل التصحيح المطلوب
          </h2>
          <div class="space-y-6 px-4">
            <div class="flex flex-col gap-2">
              <span class="font-bold text-gray-700">الاسم الحالي (الخاطئ) في السجلات:</span>
              <div class="border-2 border-gray-300 rounded p-4 bg-gray-50 text-xl font-bold text-gray-900 min-h-[60px] flex items-center">
                {{ requestData?.old_value || personnelData?.full_name || '' }}
              </div>
            </div>
            
            <div class="flex flex-col gap-2">
              <span class="font-bold text-gray-700">الاسم الصحيح المطلوب اعتماده:</span>
              <div class="border-2 border-gray-800 rounded p-4 bg-white text-xl font-black text-gray-900 min-h-[60px] flex items-center shadow-inner">
                {{ requestData?.new_value || '' }}
              </div>
            </div>

            <div class="flex flex-col gap-2">
              <span class="font-bold text-gray-700">مبررات وسبب التصحيح:</span>
              <div class="border border-gray-300 rounded p-4 text-gray-800 min-h-[80px]">
                {{ requestData?.reason || requestData?.notes || 'بناءً على الوثائق الثبوتية المرفقة (البطاقة الشخصية + نموذج 23).' }}
              </div>
            </div>
          </div>
        </section>

        <!-- Spacer to push signatures to bottom -->
        <div class="flex-grow"></div>

        <!-- Section 3: Signatures -->
        <section class="mt-auto border-t-2 border-gray-800 pt-8">
          <h2 class="text-lg font-bold text-gray-800 mb-8 bg-gray-100 py-2 px-4 border-r-4 border-gray-800">
            ثالثاً: الاعتمادات والتوقيعات
          </h2>
          <div class="grid grid-cols-3 gap-8 px-4 text-center">
            <div class="flex flex-col gap-8">
              <span class="font-bold text-gray-700">مقدم الطلب (صاحب الشأن)</span>
              <div class="border-b border-gray-400 border-dashed pb-2">التوقيع / البصمة:</div>
              <div class="border-b border-gray-400 border-dashed pb-2">التاريخ: &nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;م</div>
            </div>
            
            <div class="flex flex-col gap-8">
              <span class="font-bold text-gray-700">رئيس قسم الخدمات</span>
              <div class="border-b border-gray-400 border-dashed pb-2">الاسم:</div>
              <div class="border-b border-gray-400 border-dashed pb-2">التوقيع والختم:</div>
            </div>

            <div class="flex flex-col gap-8">
              <span class="font-bold text-gray-700">مدير إدارة القوى البشرية</span>
              <div class="border-b border-gray-400 border-dashed pb-2">المدير العام للمحافظة:</div>
              <div class="border-b border-gray-400 border-dashed pb-2">التوقيع والختم:</div>
            </div>
          </div>
        </section>
        
        <div class="mt-8 text-center text-xs text-gray-500 font-bold">
          <p>هذا النموذج معتمد ولا يقبل الكشط أو التعديل، ويجب إرفاق صورة طبق الأصل من الوثائق الثبوتية.</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCorrectionStore } from '@/stores/correction'
import { usePersonnelStore } from '@/stores/personnel'

const route = useRoute()
const router = useRouter()
const correctionStore = useCorrectionStore()
const personnelStore = usePersonnelStore()

const requestData = ref<any>(null)
const personnelData = ref<any>(null)
const currentDate = ref(new Date().toLocaleDateString('ar-YE'))
const currentHijriDate = ref(new Intl.DateTimeFormat('ar-TN-u-ca-islamic', {day: 'numeric', month: 'long', year: 'numeric'}).format(new Date()))

onMounted(async () => {
  const correctionId = route.params.id as string
  if (correctionId) {
    // In a real scenario, we fetch the specific correction request by ID
    // Since we don't have a specific getCorrectionById yet, we'll try to find it in the store
    // If not found, you can add an API call here.
    
    // Fallback: use data from query parameters if passed from UnifiedRequestForm
    if (route.query.personnelId) {
      const milNum = route.query.personnelId as string
      try {
        const pResponse = await personnelStore.getPersonnelById(milNum)
        personnelData.value = pResponse
      } catch (e) {}
    }
    
    requestData.value = {
      id: correctionId !== 'preview' ? correctionId : 'جديد',
      old_value: route.query.old_value as string,
      new_value: route.query.new_value as string,
      reason: route.query.reason as string,
    }
  }
})

function goBack() {
  router.back()
}

function printDocument() {
  window.print()
}
</script>

<style>
/* CSS specific for A4 Print */
.a4-page {
  width: 21cm;
  min-height: 29.7cm;
  background: white;
}

@media print {
  @page {
    size: A4;
    margin: 0; /* Remove default browser margins to use full page */
  }
  
  body {
    background: white;
  }
  
  .print-container {
    background: transparent;
    padding: 0;
  }
  
  .no-print {
    display: none !important;
  }
  
  .a4-page {
    box-shadow: none !important;
    width: 100%;
    min-height: auto;
  }
}
</style>
