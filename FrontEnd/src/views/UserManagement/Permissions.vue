<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('roles.permissions') || 'الصلاحيات (Permissions)'" />
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">إدارة الصلاحيات المباشرة</h2>
          <p class="text-sm text-gray-500">سجل بجميع الصلاحيات المُعرّفة في النظام، مع إمكانية ربطها بالمجموعات.</p>
        </div>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          تسجيل صلاحية جديدة
        </button>
      </div>

      <!-- Table -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div class="p-4 border-b border-gray-100 dark:border-gray-800 flex gap-4">
          <input type="text" v-model="search" placeholder="ابحث بكود الصلاحية أو الاسم..." class="block w-full max-w-md rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
        </div>

        <div v-if="loading" class="flex justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="error" class="p-8 text-center text-error-500">
          {{ error }}
        </div>

        <div v-else-if="filteredPermissions.length === 0" class="p-8 text-center text-gray-500">
          لا توجد صلاحيات لعرضها.
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الكود (Code)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الوصف (Label)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الشاشة (Module)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">مجموعة الصلاحيات</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الحالة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">إجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="perm in filteredPermissions" :key="perm.id" class="border-b border-gray-100 last:border-0 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/20">
                <td class="px-5 py-3">
                  <span class="font-mono text-sm text-gray-900 dark:text-white bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">{{ perm.code }}</span>
                </td>
                <td class="px-5 py-3 text-sm text-gray-600 dark:text-gray-400 font-medium">
                  {{ perm.label }}
                </td>
                <td class="px-5 py-3 text-sm text-gray-600 dark:text-gray-400">
                  <span class="inline-flex rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 dark:bg-blue-500/10 dark:text-blue-400">
                    {{ perm.module }}
                  </span>
                </td>
                <td class="px-5 py-3 text-sm text-gray-600 dark:text-gray-400">
                  {{ perm.group_name || 'غير محدد' }}
                </td>
                <td class="px-5 py-3">
                  <span v-if="perm.is_active" class="inline-flex items-center gap-1 rounded-full bg-success-50 px-2.5 py-0.5 text-xs font-medium text-success-700 dark:bg-success-500/10 dark:text-success-400">
                    نشط
                  </span>
                  <span v-else class="inline-flex items-center gap-1 rounded-full bg-error-50 px-2.5 py-0.5 text-xs font-medium text-error-700 dark:bg-error-500/10 dark:text-error-400">
                    معطل
                  </span>
                </td>
                <td class="px-5 py-3">
                  <div class="flex items-center gap-2">
                    <button @click="openEditModal(perm)" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-brand-600 dark:hover:bg-gray-800 transition-colors" title="تعديل">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button @click="handleDelete(perm)" class="rounded-lg p-2 text-gray-500 hover:bg-error-50 hover:text-error-600 dark:hover:bg-error-500/10 transition-colors" title="حذف">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import axiosInstance from '@/lib/api'
import Swal from 'sweetalert2'

const permissions = ref([])
const loading = ref(false)
const error = ref('')
const search = ref('')

const filteredPermissions = computed(() => {
  if (!search.value) return permissions.value
  const q = search.value.toLowerCase()
  return permissions.value.filter(p => p.code.toLowerCase().includes(q) || p.label.toLowerCase().includes(q) || p.module.toLowerCase().includes(q))
})

async function fetchPermissions() {
  loading.value = true
  error.value = ''
  try {
    const res = await axiosInstance.get('/permissions/')
    permissions.value = res.data.results || res.data || []
  } catch (err) {
    console.error(err)
    error.value = 'تعذر جلب الصلاحيات'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  Swal.fire({
    title: 'ميزة قيد التطوير',
    text: 'هذه الشاشة سيتم ربطها بواجهة إنشاء الصلاحيات التفصيلية وتحديد الـ (Module, Action, Scope)، وهي جزء من الخطة التطويرية الجارية.',
    icon: 'info'
  })
}

function openEditModal(perm) {
  openCreateModal()
}

async function handleDelete(perm) {
  if (perm.is_system) {
    return Swal.fire('مرفوض', 'لا يمكن حذف صلاحيات النظام الأساسية، يمكنك فقط تعطيلها.', 'error')
  }
  
  const res = await Swal.fire({
    title: 'تأكيد الحذف',
    text: `هل أنت متأكد من حذف الصلاحية "${perm.label}"؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء'
  })

  if (res.isConfirmed) {
    try {
      await axiosInstance.delete(`/permissions/${perm.id}/`)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الحذف', showConfirmButton: false, timer: 3000 })
      fetchPermissions()
    } catch (e) {
      Swal.fire('خطأ', 'فشل الحذف.', 'error')
    }
  }
}

onMounted(() => {
  fetchPermissions()
})
</script>
