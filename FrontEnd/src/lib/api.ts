import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios'
import Swal from 'sweetalert2'
import { useValidationStore } from '@/stores/validation'

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
})

// Request interceptor — إضافة التوكن تلقائياً
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Clear previous validation errors on new request
    try {
      const validationStore = useValidationStore()
      if (config.method !== 'get') {
        validationStore.clearAllErrors()
      }
    } catch (e) {
      // Pinia might not be ready yet
    }

    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — تجديد التوكن تلقائياً عند 401
let isRefreshing = false
let failedQueue: Array<{
  resolve: (value: unknown) => void
  reject: (reason?: unknown) => void
}> = []

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = localStorage.getItem('refresh_token')

      if (!refreshToken) {
        isRefreshing = false
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('session_id')
        localStorage.removeItem('user')
        window.location.href = '/signin'
        return Promise.reject(error)
      }

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'}/auth/refresh/`,
          { refresh_token: refreshToken }
        )

        const { access_token, refresh_token: newRefreshToken } = response.data.data

        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', newRefreshToken)

        originalRequest.headers.Authorization = `Bearer ${access_token}`

        processQueue(null, access_token)
        return api(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('session_id')
        localStorage.removeItem('user')
        window.location.href = '/signin'

        Swal.fire({
          icon: 'error',
          title: 'انتهت الجلسة',
          text: 'يرجى تسجيل الدخول مرة أخرى.',
          confirmButtonText: 'حسناً',
          confirmButtonColor: '#3085d6',
        })

        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    // Global Error Handling with SweetAlert2 for non-401 errors
    let errorMessage = 'حدث خطأ غير متوقع في الاتصال بالخادم.'
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      if (status === 403) {
        errorMessage = 'ليس لديك صلاحية للقيام بهذا الإجراء.'
      } else if (status === 404) {
        errorMessage = 'البيانات المطلوبة غير موجودة.'
      } else if (status >= 500) {
        errorMessage = 'حدث خطأ داخلي في الخادم.'
      } else if (data) {
        // Send field errors to validation store
        if (status === 400 && typeof data === 'object') {
          try {
            const validationStore = useValidationStore()
            validationStore.setErrors(data)
          } catch (e) {
            // Pinia not ready
          }
        }

        // Advanced formatting for 400 or other validation errors
        let messages: string[] = [];

        // Helper to extract messages from nested objects/arrays
        const extractMessages = (obj: any) => {
          if (typeof obj === 'string') {
            // Check if it's a python dict stringified
            if (obj.startsWith('{') && obj.endsWith('}')) {
              try {
                // VERY basic python dict cleanup to extract strings
                const clean = obj.replace(/\[|\]|'|"/g, '').replace(/\{|\}/g, '')
                clean.split(',').forEach(part => {
                  const subparts = part.split(':')
                  const msg = subparts.length > 1 ? subparts[1].trim() : part.trim()
                  if (msg) messages.push(msg)
                })
              } catch (e) {
                messages.push(obj)
              }
            } else {
              messages.push(obj)
            }
          } else if (Array.isArray(obj)) {
            obj.forEach(extractMessages)
          } else if (typeof obj === 'object' && obj !== null) {
            if (obj.detail && typeof obj.detail === 'string') messages.push(obj.detail)
            else if (obj.message && typeof obj.message === 'string') messages.push(obj.message)
            else if (obj.error && typeof obj.error === 'string') extractMessages(obj.error)
            else {
              Object.values(obj).forEach(extractMessages)
            }
          }
        }

        extractMessages(data);

        if (messages.length > 0) {
          // Remove duplicates
          const uniqueMessages = [...new Set(messages)];
          if (uniqueMessages.length === 1) {
            errorMessage = uniqueMessages[0];
          } else {
            errorMessage = `<ul style="text-align: right; list-style-type: disc; padding-right: 20px;">` +
              uniqueMessages.map(m => `<li>${m}</li>`).join('') +
              `</ul>`;
          }
        }
      }
    } else if (error.request) {
      errorMessage = 'لا يمكن الاتصال بالخادم. يرجى التحقق من اتصالك بالإنترنت.'
    }

    Swal.fire({
      icon: 'error',
      title: 'تنبيه',
      html: errorMessage,
      confirmButtonText: 'حسناً',
      confirmButtonColor: '#d33',
    })

    return Promise.reject(error)
  }
)

export default api
