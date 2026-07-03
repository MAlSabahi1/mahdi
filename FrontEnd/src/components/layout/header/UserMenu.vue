<template>
  <div class="relative" ref="dropdownRef">
    <button
      class="flex items-center text-gray-700 dark:text-gray-400"
      @click.prevent="toggleDropdown"
    >
      <span class="me-3 flex h-11 w-11 items-center justify-center overflow-hidden rounded-full border border-gray-200 dark:border-gray-800">
        <img :src="authStore.user?.profile_picture || '/images/user/owner.jpg'" alt="User" class="w-full h-full object-cover" />
      </span>

      <span class="block me-1 font-medium text-theme-sm">{{ displayName }}</span>

      <ChevronDownIcon :class="{ 'rotate-180': dropdownOpen }" />
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute end-0 mt-[17px] flex w-[260px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark z-50"
    >
      <div>
        <span class="block font-medium text-gray-700 text-theme-sm dark:text-gray-400">
          {{ authStore.user?.full_name || authStore.user?.username || '' }}
        </span>
        <span class="mt-0.5 block text-theme-xs text-gray-500 dark:text-gray-400">
          {{ authStore.user?.email || `@${authStore.user?.username}` }}
        </span>
      </div>

      <ul class="flex flex-col gap-1 pt-4 pb-3 border-b border-gray-200 dark:border-gray-800">
        <li>
          <RouterLink
            to="/profile"
            @click="closeDropdown"
            class="flex items-center gap-3 px-3 py-2 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
          >
            <UserCircleIcon class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300" />
            الملف الشخصي
          </RouterLink>
        </li>
      </ul>

      <div class="pt-3">
        <button
          @click="handleSignOut"
          class="flex w-full items-center gap-3 px-3 py-2 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
        >
          <LogoutIcon
            class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300"
          />
          تسجيل الخروج
        </button>
      </div>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup>
import { ChevronDownIcon, LogoutIcon, UserCircleIcon, SettingsIcon } from '@/icons'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const dropdownOpen = ref(false)
const dropdownRef = ref(null)

const displayName = computed(() => {
  return authStore.user?.display_name || authStore.user?.full_name || authStore.user?.username || 'مستخدم'
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleSignOut = async () => {
  closeDropdown()
  await authStore.logout()
  router.push('/signin')
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
