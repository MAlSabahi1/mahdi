<template>
  <admin-layout>
    <div class="space-y-6">
      
      <!-- Page Header -->
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('settlements.title') }}</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ $t('settlements.description') }}</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="fetchData" class="rounded-lg border border-gray-200 bg-white p-2.5 text-gray-500 hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 transition-colors">
            <svg class="h-5 w-5" :class="{'animate-spin': store.loading}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
        
        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-start text-sm text-gray-500 dark:text-gray-400">
            <thead class="bg-gray-50 text-xs uppercase text-gray-700 dark:bg-gray-800/50 dark:text-gray-300">
              <tr>
                <th scope="col" class="px-6 py-4 font-semibold">{{ $t('personnel.military_number') }}</th>
                <th scope="col" class="px-6 py-4 font-semibold">{{ $t('personnel.full_name') }}</th>
                <th scope="col" class="px-6 py-4 font-semibold">{{ $t('settlements.settlement_type') }}</th>
                <th scope="col" class="px-6 py-4 font-semibold text-center">{{ $t('settlements.from_rank') }}</th>
                <th scope="col" class="px-6 py-4 font-semibold text-center">{{ $t('settlements.to_rank') }}</th>
                <th scope="col" class="px-6 py-4 font-semibold">{{ $t('settlements.decision_number') }}</th>
                <th scope="col" class="px-6 py-4 font-semibold text-end">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
              <!-- Loading Skeleton -->
              <tr v-if="store.loading && store.pendingSettlements.length === 0">
                <td colspan="7" class="px-6 py-8">
                  <div class="flex justify-center">
                    <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                    </svg>
                  </div>
                </td>
              </tr>

              <!-- Empty State -->
              <tr v-else-if="store.pendingSettlements.length === 0">
                <td colspan="7" class="px-6 py-12 text-center">
                  <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                    <svg class="h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                  </div>
                  <h3 class="mt-4 text-sm font-medium text-gray-900 dark:text-white">{{ $t('settlements.empty_state') }}</h3>
                </td>
              </tr>

              <!-- Data Rows -->
              <tr v-for="item in store.pendingSettlements" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                  {{ item.personnel_military_number }}
                </td>
                <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                  {{ item.personnel_name }}
                  <div class="text-xs text-gray-500 font-normal mt-0.5" v-if="item.requested_by_name">
                    مقدم الطلب: {{ item.requested_by_name }}
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold"
                    :class="getTypeColor(item.settlement_type)">
                    {{ $t(`settlements.types.${item.settlement_type}`) }}
                  </span>
                  <div v-if="item.settlement_type === 'personnel_to_officer'" class="text-xs text-brand-600 dark:text-brand-400 mt-1">
                    الرقم الجديد: {{ item.new_military_number || 'غير محدد' }}
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <span class="inline-block px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded text-xs">
                    {{ item.from_rank_name || '؟' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <svg class="h-4 w-4 mx-auto text-gray-400 mb-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                  <span class="inline-block px-2 py-1 bg-brand-50 text-brand-700 dark:bg-brand-500/20 dark:text-brand-400 font-bold rounded text-xs border border-brand-200 dark:border-brand-800/50">
                    {{ item.to_rank_name || '؟' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-xs">
                  <div>{{ item.decision_number || '—' }}</div>
                  <div class="text-gray-400">{{ item.decision_date || '—' }}</div>
                </td>
                <td class="px-6 py-4 text-end">
                  <div class="flex items-center justify-end gap-2">
                    <button @click="confirmApply(item)" :disabled="actionLoading" class="inline-flex items-center justify-center rounded-lg bg-success-50 text-success-700 p-2 hover:bg-success-100 dark:bg-success-500/10 dark:text-success-400 dark:hover:bg-success-500/20 transition-colors disabled:opacity-50" title="اعتماد التسوية">
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                    <button @click="openRejectModal(item)" :disabled="actionLoading" class="inline-flex items-center justify-center rounded-lg bg-error-50 text-error-700 p-2 hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors disabled:opacity-50" title="رفض التسوية">
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div v-if="store.totalPages > 1" class="border-t border-gray-100 px-6 py-4 dark:border-gray-800">
          <div class="flex items-center justify-between">
            <p class="text-sm text-gray-700 dark:text-gray-400">
              إجمالي الطلبات: <span class="font-medium">{{ store.totalCount }}</span>
            </p>
            <div class="flex gap-2">
              <button 
                @click="changePage(store.currentPage - 1)" 
                :disabled="store.currentPage === 1"
                class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                السابق
              </button>
              <button 
                @click="changePage(store.currentPage + 1)" 
                :disabled="store.currentPage === store.totalPages"
                class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                التالي
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 print-hide">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-gray-900/50 transition-opacity dark:bg-gray-900/80" @click="showRejectModal = false"></div>
      
      <!-- Modal Content -->
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-start align-middle shadow-xl transition-all dark:bg-gray-900 border border-gray-100 dark:border-gray-800">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
          رفض طلب التسوية
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
          يرجى إدخال سبب الرفض لتسوية الرتبة للفرد ({{ selectedSettlement?.personnel_name }}).
        </p>
        
        <textarea v-model="rejectionReason" v-field-error="'rejectionReason'" rows="3" required class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 focus:border-error-500 focus:ring-error-500 dark:border-gray-700 dark:text-white" placeholder="سبب الرفض..."></textarea>
        
        <div class="mt-6 flex justify-end gap-3">
          <button @click="showRejectModal = false" class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
            إلغاء
          </button>
          <button @click="submitReject" :disabled="actionLoading" class="rounded-lg bg-error-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-error-700 transition-colors disabled:opacity-50 flex items-center gap-2">
            <svg v-if="actionLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            تأكيد الرفض
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useRankSettlementStore, type RankSettlement } from '@/stores/rankSettlement'
import Swal from 'sweetalert2'
import { validateFormFields } from '@/stores/validation'

const { t } = useI18n()
const store = useRankSettlementStore()

const actionLoading = ref(false)
const showRejectModal = ref(false)
const selectedSettlement = ref<RankSettlement | null>(null)
const rejectionReason = ref('')

onMounted(() => {
  fetchData()
})

async function fetchData(page: number | Event = 1) {
  const pageNum = typeof page === 'number' ? page : 1
  try {
    await store.fetchAllPendingSettlements({ page: pageNum })
  } catch (e) {
    // Error is handled globally
  }
}

function changePage(page: number) {
  fetchData(page)
}

function getTypeColor(type: string) {
  switch (type) {
    case 'same_class_promotion':
      return 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400'
    case 'personnel_to_officer':
      return 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400'
    case 'demotion':
      return 'bg-orange-50 text-orange-700 dark:bg-orange-500/10 dark:text-orange-400'
    default:
      return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
  }
}

async function confirmApply(item: RankSettlement) {
  const result = await Swal.fire({
    title: t('settlements.confirm_apply'),
    text: `ستقوم بتحديث بيانات الفرد (${item.personnel_name}) إلى الرتبة الجديدة (${item.to_rank_name}).`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#10B981', // success color
    cancelButtonColor: '#6B7280',
    confirmButtonText: 'نعم، اعتماد',
    cancelButtonText: 'إلغاء'
  })

  if (result.isConfirmed) {
    actionLoading.value = true
    try {
      await store.applySettlement(item.id)
      Swal.fire({
        toast: true, position: 'top-end',
        icon: 'success', title: 'تم اعتماد التسوية بنجاح',
        showConfirmButton: false, timer: 3000
      })
      fetchData(store.currentPage)
    } catch (e) {
      // Global error handler will catch this
    } finally {
      actionLoading.value = false
    }
  }
}

function openRejectModal(item: RankSettlement) {
  selectedSettlement.value = item
  rejectionReason.value = ''
  showRejectModal.value = true
}

async function submitReject() {
  if (!validateFormFields()) return

  if (!selectedSettlement.value) return
  
  actionLoading.value = true
  try {
    await store.rejectSettlement(selectedSettlement.value.id, rejectionReason.value)
    Swal.fire({
      toast: true, position: 'top-end',
      icon: 'success', title: 'تم رفض طلب التسوية',
      showConfirmButton: false, timer: 3000
    })
    showRejectModal.value = false
    fetchData(store.currentPage)
  } catch (e) {
    // Global error handler
  } finally {
    actionLoading.value = false
  }
}
</script>
