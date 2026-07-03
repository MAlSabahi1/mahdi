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
          قم بتحديد المديرية المعنية واختيار الأعمدة المقفلة (غير القابلة للتعديل) لحماية سلامة السجلات العسكرية والمالية قبل إرسال النموذج.
        </p>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Target Selection Form -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-1 space-y-4">
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
              :disabled="!selectedGovernorate"
              class="w-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-black py-2.5 rounded-lg transition-colors cursor-pointer shadow-theme-xs"
            >
              تصدير نموذج الكشف المقفل
            </button>
          </div>
        </div>

        <!-- Lock Column Configurator -->
        <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-theme-xs lg:col-span-2 space-y-4">
          <div class="flex justify-between items-center border-b border-gray-150 dark:border-gray-800 pb-3">
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white">2. مصفوفة التحكم بحماية أعمدة الإكسل</h3>
              <p class="text-[10px] text-gray-400 mt-0.5">الأعمدة المحددة كـ (مقفلة) ستكون للقراءة فقط في الملف المصدّر.</p>
            </div>
            <button @click="resetToDefaultLocks" class="text-[10px] text-brand-600 hover:underline font-bold cursor-pointer">
              إعادة تعيين القفل الافتراضي
            </button>
          </div>

          <!-- Column Groups Grid -->
          <div class="space-y-6">
            <!-- Identity & Personal Info group -->
            <div>
              <h4 class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-950 px-2.5 py-1.5 rounded-lg mb-2">بيانات الهوية والبيانات الشخصية</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="col in columns.identity" :key="col.field" class="flex items-center justify-between p-2 rounded-lg border border-gray-100 dark:border-gray-800 bg-gray-50/30 dark:bg-gray-900/20">
                  <div class="text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="col.locked ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded border">
                      {{ col.locked ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Structure group -->
            <div>
              <h4 class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-950 px-2.5 py-1.5 rounded-lg mb-2">الهيكل التنظيمي والوظيفي</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="col in columns.structure" :key="col.field" class="flex items-center justify-between p-2 rounded-lg border border-gray-100 dark:border-gray-800 bg-gray-50/30 dark:bg-gray-900/20">
                  <div class="text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="col.locked ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded border">
                      {{ col.locked ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Status and Decisions group -->
            <div>
              <h4 class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-950 px-2.5 py-1.5 rounded-lg mb-2">الحالة الخدمية والقرارات</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="col in columns.statusAndDecisions" :key="col.field" class="flex items-center justify-between p-2 rounded-lg border border-gray-100 dark:border-gray-800 bg-gray-50/30 dark:bg-gray-900/20">
                  <div class="text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="col.locked ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded border">
                      {{ col.locked ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
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

interface ColumnConfig {
  label: string
  field: string
  locked: boolean
  alwaysLocked: boolean
}

const columns = ref({
  identity: [
    { label: 'الرقم العسكري', field: 'military_number', locked: true, alwaysLocked: true },
    { label: 'الرقم العسكري القديم', field: 'old_military_number', locked: false, alwaysLocked: false },
    { label: 'الاسم الكامل', field: 'full_name', locked: true, alwaysLocked: true },
    { label: 'الرقم الوطني', field: 'national_id', locked: true, alwaysLocked: false },
    { label: 'رقم الهاتف', field: 'phone_number', locked: false, alwaysLocked: false },
    { label: 'تاريخ الميلاد', field: 'birth_date', locked: false, alwaysLocked: false },
    { label: 'المؤهل الدراسي', field: 'qualification', locked: false, alwaysLocked: false }
  ] as ColumnConfig[],
  structure: [
    { label: 'إدارة أمن المحافظة', field: 'security_admin', locked: true, alwaysLocked: false },
    { label: 'الإدارة المركزية', field: 'central_department', locked: false, alwaysLocked: false },
    { label: 'الفرع', field: 'branch', locked: false, alwaysLocked: false },
    { label: 'أمن المديرية', field: 'district_police', locked: false, alwaysLocked: false },
    { label: 'القسم', field: 'division', locked: false, alwaysLocked: false },
    { label: 'الوحدة', field: 'unit', locked: false, alwaysLocked: false },
    { label: 'تصنيف القوة', field: 'force_classification', locked: false, alwaysLocked: false },
    { label: 'نوع العمل', field: 'job_title', locked: false, alwaysLocked: false },
    { label: 'المنصب', field: 'position', locked: false, alwaysLocked: false }
  ] as ColumnConfig[],
  statusAndDecisions: [
    { label: 'الرتبة الحالية', field: 'current_rank', locked: true, alwaysLocked: false },
    { label: 'الحالة الخدمية الحالية', field: 'current_status', locked: true, alwaysLocked: false },
    { label: 'تاريخ الالتحاق', field: 'join_date', locked: false, alwaysLocked: false },
    { label: 'تاريخ صدور القرار', field: 'decision_date', locked: false, alwaysLocked: false },
    { label: 'تاريخ التصدور إلينا', field: 'transfer_date', locked: false, alwaysLocked: false },
    { label: 'حالة النفقات', field: 'expense_status', locked: false, alwaysLocked: false },
    { label: 'الملاحظات', field: 'notes', locked: false, alwaysLocked: false }
  ] as ColumnConfig[]
})

function resetToDefaultLocks() {
  columns.value.identity.forEach(c => c.locked = c.alwaysLocked || c.field === 'military_number' || c.field === 'full_name' || c.field === 'national_id')
  columns.value.structure.forEach(c => c.locked = c.field === 'security_admin')
  columns.value.statusAndDecisions.forEach(c => c.locked = c.field === 'current_rank' || c.field === 'current_status')
  Swal.fire({ toast: true, position: 'top-end', icon: 'info', title: 'تمت إعادة ضبط القفل الافتراضي', showConfirmButton: false, timer: 2000 })
}

async function triggerExport() {
  if (!selectedGovernorate.value) return
  
  try {
    const govName = coreStore.governorates.find(g => String(g.id) === String(selectedGovernorate.value))?.name || 'المديرية'
    
    // Assemble locked fields array
    const lockedFields: string[] = []
    Object.values(columns.value).flat().forEach(c => {
      if (c.locked) {
        lockedFields.push(c.field)
      }
    })

    const response = await api.get('/personnel/export_csv/', {
      params: {
        governorate: selectedGovernorate.value,
        current_status: selectedStatus.value || undefined,
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
    console.error('Failed to export locked columns sheet:', err)
  }
}

onMounted(() => {
  if (coreStore.governorates.length === 0) {
    coreStore.fetchAllReferences()
  }
})
</script>
