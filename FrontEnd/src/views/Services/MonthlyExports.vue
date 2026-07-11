<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تصدير التقارير الشهرية الموحدة" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            تصدير التقارير الشهرية الموحدة للوزارة
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            بوابة إعداد وتوليد وتصدير الكشوفات الشهرية الموحدة لرواتب ومستحقات منتسبي القوة طبقاً للنماذج الرسمية المعتمدة لدى الوزارة.
          </p>
        </div>

        <!-- Live Counters -->
        <div class="flex gap-5 flex-shrink-0">
          <div class="rounded-2xl border border-blue-200 bg-blue-50 p-4 shadow-theme-xs dark:border-blue-500/20 dark:bg-blue-500/5 text-center min-w-[120px]">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              </div>
              <div class="text-start">
                <p class="text-xs font-medium text-blue-700 dark:text-blue-400">نماذج متاحة</p>
                <h3 class="text-xl font-bold text-blue-900 dark:text-blue-300">{{ exportProfiles.length }}</h3>
              </div>
            </div>
          </div>
          <div class="rounded-2xl border border-success-200 bg-success-50 p-4 shadow-theme-xs dark:border-success-500/20 dark:bg-success-500/5 text-center min-w-[120px]">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
              </div>
              <div class="text-start">
                <p class="text-xs font-medium text-success-700 dark:text-success-400">تم تصديرها</p>
                <h3 class="text-xl font-bold text-success-900 dark:text-success-300">{{ mockHistory.length }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Profiles Grid -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div 
          v-for="(profile, index) in exportProfiles" 
          :key="profile.id" 
          class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col group transition-all hover:shadow-theme-sm"
        >
          <!-- Card Header -->
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex items-center gap-4">
            <div 
              class="flex h-12 w-12 items-center justify-center rounded-xl border group-hover:scale-110 transition-transform duration-300"
              :class="[
                profile.color === 'indigo' ? 'bg-indigo-50 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400 border-indigo-100 dark:border-indigo-500/30' : '',
                profile.color === 'amber' ? 'bg-amber-50 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400 border-amber-100 dark:border-amber-500/30' : '',
                profile.color === 'emerald' ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400 border-emerald-100 dark:border-emerald-500/30' : ''
              ]"
            >
              <!-- Step Number Badge -->
              <span class="text-lg font-black">{{ index + 1 }}</span>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-bold text-gray-900 dark:text-white leading-snug">{{ profile.title }}</h3>
              <p class="text-[10px] font-medium text-gray-500 dark:text-gray-400 mt-0.5">{{ profile.code }}</p>
            </div>
          </div>

          <!-- Card Body -->
          <div class="p-5 flex-1 flex flex-col">
            <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed flex-1">
              {{ profile.desc }}
            </p>

            <!-- Card Footer -->
            <div class="border-t border-gray-100 dark:border-gray-800 pt-4 mt-5 flex items-center justify-between gap-3">
              <div class="flex items-center gap-2">
                <div class="flex h-7 w-7 items-center justify-center rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <span class="block text-[9px] text-gray-400 dark:text-gray-500 font-bold uppercase">الجهة المستلمة</span>
                  <span class="text-[10px] font-bold text-gray-700 dark:text-gray-300">{{ profile.recipient }}</span>
                </div>
              </div>
              <BaseButton 
                @click="generateExportFile(profile)"
                variant="primary"
                size="sm"
                customClass="rounded-xl font-bold text-xs"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                توليد وتصدير
              </BaseButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Logs / History Table Card -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <!-- Card Header -->
        <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex items-center justify-between gap-4">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-warning-50 text-warning-600 dark:bg-warning-500/20 dark:text-warning-400 border border-warning-100 dark:border-warning-500/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-gray-900 dark:text-white">سجل التصدير وعمليات التوليد التاريخية</h3>
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mt-0.5">تتبع كافة ملفات كشوفات الوزارة الصادرة مسبقاً وتواريخ سحبها ومطابقتها.</p>
            </div>
          </div>
          <span class="flex items-center gap-1.5 text-xs font-bold text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-gray-800 px-3 py-1.5 rounded-lg flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            {{ mockHistory.length }} سجل
          </span>
        </div>
        
        <!-- Table Content -->
        <div class="p-5">
          <div class="overflow-x-auto">
            <table v-if="mockHistory.length > 0" class="w-full text-right border-collapse min-w-[900px]">
              <thead>
                <tr class="border-b border-gray-100 dark:border-gray-800">
                  <th class="p-3 text-start text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">اسم الكشف الصادر</th>
                  <th class="p-3 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">المعرف الكودي</th>
                  <th class="p-3 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">تاريخ ووقت التصدير</th>
                  <th class="p-3 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">مسؤول التصدير</th>
                  <th class="p-3 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">الجهة المستلمة</th>
                  <th class="p-3 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">حالة الملف</th>
                  <th class="p-3 text-left text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">تحميل المستند</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                <tr 
                  v-for="log in mockHistory" 
                  :key="log.id" 
                  class="text-xs hover:bg-gray-50/60 dark:hover:bg-gray-800/30 transition-colors"
                >
                  <td class="p-3 font-bold text-gray-900 dark:text-white">
                    <div class="flex items-center gap-2">
                      <div class="flex h-7 w-7 items-center justify-center rounded-lg bg-brand-50 text-brand-500 dark:bg-brand-500/10 dark:text-brand-400 flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      {{ log.title }}
                    </div>
                  </td>
                  <td class="p-3">
                    <span class="font-mono text-[10px] bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-md border border-gray-200/40 dark:border-gray-700 text-gray-600 dark:text-gray-400">
                      {{ log.code }}
                    </span>
                  </td>
                  <td class="p-3 font-mono text-[11px] text-gray-500 dark:text-gray-400">
                    {{ log.timestamp }}
                  </td>
                  <td class="p-3 font-semibold text-gray-800 dark:text-gray-200">
                    {{ log.user }}
                  </td>
                  <td class="p-3 text-gray-600 dark:text-gray-300">
                    {{ log.recipient }}
                  </td>
                  <td class="p-3">
                    <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full font-bold text-[10px] border bg-success-50 text-success-700 border-success-200 dark:bg-success-500/10 dark:text-success-400 dark:border-success-500/20">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                      مكتمل وموقّع
                    </span>
                  </td>
                  <td class="p-3 text-left">
                    <button 
                      @click="downloadReport(log.title)"
                      class="inline-flex items-center gap-1.5 text-[10px] font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 dark:bg-brand-500/10 dark:hover:bg-brand-500/20 border border-brand-200/30 dark:border-brand-500/20 px-3 py-1.5 rounded-lg transition-all cursor-pointer"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      تنزيل الملف
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty State -->
            <div v-else class="flex flex-col items-center justify-center py-16 text-center">
              <div class="flex h-16 w-16 items-center justify-center rounded-2xl bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h4 class="text-sm font-bold text-gray-500 dark:text-gray-400">لا توجد عمليات تصدير سابقة</h4>
              <p class="text-xs text-gray-400 dark:text-gray-500 mt-1.5 max-w-xs">
                ابدأ بتصدير أول تقرير شهري من البطاقات أعلاه وسيظهر هنا في السجل التاريخي.
              </p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import BaseButton from '@/components/common/BaseButton.vue'
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
