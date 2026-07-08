<template>
  <admin-layout>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">إدارة طلبات التصدير</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">مراجعة واعتماد طلبات تصدير البيانات للحفاظ على سريتها</p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-right text-sm">
            <thead class="bg-gray-50 dark:bg-gray-800/50 text-gray-700 dark:text-gray-300">
              <tr>
                <th class="px-6 py-4 font-semibold">رقم الطلب</th>
                <th class="px-6 py-4 font-semibold">اسم التقرير</th>
                <th class="px-6 py-4 font-semibold">مقدم الطلب</th>
                <th class="px-6 py-4 font-semibold">السبب</th>
                <th class="px-6 py-4 font-semibold">التاريخ</th>
                <th class="px-6 py-4 font-semibold">الحالة</th>
                <th class="px-6 py-4 font-semibold text-center">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="req in requests" :key="req.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                <td class="px-6 py-4 font-mono text-xs">{{ req.id }}</td>
                <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{{ req.report_name }}</td>
                <td class="px-6 py-4">{{ req.requested_by_name }}</td>
                <td class="px-6 py-4 max-w-xs truncate" :title="req.reason">{{ req.reason }}</td>
                <td class="px-6 py-4" dir="ltr">{{ new Date(req.created_at).toLocaleDateString('ar-YE') }}</td>
                <td class="px-6 py-4">
                  <span :class="getStatusBadgeClass(req.status)">
                    {{ req.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-center gap-2" v-if="req.status === 'PENDING'">
                    <button @click="openApprovalModal(req)" class="text-green-600 hover:bg-green-50 px-3 py-1 rounded border border-green-200 dark:border-green-800 dark:hover:bg-green-900/30 transition-colors">
                      موافقة
                    </button>
                    <button @click="openRejectionModal(req)" class="text-red-600 hover:bg-red-50 px-3 py-1 rounded border border-red-200 dark:border-red-800 dark:hover:bg-red-900/30 transition-colors">
                      رفض
                    </button>
                  </div>
                  <div v-else class="text-center text-gray-500 text-xs">
                    بواسطة: {{ req.approved_by_name }}
                  </div>
                </td>
              </tr>
              <tr v-if="requests.length === 0 && !loading">
                <td colspan="7" class="px-6 py-12 text-center text-gray-500">لا توجد طلبات تصدير لعرضها</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Action Modal -->
    <div v-if="selectedRequest" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div class="w-full max-w-md rounded-xl bg-white p-6 shadow-xl dark:bg-gray-900 dark:ring-1 dark:ring-white/10">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
          {{ actionType === 'APPROVE' ? 'موافقة على تصدير' : 'رفض طلب تصدير' }}
        </h3>
        
        <div class="mb-4 text-sm bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
          <p><strong>التقرير:</strong> {{ selectedRequest.report_name }}</p>
          <p><strong>مقدم الطلب:</strong> {{ selectedRequest.requested_by_name }}</p>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              ملاحظات (اختياري)
            </label>
            <textarea
              v-model="actionNotes"
              rows="3"
              class="w-full rounded-lg border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              placeholder="اكتب ملاحظاتك لمقدم الطلب..."
            ></textarea>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button @click="selectedRequest = null" class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors">
            إلغاء
          </button>
          <button
            @click="submitAction"
            :disabled="isSubmitting"
            :class="[
              actionType === 'APPROVE' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700',
              'rounded-lg px-4 py-2 text-sm font-medium text-white shadow-sm transition-colors disabled:opacity-50'
            ]"
          >
            {{ isSubmitting ? 'جاري التنفيذ...' : 'تأكيد' }}
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const requests = ref<any[]>([])
const loading = ref(false)

const selectedRequest = ref<any>(null)
const actionType = ref<'APPROVE'|'REJECT'>('APPROVE')
const actionNotes = ref('')
const isSubmitting = ref(false)

const fetchRequests = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/export-requests/')
    requests.value = Array.isArray(res.data) ? res.data : (res.data.results || res.data.data || [])
  } catch (error) {
    console.error('Failed to fetch requests', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRequests()
})

const getStatusBadgeClass = (status: string) => {
  const map: Record<string, string> = {
    'PENDING': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-500',
    'APPROVED': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-500',
    'REJECTED': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-500',
    'EXPIRED': 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400',
  }
  return `inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${map[status] || map['PENDING']}`
}

const openApprovalModal = (req: any) => {
  selectedRequest.value = req
  actionType.value = 'APPROVE'
  actionNotes.value = ''
}

const openRejectionModal = (req: any) => {
  selectedRequest.value = req
  actionType.value = 'REJECT'
  actionNotes.value = ''
}

const submitAction = async () => {
  if (!selectedRequest.value) return
  
  isSubmitting.value = true
  try {
    const endpoint = actionType.value === 'APPROVE' ? 'approve' : 'reject'
    await api.post(`/reports/export-requests/${selectedRequest.value.id}/${endpoint}/`, {
      approval_notes: actionNotes.value
    })
    
    // Refresh list
    await fetchRequests()
    selectedRequest.value = null
  } catch (error) {
    console.error('Action failed', error)
    alert('حدث خطأ أثناء تنفيذ الإجراء')
  } finally {
    isSubmitting.value = false
  }
}
</script>
