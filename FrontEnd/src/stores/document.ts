import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface DocumentRecord {
  id: number
  document_type: string
  document_type_display: string
  file_url: string
  file_name: string
  created_at: string
}

export const useDocumentStore = defineStore('document', () => {
  const loading = ref(false)

  // Upload document
  async function uploadDocument(personnelId: string, file: File, type: string, typeDisplay: string): Promise<DocumentRecord> {
    loading.value = true
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('document_type', type)
      formData.append('personnel', personnelId)
      formData.append('status', 'committed')
      
      const response = await api.post('/storage/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      const newDoc = response.data.data
      
      return {
        id: newDoc.id,
        document_type: newDoc.document_type,
        document_type_display: typeDisplay,
        file_url: newDoc.file_url,
        file_name: newDoc.original_filename || file.name,
        created_at: newDoc.created_at || new Date().toISOString()
      }
    } catch (err) {
      console.error('Failed to upload document:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Delete/Replace document (Mocked delete since API might not support pure delete)
  async function deleteDocument(personnelId: string, docId: number) {
    loading.value = true
    try {
      // In a real app with delete endpoint:
      // await api.delete(`/storage/documents/${docId}/`)
      await new Promise(resolve => setTimeout(resolve, 800))
    } catch (err) {
      console.error('Failed to delete document:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    uploadDocument,
    deleteDocument
  }
})
