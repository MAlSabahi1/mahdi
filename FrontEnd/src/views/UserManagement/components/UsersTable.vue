<template>
  <div class="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
    <!-- Loading spinner -->
    <div v-if="loading" class="flex items-center justify-center p-12">
      <svg class="h-8 w-8 animate-spin text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <!-- Error display -->
    <div v-else-if="error" class="p-8 text-center">
      <p class="text-red-500">{{ error }}</p>
      <button @click="$emit('retry')" class="mt-4 text-sm text-blue-600 hover:text-blue-700 font-semibold cursor-pointer">
        إعادة المحاولة
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="users.length === 0" class="p-8 text-center">
      <p class="text-gray-500 dark:text-gray-400">لا توجد نتائج مطابقة لبحثك.</p>
    </div>

    <!-- Table Content -->
    <div v-else class="overflow-x-auto">
      <table class="w-full border-collapse text-start">
        <thead>
          <tr class="bg-[#f8fafc] dark:bg-gray-950">
            <!-- Checkbox -->
            <th class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 w-12 text-center">
              <input
                type="checkbox"
                v-model="selectAll"
                @change="$emit('toggle-select-all')"
                class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-800"
              />
            </th>
            <!-- Row index -->
            <th v-if="isColumnVisible('index')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 w-12 text-center text-xs font-bold text-gray-700 dark:text-gray-300">#</th>
            <!-- Columns -->
            <th v-if="isColumnVisible('first_name')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-start text-xs font-bold text-gray-700 dark:text-gray-300">الاسم الأول</th>
            <th v-if="isColumnVisible('last_name')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-start text-xs font-bold text-gray-700 dark:text-gray-300">الاسم الأخير</th>
            <th v-if="isColumnVisible('username')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-start text-xs font-bold text-gray-700 dark:text-gray-300">اسم المستخدم</th>
            <th v-if="isColumnVisible('email')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-start text-xs font-bold text-gray-700 dark:text-gray-300">البريد الإلكتروني</th>
            <th v-if="isColumnVisible('system_type')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-start text-xs font-bold text-gray-700 dark:text-gray-300">نوع النظام</th>
            <th v-if="isColumnVisible('groups')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-start text-xs font-bold text-gray-700 dark:text-gray-300">المجموعات</th>
            <th v-if="isColumnVisible('is_active')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-center text-xs font-bold text-gray-700 dark:text-gray-300">مفعل ؟</th>
            <th v-if="isColumnVisible('operations')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-center text-xs font-bold text-gray-700 dark:text-gray-300">العمليات</th>
            <th v-if="isColumnVisible('actions')" class="border border-gray-200 dark:border-gray-800 px-4 py-3.5 text-center text-xs font-bold text-gray-700 dark:text-gray-300">الاجراءات</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr
            v-for="(user, index) in users"
            :key="user.id"
            class="hover:bg-gray-50/70 dark:hover:bg-gray-900/40 transition-colors"
          >
            <!-- Checkbox -->
            <td class="border border-gray-200 dark:border-gray-800 px-4 py-3 w-12 text-center align-middle">
              <input
                type="checkbox"
                :value="user.id"
                v-model="selectedUserIds"
                class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-800"
              />
            </td>
            <!-- Row index -->
            <td v-if="isColumnVisible('index')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 w-12 text-center align-middle text-sm font-semibold text-gray-800 dark:text-gray-200">
              {{ (currentPage - 1) * pageSize + index + 1 }}
            </td>
            <!-- First Name -->
            <td v-if="isColumnVisible('first_name')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 align-middle text-sm font-semibold text-gray-800 dark:text-gray-200">
              {{ splitName(user.display_name || user.full_name || user.username).first }}
            </td>
            <!-- Last Name -->
            <td v-if="isColumnVisible('last_name')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 align-middle text-sm font-semibold text-gray-800 dark:text-gray-200">
              {{ splitName(user.display_name || user.full_name || user.username).last }}
            </td>
            <!-- Username -->
            <td v-if="isColumnVisible('username')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 align-middle text-sm text-gray-600 dark:text-gray-300">
              {{ user.username }}
            </td>
            <!-- Email -->
            <td v-if="isColumnVisible('email')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 align-middle text-sm text-gray-600 dark:text-gray-300">
              {{ user.email || '—' }}
            </td>
            <!-- System Type -->
            <td v-if="isColumnVisible('system_type')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 align-middle text-sm text-gray-500 dark:text-gray-400">
              {{ user.is_staff ? 'نظام الإدارة' : 'نظام فرعي' }}
            </td>
            <!-- Groups/Roles -->
            <td v-if="isColumnVisible('groups')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 align-middle">
              <span
                v-if="user.role"
                class="inline-block rounded bg-gray-100 px-2.5 py-1 text-xs font-semibold text-gray-700 dark:bg-gray-800 dark:text-gray-300"
              >
                {{ user.role.name }}
              </span>
              <!-- Default group if no role is assigned to fill out layout dynamically -->
              <span
                v-else-if="!user.is_staff && user.is_active"
                class="inline-block rounded bg-gray-100 px-2.5 py-1 text-xs font-semibold text-gray-700 dark:bg-gray-800 dark:text-gray-300"
              >
                مجموعة موظفين
              </span>
              <span
                v-else-if="user.is_staff"
                class="inline-block rounded bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
              >
                مجموعة المدراء
              </span>
              <span v-else class="text-xs text-gray-400">—</span>
            </td>
            <!-- Is Active -->
            <td v-if="isColumnVisible('is_active')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 w-20 text-center align-middle">
              <!-- Green check if active, red cross if inactive -->
              <span
                v-if="user.is_active"
                class="inline-flex h-6 w-6 items-center justify-center rounded-full bg-green-50 text-green-600 dark:bg-green-500/10 dark:text-green-400"
                title="نشط"
              >
                <svg class="h-4.5 w-4.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
              </span>
              <span
                v-else
                class="inline-flex h-6 w-6 items-center justify-center rounded-full bg-red-50 text-red-600 dark:bg-red-500/10 dark:text-red-400"
                title="معطل"
              >
                <svg class="h-4.5 w-4.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </span>
            </td>
            <!-- Operations (العمليات) -->
            <td v-if="isColumnVisible('operations')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 w-36 text-center align-middle">
              <div class="flex items-center justify-center gap-1.5">
                <!-- Icon 1: الاعتماد (Toggle Staff / Admin status) -->
                <!-- Staff (Manager): Amber outline with user-check icon -->
                <button
                  v-if="user.is_staff"
                  @click="$emit('toggle-staff', user)"
                  class="table-btn table-btn-amber"
                  title="إلغاء الاعتماد كمدير"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="8.5" r="3" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 19v-1a4 4 0 014-4h4a4 4 0 014 4v1" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 11l1.5 1.5 2.5-2.5" />
                  </svg>
                </button>
                <!-- Non-Staff (Regular User): Green outline with user-cross icon -->
                <button
                  v-else
                  @click="$emit('toggle-staff', user)"
                  class="table-btn table-btn-green"
                  title="اعتماد كمدير"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="8.5" r="3" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 19v-1a4 4 0 014-4h4a4 4 0 014 4v1" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 9l4 4m0-4l-4 4" />
                  </svg>
                </button>

                <!-- Icon 2: إعادة ضبط كلمة السر -->
                <button
                  @click="$emit('reset-password', user)"
                  class="table-btn table-btn-gray"
                  title="إعادة ضبط كلمة السر"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <circle cx="16" cy="12" r="3" />
                    <circle cx="16" cy="12" r="0.5" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 12H6M9 12v3M6 12v3" />
                  </svg>
                </button>

                <!-- Icon 3: تفعيل/تعطيل الحساب -->
                <!-- Active: Blue outline with check-circle icon -->
                <button
                  v-if="user.is_active"
                  @click="$emit('deactivate', user)"
                  class="table-btn table-btn-blue"
                  title="تعطيل الحساب"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="9" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.5 12.5l2.5 2.5 5-5" />
                  </svg>
                </button>
                <!-- Inactive: Blue outline with close-circle icon -->
                <button
                  v-else
                  @click="$emit('activate', user)"
                  class="table-btn table-btn-blue"
                  title="تفعيل الحساب"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="9" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.5 9.5l5 5m0-5l-5 5" />
                  </svg>
                </button>
              </div>
            </td>
            <!-- Actions (الاجراءات) -->
            <td v-if="isColumnVisible('actions')" class="border border-gray-200 dark:border-gray-800 px-4 py-3 w-36 text-center align-middle">
              <div class="flex items-center justify-center gap-1.5">
                <!-- Edit (تعديل) -->
                <button
                  @click="$emit('edit', user)"
                  class="table-btn table-btn-green"
                  title="تعديل المستخدم"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>

                <!-- Delete (حذف) -->
                <button
                  @click="$emit('delete', user)"
                  class="table-btn table-btn-red"
                  title="حذف نهائي"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>

                <!-- View (رؤية) -->
                <RouterLink
                  :to="`/users/${user.id}`"
                  class="table-btn table-btn-blue"
                  title="تفاصيل الملف"
                >
                  <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </RouterLink>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

defineProps<{
  users: any[]
  loading: boolean
  error: string | null
  columns: any[]
  isColumnVisible: (key: string) => boolean
  splitName: (fullName: string) => { first: string, last: string }
  currentPage: number
  pageSize: number
}>()

defineEmits<{
  (e: 'toggle-select-all'): void
  (e: 'toggle-staff', user: any): void
  (e: 'reset-password', user: any): void
  (e: 'deactivate', user: any): void
  (e: 'activate', user: any): void
  (e: 'edit', user: any): void
  (e: 'delete', user: any): void
  (e: 'retry'): void
}>()

const selectedUserIds = defineModel<number[]>('selectedUserIds', { required: true })
const selectAll = defineModel<boolean>('selectAll', { required: true })
</script>

<style scoped>
.table-btn {
  display: flex;
  height: 2rem;
  width: 2rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  border-width: 1px;
  transition: all 0.15s ease-in-out;
  cursor: pointer;
}
.table-btn-blue {
  border-color: #2563eb;
  color: #2563eb;
  background-color: #ffffff;
}
.table-btn-blue:hover {
  background-color: #f8fafc;
}
:global(.dark) .table-btn-blue {
  background-color: transparent;
}
:global(.dark) .table-btn-blue:hover {
  background-color: rgba(37, 99, 235, 0.15);
}

.table-btn-blue-filled {
  background-color: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
}
.table-btn-blue-filled:hover {
  background-color: #1d4ed8;
}

.table-btn-green {
  border-color: #16a34a;
  color: #16a34a;
  background-color: #ffffff;
}
.table-btn-green:hover {
  background-color: #f0fdf4;
}
:global(.dark) .table-btn-green {
  background-color: transparent;
}
:global(.dark) .table-btn-green:hover {
  background-color: rgba(22, 163, 74, 0.15);
}

.table-btn-amber {
  border-color: #d97706;
  color: #d97706;
  background-color: #ffffff;
}
.table-btn-amber:hover {
  background-color: #fffbeb;
}
:global(.dark) .table-btn-amber {
  background-color: transparent;
}
:global(.dark) .table-btn-amber:hover {
  background-color: rgba(217, 119, 6, 0.15);
}

.table-btn-red {
  border-color: #dc2626;
  color: #dc2626;
  background-color: #ffffff;
}
.table-btn-red:hover {
  background-color: #fef2f2;
}
:global(.dark) .table-btn-red {
  background-color: transparent;
}
:global(.dark) .table-btn-red:hover {
  background-color: rgba(220, 38, 38, 0.15);
}

.table-btn-gray {
  border-color: #d1d5db;
  color: #6b7280;
  background-color: #ffffff;
}
.table-btn-gray:hover {
  background-color: #f9fafb;
}
:global(.dark) .table-btn-gray {
  border-color: #374151;
  color: #9ca3af;
  background-color: transparent;
}
:global(.dark) .table-btn-gray:hover {
  background-color: rgba(255, 255, 255, 0.05);
}
</style>
