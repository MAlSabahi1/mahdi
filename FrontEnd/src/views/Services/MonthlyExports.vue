<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تصدير الخدمات الشهرية لوزارة الداخلية والمالية" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          تصدير الخدمات الشهرية للوزارة (Ministry Reports Exporter)
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          بوابة إعداد وتوليد وتصدير الكشوفات الشهرية الموحدة لرواتب وأوضاع الأفراد والضباط طبقاً للنماذج الرسمية المعتمدة لدى الوزارة.
        </p>
      </div>

      <!-- Export Profiles Grid -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div v-for="profile in exportProfiles" :key="profile.id" class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs flex flex-col justify-between">
          <div class="space-y-2">
            <span class="p-2.5 rounded-lg bg-brand-50 text-brand-650 dark:bg-brand-950/40 dark:text-brand-400 inline-block">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </span>
            <h3 class="text-xs font-black text-gray-950 dark:text-white">{{ profile.title }}</h3>
            <p class="text-[10px] text-gray-400 leading-relaxed">{{ profile.desc }}</p>
          </div>
          
          <div class="border-t border-gray-150 dark:border-gray-850 pt-4 mt-4 flex items-center justify-between gap-2">
            <span class="text-[9px] font-mono text-gray-400 bg-gray-50 dark:bg-gray-900 px-2 py-0.5 rounded border border-gray-150 dark:border-gray-800">
              {{ profile.code }}
            </span>
            <button 
              @click="generateExportFile(profile)"
              class="bg-brand-600 hover:bg-brand-700 text-white text-[10px] font-bold px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
            >
              توليد وتصدير الكشف
            </button>
          </div>
        </div>
      </div>

      <!-- Export Logs / History Table -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="p-5 border-b border-gray-200 dark:border-gray-800">
          <h3 class="text-sm font-black text-gray-900 dark:text-white">سجل التصدير وعمليات التوليد التاريخية</h3>
          <p class="text-[10px] text-gray-400 mt-1">تتبع كافة ملفات كشوفات الوزارة الصادرة مسبقاً وتواريخ سحبها ومطابقتها.</p>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-450 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-5 py-3">اسم الكشف الصادر</th>
                <th class="px-5 py-3">المعرف الكودي</th>
                <th class="px-5 py-3">تاريخ التصدير</th>
                <th class="px-5 py-3">اسم الفاعل / المسؤول</th>
                <th class="px-5 py-3">نوع التصدير</th>
                <th class="px-5 py-3">التحميل</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr>
                <td colspan="6" class="px-5 py-8 text-center text-gray-400 dark:text-gray-500">
                  لم يتم إجراء عمليات تصدير شهرية معتمدة للوزارة خلال هذا الشهر المالي حتى الآن.
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
}

const exportProfiles = ref<ExportProfile[]>([
  {
    id: 1,
    title: 'كشف خلاصة الرواتب والتسويات العسكرية',
    desc: 'يتضمن كشوفات الموظفين والضباط المحدثة وفق آخر رتب وتسويات عسكرية معتمدة للشهر الجاري.',
    code: 'MINISTRY_MILITARY_PAYROLL'
  },
  {
    id: 2,
    title: 'سجل المتغيرات الشهرية للوزارة',
    desc: 'تقرير مقارنة شهري يبرز الفروق والزيادات والخصومات الحاصلة عن الشهر السابق لتبرير التعديلات.',
    code: 'MINISTRY_MONTHLY_CHANGES'
  },
  {
    id: 3,
    title: 'سجل الامتثال والالتزام للمديريات',
    desc: 'خلاصة إحصائية توضح نسب التزام فروع المحافظات بتسليم كشوفاتها والملفات المرفوضة فيها.',
    code: 'MINISTRY_COMPLIANCE_STATS'
  }
])

function generateExportFile(profile: ExportProfile) {
  Swal.fire({
    title: 'تأكيد توليد الكشف',
    text: `هل أنت متأكد من رغبتك في توليد وتصدير ملف "${profile.title}"؟ قد تستغرق المعالجة بضع ثوانٍ.`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'توليد وتصدير',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#2563eb'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: 'جاري توليد الكشف...',
        html: 'يجري جمع البيانات وتجميع الاستحقاقات...',
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading()
          setTimeout(() => {
            Swal.fire({
              toast: true,
              position: 'top-end',
              icon: 'success',
              title: 'تم تصدير الكشف بنجاح',
              showConfirmButton: false,
              timer: 3000
            })
          }, 1500)
        }
      })
    }
  })
}
</script>
