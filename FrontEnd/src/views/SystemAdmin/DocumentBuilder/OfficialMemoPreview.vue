<template>
  <AdminLayout>
    <div class="print-container min-h-screen bg-gray-100 dark:bg-gray-900 py-8" dir="rtl">
      
      <!-- Action buttons (Hidden in print) -->
      <div class="max-w-[21cm] mx-auto mb-4 flex justify-between items-center no-print">
        <button @click="closePreview" class="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg font-bold hover:bg-gray-300 transition-colors">
          عودة للتعديل
        </button>
        <div class="flex gap-2">
          <button @click="printDocument" class="bg-brand-600 text-white px-6 py-2 rounded-lg font-bold shadow-lg hover:bg-brand-700 transition-colors flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
            طباعة التعميم / المذكرة
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="max-w-[21cm] mx-auto p-12 bg-white text-center shadow-2xl">
        <p>جاري التحميل...</p>
      </div>

      <!-- The A4 Print Page -->
      <div v-else class="a4-page portrait bg-white mx-auto shadow-2xl relative overflow-hidden flex flex-col" id="print-area">
        
        <div class="relative z-10 pt-2 pb-12 flex-1 flex flex-col memo-content-wrapper">
          
          <!-- Official Report Header (Edge to edge) -->
          <OfficialMemoHeader 
            :referenceNo="memo.referenceNo || '........................'"
            :docDate="memo.docDate || '........................'"
            :correspondingDate="memo.correspondingDate || '........................'"
            :attachments="memo.attachments || '........................'"
            :bilingual="memo.bilingual || false"
            :securityLevel="memo.securityLevel || 'NORMAL'"
            :securityCustomText="memo.securityCustomText || ''"
            :securityCustomColor="memo.securityCustomColor || '#991b1b'"
            :issuerLine1="memo.issuerLine1 || ''"
            :issuerLine2="memo.issuerLine2 || ''"
            :issuerLine3="memo.issuerLine3 || ''"
          />

          <!-- Memo Body Content with standard official margins -->
          <div class="px-10 mt-0 flex-1 flex flex-col">
          <!-- Type-Specific Dynamic Tables (If needed) -->
          <div v-if="memo.involvedPersonnel && memo.involvedPersonnel.length > 0 && ['ATTENTION_NOTICE', 'WORK_COMMENCEMENT', 'PERSONNEL_MEMO'].includes(memo.documentType)" class="mb-4 overflow-hidden rounded-xl border border-gray-400 shadow-sm print:shadow-none print:border-gray-800">
              <table class="w-full text-center border-collapse text-[1.1rem]" v-if="memo.documentType === 'ATTENTION_NOTICE'">
                <thead>
                  <tr class="bg-gray-100 print:bg-gray-100 font-bold text-gray-800">
                    <th class="border border-gray-400 py-2.5 w-12">م</th>
                    <th class="border border-gray-400 py-2.5 w-28">الرتبة</th>
                    <th class="border border-gray-400 py-2.5 w-36">الرقم العسكري</th>
                    <th class="border border-gray-400 py-2.5 w-1/3">الاسم</th>
                    <th class="border border-gray-400 py-2.5">الإيضاح</th>
                  </tr>
                </thead>
                <tbody class="font-medium text-gray-900">
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i" class="hover:bg-gray-50 bg-white print:bg-white">
                    <td class="border border-gray-400 py-2">{{ Number(i) + 1 }}</td>
                    <td class="border border-gray-400 py-2">{{ person.rank }}</td>
                    <td class="border border-gray-400 py-2 font-mono tracking-wider">{{ person.militaryId }}</td>
                    <td class="border border-gray-400 py-2">{{ person.name }}</td>
                    <td class="border border-gray-400 py-2">{{ person.clarification }}</td>
                  </tr>
                </tbody>
              </table>

              <table class="w-full text-center border-collapse text-[0.75rem] print:text-[0.7rem] font-cairo" v-else-if="memo.documentType === 'WORK_COMMENCEMENT'">
                <thead>
                  <tr class="bg-gray-100 print:bg-gray-100 font-bold text-gray-800 leading-tight">
                    <th class="border border-gray-400 py-1 print:py-0.5 w-6">م</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">الرتبة</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">الرقم العسكري</th>
                    <th class="border border-gray-400 py-1 print:py-0.5 whitespace-nowrap">الاسم</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">الرقم الوطني</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">تاريخ المباشرة</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">مكان العمل</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">محل الخدمة</th>
                    <th class="border border-gray-400 py-1 print:py-0.5">رقم الهاتف</th>
                    <th class="border border-gray-400 py-1 print:py-0.5 w-16">ملاحظات</th>
                  </tr>
                </thead>
                <tbody class="font-medium text-gray-900 leading-tight">
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i" class="bg-white print:bg-white hover:bg-gray-50 transition-colors">
                    <td class="border border-gray-400 py-1.5 px-0.5 bg-gray-50 print:bg-gray-50">{{ Number(i) + 1 }}</td>
                    <td class="border border-gray-400 py-1.5 px-0.5 whitespace-nowrap">{{ person.rank }}</td>
                    <td class="border border-gray-400 py-1.5 px-0.5 font-mono tracking-wider whitespace-nowrap text-[0.7rem]">{{ person.militaryId }}</td>
                    <td class="border border-gray-400 py-1.5 px-1.5 text-right font-bold whitespace-nowrap">{{ person.name }}</td>
                    <td class="border border-gray-400 py-1.5 px-0.5 font-mono text-[0.7rem]">{{ person.nationalId }}</td>
                    <td class="border border-gray-400 py-1.5 px-0.5 whitespace-nowrap text-[0.7rem]" dir="ltr">{{ person.commencementDate }}</td>
                    <td class="border border-gray-400 py-1.5 px-1">{{ person.workplace }}</td>
                    <td class="border border-gray-400 py-1.5 px-1">{{ person.serviceLocation }}</td>
                    <td class="border border-gray-400 py-1.5 px-0.5 font-mono text-[0.7rem]">{{ person.phone }}</td>
                    <td class="border border-gray-400 py-1.5 px-1 text-[0.7rem] text-right">{{ person.secondaryNotes || person.notes }}</td>
                  </tr>
                </tbody>
              </table>

              <table class="w-full text-center border-collapse text-[0.85rem] print:text-[0.75rem]" v-else-if="memo.documentType === 'PERSONNEL_MEMO'">
                <thead>
                  <tr class="bg-gray-100 print:bg-gray-100 font-bold text-gray-800">
                    <th class="border border-gray-400 py-2 print:py-1 w-10">م</th>
                    <th v-if="memo.visibleColumns?.rank" class="border border-gray-400 py-2 print:py-1">الرتبة</th>
                    <th v-if="memo.visibleColumns?.militaryId" class="border border-gray-400 py-2 print:py-1">الرقم العسكري</th>
                    <th class="border border-gray-400 py-2 print:py-1 w-1/4">الاسم الرباعي واللقب</th>
                    <th v-if="memo.visibleColumns?.nationalId" class="border border-gray-400 py-2 print:py-1">الرقم الوطني</th>
                    <th v-if="memo.visibleColumns?.status" class="border border-gray-400 py-2 print:py-1">الحالة</th>
                    <th v-if="memo.visibleColumns?.jobTitle" class="border border-gray-400 py-2 print:py-1">المسمى الوظيفي</th>
                    <th v-if="memo.visibleColumns?.position" class="border border-gray-400 py-2 print:py-1">المنصب</th>
                    <th v-if="memo.visibleColumns?.qualification" class="border border-gray-400 py-2 print:py-1">المؤهل</th>
                    <th v-if="memo.visibleColumns?.joinDate" class="border border-gray-400 py-2 print:py-1">تاريخ التجنيد</th>
                    <th v-if="memo.visibleColumns?.workplace" class="border border-gray-400 py-2 print:py-1">مكان العمل</th>
                    <th v-if="memo.visibleColumns?.serviceLocation" class="border border-gray-400 py-2 print:py-1">محل الخدمة</th>
                    <th v-if="memo.visibleColumns?.commencementDate" class="border border-gray-400 py-2 print:py-1">تاريخ المباشرة</th>
                    <th v-if="memo.visibleColumns?.phone" class="border border-gray-400 py-2 print:py-1">رقم الهاتف</th>
                    <th v-if="memo.visibleColumns?.clarification" class="border border-gray-400 py-2 print:py-1">الإيضاح</th>
                    <th v-if="memo.visibleColumns?.correctName" class="border border-gray-400 py-2 print:py-1">الاسم الصحيح</th>
                    <th v-if="memo.visibleColumns?.wrongName" class="border border-gray-400 py-2 print:py-1">الاسم الخطأ</th>
                    <th v-if="memo.visibleColumns?.correctionTarget" class="border border-gray-400 py-2 print:py-1">المطلوب تصحيحه</th>
                    <th v-if="memo.visibleColumns?.notes" class="border border-gray-400 py-2 print:py-1">ملاحظات</th>
                  </tr>
                </thead>
                <tbody class="font-medium text-gray-900">
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i" class="hover:bg-gray-50 bg-white print:bg-white transition-colors">
                    <td class="border border-gray-400 py-1.5 px-1 bg-gray-50 print:bg-gray-50">{{ Number(i) + 1 }}</td>
                    <td v-if="memo.visibleColumns?.rank" class="border border-gray-400 py-1.5 px-1">{{ person.rank }}</td>
                    <td v-if="memo.visibleColumns?.militaryId" class="border border-gray-400 py-1.5 px-1 font-mono tracking-wider">{{ person.militaryId }}</td>
                    <td class="border border-gray-400 py-1.5 px-2 text-right">{{ person.name }}</td>
                    <td v-if="memo.visibleColumns?.nationalId" class="border border-gray-400 py-1.5 px-1">{{ person.nationalId }}</td>
                    <td v-if="memo.visibleColumns?.status" class="border border-gray-400 py-1.5 px-1">{{ person.status }}</td>
                    <td v-if="memo.visibleColumns?.jobTitle" class="border border-gray-400 py-1.5 px-1">{{ person.jobTitle }}</td>
                    <td v-if="memo.visibleColumns?.position" class="border border-gray-400 py-1.5 px-1">{{ person.position }}</td>
                    <td v-if="memo.visibleColumns?.qualification" class="border border-gray-400 py-1.5 px-1">{{ person.qualification }}</td>
                    <td v-if="memo.visibleColumns?.joinDate" class="border border-gray-400 py-1.5 px-1">{{ person.joinDate }}</td>
                    <td v-if="memo.visibleColumns?.workplace" class="border border-gray-400 py-1.5 px-1">{{ person.workplace }}</td>
                    <td v-if="memo.visibleColumns?.serviceLocation" class="border border-gray-400 py-1.5 px-1">{{ person.serviceLocation }}</td>
                    <td v-if="memo.visibleColumns?.commencementDate" class="border border-gray-400 py-1.5 px-1 whitespace-nowrap">{{ person.commencementDate }}</td>
                    <td v-if="memo.visibleColumns?.phone" class="border border-gray-400 py-1.5 px-1">{{ person.phone }}</td>
                    <td v-if="memo.visibleColumns?.clarification" class="border border-gray-400 py-1.5 px-1">{{ person.clarification }}</td>
                    <td v-if="memo.visibleColumns?.correctName" class="border border-gray-400 py-1.5 px-1">{{ person.correctName }}</td>
                    <td v-if="memo.visibleColumns?.wrongName" class="border border-gray-400 py-1.5 px-1">{{ person.wrongName }}</td>
                    <td v-if="memo.visibleColumns?.correctionTarget" class="border border-gray-400 py-1.5 px-1">{{ person.correctionTarget }}</td>
                    <td v-if="memo.visibleColumns?.notes" class="border border-gray-400 py-1.5 px-1">{{ person.secondaryNotes || person.notes }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

          <!-- Addressees -->
          <div class="mb-6 memo-addressees px-8">
            <div v-for="(addr, i) in memo.addressees" :key="i" class="flex justify-between items-end mb-2 leading-none" :class="[memo.typography?.addressee?.weight || 'font-bold', { 'underline underline-offset-4': memo.typography?.addressee?.underline }]" :style="{ fontSize: getFontSize(memo.typography?.addressee?.size, 1.3), fontFamily: memo.typography?.addressee?.family || 'Cairo' }">
              <div class="flex items-baseline">
                <span v-if="addr.prefix" class="ml-2">{{ addr.prefix }}</span>
                <span>{{ addr.name }}</span>
              </div>
              <div v-if="addr.suffix" class="text-left">
                {{ addr.suffix }}
              </div>
            </div>
          </div>

          <!-- Official Greeting -->
          <div class="px-8 mb-4 mt-2 text-center">
            <span :class="[memo.typography?.greeting?.weight || 'font-bold', { 'underline underline-offset-4': memo.typography?.greeting?.underline }]" :style="{ fontSize: getFontSize(memo.typography?.greeting?.size, 1.6), fontFamily: memo.typography?.greeting?.family || '\'Aref Ruqaa\', \'Amiri\', \'Traditional Arabic\', serif' }">
              تحية طيبة وبعد ،،،
            </span>
          </div>

          <!-- Subject -->
          <div v-if="memo.subject" class="mb-4 text-center" :style="{ fontFamily: memo.typography?.subject?.family || 'Cairo' }">
            <span class="tracking-tight pb-1 inline-block" :class="[memo.typography?.subject?.weight || 'font-black', { 'border-b-[3px] border-black': memo.typography?.subject?.underline !== false }]" :style="{ fontSize: getFontSize(memo.typography?.subject?.size, 1.4) }">
              الموضوع / {{ memo.subject }}
            </span>
          </div>

          <!-- Memo Body (Fully User Controlled) -->
          <div class="flex-none ck-content memo-body text-gray-900 mb-4 px-8 text-justify" :class="[memo.typography?.body?.weight || 'font-normal', { 'underline underline-offset-4': memo.typography?.body?.underline }]" :style="{ textJustify: 'inter-word', textAlign: 'justify', fontSize: getFontSize(memo.typography?.body?.size, 1.1), fontFamily: memo.typography?.body?.family || 'Cairo' }" v-html="memo.body"></div>

          <!-- Memo Conclusion (Action Required) -->
          <div v-if="memo.conclusion" class="px-8 mt-2" :class="memo.signatureSettings?.showLabels !== false ? 'flex-1' : 'flex-none mb-4'">
             <!-- Explicit 'وعليه' Separator -->
             <div class="text-right mb-2">
               <span class="tracking-tight pb-1 inline-block" :class="[memo.typography?.conclusionSeparator?.weight || 'font-black', { 'border-b-[3px] border-black': memo.typography?.conclusionSeparator?.underline !== false }]" :style="{ fontSize: getFontSize(memo.typography?.conclusionSeparator?.size, 1.4), fontFamily: memo.typography?.conclusionSeparator?.family || 'Cairo' }">وعليه :</span>
             </div>
             <div class="ck-content memo-body text-gray-900 text-justify" :class="[memo.typography?.conclusionBody?.weight || 'font-normal', { 'underline underline-offset-4': memo.typography?.conclusionBody?.underline }]" :style="{ textJustify: 'inter-word', textAlign: 'justify', fontSize: getFontSize(memo.typography?.conclusionBody?.size, 1.1), fontFamily: memo.typography?.conclusionBody?.family || 'Cairo' }" v-html="memo.conclusion"></div>
          </div>

          <!-- Official Custom Signatures Footer -->
          <div class="pt-4 flex flex-col w-full" :class="memo.signatureSettings?.showLabels !== false ? 'mt-auto border-t-2 border-black' : 'mt-8 flex-1'">
            <OfficialMemoFooter :signatures="memo.signatures" :settings="memo.signatureSettings" :typography="memo.typography?.signatures" class="flex-1 flex flex-col w-full" />
          </div>

          </div> <!-- Close Body Content Wrapper -->

        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import OfficialMemoHeader from '@/components/common/OfficialMemoHeader.vue'
import OfficialMemoFooter from '@/components/common/OfficialMemoFooter.vue'

const router = useRouter()
const loading = ref(true)
const memo = ref<any>({})

const loadMemo = () => {
  const draftStr = localStorage.getItem('official_memo_draft')
  if (draftStr) {
    memo.value = JSON.parse(draftStr)
  } else {
    router.replace('/admin/documents/memo-builder')
  }
  loading.value = false
}

const getFontSize = (sizeVal: string | number | undefined, defaultSize: number) => {
  if (!sizeVal) return `${defaultSize}rem`
  if (typeof sizeVal === 'string' && sizeVal.includes('rem')) return sizeVal
  return `${sizeVal}rem`
}

const printDocument = () => {
  window.print()
}

const closePreview = () => {
  window.close()
  setTimeout(() => {
    router.back()
  }, 100)
}

onMounted(() => {
  loadMemo()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800;900&family=Dancing+Script:wght@400..700&family=Noto+Nastaliq+Urdu:wght@400..700&display=swap');

/* احترام التنسيقات (المحاذاة) القادمة من محرر النصوص */
:deep(.ck-content .text-align-center),
:deep(.ck-content.text-align-center) {
  text-align: center !important;
}
:deep(.ck-content .text-align-left),
:deep(.ck-content.text-align-left) {
  text-align: left !important;
}
:deep(.ck-content .text-align-right),
:deep(.ck-content.text-align-right) {
  text-align: right !important;
}
:deep(.ck-content .text-align-justify),
:deep(.ck-content.text-align-justify) {
  text-align: justify !important;
}

.print-container {
  font-family: 'Arial', 'Tajawal', sans-serif;
}

.a4-page {
  width: 21cm;
  min-height: 29.7cm;
  background: white;
  font-family: 'Arial', 'Tajawal', sans-serif;
}

/* Specific styling for the memo addressees and subject */
.memo-addressees {
  font-family: 'Arial', 'Tajawal', sans-serif;
}
.memo-content-wrapper h2 {
  font-family: 'Arial', 'Cairo', sans-serif;
}

/* CKEditor Content Styles specifically for Print/Preview */
.ck-content.memo-body {
  font-family: 'Arial', 'Tajawal', sans-serif;
  line-height: 1.8;
  font-size: 1.25rem;
  font-weight: 600;
  text-align: justify;
}
.ck-content h1, .ck-content h2, .ck-content h3 {
  margin-bottom: 1rem;
  font-weight: 800;
}
.ck-content p {
  margin-bottom: 0.25rem;
}
.signature-content p {
  margin-bottom: 0;
}
.ck-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}
.ck-content table td, .ck-content table th {
  border: 1px solid #000;
  padding: 10px;
}
.ck-content img {
  max-width: 100%;
  height: auto;
}

.font-cairo {
  font-family: 'Cairo', sans-serif !important;
}

@media print {
  body * {
    visibility: hidden;
  }
  .no-print {
    display: none !important;
  }
  #print-area, #print-area * {
    visibility: visible;
  }
  #print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 21cm;
    height: 29.7cm;
    margin: 0;
    padding: 0;
    box-shadow: none;
  }
  @page {
    size: A4 portrait;
    margin: 0;
  }
}
</style>
