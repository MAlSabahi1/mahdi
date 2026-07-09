<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="مجمع الاعتماد الثنائي" />

    <div class="space-y-6 text-start animate-fade-in" dir="rtl">
      
      <!-- Premium Consistent Header Card -->
      <div class="relative overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-sm">
        <div class="absolute -right-16 -top-16 w-48 h-48 bg-brand-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-brand-500/10 text-brand-600 dark:text-brand-400 rounded-2xl shadow-theme-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">
                مجمع الاعتماد الثنائي (Dual Authorization Hub)
              </h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                حوكمة العمليات الفائقة الحساسية عبر بروتوكول التوقيع الثنائي (Four-Eyes Principle) لمنع انفراد شخص واحد بالقرارات السيادية.
              </p>
            </div>
          </div>

          <!-- Tabs Switcher (Identical to EmergencyAccess / AuditTrail) -->
          <div class="inline-flex p-1 bg-gray-100 dark:bg-gray-800/80 rounded-xl border border-gray-200/40 dark:border-gray-700/30">
            <button 
              @click="activeTab = 'pending'"
              class="px-4 py-2 text-xs font-black rounded-lg transition-all cursor-pointer inline-flex items-center gap-2"
              :class="[activeTab === 'pending' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-theme-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
            >
              الطلبات المعلقة
              <span 
                v-if="pendingRequests.length > 0"
                class="px-1.5 py-0.5 rounded-full text-[9px] bg-amber-500 text-white font-bold"
              >
                {{ pendingRequests.length }}
              </span>
            </button>
            <button 
              @click="activeTab = 'policies'"
              class="px-4 py-2 text-xs font-black rounded-lg transition-all cursor-pointer inline-flex items-center gap-2"
              :class="[activeTab === 'policies' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-theme-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
            >
              سياسات التحقق المزدوج
            </button>
            <button 
              @click="activeTab = 'history'"
              class="px-4 py-2 text-xs font-black rounded-lg transition-all cursor-pointer inline-flex items-center gap-2"
              :class="[activeTab === 'history' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-theme-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
            >
              السجل التاريخي
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Metrics Statistics Cards (Clean flat dashboard items) -->
      <div class="grid gap-5 grid-cols-1 sm:grid-cols-3">
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm">
          <div class="text-gray-400 dark:text-gray-500 text-[11px] font-bold uppercase">الطلبات المعلقة للمراجعة</div>
          <div class="text-2xl font-black text-gray-900 dark:text-white mt-1 flex items-center gap-2">
            <span>{{ pendingRequests.length }} طلبات</span>
          </div>
          <div class="text-[10px] text-gray-450 dark:text-gray-500 mt-1">تتطلب توقيع مسؤول مالي أو أمني مستقل</div>
        </div>
        
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm">
          <div class="text-gray-400 dark:text-gray-500 text-[11px] font-bold uppercase">قوانين الفرض المفعلة</div>
          <div class="text-2xl font-black text-brand-500 dark:text-brand-400 mt-1">6 سياسات نشطة</div>
          <div class="text-[10px] text-gray-455 dark:text-gray-500 mt-1">مفروضة قسرياً على مستوى قاعدة البيانات</div>
        </div>

        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm">
          <div class="text-gray-400 dark:text-gray-500 text-[11px] font-bold uppercase">متوسط زمن الاستجابة والاعتماد</div>
          <div class="text-2xl font-black text-emerald-600 dark:text-emerald-450 mt-1">12 دقيقة</div>
          <div class="text-[10px] text-gray-455 dark:text-gray-500 mt-1">معدل الانتهاء من التواقيع الحساسة</div>
        </div>
      </div>

      <!-- Tab: Pending Approval Queue -->
      <div v-show="activeTab === 'pending'" class="space-y-4">
        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="p-1.5 rounded-lg bg-brand-500/10 text-brand-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </span>
              <div>
                <h3 class="text-sm font-black text-gray-900 dark:text-white">قائمة الانتظار للتحقق الثنائي</h3>
                <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">الطلبات والعمليات الحساسة بانتظار اعتماد مسؤول مستقل آخر لإتمامها.</p>
              </div>
            </div>
            
            <button 
              @click="fetchPendingRequests" 
              class="px-3 py-1.5 border border-gray-200 dark:border-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs rounded-xl cursor-pointer flex items-center gap-1.5"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" :class="{'animate-spin': loading}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              تحديث القائمة
            </button>
          </div>

          <!-- Pending list Table -->
          <div class="mt-4">
            <DataTable
              :columns="pendingColumns"
              :data="pendingRequests"
              row-key="id"
            >
              <template #cell-requester="{ row }">
                <span class="font-extrabold text-gray-900 dark:text-white block">{{ row.requester_name }}</span>
                <span class="text-[10px] text-gray-400 font-mono block">Requester ID: {{ row.requester }}</span>
              </template>
              <template #cell-action="{ row }">
                <span class="font-bold text-gray-800 dark:text-gray-250 block">{{ getActionDisplay(row.action_type) }}</span>
                <span class="px-1.5 py-0.5 rounded text-[8px] font-bold bg-error-50 text-error-750 dark:bg-error-950/20 dark:text-error-450 border border-error-200/40">
                  طلب توقيع ثنائي (Four-Eyes Required)
                </span>
              </template>
              <template #cell-target="{ row }">
                <span class="font-mono text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-950 px-2 py-0.5 rounded border border-gray-200/40 dark:border-gray-800">
                  {{ row.target_object_type }} : {{ row.target_object_id }}
                </span>
              </template>
              <template #cell-reason="{ row }">
                <span class="text-gray-600 dark:text-gray-400 italic max-w-xs truncate block" :title="row.request_data?.reason">
                  {{ row.request_data?.reason || 'لم يتم تزويد مبرر.' }}
                </span>
              </template>
              <template #cell-dates="{ row }">
                <span class="block text-[10px] text-gray-500 font-mono">بدء: {{ formatDate(row.requested_at) }}</span>
                <span class="block text-[10px] text-red-500 font-bold font-mono">انتهاء: {{ formatDate(row.expires_at) }}</span>
              </template>
              <template #cell-status="{ row }">
                <div class="flex items-center gap-1.5 justify-end">
                  <button 
                    @click="approveRequest(row.id)"
                    class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-extrabold px-3 py-1.5 rounded-xl cursor-pointer transition-colors shadow-theme-xs"
                  >
                    اعتماد وتوقيع
                  </button>
                  <button 
                    @click="rejectRequest(row.id)"
                    class="border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900 text-red-650 text-[10px] font-extrabold px-3 py-1.5 rounded-xl cursor-pointer transition-colors"
                  >
                    رفض
                  </button>
                </div>
              </template>
            </DataTable>
          </div>
        </div>
      </div>

      <!-- Tab: Security Policies -->
      <div v-show="activeTab === 'policies'" class="space-y-4">
        <!-- Replaced grid cards with a premium, consistent Data Table -->
        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-gray-150 dark:border-gray-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="p-1.5 rounded-lg bg-brand-500/10 text-brand-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </span>
              <div>
                <h3 class="text-sm font-black text-gray-900 dark:text-white">السياسات الحاكمة للاعتماد المزدوج</h3>
                <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">الإجراءات السيادية والمالية والأمنية المشروطة بوجود موافقة ثنائية قسرية في قاعدة البيانات.</p>
              </div>
            </div>
          </div>

          <div class="mt-4">
            <DataTable
              :columns="policiesColumns"
              :data="systemPolicies"
              row-key="code"
            >
              <template #cell-code="{ value }">
                <span class="font-mono text-gray-700 dark:text-gray-300 font-bold">{{ value }}</span>
              </template>
              <template #cell-name="{ value }">
                <span class="font-extrabold text-gray-900 dark:text-white">{{ value }}</span>
              </template>
              <template #cell-description="{ value }">
                <span class="text-gray-650 dark:text-gray-400 leading-relaxed">{{ value }}</span>
              </template>
              <template #cell-sensitivity="{ row }">
                <span class="px-2 py-0.5 rounded bg-red-50 text-red-700 dark:bg-red-950/20 dark:text-red-400 font-bold text-[9px] border border-red-200/40">
                  حساسية فائقة
                </span>
              </template>
              <template #cell-status="{ row }">
                <div class="text-center">
                  <span class="inline-flex items-center gap-1 rounded-full bg-success-50 px-2 py-0.5 text-[9px] font-bold text-success-700 dark:bg-success-500/10 dark:text-success-400">
                    <span class="h-1 w-1 rounded-full bg-success-500"></span>
                    قيد الفرض النشط
                  </span>
                </div>
              </template>
            </DataTable>
          </div>
        </div>
      </div>

      <!-- Tab: Historical Approval Log -->
      <div v-show="activeTab === 'history'" class="space-y-4">
        <!-- Replaced history list with custom filter toolbar and table aligned with AuditTrail -->
        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-gray-150 dark:border-gray-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="p-1.5 rounded-lg bg-brand-500/10 text-brand-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </span>
              <div>
                <h3 class="text-sm font-black text-gray-900 dark:text-white">السجل التاريخي للاعتمادات الثنائية</h3>
                <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">الأرشيف الكامل للعمليات الاستثنائية التي تم اعتمادها أو رفضها مع بيانات التوقيع الرقمي للمشرفين.</p>
              </div>
            </div>
          </div>

          <!-- Filter Toolbar (Identical to AuditTrail's top bar layout) -->
          <div class="flex flex-col sm:flex-row items-center gap-3 bg-gray-50/50 dark:bg-gray-950 p-3 rounded-xl border border-gray-100 dark:border-gray-850">
            <div class="w-full sm:w-72">
              <input
                type="text"
                v-model="historySearch"
                placeholder="بحث في السجل التاريخي..."
                class="w-full text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-right"
              />
            </div>
            <div class="w-full sm:w-44">
              <select
                v-model="historyStatusFilter"
                class="w-full text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-right"
              >
                <option value="">كل الحالات</option>
                <option value="executed">تم التنفيذ</option>
                <option value="rejected">مرفوض</option>
              </select>
            </div>
            
            <button 
              v-if="historySearch || historyStatusFilter"
              @click="historySearch = ''; historyStatusFilter = ''"
              class="text-xs text-red-500 hover:text-red-650 font-bold self-end sm:self-center"
            >
              تصفية الفلاتر
            </button>
          </div>

          <!-- History Table -->
          <div class="mt-4">
            <DataTable
              :columns="historyColumns"
              :data="filteredHistory"
              row-key="id"
            >
              <template #cell-processed_at="{ value }">
                <span class="font-mono text-[11px] text-gray-500">{{ value }}</span>
              </template>
              <template #cell-requester="{ value }">
                <span class="font-extrabold text-gray-900 dark:text-white">{{ value }}</span>
              </template>
              <template #cell-action="{ row }">
                <span class="font-bold text-gray-850 dark:text-gray-200 block">{{ row.action_name }}</span>
                <span class="text-[10px] text-gray-400 block font-mono">ID: {{ row.target_id }}</span>
              </template>
              <template #cell-approver="{ value }">
                <span class="font-bold text-gray-750 dark:text-gray-300">{{ value || '—' }}</span>
              </template>
              <template #cell-notes="{ value }">
                <span class="text-gray-600 dark:text-gray-400 max-w-[250px] truncate block" :title="value">{{ value }}</span>
              </template>
              <template #cell-signature="{ value }">
                <div class="text-center">
                  <span 
                    v-if="value" 
                    class="font-mono text-[10px] bg-emerald-500/10 text-emerald-600 dark:text-emerald-450 px-2 py-0.5 rounded-lg border border-emerald-500/20"
                    :title="value"
                  >
                    {{ value.substring(0, 12) }}...
                  </span>
                  <span v-else class="text-gray-400">—</span>
                </div>
              </template>
              <template #cell-status="{ value }">
                <span 
                  class="px-2.5 py-0.5 rounded-full font-bold text-[9px] border"
                  :class="[
                    value === 'executed' ? 'bg-success-50 text-success-700 border-success-200 dark:bg-success-950/20 dark:text-success-400' : 'bg-error-50 text-error-750 border-error-200 dark:bg-error-950/20 dark:text-error-450'
                  ]"
                >
                  {{ value === 'executed' ? 'تم التنفيذ' : 'مرفوض' }}
                </span>
              </template>
            </DataTable>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const pendingColumns = [
  { key: 'requester', label: 'المنشئ (طالب الإجراء)', sortable: true },
  { key: 'action', label: 'نوع العملية الحساسة', sortable: true },
  { key: 'target', label: 'الكائن / النطاق المستهدف', sortable: true },
  { key: 'reason', label: 'مبرر العملية وسياق العمل', sortable: true },
  { key: 'dates', label: 'تاريخ الطلب وصلاحيته', sortable: false },
  { key: 'status', label: 'الإجراءات والاعتماد', sortable: false }
]

const policiesColumns = [
  { key: 'code', label: 'رمز السياسة المفروضة', sortable: true },
  { key: 'name', label: 'اسم الإجراء السيادي', sortable: true },
  { key: 'description', label: 'تفاصيل السياسة والأثر الأمني', sortable: true },
  { key: 'sensitivity', label: 'مستوى الحساسية', sortable: true },
  { key: 'status', label: 'حالة الفرض', sortable: true }
]

const historyColumns = [
  { key: 'processed_at', label: 'تاريخ المعالجة', sortable: true },
  { key: 'requester', label: 'طالب الإجراء (المنشئ)', sortable: true },
  { key: 'action', label: 'نوع العملية والمستهدف', sortable: true },
  { key: 'approver', label: 'مسؤول الاعتماد الثاني', sortable: true },
  { key: 'notes', label: 'النتيجة والمبرر', sortable: true },
  { key: 'signature', label: 'التوقيع الرقمي', sortable: false },
  { key: 'status', label: 'حالة الطلب', sortable: true }
]

interface PendingRequest {
  id: string
  requester: number
  requester_name: string
  action_type: string
  target_object_type: string
  target_object_id: string
  request_data: {
    reason: string
    [key: string]: any
  }
  status: string
  requested_at: string
  expires_at: string
}

interface HistoricalRequest {
  id: number
  requester: string
  action_name: string
  target_id: string
  approver: string
  processed_at: string
  notes: string
  signature?: string
  status: 'executed' | 'rejected'
}

const activeTab = ref('pending')
const pendingRequests = ref<PendingRequest[]>([])
const loading = ref(false)

// History Search Filters
const historySearch = ref('')
const historyStatusFilter = ref('')

// Backend ACTION_TYPE translation map
const actionTypeLabels: Record<string, string> = {
  DELETE_PERSONNEL: 'حذف فرد نهائياً من القوة العاملة',
  UNLOCK_MONTH: 'إلغاء إقفال الشهر المالي',
  MODIFY_SUPER_ADMIN: 'تعديل صلاحيات أو أدوار مدير نظام',
  CHANGE_ENCRYPTION_KEY: 'تغيير وتجديد مفاتيح تشفير قاعدة البيانات',
  BULK_DELETE: 'حذف جماعي للبيانات العسكرية',
  RESTORE_BACKUP: 'استعادة نسخة احتياطية كاملة للمنظومة'
}

function getActionDisplay(type: string): string {
  return actionTypeLabels[type] || type
}

// 6 Hardcoded Strict Backend Policies
const systemPolicies = [
  {
    code: 'DELETE_PERSONNEL',
    name: 'حذف فرد نهائياً من القوة',
    description: 'تتطلب إزالة أي سجل عسكري من القوة النشطة موافقة ثنائية لضمان حفظ الأرشيف في جداول الظل (Shadow Tables).'
  },
  {
    code: 'UNLOCK_MONTH',
    name: 'إلغاء إقفال الشهر المالي',
    description: 'عند إقفال الكشوفات الشهرية، يمنع تعديل أي راتب إلا بطلب إلغاء قفل الشهر المعتمد من مسؤول مالي مستقل.'
  },
  {
    code: 'MODIFY_SUPER_ADMIN',
    name: 'تعديل صلاحيات مدير النظام',
    description: 'أي إضافة أو سحب لصلاحيات مدراء النظام (Super Admins) تتطلب توقيع واعتماد من مديرين اثنين.'
  },
  {
    code: 'CHANGE_ENCRYPTION_KEY',
    name: 'تغيير مفتاح تشفير البيانات',
    description: 'العمليات على خوارزميات التشفير وحماية البيانات تتطلب مستويات موافقة مزدوجة معقدة.'
  },
  {
    code: 'BULK_DELETE',
    name: 'حذف جماعي للسجلات',
    description: 'تصفية أو حذف أكثر من سجل واحد في نفس اللحظة يتم تعليقه تلقائياً للحصول على توقيع ثانٍ.'
  },
  {
    code: 'RESTORE_BACKUP',
    name: 'استعادة نسخة احتياطية',
    description: 'استعادة بيانات المنظومة لنقطة زمنية سابقة تتطلب تأكيد المسؤول التقني ومسؤول الأمن العام معاً.'
  }
]

// High Fidelity Mock History database matching backend models
const mockHistory = ref<HistoricalRequest[]>([
  {
    id: 1,
    requester: 'admin',
    action_name: 'تعديل صلاحيات مدير النظام',
    target_id: 'User-104',
    approver: 'security_officer_1',
    processed_at: '2026-07-02 04:30 م',
    notes: 'تمت الموافقة وتفعيل الصلاحية بناءً على القرار الإداري رقم 89.',
    signature: '7e9c6942c3b38856b882fe79e12a142f0bc778471c8a129436141612ff58d6f0',
    status: 'executed'
  },
  {
    id: 2,
    requester: 'finance_maker',
    action_name: 'إلغاء إقفال الشهر المالي',
    target_id: 'Month-2026-05',
    approver: 'finance_checker_1',
    processed_at: '2026-06-28 11:15 ص',
    notes: 'تم الرفض بسبب عدم إرفاق أمر التكليف المالي المعتمد لتعديل الرواتب.',
    status: 'rejected'
  }
])

// Filtered History list computation
const filteredHistory = computed(() => {
  return mockHistory.value.filter(item => {
    const matchesSearch = !historySearch.value || 
      item.requester.toLowerCase().includes(historySearch.value.toLowerCase()) ||
      item.action_name.toLowerCase().includes(historySearch.value.toLowerCase()) ||
      item.target_id.toLowerCase().includes(historySearch.value.toLowerCase()) ||
      (item.notes && item.notes.toLowerCase().includes(historySearch.value.toLowerCase()))

    const matchesStatus = !historyStatusFilter.value || item.status === historyStatusFilter.value

    return matchesSearch && matchesStatus
  })
})

async function fetchPendingRequests() {
  loading.value = true
  try {
    const res = await api.get('/dual-auth/')
    pendingRequests.value = res.data.data || res.data.results || []
  } catch (err) {
    console.error('Failed to fetch pending requests:', err)
  } finally {
    loading.value = false
  }
}

async function approveRequest(id: string) {
  const result = await Swal.fire({
    title: 'توقيع واعتماد الطلب',
    text: 'هل أنت متأكد من مراجعة تفاصيل الطلب ورغبتك في اعتماده وتوقيعه رقمياً الآن؟',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتماد وتوقيع',
    cancelButtonText: 'تراجع',
    confirmButtonColor: '#465fff',
    cancelButtonColor: '#6b7280'
  })

  if (result.isConfirmed) {
    try {
      await api.post(`/dual-auth/${id}/approve/`)
      Swal.fire({
        icon: 'success',
        title: 'تم اعتماد العملية بنجاح',
        text: 'تم توقيع الطلب رقمياً وتنفيذ الإجراء في المنظومة فوراً.',
        confirmButtonColor: '#465fff'
      })
      fetchPendingRequests()
    } catch (err) {
      console.error('Approval failed:', err)
    }
  }
}

async function rejectRequest(id: string) {
  const { value: rejectReason } = await Swal.fire({
    title: 'رفض وإرجاع الطلب',
    text: 'يرجى كتابة سبب الرفض الرسمي ليظهر لطالب العملية.',
    input: 'textarea',
    inputPlaceholder: 'اكتب سبب الرفض بالتفصيل هنا...',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'تراجع',
    confirmButtonColor: '#dc2626',
    cancelButtonColor: '#6b7280',
    inputValidator: (value) => {
      if (!value || value.trim().length < 5) {
        return 'يرجى إدخال سبب رفض لا يقل عن 5 أحرف.'
      }
    }
  })

  if (rejectReason) {
    try {
      await api.post(`/dual-auth/${id}/reject/`, { reason: rejectReason })
      Swal.fire({
        icon: 'success',
        title: 'تم رفض الطلب',
        text: 'تم إرجاع الطلب للمنشئ وتدوين سبب الرفض.',
        confirmButtonColor: '#dc2626'
      })
      fetchPendingRequests()
    } catch (err) {
      console.error('Rejection failed:', err)
    }
  }
}

function formatDate(isoStr: string): string {
  if (!isoStr) return ''
  try {
    return new Date(isoStr).toLocaleString('ar-YE', {
      hour: '2-digit',
      minute: '2-digit',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  } catch (e) {
    return isoStr
  }
}

onMounted(() => {
  fetchPendingRequests()
})
</script>
