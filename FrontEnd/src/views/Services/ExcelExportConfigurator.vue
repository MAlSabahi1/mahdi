<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تهيئة وتصدير النماذج المقيدة" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-7 h-7 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            لوحة تهيئة وتصدير النماذج المقيدة
          </h1>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 max-w-2xl leading-relaxed">
            المنصة المركزية لتوليد الكشوفات ونماذج الإدخال المخصصة للقطاعات الأمنية والمديريات. حدّد نطاق الإرسال المستهدف وعيّن حماية الأعمدة لمنع التعديل على الحقول السيادية.
          </p>
        </div>
        
        <!-- Live Counters -->
        <div class="flex gap-4 bg-gray-50 dark:bg-white/[0.02] p-3 rounded-2xl border border-gray-200 dark:border-gray-800/80">
          <div class="text-center px-4 border-l border-gray-200 dark:border-gray-850">
            <span class="block text-[10px] font-bold text-gray-400">حقول التصدير النشطة</span>
            <span class="text-lg font-black text-blue-600 dark:text-blue-400">{{ totalExportable }}</span>
          </div>
          <div class="text-center px-4">
            <span class="block text-[10px] font-bold text-gray-400">حقول القراءة فقط (المغلقة)</span>
            <span class="text-lg font-black text-red-600 dark:text-red-400">{{ totalLocked }}</span>
          </div>
        </div>
      </div>

      <!-- Settings Header Bar (Horizontal) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Target Scope -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4">
          <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
            <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 text-xs font-black">1</span>
            النطاق المستهدف
          </h3>
          <div class="space-y-3">
            <div v-if="!canExportAllGovernorates" class="p-2 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 text-xs text-gray-700 dark:text-gray-300 font-bold flex justify-between">
              <span>{{ restrictedSecurityAdminName }}</span>
              <span class="text-[9px] px-2 py-0.5 bg-red-50 text-red-750 rounded-lg">صلاحيتك</span>
            </div>
            <select v-else v-model="selectedSecurityAdminId" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2 bg-gray-50/50 dark:bg-gray-900 focus:ring-brand-500">
              <option :value="null">-- إدارة أمن المحافظة --</option>
              <option v-for="admin in coreStore.securityAdmins" :key="admin.id" :value="admin.id">{{ admin.name }}</option>
            </select>

            <div class="grid grid-cols-2 gap-1.5">
              <button v-for="type in subUnitTypes" :key="type.value" type="button" :disabled="type.value !== 'all' && !selectedSecurityAdminId" @click="selectedSubUnitType = type.value" :class="[selectedSubUnitType === type.value ? 'bg-brand-600 text-white' : 'bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300 disabled:opacity-50']" class="px-2 py-1.5 rounded-lg text-[10px] font-bold">{{ type.label }}</button>
            </div>
            
            <div v-if="selectedSubUnitType !== 'all'">
              <select v-model="selectedSubUnitId" :disabled="!selectedSecurityAdminId" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2 bg-gray-50/50 dark:bg-gray-900 disabled:opacity-50">
                <option :value="null">-- {{ subUnitTypeLabel }} --</option>
                <option v-for="item in filteredSubUnits" :key="item.id" :value="item.id">{{ item.name }}</option>
              </select>
              <p v-if="!selectedSecurityAdminId" class="text-[10px] text-amber-600 mt-1 font-bold">يرجى اختيار المحافظة أولاً.</p>
            </div>
          </div>
        </div>

        <!-- Filter Statuses -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4 flex flex-col">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
              <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 text-brand-600 text-xs font-black">2</span>
              فلترة الحالات
            </h3>
            <div class="flex gap-2">
              <button @click="selectAllStatuses" type="button" class="text-[10px] text-brand-600 font-bold hover:underline">الكل</button>
              <span class="text-gray-300">|</span>
              <button @click="clearAllStatuses" type="button" class="text-[10px] text-gray-400 hover:underline">مسح</button>
            </div>
          </div>
          <div class="border border-gray-150 dark:border-gray-800/60 rounded-xl bg-gray-50/20 dark:bg-gray-900/50 p-2 flex-grow overflow-hidden flex flex-col">
            <div class="overflow-y-auto max-h-[120px] space-y-1 custom-scrollbar pr-1 flex-grow">
              <label v-for="item in coreStore.statuses" :key="item.id" class="flex items-center gap-2 p-1 hover:bg-white dark:hover:bg-gray-800 rounded cursor-pointer">
                <input type="checkbox" :value="item.id" v-model="selectedStatuses" class="h-3 w-3 text-brand-600 border-gray-300 rounded" />
                <span class="text-[10px] text-gray-700 dark:text-gray-300 font-medium">{{ item.name }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Partitioning -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
              <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 text-brand-600 text-xs font-black">3</span>
              تبويب وتقسيم
            </h3>
            <label v-if="isPartitioningAvailable" class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="enablePartitioning" class="sr-only peer" />
              <div class="w-8 h-4.5 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:right-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3.5 after:w-3.5 after:transition-all dark:border-gray-600 peer-checked:bg-brand-600"></div>
            </label>
          </div>
          <div v-if="enablePartitioning && isPartitioningAvailable" class="space-y-3">
            <select v-model="exportMode" class="w-full text-[11px] font-bold border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2 bg-gray-50/50 dark:bg-gray-900">
              <option value="single">كشف واحد موحد للجميع</option>
              <option value="multi">مبوبة بـ 4 أوراق (حسب التصنيف)</option>
            </select>
            <select v-model="splitBy" class="w-full text-[11px] font-bold border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2 bg-gray-50/50 dark:bg-gray-900">
              <option value="">بدون تقسيم مكاني إضافي</option>
              <option v-for="opt in splitOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div v-else class="h-full flex flex-col items-center justify-center space-y-2 p-4 text-center">
             <svg class="w-8 h-8 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
             <span class="text-[11px] text-gray-400 font-bold">سيتم التصدير كملف واحد موحد.</span>
          </div>
        </div>
      </div>

      <!-- Live Table Columns Preview -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4">
        
        <div class="flex flex-col md:flex-row justify-between items-center gap-4 border-b border-gray-150 dark:border-gray-850 pb-4">
          <div>
            <h2 class="text-lg font-black text-gray-900 dark:text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
              معاينة حية وتخصيص الأعمدة
            </h2>
            <p class="text-[10px] text-gray-500 mt-1">
              قم بإدارة الأعمدة مباشرة: 👁️ لإخفاء العمود من التصدير، 🔒 لقفل تعديل الخلية في الإكسل.
            </p>
          </div>
          <div class="flex gap-2">
            <!-- Hidden columns dropdown -->
            <div class="relative group">
              <button class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:bg-gray-100 dark:hover:bg-gray-800 text-[11px] font-bold text-gray-700 dark:text-gray-300 px-3 py-2 rounded-xl flex items-center gap-2 transition-all">
                <span>إظهار الأعمدة المخفية ({{ hiddenColumns.length }})</span>
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </button>
              <div class="absolute left-0 top-full mt-2 w-48 bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 rounded-xl shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-20 max-h-64 overflow-y-auto">
                <div v-if="hiddenColumns.length === 0" class="p-4 text-center text-[10px] text-gray-400">لا توجد أعمدة مخفية</div>
                <button v-for="col in hiddenColumns" :key="col.field" @click="col.exportable = true" class="w-full text-right px-4 py-2 text-[11px] hover:bg-gray-50 dark:hover:bg-gray-800 font-bold border-b border-gray-50 dark:border-gray-850 last:border-0 flex items-center justify-between group/btn text-gray-700 dark:text-gray-300">
                  {{ col.label }}
                  <svg class="w-3.5 h-3.5 text-gray-300 dark:text-gray-600 group-hover/btn:text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                </button>
              </div>
            </div>
            
            <button @click="resetToDefaultLocks" class="text-[11px] font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 dark:bg-brand-900/30 dark:hover:bg-brand-900/50 px-3 py-2 rounded-xl transition-all">
              إعادة الضبط
            </button>
          </div>
        </div>

        <!-- The Live Table -->
        <div class="overflow-x-auto border border-gray-200 dark:border-gray-800 rounded-xl custom-scrollbar relative bg-gray-50 dark:bg-gray-900/50">
          <table class="w-full text-right border-collapse whitespace-nowrap min-w-max">
            <thead class="bg-white dark:bg-gray-900">
              <tr>
                <th 
                  v-for="col in exportableColumns" 
                  :key="col.field"
                  class="border-b border-gray-200 dark:border-gray-800 p-3 min-w-[140px] relative group transition-colors duration-300"
                  :class="[col.locked ? 'bg-blue-50/60 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800' : 'bg-emerald-50/60 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800', 'border-l last:border-l-0']"
                >
                  <div class="flex flex-col gap-2.5">
                    <!-- Actions Row -->
                    <div class="flex items-center justify-between text-gray-400">
                      <!-- Hide Toggle -->
                      <button 
                        @click="col.exportable = false" 
                        :disabled="col.alwaysExportable" 
                        class="p-1 rounded bg-white/50 dark:bg-black/20 hover:bg-white dark:hover:bg-gray-800 hover:shadow-sm hover:text-gray-700 dark:hover:text-gray-300 disabled:opacity-30 disabled:cursor-not-allowed transition-all" 
                        title="إخفاء العمود"
                      >
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                      </button>
                      
                      <!-- Lock Toggle -->
                      <button 
                        @click="col.locked = !col.locked" 
                        :disabled="col.alwaysLocked" 
                        class="p-1 rounded bg-white/50 dark:bg-black/20 hover:bg-white dark:hover:bg-gray-800 hover:shadow-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all" 
                        :class="[col.locked ? 'text-blue-600 hover:text-blue-700' : 'text-emerald-600 hover:text-emerald-700']"
                        :title="col.locked ? 'مقفل (قراءة فقط)' : 'مفتوح (قابل للتعديل)'"
                      >
                        <svg v-if="col.locked" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                        <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"/></svg>
                      </button>
                    </div>

                    <!-- Header Label -->
                    <div class="text-center">
                      <span class="block text-xs font-black" :class="[col.locked ? 'text-blue-900 dark:text-blue-300' : 'text-emerald-900 dark:text-emerald-300']">
                        {{ col.label }}
                      </span>
                      <span class="block text-[9px] font-mono mt-1 opacity-70" :class="[col.locked ? 'text-blue-800 dark:text-blue-400' : 'text-emerald-800 dark:text-emerald-400']">
                        {{ col.field }}
                      </span>
                    </div>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <template v-if="loadingPreview">
                <tr v-for="i in 4" :key="i" class="bg-white dark:bg-gray-900 border-b border-gray-150">
                  <td v-for="col in exportableColumns" :key="col.field" class="border-l border-gray-150 p-4 text-center">
                    <div class="h-1.5 w-16 rounded mx-auto" :class="[col.locked ? 'bg-gray-200 dark:bg-gray-800' : 'bg-green-50 dark:bg-green-900/20']"></div>
                  </td>
                </tr>
              </template>
              <template v-else-if="previewData.length > 0">
                <tr v-for="(row, idx) in previewData" :key="idx" class="bg-white dark:bg-gray-900 border-b border-gray-150 dark:border-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <td v-for="col in exportableColumns" :key="col.field" class="border-l border-gray-150 dark:border-gray-850 p-3 text-center text-[11px] font-bold text-gray-700 dark:text-gray-300">
                    <span v-if="col.field.startsWith('pseudo_')" class="text-gray-300 dark:text-gray-600 font-normal">--</span>
                    <span v-else>{{ getPreviewValue(row, col.field) }}</span>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr>
                  <td :colspan="exportableColumns.length" class="p-8 text-center text-gray-400 text-xs font-bold bg-white dark:bg-gray-900">
                    لا توجد بيانات مطابقة لهذه الفلترة لعرضها كمعاينة.
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Trigger Export Button -->
        <button
          @click="triggerExport"
          :disabled="loading"
          class="w-full mt-6 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white text-sm font-black py-4 rounded-2xl transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
        >
          <span v-if="loading" class="h-5 w-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          تصدير وتوليد نموذج الكشف المقيد المعتمد
        </button>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useCoreStore } from '@/stores/core'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const coreStore = useCoreStore()
const authStore = useAuthStore()
const loading = ref(false)

// Role-based permissions to determine if user can configure/select all governorates
const canExportAllGovernorates = computed(() => {
  if (authStore.user?.is_superuser || authStore.user?.is_staff) {
    return true
  }
  const profile = authStore.user?.authz_profile
  if (profile?.supervises_all) {
    return true
  }
  return false
})

const isSecurityAdminRestricted = computed(() => !canExportAllGovernorates.value)

const restrictedSecurityAdminName = computed(() => {
  const profile = authStore.user?.authz_profile
  if (!profile || !profile.security_admin_id) return ''
  
  const found = coreStore.securityAdmins.find(a => a.id === profile.security_admin_id)
  return found ? found.name : `إدارة أمن رقم ${profile.security_admin_id}`
})

// 1. Target Scope Selection state
const selectedSecurityAdminId = ref<number | null>(null)
const selectedSubUnitType = ref<'all' | 'central_department' | 'branch' | 'district_police'>('all')
const selectedSubUnitId = ref<number | null>(null)

const subUnitTypes = [
  { value: 'all', label: 'كافة الأفراد بالمحافظة' },
  { value: 'central_department', label: 'إدارة مركزية' },
  { value: 'branch', label: 'فرع' },
  { value: 'district_police', label: 'أمن مديرية' }
] as const

const subUnitTypeLabel = computed(() => {
  switch (selectedSubUnitType.value) {
    case 'central_department': return 'الإدارة المركزية'
    case 'branch': return 'الفرع'
    case 'district_police': return 'أمن المديرية'
    default: return ''
  }
})

// Filter sub-units dynamically based on chosen security admin
const filteredSubUnits = computed(() => {
  if (!selectedSecurityAdminId.value) return []
  
  switch (selectedSubUnitType.value) {
    case 'central_department':
      return coreStore.centralDepartments.filter(dep => dep.security_admin === selectedSecurityAdminId.value)
    case 'branch':
      return coreStore.branches.filter(br => br.security_admin === selectedSecurityAdminId.value)
    case 'district_police':
      return coreStore.districtPolices.filter(dp => dp.security_admin === selectedSecurityAdminId.value)
    default:
      return []
  }
})

// Initialize restricted scope
function initGeographicScope() {
  const profile = authStore.user?.authz_profile
  if (isSecurityAdminRestricted.value && profile && profile.security_admin_id) {
    selectedSecurityAdminId.value = profile.security_admin_id
  }
}

watch(() => authStore.user, initGeographicScope, { immediate: true })

watch(selectedSecurityAdminId, () => {
  selectedSubUnitId.value = null
  selectedSubUnitType.value = 'all'
})

watch(selectedSubUnitType, () => {
  selectedSubUnitId.value = null
})

// 2. Additional Filters (Service Statuses)
const selectedStatuses = ref<number[]>([])

function selectAllStatuses() {
  selectedStatuses.value = coreStore.statuses.map(s => s.id)
}
function clearAllStatuses() {
  selectedStatuses.value = []
}

// 3. Advanced Excel Sheet Division option (Only active when exporting broad scopes like "كافة الأفراد بالمحافظة")
const isPartitioningAvailable = computed(() => {
  return selectedSubUnitType.value === 'all'
})

const enablePartitioning = ref(false)
const exportMode = ref('single')
const splitBy = ref('')
const splitOptions = [
  { value: 'central_department', label: 'مبوبة حسب الإدارة المركزية', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل إدارة مركزية).' },
  { value: 'branch', label: 'مبوبة حسب الفروع', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل فرع).' },
  { value: 'district_police', label: 'مبوبة حسب أمن المديريات', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل أمن مديرية).' }
]

// Automatically disable partitioning when not available
watch(isPartitioningAvailable, (newVal) => {
  if (!newVal) {
    enablePartitioning.value = false
    splitBy.value = ''
  }
})

// 4. Column Configurator matrix state
interface ColumnConfig {
  label: string
  field: string
  locked: boolean
  alwaysLocked: boolean
  exportable: boolean
  alwaysExportable: boolean
}

const columns = ref<{
  identity: ColumnConfig[]
  structure: ColumnConfig[]
  statusAndDecisions: ColumnConfig[]
}>({
  identity: [],
  structure: [],
  statusAndDecisions: []
})

const previewData = ref<any[]>([])
const loadingPreview = ref(false)

async function fetchPreviewData() {
  loadingPreview.value = true
  try {
    const params: Record<string, any> = { limit: 4 }
    
    if (selectedSecurityAdminId.value) params.security_admin = selectedSecurityAdminId.value
    if (selectedSubUnitType.value === 'branch' && selectedSubUnitId.value) params.branch = selectedSubUnitId.value
    if (selectedSubUnitType.value === 'central_department' && selectedSubUnitId.value) params.central_department = selectedSubUnitId.value
    if (selectedSubUnitType.value === 'district_police' && selectedSubUnitId.value) params.district_police = selectedSubUnitId.value
    
    const res = await api.get('/personnel/', { params })
    previewData.value = res.data.results || []
  } catch (err) {
    console.error('Preview fetch error:', err)
  } finally {
    loadingPreview.value = false
  }
}

watch([selectedSecurityAdminId, selectedSubUnitId, selectedSubUnitType], () => {
  fetchPreviewData()
})

function getPreviewValue(row: any, field: string) {
  if (field.startsWith('pseudo_')) return ''
  const val = row[field]
  if (val && typeof val === 'object' && val.name) return val.name
  return val || '—'
}

const searchFieldsQuery = ref('')

// Flat columns helper for the top compact unified configurator table
const allFlatColumns = computed(() => {
  return [
    ...columns.value.identity,
    ...columns.value.structure,
    ...columns.value.statusAndDecisions
  ]
})

const exportableColumns = computed(() => {
  return allFlatColumns.value.filter(c => c.exportable)
})

const hiddenColumns = computed(() => {
  return allFlatColumns.value.filter(c => !c.exportable)
})

const totalExportable = computed(() => {
  return exportableColumns.value.length
})

// Compute filtered columns by search query
const filteredGroups = computed(() => {
  const query = searchFieldsQuery.value.trim().toLowerCase()
  if (!query) return columns.value

  const filterFn = (col: ColumnConfig) => 
    col.label.toLowerCase().includes(query) || col.field.toLowerCase().includes(query)

  return {
    identity: columns.value.identity.filter(filterFn),
    structure: columns.value.structure.filter(filterFn),
    statusAndDecisions: columns.value.statusAndDecisions.filter(filterFn)
  }
})

const totalLocked = computed(() => {
  return allFlatColumns.value.filter(c => c.exportable && c.locked).length
})

// Bulk operations
function bulkExport(enable: boolean) {
  allFlatColumns.value.forEach(c => {
    if (!c.alwaysExportable) {
      c.exportable = enable
    }
  })
}

function bulkLock(lock: boolean) {
  allFlatColumns.value.forEach(c => {
    if (c.exportable && !c.alwaysLocked) {
      c.locked = lock
    }
  })
}

function resetToDefaultLocks() {
  allFlatColumns.value.forEach(c => {
    c.locked = c.alwaysLocked || ['military_number', 'full_name', 'national_id', 'security_admin', 'current_rank', 'current_status', 'current_status_classification'].includes(c.field)
    c.exportable = true
  })
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'info',
    title: 'تمت إعادة ضبط التصدير والقفل الافتراضي',
    showConfirmButton: false,
    timer: 2000
  })
}

// Fetch columns matrix structure from backend
async function fetchExportFields() {
  try {
    loading.value = true
    const response = await api.get('/personnel/export-fields/')
    if (response.data && response.data.groups) {
      columns.value = response.data.groups
      
      // Update custom labels to match corrected terminology
      const renameFieldLabel = (fieldList: ColumnConfig[], fieldName: string, newLabel: string) => {
        const found = fieldList.find(c => c.field === fieldName)
        if (found) found.label = newLabel
      }
      renameFieldLabel(columns.value.structure, 'security_admin', 'إدارة أمن المحافظة')
      renameFieldLabel(columns.value.structure, 'central_department', 'الإدارة المركزية')
      renameFieldLabel(columns.value.structure, 'branch', 'الفرع')
      renameFieldLabel(columns.value.structure, 'branch', 'الفرع')
      renameFieldLabel(columns.value.structure, 'district_police', 'أمن المديرية')
      
      // Inject mandatory operation columns so the user can visualize them in the Live Table preview
      if (!columns.value.statusAndDecisions.some(c => c.field === 'pseudo_status_type')) {
        columns.value.statusAndDecisions.push({
          field: 'pseudo_status_type',
          label: 'نوع الحالة (مدخل للإكسل)',
          exportable: true,
          alwaysExportable: true,
          locked: false,
          alwaysLocked: true
        })
      }
      if (!columns.value.statusAndDecisions.some(c => c.field === 'pseudo_monthly_var')) {
        columns.value.statusAndDecisions.push({
          field: 'pseudo_monthly_var',
          label: 'المتغير الشهري',
          exportable: true,
          alwaysExportable: true,
          locked: false,
          alwaysLocked: true
        })
      }
      if (!columns.value.statusAndDecisions.some(c => c.field === 'pseudo_notes')) {
        columns.value.statusAndDecisions.push({
          field: 'pseudo_notes',
          label: 'ملاحظات',
          exportable: true,
          alwaysExportable: false,
          locked: false,
          alwaysLocked: true
        })
      }
    }

  } catch (err) {
    console.error('Failed to fetch export fields:', err)
  } finally {
    loading.value = false
  }
}

// Trigger Excel Generation and Download
async function triggerExport() {
  try {
    loading.value = true
    
    // 1. Gather configured fields and locks
    const exportFields: string[] = []
    const lockedFields: string[] = []
    
    allFlatColumns.value.forEach(c => {
      if (c.exportable && !c.field.startsWith('pseudo_')) {
        exportFields.push(c.field)
        if (c.locked) {
          lockedFields.push(c.field)
        }
      }
    })

    // 2. Set scope IDs based on selection type
    const queryParams: Record<string, any> = {
      columns: exportFields.join(','),
      locked_columns: lockedFields.join(','),
      statuses: selectedStatuses.value.join(',')
    }

    if (selectedSecurityAdminId.value) {
      queryParams.security_admins = selectedSecurityAdminId.value.toString()
    }

    if (selectedSubUnitType.value === 'central_department' && selectedSubUnitId.value) {
      queryParams.central_departments = selectedSubUnitId.value.toString()
    } else if (selectedSubUnitType.value === 'branch' && selectedSubUnitId.value) {
      queryParams.branches = selectedSubUnitId.value.toString()
    } else if (selectedSubUnitType.value === 'district_police' && selectedSubUnitId.value) {
      queryParams.district_polices = selectedSubUnitId.value.toString()
    }

    // 3. Set partitioning param if active
    if (enablePartitioning.value) {
      queryParams.mode = exportMode.value
      if (splitBy.value) {
        queryParams.split_by = splitBy.value
      }
    } else {
      queryParams.mode = 'single'
    }

    const response = await api.get('/service-cycle/export/', {
      params: queryParams,
      responseType: 'blob'
    })

    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    
    // Custom filename
    a.download = `كشف_أفراد_مقيد.xlsx`
    
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)

    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'تم توليد وتصدير الكشف المعتمد بنجاح',
      showConfirmButton: false,
      timer: 3000
    })
  } catch (err) {
    console.error('Failed to export columns sheet:', err)
    Swal.fire({
      icon: 'error',
      title: 'فشل التصدير',
      text: 'حدث خطأ أثناء الاتصال بالخادم، يرجى المحاولة لاحقاً.'
    })
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchMe()
  }
  if (coreStore.securityAdmins.length === 0) {
    coreStore.fetchAllReferences()
  }
  fetchExportFields()
  fetchPreviewData()
  initGeographicScope()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #334155;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
