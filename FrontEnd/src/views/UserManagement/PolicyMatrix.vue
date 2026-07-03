<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="مصفوفة صلاحيات الحقول والسياسات" />

    <div class="space-y-6 text-start" dir="rtl">
      <!-- Header Controls -->
      <div class="flex justify-between items-center bg-white dark:bg-gray-900 p-4 rounded-xl border border-gray-200 dark:border-gray-800 shadow-theme-xs">
        <div class="text-right">
          <h2 class="text-lg font-black text-gray-900 dark:text-white">إعدادات سياسات الحقول (ABAC)</h2>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">تحديد صلاحيات القراءة والكتابة لكل حقل من حقول الأفراد بناءً على الدور الوظيفي.</p>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="$router.push({ name: 'roles-management' })"
            class="rounded-lg border border-gray-200 bg-white px-5 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 cursor-pointer"
          >
            إلغاء
          </button>
          <button 
            @click="saveMatrix"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
          >
            <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            حفظ مصفوفة الصلاحيات
          </button>
        </div>
      </div>

      <!-- Basic Config Card -->
      <div class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 overflow-hidden">
        <div class="border-b border-gray-100 p-5 dark:border-gray-800">
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">التهيئة العامة للمصفوفة</h3>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">الجدول المستهدف بالتطبيق</label>
              <select v-model="selectedTable" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-950 dark:bg-gray-850 dark:border-gray-700 dark:text-white">
                <option value="personnel">بيانات الأفراد والمنتسبين (PersonnelMaster)</option>
                <option value="export_configs">إعدادات النماذج المالية (ExportConfig)</option>
                <option value="reconciliations">سجلات المطابقات والتسويات (Reconciliation)</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">نمط فرض السياسة</label>
              <select v-model="policyMode" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-950 dark:bg-gray-850 dark:border-gray-700 dark:text-white">
                <option value="strict">فرض صارم (حظر البيانات وقفل الحقول فورياً)</option>
                <option value="monitor">مراقبة وتسجيل (تسجيل محاولات الوصول غير المصرح بها)</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">حالة السياسة</label>
              <div class="flex items-center pt-3">
                <label class="relative inline-flex cursor-pointer items-center">
                  <input v-model="policyActive" type="checkbox" class="peer sr-only" />
                  <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-success-500 peer-checked:after:translate-x-full peer-checked:after:border-white dark:border-gray-700 dark:bg-gray-700 rtl:peer-checked:after:-translate-x-full"></div>
                  <span class="ms-3 text-sm font-medium text-gray-700 dark:text-gray-300">نشطة وتعمل حالياً</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Field-level Permissions Matrix Card -->
      <div class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 overflow-hidden">
        <div class="flex flex-col gap-4 border-b border-gray-100 p-5 sm:flex-row sm:items-center sm:justify-between dark:border-gray-800">
          <div>
            <h3 class="text-base font-semibold text-gray-900 dark:text-white">جدول توزيع صلاحيات الحقول</h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">حدد حقول القراءة (عرض الحقل) وحقول الكتابة (السماح بالتعديل) لكل دور أمني.</p>
          </div>
        </div>

        <div class="overflow-x-auto w-full">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800 text-right">
            <thead class="bg-gray-50/50 dark:bg-gray-800/30">
              <tr>
                <th class="px-5 py-4 text-start text-sm font-semibold text-gray-700 dark:text-gray-300 min-w-[200px] border-l border-gray-200 dark:border-gray-800">الحقل في قاعدة البيانات</th>
                <th 
                  v-for="role in roles" 
                  :key="role.code" 
                  class="px-4 py-4 text-center border-l border-gray-200 dark:border-gray-800 last:border-0"
                >
                  <div class="text-sm font-semibold text-gray-800 dark:text-gray-200">{{ role.label }}</div>
                  <div class="text-[10px] text-gray-400 font-mono mt-0.5">{{ role.code }}</div>
                </th>
              </tr>
            </thead>
            
            <tbody class="divide-y divide-gray-100 bg-white dark:divide-gray-800 dark:bg-transparent">
              <template v-for="group in groups" :key="group.title">
                <!-- Group Header Row -->
                <tr class="bg-gray-50/70 dark:bg-gray-950/20 font-bold text-gray-900 dark:text-gray-100">
                  <td :colspan="roles.length + 1" class="px-5 py-3 text-start border-y border-gray-200 dark:border-gray-800 text-xs font-black">
                    📁 {{ group.title }}
                  </td>
                </tr>
                
                <!-- Fields Rows -->
                <tr v-for="field in group.fields" :key="field.key" class="border-b border-gray-100 last:border-0 dark:border-gray-850 hover:bg-gray-50/40 dark:hover:bg-gray-800/10">
                  <td class="px-5 py-4 text-start border-l border-gray-200 dark:border-gray-850">
                    <div class="font-semibold text-gray-900 dark:text-white text-xs">{{ field.label }}</div>
                    <div class="text-[10px] text-gray-400 font-mono mt-0.5">{{ field.key }}</div>
                  </td>
                  
                  <td 
                    v-for="role in roles" 
                    :key="role.code" 
                    class="px-4 py-4 text-center border-l border-gray-200 dark:border-gray-850 last:border-0"
                  >
                    <div v-if="permissions[field.key] && permissions[field.key][role.code]" class="inline-flex items-center gap-4 justify-center">
                      <label class="flex items-center gap-1.5 cursor-pointer">
                        <input 
                          type="checkbox" 
                          v-model="permissions[field.key][role.code].read"
                          class="h-4.5 w-4.5 rounded border-gray-300 text-brand-600 focus:ring-brand-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors"
                        />
                        <span class="text-[11px] text-gray-600 dark:text-gray-400 font-medium">قراءة</span>
                      </label>
                      
                      <label class="flex items-center gap-1.5 cursor-pointer">
                        <input 
                          type="checkbox" 
                          v-model="permissions[field.key][role.code].write"
                          class="h-4.5 w-4.5 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors"
                        />
                        <span class="text-[11px] text-gray-600 dark:text-gray-400 font-medium">كتابة</span>
                      </label>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'

const selectedTable = ref('personnel')
const policyMode = ref('strict')
const policyActive = ref(true)

const roles = [
  { code: 'admin', label: 'مدير كامل' },
  { code: 'governorate_admin', label: 'مدير أمن المحافظة' },
  { code: 'district_admin', label: 'مدير أمن المديرية' },
  { code: 'regular_user', label: 'مدخل بيانات' }
]

const groups = [
  {
    title: 'بيانات الهوية والبيانات الشخصية',
    fields: [
      { key: 'military_number', label: 'الرقم العسكري', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'old_military_number', label: 'الرقم العسكري القديم', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin', 'governorate_admin'] },
      { key: 'full_name', label: 'الاسم الكامل', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'national_id', label: 'الرقم الوطني', defaultRead: ['admin', 'governorate_admin', 'district_admin'], defaultWrite: ['admin'] },
      { key: 'phone_number', label: 'رقم الهاتف', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin', 'governorate_admin', 'district_admin', 'regular_user'] },
      { key: 'birth_date', label: 'تاريخ الميلاد', defaultRead: ['admin', 'governorate_admin', 'district_admin'], defaultWrite: ['admin'] },
      { key: 'qualification', label: 'المؤهل الدراسي', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin', 'governorate_admin'] },
    ]
  },
  {
    title: 'بيانات الهيكل التنظيمي والجغرافي',
    fields: [
      { key: 'security_admin', label: 'إدارة أمن المحافظة', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'central_department', label: 'الإدارة المركزية', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'branch', label: 'الفرع', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'district_police', label: 'أمن المديرية', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'force_classification', label: 'تصنيف القوة', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
    ]
  },
  {
    title: 'الحالة الخدمية والقرارات',
    fields: [
      { key: 'current_rank', label: 'الرتبة الحالية', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'current_status_classification', label: 'تصنيف الحالة الخدمية', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'current_status', label: 'الحالة الخدمية الحالية', defaultRead: ['admin', 'governorate_admin', 'district_admin', 'regular_user'], defaultWrite: ['admin'] },
      { key: 'join_date', label: 'تاريخ الالتحاق', defaultRead: ['admin', 'governorate_admin', 'district_admin'], defaultWrite: ['admin'] },
    ]
  }
]

const permissions = ref<Record<string, Record<string, { read: boolean; write: boolean }>>>({})

const initializePermissions = () => {
  groups.forEach(group => {
    group.fields.forEach(field => {
      permissions.value[field.key] = {}
      roles.forEach(role => {
        permissions.value[field.key][role.code] = {
          read: field.defaultRead.includes(role.code),
          write: field.defaultWrite.includes(role.code)
        }
      })
    })
  })
}

onMounted(() => {
  initializePermissions()
})

const saveMatrix = () => {
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: 'تم حفظ مصفوفة صلاحيات الحقول بنجاح',
    showConfirmButton: false,
    timer: 3000
  })
}
</script>
