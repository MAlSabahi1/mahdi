<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="إدارة الجلسات والأجهزة النشطة" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Top Premium Glassmorphic Header -->
      <div class="relative overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-white to-gray-50/50 dark:from-white/[0.03] dark:to-transparent p-6 shadow-theme-sm">
        <div class="absolute -right-16 -top-16 w-48 h-48 bg-brand-500/5 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-brand-500/10 text-brand-600 dark:text-brand-400 rounded-2xl shadow-theme-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">
                إدارة الجلسات والأجهزة النشطة
              </h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                متابعة الأجهزة المتصلة بالنظام حالياً، وحظر الوصول غير المصرح به، وإنهاء الجلسات حمايةً للبيانات.
              </p>
            </div>
          </div>
          
          <button 
            @click="loadMySessions"
            :disabled="loadingMySessions"
            class="flex items-center gap-2 border border-gray-200 bg-white hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-900 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-xl px-4 py-2 text-xs font-black transition-all cursor-pointer shadow-theme-xs"
          >
            <svg class="h-4 w-4" :class="{'animate-spin': loadingMySessions}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17" />
            </svg>
            تحديث الأجهزة
          </button>
        </div>
      </div>

      <!-- Current User Sessions Card -->
      <div class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 overflow-hidden">
        <div class="border-b border-gray-100 p-5 dark:border-gray-800 flex items-center justify-between">
          <div>
            <h3 class="text-base font-semibold text-gray-900 dark:text-white">جلساتك النشطة حالياً</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">قائمة بالأجهزة والمتصفحات المرتبطة بحسابك الشخصي حالياً.</p>
          </div>
        </div>

        <div class="p-6">
          <div v-if="loadingMySessions" class="flex justify-center py-12">
            <svg class="h-7 w-7 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
          </div>

          <div v-else-if="mySessions.length === 0" class="text-center py-12 text-gray-400 dark:text-gray-500">
            لا توجد جلسات نشطة مسجلة لحسابك.
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-250 dark:divide-gray-800 text-right">
              <thead class="bg-gray-50/50 dark:bg-gray-800/30">
                <tr>
                  <th class="px-5 py-3.5 text-sm font-semibold text-gray-700 dark:text-gray-300">الجهاز / المتصفح</th>
                  <th class="px-5 py-3.5 text-sm font-semibold text-gray-700 dark:text-gray-300">عنوان IP</th>
                  <th class="px-5 py-3.5 text-sm font-semibold text-gray-700 dark:text-gray-300">الموقع الجغرافي</th>
                  <th class="px-5 py-3.5 text-sm font-semibold text-gray-700 dark:text-gray-300">تاريخ بدء الاتصال</th>
                  <th class="px-5 py-3.5 text-sm font-semibold text-gray-700 dark:text-gray-300 text-left">التحكم</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-850">
                <tr 
                  v-for="session in mySessions" 
                  :key="session.session_id" 
                  class="hover:bg-gray-50/40 dark:hover:bg-gray-800/10 transition-colors"
                >
                  <td class="px-5 py-4">
                    <div class="flex items-center gap-3">
                      <div 
                        class="w-9 h-9 rounded-xl flex items-center justify-center border shrink-0"
                        :class="session.is_current ? 'bg-emerald-50 text-emerald-600 border-emerald-200/40 dark:bg-emerald-950/20 dark:text-emerald-400' : 'bg-gray-50 text-gray-500 border-gray-200/40 dark:bg-gray-800 dark:text-gray-400'"
                      >
                        <svg v-if="isMobile(session.user_agent)" xmlns="http://www.w3.org/2000/svg" class="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </div>
                      
                      <div>
                        <div class="font-extrabold text-gray-900 dark:text-white flex items-center gap-2">
                          <span>{{ parseUserAgent(session.user_agent) }}</span>
                          <span 
                            v-if="session.is_current" 
                            class="px-2 py-0.5 rounded-full text-[9px] bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 font-black border border-emerald-200/40 inline-flex items-center gap-1"
                          >
                            <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            الجلسة الحالية
                          </span>
                        </div>
                        <div class="text-[10px] text-gray-400 font-mono mt-0.5 truncate max-w-[280px] sm:max-w-[420px]" :title="session.user_agent">
                          {{ session.user_agent }}
                        </div>
                      </div>
                    </div>
                  </td>
                  
                  <td class="px-5 py-4 font-mono text-gray-650 dark:text-gray-300 text-xs">{{ session.ip_address || '—' }}</td>
                  <td class="px-5 py-4 text-gray-650 dark:text-gray-300 text-xs">{{ session.geo_location || 'غير محدد' }}</td>
                  <td class="px-5 py-4 text-gray-500 text-xs font-mono">{{ formatDate(session.created_at || session.timestamp) }}</td>
                  
                  <td class="px-5 py-4 text-left">
                    <button
                      v-if="!session.is_current"
                      @click="handleRevokeSession(session.session_id)"
                      class="text-[10px] font-black text-red-600 dark:text-red-400 bg-red-50 hover:bg-red-100 dark:bg-red-950/20 dark:hover:bg-red-950/40 border border-red-200/30 px-3.5 py-1.5 rounded-lg transition-all cursor-pointer inline-flex items-center gap-1 shadow-theme-xs"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                      </svg>
                      إنهاء الجلسة
                    </button>
                    <span v-else class="text-xs text-gray-400 font-medium px-4 py-1.5 block text-left">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Administrative Actions Card -->
      <div class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 overflow-hidden">
        <div class="border-b border-gray-100 p-5 dark:border-gray-800">
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">حوكمة وإنهاء جلسات مستخدمي النظام (إشراف عسكري)</h3>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">البحث عن حساب مستخدم وإلغاء كافة اتصالاته النشطة فوراً لإرغامه على تسجيل دخول جديد.</p>
        </div>

        <div class="p-6 space-y-6">
          <!-- Command bar search input -->
          <div class="flex flex-col sm:flex-row gap-3 max-w-xl">
            <div class="relative flex-1">
              <span class="absolute inset-y-0 start-0 flex items-center ps-3.5 text-gray-400 pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </span>
              <input
                type="text"
                v-model="searchQuery"
                placeholder="أدخل اسم المستخدم للبحث..."
                class="w-full ps-10 pe-4 py-2.5 text-xs border border-gray-200 dark:border-gray-800 rounded-xl bg-gray-50/50 dark:bg-gray-950 focus:bg-white focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 text-gray-900 dark:text-white transition-all text-right"
                @keyup.enter="handleSearch"
              />
            </div>
            <button
              @click="handleSearch"
              class="px-5 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-extrabold text-xs shadow-theme-xs transition-colors cursor-pointer"
            >
              بحث ومطابقة الحساب
            </button>
          </div>

          <!-- Search Results Table -->
          <div v-if="searching" class="flex justify-center py-10">
            <svg class="h-6 w-6 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
          </div>

          <div v-else-if="searched && searchResults.length === 0" class="text-center py-10 text-gray-400 dark:text-gray-500 text-xs">
            لم يتم العثور على أي حساب مستخدم يطابق معايير البحث المدخلة.
          </div>

          <div v-else-if="searchResults.length > 0" class="overflow-x-auto border border-gray-150 dark:border-gray-800 rounded-xl">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800 text-right text-xs">
              <thead class="bg-gray-50/50 dark:bg-gray-800/30">
                <tr>
                  <th class="px-5 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300">المستخدم</th>
                  <th class="px-5 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300">البريد الإلكتروني</th>
                  <th class="px-5 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300">حالة الحساب</th>
                  <th class="px-5 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300">آخر تسجيل دخول</th>
                  <th class="px-5 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300 text-left">الإجراء</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-850">
                <tr v-for="user in searchResults" :key="user.id" class="hover:bg-gray-50/40 dark:hover:bg-gray-800/10 transition-colors">
                  <td class="px-5 py-3.5">
                    <div class="font-extrabold text-gray-900 dark:text-white">{{ user.username }}</div>
                    <div class="text-[10px] text-gray-400 mt-0.5">{{ user.full_name || 'بدون اسم كامل' }}</div>
                  </td>
                  
                  <td class="px-5 py-3.5 text-gray-650 dark:text-gray-400 font-mono">{{ user.email || '—' }}</td>
                  
                  <td class="px-5 py-3.5">
                    <span 
                      class="px-2 py-0.5 rounded-full font-bold text-[9px] inline-flex items-center gap-1.5 border"
                      :class="user.is_active ? 'bg-success-50 text-success-700 border-success-200 dark:bg-success-950/20 dark:text-success-400 dark:border-success-500/20' : 'bg-gray-100 text-gray-600 border-gray-250/20 dark:bg-gray-800 dark:text-gray-400'"
                    >
                      <span class="h-1.5 w-1.5 rounded-full" :class="user.is_active ? 'bg-success-500' : 'bg-gray-400'"></span>
                      {{ user.is_active ? 'نشط' : 'معطل' }}
                    </span>
                  </td>
                  
                  <td class="px-5 py-3.5 text-gray-500 font-mono">{{ formatDate(user.last_login) }}</td>
                  
                  <td class="px-5 py-3.5 text-left">
                    <button
                      @click="handleTerminateAllSessions(user)"
                      class="text-[10px] font-black text-red-650 bg-red-50 hover:bg-red-100 dark:bg-red-950/20 dark:hover:bg-red-950/40 border border-red-200/30 px-3.5 py-1.5 rounded-lg transition-all cursor-pointer inline-flex items-center gap-1 shadow-theme-xs"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      إنهاء كافة الجلسات النشطة
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
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
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280'
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
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280'
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
