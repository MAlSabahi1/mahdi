<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="إعداد وتصدير النماذج" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          إعداد وتصدير النماذج
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          قم بتحديد المديرية المعنية واختيار الأعمدة المطلوب تصديرها مع تحديد الأعمدة المقفلة لحماية سلامة السجلات العسكرية والمالية.
        </p>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Target Selection Form -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-1 space-y-4 h-fit">
          <h3 class="text-sm font-black text-gray-900 dark:text-white mb-2">1. إعدادات النطاق المستهدف</h3>
          
          <div>
            <label class="block text-[11px] font-bold text-gray-500 mb-1.5">المديرية / المحافظة المستهدفة</label>
            <select v-model="selectedGovernorate" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option value="">اختر النطاق الجغرافي...</option>
              <option v-for="g in coreStore.governorates" :key="g.id" :value="g.id">
                {{ g.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-gray-500 mb-1.5">الحالة العسكرية المستهدفة بالتصدير</label>
            <select v-model="selectedStatus" class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option value="">كل الحالات</option>
              <option v-for="s in coreStore.statuses" :key="s.id" :value="s.id">
                {{ s.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-[11px] font-bold text-gray-500 mb-1.5">تنسيق التصدير الافتراضي</label>
            <select class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option>Excel Worksheet (.xlsx)</option>
              <option>CSV encoded UTF-8 (.csv)</option>
            </select>
          </div>

          <div class="pt-2">
            <button
              @click="triggerExport"
              :disabled="!selectedGovernorate || loading"
              class="w-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-black py-2.5 rounded-lg transition-colors cursor-pointer shadow-theme-xs flex items-center justify-center gap-2"
            >
              <span v-if="loading" class="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              تصدير نموذج الكشف المقفل
            </button>
          </div>
        </div>

        <!-- Lock Column Configurator -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-2 space-y-4">
          <div class="flex justify-between items-center border-b border-gray-150 dark:border-gray-800 pb-3">
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white">2. مصفوفة تحديد أعمدة التصدير وحمايتها</h3>
              <p class="text-[10px] text-gray-400 mt-0.5">حدّد الأعمدة المراد تضمينها في التصدير، وحالة القفل الخاصة بكل عمود لمنع التعديل العشوائي.</p>
            </div>
            <button @click="resetToDefaultLocks" class="text-[10px] text-brand-600 hover:underline font-bold cursor-pointer">
              إعادة تعيين الافتراضي
            </button>
          </div>

          <!-- Loading state -->
          <div v-if="loading" class="py-12 flex flex-col items-center justify-center gap-3">
            <div class="h-8 w-8 border-4 border-brand-600 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-xs text-gray-400">جاري تحميل مصفوفة الحقول وقاعدة البيانات...</p>
          </div>

          <!-- Column Groups Grid -->
          <div v-else class="space-y-6">
            
            <!-- Table Header Helper -->
            <div class="grid grid-cols-12 gap-2 px-3 py-1 bg-gray-50/50 dark:bg-gray-900/50 rounded-lg text-[10px] font-black text-gray-400">
              <span class="col-span-5 text-right">العمود المرجعي في قاعدة البيانات</span>
              <span class="col-span-4 text-center">حالة التصدير</span>
              <span class="col-span-3 text-center">حماية القفل</span>
            </div>

            <!-- Identity & Personal Info group -->
            <div>
              <h4 class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-950 px-2.5 py-1.5 rounded-lg mb-2">بيانات الهوية والبيانات الشخصية</h4>
              <div class="grid grid-cols-1 gap-2.5">
                <div v-for="col in columns.identity" :key="col.field" class="grid grid-cols-12 gap-2 items-center p-2.5 rounded-xl border border-gray-100 dark:border-gray-800 bg-gray-50/20 dark:bg-gray-900/10 hover:bg-gray-50/50 dark:hover:bg-gray-900/20 transition-all">
                  <div class="col-span-5 text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                  </div>
                  
                  <div class="col-span-4 flex items-center justify-center gap-2">
                    <span :class="col.exportable ? 'text-blue-600 bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/30' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20 border border-gray-200 dark:border-gray-800'" class="text-[9px] font-bold px-2 py-0.5 rounded border min-w-[50px] text-center">
                      {{ col.exportable ? 'تصدير' : 'استبعاد' }}
                    </span>
                    <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                  </div>

                  <div class="col-span-3 flex items-center justify-center gap-2">
                    <span :class="col.locked && col.exportable ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded border min-w-[50px] text-center">
                      {{ col.locked && col.exportable ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Structure group -->
            <div>
              <h4 class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-950 px-2.5 py-1.5 rounded-lg mb-2">الهيكل التنظيمي والوظيفي</h4>
              <div class="grid grid-cols-1 gap-2.5">
                <div v-for="col in columns.structure" :key="col.field" class="grid grid-cols-12 gap-2 items-center p-2.5 rounded-xl border border-gray-100 dark:border-gray-800 bg-gray-50/20 dark:bg-gray-900/10 hover:bg-gray-50/50 dark:hover:bg-gray-900/20 transition-all">
                  <div class="col-span-5 text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                  </div>
                  
                  <div class="col-span-4 flex items-center justify-center gap-2">
                    <span :class="col.exportable ? 'text-blue-600 bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/30' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20 border border-gray-200 dark:border-gray-800'" class="text-[9px] font-bold px-2 py-0.5 rounded border min-w-[50px] text-center">
                      {{ col.exportable ? 'تصدير' : 'استبعاد' }}
                    </span>
                    <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                  </div>

                  <div class="col-span-3 flex items-center justify-center gap-2">
                    <span :class="col.locked && col.exportable ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded border min-w-[50px] text-center">
                      {{ col.locked && col.exportable ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Status and Decisions group -->
            <div>
              <h4 class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-950 px-2.5 py-1.5 rounded-lg mb-2">الحالة الخدمية والقرارات</h4>
              <div class="grid grid-cols-1 gap-2.5">
                <div v-for="col in columns.statusAndDecisions" :key="col.field" class="grid grid-cols-12 gap-2 items-center p-2.5 rounded-xl border border-gray-100 dark:border-gray-800 bg-gray-50/20 dark:bg-gray-900/10 hover:bg-gray-50/50 dark:hover:bg-gray-900/20 transition-all">
                  <div class="col-span-5 text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                  </div>
                  
                  <div class="col-span-4 flex items-center justify-center gap-2">
                    <span :class="col.exportable ? 'text-blue-600 bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/30' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20 border border-gray-200 dark:border-gray-800'" class="text-[9px] font-bold px-2 py-0.5 rounded border min-w-[50px] text-center">
                      {{ col.exportable ? 'تصدير' : 'استبعاد' }}
                    </span>
                    <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                  </div>

                  <div class="col-span-3 flex items-center justify-center gap-2">
                    <span :class="col.locked && col.exportable ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded border min-w-[50px] text-center">
                      {{ col.locked && col.exportable ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useCoreStore } from '@/stores/core'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const coreStore = useCoreStore()
const selectedGovernorate = ref('')
const selectedStatus = ref('')
const loading = ref(false)

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

async function fetchExportFields() {
  try {
    loading.value = true
    const response = await api.get('/personnel/export-fields/')
    if (response.data && response.data.groups) {
      columns.value = response.data.groups
    }
  } catch (err) {
    console.error('Failed to fetch export fields:', err)
  } finally {
    loading.value = false
  }
}

function resetToDefaultLocks() {
  Object.values(columns.value).flat().forEach(c => {
    c.locked = c.alwaysLocked || ['military_number', 'full_name', 'national_id', 'security_admin', 'current_rank', 'current_status'].includes(c.field)
    c.exportable = true
  })
  Swal.fire({ toast: true, position: 'top-end', icon: 'info', title: 'تمت إعادة ضبط التصدير والقفل الافتراضي', showConfirmButton: false, timer: 2000 })
}

async function triggerExport() {
  if (!selectedGovernorate.value) return
  
  try {
    const govName = coreStore.governorates.find(g => String(g.id) === String(selectedGovernorate.value))?.name || 'المديرية'
    
    // Assemble export fields & locked fields
    const exportFields: string[] = []
    const lockedFields: string[] = []
    
    Object.values(columns.value).flat().forEach(c => {
      if (c.exportable) {
        exportFields.push(c.field)
        if (c.locked) {
          lockedFields.push(c.field)
        }
      }
    })

    const response = await api.get('/personnel/export_csv/', {
      params: {
        governorate: selectedGovernorate.value,
        current_status: selectedStatus.value || undefined,
        columns: exportFields.join(','),
        locked_columns: lockedFields.join(',')
      },
      responseType: 'blob'
    })

    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    a.download = `كشف_الأفراد_المقفل_${govName}.xlsx`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)

    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'تم تصدير النموذج المقفل بنجاح',
      showConfirmButton: false,
      timer: 3000
    })
  } catch (err) {
    console.error('Failed to export columns sheet:', err)
  }
}

onMounted(() => {
  if (coreStore.governorates.length === 0) {
    coreStore.fetchAllReferences()
  }
  fetchExportFields()
})
</script>
