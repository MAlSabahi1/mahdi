<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('services.resolve_conflicts') || 'حل تعارضات المطابقة'" />
    <div class="space-y-6">
      
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <p v-if="task" class="text-sm text-gray-500 dark:text-gray-400">
            {{ $t('services.task') || 'المهمة' }}: <span class="font-bold text-gray-900 dark:text-white">{{ task.name }}</span> | {{ $t('services.type') || 'النوع' }}: {{ task.task_type }}
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="submitResolutions"
            :disabled="resolutions.length === 0 || isSubmitting"
            class="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-colors disabled:opacity-50 cursor-pointer"
          >
            <svg v-if="isSubmitting" class="h-4.5 w-4.5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            <svg v-else class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            {{ $t('services.apply_resolutions') || 'تطبيق الحلول المحددة' }} ({{ resolutions.length }})
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-center p-12">
        <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
      </div>

      <div v-else-if="!task" class="p-8 text-center bg-white rounded-2xl dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
        <h3 class="text-lg font-bold text-error-600">المهمة غير موجودة</h3>
      </div>
      
      <div v-else-if="task.status === 'resolved'" class="p-8 text-center bg-white rounded-2xl dark:bg-gray-900 border border-gray-200 dark:border-gray-800 flex flex-col items-center">
        <div class="h-16 w-16 bg-success-100 text-success-600 rounded-full flex items-center justify-center mb-4 dark:bg-success-900/30 dark:text-success-400">
          <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">المهمة مكتملة ومحلولة</h3>
        <p class="mt-2 text-gray-500 dark:text-gray-400">لقد تم تطبيق جميع الحلول على هذه المهمة بنجاح.</p>
      </div>

      <div v-else-if="discrepancies.length === 0" class="p-8 text-center bg-white rounded-2xl dark:bg-gray-900 border border-gray-200 dark:border-gray-800 flex flex-col items-center">
        <div class="h-16 w-16 bg-brand-100 text-brand-600 rounded-full flex items-center justify-center mb-4 dark:bg-brand-900/30 dark:text-brand-400">
          <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.514"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">لا توجد اختلافات!</h3>
        <p class="mt-2 text-gray-500 dark:text-gray-400">تمت مطابقة الملف بشكل كامل مع قاعدة البيانات ولا توجد أي بيانات متعارضة.</p>
      </div>

      <!-- Data Table -->
      <div v-else class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-start">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">مفتاح الربط</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">البيانات الحالية (النظام)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">البيانات الواردة (الملف)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">القرار (أي القيم ستعتمد؟)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="(item, idx) in discrepancies" :key="idx" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td class="px-5 py-4 font-mono text-sm font-medium text-gray-900 dark:text-white">
                  {{ item.key_value || item.system_record?.military_number || '-' }}
                </td>
                <td class="px-5 py-4 text-sm">
                  <div class="space-y-1">
                    <div v-for="(val, field) in item.system_record" :key="field">
                      <span v-if="isFieldDifferent(field, item)" class="font-bold text-gray-500 dark:text-gray-400">{{ formatFieldName(field) }}: </span>
                      <span v-if="isFieldDifferent(field, item)" class="text-error-600 line-through decoration-error-500/50">{{ val || '-' }}</span>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-4 text-sm">
                  <div class="space-y-1">
                    <div v-for="(val, field) in item.file_record" :key="field">
                      <span v-if="isFieldDifferent(field, item)" class="font-bold text-gray-500 dark:text-gray-400">{{ formatFieldName(field) }}: </span>
                      <span v-if="isFieldDifferent(field, item)" class="text-success-600 font-bold bg-success-50 dark:bg-success-500/10 px-1 rounded">{{ val || '-' }}</span>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <div class="flex flex-col gap-2">
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" :name="`resolve_${idx}`" :value="'system'" v-model="resolutionMap[idx]" @change="updateResolutions" class="h-4 w-4 text-brand-600 focus:ring-brand-500 border-gray-300">
                      <span class="text-sm text-gray-700 dark:text-gray-300">البقاء على النظام</span>
                    </label>
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" :name="`resolve_${idx}`" :value="'file'" v-model="resolutionMap[idx]" @change="updateResolutions" class="h-4 w-4 text-success-600 focus:ring-success-500 border-gray-300">
                      <span class="text-sm font-medium text-success-700 dark:text-success-400">اعتماد بيانات الملف</span>
                    </label>
                  </div>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()

const isLoading = ref(true)
const isSubmitting = ref(false)
const task = ref<any>(null)
const discrepancies = ref<any[]>([])

// Map to hold radio selections: index -> 'system' | 'file'
const resolutionMap = ref<Record<number, string>>({})
const resolutions = ref<any[]>([])

onMounted(async () => {
  const taskId = route.params.id as string
  if (taskId) {
    try {
      task.value = await servicesStore.fetchReconciliationTaskDetails(taskId)
      // Extract discrepancies from task results
      if (task.value.results && task.value.results.discrepancies) {
        discrepancies.value = task.value.results.discrepancies
        // Pre-select 'file' (accept file changes by default to save time)
        discrepancies.value.forEach((d, idx) => {
          resolutionMap.value[idx] = 'file'
        })
        updateResolutions()
      }
    } catch (e) {
      Swal.fire('خطأ', 'فشل تحميل بيانات المهمة', 'error')
    } finally {
      isLoading.value = false
    }
  }
})

function updateResolutions() {
  resolutions.value = Object.keys(resolutionMap.value).map(idx => {
    return {
      record_index: parseInt(idx),
      source: resolutionMap.value[parseInt(idx)]
    }
  })
}

function isFieldDifferent(field: string | number, item: any): boolean {
  const fieldStr = String(field)
  // If the backend returns a fields_changed array, use it
  if (item.fields_changed && Array.isArray(item.fields_changed)) {
    return item.fields_changed.includes(fieldStr)
  }
  // Fallback string comparison
  return String(item.system_record[fieldStr]) !== String(item.file_record[fieldStr])
}

function formatFieldName(field: string | number): string {
  const fieldStr = String(field)
  const map: Record<string, string> = {
    military_number: 'الرقم العسكري',
    full_name: 'الاسم',
    rank: 'الرتبة',
    salary: 'الراتب',
    status: 'الحالة',
    national_id: 'الرقم الوطني'
  }
  return map[fieldStr] || fieldStr
}

async function submitResolutions() {
  if (resolutions.value.length === 0) return
  
  isSubmitting.value = true
  try {
    const res = await servicesStore.resolveReconciliation(task.value.id, resolutions.value)
    Swal.fire({
      title: 'تم الحل',
      text: `تم تطبيق الحلول بنجاح: تم تطبيق ${res.data?.applied || 0} سجل، وفشل ${res.data?.failed || 0}.`,
      icon: 'success',
      confirmButtonText: 'حسناً',
      confirmButtonColor: '#10b981'
    }).then(() => {
      router.push('/services/reconciliation')
    })
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل تطبيق الحلول', 'error')
  } finally {
    isSubmitting.value = false
  }
}
</script>
