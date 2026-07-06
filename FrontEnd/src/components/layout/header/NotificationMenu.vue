<template>
  <div class="relative" ref="dropdownRef">
    <button
      class="relative flex items-center justify-center text-gray-500 transition-colors bg-white border border-gray-200 rounded-full hover:text-dark-900 h-11 w-11 hover:bg-gray-100 hover:text-gray-700 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-white"
      @click="toggleDropdown"
    >
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -end-1 z-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white ring-2 ring-white dark:ring-gray-900"
      >
        {{ unreadCount }}
      </span>
      <span
        v-else-if="notifying"
        class="absolute end-0 top-0.5 z-1 h-2 w-2 rounded-full bg-orange-400"
      >
        <span
          class="absolute inline-flex w-full h-full bg-orange-400 rounded-full opacity-75 -z-1 animate-ping"
        ></span>
      </span>
      <svg
        class="fill-current"
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M10.75 2.29248C10.75 1.87827 10.4143 1.54248 10 1.54248C9.58583 1.54248 9.25004 1.87827 9.25004 2.29248V2.83613C6.08266 3.20733 3.62504 5.9004 3.62504 9.16748V14.4591H3.33337C2.91916 14.4591 2.58337 14.7949 2.58337 15.2091C2.58337 15.6234 2.91916 15.9591 3.33337 15.9591H4.37504H15.625H16.6667C17.0809 15.9591 17.4167 15.6234 17.4167 15.2091C17.4167 14.7949 17.0809 14.4591 16.6667 14.4591H16.375V9.16748C16.375 5.9004 13.9174 3.20733 10.75 2.83613V2.29248ZM14.875 14.4591V9.16748C14.875 6.47509 12.6924 4.29248 10 4.29248C7.30765 4.29248 5.12504 6.47509 5.12504 9.16748V14.4591H14.875ZM8.00004 17.7085C8.00004 18.1228 8.33583 18.4585 8.75004 18.4585H11.25C11.6643 18.4585 12 18.1228 12 17.7085C12 17.2943 11.6643 16.9585 11.25 16.9585H8.75004C8.33583 16.9585 8.00004 17.2943 8.00004 17.7085Z"
          fill=""
        />
      </svg>
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute -end-[240px] mt-[17px] flex h-[480px] w-[350px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark sm:w-[361px] lg:end-0"
    >
      <div
        class="flex items-center justify-between pb-3 mb-3 border-b border-gray-100 dark:border-gray-800"
      >
        <h5 class="text-lg font-semibold text-gray-800 dark:text-white/90">الإشعارات</h5>

        <button @click="closeDropdown" class="text-gray-500 dark:text-gray-400">
          <svg
            class="fill-current"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M6.21967 7.28131C5.92678 6.98841 5.92678 6.51354 6.21967 6.22065C6.51256 5.92775 6.98744 5.92775 7.28033 6.22065L11.999 10.9393L16.7176 6.22078C17.0105 5.92789 17.4854 5.92788 17.7782 6.22078C18.0711 6.51367 18.0711 6.98855 17.7782 7.28144L13.0597 12L17.7782 16.7186C18.0711 17.0115 18.0711 17.4863 17.7782 17.7792C17.4854 18.0721 17.0105 18.0721 16.7176 17.7792L11.999 13.0607L7.28033 17.7794C6.98744 18.0722 6.51256 18.0722 6.21967 17.7794C5.92678 17.4865 5.92678 17.0116 6.21967 16.7187L10.9384 12L6.21967 7.28131Z"
              fill=""
            />
          </svg>
        </button>
      </div>

      <ul class="flex flex-col h-[320px] overflow-y-auto custom-scrollbar divide-y divide-gray-100 dark:divide-gray-800">
        <li v-if="notifications.length === 0" class="p-6 text-center text-gray-400 text-sm">
          لا توجد إشعارات جديدة
        </li>
        <li v-for="notification in notifications" :key="notification.id" @click="handleItemClick(notification)">
          <a
            class="flex gap-3 p-3 hover:bg-gray-50 dark:hover:bg-white/5 cursor-pointer transition duration-150 rounded-lg"
            :class="{ 'bg-blue-50/40 dark:bg-blue-900/10': !notification.is_read }"
          >
            <!-- Priority Icon Indicator -->
            <span class="flex items-center justify-center w-8 h-8 rounded-full z-1 max-w-8"
              :class="{
                'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400': notification.priority === 'high' || notification.priority === 'urgent',
                'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400': notification.priority === 'normal',
                'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400': notification.priority === 'low'
              }"
            >
              <svg v-if="notification.priority === 'high' || notification.priority === 'urgent'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </span>

            <span class="block flex-1 min-w-0 text-right">
              <span class="block text-sm font-semibold text-gray-800 dark:text-white/90 truncate">
                {{ notification.title }}
              </span>
              <span class="block text-xs text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">
                {{ notification.message }}
              </span>
              <span class="flex items-center justify-start gap-1.5 text-[10px] text-gray-400 mt-1">
                <span>بواسطة: {{ notification.triggered_by_name || 'النظام' }}</span>
                <span>•</span>
                <span>{{ formatDate(notification.created_at) }}</span>
              </span>
            </span>
          </a>
        </li>
      </ul>

      <button
        class="mt-3 flex justify-center rounded-lg border border-gray-300 bg-white p-3 text-theme-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
        @click="handleViewAllClick"
      >
        إخفاء النافذة
      </button>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/api'

const router = useRouter()
const dropdownOpen = ref(false)
const notifying = ref(false)
const dropdownRef = ref(null)

const notifications = ref<any[]>([])
const unreadCount = ref(0)
let pollInterval: any = null

async function fetchNotifications() {
  try {
    const res = await api.get('/dictionaries/notifications/')
    notifications.value = res.data.results || res.data || []
    
    const countRes = await api.get('/dictionaries/notifications/unread-count/')
    unreadCount.value = countRes.data.unread_count || 0
    notifying.value = unreadCount.value > 0
  } catch (err) {
    console.error('Failed to fetch notifications:', err)
  }
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) {
    fetchNotifications()
  }
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleClickOutside = (event: any) => {
  if (dropdownRef.value && !(dropdownRef.value as any).contains(event.target)) {
    closeDropdown()
  }
}

const handleItemClick = async (notification: any) => {
  try {
    if (!notification.is_read) {
      await api.post(`/dictionaries/notifications/${notification.id}/mark-read/`)
    }
    closeDropdown()
    fetchNotifications()
    
    if (notification.action_url) {
      router.push(notification.action_url)
    }
  } catch (err) {
    console.error('Error handling notification click:', err)
  }
}

const handleViewAllClick = (event: any) => {
  event.preventDefault()
  closeDropdown()
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-YE', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  fetchNotifications()
  pollInterval = setInterval(fetchNotifications, 30000) // Poll every 30s
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (pollInterval) clearInterval(pollInterval)
})
</script>
