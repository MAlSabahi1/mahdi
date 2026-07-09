<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="h-8 w-8 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            الأرشيف واللقطة الشهرية
          </h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            تجميد وتوثيق حالة القوة العاملة نهاية كل شهر كمرجع ثابت للرواتب والإحصائيات
          </p>
        </div>
        <button
          @click="generateSnapshot"
          :disabled="isGenerating"
          class="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-brand-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 disabled:opacity-70 disabled:cursor-not-allowed transition-all"
        >
          <svg v-if="isGenerating" class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          إصدار لقطة الشهر الحالي
        </button>
      </div>

      <!-- Feedback Messages -->
      <div v-if="message" class="rounded-lg bg-green-50 p-4 dark:bg-green-900/30 border border-green-200 dark:border-green-800">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="mr-3">
            <p class="text-sm font-medium text-green-800 dark:text-green-300">{{ message }}</p>
          </div>
        </div>
      </div>
      <div v-if="error" class="rounded-lg bg-red-50 p-4 dark:bg-red-900/30 border border-red-200 dark:border-red-800">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="mr-3">
            <p class="text-sm font-medium text-red-800 dark:text-red-300">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-right text-sm">
            <thead class="bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700">
              <tr>
                <th class="px-6 py-4 font-semibold">تاريخ اللقطة (الشهر)</th>
                <th class="px-6 py-4 font-semibold">إجمالي الأفراد المؤرشفين</th>
                <th class="px-6 py-4 font-semibold text-left">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="item in snapshots" :key="item.snapshot_date" class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="h-10 w-10 flex-shrink-0 rounded-lg bg-brand-100 dark:bg-brand-900/40 flex items-center justify-center">
                      <svg class="h-5 w-5 text-brand-600 dark:text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <div class="font-bold text-gray-900 dark:text-white text-base" dir="ltr">{{ item.snapshot_date }}</div>
                      <div class="text-xs text-gray-500">أرشيف رسمي معتمد</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-sm font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 ring-1 ring-inset ring-blue-700/10">
                    {{ item.total_personnel }} فرد
                  </span>
                </td>
                <td class="px-6 py-4 text-left">
                  <button class="text-brand-600 hover:text-brand-900 dark:text-brand-400 dark:hover:text-brand-300 font-medium">
                    استعراض الأرشيف
                  </button>
                </td>
              </tr>
              <tr v-if="snapshots.length === 0 && !loading">
                <td colspan="3" class="px-6 py-12 text-center text-gray-500">
                  <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                  </svg>
                  لا توجد لقطات شهرية مؤرشفة بعد
                </td>
              </tr>
              <tr v-if="loading">
                <td colspan="3" class="px-6 py-12 text-center">
                  <svg class="animate-spin mx-auto h-8 w-8 text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
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
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const snapshots = ref<any[]>([])
const loading = ref(false)
const isGenerating = ref(false)
const message = ref('')
const error = ref('')

const fetchSnapshots = async () => {
  loading.value = true
  try {
    const res = await api.get('/personnel/snapshots/')
    snapshots.value = res.data
  } catch (err) {
    console.error('Failed to load snapshots', err)
  } finally {
    loading.value = false
  }
}

const generateSnapshot = async () => {
  if (!confirm('هل أنت متأكد من رغبتك في تجميد حالة القوة العاملة الحالية؟ هذه العملية قد تستغرق بضع دقائق.')) {
    return
  }
  
  isGenerating.value = true
  message.value = ''
  error.value = ''
  
  try {
    const res = await api.post('/personnel/snapshots/', {})
    message.value = res.data.message
    await fetchSnapshots()
  } catch (err: any) {
    error.value = err.response?.data?.error || 'حدث خطأ أثناء محاولة توليد اللقطة.'
  } finally {
    isGenerating.value = false
  }
}

onMounted(() => {
  fetchSnapshots()
})
</script>
