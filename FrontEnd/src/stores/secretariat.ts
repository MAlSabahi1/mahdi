import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export const useSecretariatStore = defineStore('secretariat', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const correspondences = ref([])
  const tasks = ref([])
  const circulars = ref([])
  const meetings = ref([])
  const documentRequests = ref([])
  const inventoryItems = ref([])
  const inventoryRequests = ref([])
  const custodies = ref([])
  const attendanceLogs = ref([])
  const financialAllocations = ref([])
  const expenses = ref([])
  
  const totalCorrespondencesCount = ref(0)
  const totalTasksCount = ref(0)
  const totalCircularsCount = ref(0)
  const totalMeetingsCount = ref(0)
  const totalDocumentRequestsCount = ref(0)
  const totalInventoryItemsCount = ref(0)
  const totalInventoryRequestsCount = ref(0)
  const totalCustodiesCount = ref(0)
  const totalAttendanceCount = ref(0)

  // Fetch Correspondences
  async function fetchCorrespondences(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/correspondences/', { params })
      correspondences.value = response.data.results
      totalCorrespondencesCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب المراسلات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCorrespondenceById(id: string | number) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/secretariat/correspondences/${id}/`)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب تفاصيل المراسلة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCorrespondence(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/correspondences/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء المراسلة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCorrespondence(id: string | number, data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/secretariat/correspondences/${id}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تعديل المراسلة'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Correspondence Attachments
  async function uploadAttachment(formData: FormData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/attachments/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل رفع المرفق'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteAttachment(id: string | number) {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/secretariat/attachments/${id}/`)
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل حذف المرفق'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Fetch Tasks
  async function fetchTasks(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/tasks/', { params })
      tasks.value = response.data.results
      totalTasksCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب المهام'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createTask(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/tasks/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء المهمة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTask(id: string | number, data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/secretariat/tasks/${id}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحديث المهمة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteTask(id: string | number) {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/secretariat/tasks/${id}/`)
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل حذف المهمة'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Fetch Circulars
  async function fetchCirculars(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/circulars/', { params })
      circulars.value = response.data.results
      totalCircularsCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب التعاميم'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCircular(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/circulars/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء التعميم'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Meeting Minutes
  async function fetchMeetings(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/meetings/', { params })
      meetings.value = response.data.results
      totalMeetingsCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب محاضر الاجتماعات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createMeeting(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/meetings/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل حفظ محضر الاجتماع'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Document Office Work Requests
  async function fetchDocumentRequests(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/document-requests/', { params })
      documentRequests.value = response.data.results
      totalDocumentRequestsCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب طلبات الأعمال المكتبية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createDocumentRequest(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/document-requests/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء طلب الأعمال المكتبية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateDocumentRequest(id: string | number, data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/secretariat/document-requests/${id}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تعديل طلب الأعمال المكتبية'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Inventory items
  async function fetchInventoryItems(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/inventory-items/', { params })
      inventoryItems.value = response.data.results
      totalInventoryItemsCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب المواد المخزنية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createInventoryItem(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/inventory-items/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إضافة مادة مخزنية'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Inventory Requests
  async function fetchInventoryRequests(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/inventory-requests/', { params })
      inventoryRequests.value = response.data.results
      totalInventoryRequestsCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب طلبات القرطاسية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createInventoryRequest(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/inventory-requests/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل إنشاء طلب الصرف'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateInventoryRequest(id: string | number, data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/secretariat/inventory-requests/${id}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تحديث حالة طلب الصرف'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Custodies
  async function fetchCustodies(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/custodies/', { params })
      custodies.value = response.data.results
      totalCustodiesCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب سجلات العهد'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCustody(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/custodies/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل قيد العهدة'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCustody(id: string | number, data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.patch(`/secretariat/custodies/${id}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تعديل العهدة'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Attendance
  async function fetchAttendanceLogs(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/attendance-logs/', { params })
      attendanceLogs.value = response.data.results
      totalAttendanceCount.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب سجلات الدوام'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createAttendanceLog(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/attendance-logs/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تسجيل الدوام'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Financial Allocations & Expenses
  async function fetchFinancialAllocations(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/financial-allocations/', { params })
      financialAllocations.value = response.data.results
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب الاعتمادات المالية'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createFinancialAllocation(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/financial-allocations/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل قيد الاعتماد المالي'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchExpenses(params: any = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/secretariat/expenses/', { params })
      expenses.value = response.data.results
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل جلب المصروفات'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createExpense(data: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/secretariat/expenses/', data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'فشل تسجيل المصروف'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    correspondences,
    tasks,
    circulars,
    meetings,
    documentRequests,
    inventoryItems,
    inventoryRequests,
    custodies,
    attendanceLogs,
    financialAllocations,
    expenses,
    totalCorrespondencesCount,
    totalTasksCount,
    totalCircularsCount,
    totalMeetingsCount,
    totalDocumentRequestsCount,
    totalInventoryItemsCount,
    totalInventoryRequestsCount,
    totalCustodiesCount,
    totalAttendanceCount,
    fetchCorrespondences,
    fetchCorrespondenceById,
    createCorrespondence,
    updateCorrespondence,
    uploadAttachment,
    deleteAttachment,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    fetchCirculars,
    createCircular,
    fetchMeetings,
    createMeeting,
    fetchDocumentRequests,
    createDocumentRequest,
    updateDocumentRequest,
    fetchInventoryItems,
    createInventoryItem,
    fetchInventoryRequests,
    createInventoryRequest,
    updateInventoryRequest,
    fetchCustodies,
    createCustody,
    updateCustody,
    fetchAttendanceLogs,
    createAttendanceLog,
    fetchFinancialAllocations,
    createFinancialAllocation,
    fetchExpenses,
    createExpense
  }
})
