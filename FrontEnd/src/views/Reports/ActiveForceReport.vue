<template>
  <admin-layout>
    <div class="space-y-6 pb-20">
      <!-- Toolbar & Page Header -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 print:hidden">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">تفاصيل القوة العاملة</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">يعرض كشوفات تفصيلية بأسماء الأفراد وتوزيعهم على الإدارات</p>
        </div>
        <div class="flex items-center gap-2">
          <button @click="fetchData" class="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-all">
            <svg class="h-4.5 w-4.5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            تحديث
          </button>
          <button @click="exportExcel" class="flex items-center gap-2 rounded-lg bg-success-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-success-700 transition-all">
            <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            تصدير إكسل
          </button>
          <button @click="printReport" class="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700 transition-all">
            <svg class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            طباعة
          </button>
        </div>
      </div>

      <!-- Filters Panel -->
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 print:hidden">
        <div class="flex flex-col md:flex-row items-end gap-4">
          <div class="w-full md:w-1/3">
            <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">تصفية حسب المستوى الإداري:</label>
            <select 
              v-model="selectedLevel" 
              @change="fetchData"
              class="w-full rounded-lg border-gray-300 bg-gray-50 px-3.5 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-colors"
            >
              <option value="all">كل المستويات (الجمهورية)</option>
              <option value="central">الإدارات المركزية</option>
              <option value="branch">الفروع</option>
              <option value="district">شرطات المديريات</option>
            </select>
          </div>
          <div class="w-full md:w-1/3">
             <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">بحث سريع:</label>
             <div class="relative">
               <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                 <svg class="h-4.5 w-4.5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                   <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                 </svg>
               </div>
               <input 
                 type="text" 
                 v-model="searchQuery" 
                 placeholder="ابحث بالاسم أو الرقم العسكري..." 
                 class="block w-full rounded-lg border-gray-300 bg-gray-50 py-2.5 pr-10 pl-3 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-colors"
               />
             </div>
          </div>
        </div>
      </div>



      <!-- Data Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-32 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        <svg class="animate-spin h-10 w-10 text-brand-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-gray-500 dark:text-gray-400 font-medium">جاري جلب البيانات...</span>
      </div>
      


      <!-- Grouped Display -->
      <!-- Grouped Display -->
      <div v-else class="space-y-12 printable-area">
        <div 
          v-for="(group, index) in filteredGroupedData" 
          :key="index" 
          class="print-page-break print-group relative"
          v-show="!printingUnit || printingUnit === group.unit"
        >
          <!-- Official Print Header (Repeated for every unit page in print) -->
          <div class="hidden print:block mb-6">
            <report-header 
              :title="`كشف القوة العاملة فعلياً (${group.unit})`" 
              subtitle="يعرض القوة العاملة النشطة والمنتظمة في الدوام" 
              reportType="report_4"
            />
          </div>

          <!-- Title block matching the paper: a sharp, professional box -->
          <div class="flex justify-center mb-5 relative group/header print:hidden">
            <div class="bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 px-12 py-2.5 text-center min-w-[350px] shadow-sm relative">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white">
                كشف بالقوة العاملة بـ ( {{ group.unit }} )
              </h3>
              <!-- Individual Print Button (Hidden in print) -->
              <button 
                @click="printSingleUnit(group.unit)" 
                class="absolute left-[-50px] top-1/2 -translate-y-1/2 opacity-0 group-hover/header:opacity-100 transition-opacity print:hidden bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 p-2 rounded-full shadow-sm text-gray-700 dark:text-gray-300"
                title="طباعة كشف هذه الجهة فقط"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Native Table matching official reports -->
          <div class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            <table class="w-full text-right text-sm border-collapse">
              <thead class="bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-200 border-b-2 border-gray-300 dark:border-gray-600">
                <tr>
                  <th v-for="col in columns" :key="col.key" class="px-4 py-3.5 border-l border-gray-200 dark:border-gray-700 font-bold text-sm text-center align-middle whitespace-nowrap">
                    {{ col.label }}
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="row in group.items" :key="row.index" class="hover:bg-brand-50/50 dark:hover:bg-brand-900/10 transition-colors">
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-bold text-gray-600 dark:text-gray-400">{{ row.index }}</td>
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-medium text-gray-900 dark:text-white whitespace-nowrap">{{ row.rank || '-' }}</td>
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-mono font-medium text-gray-600 dark:text-gray-300">{{ row.military_number || '-' }}</td>
                  <td class="px-4 py-3 border-l border-gray-200 dark:border-gray-700 font-bold text-gray-900 dark:text-white text-base">{{ row.full_name || '-' }}</td>
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-medium text-gray-800 dark:text-gray-200">{{ row.unit !== 'غير محدد (لا توجد بيانات)' ? row.unit : '-' }}</td>
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-medium text-gray-800 dark:text-gray-200">{{ row.service_type || '-' }}</td>
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-mono font-medium text-gray-600 dark:text-gray-300">{{ row.national_id || '-' }}</td>
                  <td class="px-3 py-3 border-l border-gray-200 dark:border-gray-700 text-center font-medium text-gray-800 dark:text-gray-200">{{ row.qualification || '-' }}</td>
                  <td class="px-3 py-3 text-center text-gray-600 dark:text-gray-400 max-w-[150px] truncate" :title="row.notes">{{ row.notes || '-' }}</td>
                </tr>
                <!-- Empty state for dummy group -->
                <tr v-if="group.items.length === 0">
                  <td :colspan="columns.length" class="px-6 py-12 text-center text-gray-500 bg-gray-50 dark:bg-gray-800/50">
                    <svg class="mx-auto h-10 w-10 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                    <span class="font-medium text-sm">لا توجد بيانات مطابقة لمعايير البحث</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'

const selectedLevel = ref('all')
const searchQuery = ref('')
const reportData = ref([])
const loading = ref(false)
const printingUnit = ref<string | null>(null)

const columns = [
  { key: 'index', label: 'م' },
  { key: 'rank', label: 'الرتبة' },
  { key: 'military_number', label: 'الرقم العسكري' },
  { key: 'full_name', label: 'الاسم' },
  { key: 'unit', label: 'محل الخدمة' },
  { key: 'service_type', label: 'نوع الخدمة' },
  { key: 'national_id', label: 'الرقم الوطني' },
  { key: 'qualification', label: 'المؤهل' },
  { key: 'notes', label: 'ملاحظات' }
]

// تجميع البيانات بحسب "الجهة" (unit)
const groupedData = computed(() => {
  if (reportData.value.length === 0) {
    return [{
      unit: 'غير محدد (لا توجد بيانات)',
      items: []
    }]
  }

  const groups: Record<string, any[]> = {}
  
  reportData.value.forEach((item: any) => {
    const unit = item.unit || 'غير محدد'
    if (!groups[unit]) {
      groups[unit] = []
    }
    groups[unit].push(item)
  })
  
  return Object.keys(groups).sort().map(unitName => {
    const items = groups[unitName].map((item, index) => ({
      ...item,
      index: index + 1
    }))
    
    return {
      unit: unitName,
      items: items
    }
  })
})

const filteredGroupedData = computed(() => {
  if (!searchQuery.value) return groupedData.value
  
  const query = searchQuery.value.toLowerCase()
  return groupedData.value.map(group => {
    const filteredItems = group.items.filter(item => 
      item.full_name?.toLowerCase().includes(query) || 
      item.military_number?.includes(query) ||
      item.national_id?.includes(query)
    )
    return {
      ...group,
      items: filteredItems
    }
  }).filter(group => group.items.length > 0)
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/reports/detailed-reports/active-force/', {
      params: { level: selectedLevel.value }
    })
    reportData.value = res.data.data || []
  } catch (error) {
    console.error('Failed to fetch active force report', error)
  } finally {
    loading.value = false
  }
}

const printReport = () => {
  printingUnit.value = null
  nextTick(() => {
    window.print()
  })
}

const printSingleUnit = (unit: string) => {
  printingUnit.value = unit
  nextTick(() => {
    window.print()
    // Optional: reset after printing so they don't get stuck viewing one
    // window.onafterprint can be tricky, so we rely on the normal view restoring if needed, 
    // actually it's better to just reset it back immediately after calling window.print() 
    // because window.print() is blocking in most browsers.
    setTimeout(() => {
      printingUnit.value = null
    }, 500)
  })
}

const exportExcel = () => {
  alert('ميزة التصدير إلى إكسل قيد التطوير حالياً وسيتم ربطها بنظام التصدير المركزي قريباً.')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
@media print {
  @page {
    size: A4 landscape;
    margin: 0; /* This forces the browser to hide default headers/footers like Date and URL */
  }
  
  /* Hide all generic app layout elements */
  body > *:not(#app) { display: none !important; }
  
  /* Override any layout restrictions to allow multi-page printing */
  html, body, #app, main, .admin-layout-content {
    height: auto !important;
    min-height: auto !important;
    overflow: visible !important;
    position: static !important;
  }
  
  /* Only display the printable area, hide all other siblings */
  .printable-area {
    display: block !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 1cm !important;
  }
  
  /* Force hide non-printable elements using a class */
  .print\:hidden {
    display: none !important;
  }
  
  .print-page-break {
    page-break-after: always;
    break-after: page;
    width: 100%;
    display: block;
    clear: both;
  }
  .print-page-break:last-child {
    page-break-after: auto;
    break-after: auto;
  }
  
  table {
    border: 2px solid #000 !important;
    width: 100% !important;
  }
  th, td {
    border: 1px solid #000 !important;
    color: #000 !important;
  }
  th {
    background-color: #f3f4f6 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
</style>
