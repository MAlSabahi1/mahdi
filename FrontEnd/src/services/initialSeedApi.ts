import api from '@/lib/api'

export interface SeedErrorDetail {
  field: string
  message: string
}

export interface SeedRowError {
  row: number
  military_number: string
  name: string
  errors: SeedErrorDetail[]
  rowData: Record<string, any>
}

export interface PreviewSeedResponse {
  headers: string[]
  rows: any[][]
}

export interface ValidateSeedResponse {
  total_rows: number
  valid_rows: number
  error_count: number
  is_valid: boolean
  errors: SeedRowError[]
  all_rows?: Record<string, any>[]
}

export interface CommitSeedResponse {
  created: number
  name_corrections: number
  monthly_vars: number
}

/**
 * يعرض معاينة لأول 10 صفوف من الملف
 */
export async function previewInitialSeed(file: File): Promise<{ success: boolean; data?: PreviewSeedResponse; message?: string }> {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/service-cycle/initial-seed/preview/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data
    }
    throw error
  }
}

/**
 * يرفع ملف الإكسل التأسيسي للفحص الصارم
 */
export async function validateInitialSeed(file: File, mapping?: Record<string, string>): Promise<{ success: boolean; data?: ValidateSeedResponse; message?: string }> {
  try {
    const formData = new FormData()
    formData.append('file', file)
    if (mapping) {
      formData.append('mapping', JSON.stringify(mapping))
    }
    
    const response = await api.post('/service-cycle/initial-seed/validate/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data
    }
    throw error
  }
}

/**
 * يعتمد ملف التأسيس بعد التأكد من صحته 100%
 */
export async function commitInitialSeed(file: File, mapping?: Record<string, string>): Promise<{ success: boolean; data?: CommitSeedResponse; message?: string }> {
  try {
    const formData = new FormData()
    formData.append('file', file)
    if (mapping) {
      formData.append('mapping', JSON.stringify(mapping))
    }
    
    const response = await api.post('/service-cycle/initial-seed/commit/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data
    }
    throw error
  }
}

/**
 * فحص بيانات التأسيس عبر JSON المباشر (المسار الجديد)
 */
export async function validateInitialSeedJson(rowsData: Record<string, any>[]): Promise<{ success: boolean; data?: ValidateSeedResponse; message?: string }> {
  try {
    const response = await api.post('/service-cycle/initial-seed/validate-json/', { data: rowsData })
    return response.data
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data
    }
    throw error
  }
}

/**
 * اعتماد بيانات التأسيس عبر JSON المباشر (المسار الجديد)
 */
export async function commitInitialSeedJson(rowsData: Record<string, any>[], batchId?: string): Promise<{ success: boolean; data?: CommitSeedResponse; message?: string }> {
  try {
    const response = await api.post('/service-cycle/initial-seed/commit-json/', { data: rowsData, batch_id: batchId })
    return response.data
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data
    }
    throw error
  }
}
