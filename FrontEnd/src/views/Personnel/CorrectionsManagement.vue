<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('personnel.manage_corrections') || 'إدارة طلبات التصحيح'" />
    <div class="space-y-6">
      <!-- Header Section -->
      <div class="flex justify-end gap-3">
        <!-- Batch Actions Toolbar -->
        <div v-if="selectedIds.length > 0" class="flex items-center gap-3 bg-gray-50 px-4 py-1.5 rounded-lg border border-gray-200 dark:bg-gray-800 dark:border-gray-700 shadow-theme-xs">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ selectedIds.length }} محدد</span>
          <div class="h-4 w-px bg-gray-300 dark:bg-gray-600"></div>
          <button @click="showBatchApproveModal = true" class="text-sm bg-success-50 text-success-700 px-3 py-1 rounded-md hover:bg-success-100 dark:bg-success-500/10 dark:text-success-400 dark:hover:bg-success-500/20 transition-colors font-medium cursor-pointer">موافقة جماعية</button>
          <button @click="openBatchRejectModal" class="text-sm bg-error-50 text-error-700 px-3 py-1 rounded-md hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors font-medium cursor-pointer">رفض جماعي</button>
        </div>

        <button
          @click="loadCorrections"
          class="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors cursor-pointer"
        >
          <svg class="h-4.5 w-4.5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ $t('common.refresh') || 'تحديث' }}
        </button>
      </div>



      <!-- Data Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>

        <!-- Empty State -->
        <div v-else-if="requests.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="mb-4 rounded-full bg-gray-50 p-4 dark:bg-gray-800 shadow-theme-xs">
            <svg class="h-10 w-10 text-success-500 dark:text-success-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">لا توجد طلبات معلقة</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 text-center max-w-sm">جميع طلبات تصحيح البيانات تم البت فيها بنجاح.</p>
        </div>

        <!-- Table Content -->
        <div v-else class="overflow-x-auto">
          <table class="w-full text-start">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
                <th class="px-5 py-3 text-start w-12">
                  <input type="checkbox" v-model="selectAll" class="rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-brand-500" />
                </th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الفرد</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">الحقل المطلوب تصحيحه</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">القيمة القديمة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">القيمة الجديدة</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">تاريخ الطلب</th>
                <th class="px-5 py-3 text-start text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('common.actions') || 'الإجراءات' }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr
                v-for="req in requests"
                :key="req.id"
                class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
              >
                <td class="px-5 py-4 w-12">
                  <input type="checkbox" :value="req.id" v-model="selectedIds" class="rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-brand-500" />
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400 font-bold">
                      {{ req.personnel_name?.substring(0, 1) || '؟' }}
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        <RouterLink :to="`/personnel/${req.military_number}`" class="hover:text-brand-500 transition-colors">
                          {{ req.personnel_name || 'غير محدد' }}
                        </RouterLink>
                      </div>
                      <div class="text-xs text-gray-500 flex items-center gap-2 mt-0.5">
                        <span>{{ req.military_number }}</span>
                        <span class="inline-block h-1 w-1 rounded-full bg-gray-300 dark:bg-gray-600"></span>
                        <span>{{ req.personnel_rank || 'غير محدد' }}</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <span class="inline-flex items-center rounded-md bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-800 dark:bg-gray-800 dark:text-gray-300 border border-gray-200 dark:border-gray-700">
                    {{ getFieldLabel(req.field) }}
                  </span>
                  <div v-if="req.requested_by_name" class="mt-1.5 text-xs text-gray-500 flex items-center gap-1">
                    <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    بواسطة: {{ req.requested_by_name }}
                  </div>
                </td>
                <td class="px-5 py-4">
                  <div class="text-sm text-gray-500 dark:text-gray-400 line-through decoration-error-500/50">
                    {{ req.old_value || 'فارغ' }}
                  </div>
                </td>
                <td class="px-5 py-4">
                  <div class="text-sm font-medium text-success-600 dark:text-success-400 flex items-center gap-1.5">
                    <svg class="h-4 w-4 shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                    </svg>
                    {{ req.new_value }}
                  </div>
                </td>
                <td class="px-5 py-4">
                  <div class="text-sm text-gray-900 dark:text-white">{{ formatDate(req.requested_at) }}</div>
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <button
                      @click="openApproveModal(req)"
                      class="flex items-center justify-center rounded-lg bg-success-50 p-2 text-success-600 hover:bg-success-100 dark:bg-success-500/10 dark:text-success-400 dark:hover:bg-success-500/20 transition-colors"
                      title="موافقة"
                    >
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                    <button
                      @click="openRejectModal(req)"
                      class="flex items-center justify-center rounded-lg bg-error-50 p-2 text-error-600 hover:bg-error-100 dark:bg-error-500/10 dark:text-error-400 dark:hover:bg-error-500/20 transition-colors"
                      title="رفض"
                    >
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
        <div v-if="!loading && store.totalItems > 0" class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex justify-between items-center">
          <span class="text-sm text-gray-500">{{ $t('common.page') }} {{ store.currentPage }} {{ $t('common.from') }} {{ store.totalPages }} ({{ $t('common.total') }}: {{ store.totalItems }})</span>
          <div class="flex gap-2">
            <button :disabled="store.currentPage <= 1" @click="goToPage(store.currentPage - 1)" class="px-3 py-1 text-sm border rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800">{{ $t('common.previous') }}</button>
            <button :disabled="store.currentPage >= store.totalPages" @click="goToPage(store.currentPage + 1)" class="px-3 py-1 text-sm border rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800">{{ $t('common.next') }}</button>
          </div>
        </div>
      </div>
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
                  placeholder="أدخل السبب بوضوح..."
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
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">تأكيد الموافقة الجماعية</h3>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                سيتم اعتماد {{ selectedIds.length }} طلبات تصحيح وتحديث السجلات. يرجى إدخال رقم وثيقة المذكرة الداعمة للتصحيح الجماعي.
              </p>
              
              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">رقم/معرّف وثيقة الاعتماد <span class="text-error-500">*</span></label>
                <input
                  v-model="memoDocumentId"
                  type="text"
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-success-500 focus:ring-success-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                  placeholder="مثال: DOC-2026-001"
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
            اعتماد الكل
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
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">تأكيد الرفض الجماعي</h3>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                سيتم رفض {{ selectedIds.length }} طلبات تصحيح. يرجى إدخال سبب الرفض الجماعي.
              </p>
              
              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ $t('personnel.rejection_reason') || 'سبب الرفض' }} <span class="text-error-500">*</span></label>
                <textarea
                  v-model="rejectionReason"
                  rows="3"
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-error-500 focus:ring-error-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:border-error-500 dark:focus:ring-error-500"
                  placeholder="أدخل السبب بوضوح..."
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
            رفض الكل
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

const store = useCorrectionStore()

const requests = ref<any[]>([])
const loading = ref(true)

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
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد التصحيح وتحديث بيانات الفرد بنجاح', showConfirmButton: false, timer: 3000 })
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
    rejectError.value = 'الرجاء إدخال سبب الرفض'
    return
  }
  
  actionLoading.value = true
  try {
    await store.rejectCorrection(selectedRequest.value.id, rejectionReason.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم رفض الطلب بنجاح', showConfirmButton: false, timer: 3000 })
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
    approveError.value = 'الرجاء إدخال رقم/معرّف المذكرة'
    return
  }
  
  actionLoading.value = true
  try {
    await store.approveBatchCorrection(selectedIds.value, memoDocumentId.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد الطلبات المحددة بنجاح', showConfirmButton: false, timer: 3000 })
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
    rejectError.value = 'الرجاء إدخال سبب الرفض الجماعي'
    return
  }
  
  actionLoading.value = true
  try {
    await store.rejectBatchCorrection(selectedIds.value, rejectionReason.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم رفض الطلبات المحددة بنجاح', showConfirmButton: false, timer: 3000 })
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
