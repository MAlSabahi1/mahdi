<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تصدير التقارير الشهرية الموحدة للوزارة" />

    <div class="space-y-6 text-start animate-fade-in" dir="rtl">
      
      <!-- Premium Page Header Card -->
      <div class="relative overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-sm">
        <div class="absolute -right-16 -top-16 w-48 h-48 bg-brand-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-brand-500/10 text-brand-650 dark:text-brand-400 rounded-2xl shadow-theme-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">
                تصدير التقارير الشهرية الموحدة للوزارة (Ministry Reports Exporter)
              </h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                بوابة إعداد وتوليد وتصدير الكشوفات الشهرية الموحدة لرواتب ومستحقات منتسبي القوة طبقاً للنماذج الرسمية المعتمدة لدى الوزارة.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Profiles Grid -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div 
          v-for="profile in exportProfiles" 
          :key="profile.id" 
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-brand-500/30 transition-all duration-300 flex flex-col justify-between group"
        >
          <div class="space-y-4">
            <!-- Icon Wrapper styled per profile theme color -->
            <div 
              class="w-11 h-11 rounded-xl flex items-center justify-center transition-transform group-hover:scale-105 duration-300"
              :class="[
                profile.color === 'indigo' ? 'bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400' : '',
                profile.color === 'amber' ? 'bg-amber-50 text-amber-600 dark:bg-amber-950/40 dark:text-amber-400' : '',
                profile.color === 'emerald' ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/40 dark:text-emerald-400' : ''
              ]"
            >
              <!-- Dynamic Icon SVGs -->
              <svg v-if="profile.icon === 'payroll'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <svg v-else-if="profile.icon === 'changes'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm-5-9V7a2 2 0 012-2h2a2 2 0 012 2v2m-6 0h6" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white">{{ profile.title }}</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 leading-relaxed h-12 overflow-hidden">
                {{ profile.desc }}
              </p>
            </div>
          </div>
          
          <div class="border-t border-gray-150 dark:border-gray-800 pt-4 mt-5 flex items-center justify-between gap-2">
            <div>
              <span class="block text-[9px] text-gray-400 dark:text-gray-500 font-bold uppercase">الجهة المستلمة</span>
              <span class="text-[10px] font-bold text-gray-700 dark:text-gray-300">{{ profile.recipient }}</span>
            </div>
            <button 
              @click="generateExportFile(profile)"
              class="bg-brand-500 hover:bg-brand-600 text-white text-xs font-black px-4 py-2 rounded-xl transition-colors cursor-pointer shadow-theme-xs"
            >
              توليد وتصدير الكشف
            </button>
          </div>
        </div>
      </div>

      <!-- Export Logs / History Table -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-sm space-y-4 p-5">
        <div class="flex items-center justify-between border-b border-gray-150 dark:border-gray-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="p-1.5 rounded-lg bg-brand-500/10 text-brand-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </span>
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white">سجل التصدير وعمليات التوليد التاريخية</h3>
              <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">تتبع كافة ملفات كشوفات الوزارة الصادرة مسبقاً وتواريخ سحبها ومطابقتها.</p>
            </div>
          </div>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse min-w-[900px]">
            <thead>
              <tr class="border-b border-gray-100 dark:border-gray-800 text-xs font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-900/50">
                <th class="p-3 text-start">اسم الكشف الصادر</th>
                <th class="p-3">المعرف الكودي</th>
                <th class="p-3">تاريخ ووقت التصدير</th>
                <th class="p-3">مسؤول التصدير الفاعل</th>
                <th class="p-3">الجهة المستلمة</th>
                <th class="p-3">حالة الملف</th>
                <th class="p-3 text-left">تحميل المستند</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-850">
              <tr 
                v-for="log in mockHistory" 
                :key="log.id" 
                class="text-xs hover:bg-gray-50/40 dark:hover:bg-gray-850/20 transition-colors"
              >
                <td class="p-3 font-extrabold text-gray-900 dark:text-white">
                  {{ log.title }}
                </td>
                <td class="p-3">
                  <span class="font-mono text-[10px] bg-gray-100 dark:bg-gray-950 px-2 py-0.5 rounded border border-gray-200/40 dark:border-gray-800 text-gray-600 dark:text-gray-400">
                    {{ log.code }}
                  </span>
                </td>
                <td class="p-3 font-mono text-[11px] text-gray-500">
                  {{ log.timestamp }}
                </td>
                <td class="p-3 font-semibold text-gray-800 dark:text-gray-200">
                  {{ log.user }}
                </td>
                <td class="p-3 text-gray-650 dark:text-gray-300">
                  {{ log.recipient }}
                </td>
                <td class="p-3">
                  <span class="px-2 py-0.5 rounded-full font-bold text-[9px] border bg-success-50 text-success-700 border-success-200 dark:bg-success-950/20 dark:text-success-400">
                    مكتمل وموقّع
                  </span>
                </td>
                <td class="p-3 text-left">
                  <button 
                    @click="downloadReport(log.title)"
                    class="text-[9.5px] font-black text-brand-600 bg-brand-50 hover:bg-brand-100 dark:bg-brand-950/20 dark:hover:bg-brand-950/40 border border-brand-200/30 px-3 py-1.5 rounded-lg transition-all cursor-pointer"
                  >
                    تنزيل الملف
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'

interface ExportProfile {
  id: number
  title: string
  desc: string
  code: string
  icon: string
  color: string
  recipient: string
}

interface ExportHistoryLog {
  id: number
  title: string
  code: string
  timestamp: string
  user: string
  recipient: string
}

const exportProfiles = ref<ExportProfile[]>([
  {
    id: 1,
    title: 'كشف القوة الموحد الموزع على الحالات (Excel بأربع ورقات)',
    desc: 'توليد ملف كشف القوة الموحد بضغطة زر واحدة موزعاً تلقائياً على 4 ورقات (عاملة، غير عاملة، كاملة، غياب) وفقاً للحالات المسجلة.',
    code: 'OFFICIAL_UNIFIED_STRENGTH_SHEET',
    icon: 'payroll',
    color: 'indigo',
    recipient: 'الوزارة'
  },
  {
    id: 2,
    title: 'كشف الخلاصة العددية للقوة غير العاملة (نموذج رقم 3)',
    desc: 'توليد الخلاصة الشهرية العددية آلياً بجمع إحصائيات السجناء والمجازين والمنقطعين من الواقع الميداني وتصديرها.',
    code: 'NUMERICAL_SUMMARY_FORM_3',
    icon: 'changes',
    color: 'amber',
    recipient: 'الوزارة'
  },
  {
    id: 3,
    title: 'مذكرة التغطية الرسمية المرفقة بالكشوفات',
    desc: 'إصدار مذكرة التغطية الرسمية الصادرة من المديرية/القطاع بترويسة ونموذج معتمد لتغطية إرسال البيانات المعتمدة.',
    code: 'OFFICIAL_COVERING_MEMO',
    icon: 'compliance',
    color: 'emerald',
    recipient: 'قيادة الوزارة'
  }
])

const mockHistory = ref<ExportHistoryLog[]>([
  {
    id: 1,
    title: 'كشف القوة الموحد لشهر يونيو 2026',
    code: 'OFFICIAL_UNIFIED_STRENGTH_SHEET',
    timestamp: '2026-07-02 09:30 ص',
    user: 'العميد أمين (أدمن)',
    recipient: 'الوزارة'
  },
  {
    id: 2,
    title: 'كشف الخلاصة العددية للقوة غير العاملة (نموذج 3) لشهر يونيو 2026',
    code: 'NUMERICAL_SUMMARY_FORM_3',
    timestamp: '2026-07-01 11:15 ص',
    user: 'العقيد طارق (مسؤول مالي)',
    recipient: 'الوزارة'
  }
])

function generateExportFile(profile: ExportProfile) {
  Swal.fire({
    title: 'تأكيد توليد الكشف الموحد',
    text: `هل أنت متأكد من رغبتك في توليد وتصدير ملف "${profile.title}" للوزارة؟ قد تستغرق المعالجة بضع ثوانٍ.`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'توليد وتصدير',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#465fff',
    cancelButtonColor: '#6b7280'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: 'جاري توليد الكشف الموحد...',
        html: 'يجري جمع البيانات وتجميع الاستحقاقات بصيغة رسمية معتمدة...',
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading()
          setTimeout(() => {
            Swal.fire({
              toast: true,
              position: 'top-end',
              icon: 'success',
              title: 'تم تصدير وتوقيع الكشف الموحد بنجاح',
              showConfirmButton: false,
              timer: 3000
            })
            
            // Add a new item to history
            const newLog: ExportHistoryLog = {
              id: Date.now(),
              title: `${profile.title} - ${new Date().toLocaleDateString('ar-YE')}`,
              code: profile.code,
              timestamp: new Date().toLocaleString('ar-YE', {
                hour: '2-digit',
                minute: '2-digit',
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
              }),
              user: 'العميد أمين (أدمن)',
              recipient: profile.recipient
            }
            mockHistory.value.unshift(newLog)
          }, 1500)
        }
      })
    }
  })
}

function downloadReport(title: string) {
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: `بدأ تحميل كشف: ${title}`,
    showConfirmButton: false,
    timer: 2000
  })
}
</script>
