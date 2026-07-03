<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-3">
          <RouterLink to="/users" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
          </RouterLink>
          <div>
            <h1 class="text-xl font-bold text-gray-800 dark:text-white/90">
              {{ $t('users.user_details') }}
            </h1>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {{ user?.full_name || user?.username || $t('common.loading') }}
            </p>
          </div>
        </div>
        <div class="flex items-center gap-3" v-if="user">
          <button
            @click="terminateSessions"
            class="inline-flex items-center gap-2 rounded-lg bg-error-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-error-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
            </svg>
            {{ $t('users.terminate_sessions') || 'إنهاء جميع الجلسات' }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center p-12">
        <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <div v-else-if="user" class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Personal Info -->
        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 lg:col-span-1">
          <div class="flex flex-col items-center text-center">
            <div class="mb-4 h-24 w-24 overflow-hidden rounded-full border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <img v-if="user.profile_picture" :src="user.profile_picture" class="h-full w-full object-cover" />
              <span v-else class="text-2xl font-bold text-gray-500">{{ user.username.charAt(0).toUpperCase() }}</span>
            </div>
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{{ user.display_name || user.username }}</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400">@{{ user.username }}</p>
            
            <div class="mt-4 flex flex-wrap justify-center gap-2">
              <span
                :class="user.is_staff ? 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400' : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'"
                class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium"
              >
                {{ user.is_staff ? ($t('users.admin') || 'مدير نظام') : ($t('users.regular_user') || 'مستخدم عادي') }}
              </span>
              <span
                v-if="user.role"
                class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400"
              >
                {{ user.role.name }}
              </span>
            </div>
          </div>

          <div class="mt-8 space-y-4">
            <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-800">
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.email') }}</span>
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ user.email || '—' }}</span>
            </div>
            <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-800">
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.phone') }}</span>
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ user.phone || '—' }}</span>
            </div>
            <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-800">
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.status') }}</span>
              <span
                v-if="user.is_active"
                class="inline-flex items-center gap-1 rounded-full bg-success-50 px-2.5 py-0.5 text-xs font-medium text-success-700 dark:bg-success-500/10 dark:text-success-400"
              >
                {{ $t('users.active') }}
              </span>
              <span
                v-else
                class="inline-flex items-center gap-1 rounded-full bg-error-50 px-2.5 py-0.5 text-xs font-medium text-error-700 dark:bg-error-500/10 dark:text-error-400"
              >
                {{ $t('users.inactive') }}
              </span>
            </div>
            <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-800">
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.join_date') || 'تاريخ الانضمام' }}</span>
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ formatDate(user.created_at) }}</span>
            </div>
            <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-800">
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.last_login') || 'آخر ظهور' }}</span>
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ user.last_login ? formatDate(user.last_login) : ($t('users.never_logged_in') || 'لم يدخل بعد') }}</span>
            </div>
          </div>
        </div>

        <!-- Security & Sessions -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Security Stats -->
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
            <h3 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">الأمان</h3>
            <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <div class="rounded-lg bg-gray-50 p-4 dark:bg-gray-800/50">
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.failed_attempts') || 'محاولات فاشلة' }}</p>
                <p class="mt-1 text-xl font-bold text-gray-900 dark:text-white">{{ security.failed_login_attempts || 0 }}</p>
              </div>
              <div class="rounded-lg bg-gray-50 p-4 dark:bg-gray-800/50">
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('users.active_sessions') || 'الجلسات النشطة' }}</p>
                <p class="mt-1 text-xl font-bold text-gray-900 dark:text-white">{{ active_sessions_count || 0 }}</p>
              </div>
              <div class="rounded-lg bg-gray-50 p-4 dark:bg-gray-800/50">
                <p class="text-sm text-gray-500 dark:text-gray-400">تغيير المرور إجباري</p>
                <p class="mt-1 text-xl font-bold text-gray-900 dark:text-white">{{ security.must_change_password ? 'نعم' : 'لا' }}</p>
              </div>
              <div class="rounded-lg p-4" :class="security.is_locked ? 'bg-error-50 dark:bg-error-500/10' : 'bg-success-50 dark:bg-success-500/10'">
                <p class="text-sm" :class="security.is_locked ? 'text-error-600 dark:text-error-400' : 'text-success-600 dark:text-success-400'">الحالة الأمنية</p>
                <p class="mt-1 text-xl font-bold" :class="security.is_locked ? 'text-error-700 dark:text-error-500' : 'text-success-700 dark:text-success-500'">
                  {{ security.is_locked ? 'حساب مقفل' : 'آمن' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Sessions List -->
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
            <h3 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">{{ $t('users.active_devices') || 'الأجهزة النشطة' }}</h3>
            <div v-if="active_sessions.length === 0" class="py-6 text-center text-gray-500 dark:text-gray-400">
              {{ $t('users.no_active_sessions') || 'لا توجد جلسات نشطة حالياً.' }}
            </div>
            <div v-else class="space-y-4">
              <div v-for="session in active_sessions" :key="session.id" class="flex items-center justify-between rounded-lg border border-gray-100 p-4 dark:border-gray-800">
                <div class="flex items-start gap-4">
                  <div class="rounded-lg bg-gray-100 p-2 dark:bg-gray-800">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-medium text-gray-900 dark:text-white">{{ session.device_info || 'جهاز غير معروف' }}</h4>
                    <div class="mt-1 flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400">
                      <span>IP: {{ session.ip_address }}</span>
                      <span>•</span>
                      <span>آخر نشاط: {{ formatDate(session.last_activity) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const loading = ref(true)
const user = ref(null)
const security = ref({})
const active_sessions = ref([])
const active_sessions_count = ref(0)

const userId = route.params.id

async function loadUserDetails() {
  loading.value = true
  try {
    const res = await api.get(`/users/${userId}/`)
    user.value = res.data.data.user
    security.value = res.data.data.security
    active_sessions.value = res.data.data.active_sessions || []
    active_sessions_count.value = res.data.data.active_sessions_count
  } catch (error) {
    Swal.fire(t('common.error') || 'خطأ!', t('users.load_error') || 'فشل تحميل بيانات المستخدم', 'error')
    router.push('/users')
  } finally {
    loading.value = false
  }
}

async function terminateSessions() {
  const result = await Swal.fire({
    title: t('users.confirm_terminate_title') || 'تأكيد الإنهاء',
    text: t('users.confirm_terminate_text') || 'هل أنت متأكد من إنهاء جميع جلسات هذا المستخدم؟ سيتم تسجيل خروجه من جميع الأجهزة فوراً.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    confirmButtonText: t('users.confirm_terminate_yes') || 'نعم، إنهاء',
    cancelButtonText: t('common.cancel') || 'إلغاء'
  })

  if (result.isConfirmed) {
    try {
      await api.post(`/users/${userId}/terminate-sessions/`)
      Swal.fire(t('users.done') || 'تم!', t('users.terminate_success') || 'تم إنهاء جميع الجلسات بنجاح.', 'success')
      loadUserDetails() // Reload to reflect changes
    } catch (error) {
      Swal.fire(t('common.error') || 'خطأ!', t('users.terminate_error') || 'حدث خطأ أثناء إنهاء الجلسات.', 'error')
    }
  }
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

onMounted(() => {
  loadUserDetails()
})
</script>
