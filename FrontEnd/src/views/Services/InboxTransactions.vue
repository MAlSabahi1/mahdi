<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="قائمة المعاملات والمهام الجارية" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-3">
          قائمة المعاملات والمهام (Transactions Inbox)
          <span v-if="filterType" class="text-[10px] bg-brand-50 text-brand-600 border border-brand-100 dark:bg-brand-950/30 dark:border-brand-900 px-3 py-1 rounded-full flex items-center gap-2">
            مفلتر بنوع الخدمة: {{ filterType }}
            <RouterLink to="/services/inbox" class="hover:text-red-500 font-bold ml-1">×</RouterLink>
          </span>
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          إدارة طلبات المعاملات وكروت الخدمات المرفوعة من المديريات، واعتمادها أو رفضها أو إقفالها نهائياً.
        </p>
      </div>

      <!-- Stats Cards (#10) -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="stat in inboxStats" :key="stat.label" class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-sm">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">{{ stat.label }}</p>
          <div class="flex items-center justify-between">
            <p class="text-2xl font-black text-gray-900 dark:text-white font-mono">{{ stat.value }}</p>
            <span :class="stat.dotClass" class="h-3 w-3 rounded-full"></span>
          </div>
        </div>
      </div>

      <!-- Transactions Table Grid -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="p-5 border-b border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <h3 class="text-sm font-black text-gray-900 dark:text-white">جدول مراجعة الطلبات والاعتمادات الجارية</h3>
            <p class="text-[10px] text-gray-400 mt-0.5">الطلبات الحالية التي تتطلب المراجعة الفنية واعتماد لجان شؤون الأفراد والخدمات.</p>
          </div>
          
          <div class="flex gap-2">
            <select v-model="filterStatus" class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option value="all">جميع الحالات</option>
              <option value="in_progress">قيد الإجراء بانتظار الاعتماد</option>
              <option value="approved">المعتمدة تاريخياً</option>
              <option value="rejected">المرفوضة</option>
              <option value="returned">المُرجعة للتعديل</option>
            </select>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-450 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-5 py-3 w-[120px]">رقم المعاملة</th>
                <th class="px-5 py-3">نوع كرت الخدمة</th>
                <th class="px-5 py-3">تاريخ التقديم</th>
                <th class="px-5 py-3">المديرية المصدرة</th>
                <th class="px-5 py-3">الحالة الحالية</th>
                <th class="px-5 py-3 text-center w-[180px]">العمليات والإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr v-if="displayedForms.length === 0">
                <td colspan="6" class="px-5 py-12 text-center text-gray-400 dark:text-gray-500">
                  لا توجد معاملات جارية بانتظار المراجعة والاعتماد حالياً.
                </td>
              </tr>
              <tr v-for="tx in displayedForms" :key="tx.id" class="hover:bg-gray-50/50 dark:hover:bg-gray-950/30">
                <td class="px-5 py-3 font-mono font-bold">
                  <RouterLink :to="`/services/forms/${tx.id}`" class="text-brand-600 hover:text-brand-700 hover:underline">
                    {{ tx.id }}
                  </RouterLink>
                </td>
                <td class="px-5 py-3 font-bold text-gray-800 dark:text-gray-200">{{ tx.form_type_display || tx.form_type }}</td>
                <td class="px-5 py-3 font-mono text-gray-450">{{ tx.submitted_at ? new Date(tx.submitted_at).toLocaleDateString('en-GB') : '-' }}</td>
                <td class="px-5 py-3">{{ tx.personnel?.full_name || tx.personnel_details?.full_name || tx.personnel }}</td>
                <td class="px-5 py-3 min-w-[200px]">
                  <!-- عرض تقدم المراحل (Progress Stepper) -->
                  <div v-if="tx.status === 'in_progress' && tx.all_steps && tx.all_steps.length > 0" class="w-full">
                    <div class="flex items-center gap-1 mb-1.5 justify-between">
                      <span class="text-[10px] font-bold text-gray-700 dark:text-gray-300">
                        مرحلة {{ tx.current_step_index + 1 }} من {{ tx.all_steps.length }}
                      </span>
                      <span class="text-[9px] text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-400 px-1.5 py-0.5 rounded font-bold">
                        بانتظار: {{ tx.current_step_name }}
                      </span>
                    </div>
                    <div class="flex items-center gap-1 w-full" :title="'المراحل: ' + tx.all_steps.join(' ← ')">
                      <div 
                        v-for="(step, idx) in tx.all_steps" 
                        :key="idx"
                        class="h-1.5 flex-1 rounded-full transition-colors duration-300"
                        :class="[
                          idx < tx.current_step_index ? 'bg-emerald-500' : 
                          idx === tx.current_step_index ? 'bg-blue-500 animate-pulse' : 'bg-gray-200 dark:bg-gray-700'
                        ]"
                      ></div>
                    </div>
                  </div>
                  <!-- الحالة العادية (في حال لم يكن هناك مراحل أو حالة أخرى) -->
                  <span v-else :class="getStatusColor(tx.status)" class="inline-flex items-center gap-1 rounded px-2.5 py-0.5 text-[10px] font-bold">
                    <span :class="getStatusDot(tx.status)" class="h-1.5 w-1.5 rounded-full"></span>
                    {{ getStatusLabel(tx.status, tx.current_step_name) }}
                  </span>
                </td>
                <td class="px-5 py-3 flex items-center justify-center gap-2">
                  <button 
                    v-if="tx.status === 'in_progress'"
                    @click="approveTx(tx)"
                    class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded transition-colors cursor-pointer"
                  >
                    اعتماد
                  </button>
                  <button 
                    v-if="tx.status === 'in_progress'"
                    @click="rejectTx(tx)"
                    class="bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold px-2.5 py-1 rounded transition-colors cursor-pointer"
                  >
                    رفض
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'
import { useServicesStore } from '@/stores/services'
import { useRoute } from 'vue-router'

const route = useRoute()
const servicesStore = useServicesStore()
const filterStatus = ref('all')
const filterType = ref(route.query.type as string || '')
const allForms = ref<any[]>([])

const displayedForms = computed(() => {
  if (filterStatus.value === 'all') return allForms.value
  return allForms.value.filter(f => f.status === filterStatus.value)
})

onMounted(async () => {
  // If there's a type in query, we default to all statuses to see them
  if (filterType.value) {
    filterStatus.value = 'all'
  } else {
    filterStatus.value = 'in_progress'
  }
  fetchAllData()
})

watch(() => route.query.type, (newType) => {
  filterType.value = newType as string || ''
  fetchAllData()
})

async function fetchAllData() {
  try {
    const q: any = {}
    if (filterType.value) q.type = filterType.value // Use type instead of form_type
    
    // Pass page sizes or leave as default, the backend handles it.
    const res = await servicesStore.fetchForms(q)
    // Directly use the API response results so it doesn't flash all forms
    allForms.value = res?.results || res || []
  } catch { /* ignore */ }
}

// #10 — Stats Cards
const inboxStats = computed(() => {
  const forms = allForms.value
  return [
    { label: 'مسودات (Draft)', value: forms.filter((f: any) => f.status === 'draft').length, dotClass: 'bg-gray-400' },
    { label: 'قيد الإجراء (In Progress)', value: forms.filter((f: any) => f.status === 'in_progress').length, dotClass: 'bg-blue-500' },
    { label: 'معتمدة نهائياً', value: forms.filter((f: any) => f.status === 'approved').length, dotClass: 'bg-emerald-500' },
    { label: 'مرفوضة / مُرجعة', value: forms.filter((f: any) => f.status === 'rejected' || f.status === 'returned').length, dotClass: 'bg-red-500' },
  ]
})

async function approveTx(tx: any) {
  Swal.fire({
    title: 'اعتماد المعاملة وتمريرها للمرحلة التالية؟',
    text: `أنت بصدد الموافقة على المعاملة في مرحلة (${tx.current_step_name || 'الاعتماد'}).`,
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتماد الكرت',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981'
  }).then(async (result) => {
    if (result.isConfirmed) {
      await servicesStore.approveForm(tx.id)
      fetchAllData()
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة بنجاح', showConfirmButton: false, timer: 2000 })
    }
  })
}

async function rejectTx(tx: any) {
  Swal.fire({
    title: 'رفض المعاملة وإحالتها لسجل المرفوضات؟',
    text: `الرجاء كتابة سبب الرفض:`,
    input: 'text',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444'
  }).then(async (result) => {
    if (result.isConfirmed && result.value) {
      await servicesStore.rejectForm(tx.id, result.value)
      fetchAllData()
      Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض المعاملة', showConfirmButton: false, timer: 2000 })
    }
  })
}

function getStatusLabel(status: string, stepName?: string) {
  if (status === 'in_progress') return `بانتظار: ${stepName || 'المراجعة'}`
  const map: any = {
    'draft': 'مسودة',
    'approved': 'معتمد نهائياً',
    'rejected': 'مرفوض',
    'returned': 'مُرجع للتعديل'
  }
  return map[status] || status
}

// #12 — Dynamic status colors
function getStatusColor(status: string) {
  const colors: any = {
    'draft': 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    'in_progress': 'bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400',
    'approved': 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/20 dark:text-emerald-400',
    'rejected': 'bg-red-50 text-red-700 dark:bg-red-950/20 dark:text-red-400',
    'returned': 'bg-orange-50 text-orange-700 dark:bg-orange-950/20 dark:text-orange-400',
  }
  return colors[status] || 'bg-gray-100 text-gray-600'
}

function getStatusDot(status: string) {
  const dots: any = {
    'draft': 'bg-gray-400',
    'in_progress': 'bg-blue-500',
    'approved': 'bg-emerald-500',
    'rejected': 'bg-red-500',
    'returned': 'bg-orange-500',
  }
  return dots[status] || 'bg-gray-400'
}
</script>
