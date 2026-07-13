<template>
  <AdminLayout>
  <div class="print-container min-h-screen bg-gray-100 dark:bg-gray-900 py-8" dir="rtl">
    
    <!-- Action buttons (Hidden in print) -->
    <div class="max-w-[21cm] mx-auto mb-4 flex justify-between items-center no-print">
      <button @click="closePreview" class="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg font-bold hover:bg-gray-300 transition-colors">
        إغلاق المعاينة
      </button>
      <div class="flex gap-2">
        <button @click="printDocument" class="bg-brand-600 text-white px-6 py-2 rounded-lg font-bold shadow-lg hover:bg-brand-700 transition-colors flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
          طباعة القالب
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="max-w-[21cm] mx-auto p-12 bg-white text-center shadow-2xl">
      <p>جاري التحميل...</p>
    </div>

    <!-- The A4 Print Page -->
    <div v-else class="a4-page bg-white mx-auto shadow-2xl relative overflow-hidden flex flex-col portrait" id="print-area">
      
      <!-- Watermark (optional) -->
      <div class="absolute inset-0 flex items-center justify-center opacity-[0.03] pointer-events-none">
        <img src="/images/logo/logo.svg" alt="watermark" class="w-96 h-96 grayscale" onerror="this.style.display='none'">
      </div>

      <div class="relative z-10 p-12 flex-1 flex flex-col">
        
        <!-- Header -->
        <header class="flex justify-between items-start border-b-2 border-gray-800 pb-6 mb-8">
          <div v-for="(block, index) in template.header_blocks" :key="'h'+index" 
               class="flex-1 ck-content font-bold text-gray-800 leading-relaxed text-sm"
               :class="{'text-right': index===0, 'text-center': index===1, 'text-left': index===2}"
               v-html="replaceDynamicFields(block)">
          </div>
        </header>

        <!-- Body Placeholder for Report Template -->
        <main class="flex-1 ck-content text-gray-900 leading-relaxed mb-12 flex items-center justify-center border-4 border-dashed border-gray-200 bg-gray-50 rounded-xl opacity-70">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            <h3 class="text-xl font-bold text-gray-500 mb-2">مساحة التقرير الديناميكية</h3>
            <p class="text-sm text-gray-400">سيتم إدراج بيانات التقرير الفعلي هنا أثناء الطباعة</p>
          </div>
        </main>

        <!-- Footer -->
        <footer class="mt-auto pt-8 flex justify-between items-end border-t border-gray-300">
          <div v-for="(block, index) in template.footer_blocks" :key="'f'+index" 
               class="flex-1 ck-content font-bold text-gray-800 text-sm"
               :class="{'text-right': index===0, 'text-center': index===1, 'text-left': index===2}"
               v-html="replaceDynamicFields(block)">
          </div>
        </footer>

      </div>
    </div>
  </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const route = useRoute()
const router = useRouter()
const templateId = route.params.id
const loading = ref(true)
const template = ref<any>({})

// Sample Dummy Data for Preview
const dummyData = {
  '{{الرقم_العسكري}}': '12345678',
  '{{الاسم_الرباعي}}': 'أحمد محمد علي صالح',
  '{{الرتبة}}': 'مساعد أول',
  '{{الوحدة}}': 'الإدارة العامة لشؤون الأفراد',
  '{{تاريخ_اليوم}}': new Date().toLocaleDateString('ar-YE')
}

const replaceDynamicFields = (html: string) => {
  if (!html) return ''
  let processed = html
  for (const [key, value] of Object.entries(dummyData)) {
    processed = processed.replace(new RegExp(key, 'g'), value)
  }
  return processed
}

const loadTemplate = async () => {
  if (templateId === 'draft') {
    const draftStr = localStorage.getItem('report_template_draft')
    if (draftStr) {
      template.value = JSON.parse(draftStr)
    }
    loading.value = false
    return
  }

  try {
    const res = await api.get(`/reports/templates/${templateId}/`)
    template.value = res.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
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
  loadTemplate()
})
</script>

<style scoped>
.print-container {
  font-family: 'Arial', sans-serif;
}

.a4-page {
  width: 21cm;
  min-height: 29.7cm;
  background: white;
}

.a4-page.landscape {
  width: 29.7cm;
  min-height: 21cm;
}

/* CKEditor Content Styles specifically for Print/Preview */
.ck-content {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
}
.ck-content h1, .ck-content h2, .ck-content h3 {
  margin-bottom: 1rem;
  font-weight: bold;
}
.ck-content p {
  margin-bottom: 0.75rem;
}
.ck-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
.ck-content table td, .ck-content table th {
  border: 1px solid #000;
  padding: 8px;
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
  #print-area.landscape {
    width: 29.7cm;
    height: 21cm;
  }
  @page {
    size: A4 portrait;
    margin: 0;
  }
}
</style>
