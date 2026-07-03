import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export const useSecretariatStore = defineStore('secretariat', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const correspondences = ref([])
  const tasks = ref([])
  const circulars = ref([])
  
  const totalCorrespondencesCount = ref(0)
  const totalTasksCount = ref(0)
  const totalCircularsCount = ref(0)

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

  // Create Correspondence
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

  // Create Task
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

  // Create Circular
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

  return {
    loading,
    error,
    correspondences,
    tasks,
    circulars,
    totalCorrespondencesCount,
    totalTasksCount,
    totalCircularsCount,
    fetchCorrespondences,
    createCorrespondence,
    fetchTasks,
    createTask,
    fetchCirculars,
    createCircular
  }
})
