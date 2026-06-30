import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface AuditLog {
  id: number
  action: string
  model_name: string
  object_id: string
  severity: string
  username: string
  module: string
  timestamp: string
  ip_address: string
  change_reason: string
  is_verified: boolean
  old_data?: any
  new_data?: any
}

export interface LoginAudit {
  id: number
  action: string
  username_attempted: string
  ip_address: string
  user_agent: string
  geo_location: string
  failure_reason: string
  timestamp: string
}

export const useAuditStore = defineStore('audit', () => {
  const systemLogs = ref<AuditLog[]>([])
  const loginLogs = ref<LoginAudit[]>([])
  const stats = ref<any>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const totalSystemLogs = ref(0)
  const totalLoginLogs = ref(0)
  
  // Pagination
  const systemLogsPage = ref(1)
  const systemLogsTotalPages = ref(1)
  const loginLogsPage = ref(1)
  const loginLogsTotalPages = ref(1)

  const fetchSystemLogs = async (params: any = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/audit/logs/', { params: { ...params, page: systemLogsPage.value } })
      if (response.data.results) {
         systemLogs.value = response.data.results
         totalSystemLogs.value = response.data.count
         systemLogsTotalPages.value = Math.ceil(response.data.count / 50) || 1
      }
    } catch (err: any) {
      error.value = 'فشل تحميل سجلات التدقيق'
    } finally {
      loading.value = false
    }
  }

  const fetchLoginLogs = async (params: any = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/audit/logins/', { params: { ...params, page: loginLogsPage.value } })
      if (response.data.results) {
         loginLogs.value = response.data.results
         totalLoginLogs.value = response.data.count
         loginLogsTotalPages.value = Math.ceil(response.data.count / 50) || 1
      }
    } catch (err: any) {
      error.value = 'فشل تحميل سجلات الدخول'
    } finally {
      loading.value = false
    }
  }

  const fetchStats = async () => {
    try {
      const response = await api.get('/audit/logs/stats/')
      stats.value = response.data.data
    } catch (err) {
      console.error('Failed to fetch stats', err)
    }
  }

  const verifySignature = async (id: number) => {
    const response = await api.post(`/audit/logs/${id}/verify/`)
    return response.data
  }

  const getLogDetails = async (id: number) => {
    const response = await api.get(`/audit/logs/${id}/`)
    return response.data.data
  }

  return {
    systemLogs,
    loginLogs,
    stats,
    loading,
    error,
    totalSystemLogs,
    totalLoginLogs,
    systemLogsPage,
    systemLogsTotalPages,
    loginLogsPage,
    loginLogsTotalPages,
    fetchSystemLogs,
    fetchLoginLogs,
    fetchStats,
    verifySignature,
    getLogDetails,
  }
})
