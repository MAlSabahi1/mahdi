import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface PermissionItem {
  id: number
  code: string
  action: string
  label: string
  scope: string
}

export interface ScreenPermissions {
  view: PermissionItem[]
  create: PermissionItem[]
  edit: PermissionItem[]
  delete: PermissionItem[]
  approve: PermissionItem[]
  export: PermissionItem[]
  manage: PermissionItem[]
  execute: PermissionItem[]
  import: PermissionItem[]
  custom: PermissionItem[]
}

export interface Screen {
  name: string
  label: string
  permissions: ScreenPermissions
}

export interface Role {
  id: number
  name: string
  code: string
  description: string
  permissions: string[]
  is_active: boolean
  is_system_role: boolean
  users_count: number
  created_at: string
  updated_at: string
}

export const useRolesStore = defineStore('roles', () => {
  const roles = ref<Role[]>([])
  const screens = ref<Screen[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchRoles() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/roles/')
      roles.value = response.data.results
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحميل المجموعات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchPermissionsMatrix() {
    try {
      const response = await api.get('/permissions/matrix/')
      screens.value = response.data.screens
    } catch (err: any) {
      console.error('Failed to fetch permissions matrix:', err)
    }
  }

  async function createRole(payload: { name: string; code: string; description: string; permissions: string[] }) {
    const response = await api.post('/roles/', payload)
    await fetchRoles()
    return response.data
  }

  async function updateRole(id: number, payload: { name?: string; description?: string; is_active?: boolean; permissions?: string[] }) {
    const response = await api.put(`/roles/${id}/`, payload)
    await fetchRoles()
    return response.data
  }

  async function deleteRole(id: number) {
    await api.delete(`/roles/${id}/`)
    await fetchRoles()
  }

  return {
    roles,
    screens,
    loading,
    error,
    fetchRoles,
    fetchPermissionsMatrix,
    createRole,
    updateRole,
    deleteRole,
  }
})
