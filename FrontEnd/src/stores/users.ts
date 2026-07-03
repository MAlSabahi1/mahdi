import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface UserRecord {
  id: number
  username: string
  full_name: string
  display_name: string
  email: string
  phone: string
  is_active: boolean
  is_staff: boolean
  last_login: string | null
  created_at: string
  updated_at: string
  role: { id: number; name: string; code: string } | null
  security_status: {
    is_locked: boolean
    failed_attempts: number
    must_change_password: boolean
  }
}

export interface CreateUserPayload {
  username: string
  password: string
  full_name?: string
  email?: string
  phone?: string
  is_staff?: boolean
  role_id?: number | null
}

export interface UpdateUserPayload {
  full_name?: string
  email?: string
  phone?: string
  is_active?: boolean
  is_staff?: boolean
  role_id?: number | null
}

export const useUsersStore = defineStore('users', () => {
  const users = ref<UserRecord[]>([])
  const availableRoles = ref<{ id: number; name: string; code: string }[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const totalCount = ref(0)
  const totalPages = ref(1)
  const currentPage = ref(1)

  async function fetchUsers(search?: string, isActive?: boolean | null, page: number = 1) {
    loading.value = true
    error.value = null

    try {
      const params: Record<string, string> = {}
      if (search) params.search = search
      if (isActive !== null && isActive !== undefined) {
        params.is_active = String(isActive)
      }
      if (page) {
        params.page = String(page)
      }

      const response = await api.get('/users/', { params })
      users.value = response.data.results
      totalCount.value = response.data.count
      
      // DRF PageNumberPagination might return links (next/previous) 
      // We'll calculate totalPages from count and PAGE_SIZE (10)
      totalPages.value = Math.ceil(response.data.count / 10) || 1
      currentPage.value = page || 1
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحميل المستخدمين'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchRoles() {
    try {
      const response = await api.get('/roles/')
      availableRoles.value = response.data.results
    } catch (err: any) {
      console.error('Failed to fetch roles:', err)
    }
  }

  async function createUser(payload: CreateUserPayload) {
    const response = await api.post('/users/', payload)
    await fetchUsers()
    return response.data
  }

  async function updateUser(userId: number, payload: UpdateUserPayload) {
    const response = await api.put(`/users/${userId}/`, payload)
    await fetchUsers()
    return response.data
  }

  async function deactivateUser(userId: number) {
    const response = await api.delete(`/users/${userId}/`)
    await fetchUsers()
    return response.data
  }

  async function activateUser(userId: number) {
    const response = await api.post(`/users/${userId}/activate/`)
    await fetchUsers()
    return response.data
  }

  async function resetPassword(userId: number, newPassword: string) {
    const response = await api.post(`/users/${userId}/reset-password/`, {
      new_password: newPassword,
    })
    return response.data
  }

  async function unlockUser(userId: number) {
    const response = await api.post(`/users/${userId}/unlock/`)
    await fetchUsers()
    return response.data
  }

  return {
    users,
    availableRoles,
    loading,
    error,
    totalCount,
    totalPages,
    currentPage,
    fetchUsers,
    fetchRoles,
    createUser,
    updateUser,
    deactivateUser,
    activateUser,
    resetPassword,
    unlockUser,
  }
})
