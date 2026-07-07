import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface DisciplinaryAction {
  id: string
  personnel: string
  personnel_name: string
  personnel_military_number: string
  action_type: string
  action_type_display: string
  source_type: string
  source_type_display: string
  issued_by_name: string
  decision_ref: string
  issued_date: string
  effective_date: string
  duration_days: number | null
  description: string
  status: string
  status_display: string
  ministry_notified: boolean
  notes: string
  created_at: string
}

export const useDisciplinaryStore = defineStore('disciplinary', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const actions = ref<DisciplinaryAction[]>([])
  const totalCount = ref(0)
  const totalPages = ref(1)
  const currentPage = ref(1)

  async function fetchActions(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/service-cycle/disciplinary/actions/', { params })
      actions.value = response.data.results || response.data || []
      totalCount.value = response.data.count || actions.value.length
      totalPages.value = Math.ceil(totalCount.value / 10) || 1
      currentPage.value = params.page || 1
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحميل الجزاءات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createAction(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/service-cycle/disciplinary/actions/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء الجزاء'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function approveAction(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/disciplinary/actions/${id}/execute/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تنفيذ الجزاء'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function cancelAction(id: string, reason: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/disciplinary/actions/${id}/cancel/`, {
        cancellation_reason: reason
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إلغاء الجزاء'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Absence Records
  async function fetchAbsenceRecords(params: any = {}) {
    loading.value = true
    try {
      const response = await api.get('/services/absence-records/', { params })
      return response.data.results || response.data || []
    } catch (err: any) {
      console.error('Failed to fetch absence records:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  async function createAbsenceRecord(data: any) {
    loading.value = true
    try {
      const response = await api.post('/services/absence-records/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تسجيل بلاغ الغياب'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    actions,
    totalCount,
    totalPages,
    currentPage,
    fetchActions,
    createAction,
    approveAction,
    cancelAction,
    fetchAbsenceRecords,
    createAbsenceRecord
  }
})
