import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/lib/api'

export interface User {
  id: number
  username: string
  full_name: string
  display_name: string
  email: string
  phone: string
  is_active: boolean
  is_staff: boolean
  is_superuser?: boolean
  last_login: string | null
  profile_picture?: string | null
  bio?: string
  country?: string
  city?: string
  postal_code?: string
  tax_id?: string
  facebook_link?: string
  x_link?: string
  linkedin_link?: string
  instagram_link?: string
  authz_profile?: {
    role_id: number
    role_name: string
    role_code: string
    security_admin_id: number | null
    central_department_id: number | null
    branch_id: number | null
    district_police_id: number | null
    supervises_all: boolean
    supervised_security_admins: number[]
  } | null
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const sessionId = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.is_staff || user.value?.is_superuser || false)
  const displayName = computed(() => user.value?.display_name || user.value?.full_name || user.value?.username || '')

  // Initialize from localStorage
  function initFromStorage() {
    const storedToken = localStorage.getItem('access_token')
    const storedRefresh = localStorage.getItem('refresh_token')
    const storedSession = localStorage.getItem('session_id')
    const storedUser = localStorage.getItem('user')

    if (storedToken) accessToken.value = storedToken
    if (storedRefresh) refreshToken.value = storedRefresh
    if (storedSession) sessionId.value = storedSession
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch {
        user.value = null
      }
    }
  }

  // Login
  async function login(username: string, password: string) {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/login/', { username, password })
      const data = response.data.data

      accessToken.value = data.access_token
      refreshToken.value = data.refresh_token
      sessionId.value = data.session_id
      user.value = data.user

      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('session_id', data.session_id)
      localStorage.setItem('user', JSON.stringify(data.user))

      return { success: true, isSuspicious: data.is_suspicious }
    } catch (err: any) {
      const message = err.response?.data?.error || 'فشل تسجيل الدخول. تحقق من اسم المستخدم وكلمة المرور.'
      error.value = message
      throw new Error(message)
    } finally {
      loading.value = false
    }
  }

  // Logout
  async function logout() {
    try {
      if (accessToken.value) {
        await api.post('/auth/logout/', {
          refresh_token: refreshToken.value || '',
          session_id: sessionId.value || '',
        })
      }
    } catch {
      // تسجيل الخروج محلياً حتى لو فشل الطلب
    } finally {
      clearAuth()
    }
  }

  // Fetch current user
  async function fetchMe() {
    try {
      const response = await api.get('/auth/me/')
      user.value = response.data.data
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch {
      clearAuth()
    }
  }

  // Change password
  async function changePassword(oldPassword: string, newPassword: string, confirmPassword: string) {
    const response = await api.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    })
    return response.data
  }

  // Clear auth state
  function clearAuth() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    sessionId.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('session_id')
    localStorage.removeItem('user')
  }

  return {
    user,
    accessToken,
    refreshToken,
    sessionId,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    displayName,
    initFromStorage,
    login,
    logout,
    fetchMe,
    changePassword,
    clearAuth,
  }
})
