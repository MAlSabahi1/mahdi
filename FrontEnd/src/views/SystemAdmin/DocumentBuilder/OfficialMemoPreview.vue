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
          <div class="px-10 mt-2 flex-1 flex flex-col">
          <!-- Involved Personnel Table (For Disciplinary/Attention Notices) -->
          <div v-if="memo.documentType === 'ATTENTION_NOTICE' && memo.involvedPersonnel && memo.involvedPersonnel.length > 0" class="mb-8 px-4 mt-2">
            <div class="rounded-2xl border-2 border-gray-500 overflow-hidden shadow-sm">
              <table class="w-full text-center border-collapse text-[1.1rem]">
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
                  <tr v-for="(person, i) in memo.involvedPersonnel" :key="i" class="hover:bg-gray-50">
                    <td class="border border-gray-400 py-2">{{ Number(i) + 1 }}</td>
                    <td class="border border-gray-400 py-2">{{ person.rank }}</td>
                    <td class="border border-gray-400 py-2 font-mono tracking-wider">{{ person.militaryId }}</td>
                    <td class="border border-gray-400 py-2">{{ person.name }}</td>
                    <td class="border border-gray-400 py-2">{{ person.clarification }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Involved Personnel Table (For Work Commencement) -->
          <div v-if="memo.documentType === 'WORK_COMMENCEMENT' && memo.involvedPersonnel && memo.involvedPersonnel.length > 0" class="mb-8 px-4 mt-2">
            <div class="rounded-2xl border-2 border-gray-500 overflow-hidden shadow-sm">
              <table class="w-full text-center border-collapse text-[1.05rem]">
                <thead>
                  <tr class="bg-gray-100 print:bg-gray-100 font-bold text-gray-800">
                    <th class="border border-gray-400 py-2.5 w-10">م</th>
                    <th class="border border-gray-400 py-2.5 w-24">الرتبة</th>
                    <th class="border border-gray-400 py-2.5 w-32">الرقم العسكري</th>
                    <th class="border border-gray-400 py-2.5 w-1/4">الاسم</th>
                    <th class="border border-gray-400 py-2.5 w-1/5">مكان العمل</th>
                    <th class="border border-gray-400 py-2.5 w-1/5">محل الخدمة</th>
                  </tr>
                </thead>
                <tbody class="font-medium text-gray-900">
                  <template v-for="(person, i) in memo.involvedPersonnel" :key="i">
                    <!-- Main Row -->
                    <tr>
                      <td rowspan="2" class="border border-gray-400 py-2 bg-gray-50 print:bg-gray-50 align-middle">{{ Number(i) + 1 }}</td>
                      <td class="border border-gray-400 py-2">{{ person.rank }}</td>
                      <td class="border border-gray-400 py-2 font-mono tracking-wider">{{ person.militaryId }}</td>
                      <td class="border border-gray-400 py-2">{{ person.name }}</td>
                      <td class="border border-gray-400 py-2">{{ person.workplace }}</td>
                      <td class="border border-gray-400 py-2">{{ person.serviceLocation }}</td>
                    </tr>
                    <!-- Sub Row for extra details -->
                    <tr class="bg-gray-50 print:bg-gray-50 text-[0.95rem]">
                      <td colspan="5" class="border border-gray-400 py-2 px-4">
                        <div class="flex justify-between items-center text-right text-gray-800">
                          <span v-if="person.commencementDate"><span class="text-gray-500 ml-1 font-bold">تاريخ المباشرة:</span> {{ person.commencementDate }}</span>
                          <span v-if="person.nationalId"><span class="text-gray-500 ml-1 font-bold">الرقم الوطني:</span> <span class="font-mono tracking-wider">{{ person.nationalId }}</span></span>
                          <span v-if="person.phone"><span class="text-gray-500 ml-1 font-bold">رقم الهاتف:</span> <span class="font-mono tracking-wider">{{ person.phone }}</span></span>
                          <span v-if="person.secondaryNotes || person.notes"><span class="text-gray-500 ml-1 font-bold">ملاحظات:</span> {{ person.secondaryNotes || person.notes }}</span>
                        </div>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Addressees -->
          <div class="mb-8 memo-addressees">
            <div v-for="(addr, i) in memo.addressees" :key="i" class="flex justify-between items-center mb-1.5 font-bold text-[1.25rem]">
              <div class="flex items-center">
                <span v-if="addr.prefix" class="ml-2 font-black">{{ addr.prefix }}</span>
                <span>{{ addr.name }}</span>
              </div>
              <div v-if="addr.suffix" class="text-left font-black">
                {{ addr.suffix }}
              </div>
            </div>
            <div class="mt-6 text-[1.2rem] font-bold">
              السلام عليكم ورحمة الله وبركاته.. وبعد،،
            </div>
          </div>

          <!-- Subject -->
          <div v-if="memo.subject" class="mb-10 mt-2 text-center relative w-full flex items-center justify-center">
            <!-- Decorative line -->
            <div class="flex-1 border-b-[3px] border-black"></div>
            <h2 class="mx-6 font-black text-2xl tracking-tight leading-none whitespace-nowrap">الموضـــــــــــوع / {{ memo.subject }}</h2>
            <div class="flex-1 border-b-[3px] border-black"></div>
          </div>



          <!-- Memo Body -->
          <main class="flex-none ck-content memo-body text-gray-900 mb-6 px-2" v-html="memo.body"></main>

          <!-- Memo Conclusion -->
          <div v-if="memo.conclusion" class="flex-1 px-2">
             <div class="ck-content memo-body font-bold text-gray-900" v-html="memo.conclusion"></div>
          </div>

          <!-- Official Custom Signatures Footer -->
          <div class="mt-auto pt-4 border-t-2 border-black">
            <OfficialMemoFooter :signatures="memo.signatures" />
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
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800;900&display=swap');

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
  margin-bottom: 1.2rem;
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
