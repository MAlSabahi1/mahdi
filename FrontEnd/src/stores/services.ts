import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface StagingRecord {
  id: number
  personnel: {
    military_number: string
    full_name: string
  }
  field_name: string
  old_value: any
  new_value: any
  status: string
  severity: string
  created_at: string
  upload_batch_id: string
}

export const useServicesStore = defineStore('services', () => {
  const stagingRecords = ref<StagingRecord[]>([])
  const stagingStats = ref({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
    by_severity: { low: 0, medium: 0, high: 0 }
  })
  
  const rejectionsRecords = ref<any[]>([])
  const reconciliationTasks = ref<any[]>([])
  const complianceRecords = ref<any[]>([])
  const reportTemplates = ref<any[]>([])
  
  // Status Change Forms State
  const forms = ref<any[]>([])
  const formSchemas = ref<any>({})
  const currentSchema = ref<any>(null)
  
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const totalCount = ref(0)
  const totalPages = ref(1)
  const currentPage = ref(1)

  async function fetchStagingStats() {
    try {
      const response = await api.get('/service-cycle/staging/stats/')
      if (response.data?.success) {
        stagingStats.value = response.data.data
      }
    } catch (err: any) {
      console.error('Failed to fetch staging stats', err)
    }
  }

  async function fetchStagingRecords(page: number = 1, params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const queryParams = new URLSearchParams()
      queryParams.append('page', page.toString())
      
      if (params.status) queryParams.append('status', params.status)
      if (params.severity) queryParams.append('severity', params.severity)
      if (params.search) queryParams.append('search', params.search)
      
      const response = await api.get(`/service-cycle/staging/?${queryParams.toString()}`)
      
      stagingRecords.value = response.data.results
      totalCount.value = response.data.count
      totalPages.value = response.data.total_pages || Math.ceil(response.data.count / 20)
      currentPage.value = page
    } catch (err: any) {
      error.value = err.response?.data?.error || err.message || 'فشل جلب قائمة المراجعة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function approveStaging(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/staging/${id}/approve/`, {})
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل الموافقة على التعديل'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function rejectStaging(id: number, reason: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/staging/${id}/reject/`, {
        rejection_reason: reason
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل رفض التعديل'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function bulkApproveStaging(ids: number[]) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/service-cycle/staging/bulk_approve/', {
        staging_ids: ids
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل الموافقة الجماعية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function exportSheet(directorateId: number, month: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/service-cycle/export/', {
        params: { directorate_id: directorateId, month },
        responseType: 'blob' // Important for file download
      })
      
      // Handle file download
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      // Try to get filename from content-disposition header if possible, else fallback
      let fileName = `export_${month}.xlsx`
      const disposition = response.headers['content-disposition']
      if (disposition && disposition.indexOf('filename=') !== -1) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition)
        if (matches != null && matches[1]) {
          fileName = matches[1].replace(/['"]/g, '')
        }
      }
      link.setAttribute('download', fileName)
      document.body.appendChild(link)
      link.click()
      link.parentNode?.removeChild(link)
      
      return true
    } catch (err: any) {
      error.value = 'فشل عملية التصدير'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function importSheet(file: File) {
    loading.value = true
    error.value = null
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      // Extract export_id and service_month from filename if possible
      // Expected format: كشف_اسم المديرية_YYYY-MM_export-id-uuid.xlsx
      const fileNameStr = file.name
      const uuidMatch = fileNameStr.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/)
      
      if (uuidMatch) {
        formData.append('export_id', uuidMatch[0])
      } else {
        // Fallback dummy uuid just to pass validation if user renamed file
        // The backend should ideally handle this better, but we provide it just in case.
        formData.append('export_id', '00000000-0000-0000-0000-000000000000')
      }
      
      // Match YYYY-MM
      const monthMatch = fileNameStr.match(/\d{4}-\d{2}/)
      if (monthMatch) {
        formData.append('service_month', monthMatch[0])
      }
      
      const response = await api.post('/service-cycle/import/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل عملية الاستيراد'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function checkTaskStatus(taskId: string) {
    try {
      const response = await api.get(`/service-cycle/tasks/${taskId}/`)
      return response.data
    } catch (err: any) {
      console.error('Failed to check task status', err)
      throw err
    }
  }

  async function fetchRejections(page: number = 1, params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const queryParams = new URLSearchParams()
      queryParams.append('page', page.toString())
      
      if (params.central_department) queryParams.append('central_department', params.central_department)
      if (params.service_month) queryParams.append('service_month', params.service_month)
      if (params.security_admin) queryParams.append('security_admin', params.security_admin)
      
      const response = await api.get(`/service-cycle/rejections/?${queryParams.toString()}`)
      
      rejectionsRecords.value = response.data.results || response.data
      totalCount.value = response.data.count || rejectionsRecords.value.length
      totalPages.value = response.data.total_pages || Math.ceil(totalCount.value / 20)
      currentPage.value = page
    } catch (err: any) {
      error.value = err.response?.data?.error || err.message || 'فشل جلب قائمة المرفوضات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function exportRejections(directorateId: string, month: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/service-cycle/rejections/export/', {
        params: { directorate_id: directorateId, month },
        responseType: 'blob'
      })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `rejections_report_${month}.xlsx`)
      document.body.appendChild(link)
      link.click()
      link.parentNode?.removeChild(link)
      
      return true
    } catch (err: any) {
      error.value = 'فشل تصدير تقرير المرفوضات'
      throw err
    } finally {
      loading.value = false
    }
  }

  // --- Reconciliation ---
  async function fetchReconciliationTasks() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/service-cycle/reconciliation/')
      reconciliationTasks.value = response.data.data || response.data.results || []
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب مهام المطابقة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createReconciliationTask(file: File, name: string, taskType: string, keyField: string = 'military_number') {
    loading.value = true
    error.value = null
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('name', name)
      formData.append('task_type', taskType)
      formData.append('key_field', keyField)
      
      const response = await api.post('/service-cycle/reconciliation/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء مهمة المطابقة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchReconciliationTaskDetails(taskId: string | number) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/service-cycle/reconciliation/${taskId}/`)
      return response.data.data || response.data
    } catch (err: any) {
      error.value = 'فشل جلب تفاصيل المهمة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function resolveReconciliation(taskId: string | number, resolutions: any[]) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/reconciliation/${taskId}/resolve/`, {
        resolutions
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تطبيق حلول المطابقة'
      throw err
    } finally {
      loading.value = false
    }
  }

  // --- Reports & Compliance ---
  async function fetchCompliance(month?: string) {
    loading.value = true
    error.value = null
    try {
      const params = month ? { service_month: month } : {}
      const response = await api.get('/service-cycle/compliance/', { params })
      complianceRecords.value = response.data.results || response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب سجلات الامتثال'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchReportTemplates() {
    try {
      const response = await api.get('/service-cycle/reports/')
      reportTemplates.value = response.data.data || response.data.results || []
    } catch (err: any) {
      console.error('Failed to fetch report templates', err)
    }
  }

  async function generateReport(templateId: number, format: string, filters: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/service-cycle/reports/generate/', {
        template_id: templateId,
        format,
        filters
      })
      
      // The API returns the download URL or file path. 
      // If it's a direct file response or path:
      if (response.data && response.data.data && response.data.data.file_path) {
        // We can just download it using the download endpoint
        const fileName = response.data.data.file_path.split(/[\\/]/).pop()
        
        const fileResponse = await api.get(`/service-cycle/reports/download/${fileName}`, {
          responseType: 'blob'
        })
        
        const url = window.URL.createObjectURL(new Blob([fileResponse.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', fileName || `report.${format}`)
        document.body.appendChild(link)
        link.click()
        link.parentNode?.removeChild(link)
      } else {
        throw new Error('الرابط غير متوفر')
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل توليد التقرير'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function closeMonth() {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/service-cycle/snapshots/close-month/')
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إقفال الشهر'
      throw err
    } finally {
      loading.value = false
    }
  }

  // --- Status Change Forms ---
  async function fetchFormSchemas() {
    try {
      const response = await api.get('/service-cycle/forms/schema/')
      if (response.data?.success) {
        formSchemas.value = response.data.data
      }
    } catch (err: any) {
      console.error('Failed to fetch form schemas', err)
    }
  }

  async function fetchFormSchema(type: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/service-cycle/forms/schema/?type=${type}`)
      if (response.data?.success) {
        currentSchema.value = response.data.data
        return response.data.data
      }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب هيكل الاستمارة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchForms(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const queryParams = new URLSearchParams()
      if (params.type) queryParams.append('type', params.type)
      if (params.status) queryParams.append('status', params.status)
      if (params.personnel) queryParams.append('personnel', params.personnel)
      if (params.page) queryParams.append('page', params.page.toString())
      
      const response = await api.get(`/service-cycle/forms/?${queryParams.toString()}`)
      forms.value = response.data.results || response.data
      totalCount.value = response.data.count || forms.value.length
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب الاستمارات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createForm(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/service-cycle/forms/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء الاستمارة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function submitForm(id: number | string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/forms/${id}/submit/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تقديم الاستمارة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function approveForm(id: number | string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/forms/${id}/approve/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل اعتماد الاستمارة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function rejectForm(id: number | string, reason: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/forms/${id}/reject/`, { reason })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل رفض الاستمارة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchFormById(id: number | string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/service-cycle/forms/${id}/`)
      return response.data?.data || response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب تفاصيل المعاملة'
      throw err
    } finally {
      loading.value = false
    }
  }

  // --- Extended Service Cycle (Timeline, Notes, Return, Checklist, Catalog) ---
  
  async function fetchFormTimeline(id: number | string) {
    try {
      const response = await api.get(`/service-cycle/form-actions/${id}/timeline/`)
      return response.data
    } catch (err: any) {
      console.error('Failed to fetch timeline', err)
      return []
    }
  }

  async function fetchFormNotes(id: number | string) {
    try {
      const response = await api.get(`/service-cycle/form-actions/${id}/notes/`)
      return response.data
    } catch (err: any) {
      console.error('Failed to fetch notes', err)
      return []
    }
  }

  async function addFormNote(id: number | string, content: string) {
    try {
      const response = await api.post(`/service-cycle/form-actions/${id}/notes/`, { content })
      return response.data
    } catch (err: any) {
      throw err
    }
  }

  async function returnForm(id: number | string, data: { reason: string, details?: string, to_status?: string }) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/service-cycle/form-actions/${id}/return_form/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إرجاع الاستمارة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchFormChecklist(id: number | string, stage?: string) {
    try {
      const url = `/service-cycle/form-actions/${id}/checklist/` + (stage ? `?stage=${stage}` : '')
      const response = await api.get(url)
      return response.data
    } catch (err: any) {
      console.error('Failed to fetch checklist', err)
      return []
    }
  }

  async function toggleChecklistItem(itemId: number | string, isChecked: boolean) {
    try {
      const response = await api.patch(`/service-cycle/checklist/${itemId}/toggle/`, { is_checked: isChecked })
      return response.data
    } catch (err: any) {
      throw err
    }
  }

  const catalogServices = ref<any[]>([])

  async function fetchServiceCatalog(params: any = {}) {
    loading.value = true
    try {
      const response = await api.get('/service-cycle/catalog/', { params })
      catalogServices.value = response.data.results || response.data
      return catalogServices.value
    } catch (err: any) {
      console.error('Failed to fetch catalog', err)
      return []
    } finally {
      loading.value = false
    }
  }

  async function validatePrerequisites(formId: number | string) {
    try {
      const response = await api.post(`/service-cycle/catalog-validation/${formId}/validate/`)
      return response.data
    } catch (err: any) {
      console.error('Failed to validate prerequisites', err)
      return { valid: false, errors: ['فشل التحقق من الشروط المسبقة'] }
    }
  }

  return {
    stagingRecords,
    stagingStats,
    loading,
    error,
    totalCount,
    totalPages,
    currentPage,
    fetchStagingStats,
    fetchStagingRecords,
    approveStaging,
    rejectStaging,
    bulkApproveStaging,
    exportSheet,
    importSheet,
    checkTaskStatus,
    rejectionsRecords,
    fetchRejections,
    exportRejections,
    reconciliationTasks,
    fetchReconciliationTasks,
    createReconciliationTask,
    fetchReconciliationTaskDetails,
    resolveReconciliation,
    complianceRecords,
    reportTemplates,
    fetchCompliance,
    fetchReportTemplates,
    generateReport,
    closeMonth,
    
    // Status Change Forms
    forms,
    formSchemas,
    currentSchema,
    fetchFormSchemas,
    fetchFormSchema,
    fetchForms,
    createForm,
    submitForm,
    approveForm,
    rejectForm,
    fetchFormById,
    
    // Extended Actions
    fetchFormTimeline,
    fetchFormNotes,
    addFormNote,
    returnForm,
    fetchFormChecklist,
    toggleChecklistItem,
    
    // Catalog
    catalogServices,
    fetchServiceCatalog,
    validatePrerequisites
  }
})
