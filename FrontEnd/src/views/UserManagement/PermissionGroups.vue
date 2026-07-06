<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('roles.permission_groups') || 'مجموعات الصلاحيات'" />
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">إدارة مجموعات الصلاحيات</h2>
          <p class="text-sm text-gray-500">قم بتنظيم الصلاحيات في مجموعات منطقية لسهولة إدارتها.</p>
        </div>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          إضافة مجموعة جديدة
        </button>
      </div>

      <!-- Table -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div v-if="loading" class="flex justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="error" class="p-8 text-center text-error-500">
          {{ error }}
        </div>

        <div v-else-if="groups.length === 0" class="p-8 text-center text-gray-500">
          لا توجد مجموعات لعرضها.
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">اسم المجموعة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الوحدة (Module)</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">ترتيب العرض</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">تاريخ الإنشاء</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">إجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="group in groups" :key="group.id" class="border-b border-gray-100 last:border-0 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/20">
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <div class="h-8 w-8 rounded-lg bg-brand-50 flex items-center justify-center text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                      <i :class="group.icon || 'mdi mdi-folder-outline'" class="text-lg"></i>
                    </div>
                    <span class="font-medium text-gray-900 dark:text-white">{{ group.name }}</span>
                  </div>
                </td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-400">
                  <span class="inline-flex rounded-md bg-gray-100 px-2 py-1 text-xs font-medium text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                    {{ group.module_name || 'عام' }}
                  </span>
                </td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-400">
                  {{ group.display_order }}
                </td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-400">
                  {{ new Date(group.created_at).toLocaleDateString('ar-YE') }}
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <button @click="openEditModal(group)" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-brand-600 dark:hover:bg-gray-800 transition-colors" title="تعديل">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button @click="handleDelete(group)" class="rounded-lg p-2 text-gray-500 hover:bg-error-50 hover:text-error-600 dark:hover:bg-error-500/10 transition-colors" title="حذف">
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
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import axiosInstance from '@/lib/api'
import Swal from 'sweetalert2'

const groups = ref([])
const loading = ref(false)
const error = ref('')

async function fetchGroups() {
  loading.value = true
  error.value = ''
  try {
    const res = await axiosInstance.get('/permission-groups/')
    groups.value = res.data.results || res.data || []
  } catch (err) {
    console.error(err)
    error.value = 'تعذر جلب مجموعات الصلاحيات'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  Swal.fire({
    title: 'ميزة قيد التطوير',
    text: 'هذه الشاشة سيتم ربطها بواجهة الإنشاء والتعديل الكاملة، وهي جزء من الخطة التطويرية.',
    icon: 'info'
  })
}

function openEditModal(group) {
  openCreateModal()
}

async function handleDelete(group) {
  const res = await Swal.fire({
    title: 'تأكيد الحذف',
    text: `هل أنت متأكد من حذف مجموعة "${group.name}"؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء'
  })

  if (res.isConfirmed) {
    try {
      await axiosInstance.delete(`/permission-groups/${group.id}/`)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الحذف', showConfirmButton: false, timer: 3000 })
      fetchGroups()
    } catch (e) {
      Swal.fire('خطأ', 'فشل الحذف. قد تكون هناك صلاحيات مرتبطة بهذه المجموعة.', 'error')
    }
  }
}

onMounted(() => {
  fetchGroups()
})
</script>
