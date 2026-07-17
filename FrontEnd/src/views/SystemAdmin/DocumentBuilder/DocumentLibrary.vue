<template>
  <AdminLayout>
    <div class="px-6 py-8" dir="rtl">
      <!-- Header -->
      <div class="mb-8 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-900/30 rounded-xl text-brand-600 dark:text-brand-400">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
            </div>
            مركز الوثائق والمراسلات (مكتبة القوالب)
          </h1>
          <p class="text-gray-500 dark:text-gray-400 mt-2 text-sm max-w-2xl">
            من هنا يمكنك إدارة جميع قوالب المذكرات الرسمية، ربطها بالكشوفات والطلبات، وطباعتها بضغطة زر واحدة وفقاً للمعايير الحكومية المعتمدة.
          </p>
        </div>
        <div class="flex gap-3">
          <button @click="showCreateModal = true" class="bg-brand-600 hover:bg-brand-700 text-white font-bold py-2.5 px-5 rounded-xl shadow-lg shadow-brand-500/30 transition-all flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            إنشاء قالب جديد
          </button>
        </div>
      </div>

      <!-- Templates Grid -->
      <div v-if="templates.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        
        <div v-for="(template, index) in templates" :key="index" class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-xl transition-all overflow-hidden flex flex-col group">
          <div class="p-5 flex-1 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-brand-100/50 to-transparent dark:from-brand-900/20 rounded-bl-full -mr-16 -mt-16 transition-transform group-hover:scale-110"></div>
            
            <div class="flex justify-between items-start mb-4 relative z-10">
              <div class="w-12 h-12 rounded-xl bg-brand-50 dark:bg-brand-900/30 text-brand-600 flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              </div>
              <span class="text-xs font-bold px-2.5 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                {{ template.fullTemplate?.documentType === 'PERSONNEL_MEMO' ? 'مذكرة أفراد' : 'مذكرة عامة' }}
              </span>
            </div>
            
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2 relative z-10 line-clamp-1" :title="template.name">
              {{ template.name }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 relative z-10">
              {{ template.fullTemplate?.subject || 'بدون موضوع' }}
            </p>
          </div>
          
          <div class="p-4 bg-gray-50 dark:bg-gray-800/80 border-t border-gray-100 dark:border-gray-700 grid grid-cols-2 gap-2">
            <button @click="editTemplate(template, index)" class="col-span-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-lg text-sm transition-colors flex items-center justify-center gap-1.5 shadow-sm">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
              استخدام وتعديل القالب
            </button>
            <button @click="deleteTemplate(index)" class="col-span-2 bg-white dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20 border border-gray-200 dark:border-gray-600 hover:border-red-200 dark:hover:border-red-800 text-red-600 dark:text-red-400 font-bold py-2 rounded-lg text-sm transition-colors flex items-center justify-center gap-1.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              حذف القالب
            </button>
          </div>
        </div>

      </div>

      <!-- Empty State -->
      <div v-else class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 border-dashed p-12 text-center">
        <div class="mx-auto w-24 h-24 bg-gray-50 dark:bg-gray-900/50 rounded-full flex items-center justify-center mb-4">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">المكتبة فارغة حالياً</h3>
        <p class="text-gray-500 dark:text-gray-400 max-w-md mx-auto mb-6">
          لم تقم بإنشاء أي قوالب مذكرات بعد. يمكنك إنشاء قالب جديد، تصميمه، وحفظه لاستخدامه لاحقاً مع الكشوفات المختلفة.
        </p>
        <button @click="showCreateModal = true" class="bg-brand-600 hover:bg-brand-700 text-white font-bold py-2.5 px-6 rounded-xl transition-all mx-auto block">
          البدء بإنشاء أول قالب
        </button>
      </div>

    </div>

    <!-- Create Document Type Selection Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4" dir="rtl">
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-3xl overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-brand-50 dark:bg-brand-900/20 flex justify-between items-center">
          <h3 class="text-xl font-bold text-brand-800 dark:text-brand-300 flex items-center gap-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            تحديد نوع الوثيقة
          </h3>
          <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-[70vh]">
          <p class="text-gray-600 dark:text-gray-400 mb-6 font-medium">اختر نوع المذكرة التي تود إنشاءها. سيتم تخصيص واجهة المُنشئ وإخفاء الحقول غير الضرورية بناءً على اختيارك.</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Normal Memo -->
            <button @click="createNewTemplate('MEMO')" class="flex items-start text-right gap-4 p-5 rounded-2xl border-2 border-transparent bg-gray-50 hover:bg-brand-50 hover:border-brand-200 transition-all dark:bg-gray-700/50 dark:hover:bg-brand-900/20 dark:hover:border-brand-800/50 group">
              <div class="w-12 h-12 shrink-0 rounded-xl bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-brand-600 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white text-lg mb-1">مذكرة عادية / تغطية</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">مثالية لخطابات التغطية، المراسلات بين الإدارات، والمذكرات العامة التي لا تتطلب كشوفات بأسماء الأفراد.</p>
              </div>
            </button>
            
            <!-- Circular -->
            <button @click="createNewTemplate('CIRCULAR')" class="flex items-start text-right gap-4 p-5 rounded-2xl border-2 border-transparent bg-gray-50 hover:bg-blue-50 hover:border-blue-200 transition-all dark:bg-gray-700/50 dark:hover:bg-blue-900/20 dark:hover:border-blue-800/50 group">
              <div class="w-12 h-12 shrink-0 rounded-xl bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-blue-600 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"></path></svg>
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white text-lg mb-1">تعميم</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">لإصدار تعاميم رسمية لعدة جهات معاً. يتميز بتنسيق الموضوع العريض وإلغاء بعض عناصر الخطابات الشخصية.</p>
              </div>
            </button>
            
            <!-- Attention Notice -->
            <button @click="createNewTemplate('ATTENTION_NOTICE')" class="flex items-start text-right gap-4 p-5 rounded-2xl border-2 border-transparent bg-gray-50 hover:bg-red-50 hover:border-red-200 transition-all dark:bg-gray-700/50 dark:hover:bg-red-900/20 dark:hover:border-red-800/50 group">
              <div class="w-12 h-12 shrink-0 rounded-xl bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-red-600 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white text-lg mb-1">لفت نظر / عقوبة</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">يظهر جدولاً مخصصاً للأفراد المعاقبين، مع مساحة للإيضاح وتنسيق خاص بالتوقيعات التأديبية.</p>
              </div>
            </button>
            
            <!-- Work Commencement -->
            <button @click="createNewTemplate('WORK_COMMENCEMENT')" class="flex items-start text-right gap-4 p-5 rounded-2xl border-2 border-transparent bg-gray-50 hover:bg-emerald-50 hover:border-emerald-200 transition-all dark:bg-gray-700/50 dark:hover:bg-emerald-900/20 dark:hover:border-emerald-800/50 group">
              <div class="w-12 h-12 shrink-0 rounded-xl bg-white dark:bg-gray-800 shadow-sm flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white text-lg mb-1">إثبات مباشرة عمل</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">يتضمن جدولاً لتحديد مكان ومحل الخدمة وتاريخ المباشرة لكل فرد.</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>



  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useCorrectionStore } from '@/stores/correction'
import { useDisciplinaryStore } from '@/stores/disciplinary'
import { useServicesStore } from '@/stores/services'
import { usePersonnelStore } from '@/stores/personnel'

const router = useRouter()
const correctionStore = useCorrectionStore()
const disciplinaryStore = useDisciplinaryStore()
const servicesStore = useServicesStore()
const personnelStore = usePersonnelStore()

// State
const templates = ref<any[]>([])
const showCreateModal = ref(false)


const availableForms = {
  'martyr': 'إثبات حالة (شهيد)',
  'death': 'إثبات حالة (وفاة)',
  'retirement_age': 'إثبات حالة (بلوغ السن القانوني)',
  'medical_unfit': 'إثبات حالة (عدم اللياقة الصحية)',
  'missing': 'إثبات حالة (مفقود)',
  'imprisoned': 'إثبات حالة (مسجون)',
  'seconded': 'إثبات حالة (منتدب)',
  'escort': 'إثبات حالة (مرافق)',
  'study_leave': 'إثبات حالة (مفرغ لدراسة)',
  'end_of_service': 'إثبات حالة (إنهاء مدة)',
  'retired': 'إثبات حالة (محال للتقاعد)'
}

onMounted(() => {
  loadTemplates()
})

function loadTemplates() {
  const defaultTemplates = [
      {
        name: 'مذكرة طلبات تصحيح بيانات معتمدة',
        fullTemplate: {
          documentType: 'PERSONNEL_MEMO',
          date: new Date().toISOString().split('T')[0],
          referenceNo: '',
          subject: 'تصحيح بيانات الأفراد العسكريين',
          addressees: [{ prefix: 'الأخ /', name: 'مدير إدارة نظم المعلومات', suffix: 'المحترم' }],
          body: '<p dir="rtl" style="text-align: justify; line-height: 1.8;">إشارة إلى الموضوع أعلاه، وبناءً على المراجعة والمطابقة الإدارية لبيانات الأفراد المدرجة أسماؤهم في الكشف أدناه.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;">نرجو التكرم بالاطلاع والتوجيه لجهات الاختصاص لديكم لإجراء عمليات التصحيح اللازمة في قاعدة البيانات الموحدة وفقاً لما هو موضح أمام كل اسم.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;"><strong>ولكم خالص التحية والتقدير،،،</strong></p>',
          signatures: [
            { title: 'مدير إدارة القوى البشرية', name: 'حسين عبده سعيد', rank: 'العقيد', showSeal: false },
            { title: 'مدير عام شرطة المحافظة', name: 'يحيى علي حُميد', rank: 'العميد', showSeal: true }
          ],
          attachments: 'أوليات التصحيح والمطابقة',
          involvedPersonnel: [],
          visibleColumns: { militaryId: true, rank: true, name: true, correctName: true, correctionTarget: true },
          typography: {
            addressee: { family: "'Cairo', sans-serif", size: 1.3, weight: 'font-bold', underline: false },
            greeting: { family: "'Cairo', sans-serif", size: 1.6, weight: 'font-bold', underline: false },
            subject: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: true },
            body: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            conclusionSeparator: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: false },
            conclusionBody: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            signatures: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', underline: false },
            signatureRank: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureName: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureTitle: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false }
          },
          signatureSettings: { showFrame: false, showLabels: true }
        }
      },
      {
        name: 'مذكرة لفت نظر (عقوبة إدارية)',
        fullTemplate: {
          documentType: 'ATTENTION_NOTICE',
          date: new Date().toISOString().split('T')[0],
          referenceNo: '',
          subject: 'لفت نظر بخصوص القصور الإداري',
          addressees: [{ prefix: 'الأخ /', name: 'مدير إدارة ........................', suffix: 'المحترم' }],
          body: '<p dir="rtl" style="text-align: justify; line-height: 1.8;">نلفت عنايتكم إلى أنه لوحظ في الآونة الأخيرة تكرار بعض التجاوزات الإدارية المتمثلة في التأخير عن رفع التمام اليومي، وعدم الالتزام بالضوابط والتعليمات الصادرة من القيادة.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;">وعليه، نوجه لكم هذا الإشعار كـ (لفت نظر)، ونأمل عدم تكرار مثل هذه التجاوزات، والتشديد على مرؤوسيكم بالانضباط التام.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;"><strong>ولكم خالص التحية والتقدير،،،</strong></p>',
          signatures: [
            { title: 'مدير عام شرطة المحافظة', name: 'يحيى علي حُميد', rank: 'العميد', showSeal: true }
          ],
          attachments: '',
          involvedPersonnel: [],
          visibleColumns: { militaryId: true, rank: true, name: true },
          typography: {
            addressee: { family: "'Cairo', sans-serif", size: 1.3, weight: 'font-bold', underline: false },
            greeting: { family: "'Cairo', sans-serif", size: 1.6, weight: 'font-bold', underline: false },
            subject: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: true },
            body: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            conclusionSeparator: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: false },
            conclusionBody: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            signatures: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', underline: false },
            signatureRank: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureName: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureTitle: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false }
          },
          signatureSettings: { showFrame: true, showLabels: true }
        }
      },
      {
        name: 'مذكرة إثبات مباشرة عمل',
        fullTemplate: {
          documentType: 'WORK_COMMENCEMENT',
          date: new Date().toISOString().split('T')[0],
          referenceNo: '',
          subject: 'مباشرة عمل',
          addressees: [{ prefix: 'الأخ /', name: 'مدير إدارة القوى البشرية', suffix: 'المحترم' }],
          body: '<p dir="rtl" style="text-align: justify; line-height: 1.8;">تحية طيبة وبعد،،</p><p dir="rtl" style="text-align: justify; line-height: 1.8;">نرفق لكم استمارة مباشرة العمل الخاصة بالضابط / الفرد المذكور أعلاه، والذي باشر عمله لدينا اعتباراً من تاريخ الاستمارة المرفقة.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;">يرجى التكرم بالاطلاع واعتماد المباشرة في النظام.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;"><strong>وتقبلوا خالص التحيات،،،</strong></p>',
          signatures: [
            { title: 'قائد الوحدة / الفرع', name: '', rank: '', showSeal: true }
          ],
          attachments: 'استمارة المباشرة',
          involvedPersonnel: [],
          visibleColumns: { militaryId: true, rank: true, name: true, workplace: true },
          typography: {
            addressee: { family: "'Cairo', sans-serif", size: 1.3, weight: 'font-bold', underline: false },
            greeting: { family: "'Cairo', sans-serif", size: 1.6, weight: 'font-bold', underline: false },
            subject: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: true },
            body: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            conclusionSeparator: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: false },
            conclusionBody: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            signatures: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', underline: false },
            signatureRank: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureName: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureTitle: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false }
          },
          signatureSettings: { showFrame: true, showLabels: true }
        }
      },
      {
        name: 'طلب إحالة للتقاعد',
        fullTemplate: {
          documentType: 'MEMO',
          date: new Date().toISOString().split('T')[0],
          referenceNo: '',
          subject: 'إحالة للتقاعد',
          addressees: [{ prefix: 'الأخ /', name: 'المدير العام للقوى البشرية', suffix: 'المحترم' }],
          body: '<p dir="rtl" style="text-align: justify; line-height: 1.8;">إشارة إلى الموضوع أعلاه، نرفق لكم استمارة طلب الإحالة للتقاعد الخاصة بالضابط / الفرد المذكور في الاستمارة المرفقة، وذلك لبلوغه الأجلين واستكمال الإجراءات القانونية اللازمة وفقاً لقانون هيئة الشرطة.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;">نرجو التكرم بالاطلاع والتوجيه.</p><p dir="rtl" style="text-align: justify; line-height: 1.8;"><strong>ولكم خالص التحية،،،</strong></p>',
          signatures: [
            { title: 'مدير إدارة القوى البشرية', name: 'حسين عبده سعيد', rank: 'العقيد', showSeal: false },
            { title: 'مدير عام شرطة المحافظة', name: 'يحيى علي حُميد', rank: 'العميد', showSeal: true }
          ],
          attachments: 'استمارة التقاعد + ملف الخدمة',
          involvedPersonnel: [],
          visibleColumns: {},
          typography: {
            addressee: { family: "'Cairo', sans-serif", size: 1.3, weight: 'font-bold', underline: false },
            greeting: { family: "'Cairo', sans-serif", size: 1.6, weight: 'font-bold', underline: false },
            subject: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: true },
            body: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            conclusionSeparator: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: false },
            conclusionBody: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
            signatures: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', underline: false },
            signatureRank: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureName: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
            signatureTitle: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false }
          },
          signatureSettings: { showFrame: false, showLabels: true }
        }
      }
  ]

  let currentTemplates = JSON.parse(localStorage.getItem('memoTypographyPresets') || '[]')
  
  let hasChanges = false
  defaultTemplates.forEach(dt => {
    const existingIndex = currentTemplates.findIndex((ct: any) => ct.name === dt.name)
    if (existingIndex === -1) {
      currentTemplates.push(dt)
      hasChanges = true
    } else {
      // Force update existing default templates to fix old structure bugs!
      // ONLY update them if their structure is old (using 'to' instead of 'addressees')
      if (currentTemplates[existingIndex].fullTemplate?.to) {
        currentTemplates[existingIndex] = dt
        hasChanges = true
      }
    }
  })

  if (hasChanges || currentTemplates.length === 0) {
    localStorage.setItem('memoTypographyPresets', JSON.stringify(currentTemplates))
  }
  
  templates.value = currentTemplates
}

function createNewTemplate(type: string) {
  localStorage.removeItem('official_memo_draft') // Clear draft to start fresh
  showCreateModal.value = false
  router.push(`/admin/documents/memo-builder?type=${type}`)
}

function editTemplate(template: any, index: number) {
  let draftForm = template.fullTemplate || {}
  
  // Backwards compatibility with old typography-only templates
  if (!template.fullTemplate && template.typography) {
    draftForm = { typography: template.typography }
  }

  localStorage.setItem('official_memo_draft', JSON.stringify(draftForm))
  localStorage.setItem('official_memo_edit_index', index.toString())
  router.push('/admin/documents/memo-builder')
}

function deleteTemplate(index: number) {
  if (confirm('هل أنت متأكد من حذف هذا القالب؟ لا يمكن التراجع عن هذا الإجراء.')) {
    templates.value.splice(index, 1)
    localStorage.setItem('memoTypographyPresets', JSON.stringify(templates.value))
  }
}

</script>
