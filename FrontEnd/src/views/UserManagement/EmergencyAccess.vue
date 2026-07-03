<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تفويض الصلاحيات والوصول الطارئ" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 border-b border-gray-200 dark:border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            تفويض الصلاحيات والوصول الطارئ (Break-Glass)
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            إدارة فترات تفويض الصلاحيات المؤقتة بين الضباط وتفعيل بروتوكولات الوصول الاستثنائي عند الطوارئ.
          </p>
        </div>
      </div>

      <!-- Emergency Break-Glass Alert Card -->
      <div class="bg-red-50/60 dark:bg-red-950/10 border border-red-200 dark:border-red-900/30 rounded-2xl p-6">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div class="flex items-start gap-4">
            <span class="p-3 rounded-xl bg-red-100 text-red-650 dark:bg-red-950/40 dark:text-red-400 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </span>
            <div>
              <h3 class="text-sm font-black text-red-800 dark:text-red-300">نظام الوصول الاستثنائي (Break-Glass System)</h3>
              <p class="text-[11px] text-red-700/80 dark:text-red-400/80 mt-1.5 leading-relaxed max-w-3xl">
                يسمح وضع الطوارئ للضباط المعتمدين بتجاوز قيود الـ ABAC العادية للوصول الفوري إلى البيانات الحيوية عند الكوارث أو تعطل الاتصالات الإقليمية. يخضع هذا الإجراء للتدقيق الفوري ويقوم بإرسال إشعارات فورية لجميع مدراء النظام.
              </p>
            </div>
          </div>
          
          <button class="bg-red-650 hover:bg-red-700 text-white text-xs font-black px-4 py-2.5 rounded-xl cursor-pointer shrink-0 shadow-theme-xs">
            تفعيل وضع الطوارئ (Break-Glass)
          </button>
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- New Delegation Form -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-1">
          <h3 class="text-sm font-black text-gray-900 dark:text-white mb-4">إنشاء تفويض صلاحيات مؤقت</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-[11px] font-bold text-gray-500 mb-1.5">الضابط المفوض له الصلاحية</label>
              <select class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
                <option value="">اختر الحساب...</option>
                <option v-for="u in users" :key="u.id" :value="u.id">
                  {{ u.full_name || u.username }} ({{ u.username }})
                </option>
              </select>
            </div>

            <div>
              <label class="block text-[11px] font-bold text-gray-500 mb-1.5">الحزمة الصلاحية المفوضة</label>
              <select class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
                <option>صلاحية اعتماد الكشوفات الإقليمية</option>
                <option>صلاحية تعديل الرتب والتسويات</option>
                <option>صلاحية الاطلاع الكامل دون تعديل</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[11px] font-bold text-gray-500 mb-1.5">تاريخ البدء</label>
                <input type="date" value="2026-07-04" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300" />
              </div>
              <div>
                <label class="block text-[11px] font-bold text-gray-500 mb-1.5">تاريخ الانتهاء</label>
                <input type="date" value="2026-07-10" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300" />
              </div>
            </div>

            <div>
              <label class="block text-[11px] font-bold text-gray-500 mb-1.5">سبب التفويض المعتمد</label>
              <textarea placeholder="تحديد المهمة الرسمية لتفويض الصلاحية..." rows="3" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300"></textarea>
            </div>

            <button class="w-full bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold py-2 rounded-lg cursor-pointer">
              إصدار أمر التفويض
            </button>
          </div>
        </div>

        <!-- Active Delegations Table -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden lg:col-span-2 flex flex-col">
          <div class="p-5 border-b border-gray-200 dark:border-gray-800">
            <h3 class="text-sm font-black text-gray-900 dark:text-white">سجل التفويضات النشطة والمعلقة</h3>
            <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-1">
              متابعة التفويضات السارية المفعول بين الإدارات لإلغائها أو تعديل مدتها.
            </p>
          </div>

          <div class="overflow-x-auto flex-1">
            <table class="w-full text-right border-collapse text-xs">
              <thead>
                <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-950/20">
                  <th class="px-5 py-3">المفوض</th>
                  <th class="px-5 py-3">المفوض له</th>
                  <th class="px-5 py-3">الصلاحية</th>
                  <th class="px-5 py-3">الفترة الزمنية</th>
                  <th class="px-5 py-3">الحالة</th>
                  <th class="px-5 py-3">العمليات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
                <tr>
                  <td colspan="6" class="px-5 py-8 text-center text-gray-400 dark:text-gray-500">
                    لا توجد تفويضات نشطة أو معلقة حالياً في النظام.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Break-Glass Audit Trail Log -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="p-5 border-b border-gray-200 dark:border-gray-800">
          <h3 class="text-sm font-black text-gray-900 dark:text-white">سجل استخدام وضع الطوارئ والوصول الطارئ (Break-Glass Audit Log)</h3>
          <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-1">
            سجل تاريخي دقيق يوثق مبررات تفعيل وضع الطوارئ وهوية المستخدمين الفاعلين.
          </p>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-5 py-3">المستخدم</th>
                <th class="px-5 py-3">الرتبة والإدارة</th>
                <th class="px-5 py-3">البيانات التي تم الوصول إليها</th>
                <th class="px-5 py-3">تاريخ التفعيل</th>
                <th class="px-5 py-3">سبب وحالة التفعيل</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr>
                <td colspan="5" class="px-5 py-8 text-center text-gray-400 dark:text-gray-500">
                  لا توجد سجلات تفعيل لوضع الوصول الاستثنائي (Break-Glass) حالياً.
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
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import api from '@/lib/api'

interface UserRecord {
  id: number
  username: string
  full_name: string
}

const users = ref<UserRecord[]>([])
const loadingUsers = ref(false)

async function fetchUsers() {
  loadingUsers.value = true
  try {
    const res = await api.get('/users/', { params: { page_size: 500 } })
    users.value = res.data.results || []
  } catch (err) {
    console.error('Failed to fetch users for delegation:', err)
  } finally {
    loadingUsers.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
