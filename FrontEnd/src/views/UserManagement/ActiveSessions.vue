<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="إدارة الجلسات والأجهزة النشطة" />

    <div class="space-y-6" dir="rtl">
      <!-- Info Header -->
      <div class="p-4 rounded-2xl bg-blue-500/10 border border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200 text-xs leading-relaxed">
        <strong>💡 حوكمة أمن الجلسات والأجهزة:</strong>
        تتيح لك هذه الصفحة التحكم الكامل في الأجهزة المتصلة بحسابك حالياً. يمكنك إنهاء أي جلسة غير معروفة فوراً لضمان عدم اختراق الحساب. كما يتيح لك القسم السفلي البحث عن أي مستخدم آخر وإنهاء كافة جلساته النشطة دفعة واحدة في حال وجود اشتباه أمني.
      </div>

      <!-- Current User Sessions -->
      <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm">
        <h3 class="text-sm font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
          أجهزتك وجلساتك النشطة حالياً
        </h3>

        <div v-if="loadingMySessions" class="flex justify-center py-8">
          <svg class="h-6 w-6 animate-spin text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>

        <div v-else-if="mySessions.length === 0" class="text-center py-8 text-gray-400">
          لا توجد جلسات نشطة مسجلة لحسابك.
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-right border-collapse">
            <thead>
              <tr class="border-b border-gray-100 dark:border-gray-800 text-xs font-bold text-gray-400">
                <th class="pb-3 text-start">الجهاز / المتصفح</th>
                <th class="pb-3">عنوان IP</th>
                <th class="pb-3">الموقع الجغرافي</th>
                <th class="pb-3">بدء الاتصال</th>
                <th class="pb-3 text-left">التحكم</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-850">
              <tr 
                v-for="session in mySessions" 
                :key="session.session_id" 
                class="text-xs hover:bg-gray-50/50 dark:hover:bg-gray-850/30 transition-colors"
              >
                <td class="py-4">
                  <div class="flex items-center gap-2.5">
                    <!-- Icon based on User Agent -->
                    <span class="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500">
                      <svg v-if="isMobile(session.user_agent)" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </span>
                    <div>
                      <div class="font-extrabold text-gray-900 dark:text-white flex items-center gap-1.5">
                        <span>{{ parseUserAgent(session.user_agent) }}</span>
                        <span v-if="session.is_current" class="px-2 py-0.5 rounded-full text-[9px] bg-green-500/10 text-green-600 font-black">الجلسة الحالية</span>
                      </div>
                      <div class="text-[10px] text-gray-400 font-mono mt-0.5 truncate max-w-[320px]">{{ session.user_agent }}</div>
                    </div>
                  </div>
                </td>
                <td class="py-4 font-mono text-gray-600 dark:text-gray-400">{{ session.ip_address || '—' }}</td>
                <td class="py-4 text-gray-600 dark:text-gray-400">{{ session.geo_location || 'غير معروف' }}</td>
                <td class="py-4 text-gray-500">{{ formatDate(session.created_at || session.timestamp) }}</td>
                <td class="py-4 text-left">
                  <button
                    v-if="!session.is_current"
                    @click="handleRevokeSession(session.session_id)"
                    class="text-[11px] font-bold text-red-600 dark:text-red-400 bg-red-500/10 hover:bg-red-500/20 px-3 py-1.5 rounded-xl transition-all cursor-pointer"
                  >
                    إنهاء الاتصال
                  </button>
                  <span v-else class="text-[11px] text-gray-400 font-bold px-3 py-1.5 block">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Administrative Actions: Manage Other Users' Sessions -->
      <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm">
        <h3 class="text-sm font-black text-gray-900 dark:text-white mb-2 flex items-center gap-2">
          <span class="p-1.5 rounded-lg bg-blue-500/10 text-blue-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </span>
          حوكمة وإنهاء جلسات مستخدمي النظام (إدارة إشرافية)
        </h3>
        <p class="text-[11px] text-gray-500 mb-4">
          البحث عن حساب مستخدم وإنهاء جميع جلساته وأجهزته النشطة فوراً لإرغامه على إعادة تسجيل الدخول.
        </p>

        <!-- Search Bar -->
        <div class="flex flex-col sm:flex-row gap-3 max-w-xl mb-6">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="ادخل اسم المستخدم أو جزء من اسمه للبحث..."
            class="flex-1 text-xs px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500/25 focus:border-blue-500 text-right"
            @keyup.enter="handleSearch"
          />
          <button
            @click="handleSearch"
            class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md shadow-blue-500/10 transition-all cursor-pointer"
          >
            بحث ومطابقة
          </button>
        </div>

        <!-- Search Results -->
        <div v-if="searching" class="flex justify-center py-6">
          <svg class="h-6 w-6 animate-spin text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>

        <div v-else-if="searched && searchResults.length === 0" class="text-center py-6 text-gray-400 text-xs">
          لم يتم العثور على أي مستخدم يطابق معايير البحث.
        </div>

        <div v-else-if="searchResults.length > 0" class="overflow-x-auto">
          <table class="w-full text-right border-collapse">
            <thead>
              <tr class="border-b border-gray-100 dark:border-gray-800 text-xs font-bold text-gray-400">
                <th class="pb-2 text-start">المستخدم</th>
                <th class="pb-2">البريد الإلكتروني</th>
                <th class="pb-2">حالة الحساب</th>
                <th class="pb-2">آخر تسجيل دخول</th>
                <th class="pb-2 text-left">التحكم</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-850">
              <tr v-for="user in searchResults" :key="user.id" class="text-xs">
                <td class="py-3">
                  <div class="font-extrabold text-gray-900 dark:text-white">{{ user.username }}</div>
                  <div class="text-[10px] text-gray-500">{{ user.full_name || '—' }}</div>
                </td>
                <td class="py-3 text-gray-600 dark:text-gray-400 font-mono">{{ user.email || '—' }}</td>
                <td class="py-3">
                  <span v-if="user.is_active" class="inline-flex items-center gap-1 rounded-full bg-success-50 px-2 py-0.5 text-[10px] font-medium text-success-700 dark:bg-success-500/10 dark:text-success-400">
                    نشط
                  </span>
                  <span v-else class="inline-flex items-center gap-1 rounded-full bg-error-50 px-2 py-0.5 text-[10px] font-medium text-error-700 dark:bg-error-500/10 dark:text-error-400">
                    معطل
                  </span>
                </td>
                <td class="py-3 text-gray-500 font-mono">{{ formatDate(user.last_login) }}</td>
                <td class="py-3 text-left">
                  <button
                    @click="handleTerminateAllSessions(user)"
                    class="text-[11px] font-black text-red-600 dark:text-red-400 bg-red-500/10 hover:bg-red-500/20 px-3 py-1.5 rounded-xl transition-all cursor-pointer"
                  >
                    إنهاء كافة جلسات هذا الحساب
                  </button>
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
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import api from '@/lib/api'
import Swal from 'sweetalert2'

interface UserSession {
  session_id: string
  user_agent: string
  ip_address: string
  geo_location: string
  created_at?: string
  timestamp?: string
  is_current: boolean
}

interface UserRecord {
  id: number
  username: string
  full_name: string
  email: string
  is_active: boolean
  last_login: string | null
}

const loadingMySessions = ref(false)
const mySessions = ref<UserSession[]>([])

const searchQuery = ref('')
const searching = ref(false)
const searched = ref(false)
const searchResults = ref<UserRecord[]>([])

async function loadMySessions() {
  loadingMySessions.value = true
  try {
    const res = await api.get('/sessions/')
    mySessions.value = res.data.data || []
  } catch (err) {
    console.error('Failed to load my sessions:', err)
  } finally {
    loadingMySessions.value = false
  }
}

async function handleRevokeSession(sessionId: string) {
  const result = await Swal.fire({
    title: 'تأكيد تسجيل الخروج',
    text: 'هل أنت متأكد من رغبتك في تسجيل الخروج من هذا الجهاز؟',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'نعم، قم بإنهاء الجلسة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444'
  })

  if (result.isConfirmed) {
    try {
      await api.post('/sessions/terminate/', { session_id: sessionId })
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'تم إنهاء الجلسة بنجاح',
        showConfirmButton: false,
        timer: 3000
      })
      await loadMySessions()
    } catch (err) {
      Swal.fire('خطأ', 'فشل إلغاء الجلسة', 'error')
    }
  }
}

async function handleSearch() {
  if (!searchQuery.value.trim()) return
  searching.value = true
  searched.value = true
  try {
    const res = await api.get('/users/', { params: { search: searchQuery.value } })
    searchResults.value = res.data.results || []
  } catch (err) {
    console.error('Failed to search users:', err)
  } finally {
    searching.value = false
  }
}

async function handleTerminateAllSessions(user: UserRecord) {
  const result = await Swal.fire({
    title: 'تأكيد تصفير جلسات المستخدم',
    text: `هل أنت متأكد من إنهاء كافة الاتصالات والجلسات النشطة للمستخدم "${user.username}"؟ سيتم إخراجه فوراً من جميع الأجهزة المتصلة.`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'نعم، تصفير الجلسات وإخراج المستخدم',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444'
  })

  if (result.isConfirmed) {
    try {
      await api.post(`/users/${user.id}/terminate-sessions/`)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: `تم إنهاء جميع جلسات المستخدم ${user.username} بنجاح`,
        showConfirmButton: false,
        timer: 3000
      })
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'فشل إنهاء جلسات المستخدم'
      Swal.fire('خطأ', errorMsg, 'error')
    }
  }
}

function parseUserAgent(userAgent: string): string {
  if (!userAgent) return 'جهاز غير معروف'
  const ua = userAgent.toLowerCase()
  let os = 'نظام تشغيل غير معروف'
  let browser = 'متصفح غير معروف'

  if (ua.includes('windows')) os = 'Windows'
  else if (ua.includes('macintosh') || ua.includes('mac os')) os = 'macOS'
  else if (ua.includes('linux')) os = 'Linux'
  else if (ua.includes('android')) os = 'Android'
  else if (ua.includes('iphone') || ua.includes('ipad')) os = 'iOS'

  if (ua.includes('chrome')) browser = 'Chrome'
  else if (ua.includes('firefox')) browser = 'Firefox'
  else if (ua.includes('safari')) browser = 'Safari'
  else if (ua.includes('edge')) browser = 'Edge'

  return `${browser} (${os})`
}

function isMobile(userAgent: string): boolean {
  if (!userAgent) return false
  const ua = userAgent.toLowerCase()
  return ua.includes('android') || ua.includes('iphone') || ua.includes('ipad')
}

function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleString('ar-YE', {
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

onMounted(() => {
  loadMySessions()
})
</script>
