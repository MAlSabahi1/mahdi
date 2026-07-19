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

      <!-- The A4 Print Pages (Bundle) -->
      <div v-else class="flex flex-col gap-8 print-bundle-container" id="print-area">
        
        <!-- Document 1: The Cover Memo -->
        <div class="a4-page portrait bg-white mx-auto shadow-2xl relative overflow-hidden flex flex-col print-page-break">
          
          <div class="relative z-10 pt-2 pb-4 flex-1 flex flex-col memo-content-wrapper">
          
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
          <div v-if="memo.includeTable !== false && memo.involvedPersonnel && memo.involvedPersonnel.length > 0 && ['ATTENTION_NOTICE', 'WORK_COMMENCEMENT', 'PERSONNEL_MEMO', 'CORRECTION'].includes(memo.documentType)" class="mb-8 print:mb-10 table-wrapper -mx-4 print:-mx-4">
              <table class="official-table" v-if="memo.documentType === 'ATTENTION_NOTICE'">
                <thead>
                  <tr>
                    <th style="width: 30px">م</th>
                    <th style="white-space: nowrap">الرتبة</th>
                    <th style="white-space: nowrap">الرقم العسكري</th>
                    <th>الاسم</th>
                    <th>الإيضاح</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i">
                    <td>{{ Number(i) + 1 }}</td>
                    <td style="white-space: nowrap">{{ person.rank }}</td>
                    <td style="white-space: nowrap">{{ person.militaryId }}</td>
                    <td style="font-weight: 700;">{{ person.name }}</td>
                    <td>{{ person.clarification }}</td>
                  </tr>
                </tbody>
              </table>

              <table class="official-table" v-else-if="memo.documentType === 'WORK_COMMENCEMENT'">
                <thead>
                  <tr>
                    <th style="width: 30px">م</th>
                    <th style="white-space: nowrap">الرتبة</th>
                    <th style="white-space: nowrap">الرقم العسكري</th>
                    <th>الاسم</th>
                    <th style="white-space: nowrap">الرقم الوطني</th>
                    <th style="white-space: nowrap">تاريخ المباشرة</th>
                    <th>مكان العمل</th>
                    <th>محل الخدمة</th>
                    <th style="white-space: nowrap">رقم الهاتف</th>
                    <th>ملاحظات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i">
                    <td>{{ Number(i) + 1 }}</td>
                    <td style="white-space: nowrap">{{ person.rank }}</td>
                    <td style="white-space: nowrap">{{ person.militaryId }}</td>
                    <td style="font-weight: 700;">{{ person.name }}</td>
                    <td style="white-space: nowrap">{{ person.nationalId }}</td>
                    <td style="white-space: nowrap; direction: ltr;">{{ person.commencementDate }}</td>
                    <td>{{ person.workplace }}</td>
                    <td>{{ person.serviceLocation }}</td>
                    <td style="white-space: nowrap">{{ person.phone }}</td>
                    <td>{{ person.secondaryNotes || person.notes }}</td>
                  </tr>
                </tbody>
              </table>

              <table class="official-table" v-else-if="memo.documentType === 'CORRECTION'">
                <thead>
                  <tr>
                    <th style="width: 30px">م</th>
                    <th style="white-space: nowrap">الرتبة</th>
                    <th style="white-space: nowrap">الرقم العسكري</th>
                    <th>الاسم الصحيح</th>
                    <th>الاسم الخطأ</th>
                    <th>المطلوب تصحيحه</th>
                    <th>ملاحظات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i">
                    <td>{{ Number(i) + 1 }}</td>
                    <td style="white-space: nowrap">{{ person.rank }}</td>
                    <td style="white-space: nowrap">{{ person.militaryId }}</td>
                    <td style="font-weight: 700;">{{ person.correctName }}</td>
                    <td>{{ person.wrongName || person.name }}</td>
                    <td>{{ person.correctionTarget }}</td>
                    <td>{{ person.notes || person.secondaryNotes }}</td>
                  </tr>
                </tbody>
              </table>

              <table class="official-table" v-else-if="memo.documentType === 'PERSONNEL_MEMO'">
                <thead>
                  <tr>
                    <th style="width: 30px">م</th>
                    <th v-if="memo.visibleColumns?.rank" style="white-space: nowrap">الرتبة</th>
                    <th v-if="memo.visibleColumns?.militaryId" style="white-space: nowrap">الرقم العسكري</th>
                    <th>الاسم الرباعي واللقب</th>
                    <th v-if="memo.visibleColumns?.nationalId" style="white-space: nowrap">الرقم الوطني</th>
                    <th v-if="memo.visibleColumns?.status" style="white-space: nowrap">الحالة</th>
                    <th v-if="memo.visibleColumns?.jobTitle">المسمى الوظيفي</th>
                    <th v-if="memo.visibleColumns?.position">المنصب</th>
                    <th v-if="memo.visibleColumns?.qualification">المؤهل</th>
                    <th v-if="memo.visibleColumns?.joinDate" style="white-space: nowrap">تاريخ التجنيد</th>
                    <th v-if="memo.visibleColumns?.workplace">مكان العمل</th>
                    <th v-if="memo.visibleColumns?.serviceLocation">محل الخدمة</th>
                    <th v-if="memo.visibleColumns?.commencementDate" style="white-space: nowrap">تاريخ المباشرة</th>
                    <th v-if="memo.visibleColumns?.phone" style="white-space: nowrap">رقم الهاتف</th>
                    <th v-if="memo.visibleColumns?.clarification">الإيضاح</th>
                    <th v-if="memo.visibleColumns?.correctName" style="font-weight: 700;">الاسم الصحيح</th>
                    <th v-if="memo.visibleColumns?.wrongName">الاسم الخطأ</th>
                    <th v-if="memo.visibleColumns?.correctionTarget">المطلوب تصحيحه</th>
                    <th v-if="memo.visibleColumns?.notes">ملاحظات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i">
                    <td>{{ Number(i) + 1 }}</td>
                    <td v-if="memo.visibleColumns?.rank" style="white-space: nowrap">{{ person.rank }}</td>
                    <td v-if="memo.visibleColumns?.militaryId" style="white-space: nowrap">{{ person.militaryId }}</td>
                    <td style="font-weight: 700;">{{ person.name }}</td>
                    <td v-if="memo.visibleColumns?.nationalId" style="white-space: nowrap">{{ person.nationalId }}</td>
                    <td v-if="memo.visibleColumns?.status" style="white-space: nowrap">{{ person.status }}</td>
                    <td v-if="memo.visibleColumns?.jobTitle">{{ person.jobTitle }}</td>
                    <td v-if="memo.visibleColumns?.position">{{ person.position }}</td>
                    <td v-if="memo.visibleColumns?.qualification">{{ person.qualification }}</td>
                    <td v-if="memo.visibleColumns?.joinDate" style="white-space: nowrap">{{ person.joinDate }}</td>
                    <td v-if="memo.visibleColumns?.workplace">{{ person.workplace }}</td>
                    <td v-if="memo.visibleColumns?.serviceLocation">{{ person.serviceLocation }}</td>
                    <td v-if="memo.visibleColumns?.commencementDate" style="white-space: nowrap; direction: ltr;">{{ person.commencementDate }}</td>
                    <td v-if="memo.visibleColumns?.phone" style="white-space: nowrap">{{ person.phone }}</td>
                    <td v-if="memo.visibleColumns?.clarification">{{ person.clarification }}</td>
                    <td v-if="memo.visibleColumns?.correctName" style="font-weight: 700;">{{ person.correctName }}</td>
                    <td v-if="memo.visibleColumns?.wrongName">{{ person.wrongName }}</td>
                    <td v-if="memo.visibleColumns?.correctionTarget">{{ person.correctionTarget }}</td>
                    <td v-if="memo.visibleColumns?.notes">{{ person.secondaryNotes || person.notes }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

          <!-- Addressees -->
          <div class="mb-6 mt-4 print:mt-6 memo-addressees">
            <div v-for="(addr, i) in memo.addressees" :key="i" class="flex justify-between items-end mb-5 text-black">
              <div :style="{ fontFamily: memo.typography?.addressee?.family || 'Cairo' }">
                <span class="tracking-wide inline-block font-black" :class="{ 'border-b-[3px] border-black': memo.typography?.addressee?.underline }" :style="{ fontSize: memo.typography?.addressee?.size ? getFontSize(memo.typography.addressee.size, 1.4) : '20px' }">
                  {{ addr.prefix ? addr.prefix + ' ' : '' }}{{ applyOfficialTatweel(addr.name) }}
                </span>
              </div>
              <div v-if="addr.suffix" class="text-left" :style="{ fontFamily: memo.typography?.addressee?.family || 'Cairo' }">
                <span class="tracking-widest inline-block font-black" :class="{ 'border-b-[3px] border-black': memo.typography?.addressee?.underline }" :style="{ fontSize: memo.typography?.addressee?.size ? getFontSize(memo.typography.addressee.size, 1.4) : '21px' }">
                  {{ applyOfficialTatweel(addr.suffix) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Official Greeting -->
          <div class="text-center mb-3 -mt-2">
            <span class="inline-block text-black" :class="[memo.typography?.greeting?.weight || 'font-black', { 'underline underline-offset-4': memo.typography?.greeting?.underline }]" :style="{ fontSize: memo.typography?.greeting?.size ? getFontSize(memo.typography.greeting.size, 1.6) : '30px', fontFamily: '\'Samt7017\', \'Aref Ruqaa\', serif' }">
              تحيـــــة طيبـــــة وبعـــــد ،،،
            </span>
          </div>

          <!-- Subject -->
          <div v-if="memo.subject" class="mb-4 text-center text-black" :style="{ fontFamily: memo.typography?.subject?.family || 'Cairo' }">
            <span class="tracking-wide pb-1 inline-block font-black" :class="{ 'border-b-[3px] border-black': memo.typography?.subject?.underline !== false }" :style="{ fontSize: memo.typography?.subject?.size ? getFontSize(memo.typography.subject.size, 1.4) : '20px' }">
              الموضوع / {{ applyOfficialTatweel(memo.subject) }}
            </span>
          </div>

          <!-- Memo Body (Fully User Controlled) -->
          <div class="flex-none ck-content memo-body text-gray-900 mb-4 text-justify" :class="[memo.typography?.body?.weight || 'font-bold', { 'underline underline-offset-4': memo.typography?.body?.underline }]" :style="{ textJustify: 'inter-word', textAlign: 'justify', fontSize: getFontSize(memo.typography?.body?.size, 1.1), fontFamily: memo.typography?.body?.family || 'Cairo' }" v-html="memo.body"></div>

          <!-- Memo Conclusion (Action Required) -->
          <div v-if="memo.conclusion" class="mt-2 text-black" :class="memo.signatureSettings?.showLabels !== false ? 'flex-1' : 'flex-none mb-4'">
             <!-- Explicit 'وعليه' Separator -->
             <div class="text-right mb-2">
               <span class="tracking-wide pb-1 inline-block font-black" :class="{ 'border-b-[3px] border-black': memo.typography?.conclusionSeparator?.underline !== false }" :style="{ fontSize: memo.typography?.conclusionSeparator?.size ? getFontSize(memo.typography.conclusionSeparator.size, 1.4) : '20px', fontFamily: memo.typography?.conclusionSeparator?.family || 'Cairo' }">وعليـــــه :</span>
             </div>
             <div class="ck-content memo-body text-gray-900 text-justify" :class="[memo.typography?.conclusionBody?.weight || 'font-bold', { 'underline underline-offset-4': memo.typography?.conclusionBody?.underline }]" :style="{ textJustify: 'inter-word', textAlign: 'justify', fontSize: getFontSize(memo.typography?.conclusionBody?.size, 1.1), fontFamily: memo.typography?.conclusionBody?.family || 'Cairo' }" v-html="memo.conclusion"></div>
          </div>

          <!-- Official Custom Signatures Footer -->
          <div class="pt-4 flex flex-col w-full" :class="memo.signatureSettings?.showLabels !== false ? 'mt-auto border-t-2 border-black' : 'mt-8 flex-1'">
            <OfficialMemoFooter :signatures="memo.signatures" :settings="memo.signatureSettings" :typography="memo.typography?.signatures" :referenceNo="memo.referenceNo" class="flex-1 flex flex-col w-full" />
          </div>

          </div> <!-- Close Body Content Wrapper -->

          </div> <!-- Close content wrapper -->
        </div> <!-- Close Memo Page (a4-page) -->

        <!-- Document 2: Model 23 Matching List / Correction List (Landscape) -->
        <div v-if="memo.documentType === 'CORRECTION' && memo.isNameCorrection" class="a4-page landscape-section bg-white mx-auto shadow-2xl relative overflow-hidden flex flex-col print-page-break p-8">
          <AuditMovementReports reportIdProp="23" :isEmbedded="true" :monthProp="memoMonth" />
        </div>

        <!-- Document 3: Attachments (Subsequent portrait pages) -->
        <div 
          v-for="(att, aIdx) in allAttachments" 
          :key="'att-preview-'+aIdx" 
          class="a4-page portrait bg-white mx-auto shadow-2xl relative flex flex-col print-page-break px-8 py-10"
        >
          <!-- Header for attachment context -->
          <div class="w-full flex justify-between items-center mb-4 pb-2 border-b border-gray-300 font-cairo text-sm text-gray-700">
            <div>
              <span class="text-gray-500">نوع الوثيقة:</span>
              <span class="mr-1 font-bold">{{ att.document_type_display }}</span>
            </div>
            <div>
              <span class="text-gray-500">تخص الموظف:</span>
              <span class="mr-1 font-bold">{{ att.personnel_name }}</span>
            </div>
          </div>
          
          <template v-if="!att.url.toLowerCase().endsWith('.pdf')">
            <div class="flex-1 w-full flex items-center justify-center min-h-0 py-2">
              <img v-show="!att._imageError" :src="resolveAttachmentUrl(att.url)" @error="att._imageError = resolveAttachmentUrl(att.url)" class="max-w-full max-h-full object-contain rounded-lg shadow-sm" alt="مرفق" />
            </div>
            <div v-if="att._imageError" class="text-center p-8 bg-red-50 border-2 border-red-200 border-dashed rounded-xl w-full max-w-2xl mx-auto mt-4">
              <p class="font-bold text-red-700 text-lg mb-2">فشل تحميل الصورة</p>
              <p class="text-gray-700 text-sm dir-ltr font-mono bg-white p-2 border rounded shadow-inner break-all">{{ att._imageError }}</p>
            </div>
          </template>
          <template v-else>
            <div class="text-center p-10 border-2 border-dashed border-gray-400 bg-gray-50 rounded-xl my-auto w-full max-w-2xl">
              <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
              </svg>
              <p class="font-bold text-gray-800 text-2xl mb-2">هذا المرفق بصيغة PDF</p>
              <p class="text-gray-600 text-lg mb-4">النظام لا يمكنه دمج ملفات PDF داخل حزمة الطباعة المباشرة.</p>
              <a :href="resolveAttachmentUrl(att.url)" target="_blank" class="text-brand-600 font-bold underline text-lg">اضغط هنا لفتح وطباعة المرفق بشكل مستقل</a>
            </div>
          </template>
          
          <!-- Footer for attachment context -->
          <div class="w-full text-center mt-auto pt-4 text-xs text-gray-500 font-mono tracking-wider">
            REF: ATT-{{ att.form_id }}-{{ aIdx }} | {{ new Date().toLocaleString('en-GB') }}
          </div>
        </div>


      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import OfficialMemoHeader from '@/components/common/OfficialMemoHeader.vue'
import OfficialMemoFooter from '@/components/common/OfficialMemoFooter.vue'
import CorrectionListPrintForm from '@/views/Services/PrintTemplates/CorrectionListPrintForm.vue'
import AuditMovementReports from '@/views/Reports/AuditMovementReports.vue'

import { useServicesStore } from '@/stores/services'
import { useCorrectionStore } from '@/stores/correction'

const router = useRouter()
const servicesStore = useServicesStore()
const correctionStore = useCorrectionStore()

const loading = ref(true)
const memo = ref<any>({})

// Helper to automatically apply Arabic Tatweel (stretching) to official names, smartly avoiding overstretching
const applyOfficialTatweel = (text: string) => {
  if (!text) return '';
  const targetWords = ['عام', 'العامة', 'المحترم', 'تحية', 'طيبة', 'وبعد', 'وعليه', 'وزارة', 'الداخلية', 'شئون', 'الضباط', 'البشرية', 'المحافظة', 'شرطة', 'الأمن', 'المرور', 'المصلحة', 'الجوازات', 'الأحوال', 'المدنية', 'الجمهورية', 'اليمنية'];
  const connectors = /[بتثجحخسشصضطظعغفقكلمنهيئ]/;
  
  const words = text.split(' ');
  return words.map((word, w) => {
    if (word.includes('ـ')) return word;
    let cleanWord = word.replace(/ـ/g, '');
    
    // Stretch if it's a target word, OR if it's the very last word of the line to balance it
    if (targetWords.includes(cleanWord) || (w === words.length - 1 && cleanWord.length >= 4)) {
      for (let i = word.length - 2; i >= 0; i--) {
        if (connectors.test(word[i])) {
          // Do not break "لا" ligatures
          if (word[i] === 'ل' && ['ا', 'أ', 'إ', 'آ'].includes(word[i+1])) continue;
          return word.slice(0, i + 1) + 'ــــــ' + word.slice(i + 1);
        }
      }
    }
    return word;
  }).join(' ');
};

const mappedCorrections = computed(() => {
  if (!memo.value?.involvedPersonnel) return []
  return memo.value.involvedPersonnel.map((p: any) => ({
    rank: p.rank,
    military_number: p.militaryId,
    full_name: p.wrongName,
    new_value: p.correctName,
    notes: `المطلوب تصحيح: ${p.correctionTarget} \n المبررات: ${p.notes || p.secondaryNotes}`
  }))
})

const memoMonth = computed(() => {
  if (!memo.value?.docDate) return ''
  const cleanDate = memo.value.docDate.replace('م', '').trim()
  if (cleanDate.includes('-')) {
    const parts = cleanDate.split('-')
    if (parts[0].length === 4) return `${parts[0]}-${parts[1]}`
  } else if (cleanDate.includes('/')) {
    const parts = cleanDate.split('/')
    if (parts[2].length === 4) return `${parts[2]}-${parts[1]}`
  }
  return ''
})

const loadedForms = ref<any[]>([])

const allAttachments = computed(() => {
  const list: any[] = []
  for (const form of loadedForms.value) {
    if (form.form_type === 'CORRECTION' || form.correction_type) {
      if (form.supporting_document_url) {
        list.push({
          url: form.supporting_document_url,
          document_type: 'correction_supporting_document',
          document_type_display: 'المستند الداعم لطلب التصحيح',
          personnel_name: form.personnel_name || form.personnel?.full_name || 'غير محدد',
          form_id: form.id
        })
      }
    } else {
      if (form.attachments && form.attachments.length > 0) {
        for (const att of form.attachments) {
          list.push({
            url: att.file || att.file_url || att.url || att.document_path || '',
            document_type: att.document_type || att.label || '',
            document_type_display: translateAttachmentType(att),
            personnel_name: form.personnel?.full_name || form.full_name || 'غير محدد',
            form_id: form.id
          })
        }
      }
    }
  }
  return list
})

function translateAttachmentType(att: any) {
  const key = att.document_type_display || att.document_type || att.label || att.name || att.title || ''
  if (!key) return 'مرفق إضافي'
  const normalizedKey = String(key).toLowerCase().trim()
  const map: Record<string, string> = {
    attorney_id: 'هوية الوكيل',
    power_of_attorney: 'وكالة شرعية',
    legal_power_of_attorney: 'وكالة شرعية',
    'legal power of attorney': 'وكالة شرعية',
    photo: 'صورة شخصية',
    id_card: 'هوية شخصية',
    birth_certificate: 'شهادة ميلاد',
    death_certificate: 'شهادة وفاة',
    medical_report: 'تقرير طبي',
    'national id front': 'الوجه الأمامي للهوية الوطنية',
    'national_id_front': 'الوجه الأمامي للهوية الوطنية',
    'national id back': 'الوجه الخلفي للهوية الوطنية',
    'national_id_back': 'الوجه الخلفي للهوية الوطنية',
    memo: 'مذكرة',
    court_ruling: 'حكم محكمة',
    'court ruling': 'حكم محكمة',
    appointment_ruling: 'حكم تنصيب',
    'appointment ruling': 'حكم تنصيب',
    heir_ruling: 'انحصار ورثة',
    'heir ruling': 'انحصار ورثة',
    order_copy: 'نسخة من أمر التكليف',
    'order copy': 'نسخة من أمر التكليف',
    study_order: 'نسخة من أمر التفرغ الدراسي',
    'study order': 'نسخة من أمر التفرغ الدراسي',
    certified_id: 'نسخة من البطاقة العسكرية/الشخصية',
    'certified id': 'نسخة من البطاقة العسكرية/الشخصية',
    personal_request: 'الطلب الشخصي',
    'personal request': 'الطلب الشخصي',
    approval_document: 'مذكرة الاعتماد',
    'approval document': 'مذكرة الاعتماد',
    ministry_approval: 'موافقة الوزارة',
    'ministry approval': 'موافقة الوزارة',
    agent_id: 'هوية الوكيل',
    'agent id': 'هوية الوكيل',
    personnel_id: 'صورة الهوية',
    'personnel id': 'صورة الهوية',
    secondment_order: 'نسخة من الأمر',
    'secondment order': 'نسخة من الأمر',
    ruling_copy: 'نسخة من الحكم',
    'ruling copy': 'نسخة من الحكم',
    legal_ruling: 'حكم شرعي بالفقدان',
    'legal ruling': 'حكم شرعي بالفقدان',
    newspaper_ad: 'إعلان الجريدة',
    'newspaper ad': 'إعلان الجريدة',
    original_medical_decision: 'القرار الطبي الأصل',
    recent_photo: 'صورة حديثة'
  }
  return map[normalizedKey] || String(key).replace(/_/g, ' ')
}

function resolveAttachmentUrl(url: string) {
  if (!url) return ''
  if (url.startsWith('http://backend:') || url.startsWith('http://api:')) {
    try {
      const urlObj = new URL(url)
      url = `http://127.0.0.1:8000${urlObj.pathname}${urlObj.search}`
    } catch(e) {}
  }
  if (url.startsWith('http')) return url
  if (!url.startsWith('/media') && !url.startsWith('/api') && !url.startsWith('/')) {
    url = '/media/' + url
  } else if (url.startsWith('/') && !url.startsWith('/media') && !url.startsWith('/api')) {
    url = '/media' + url
  }
  if (!url.startsWith('/')) url = '/' + url
  const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'
  const baseUrl = apiUrl.split('/api')[0] || 'http://127.0.0.1:8000'
  return `${baseUrl}${url}`
}

const loadMemo = async () => {
  const draftStr = localStorage.getItem('official_memo_draft')
  if (draftStr) {
    memo.value = JSON.parse(draftStr)
    
    // Fetch all linked forms data if present
    if (memo.value.linkedForms && memo.value.linkedForms.length > 0) {
      for (const lf of memo.value.linkedForms) {
        try {
          let itemData = null;
          if (lf.type === 'CORRECTION') {
            itemData = await correctionStore.fetchCorrectionById(lf.id)
            if (itemData) itemData.form_type = 'CORRECTION'
          } else {
            // Treat as generic service form
            itemData = await servicesStore.fetchFormById(lf.id)
          }
          if (itemData) {
            loadedForms.value.push(itemData)
          }
        } catch(e) {
          console.error('Failed to load linked form', lf, e)
        }
      }
    }
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

@font-face {
  font-family: 'Samt7017';
  src: url('/fonts/samt7017.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}


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
  font-family: 'Cairo', sans-serif;
}

.a4-page {
  width: 21cm;
  min-height: 29.7cm;
  background: white;
  font-family: 'Cairo', sans-serif;
}

/* Specific styling for the memo addressees and subject */
.memo-addressees {
  font-family: 'Cairo', sans-serif;
}
.memo-content-wrapper h2 {
  font-family: 'Cairo', sans-serif;
}

/* CKEditor Content Styles specifically for Print/Preview */
.ck-content.memo-body {
  font-family: 'Cairo', sans-serif;
  line-height: 1.8;
  font-size: 16px;
  font-weight: 400;
  text-align: justify;
  color: #000;
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

/* Official Government Table Styling */
.table-wrapper {
  width: auto !important;
  border: 2px solid #000 !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  margin-bottom: 2px !important;
  background-color: transparent !important;
}
.official-table {
  width: 100% !important;
  border-collapse: collapse !important;
  text-align: center !important;
  background-color: transparent !important;
  table-layout: auto !important;
  word-wrap: break-word !important;
}
.official-table th {
  background-color: var(--th-bg-color, #e8ede1) !important;
  box-shadow: inset 0 0 0 1000px var(--th-bg-color, #e8ede1) !important;
  color: var(--th-text-color, #1a2415) !important;
  font-family: 'Cairo', sans-serif !important;
  font-weight: 700 !important;
  font-size: 12px !important;
  border-bottom: 1.5px solid #000 !important;
  border-left: 1.5px solid #000 !important;
  padding: 3px !important;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}
.official-table td {
  font-family: 'Cairo', sans-serif !important;
  font-weight: 600 !important;
  font-size: 12.5px !important;
  color: #0f172a !important;
  padding: 3px 2px !important;
  border-bottom: 1.5px solid #000 !important;
  border-left: 1.5px solid #000 !important;
}
.official-table th:last-child,
.official-table td:last-child {
  border-left: none !important;
}
.official-table tr:last-child td {
  border-bottom: none !important;
}

@media print {
  /* Reset layout structure on all parent containers to allow correct page rotation flow */
  html, body, #app, #app > div, .print-container {
    display: block !important;
    position: static !important;
    overflow: visible !important;
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
  }

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
    position: static !important;
    display: block !important;
    width: 100% !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
  }
  
  .a4-page.portrait {
    width: 21cm !important;
    height: 29.7cm !important;
    max-height: 29.7cm !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    margin: 0 auto !important;
    padding: 0 !important;
    background: white !important;
  }
  
  .a4-page.landscape-section {
    width: 29.7cm !important;
    height: 21cm !important;
    max-height: 21cm !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    margin: 0 auto !important;
    padding: 0.5cm !important;
    background: white !important;
  }

  .print-page-break {
    page-break-before: always !important;
    break-before: page !important;
  }
  
  /* Print Optimization for Official Table */
  .official-table th {
    padding: 1px !important;
  }
  .official-table td {
    padding: 1px 2px !important;
  }
  .table-wrapper {
    margin-bottom: 2px !important;
  }
  
  /* Ensure the form page containers act perfectly like an A4 page */
  .form-page-container {
    width: 21cm !important;
    min-height: 29.7cm !important;
    background: white;
  }
  
  /* Target the inner container of StatusChangePrintForm to ensure it fills the page */
  .form-page-container > .print-preview-container {
    width: 100% !important;
    height: 100% !important;
    min-height: 29.7cm !important;
    zoom: 1 !important; /* Reset zoom because we're nesting it */
  }
  
  /* Clean up the border inside print */
  .form-page-container .outer-border {
    border: none !important; /* Avoid double borders if we want a clean print */
  }
}
</style>

<style>
@page {
  size: A4 portrait;
  margin: 0 !important;
}
@page landscape-page {
  size: A4 landscape;
  margin: 0 !important;
}
@media print {
  .landscape-section {
    page: landscape-page !important;
  }
}
</style>
