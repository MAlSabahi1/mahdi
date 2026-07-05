<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('settlements.title') || 'تسويات رتب الأفراد'" />
    <div class="space-y-6">
      
      <!-- Data Table -->
      <BasicTable
        :columns="tableColumns"
        :data="filteredSettlements"
        row-key="id"
        :loading="store.loading"
        :has-actions="true"
        actions-width="120px"
        :empty-title="$t('settlements.empty_state') || 'لا توجد طلبات تسوية'"
        :empty-description="$t('settlements.empty_state_desc') || 'جميع طلبات تسوية الرتب تم البت فيها بنجاح.'"
      >
        <!-- Table Header Toolbar -->
        <template #header>
          <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 w-full">
            <!-- Search -->
            <div class="relative w-full sm:max-w-xs shrink-0">
              <div class="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-3">
                <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="$t('settlements.search_placeholder') || 'بحث باسم الفرد أو الرقم العسكري...'"
                class="w-full h-10 rounded-lg border border-gray-300 bg-gray-50 py-2 ps-9 pe-8 text-theme-sm text-gray-900 placeholder-gray-400 focus:border-brand-300 focus:bg-white focus:ring-2 focus:ring-brand-500/10 focus:outline-none dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500 transition-all"
              />
            </div>
            
            <div class="flex justify-end gap-3 flex-wrap">
              <button
                @click="fetchData"
                class="flex h-10 items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <svg class="h-4.5 w-4.5 text-gray-500" :class="{'animate-spin': store.loading}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {{ $t('common.refresh') || 'تحديث' }}
              </button>
            </div>
          </div>
        </template>

        <template #cell-military_number="{ row }">
          <span class="font-medium text-gray-900 dark:text-white">{{ row.personnel_military_number }}</span>
        </template>

        <template #cell-full_name="{ row }">
          <span class="font-medium text-gray-900 dark:text-white">{{ row.personnel_name }}</span>
          <div class="text-xs text-gray-500 font-normal mt-0.5" v-if="row.requested_by_name">
            {{ $t('settlements.requester') || 'مقدم الطلب' }}: {{ row.requested_by_name }}
          </div>
        </template>

        <template #cell-settlement_type="{ row }">
          <span class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold"
            :class="getTypeColor(row.settlement_type)">
            {{ $t(`settlements.types.${row.settlement_type}`) }}
          </span>
          <div v-if="row.settlement_type === 'personnel_to_officer'" class="text-xs text-brand-600 dark:text-brand-400 mt-1">
            {{ $t('settlements.new_number') || 'الرقم الجديد' }}: {{ row.new_military_number || $t('personnel.unspecified') || 'غير محدد' }}
          </div>
        </template>

        <template #cell-from_rank="{ row }">
          <span class="inline-block px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded text-xs">
            {{ row.from_rank_name || '؟' }}
          </span>
        </template>

        <template #cell-to_rank="{ row }">
          <svg class="h-4 w-4 mx-auto text-gray-400 mb-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
          <span class="inline-block px-2 py-1 bg-brand-50 text-brand-700 dark:bg-brand-500/20 dark:text-brand-400 font-bold rounded text-xs border border-brand-200 dark:border-brand-800/50">
            {{ row.to_rank_name || '؟' }}
          </span>
        </template>

        <template #cell-decision_number="{ row }">
          <div>{{ row.decision_number || '—' }}</div>
          <div class="text-gray-400">{{ row.decision_date || '—' }}</div>
        </template>

        <template #actions="{ row }">
          <button @click="confirmApply(row)" :disabled="actionLoading" class="inline-flex items-center justify-center rounded-lg bg-success-50 text-success-700 p-2 hover:bg-success-100 dark:bg-success-500/10 dark:text-success-400 dark:hover:bg-success-500/20 transition-colors disabled:opacity-50" :title="$t('personnel.approve') || 'اعتماد'">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </button>
          <button @click="openRejectModal(row)" :disabled="actionLoading" class="inline-flex items-center justify-center rounded-lg bg-error-50 text-error-700 p-2 hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors disabled:opacity-50" :title="$t('personnel.reject') || 'رفض'">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </template>

        <template #footer>
          <TablePagination
            v-if="!store.loading && store.totalCount > 0"
            :currentPage="store.currentPage"
            :totalPages="store.totalPages"
            :totalCount="store.totalCount"
            :pageSize="store.pageSize || 15"
            :visiblePages="computedVisiblePages"
            @change-page="changePage"
          />
        </template>
      </BasicTable>
    </div>

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 print-hide">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-gray-900/50 transition-opacity dark:bg-gray-900/80" @click="showRejectModal = false"></div>
      
      <!-- Modal Content -->
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-start align-middle shadow-xl transition-all dark:bg-gray-900 border border-gray-100 dark:border-gray-800">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
          {{ $t('settlements.reject_modal_title') || 'رفض طلب التسوية' }}
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
          {{ $t('settlements.reject_modal_desc', { name: selectedSettlement?.personnel_name }) || `يرجى إدخال سبب الرفض لتسوية الرتبة للفرد (${selectedSettlement?.personnel_name}).` }}
        </p>
        
        <textarea v-model="rejectionReason" v-field-error="'rejectionReason'" rows="3" required class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 focus:border-error-500 focus:ring-error-500 dark:border-gray-700 dark:text-white" :placeholder="$t('settlements.reject_reason_placeholder') || 'سبب الرفض...'"></textarea>
        
        <div class="mt-6 flex justify-end gap-3">
          <button @click="showRejectModal = false" class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
            {{ $t('common.cancel') || 'إلغاء' }}
          </button>
          <button @click="submitReject" :disabled="actionLoading" class="rounded-lg bg-error-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-error-700 transition-colors disabled:opacity-50 flex items-center gap-2">
            <svg v-if="actionLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ $t('settlements.confirm_reject_btn') || 'تأكيد الرفض' }}
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import BasicTable from '@/components/tables/BasicTable.vue'
import TablePagination from '@/components/common/TablePagination.vue'
import { useRankSettlementStore, type RankSettlement } from '@/stores/rankSettlement'
import Swal from 'sweetalert2'
import { validateFormFields } from '@/stores/validation'

const { t } = useI18n()
const store = useRankSettlementStore()

const tableColumns = [
  { key: 'military_number', label: t('personnel.military_number') || 'الرقم العسكري' },
  { key: 'full_name', label: t('personnel.full_name') || 'الاسم' },
  { key: 'settlement_type', label: t('settlements.settlement_type') || 'نوع التسوية' },
  { key: 'from_rank', label: t('settlements.from_rank') || 'من رتبة', class: 'text-center', tdClass: 'text-center' },
  { key: 'to_rank', label: t('settlements.to_rank') || 'إلى رتبة', class: 'text-center', tdClass: 'text-center' },
  { key: 'decision_number', label: t('settlements.decision_number') || 'رقم القرار' }
]

const computedVisiblePages = computed((): (number | string)[] => {
  const total = store.totalPages || 1
  const current = store.currentPage || 1
  const pages: (number | string)[] = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

const actionLoading = ref(false)
const showRejectModal = ref(false)
const selectedSettlement = ref<RankSettlement | null>(null)
const rejectionReason = ref('')

const searchQuery = ref('')
const filteredSettlements = computed(() => {
  if (!searchQuery.value) return store.pendingSettlements
  const q = searchQuery.value.toLowerCase()
  return store.pendingSettlements.filter((r: any) => 
    (r.personnel_name && r.personnel_name.toLowerCase().includes(q)) ||
    (r.personnel_military_number && r.personnel_military_number.includes(q)) ||
    (r.decision_number && String(r.decision_number).toLowerCase().includes(q))
  )
})

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
    title: t('settlements.confirm_apply_title') || 'تأكيد الاعتماد',
    text: t('settlements.confirm_apply_text', { name: item.personnel_name, rank: item.to_rank_name }) || `ستقوم بتحديث بيانات الفرد (${item.personnel_name}) إلى الرتبة الجديدة (${item.to_rank_name}).`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#10B981', // success color
    cancelButtonColor: '#6B7280',
    confirmButtonText: t('settlements.yes_apply') || 'نعم، اعتماد',
    cancelButtonText: t('common.cancel') || 'إلغاء'
  })

  if (result.isConfirmed) {
    actionLoading.value = true
    try {
      await store.applySettlement(item.id)
      Swal.fire({
        toast: true, position: 'top-end',
        icon: 'success', title: t('settlements.apply_success') || 'تم اعتماد التسوية بنجاح',
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
      icon: 'success', title: t('settlements.reject_success') || 'تم رفض طلب التسوية',
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
