<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="مصفوفة صلاحيات الحقول والسياسات" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 border-b border-gray-200 dark:border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            مصفوفة صلاحيات الحقول والسياسات (ABAC)
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            تهيئة وتصميم سياسات التحكم بالوصول المستند إلى السمات وصلاحيات القراءة/الكتابة على مستوى الحقول.
          </p>
        </div>
      </div>

      <!-- ABAC Context Info -->
      <div class="grid gap-6 md:grid-cols-3">
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
          <div class="flex items-center gap-3 mb-3">
            <span class="p-1.5 rounded-lg bg-blue-50 text-blue-600 dark:bg-blue-950/30 dark:text-blue-450">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
            </span>
            <h3 class="text-xs font-black text-gray-900 dark:text-white">سمات المستخدم (Subject)</h3>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed">
            التحقق من الرتبة العسكرية، الإدارة الفرعية، المحافظة الجغرافية، والمنصب الوظيفي الحالي للمستخدم عند فحص الصلاحية.
          </p>
        </div>

        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
          <div class="flex items-center gap-3 mb-3">
            <span class="p-1.5 rounded-lg bg-purple-50 text-purple-650 dark:bg-purple-950/30 dark:text-purple-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 .621-.504 1.125-1.125 1.125H4.875A1.125 1.125 0 013.75 18.65v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.453.25-.718.25H4.875a1.125 1.125 0 01-.718-.25m16.5 0a1.5 1.5 0 01-1.5 1.5H4.875a1.5 1.5 0 01-1.5-1.5m16.5 0v-4.5m-16.5 4.5a2.18 2.18 0 01-.75-1.661V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m-7.5 8.006V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m0 0V6c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m0 0V8.706" />
              </svg>
            </span>
            <h3 class="text-xs font-black text-gray-900 dark:text-white">سمات البيانات (Resource)</h3>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed">
            تحديد حقول البيانات الحساسة مثل (الرقم المالي، معلومات الاتصال، الرتبة المقترحة) وتطبيق قيود الوصول الخاصة بها.
          </p>
        </div>

        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs">
          <div class="flex items-center gap-3 mb-3">
            <span class="p-1.5 rounded-lg bg-orange-50 text-orange-600 dark:bg-orange-950/30 dark:text-orange-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v10.5m0 0L7.5 9m4.5 4.5L16.5 9m-9 7.5h9" />
              </svg>
            </span>
            <h3 class="text-xs font-black text-gray-900 dark:text-white">بيئة الطلب (Environment)</h3>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed">
            قييد فترات الوصول بـ (أوقات الدوام الرسمي، الدخول من نطاق الشبكة العسكرية الداخلية IP، أو المواقع المعتمدة فقط).
          </p>
        </div>
      </div>

      <!-- Field-level Permissions Matrix -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="p-5 border-b border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h3 class="text-sm font-black text-gray-900 dark:text-white">مصفوفة صلاحيات الحقول لبيانات الأفراد</h3>
            <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-1">
              تحديد الحقول التي يمكن قراءتها وتعديلها لكل دور من الأدوار الأمنية في النظام.
            </p>
          </div>
          
          <div class="flex items-center gap-2">
            <select class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg px-3 py-1.5 bg-white dark:bg-gray-950 text-gray-700 dark:text-gray-300">
              <option>جدول الأفراد والضباط</option>
              <option>جدول الكشوفات والاستحقاق</option>
              <option>سجل السكرتارية والمستندات</option>
            </select>
            <button class="bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold px-3.5 py-1.5 rounded-lg cursor-pointer">
              حفظ المصفوفة
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-5 py-3 text-start">حقل البيانات</th>
                <th class="px-5 py-3 text-center">مدير النظام (Admin)</th>
                <th class="px-5 py-3 text-center">ضابط شؤون الأفراد</th>
                <th class="px-5 py-3 text-center">أمين سر السكرتارية</th>
                <th class="px-5 py-3 text-center">المدقق المالي والمفتش</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr v-for="field in fields" :key="field.key" class="hover:bg-gray-50/40 dark:hover:bg-gray-800/10">
                <td class="px-5 py-3.5">
                  <div class="font-extrabold text-gray-900 dark:text-white">{{ field.label }}</div>
                  <div class="text-[10px] text-gray-400 font-mono mt-0.5">{{ field.key }}</div>
                </td>
                
                <td v-for="role in roles" :key="role" class="px-5 py-3.5 text-center">
                  <div class="inline-flex items-center gap-3">
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input type="checkbox" checked class="rounded border-gray-300 text-brand-600 focus:ring-brand-500 h-3.5 w-3.5" />
                      <span class="text-[10px] text-gray-500">قراءة</span>
                    </label>
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input type="checkbox" :checked="field.writeRoles.includes(role)" class="rounded border-gray-300 text-brand-600 focus:ring-brand-500 h-3.5 w-3.5" />
                      <span class="text-[10px] text-gray-500">كتابة</span>
                    </label>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Policy Editor / ABAC Rule Builder -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs">
        <h3 class="text-sm font-black text-gray-900 dark:text-white mb-1">مصمم قواعد الـ ABAC الذكية</h3>
        <p class="text-[11px] text-gray-400 dark:text-gray-500 mb-5">
          صياغة قواعد وصول شرطية ديناميكية استناداً للمطابقة الجغرافية أو الرتب والمنصب العسكري الفعلي.
        </p>

        <div class="space-y-4">
          <div class="flex flex-wrap items-center gap-3 bg-gray-50 dark:bg-gray-950/40 p-4 rounded-xl border border-gray-150 dark:border-gray-850">
            <span class="text-xs font-bold text-gray-650">قاعدة 1: السماح بالوصول إذا كان</span>
            
            <select class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg px-2.5 py-1 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option>محافظة المستخدم (Subject.Region)</option>
              <option>رتبة المستخدم (Subject.Rank)</option>
              <option>المنصب الوظيفي (Subject.Role)</option>
            </select>

            <span class="text-xs font-bold text-gray-400">تساوي (=)</span>

            <select class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg px-2.5 py-1 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option>محافظة السجل (Resource.Region)</option>
              <option>منطقة الفرع عسكري (Resource.Branch)</option>
            </select>

            <span class="text-xs font-bold text-gray-650">و</span>

            <select class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg px-2.5 py-1 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option>نوع العملية (Action.Type)</option>
              <option>وقت الطلب (Environment.Time)</option>
            </select>

            <span class="text-xs font-bold text-gray-400">ضمن (IN)</span>

            <span class="px-2 py-0.5 rounded text-[10px] bg-blue-50 text-blue-700 border border-blue-200 dark:bg-blue-950/20 dark:text-blue-400 font-bold">
              [قراءة، تصدير الكشوفات]
            </span>
          </div>

          <div class="flex justify-between items-center">
            <button class="text-xs text-brand-600 hover:text-brand-700 font-black cursor-pointer flex items-center gap-1">
              <span>+ إضافة شرط فرعي آخر</span>
            </button>
            <button class="bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-750 text-gray-700 dark:text-gray-300 text-xs font-bold px-3.5 py-1.5 rounded-lg cursor-pointer">
              تطبيق واختبار القاعدة
            </button>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

const roles = ['admin', 'officer', 'secretary', 'auditor']

const fields = [
  { label: 'الاسم الكامل واللقب للضابط', key: 'full_name', writeRoles: ['admin', 'officer'] },
  { label: 'الرتبة العسكرية الحالية', key: 'rank_id', writeRoles: ['admin', 'officer'] },
  { label: 'الرقم المالي والراتب الأساسي', key: 'salary_details', writeRoles: ['admin', 'auditor'] },
  { label: 'رقم الجوال ووسيلة الاتصال', key: 'phone_number', writeRoles: ['admin', 'officer', 'secretary'] },
  { label: 'المحافظة الحالية ومحل الميلاد', key: 'region_id', writeRoles: ['admin', 'officer'] },
  { label: 'سجل الملاحظات والتقارير السرية', key: 'secret_reports', writeRoles: ['admin'] }
]
</script>
