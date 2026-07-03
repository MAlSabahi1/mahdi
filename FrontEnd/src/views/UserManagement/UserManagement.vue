<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 dark:text-white/90">
            {{ $t('users.title') }}
          </h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ $t('users.subtitle') }}
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="exportData"
            class="inline-flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-200 transition-colors dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            {{ $t('common.export') || 'تصدير' }}
          </button>
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            {{ $t('users.add_user') }}
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              @input="debouncedSearch"
              type="text"
              :placeholder="$t('common.search')"
              class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          <div class="flex gap-2">
            <button
              @click="filterActive = null; loadUsers()"
              :class="[
                'rounded-lg px-4 py-2.5 text-sm font-medium transition-colors',
                filterActive === null
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
              ]"
            >
              {{ $t('common.all') || 'الكل' }}
            </button>
            <button
              @click="filterActive = true; loadUsers()"
              :class="[
                'rounded-lg px-4 py-2.5 text-sm font-medium transition-colors',
                filterActive === true
                  ? 'bg-success-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
              ]"
            >
              {{ $t('users.active') }}
            </button>
            <button
              @click="filterActive = false; loadUsers()"
              :class="[
                'rounded-lg px-4 py-2.5 text-sm font-medium transition-colors',
                filterActive === false
                  ? 'bg-error-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
              ]"
            >
              {{ $t('users.inactive') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <!-- Loading -->
        <div v-if="usersStore.loading" class="flex items-center justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>

        <!-- Error -->
        <div v-else-if="usersStore.error" class="p-8 text-center">
          <p class="text-error-500">{{ usersStore.error }}</p>
          <button @click="loadUsers()" class="mt-4 text-sm text-brand-500 hover:text-brand-600">
            {{ $t('common.retry') || 'إعادة المحاولة' }}
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="usersStore.users.length === 0" class="p-8 text-center">
          <p class="text-gray-500 dark:text-gray-400">{{ $t('common.no_data') || 'لا توجد نتائج' }}</p>
        </div>

        <!-- Table Content -->
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800">
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.user') || 'المستخدم' }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.email') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.phone') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.status') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.role') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('users.last_login') }}</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="user in usersStore.users"
                :key="user.id"
                class="border-b border-gray-100 last:border-0 dark:border-gray-800"
              >
                <!-- User Info -->
                <td class="px-5 py-4">
                  <RouterLink :to="`/users/${user.id}`" class="group flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-full bg-brand-100 text-sm font-semibold text-brand-600 group-hover:bg-brand-200 dark:bg-brand-500/20 dark:text-brand-400 dark:group-hover:bg-brand-500/30 transition-colors">
                      {{ user.display_name?.charAt(0) || user.username.charAt(0) }}
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-800 group-hover:text-brand-500 dark:text-white/90 dark:group-hover:text-brand-400 transition-colors">
                        {{ user.display_name || user.full_name || user.username }}
                      </p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">@{{ user.username }}</p>
                    </div>
                  </RouterLink>
                </td>
                <!-- Email -->
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300">
                  {{ user.email || '—' }}
                </td>
                <!-- Phone -->
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300">
                  {{ user.phone || '—' }}
                </td>
                <!-- Status -->
                <td class="px-5 py-4">
                  <span v-if="user.security_status?.is_locked"
                    class="inline-flex items-center gap-1 rounded-full bg-warning-50 px-2.5 py-0.5 text-xs font-medium text-warning-700 dark:bg-warning-500/10 dark:text-warning-400">
                    <span class="h-1.5 w-1.5 rounded-full bg-warning-500"></span>
                    {{ $t('users.locked') || 'مقفل' }}
                  </span>
                  <span v-else-if="user.is_active" class="inline-flex items-center gap-1.5 rounded-full bg-success-50 px-2.5 py-1 text-xs font-medium text-success-700 dark:bg-success-500/10 dark:text-success-400">
                    <span class="h-1.5 w-1.5 rounded-full bg-success-500"></span>
                    {{ $t('users.active') }}
                  </span>
                  <span v-else class="inline-flex items-center gap-1.5 rounded-full bg-error-50 px-2.5 py-1 text-xs font-medium text-error-700 dark:bg-error-500/10 dark:text-error-400">
                    <span class="h-1.5 w-1.5 rounded-full bg-error-500"></span>
                    {{ $t('users.inactive') }}
                  </span>
                </td>
                <!-- Role -->
                <td class="px-5 py-4">
                  <div class="flex flex-wrap gap-1">
                    <span
                      :class="user.is_staff
                        ? 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400'
                        : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'"
                      class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium"
                    >
                      {{ user.is_staff ? $t('users.admin') : $t('users.regular_user') }}
                    </span>
                    <span
                      v-if="user.role"
                      class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400"
                    >
                      {{ user.role.name }}
                    </span>
                  </div>
                </td>
                <!-- Last Login -->
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300">
                  {{ user.last_login ? formatDate(user.last_login) : $t('users.never_logged_in') }}
                </td>
                <!-- Actions -->
                <td class="px-5 py-4">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      @click="openEditModal(user)"
                      class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200 transition-colors"
                      :title="$t('common.edit')"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button
                      @click="openResetPasswordModal(user)"
                      class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200 transition-colors"
                      :title="$t('users.reset_password') || 'إعادة تعيين كلمة المرور'"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                      </svg>
                    </button>
                    <button
                      v-if="user.security_status?.is_locked"
                      @click="handleUnlock(user)"
                      class="rounded-lg p-2 text-warning-500 hover:bg-warning-50 hover:text-warning-700 dark:hover:bg-warning-500/10 transition-colors"
                      :title="$t('users.unlock') || 'فك القفل'"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 2a5 5 0 00-5 5v2a2 2 0 00-2 2v5a2 2 0 002 2h10a2 2 0 002-2v-5a2 2 0 00-2-2H7V7a3 3 0 015.905-.75 1 1 0 001.937-.5A5.002 5.002 0 0010 2z" />
                      </svg>
                    </button>
                    <button
                      v-if="user.is_active"
                      @click="handleDeactivate(user)"
                      class="rounded-lg p-2 text-error-500 hover:bg-error-50 hover:text-error-700 dark:hover:bg-error-500/10 transition-colors"
                      :title="$t('users.deactivate') || 'تعطيل'"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 008.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clip-rule="evenodd" />
                      </svg>
                    </button>
                    <button
                      v-else
                      @click="handleActivate(user)"
                      class="rounded-lg p-2 text-success-500 hover:bg-success-50 hover:text-success-700 dark:hover:bg-success-500/10 transition-colors"
                      :title="$t('users.activate') || 'تفعيل'"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination & Count -->
        <div v-if="!usersStore.loading && usersStore.users.length > 0" class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <p class="text-sm text-gray-500 dark:text-gray-400 text-center sm:text-start">
            {{ $t('common.page') }} <span class="font-medium text-gray-900 dark:text-white">{{ usersStore.currentPage }}</span> {{ $t('common.from') }} <span class="font-medium text-gray-900 dark:text-white">{{ usersStore.totalPages }}</span>
            ({{ $t('common.total') }}: {{ usersStore.totalCount }} {{ $t('roles.users_count') }})
          </p>
          <div class="flex justify-center gap-2">
            <button
              @click="goToPage(usersStore.currentPage - 1)"
              :disabled="usersStore.currentPage === 1"
              class="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
            >
              <svg class="h-4 w-4 rtl:rotate-180" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              {{ $t('common.previous') || 'السابق' }}
            </button>
            <button
              @click="goToPage(usersStore.currentPage + 1)"
              :disabled="usersStore.currentPage === usersStore.totalPages"
              class="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
            >
              {{ $t('common.next') || 'التالي' }}
              <svg class="h-4 w-4 rtl:rotate-180" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Modals -->
    <CreateUserModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="onUserCreated"
    />
    <EditUserModal
      v-if="showEditModal && selectedUser"
      :user="selectedUser"
      @close="showEditModal = false"
      @updated="onUserUpdated"
    />
    <ResetPasswordModal
      v-if="showResetModal && selectedUser"
      :user="selectedUser"
      @close="showResetModal = false"
      @reset="onPasswordReset"
    />
  </admin-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useUsersStore } from '@/stores/users'
import CreateUserModal from './components/CreateUserModal.vue'
import EditUserModal from './components/EditUserModal.vue'
import ResetPasswordModal from './components/ResetPasswordModal.vue'
import Swal from 'sweetalert2'

const usersStore = useUsersStore()

const searchQuery = ref('')
const filterActive = ref(null)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showResetModal = ref(false)
const selectedUser = ref(null)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadUsers()
  }, 400)
}

function loadUsers(page = 1) {
  usersStore.fetchUsers(searchQuery.value || undefined, filterActive.value, page)
}

function goToPage(page) {
  if (page >= 1 && page <= usersStore.totalPages) {
    loadUsers(page)
  }
}

function exportData() {
  const token = localStorage.getItem('access_token')
  const url = `${import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'}/users/export/`
  
  fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  .then(response => response.blob())
  .then(blob => {
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.style.display = 'none'
    a.href = downloadUrl
    a.download = 'users_export.csv'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    a.remove()
    showToast('تم التصدير بنجاح')
  })
  .catch(() => {
    showToast('فشل تصدير البيانات', 'error')
  })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function showToast(message, type = 'success') {
  Swal.fire({ toast: true, position: 'top-end', icon: type, title: message, showConfirmButton: false, timer: 3000 })
}

function openEditModal(user) {
  selectedUser.value = user
  showEditModal.value = true
}

function openResetPasswordModal(user) {
  selectedUser.value = user
  showResetModal.value = true
}

async function handleDeactivate(user) {
  const result = await Swal.fire({
    title: 'تعطيل الحساب',
    text: `هل أنت متأكد من تعطيل حساب "${user.display_name || user.username}"؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#6B7280',
    confirmButtonText: 'نعم، تعطيل',
    cancelButtonText: 'إلغاء'
  })
  if (!result.isConfirmed) return
  try {
    await usersStore.deactivateUser(user.id)
    showToast('تم تعطيل الحساب بنجاح')
  } catch {
    showToast('فشل تعطيل الحساب', 'error')
  }
}

async function handleActivate(user) {
  try {
    await usersStore.activateUser(user.id)
    showToast('تم تفعيل الحساب بنجاح')
  } catch {
    showToast('فشل تفعيل الحساب', 'error')
  }
}

async function handleUnlock(user) {
  try {
    await usersStore.unlockUser(user.id)
    showToast('تم فك قفل الحساب بنجاح')
  } catch {
    showToast('فشل فك قفل الحساب', 'error')
  }
}

function onUserCreated() {
  showCreateModal.value = false
  showToast('تم إنشاء المستخدم بنجاح')
}

function onUserUpdated() {
  showEditModal.value = false
  showToast('تم تحديث المستخدم بنجاح')
}

function onPasswordReset() {
  showResetModal.value = false
  showToast('تم إعادة تعيين كلمة المرور بنجاح')
}

onMounted(() => {
  usersStore.fetchRoles()
  loadUsers()
})
</script>
