<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('personnel.manage_corrections') || 'إدارة طلبات التصحيح'" />
    <div class="space-y-6">



      <!-- Data Table -->
      <BasicTable
        :columns="tableColumns"
        :data="filteredRequests"
        row-key="id"
        :loading="loading"
        :has-actions="true"
        actions-width="120px"
        :empty-title="$t('corrections.no_requests') || 'لا توجد طلبات معلقة'"
        :empty-description="$t('corrections.no_requests_desc') || 'جميع طلبات تصحيح البيانات تم البت فيها بنجاح.'"
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
                :placeholder="$t('corrections.search_placeholder') || 'بحث باسم الفرد أو الرقم العسكري...'"
                class="w-full h-10 rounded-lg border border-gray-300 bg-gray-50 py-2 ps-9 pe-8 text-theme-sm text-gray-900 placeholder-gray-400 focus:border-brand-300 focus:bg-white focus:ring-2 focus:ring-brand-500/10 focus:outline-none dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500 transition-all"
              />
            </div>
            
            <div class="flex justify-end gap-3 flex-wrap">
              <!-- Batch Actions Toolbar -->
              <div v-if="selectedIds.length > 0" class="flex items-center gap-3 bg-gray-50 px-4 py-1.5 rounded-lg border border-gray-200 dark:bg-gray-800 dark:border-gray-700 shadow-theme-xs">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ selectedIds.length }} {{ $t('common.selected') || 'محدد' }}</span>
                <div class="h-4 w-px bg-gray-300 dark:bg-gray-600"></div>
                <button @click="showBatchApproveModal = true" class="text-sm bg-success-50 text-success-700 px-3 py-1 rounded-md hover:bg-success-100 dark:bg-success-500/10 dark:text-success-400 dark:hover:bg-success-500/20 transition-colors font-medium cursor-pointer">{{ $t('common.batch_approve') || 'موافقة جماعية' }}</button>
                <button @click="openBatchRejectModal" class="text-sm bg-error-50 text-error-700 px-3 py-1 rounded-md hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors font-medium cursor-pointer">{{ $t('common.batch_reject') || 'رفض جماعي' }}</button>
              </div>

              <button
                @click="loadCorrections"
                class="flex h-10 items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <svg class="h-4.5 w-4.5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {{ $t('common.refresh') || 'تحديث' }}
              </button>
            </div>
          </div>
        </template>

        <!-- Header Checkbox -->
        <template #header-checkbox>
          <input type="checkbox" v-model="selectAll" class="rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-brand-500" />
        </template>

        <!-- Cell Checkbox -->
        <template #cell-checkbox="{ row }">
          <input type="checkbox" :value="row.id" v-model="selectedIds" class="rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-brand-500" />
        </template>

        <!-- Cell Personnel -->
        <template #cell-personnel="{ row }">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400 font-bold">
              {{ row.personnel_name?.substring(0, 1) || '؟' }}
            </div>
            <div>
              <div class="text-sm font-medium text-gray-900 dark:text-white">
                <RouterLink :to="`/personnel/${row.military_number}`" class="hover:text-brand-500 transition-colors">
                  {{ row.personnel_name || $t('personnel.unspecified') || 'غير محدد' }}
                </RouterLink>
              </div>
              <div class="text-xs text-gray-500 flex items-center gap-2 mt-0.5">
                <span>{{ row.military_number }}</span>
                <span class="inline-block h-1 w-1 rounded-full bg-gray-300 dark:bg-gray-600"></span>
                <span>{{ row.personnel_rank || $t('personnel.unspecified') || 'غير محدد' }}</span>
              </div>
            </div>
          </div>
        </template>

        <!-- Cell Field -->
        <template #cell-field="{ row }">
          <span class="inline-flex items-center rounded-md bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-800 dark:bg-gray-800 dark:text-gray-300 border border-gray-200 dark:border-gray-700">
            {{ getFieldLabel(row.field) }}
          </span>
          <div v-if="row.requested_by_name" class="mt-1.5 text-xs text-gray-500 flex items-center gap-1">
            <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ $t('corrections.by') || 'بواسطة' }}: {{ row.requested_by_name }}
          </div>
        </template>

        <!-- Cell Old Value -->
        <template #cell-old_value="{ row }">
          <div class="text-sm text-gray-500 dark:text-gray-400 line-through decoration-error-500/50">
            {{ row.old_value || $t('corrections.empty_val') || 'فارغ' }}
          </div>
        </template>

        <!-- Cell New Value -->
        <template #cell-new_value="{ row }">
          <div class="text-sm font-medium text-success-600 dark:text-success-400 flex items-center gap-1.5">
            <svg class="h-4 w-4 shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
            {{ row.new_value }}
          </div>
        </template>

        <!-- Cell Requested At -->
        <template #cell-requested_at="{ row }">
          <div class="text-sm text-gray-900 dark:text-white">{{ formatDate(row.requested_at) }}</div>
        </template>

        <!-- Actions -->
        <template #actions="{ row }">
          <div class="flex items-center gap-2">
            <button
              @click="openApproveModal(row)"
              class="flex items-center justify-center rounded-lg bg-success-50 p-2 text-success-600 hover:bg-success-100 dark:bg-success-500/10 dark:text-success-400 dark:hover:bg-success-500/20 transition-colors cursor-pointer"
              :title="$t('personnel.approve') || 'موافقة'"
            >
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
            <button
              @click="openRejectModal(row)"
              class="flex items-center justify-center rounded-lg bg-error-50 p-2 text-error-600 hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors cursor-pointer"
              :title="$t('personnel.reject') || 'رفض'"
            >
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </template>
        <!-- Pagination Footer -->
        <template #footer>
          <TablePagination
            v-if="!loading && store.totalItems > 0"
            :currentPage="store.currentPage"
            :totalPages="store.totalPages"
            :totalCount="store.totalItems"
            :pageSize="15"
            :visiblePages="computedVisiblePages"
            @change-page="goToPage"
          />
        </template>
      </BasicTable>
      </div>

    <!-- Approve Modal -->
    <div v-if="showApproveModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0 bg-gray-900/50">
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white text-start shadow-xl transition-all dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
        <div class="px-6 py-6">
          <div class="flex items-start gap-4">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="mt-1">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('personnel.confirm_approval') || 'تأكيد الموافقة' }}</h3>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                {{ $t('personnel.approve_confirmation_msg') || 'هل أنت متأكد من الموافقة على هذا التعديل؟ سيتم تغيير بيانات الفرد مباشرة.' }}
              </p>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 dark:bg-gray-800/50 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="showApproveModal = false"
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors"
          >
            {{ $t('common.cancel') || 'إلغاء' }}
          </button>
          <button
            type="button"
            @click="confirmApprove"
            :disabled="actionLoading"
            class="inline-flex items-center gap-2 rounded-lg bg-success-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-success-700 transition-colors disabled:opacity-50"
          >
            <svg v-if="actionLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ $t('personnel.approve') || 'موافقة وتحديث' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0 bg-gray-900/50">
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white text-start shadow-xl transition-all dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
        <div class="px-6 py-6">
          <div class="flex items-start gap-4">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-error-100 text-error-600 dark:bg-error-500/20 dark:text-error-400">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div class="mt-1 w-full">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('personnel.reject') || 'رفض الطلب' }}</h3>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                {{ $t('personnel.enter_rejection_reason') || 'يرجى كتابة سبب رفض الطلب (هذا الحقل إلزامي وسيطّلع عليه مقدم الطلب).' }}
              </p>
              
              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('personnel.rejection_reason') || 'سبب الرفض' }} <span class="text-error-500">*</span></label>
                <textarea
                  v-model="rejectionReason"
                  rows="3"
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-error-500 focus:ring-error-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:border-error-500 dark:focus:ring-error-500"
                  :placeholder="$t('corrections.reason_placeholder') || 'أدخل السبب بوضوح...'"
                ></textarea>
                <p v-if="rejectError" class="mt-1 text-xs text-error-500">{{ rejectError }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 dark:bg-gray-800/50 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="showRejectModal = false"
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors"
          >
            {{ $t('common.cancel') || 'إلغاء' }}
          </button>
          <button
            type="button"
            @click="confirmReject"
            :disabled="actionLoading || !rejectionReason.trim()"
            class="inline-flex items-center gap-2 rounded-lg bg-error-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-error-700 transition-colors disabled:opacity-50"
          >
            <svg v-if="actionLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ $t('personnel.reject') || 'تأكيد الرفض' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Batch Approve Modal -->
    <div v-if="showBatchApproveModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0 bg-gray-900/50">
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white text-start shadow-xl transition-all dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
        <div class="px-6 py-6">
          <div class="flex items-start gap-4">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="mt-1 w-full">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('corrections.confirm_batch_approve') || 'تأكيد الموافقة الجماعية' }}</h3>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                {{ $t('corrections.confirm_batch_approve_desc', { count: selectedIds.length }) || `سيتم اعتماد ${selectedIds.length} طلبات تصحيح وتحديث السجلات. يرجى إدخال رقم وثيقة المذكرة الداعمة للتصحيح الجماعي.` }}
              </p>
              
              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('corrections.memo_doc_id') || 'رقم/معرّف وثيقة الاعتماد' }} <span class="text-error-500">*</span></label>
                <input
                  v-model="memoDocumentId"
                  type="text"
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-success-500 focus:ring-success-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                  :placeholder="$t('corrections.memo_doc_placeholder') || 'مثال: DOC-2026-001'"
                />
                <p v-if="approveError" class="mt-1 text-xs text-error-500">{{ approveError }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 dark:bg-gray-800/50 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="showBatchApproveModal = false; approveError = ''"
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors"
          >
            {{ $t('common.cancel') || 'إلغاء' }}
          </button>
          <button
            type="button"
            @click="confirmBatchApprove"
            :disabled="actionLoading || !memoDocumentId.trim()"
            class="inline-flex items-center gap-2 rounded-lg bg-success-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-success-700 transition-colors disabled:opacity-50"
          >
            <svg v-if="actionLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ $t('corrections.approve_all') || 'اعتماد الكل' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Batch Reject Modal -->
    <div v-if="showBatchRejectModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0 bg-gray-900/50">
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white text-start shadow-xl transition-all dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
        <div class="px-6 py-6">
          <div class="flex items-start gap-4">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-error-100 text-error-600 dark:bg-error-500/20 dark:text-error-400">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div class="mt-1 w-full">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('corrections.confirm_batch_reject') || 'تأكيد الرفض الجماعي' }}</h3>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                {{ $t('corrections.confirm_batch_reject_desc', { count: selectedIds.length }) || `سيتم رفض ${selectedIds.length} طلبات تصحيح. يرجى إدخال سبب الرفض الجماعي.` }}
              </p>
              
              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('personnel.rejection_reason') || 'سبب الرفض' }} <span class="text-error-500">*</span></label>
                <textarea
                  v-model="rejectionReason"
                  rows="3"
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-error-500 focus:ring-error-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:border-error-500 dark:focus:ring-error-500"
                  :placeholder="$t('corrections.reason_placeholder') || 'أدخل السبب بوضوح...'"
                ></textarea>
                <p v-if="rejectError" class="mt-1 text-xs text-error-500">{{ rejectError }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 dark:bg-gray-800/50 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="showBatchRejectModal = false; rejectError = ''"
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors"
          >
            {{ $t('common.cancel') || 'إلغاء' }}
          </button>
          <button
            type="button"
            @click="confirmBatchReject"
            :disabled="actionLoading || !rejectionReason.trim()"
            class="inline-flex items-center gap-2 rounded-lg bg-error-600 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-error-700 transition-colors disabled:opacity-50"
          >
            <svg v-if="actionLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ $t('corrections.reject_all') || 'رفض الكل' }}
          </button>
        </div>
      </div>
    </div>

  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useCorrectionStore } from '@/stores/correction'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'
import BasicTable from '@/components/tables/BasicTable.vue'
import TablePagination from '@/components/common/TablePagination.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const tableColumns = computed(() => [
  { key: 'checkbox', label: '', class: 'w-12 text-center', tdClass: 'w-12 text-center', sortable: false },
  { key: 'personnel', label: t('corrections.personnel_col') || 'الفرد' },
  { key: 'field', label: t('corrections.field_col') || 'الحقل المطلوب تصحيحه' },
  { key: 'old_value', label: t('corrections.old_val_col') || 'القيمة القديمة' },
  { key: 'new_value', label: t('corrections.new_val_col') || 'القيمة الجديدة' },
  { key: 'requested_at', label: t('corrections.req_date_col') || 'تاريخ الطلب' }
])

const store = useCorrectionStore()

const requests = ref<any[]>([])
const loading = ref(true)

const searchQuery = ref('')
const filteredRequests = computed(() => {
  if (!searchQuery.value) return requests.value
  const q = searchQuery.value.toLowerCase()
  return requests.value.filter(r => 
    (r.personnel_name && r.personnel_name.toLowerCase().includes(q)) ||
    (r.military_number && r.military_number.includes(q)) ||
    (r.old_value && String(r.old_value).toLowerCase().includes(q)) ||
    (r.new_value && String(r.new_value).toLowerCase().includes(q))
  )
})

// Pagination logic for TablePagination
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

// Modals State
const showApproveModal = ref(false)
const showRejectModal = ref(false)
const showBatchApproveModal = ref(false)
const showBatchRejectModal = ref(false)

const selectedRequest = ref<any>(null)
const selectedIds = ref<string[]>([])
const selectAll = computed({
  get: () => selectedIds.value.length === requests.value.length && requests.value.length > 0,
  set: (val) => {
    selectedIds.value = val ? requests.value.map(r => r.id) : []
  }
})

const rejectionReason = ref('')
const rejectError = ref('')
const memoDocumentId = ref('')
const approveError = ref('')
const actionLoading = ref(false)

async function loadCorrections(page: number | Event = 1) {
  loading.value = true
  const pageNum = typeof page === 'number' ? page : 1
  try {
    const rawData = await store.fetchAllPendingCorrections(pageNum)
    requests.value = rawData.filter((r: any) => r.status === 'pending')
  } catch (err) {
    // Global handler shows Swal
  } finally {
    loading.value = false
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= store.totalPages) {
    loadCorrections(page)
  }
}

onMounted(() => {
  loadCorrections()
})

// Field translations helper
function getFieldLabel(field: string): string {
  const fields: Record<string, string> = {
    full_name: 'الاسم الكامل',
    birth_date: 'تاريخ الميلاد',
    join_date: 'تاريخ التجنيد',
    position: 'المنصب',
    job_title: 'المسمى الوظيفي',
    military_number: 'الرقم العسكري',
    national_id: 'الرقم الوطني',
    current_rank: 'الرتبة',
    central_department: 'الجهة'
  }
  return fields[field] || field
}

// Date formatter
function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('ar-EG', { year: 'numeric', month: 'short', day: 'numeric' })
}

// Actions
function openApproveModal(req: any) {
  selectedRequest.value = req
  showApproveModal.value = true
}

function openRejectModal(req: any) {
  selectedRequest.value = req
  rejectionReason.value = ''
  rejectError.value = ''
  showRejectModal.value = true
}

function openBatchRejectModal() {
  rejectionReason.value = ''
  rejectError.value = ''
  showBatchRejectModal.value = true
}

// Ensure the standard reject modal handles individual or batch if they reuse it, 
// But here we mapped `showRejectModal` for single, and `showBatchRejectModal` is separate.
// Wait, we can reuse `showRejectModal` for batch if we check `selectedIds` or just make a separate modal. 
// For simplicity, let's just make confirmBatchReject and confirmReject distinct.

async function confirmApprove() {
  if (!selectedRequest.value) return
  actionLoading.value = true
  try {
    await store.approveCorrection(selectedRequest.value.id)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('corrections.approve_success') || 'تم اعتماد التصحيح وتحديث بيانات الفرد بنجاح', showConfirmButton: false, timer: 3000 })
    showApproveModal.value = false
    requests.value = requests.value.filter(r => r.id !== selectedRequest.value.id)
  } catch (err) {
    // Global handler
  } finally {
    actionLoading.value = false
  }
}

async function confirmReject() {
  if (!rejectionReason.value.trim()) {
    rejectError.value = t('personnel.enter_rejection_reason') || 'الرجاء إدخال سبب الرفض'
    return
  }
  
  actionLoading.value = true
  try {
    await store.rejectCorrection(selectedRequest.value.id, rejectionReason.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('corrections.reject_success') || 'تم رفض الطلب بنجاح', showConfirmButton: false, timer: 3000 })
    showRejectModal.value = false
    requests.value = requests.value.filter(r => r.id !== selectedRequest.value.id)
  } catch (err) {
    // Global handler
  } finally {
    actionLoading.value = false
  }
}
async function confirmBatchApprove() {
  if (!memoDocumentId.value.trim()) {
    approveError.value = t('corrections.memo_required') || 'الرجاء إدخال رقم/معرّف المذكرة'
    return
  }
  
  actionLoading.value = true
  try {
    await store.approveBatchCorrection(selectedIds.value, memoDocumentId.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('corrections.batch_approve_success') || 'تم اعتماد الطلبات المحددة بنجاح', showConfirmButton: false, timer: 3000 })
    showBatchApproveModal.value = false
    requests.value = requests.value.filter(r => !selectedIds.value.includes(r.id))
    selectedIds.value = []
    memoDocumentId.value = ''
    approveError.value = ''
  } catch (err) {
    // Global handler
  } finally {
    actionLoading.value = false
  }
}

async function confirmBatchReject() {
  if (!rejectionReason.value.trim()) {
    rejectError.value = t('corrections.batch_reject_reason_required') || 'الرجاء إدخال سبب الرفض الجماعي'
    return
  }
  
  actionLoading.value = true
  try {
    await store.rejectBatchCorrection(selectedIds.value, rejectionReason.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('corrections.batch_reject_success') || 'تم رفض الطلبات المحددة بنجاح', showConfirmButton: false, timer: 3000 })
    showBatchRejectModal.value = false
    requests.value = requests.value.filter(r => !selectedIds.value.includes(r.id))
    selectedIds.value = []
    rejectionReason.value = ''
    rejectError.value = ''
  } catch (err) {
    // Global handler
  } finally {
    actionLoading.value = false
  }
}
</script>
