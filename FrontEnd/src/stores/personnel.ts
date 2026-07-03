import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface PersonnelRecord {
  military_number: string
  old_military_number: string | null
  military_number_type: any
  full_name: string
  national_id: string | null
  national_id_status: string
  national_id_status_display: string
  
  current_rank: number | null
  rank_name: string | null
  pending_rank: number | null
  pending_rank_name: string | null
  
  current_status: number | null
  status_name: string | null
  status_classification: string | null
  
  security_admin: number | null
  security_admin_name: string | null
  central_department: number | null
  central_department_name: string | null
  branch: number | null
  branch_name: string | null
  district_police: number | null
  district_police_name: string | null
  division: number | null
  division_name: string | null
  unit: number | null
  unit_name: string | null
  
  category: number | null
  category_name: string | null
  job_title: number | null
  job_title_name: string | null
  position: number | null
  position_name: string | null
  
  force_classification: number | null
  force_classification_name: string | null
  qualification: number | null
  qualification_name: string | null
  
  phone_number: string | null
  birth_date: string | null
  join_date: string | null
  
  expense_status: string | null
  appointment_info: string | null
  notes: string | null
  
  is_complete: boolean
  is_data_clean: boolean
  data_quality_score: number
  has_pending_correction: boolean
  
  updated_at: string
}

export const usePersonnelStore = defineStore('personnel', () => {
  const records = ref<PersonnelRecord[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const totalCount = ref(0)
  const totalPages = ref(1)
  const currentPage = ref(1)

  async function fetchPersonnel(params: {
    search?: string
    page?: number
    current_status?: string | number
    current_rank?: string | number
    governorate?: string | number
  } = {}) {
    loading.value = true
    error.value = null

    try {
      const response = await api.get('/personnel/', { params })
      records.value = response.data.results
      totalCount.value = response.data.count
      
      totalPages.value = Math.ceil(response.data.count / 10) || 1
      currentPage.value = params.page || 1
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحميل بيانات الأفراد'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function checkNationalId(value: string) {
    try {
      const response = await api.get('/personnel/check-national-id/', {
        params: { value }
      })
      return response.data
    } catch (err: any) {
      console.error('Failed to check national ID:', err)
      return { valid_format: false, exists: false }
    }
  }

  async function createPersonnel(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/personnel/', data)
      return response.data
    } catch (err: any) {
      if (err.response?.data?.error?.detail) {
        const details = err.response.data.error.detail
        error.value = Object.entries(details).map(([k, v]) => `${k}: ${(v as any).join(', ')}`).join(' | ')
      } else {
        error.value = err.response?.data?.error?.message || err.response?.data?.detail || 'فشل إضافة الفرد'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updatePersonnel(id: string, data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/personnel/${id}/`, data)
      return response.data
    } catch (err: any) {
      if (err.response?.data?.error?.detail) {
        const details = err.response.data.error.detail
        error.value = Object.entries(details).map(([k, v]) => `${k}: ${(v as any).join(', ')}`).join(' | ')
      } else {
        error.value = err.response?.data?.error?.message || err.response?.data?.detail || 'فشل تعديل بيانات الفرد'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getPersonnelById(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/personnel/${id}/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب بيانات الفرد'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateNationalId(militaryNumber: string, nationalId: string, documentIds: number[]) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/personnel/${militaryNumber}/update-national-id/`, {
        national_id: nationalId,
        document_ids: documentIds
      })
      return response.data
    } catch (err: any) {
      if (err.response?.data?.error?.detail) {
        const details = err.response.data.error.detail
        error.value = Object.entries(details).map(([k, v]) => `${k}: ${(v as any).join(', ')}`).join(' | ')
      } else {
        error.value = err.response?.data?.error?.message || err.response?.data?.detail || 'فشل تحديث الرقم الوطني'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  async function importLegacyData(file: File, dryRun: boolean = true) {
    loading.value = true
    error.value = null
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('dry_run', dryRun.toString())

      const response = await api.post('/personnel/legacy-import/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || err.message || 'فشل رفع ملف البيانات'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    records,
    loading,
    error,
    totalCount,
    totalPages,
    currentPage,
    fetchPersonnel,
    checkNationalId,
    createPersonnel,
    updatePersonnel,
    updateNationalId,
    getPersonnelById,
    importLegacyData
  }
})
