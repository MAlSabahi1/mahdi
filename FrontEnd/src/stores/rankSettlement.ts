import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface RankSettlement {
  id: string
  personnel: string
  personnel_name: string
  personnel_military_number: string
  settlement_type: string
  from_rank: number | null
  from_rank_name: string | null
  to_rank: number | null
  to_rank_name: string | null
  new_military_number: string | null
  decision_number: string | null
  decision_date: string | null
  supporting_document: number | null
  status: string
  requested_by_name: string | null
  applied_by_name: string | null
  applied_at: string | null
  rejection_reason: string | null
  notes: string | null
  created_at: string
}

export const useRankSettlementStore = defineStore('rankSettlement', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pendingSettlements = ref<RankSettlement[]>([])
  const totalCount = ref(0)
  const totalPages = ref(1)
  const currentPage = ref(1)

  async function fetchAllPendingSettlements(params: { page?: number } = {}) {
    loading.value = true
    error.value = null
    try {
      // By default fetch only pending
      const response = await api.get('/personnel/rank-settlements/', {
        params: { ...params, status: 'pending' }
      })
      pendingSettlements.value = response.data.results
      totalCount.value = response.data.count
      totalPages.value = Math.ceil(response.data.count / 10) || 1
      currentPage.value = params.page || 1
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحميل طلبات تسوية الرتب'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createSettlement(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/personnel/rank-settlements/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تقديم طلب التسوية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function applySettlement(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/personnel/rank-settlements/${id}/apply/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل اعتماد التسوية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function rejectSettlement(id: string, reason: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/personnel/rank-settlements/${id}/reject/`, {
        rejection_reason: reason
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل رفض التسوية'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    pendingSettlements,
    totalCount,
    totalPages,
    currentPage,
    fetchAllPendingSettlements,
    createSettlement,
    applySettlement,
    rejectSettlement
  }
})
