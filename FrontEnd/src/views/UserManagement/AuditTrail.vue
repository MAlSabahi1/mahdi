<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="السجل المركزي لتدقيق البيانات" />

    <div class="space-y-6" dir="rtl">
      <!-- Top Filters and Toolbar -->
      <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </span>
            <h3 class="text-sm font-black text-gray-900 dark:text-white">خيارات البحث والتصفية المتقدمة</h3>
          </div>
          <button
            @click="resetFilters"
            class="text-xs text-amber-600 hover:text-amber-700 bg-amber-500/10 hover:bg-amber-500/20 px-3 py-1.5 rounded-xl font-bold transition-all cursor-pointer"
          >
            إعادة تعيين الفلاتر
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Text Search -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1">بحث عام</label>
            <input
              type="text"
              v-model="filters.search"
              placeholder="اسم المستخدم، السبب، معرف السجل..."
              class="w-full text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500/25 text-right"
              @input="handleFilterChange"
            />
          </div>

          <!-- Module/Subsystem Filter -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1">النظام الفرعي</label>
            <select
              v-model="filters.module"
              class="w-full text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500/25 text-right"
              @change="handleFilterChange"
            >
              <option value="">الكل</option>
              <option value="personnel">شؤون الأفراد</option>
              <option value="services">الخدمات والكشوفات</option>
              <option value="security">الأمن والصلاحيات</option>
              <option value="system">إعدادات النظام</option>
            </select>
          </div>

          <!-- Action Filter -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1">نوع العملية</label>
            <select
              v-model="filters.action"
              class="w-full text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500/25 text-right"
              @change="handleFilterChange"
            >
              <option value="">الكل</option>
              <option value="CREATE">إضافة (CREATE)</option>
              <option value="UPDATE">تعديل (UPDATE)</option>
              <option value="DELETE">تعطيل/حذف (DELETE)</option>
              <option value="APPROVE">اعتماد/موافقة (APPROVE)</option>
              <option value="REJECT">رفض (REJECT)</option>
              <option value="EXPORT">تصدير (EXPORT)</option>
            </select>
          </div>

          <!-- Severity Filter -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1">مستوى الحساسية</label>
            <select
              v-model="filters.severity"
              class="w-full text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500/25 text-right"
              @change="handleFilterChange"
            >
              <option value="">الكل</option>
              <option value="info">معلومات (info)</option>
              <option value="low">منخفض (low)</option>
              <option value="medium">متوسط (medium)</option>
              <option value="high">عالي (high)</option>
              <option value="critical">حرج (critical)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Logs Grid / Table -->
      <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
            <span>سجلات تدقيق العمليات</span>
            <span class="text-xs text-gray-500 font-bold bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-lg">
              {{ auditStore.totalSystemLogs }} سجل
            </span>
          </h3>
        </div>

        <div v-if="auditStore.loading" class="flex justify-center py-12">
          <svg class="h-8 w-8 animate-spin text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>

        <div v-else-if="auditStore.systemLogs.length === 0" class="text-center py-12 text-gray-400">
          لا توجد سجلات تدقيق تطابق شروط البحث.
        </div>

        <div v-else class="space-y-4">
          <div class="mt-4">
            <DataTable
              :columns="auditColumns"
              :data="auditStore.systemLogs"
              row-key="id"
            >
              <template #cell-timestamp="{ row }">
                <span class="font-mono text-[11px] text-gray-500">{{ formatDate(row.timestamp) }}</span>
              </template>
              <template #cell-user="{ row }">
                <span class="font-extrabold text-gray-900 dark:text-white">{{ row.username }}</span>
                <span class="text-[10px] text-gray-400 block font-mono">IP: {{ row.ip_address || '—' }}</span>
              </template>
              <template #cell-action="{ row }">
                <span 
                  class="px-2 py-0.5 rounded-md font-extrabold text-[10px]"
                  :class="getActionClass(row.action)"
                >
                  {{ row.action }}
                </span>
              </template>
              <template #cell-model="{ row }">
                <span class="font-bold text-gray-700 dark:text-gray-300">{{ row.model_name }}</span>
                <span class="text-[10px] text-gray-400 block font-mono">ID: {{ row.object_id }}</span>
              </template>
              <template #cell-reason="{ row }">
                <span class="max-w-[200px] truncate block" :title="row.change_reason">
                  {{ row.change_reason || '—' }}
                </span>
              </template>
              <template #cell-severity="{ row }">
                <span 
                  class="px-2 py-0.5 rounded-full font-black text-[9px]"
                  :class="getSeverityClass(row.severity)"
                >
                  {{ getSeverityLabel(row.severity) }}
                </span>
              </template>
              <template #cell-signature="{ row }">
                <button 
                  @click.stop="handleVerifySignature(row)"
                  class="px-2 py-1 rounded-xl text-[10px] font-black transition-all flex items-center justify-center gap-1 mx-auto cursor-pointer w-fit"
                  :class="[
                    verificationStatus[row.id] === 'valid' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' :
                    verificationStatus[row.id] === 'invalid' ? 'bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20' :
                    verificationStatus[row.id] === 'checking' ? 'bg-blue-500/10 text-blue-600 animate-pulse' :
                    'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-200'
                  ]"
                >
                  <svg v-if="verificationStatus[row.id] === 'valid'" xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M2.166 11.37a1 1 0 011.196-.718l2.802.73 4.29-6.865a1 1 0 011.64 1.024l-4.952 7.923a1 1 0 01-1.464.236l-3.212-2.529a1 1 0 01-.304-1.12z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else-if="verificationStatus[row.id] === 'invalid'" xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  <span>{{ getVerificationText(row.id) }}</span>
                </button>
              </template>
              <template #cell-details="{ row }">
                <button
                  @click="showDetailsModal(row)"
                  class="text-blue-600 hover:text-blue-700 font-extrabold text-[11px] hover:underline cursor-pointer"
                >
                  عرض التعديلات &larr;
                </button>
              </template>
            </DataTable>
          </div>

          <!-- Pagination -->
          <div class="flex items-center justify-between border-t border-gray-100 dark:border-gray-800 pt-4 text-xs">
            <span class="text-gray-500">
              الصفحة {{ auditStore.systemLogsPage }} من {{ auditStore.systemLogsTotalPages }}
            </span>
            <div class="flex items-center gap-2">
              <button
                :disabled="auditStore.systemLogsPage === 1"
                @click="changePage(auditStore.systemLogsPage - 1)"
                class="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-50 disabled:opacity-50 cursor-pointer"
              >
                السابق
              </button>
              <button
                :disabled="auditStore.systemLogsPage === auditStore.systemLogsTotalPages"
                @click="changePage(auditStore.systemLogsPage + 1)"
                class="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-50 disabled:opacity-50 cursor-pointer"
              >
                التالي
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Log Details Modal (JSON Diff Viewer) -->
    <div 
      v-if="selectedLog"
      class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-[9999] animate-fade-in"
      dir="rtl"
    >
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-850 rounded-2xl max-w-4xl w-full max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
        <!-- Modal Header -->
        <div class="p-4 bg-gray-50 dark:bg-gray-950 border-b border-gray-200 dark:border-gray-850 flex justify-between items-center">
          <div>
            <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
              <span>تفاصيل التغيير للسجل الرقم:</span>
              <span class="font-mono bg-blue-500/10 text-blue-600 px-2 py-0.5 rounded-lg text-xs">{{ selectedLog.id }}</span>
            </h3>
            <div class="text-[10px] text-gray-400 mt-0.5">
              بواسطة {{ selectedLog.username }} في {{ formatDate(selectedLog.timestamp) }}
            </div>
          </div>
          <button 
            @click="selectedLog = null"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-1.5 rounded-lg hover:bg-gray-200/50 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Modal Body (Diff Columns) -->
        <div class="p-6 overflow-y-auto space-y-4">
          <!-- Change Justification -->
          <div class="p-3.5 rounded-xl bg-amber-500/5 border border-amber-500/15 text-xs text-amber-800 dark:text-amber-300">
            <span class="font-black block mb-1">مبرر التغيير المدخل:</span>
            <span>{{ selectedLog.change_reason || 'لا يوجد مبرر مدخل لهذه العملية.' }}</span>
          </div>

          <!-- Side-by-Side Diff -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Old Data -->
            <div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden bg-gray-50/50 dark:bg-gray-950/40">
              <div class="bg-gray-100/80 dark:bg-gray-900 px-3 py-2 text-xs font-bold text-gray-500 border-b border-gray-200 dark:border-gray-800">
                البيانات السابقة (قبل التعديل)
              </div>
              <div class="p-4 font-mono text-[10px] text-gray-600 dark:text-gray-300 overflow-x-auto whitespace-pre max-h-[300px] text-left">
                {{ formatJson(selectedLog.old_data) }}
              </div>
            </div>

            <!-- New Data -->
            <div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden bg-gray-50/50 dark:bg-gray-950/40">
              <div class="bg-gray-100/80 dark:bg-gray-900 px-3 py-2 text-xs font-bold text-gray-500 border-b border-gray-200 dark:border-gray-800">
                البيانات الجديدة (بعد التعديل)
              </div>
              <div class="p-4 font-mono text-[10px] text-gray-600 dark:text-gray-300 overflow-x-auto whitespace-pre max-h-[300px] text-left">
                {{ formatJson(selectedLog.new_data) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-4 bg-gray-50 dark:bg-gray-950 border-t border-gray-200 dark:border-gray-850 flex justify-end">
          <button 
            @click="selectedLog = null"
            class="px-5 py-2 rounded-xl bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 font-extrabold text-xs cursor-pointer"
          >
            إغلاق النافذة
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import { useAuditStore } from '@/stores/audit'
import Swal from 'sweetalert2'

const auditColumns = [
  { key: 'timestamp', label: 'التوقيت', sortable: true },
  { key: 'user', label: 'المستخدم', sortable: true },
  { key: 'action', label: 'الحدث / العملية', sortable: true },
  { key: 'model', label: 'النموذج المتأثر', sortable: true },
  { key: 'reason', label: 'مبرر التغيير', sortable: true },
  { key: 'severity', label: 'مستوى الأمان', sortable: true },
  { key: 'signature', label: 'التوقيع الرقمي', sortable: false },
  { key: 'details', label: 'التفاصيل', sortable: false }
]

const auditStore = useAuditStore()
const selectedLog = ref<any>(null)

const filters = ref({
  search: '',
  module: '',
  action: '',
  severity: '',
})

const verificationStatus = ref<Record<number, 'unchecked' | 'checking' | 'valid' | 'invalid'>>({})

async function loadLogs() {
  const params: Record<string, string> = {}
  if (filters.value.search) params.search = filters.value.search
  if (filters.value.module) params.module = filters.value.module
  if (filters.value.action) params.action = filters.value.action
  if (filters.value.severity) params.severity = filters.value.severity
  
  await auditStore.fetchSystemLogs(params)
}

function handleFilterChange() {
  auditStore.systemLogsPage = 1
  loadLogs()
}

function resetFilters() {
  filters.value = {
    search: '',
    module: '',
    action: '',
    severity: '',
  }
  auditStore.systemLogsPage = 1
  loadLogs()
}

async function changePage(page: number) {
  auditStore.systemLogsPage = page
  await loadLogs()
}

async function handleVerifySignature(log: any) {
  verificationStatus.value[log.id] = 'checking'
  try {
    const res = await auditStore.verifySignature(log.id)
    if (res.success && res.data?.is_verified) {
      verificationStatus.value[log.id] = 'valid'
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'السجل سليم رقمياً ومطابق للتوقيع المعتمد',
        showConfirmButton: false,
        timer: 3000
      })
    } else {
      verificationStatus.value[log.id] = 'invalid'
      Swal.fire('تحذير أمني خطير', '⚠️ تم اكتشاف عدم تطابق التوقيع الرقمي مع محتوى السجل! قد يكون هناك تلاعب مباشر بقاعدة البيانات.', 'warning')
    }
  } catch (err) {
    verificationStatus.value[log.id] = 'unchecked'
    Swal.fire('خطأ', 'فشل التحقق من التوقيع الرقمي', 'error')
  }
}

function getVerificationText(id: number): string {
  const status = verificationStatus.value[id]
  if (status === 'valid') return 'سليم وموقع'
  if (status === 'invalid') return 'تلاعب مكتشف!'
  if (status === 'checking') return 'جاري الفحص...'
  return 'تحقق من التوقيع'
}

function showDetailsModal(log: any) {
  selectedLog.value = log
}

function getActionClass(action: string): string {
  const classes: Record<string, string> = {
    CREATE: 'bg-emerald-500/10 text-emerald-600',
    UPDATE: 'bg-blue-500/10 text-blue-600',
    DELETE: 'bg-red-500/10 text-red-600',
    APPROVE: 'bg-purple-500/10 text-purple-600',
    REJECT: 'bg-amber-500/10 text-amber-600',
    EXPORT: 'bg-indigo-500/10 text-indigo-600',
  }
  return classes[action] || 'bg-gray-500/10 text-gray-600'
}

function getSeverityClass(severity: string): string {
  const classes: Record<string, string> = {
    info: 'bg-gray-500/10 text-gray-600 dark:text-gray-400',
    low: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
    medium: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
    high: 'bg-orange-500/10 text-orange-600 dark:text-orange-400',
    critical: 'bg-red-500/15 text-red-600 dark:text-red-400 animate-pulse',
  }
  return classes[severity] || 'bg-gray-500/10 text-gray-600'
}

function getSeverityLabel(severity: string): string {
  const labels: Record<string, string> = {
    info: 'معلومات',
    low: 'منخفض',
    medium: 'متوسط',
    high: 'عالي',
    critical: 'حرج',
  }
  return labels[severity] || severity
}

function formatJson(data: any): string {
  if (!data) return '{\n  "empty": true\n}'
  if (typeof data === 'string') {
    try {
      return JSON.stringify(JSON.parse(data), null, 2)
    } catch {
      return data
    }
  }
  return JSON.stringify(data, null, 2)
}

function formatDate(dateStr: string): string {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleString('ar-YE', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

onMounted(() => {
  loadLogs()
})
</script>
