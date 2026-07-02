<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('roles.title')" />
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-end">
        <button
          @click="$router.push({ name: 'role-create' })"
          class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          {{ $t('roles.add_role') }}
        </button>
      </div>

      <!-- Table -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div v-if="rolesStore.loading" class="flex justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="rolesStore.error" class="p-8 text-center text-error-500">
          {{ rolesStore.error }}
        </div>

        <div v-else-if="rolesStore.roles.length === 0" class="p-8 text-center text-gray-500">
          {{ $t('common.no_data') || 'لا توجد مجموعات لعرضها.' }}
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('roles.role_name') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('roles.description') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('roles.permissions') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.role') || 'نوع المجموعة' }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.status') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="role in rolesStore.roles" :key="role.id" class="border-b border-gray-100 last:border-0 dark:border-gray-800">
                <td class="px-5 py-4">
                  <span class="font-medium text-gray-900 dark:text-white">{{ role.name }}</span>
                </td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-400">
                  {{ role.description || '—' }}
                </td>
                <td class="px-5 py-4 text-sm text-brand-600 dark:text-brand-400 font-medium">
                  {{ role.permissions?.length || 0 }} {{ $t('roles.permissions') }}
                </td>
                <td class="px-5 py-4">
                  <span v-if="role.is_system_role" class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium bg-purple-50 text-purple-700 dark:bg-purple-500/10 dark:text-purple-400">
                    {{ $t('users.admin') || 'أساسي (نظام)' }}
                  </span>
                  <span v-else class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                    {{ $t('users.regular_user') || 'مخصص' }}
                  </span>
                </td>
                <td class="px-5 py-4">
                  <span v-if="role.is_active" class="inline-flex items-center gap-1 rounded-full bg-success-50 px-2.5 py-0.5 text-xs font-medium text-success-700 dark:bg-success-500/10 dark:text-success-400">
                    <span class="h-1.5 w-1.5 rounded-full bg-success-500"></span>
                    {{ $t('users.active') }}
                  </span>
                  <span v-else class="inline-flex items-center gap-1 rounded-full bg-error-50 px-2.5 py-0.5 text-xs font-medium text-error-700 dark:bg-error-500/10 dark:text-error-400">
                    <span class="h-1.5 w-1.5 rounded-full bg-error-500"></span>
                    {{ $t('users.inactive') }}
                  </span>
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <button @click="$router.push({ name: 'role-edit', params: { id: role.id } })" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-brand-600 dark:hover:bg-gray-800 transition-colors" :title="$t('common.edit') || 'تعديل'">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button v-if="!role.is_system_role" @click="handleDelete(role)" class="rounded-lg p-2 text-gray-500 hover:bg-error-50 hover:text-error-600 dark:hover:bg-error-500/10 transition-colors" :title="$t('common.delete') || 'حذف'">
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
import { onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useRolesStore } from '@/stores/roles'
import Swal from 'sweetalert2'

const rolesStore = useRolesStore()

onMounted(() => {
  rolesStore.fetchRoles()
  rolesStore.fetchPermissionsMatrix()
})

async function handleDelete(role) {
  const res = await Swal.fire({
    title: 'تأكيد החذف',
    text: `هل أنت متأكد من حذف مجموعة "${role.name}"؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء'
  })

  if (res.isConfirmed) {
    try {
      await rolesStore.deleteRole(role.id)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الحذف', showConfirmButton: false, timer: 3000 })
    } catch (e) {
      Swal.fire('خطأ', 'فشل حذف المجموعة', 'error')
    }
  }
}
</script>
