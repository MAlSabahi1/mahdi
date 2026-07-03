<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="مجمع الاعتماد الثنائي" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 border-b border-gray-200 dark:border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            مجمع الاعتماد الثنائي (Dual Authorization Hub)
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            نظام التحقق المزدوج (Maker-Checker) لاعتماد العمليات الحساسة وتفادي انفراد شخص واحد بالقرارات الأمنية والمالية.
          </p>
        </div>
      </div>

      <!-- Quick Metrics -->
      <div class="grid gap-5 grid-cols-1 sm:grid-cols-3">
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
          <div class="text-gray-400 dark:text-gray-500 text-[10px] font-bold uppercase">الطلبات المعلقة الحالية</div>
          <div class="text-2xl font-black text-gray-900 dark:text-white mt-1">{{ pendingRequests.length }} طلبات</div>
          <div class="text-[10px] text-gray-400 dark:text-gray-500 mt-1">لا توجد طلبات معلقة</div>
        </div>
        
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
          <div class="text-gray-400 dark:text-gray-500 text-[10px] font-bold uppercase">متوسط زمن الاعتماد</div>
          <div class="text-2xl font-black text-gray-900 dark:text-white mt-1">0 دقيقة</div>
          <div class="text-[10px] text-gray-400 dark:text-gray-500 mt-1">خلال آخر 24 ساعة</div>
        </div>

        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
          <div class="text-gray-400 dark:text-gray-500 text-[10px] font-bold uppercase">نسبة الرفض والاعتراض</div>
          <div class="text-2xl font-black text-gray-900 dark:text-white mt-1">0%</div>
          <div class="text-[10px] text-gray-400 dark:text-gray-500 mt-1">لا توجد عمليات نشطة</div>
        </div>
      </div>

      <!-- Pending Approval Queue -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="p-5 border-b border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h3 class="text-sm font-black text-gray-900 dark:text-white">قائمة عمليات التحقق الثنائي النشطة</h3>
            <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-1">
              العمليات الأمنية الحساسة التي أطلقت بواسطة مشرف وبانتظار موافقة مشرف آخر لإكمالها.
            </p>
          </div>
          
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500">حالة التصفية:</span>
            <select class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg px-3 py-1.5 bg-white dark:bg-gray-950 text-gray-700 dark:text-gray-300">
              <option>عرض الكل (المعلقة)</option>
              <option>عمليات حذف الحسابات</option>
              <option>عمليات تعديل الحقول المالية</option>
            </select>
          </div>
        </div>

        <div class="divide-y divide-gray-150 dark:divide-gray-850">
          <div v-if="pendingRequests.length === 0" class="p-8 text-center text-gray-400 dark:text-gray-500 text-xs">
            لا توجد طلبات معلقة بانتظار الاعتماد المزدوج حالياً في النظام.
          </div>
          <div v-else v-for="req in pendingRequests" :key="req.id" class="p-5 hover:bg-gray-50/40 dark:hover:bg-gray-800/10 transition-colors">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
              
              <!-- Left Detail Info -->
              <div class="flex items-start gap-4">
                <span :class="[
                  'p-2.5 rounded-xl shrink-0 mt-0.5',
                  req.level === 'high' 
                    ? 'bg-red-50 text-red-650 dark:bg-red-950/20 dark:text-red-400' 
                    : 'bg-orange-50 text-orange-600 dark:bg-orange-950/20 dark:text-orange-400'
                ]">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0110 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.746 3.746 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0114 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
                  </svg>
                </span>
                
                <div class="space-y-1">
                  <div class="flex items-center flex-wrap gap-2">
                    <h4 class="text-xs font-black text-gray-900 dark:text-white">{{ req.action }}</h4>
                    <span :class="[
                      'px-2 py-0.5 rounded text-[10px] font-bold',
                      req.level === 'high' 
                        ? 'bg-red-50 text-red-700 dark:bg-red-950/20 dark:text-red-400 border border-red-200 dark:border-red-900/30' 
                        : 'bg-orange-50 text-orange-700 dark:bg-orange-950/20 dark:text-orange-400 border border-orange-200 dark:border-orange-900/30'
                    ]">
                      {{ req.level === 'high' ? 'حساسية مرتفعة جداً' : 'حساسية متوسطة' }}
                    </span>
                  </div>
                  <p class="text-[11px] text-gray-600 dark:text-gray-300">
                    الهدف: <span class="font-mono font-bold text-gray-800 dark:text-gray-200">{{ req.target }}</span>
                  </p>
                  <p class="text-[10px] text-gray-400 dark:text-gray-500">
                    مقدم الطلب: <span class="font-bold text-gray-650">{{ req.initiator }}</span> | تاريخ الطلب: <span class="font-mono">{{ req.date }}</span>
                  </p>
                  <p class="text-[10px] text-gray-500 dark:text-gray-400 italic bg-gray-50 dark:bg-gray-950/30 p-2 rounded-lg mt-2">
                    السبب: {{ req.reason }}
                  </p>
                </div>
              </div>

              <!-- Right Action Buttons -->
              <div class="flex items-center gap-2 self-end md:self-center">
                <button class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3.5 py-2 rounded-xl cursor-pointer">
                  اعتماد العملية
                </button>
                <button class="border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900 text-red-650 text-xs font-bold px-3.5 py-2 rounded-xl cursor-pointer">
                  رفض الطلب
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>

      <!-- Authorization Rule Engine -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs">
        <h3 class="text-sm font-black text-gray-900 dark:text-white mb-1">السياسات الأمنية المفعلة للاعتماد الثنائي</h3>
        <p class="text-[11px] text-gray-400 dark:text-gray-500 mb-5">
          العمليات الإدارية التي تتطلب موافقة من مستخدمين اثنين بشكل قسري ولا يمكن تجاوزها.
        </p>

        <div class="space-y-3">
          <div class="flex justify-between items-center p-3 rounded-xl bg-gray-50 dark:bg-gray-950/20 border border-gray-150 dark:border-gray-850 text-xs">
            <span class="font-bold text-gray-800 dark:text-gray-200">حذف أو تعطيل حسابات الضباط برتبة عقيد وما فوق</span>
            <span class="text-[10px] font-bold text-emerald-650 dark:text-emerald-450 bg-emerald-50 dark:bg-emerald-950/20 px-2.5 py-1 rounded-full">مفعلة وتتطلب رتبة عميد كمعتمد ثانٍ</span>
          </div>

          <div class="flex justify-between items-center p-3 rounded-xl bg-gray-50 dark:bg-gray-950/20 border border-gray-150 dark:border-gray-850 text-xs">
            <span class="font-bold text-gray-800 dark:text-gray-200">تعديل الأرقام المالية وبيانات الاستحقاق للرواتب يدوياً</span>
            <span class="text-[10px] font-bold text-emerald-650 dark:text-emerald-450 bg-emerald-50 dark:bg-emerald-950/20 px-2.5 py-1 rounded-full">مفعلة وتتطلب موافقة المفتش المالي</span>
          </div>

          <div class="flex justify-between items-center p-3 rounded-xl bg-gray-50 dark:bg-gray-950/20 border border-gray-150 dark:border-gray-850 text-xs">
            <span class="font-bold text-gray-800 dark:text-gray-200">تعديل إعدادات وسياسات الـ ABAC العامة</span>
            <span class="text-[10px] font-bold text-emerald-650 dark:text-emerald-450 bg-emerald-50 dark:bg-emerald-950/20 px-2.5 py-1 rounded-full">مفعلة وتتطلب موافقة مدير أمن النظام</span>
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

interface RequestRecord {
  id: number
  action: string
  target: string
  initiator: string
  date: string
  level: string
  reason: string
}

const pendingRequests = ref<RequestRecord[]>([])
</script>
