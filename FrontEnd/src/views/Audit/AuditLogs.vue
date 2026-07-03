<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 dark:text-white/90">{{ $t('audit.title') }}</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ $t('audit.subtitle') }}</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="exportCSV" class="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ $t('audit.export_csv') }}
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div v-if="auditStore.stats" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('audit.total_records') }}</p>
          <p class="mt-2 text-2xl font-bold text-gray-900 dark:text-white">{{ auditStore.stats.total_records?.toLocaleString() || 0 }}</p>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ $t('audit.today_records') }}</p>
          <p class="mt-2 text-2xl font-bold text-brand-600 dark:text-brand-400">{{ auditStore.stats.today_count?.toLocaleString() || 0 }}</p>
        </div>
      </div>

      <!-- Tabs & Filters -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div class="border-b border-gray-200 dark:border-gray-800 px-5 pt-5">
          <div class="flex gap-6 border-b border-gray-200 dark:border-gray-800">
            <button
              @click="activeTab = 'system'"
              :class="[
                'pb-3 text-sm font-medium transition-colors border-b-2',
                activeTab === 'system'
                  ? 'border-brand-500 text-brand-600 dark:text-brand-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              {{ $t('audit.system_logs') }}
            </button>
            <button
              @click="activeTab = 'logins'"
              :class="[
                'pb-3 text-sm font-medium transition-colors border-b-2',
                activeTab === 'logins'
                  ? 'border-brand-500 text-brand-600 dark:text-brand-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              {{ $t('audit.login_logs') }}
            </button>
          </div>
        </div>

        <div class="p-5 flex flex-wrap gap-4 items-end bg-gray-50/50 dark:bg-gray-800/20">
          <div>
            <label class="mb-1.5 block text-xs font-medium text-gray-700 dark:text-gray-400">{{ $t('audit.date_from') }}</label>
            <input v-model="filters.date_from" v-field-error="'date_from'" type="date" class="h-10 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-800 dark:border-gray-700 dark:bg-gray-900 dark:text-white" />
          </div>
          <div>
            <label class="mb-1.5 block text-xs font-medium text-gray-700 dark:text-gray-400">{{ $t('audit.date_to') }}</label>
            <input v-model="filters.date_to" v-field-error="'date_to'" type="date" class="h-10 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-800 dark:border-gray-700 dark:bg-gray-900 dark:text-white" />
          </div>
          <div class="flex-1 min-w-[200px]">
            <label class="mb-1.5 block text-xs font-medium text-gray-700 dark:text-gray-400">{{ $t('audit.general_search') }}</label>
            <input v-model="filters.search" v-field-error="'search'" @keyup.enter="applyFilters" type="text" :placeholder="$t('audit.search_placeholder')" class="h-10 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-800 dark:border-gray-700 dark:bg-gray-900 dark:text-white" />
          </div>
          <button @click="applyFilters" class="h-10 rounded-lg bg-brand-500 px-4 text-sm font-medium text-white hover:bg-brand-600 transition-colors">{{ $t('audit.apply_filters') }}</button>
          <button @click="clearFilters" class="h-10 rounded-lg border border-gray-300 bg-white px-4 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 transition-colors">{{ $t('audit.clear_filters') }}</button>
        </div>

        <!-- Table System Logs -->
        <div v-if="activeTab === 'system'" class="overflow-x-auto">
          <div v-if="auditStore.loading" class="flex justify-center p-12">
            <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
          </div>
          <table v-else class="w-full">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr class="border-b border-gray-200 dark:border-gray-800">
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.timestamp') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.user') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.model') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.action') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.severity') }}</th>
                <th class="px-5 py-3 text-end text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.details') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in auditStore.systemLogs" :key="log.id" class="border-b border-gray-100 last:border-0 dark:border-gray-800">
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300" dir="ltr" style="text-align: right">{{ formatDate(log.timestamp) }}</td>
                <td class="px-5 py-4 text-sm font-medium text-gray-900 dark:text-white">{{ log.username || $t('audit.system') }}</td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300">{{ log.model_name }}</td>
                <td class="px-5 py-4">
                  <span class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium" :class="getActionColor(log.action)">{{ log.action }}</span>
                </td>
                <td class="px-5 py-4">
                  <span class="inline-flex rounded-full px-2 py-0.5 text-xs" :class="getSeverityColor(log.severity)">{{ log.severity }}</span>
                </td>
                <td class="px-5 py-4 text-end">
                  <button @click="openDetails(log)" class="text-sm font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400">{{ $t('common.view') }}</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="!auditStore.loading && auditStore.totalSystemLogs > 0" class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex justify-between items-center">
             <span class="text-sm text-gray-500">{{ $t('common.page') }} {{ auditStore.systemLogsPage }} {{ $t('common.from') }} {{ auditStore.systemLogsTotalPages }} ({{ $t('common.total') }}: {{ auditStore.totalSystemLogs }})</span>
             <div class="flex gap-2">
               <button :disabled="auditStore.systemLogsPage <= 1" @click="auditStore.systemLogsPage--; fetchLogs()" class="px-3 py-1 text-sm border rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800">{{ $t('common.previous') }}</button>
               <button :disabled="auditStore.systemLogsPage >= auditStore.systemLogsTotalPages" @click="auditStore.systemLogsPage++; fetchLogs()" class="px-3 py-1 text-sm border rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800">{{ $t('common.next') }}</button>
             </div>
          </div>
        </div>

        <!-- Table Login Logs -->
        <div v-if="activeTab === 'logins'" class="overflow-x-auto">
          <div v-if="auditStore.loading" class="flex justify-center p-12">
            <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
          </div>
          <table v-else class="w-full">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr class="border-b border-gray-200 dark:border-gray-800">
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.timestamp') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.user') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.action') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.ip_address') }}</th>
                <th class="px-5 py-3 text-start text-xs font-medium text-gray-500 dark:text-gray-400">{{ $t('audit.failure_reason') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in auditStore.loginLogs" :key="log.id" class="border-b border-gray-100 last:border-0 dark:border-gray-800">
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300" dir="ltr" style="text-align: right">{{ formatDate(log.timestamp) }}</td>
                <td class="px-5 py-4 text-sm font-medium text-gray-900 dark:text-white">{{ log.username_attempted }}</td>
                <td class="px-5 py-4">
                  <span class="inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium" :class="getLoginActionColor(log.action)">{{ log.action }}</span>
                </td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300">{{ log.ip_address || '—' }}</td>
                <td class="px-5 py-4 text-sm text-gray-600 dark:text-gray-300">{{ log.failure_reason || '—' }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="!auditStore.loading && auditStore.totalLoginLogs > 0" class="border-t border-gray-200 px-5 py-4 dark:border-gray-800 flex justify-between items-center">
             <span class="text-sm text-gray-500">{{ $t('common.page') }} {{ auditStore.loginLogsPage }} {{ $t('common.from') }} {{ auditStore.loginLogsTotalPages }} ({{ $t('common.total') }}: {{ auditStore.totalLoginLogs }})</span>
             <div class="flex gap-2">
               <button :disabled="auditStore.loginLogsPage <= 1" @click="auditStore.loginLogsPage--; fetchLogs()" class="px-3 py-1 text-sm border rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800">{{ $t('common.previous') }}</button>
               <button :disabled="auditStore.loginLogsPage >= auditStore.loginLogsTotalPages" @click="auditStore.loginLogsPage++; fetchLogs()" class="px-3 py-1 text-sm border rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800">{{ $t('common.next') }}</button>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <AuditDetailsModal v-if="showDetails" :log="selectedLog" @close="showDetails = false" />
  </admin-layout>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useAuditStore } from '@/stores/audit'
import AuditDetailsModal from './components/AuditDetailsModal.vue'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const auditStore = useAuditStore()
const activeTab = ref('system')
const showDetails = ref(false)
const selectedLog = ref(null)

const filters = ref({
  date_from: '',
  date_to: '',
  search: ''
})

onMounted(() => {
  auditStore.fetchStats()
  fetchLogs()
})

watch(activeTab, () => {
  fetchLogs()
})

function fetchLogs() {
  const params = {}
  if (filters.value.date_from) params.date_from = filters.value.date_from
  if (filters.value.date_to) params.date_to = filters.value.date_to
  if (filters.value.search) {
    if (activeTab.value === 'system') params.search = filters.value.search
    else params.username = filters.value.search
  }

  if (activeTab.value === 'system') {
    auditStore.fetchSystemLogs(params)
  } else {
    auditStore.fetchLoginLogs(params)
  }
}

function applyFilters() {
  if (activeTab.value === 'system') auditStore.systemLogsPage = 1
  else auditStore.loginLogsPage = 1
  fetchLogs()
}

function clearFilters() {
  filters.value = { date_from: '', date_to: '', search: '' }
  applyFilters()
}

function openDetails(log) {
  selectedLog.value = log
  showDetails.value = true
}

async function exportCSV() {
  try {
    let url = activeTab.value === 'system' ? '/audit/logs/export/?format=csv' : '/audit/logins/export/?format=csv'
    const queryParams = new URLSearchParams()
    if (filters.value.date_from) queryParams.append('date_from', filters.value.date_from)
    if (filters.value.date_to) queryParams.append('date_to', filters.value.date_to)
    
    const qs = queryParams.toString()
    if (qs) url += `&${qs}`
    
    const res = await api.get(url, { responseType: 'blob' })
    const blob = new Blob([res.data], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.setAttribute('download', activeTab.value === 'system' ? 'system_audit.csv' : 'login_audit.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم التصدير بنجاح', showConfirmButton: false, timer: 2500 })
  } catch (error) {
    // Global handler shows Swal
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('en-US', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
}

function getActionColor(action) {
  if (!action) return 'bg-gray-100 text-gray-600 dark:bg-gray-800'
  const act = action.toUpperCase()
  if (act.includes('CREATE')) return 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400'
  if (act.includes('UPDATE')) return 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400'
  if (act.includes('DELETE')) return 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
  return 'bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400'
}

function getSeverityColor(sev) {
  if (sev === 'HIGH' || sev === 'CRITICAL') return 'bg-error-100 text-error-800 border border-error-200'
  if (sev === 'MEDIUM') return 'bg-warning-100 text-warning-800 border border-warning-200'
  return 'bg-gray-100 text-gray-800 border border-gray-200'
}

function getLoginActionColor(action) {
  return action === 'LOGIN_SUCCESS' 
    ? 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400' 
    : 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
}
</script>
