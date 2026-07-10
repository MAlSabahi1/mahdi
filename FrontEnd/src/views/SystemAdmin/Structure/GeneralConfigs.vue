<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.general_configs')" />
    
    <div class="flex flex-col lg:flex-row gap-6 text-start min-h-[calc(100vh-160px)]" dir="rtl">
      
      <!-- Sidebar Navigation for Configs -->
      <div class="w-full lg:w-72 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-4 shadow-sm h-fit shrink-0">
        <h3 class="font-black text-gray-900 dark:text-white px-2 mb-4 text-lg">تهيئة الهيكل</h3>
        
        <div class="space-y-1">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer"
            :class="[
              activeTab === tab.id 
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' 
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5" />
            {{ tab.name }}
          </button>
        </div>
      </div>

      <!-- Main Content Area -->
      <div class="flex-1 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm overflow-hidden flex flex-col">
        
        <!-- Tab Header -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 class="text-xl font-black text-gray-900 dark:text-white flex items-center gap-2">
              <component :is="currentTab.icon" class="w-6 h-6 text-blue-500" />
              {{ currentTab.name }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ currentTab.description }}</p>
          </div>
          
          <button @click="handleAddRecord" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shrink-0 cursor-pointer">
            <Plus class="w-4 h-4" /> إضافة سجل جديد
          </button>
        </div>

        <!-- DataTable Component -->
        <div class="flex-1 overflow-hidden">
          <DataTable
            :columns="currentColumns"
            :data="currentData"
            :search-placeholder="'بحث في ' + currentTab.name + '...'"
          >
            <!-- Custom Cell for Military Ranks Icon/Badge -->
            <template #cell-badge="{ row }">
              <div v-if="activeTab === 'ranks'" class="flex items-center justify-center w-8 h-8 rounded bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <ShieldCheck class="w-4 h-4 text-amber-500" />
              </div>
              <div v-else-if="activeTab === 'statuses'" class="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold" :class="row.is_active ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'">
                <div class="w-2 h-2 rounded-full" :class="row.is_active ? 'bg-emerald-500' : 'bg-red-500'"></div>
                {{ row.is_active ? 'نشط' : 'غير نشط' }}
              </div>
              <span v-else class="text-gray-500">-</span>
            </template>
            
            <template #cell-actions="{ row }">
              <div class="flex items-center gap-2">
                <button @click="handleEditRecord(row)" class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="تعديل">
                  <Edit class="w-4 h-4" />
                </button>
                <button @click="handleDeleteRecord(row)" class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors cursor-pointer" title="حذف">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </template>
          </DataTable>
        </div>
      </div>
      
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import { 
  Plus, Edit, Trash2, 
  ShieldCheck, UserCheck, Briefcase, Award, Settings2 
} from 'lucide-vue-next'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const { t } = useI18n()

// Tabs Configuration
const activeTab = ref('ranks')

const tabs = [
  { id: 'ranks', name: 'الرتب العسكرية', description: 'إدارة الرتب العسكرية واختصاراتها وترتيبها الهرمي', icon: ShieldCheck },
  { id: 'statuses', name: 'الحالات الوظيفية', description: 'إدارة حالات الخدمة (على رأس العمل، منتدب، الخ)', icon: UserCheck },
  { id: 'categories', name: 'الفئات الوظيفية', description: 'تصنيف الأفراد (فني، إداري، مقاتل)', icon: Briefcase },
  { id: 'titles', name: 'المسميات القيادية', description: 'إدارة المسميات الوظيفية والمناصب القيادية', icon: Award },
]

const currentTab = computed(() => tabs.find(t => t.id === activeTab.value) || tabs[0])

// Columns config per tab
const tabColumns: Record<string, any[]> = {
  ranks: [
    { key: 'badge', label: 'الشارة', sortable: false },
    { key: 'name', label: 'اسم الرتبة', sortable: true },
    { key: 'order', label: 'المستوى (الترتيب)', sortable: true },
    { key: 'type', label: 'التصنيف', sortable: true },
  ],
  statuses: [
    { key: 'name', label: 'اسم الحالة', sortable: true },
    { key: 'classification_display', label: 'التصنيف', sortable: true },
    { key: 'badge', label: 'الحالة النظامية', sortable: false },
    { key: 'salary', label: 'يستحق راتب', sortable: false },
  ],
  categories: [
    { key: 'name', label: 'اسم الفئة', sortable: true },
    { key: 'job_titles_count', label: 'عدد المسميات', sortable: true },
  ],
  titles: [
    { key: 'name', label: 'المسمى القيادي', sortable: true },
    { key: 'level', label: 'المستوى الإداري', sortable: true },
    { key: 'requires_rank_name', label: 'الرتبة كحد أدنى', sortable: true },
  ]
}

const tabData = ref<any[]>([])
const isLoading = ref(false)

const apiEndpoints: Record<string, string> = {
  ranks: '/dictionaries/ranks/',
  statuses: '/dictionaries/statuses/',
  categories: '/dictionaries/job-categories/',
  titles: '/dictionaries/positions/',
}

const fetchTabData = async () => {
  isLoading.value = true
  try {
    const endpoint = apiEndpoints[activeTab.value]
    const res = await api.get(endpoint)
    const items = res.data.results || res.data || []
    
    if (activeTab.value === 'ranks') {
      tabData.value = items.map((r: any) => ({
        ...r,
        id: r.id,
        name: r.name,
        order: r.order,
        type: r.is_officer ? 'ضباط' : 'أفراد',
        is_active: true
      }))
    } else if (activeTab.value === 'statuses') {
      tabData.value = items.map((s: any) => ({
        ...s,
        id: s.id,
        name: s.name,
        classification_display: s.classification_display || s.classification,
        is_active: !s.is_permanent_deactivation,
        salary: s.receives_salary ? 'نعم' : 'لا'
      }))
    } else if (activeTab.value === 'categories') {
      tabData.value = items.map((c: any) => ({
        ...c,
        id: c.id,
        name: c.name,
        job_titles_count: c.job_titles_count || 0
      }))
    } else if (activeTab.value === 'titles') {
      tabData.value = items.map((p: any) => ({
        ...p,
        id: p.id,
        name: p.name,
        level: p.level || '-',
        requires_rank_name: p.requires_rank_name || '-'
      }))
    }
  } catch (error) {
    console.error('Error fetching tab data', error)
    tabData.value = []
  } finally {
    isLoading.value = false
  }
}

watch(activeTab, () => {
  fetchTabData()
})

onMounted(() => {
  fetchTabData()
})

const currentColumns = computed(() => {
  const baseColumns = tabColumns[activeTab.value] || []
  return [...baseColumns, { key: 'actions', label: 'الإجراءات', sortable: false }]
})

const currentData = computed(() => tabData.value)

// Add forms config per tab
type FormField = { id: string; label: string; type?: string; options?: {value: string, label: string}[] }
const addFormConfig: Record<string, { title: string; fields: FormField[] }> = {
  ranks: {
    title: 'إضافة رتبة جديدة',
    fields: [
      { id: 'name', label: 'اسم الرتبة' },
      { id: 'order', label: 'الترتيب', type: 'number' },
    ]
  },
  statuses: {
    title: 'إضافة حالة وظيفية',
    fields: [
      { id: 'name', label: 'اسم الحالة' },
      { id: 'classification', label: 'التصنيف', type: 'select', options: [
        { value: 'active_full', label: 'قوة عاملة فعلية' },
        { value: 'active_part', label: 'قوة عاملة غير فعلية' },
        { value: 'inactive_temp', label: 'قوة غير عاملة مؤقتاً' },
        { value: 'inactive_perm', label: 'قوة غير عاملة نهائياً' }
      ]}
    ]
  },
  categories: {
    title: 'إضافة فئة وظيفية',
    fields: [
      { id: 'name', label: 'اسم الفئة' },
    ]
  },
  titles: {
    title: 'إضافة مسمى قيادي',
    fields: [
      { id: 'name', label: 'المسمى القيادي' },
      { id: 'level', label: 'المستوى الإداري' },
    ]
  }
}

const handleAddRecord = () => {
  const config = addFormConfig[activeTab.value]
  if (!config) return

  const htmlFields = config.fields.map(f => {
    if (f.type === 'select') {
      const opts = f.options?.map(o => `<option value="${o.value}">${o.label}</option>`).join('')
      return `<select id="swal-${f.id}" class="swal2-input" dir="rtl"><option value="" disabled selected>${f.label}</option>${opts}</select>`
    }
    return `<input id="swal-${f.id}" class="swal2-input" placeholder="${f.label}" type="${f.type || 'text'}" dir="rtl">`
  }).join('')

  Swal.fire({
    title: config.title,
    html: htmlFields,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'حفظ',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#3b82f6',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      const data: Record<string, any> = {}
      for (const f of config.fields) {
        const inputEl = document.getElementById(`swal-${f.id}`) as HTMLInputElement | HTMLSelectElement
        const val = inputEl.value
        if (!val && (f.id === 'name' || f.id === 'classification')) {
          Swal.showValidationMessage(`${f.label} مطلوب`)
          return false
        }
        data[f.id] = f.type === 'number' ? parseInt(val) || 0 : val
      }
      try {
        const endpoint = apiEndpoints[activeTab.value]
        await api.post(endpoint, data)
        return true
      } catch (e: any) {
        const errData = e.response?.data
        let msg = 'حدث خطأ أثناء الحفظ'
        
        if (errData?.error?.detail) {
          const detail = errData.error.detail
          const firstKey = Object.keys(detail)[0]
          if (firstKey && Array.isArray(detail[firstKey]) && detail[firstKey].length > 0) {
            msg = detail[firstKey][0]
          } else if (typeof detail === 'string') {
            msg = detail
          }
        } else if (errData?.name?.[0]) {
          msg = errData.name[0]
        } else if (errData?.detail) {
          msg = errData.detail
        }
        
        Swal.showValidationMessage(msg)
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      fetchTabData()
      Swal.fire('تمت الإضافة', 'تم إضافة السجل بنجاح', 'success')
    }
  })
}

const handleEditRecord = (row: any) => {
  const config = addFormConfig[activeTab.value]
  if (!config) return

  const htmlFields = config.fields.map(f => {
    const val = row[f.id] !== undefined ? row[f.id] : ''
    if (f.type === 'select') {
      const opts = f.options?.map(o => `<option value="${o.value}" ${o.value === val ? 'selected' : ''}>${o.label}</option>`).join('')
      return `<select id="swal-edit-${f.id}" class="swal2-input" dir="rtl"><option value="" disabled>${f.label}</option>${opts}</select>`
    }
    return `<input id="swal-edit-${f.id}" class="swal2-input" placeholder="${f.label}" type="${f.type || 'text'}" value="${val}" dir="rtl">`
  }).join('')

  Swal.fire({
    title: config.title.replace('إضافة', 'تعديل').replace('جديدة', ''),
    html: htmlFields,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'تحديث',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#3b82f6',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      const data: Record<string, any> = {}
      for (const f of config.fields) {
        const inputEl = document.getElementById(`swal-edit-${f.id}`) as HTMLInputElement | HTMLSelectElement
        const val = inputEl.value
        if (!val && (f.id === 'name' || f.id === 'classification')) {
          Swal.showValidationMessage(`${f.label} مطلوب`)
          return false
        }
        data[f.id] = f.type === 'number' ? parseInt(val) || 0 : val
      }
      try {
        const endpoint = apiEndpoints[activeTab.value]
        await api.patch(`${endpoint}${row.id}/`, data)
        return true
      } catch (e: any) {
        const errData = e.response?.data
        let msg = 'حدث خطأ أثناء التحديث'
        if (errData?.error?.detail) {
          const detail = errData.error.detail
          const firstKey = Object.keys(detail)[0]
          if (firstKey && Array.isArray(detail[firstKey]) && detail[firstKey].length > 0) {
            msg = detail[firstKey][0]
          } else if (typeof detail === 'string') {
            msg = detail
          }
        } else if (errData?.name?.[0]) {
          msg = errData.name[0]
        } else if (errData?.detail) {
          msg = errData.detail
        }
        Swal.showValidationMessage(msg)
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      fetchTabData()
      Swal.fire('تم التحديث', 'تم تحديث السجل بنجاح', 'success')
    }
  })
}

const handleDeleteRecord = (row: any) => {
  Swal.fire({
    title: 'تأكيد الحذف',
    text: `هل أنت متأكد من حذف "${row.name}"؟ لا يمكن التراجع عن هذا الإجراء!`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#9ca3af',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      try {
        const endpoint = apiEndpoints[activeTab.value]
        await api.delete(`${endpoint}${row.id}/`)
        return true
      } catch (error: any) {
        let errorMsg = error.response?.data?.error?.message || error.response?.data?.detail || 'حدث خطأ أثناء الحذف، ربما السجل مرتبط ببيانات أخرى'
        Swal.showValidationMessage(errorMsg)
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      fetchTabData()
      Swal.fire('تم الحذف!', 'تم حذف السجل بنجاح', 'success')
    }
  })
}

</script>
