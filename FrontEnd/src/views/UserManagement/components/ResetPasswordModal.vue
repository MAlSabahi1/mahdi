<template>
  <div class="fixed inset-0 z-[99999] flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
    <div class="w-full max-w-md rounded-xl bg-white p-6 shadow-xl dark:bg-gray-900">
      <div class="mb-5 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white/90">إعادة تعيين كلمة المرور</h2>
        <button @click="$emit('close')" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <p class="mb-4 text-sm text-gray-500 dark:text-gray-400">
        إعادة تعيين كلمة مرور المستخدم <strong class="text-gray-800 dark:text-white/90">{{ user.display_name || user.username }}</strong>
      </p>

      <div v-if="error" class="mb-4 rounded-lg border border-error-300 bg-error-50 p-3 text-sm text-error-700 dark:border-error-500/30 dark:bg-error-500/10 dark:text-error-400">
        {{ error }}
      </div>

      <form @submit.prevent="handleReset" class="space-y-4">
        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
            كلمة المرور الجديدة <span class="text-error-500">*</span>
          </label>
          <input v-model="newPassword" type="password" required minlength="8"
            class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="8 حروف على الأقل" />
        </div>
        <div>
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
            تأكيد كلمة المرور <span class="text-error-500">*</span>
          </label>
          <input v-model="confirmPassword" type="password" required minlength="8"
            class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="أعد كتابة كلمة المرور" />
          <p v-if="confirmPassword && newPassword !== confirmPassword" class="mt-1 text-xs text-error-500">
            كلمتا المرور غير متطابقتين
          </p>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="$emit('close')"
            class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700">
            إلغاء
          </button>
          <button type="submit" :disabled="loading || !newPassword || newPassword !== confirmPassword"
            class="flex items-center gap-2 rounded-lg bg-warning-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-warning-600 disabled:opacity-50">
            <svg v-if="loading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            إعادة التعيين
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUsersStore } from '@/stores/users'

const props = defineProps({
  user: { type: Object, required: true },
})
const emit = defineEmits(['close', 'reset'])
const usersStore = useUsersStore()

const loading = ref(false)
const error = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

async function handleReset() {
  if (newPassword.value !== confirmPassword.value) return

  loading.value = true
  error.value = ''
  try {
    await usersStore.resetPassword(props.user.id, newPassword.value)
    emit('reset')
  } catch (err) {
    error.value = err.response?.data?.error || err.response?.data?.detail || 'فشل إعادة تعيين كلمة المرور'
  } finally {
    loading.value = false
  }
}
</script>
