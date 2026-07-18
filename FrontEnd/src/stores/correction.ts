import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface CorrectionRequest {
  id: string
  military_number: string
  field: string
  old_value: string
  new_value: string
  reason: string
  status: 'pending' | 'approved' | 'rejected'
  requested_at: string
  approval_document_url?: string
}

export const useCorrectionStore = defineStore('correction', () => {
  const corrections = ref<CorrectionRequest[]>([])
  const loading = ref(false)

  // Fetch corrections for a specific person
  async function fetchCorrections(militaryNumber: string) {
    loading.value = true
    try {
      const response = await api.get(`/personnel/corrections/?personnel=${militaryNumber}`)
      const rawData = response.data.results || response.data || []
      corrections.value = rawData.map((item: any) => ({
        id: item.id,
        military_number: item.personnel_military_number || militaryNumber,
        field: item.field_name,
        old_value: item.old_value,
        new_value: item.new_value,
        reason: item.notes,
        status: item.status,
        requested_at: item.requested_at,
        approval_document_url: item.approval_document_url
      }))
      return corrections.value
    } catch (err) {
      console.error('Failed to fetch corrections:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  const totalPages = ref(1)
  const currentPage = ref(1)
  const totalItems = ref(0)

  // Fetch all pending corrections for admin/manager view
  async function fetchAllPendingCorrections(page = 1) {
    loading.value = true
    try {
      const response = await api.get(`/personnel/corrections/?status=pending&page=${page}`)
      const rawData = response.data.results || response.data || []
      
      if (response.data.count !== undefined) {
        totalItems.value = response.data.count
        totalPages.value = Math.ceil(response.data.count / 10) // Assuming 10 per page
        currentPage.value = page
      }

      const allCorrections = rawData.map((item: any) => ({
        id: item.id,
        military_number: item.personnel_military_number,
        personnel_name: item.personnel_name,
        personnel_rank: item.personnel_rank,
        field: item.field_name,
        old_value: item.old_value,
        new_value: item.new_value,
        reason: item.notes,
        status: item.status,
        requested_at: item.requested_at,
        requested_by_name: item.requested_by_name
      }))
      return allCorrections
    } catch (err) {
      console.error('Failed to fetch pending corrections:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  // Fetch a single correction by ID
  async function fetchCorrectionById(id: string) {
    loading.value = true
    try {
      const response = await api.get(`/personnel/corrections/${id}/`)
      return response.data
    } catch (err) {
      console.error('Failed to fetch correction by ID:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Submit a new correction
  async function submitCorrection(data: any) {
    loading.value = true
    try {
      let correctionType = 'data_correction'
      let fieldName = data.field

      if (data.field === 'name_correction') {
        correctionType = 'name_correction'
        fieldName = 'full_name'
      } else if (data.field === 'national_id_correction') {
        correctionType = 'national_id_correction'
        fieldName = 'national_id'
      } else if (data.field === 'military_number_correction') {
        correctionType = 'military_number_correction'
        fieldName = 'military_number'
      } else if (data.field === 'military_number_swap') {
        correctionType = 'military_number_swap'
        fieldName = 'military_number_swap'
      }

      const payload = {
        personnel_military_number_input: data.military_number,
        correction_type: correctionType,
        field_name: fieldName,
        old_value: data.old_value,
        new_value: data.new_value,
        notes: data.reason,
        supporting_document: data.document_ids?.length > 0 ? data.document_ids[0] : null
      }
      
      const response = await api.post('/personnel/corrections/', payload)
      const newRequest = response.data
      
      // Transform response to match frontend interface
      const mappedRequest: CorrectionRequest = {
        id: newRequest.id,
        military_number: data.military_number,
        field: newRequest.field_name,
        old_value: newRequest.old_value,
        new_value: newRequest.new_value,
        reason: newRequest.notes,
        status: newRequest.status,
        requested_at: newRequest.requested_at,
        approval_document_url: newRequest.approval_document_url
      }
      
      corrections.value.unshift(mappedRequest)
      return mappedRequest
    } catch (err) {
      console.error('Failed to submit correction:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Admin actions
  async function approveCorrection(id: string, approvalDocumentId: number) {
    try {
      await api.post(`/personnel/corrections/${id}/approve/`, {
        approval_document_id: approvalDocumentId
      })
      const req = corrections.value.find(c => String(c.id) === String(id))
      if (req) {
        req.status = 'approved'
      }
      return true
    } catch (err) {
      console.error('Failed to approve correction:', err)
      throw err
    }
  }

  async function rejectCorrection(id: string, reason: string) {
    try {
      await api.post(`/personnel/corrections/${id}/reject/`, { reason: reason })
      const req = corrections.value.find(c => String(c.id) === String(id))
      if (req) {
        req.status = 'rejected'
      }
      return true
    } catch (err) {
      console.error('Failed to reject correction:', err)
      throw err
    }
  }

  async function approveBatchCorrection(correctionIds: string[], memoDocumentId: string) {
    try {
      await api.post(`/personnel/corrections/approve_batch/`, {
        correction_ids: correctionIds,
        memo_document_id: memoDocumentId
      })
      // Update local state
      correctionIds.forEach(id => {
        const req = corrections.value.find(c => String(c.id) === String(id))
        if (req) {
          req.status = 'approved'
        }
      })
      return true
    } catch (err) {
      console.error('Failed to batch approve corrections:', err)
      throw err
    }
  }

  async function rejectBatchCorrection(correctionIds: string[], reason: string, clearName = false) {
    try {
      await api.post(`/personnel/corrections/reject_batch/`, {
        correction_ids: correctionIds,
        reason,
        clear_name: clearName
      })
      // Update local state
      correctionIds.forEach(id => {
        const req = corrections.value.find(c => String(c.id) === String(id))
        if (req) {
          req.status = 'rejected'
        }
      })
      return true
    } catch (err) {
      console.error('Failed to batch reject corrections:', err)
      throw err
    }
  }

  return {
    corrections,
    loading,
    totalPages,
    currentPage,
    totalItems,
    fetchCorrections,
    fetchAllPendingCorrections,
    fetchCorrectionById,
    submitCorrection,
    approveCorrection,
    rejectCorrection,
    approveBatchCorrection,
    rejectBatchCorrection
  }
})
