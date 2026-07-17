<template>
  <div class="print-manager bg-gray-100 print:bg-white" dir="rtl">
    
    <OfficialMemoTemplate 
      departmentName="لجنة بناء الامدادات"
      :documentNumber="'CORR-' + String(correction?.id || '').padStart(5, '0')"
      :documentDate="new Date().toLocaleDateString('en-GB')"
      attachmentsText="كشف مطابقة — نموذج (23)"
      printedBy="النظام"
      :referenceNumber="'CORR-' + String(correction?.id || '').padStart(5, '0')"
    >
      <template #body>
        <div class="flex items-center gap-16 mb-3 mt-3">
          <h2 class="text-[17px] font-black tracking-wide" style="font-family: 'Cairo', sans-serif;">
            الأخ / المدير العام للمحافظة
          </h2>
          <h2 class="text-[17px] font-black tracking-widest" style="font-family: 'Cairo', sans-serif;">
            المحتـــــــرم
          </h2>
        </div>
        
        <div class="text-center mb-3 mt-1">
          <span class="inline-block text-[20px] font-bold" style="font-family: 'Samt7017', 'Aref Ruqaa', serif;">
            تحيـــــة طيبـــــة وبعـــــد ،،،
          </span>
        </div>
        
        <template v-if="isSmallRequest && !printWithList">
          <p class="font-bold text-[15px] mb-2 leading-[1.8] text-justify" style="font-family: 'Cairo', sans-serif;">
            نحيط سيادتكم علماً بأنه ورد إلينا طلب تصحيح بيانات للمنتسب الموضح أدناه.
          </p>
          
          <div class="w-full my-3 rounded-md overflow-hidden bg-white" style="border: 2px solid #1a1a1a;">
            <table class="w-full text-center border-collapse" style="font-family: 'Cairo', sans-serif;">
              <thead>
                <tr style="background: #e8e8e8;">
                  <th class="py-1.5 px-2 text-[12px] font-black text-gray-900" style="border-left: 1.5px solid #1a1a1a; border-bottom: 2px solid #1a1a1a;">الرتبة</th>
                  <th class="py-1.5 px-2 text-[12px] font-black text-gray-900" style="border-left: 1.5px solid #1a1a1a; border-bottom: 2px solid #1a1a1a;">الرقم العسكري</th>
                  <th class="py-1.5 px-2 text-[12px] font-black text-gray-900" style="border-left: 1.5px solid #1a1a1a; border-bottom: 2px solid #1a1a1a;">الاسم الحالي</th>
                  <th class="py-1.5 px-2 text-[12px] font-black text-gray-900" style="border-left: 1.5px solid #1a1a1a; border-bottom: 2px solid #1a1a1a;">الاسم الصحيح</th>
                  <th class="py-1.5 px-2 text-[12px] font-black text-gray-900" style="border-bottom: 2px solid #1a1a1a;">المطلوب تصحيحه</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in flatCorrections" :key="index">
                  <td class="py-1.5 px-2 text-[11px] font-bold" style="border-left: 1px solid #555; border-bottom: 1px solid #ccc;">{{ item.rank || item.personnel_rank || '—' }}</td>
                  <td class="py-1.5 px-2 text-[12px] font-bold font-mono tracking-wider" style="border-left: 1px solid #555; border-bottom: 1px solid #ccc;">{{ item.military_number || item.personnel_military_number || '—' }}</td>
                  <td class="py-1.5 px-2 text-[11px] font-bold" style="border-left: 1px solid #555; border-bottom: 1px solid #ccc;">{{ item.full_name || item.personnel_name || item.old_value || '—' }}</td>
                  <td class="py-1.5 px-2 text-[11px] font-bold" style="border-left: 1px solid #555; border-bottom: 1px solid #ccc;">{{ item.correct_name || item.new_value || '—' }}</td>
                  <td class="py-1.5 px-2 text-[11px] font-bold" style="border-bottom: 1px solid #ccc;">{{ getParsedData(item).target }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <p class="font-bold text-[15px] mb-2 leading-[1.8] text-justify mt-1" style="font-family: 'Cairo', sans-serif;">
            نرفق لكم الأوليات والمرفقات الثبوتية مع <strong>(كشف المطابقة — نموذج 23)</strong> للمطابقة، وذلك لاتخاذ الإجراءات اللازمة بحسب النظام والمصادقة على التصحيح المطلوب.
          </p>
        </template>
        
        <template v-else>
          <p class="font-bold text-[15px] mb-3 leading-[1.8] text-justify" style="font-family: 'Cairo', sans-serif;">
            نحيط سيادتكم علماً بأنه ورد إلينا 
            <template v-if="flatCorrections.length === 1">طلب تصحيح بيانات للمنتسب الموضح في الكشف المرفق.</template>
            <template v-else>طلبات تصحيح بيانات لعدد <strong>({{ flatCorrections.length }})</strong> من المنتسبين.</template>
          </p>
          <p class="font-bold text-[15px] mb-2 leading-[1.8] text-justify" style="font-family: 'Cairo', sans-serif;">
            نرفق لكم كشفاً تفصيلياً بأسماء المطلوب تصحيحها <strong>(كشف المطابقة — نموذج 23)</strong>، مع الأوليات والمرفقات الثبوتية لكل فرد، وذلك لاتخاذ الإجراءات اللازمة بحسب النظام والمصادقة على التصحيحات المطلوبة.
          </p>
        </template>
        
        <div class="flex-grow"></div>
        <p class="text-center text-[18px] font-bold mb-1" style="font-family: 'Samt7017', 'Aref Ruqaa', serif;">
          وتقبلــــوا خالــــص تحياتنــــا ،،،
        </p>
      </template>

      <!-- ============================================
           التوقيعات — تصميم 2 الحكومي الاحترافي
           الرتبة أولاً → الاسم → المنصب
           بدون خط فاصل، بدون نقاط
           ============================================ -->
      <template #signatures>
        <div class="flex justify-between items-start pt-8 pb-2 w-full" style="font-family: 'Arial', 'Tajawal', sans-serif;">
          
          <!-- التوقيع الأول: مدير إدارة القوى البشرية (يمين) -->
          <div class="flex-1 text-center leading-relaxed">
            <p class="text-[12px] font-bold text-gray-800 mb-5">الرتبة /</p>
            <p class="text-[12px] font-bold text-gray-800 mb-5">الاسم /</p>
            <p class="text-[13px] font-black text-gray-900 mb-4">مدير إدارة القوى البشرية</p>
            <p class="text-[11px] font-bold text-gray-600">التوقيع /</p>
          </div>
          
          <!-- التوقيع الثاني: المدير العام لإدارة أمن مأرب (يسار) -->
          <div class="flex-1 text-center leading-relaxed">
            <p class="text-[12px] font-bold text-gray-800 mb-5">الرتبة /</p>
            <p class="text-[12px] font-bold text-gray-800 mb-5">الاسم /</p>
            <p class="text-[13px] font-black text-gray-900 mb-4">المدير العام لإدارة أمن مأرب</p>
            <p class="text-[11px] font-bold text-gray-600">التوقيع /</p>
          </div>

        </div>
      </template>
    </OfficialMemoTemplate>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import OfficialMemoTemplate from '@/components/print/OfficialMemoTemplate.vue'

const props = defineProps<{
  correction?: any
  corrections?: any[]
  selectedMonth?: string
  printWithList?: boolean
}>()

const flatCorrections = computed(() => {
  if (props.corrections && props.corrections.length > 0) return props.corrections
  if (props.correction) return [props.correction]
  return []
})

const isSmallRequest = computed(() => {
  return flatCorrections.value.length > 0 && flatCorrections.value.length <= 2
})

function getParsedData(corr: any) {
  if (!corr) return { target: '—', notes: '—' }
  let rawNotes = corr.notes || corr.reason || ''
  let target = '—'
  let notes = rawNotes
  
  if (typeof rawNotes === 'string') {
    const targetMatch = rawNotes.match(/المطلوب تصحيح[هة]:\s*([\s\S]*?)(?=\s*المبررات:|$)/)
    const reasonMatch = rawNotes.match(/المبررات:\s*([\s\S]*)/)
    
    if (targetMatch && targetMatch[1]) {
      target = targetMatch[1].trim()
      if (reasonMatch && reasonMatch[1]) notes = reasonMatch[1].trim()
      else notes = '—'
    }
  }
  
  if (target === '—') {
    if (corr.field_name === 'full_name' || corr.correction_type === 'name_correction') target = 'تصحيح الاسم'
    else if (corr.field_name === 'national_id' || corr.correction_type === 'national_id_correction') target = 'تصحيح الرقم الوطني'
    else if (corr.field_name === 'military_number' || corr.correction_type === 'military_number_correction') target = 'تصحيح الرقم العسكري'
    else target = corr.field_name || corr.correction_type || 'تحديث بيانات'
  }
  
  return { target, notes: notes || '—' }
}
</script>

<style>
/* 
  UNSCOPED — ضروري لتتغلب على أنماط OfficialMemoTemplate العالمية
  نستهدف فقط .print-manager لعدم التأثير على أي شاشة أخرى
*/
@media print {
  .print-manager .print-preview-container {
    page-break-after: auto !important;
    min-height: auto !important;
    height: auto !important;
  }
  .print-manager .outer-border {
    min-height: auto !important;
    height: auto !important;
  }
}
</style>
