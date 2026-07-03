<template>
  <div class="fixed inset-0 z-[99999] flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
    <div class="w-full max-w-4xl max-h-[90vh] flex flex-col rounded-xl bg-white shadow-xl dark:bg-gray-900">
      
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-100 p-5 dark:border-gray-800">
        <div>
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white/90">
            تفاصيل السجل
            <span class="ml-2 inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium"
              :class="getActionColor(log?.action)">
              {{ log?.action }}
            </span>
          </h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            سجل رقم #{{ log?.id }} | {{ formatDate(log?.timestamp) }}
          </p>
        </div>
        <button @click="$emit('close')" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-5">
        <div v-if="loading" class="flex justify-center py-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="detail" class="space-y-6">
          <!-- Main Info -->
          <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div class="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
              <span class="block text-xs text-gray-500 dark:text-gray-400">المستخدم</span>
              <span class="mt-1 block font-medium text-gray-900 dark:text-white">{{ detail.username || 'نظام' }}</span>
            </div>
            <div class="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
              <span class="block text-xs text-gray-500 dark:text-gray-400">النموذج</span>
              <span class="mt-1 block font-medium text-gray-900 dark:text-white">{{ detail.model_name }}</span>
            </div>
            <div class="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
              <span class="block text-xs text-gray-500 dark:text-gray-400">معرف الكائن</span>
              <span class="mt-1 block font-medium text-gray-900 dark:text-white">{{ detail.object_id }}</span>
            </div>
            <div class="rounded-lg bg-gray-50 p-3 dark:bg-gray-800/50">
              <span class="block text-xs text-gray-500 dark:text-gray-400">رقم IP</span>
              <span class="mt-1 block font-medium text-gray-900 dark:text-white">{{ detail.ip_address || '—' }}</span>
            </div>
          </div>

          <!-- Reason -->
          <div v-if="detail.change_reason" class="rounded-lg border border-gray-100 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
            <span class="block text-xs text-gray-500 dark:text-gray-400">سبب التغيير</span>
            <p class="mt-1 text-sm text-gray-800 dark:text-gray-200">{{ detail.change_reason }}</p>
          </div>

          <!-- Data Comparison -->
          <div v-if="hasDataChanges" class="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <!-- Old Data -->
            <div class="rounded-lg border border-error-100 bg-error-50/30 p-4 dark:border-error-500/20 dark:bg-error-500/5">
              <h3 class="mb-3 flex items-center gap-2 text-sm font-bold text-error-700 dark:text-error-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                البيانات القديمة
              </h3>
              <pre class="overflow-x-auto text-xs text-gray-700 dark:text-gray-300 whitespace-pre-wrap ltr" dir="ltr">{{ formatJSON(detail.old_data) }}</pre>
            </div>
            
            <!-- New Data -->
            <div class="rounded-lg border border-success-100 bg-success-50/30 p-4 dark:border-success-500/20 dark:bg-success-500/5">
              <h3 class="mb-3 flex items-center gap-2 text-sm font-bold text-success-700 dark:text-success-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                البيانات الجديدة
              </h3>
              <pre class="overflow-x-auto text-xs text-gray-700 dark:text-gray-300 whitespace-pre-wrap ltr" dir="ltr">{{ formatJSON(detail.new_data) }}</pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between border-t border-gray-100 bg-gray-50 px-5 py-4 dark:border-gray-800 dark:bg-gray-800/50 rounded-b-xl">
        <div class="flex items-center gap-3">
          <button @click="verifyRecord" :disabled="verifying || loading"
            class="inline-flex items-center gap-2 rounded-lg border border-brand-200 bg-brand-50 px-4 py-2 text-sm font-medium text-brand-700 hover:bg-brand-100 dark:border-brand-500/20 dark:bg-brand-500/10 dark:text-brand-400 disabled:opacity-50">
            <svg v-if="verifying" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            التحقق من سلامة السجل
          </button>
        </div>
        <button @click="$emit('close')"
          class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700">
          إغلاق
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuditStore } from '@/stores/audit'
import Swal from 'sweetalert2'

const props = defineProps({
  log: { type: Object, required: true }
})

const emit = defineEmits(['close'])
const auditStore = useAuditStore()

const loading = ref(true)
const detail = ref(null)
const verifying = ref(false)

const hasDataChanges = computed(() => {
  if (!detail.value) return false
  const oldEmpty = !detail.value.old_data || Object.keys(detail.value.old_data).length === 0
  const newEmpty = !detail.value.new_data || Object.keys(detail.value.new_data).length === 0
  return !(oldEmpty && newEmpty)
})

onMounted(async () => {
  try {
    detail.value = await auditStore.getLogDetails(props.log.id)
  } catch (err) {
    Swal.fire('خطأ', 'تعذر تحميل تفاصيل السجل', 'error')
    emit('close')
  } finally {
    loading.value = false
  }
})

function formatJSON(obj) {
  if (!obj) return ''
  try {
    return JSON.stringify(obj, null, 2)
  } catch {
    return String(obj)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('ar-SA', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
}

function getActionColor(action) {
  if (!action) return 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
  const act = action.toUpperCase()
  if (act.includes('CREATE')) return 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400'
  if (act.includes('UPDATE')) return 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400'
  if (act.includes('DELETE')) return 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
  return 'bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400'
}

async function verifyRecord() {
  verifying.value = true
  try {
    const result = await auditStore.verifySignature(props.log.id)
    if (result.data.is_verified) {
      Swal.fire({
        icon: 'success',
        title: 'السجل سليم وموثوق',
        text: 'تمت مطابقة التوقيع المشفر ولم يتم التلاعب بالسجل.',
        confirmButtonText: 'حسناً'
      })
    } else {
      Swal.fire({
        icon: 'error',
        title: 'تلاعب بالسجل!',
        text: 'السجل غير سليم وتم تعديله خارج النظام.',
        confirmButtonColor: '#ef4444',
        confirmButtonText: 'إغلاق'
      })
    }
  } catch (err) {
    Swal.fire('خطأ', 'فشل إجراء التحقق', 'error')
  } finally {
    verifying.value = false
  }
}
</script>
