<template>
  <div class="fixed inset-0 z-[99999] flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
    <div class="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl dark:bg-gray-900">
      <div class="mb-5 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white/90">تعديل المستخدم</h2>
        <button @click="$emit('close')" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div v-if="error" class="mb-4 rounded-lg border border-error-300 bg-error-50 p-3 text-sm text-error-700 dark:border-error-500/30 dark:bg-error-500/10 dark:text-error-400">
        {{ error }}
      </div>

      <form @submit.prevent="handleUpdate" class="space-y-4">
        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">اسم المستخدم</label>
          <input :value="user.username" type="text" disabled
            class="h-11 w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-not-allowed" />
        </div>
        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الاسم الكامل</label>
          <input v-model="form.full_name" v-field-error="'full_name'" type="text"
            class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="الاسم الكامل" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">البريد الإلكتروني</label>
            <input v-model="form.email" v-field-error="'email'" type="email"
              class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="email@example.com" />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">رقم الهاتف</label>
            <input v-model="form.phone" v-field-error="'phone'" type="text"
              class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="رقم الهاتف" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div class="flex flex-col gap-4">
            <div class="flex items-center gap-3">
              <label class="relative inline-flex cursor-pointer items-center">
                <input v-model="form.is_staff" :disabled="user.id === authStore.user?.id" v-field-error="'is_staff'" type="checkbox" class="peer sr-only" />
                <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-brand-500 peer-checked:after:translate-x-full peer-checked:after:border-white dark:border-gray-700 dark:bg-gray-700 rtl:peer-checked:after:-translate-x-full peer-disabled:opacity-50"></div>
              </label>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-400" :class="{'opacity-50': user.id === authStore.user?.id}">صلاحية مدير</span>
            </div>
            <div class="flex items-center gap-3">
              <label class="relative inline-flex cursor-pointer items-center">
                <input v-model="form.is_active" :disabled="user.id === authStore.user?.id" v-field-error="'is_active'" type="checkbox" class="peer sr-only" />
                <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-success-500 peer-checked:after:translate-x-full peer-checked:after:border-white dark:border-gray-700 dark:bg-gray-700 rtl:peer-checked:after:-translate-x-full peer-disabled:opacity-50"></div>
              </label>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-400" :class="{'opacity-50': user.id === authStore.user?.id}">حساب نشط</span>
            </div>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              الدور (الصلاحيات)
            </label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.role_id" v-field-error="'role_id'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">بدون دور</option>
                <option v-for="role in usersStore.availableRoles" :key="role.id" :value="role.id">
                  {{ role.name }}
                </option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </span>
            </div>
            <p v-if="usersStore.availableRoles.length === 0" class="mt-1 text-xs text-gray-500 dark:text-gray-400">لا توجد أدوار.</p>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="$emit('close')"
            class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700">
            إلغاء
          </button>
          <button type="submit" :disabled="loading"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 disabled:opacity-50">
            <svg v-if="loading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            حفظ التغييرات
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUsersStore } from '@/stores/users'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  user: { type: Object, required: true },
})
const emit = defineEmits(['close', 'updated'])
const usersStore = useUsersStore()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')
const form = reactive({
  full_name: props.user.full_name || '',
  email: props.user.email || '',
  phone: props.user.phone || '',
  is_staff: props.user.is_staff || false,
  is_active: props.user.is_active ?? true,
  role_id: props.user.role?.id || null,
})

async function handleUpdate() {
  loading.value = true
  error.value = ''
  try {
    await usersStore.updateUser(props.user.id, form)
    emit('updated')
  } catch (err) {
    error.value = err.response?.data?.error || err.response?.data?.detail || 'فشل تحديث المستخدم'
  } finally {
    loading.value = false
  }
}
</script>
