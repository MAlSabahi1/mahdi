<template>
  <admin-layout>
    <div class="p-6 print:p-0 print:m-0">
      
      <!-- Official Print Header (Hidden on screen) -->
      <ReportHeader title="الهيكل التنظيمي والقوة الفعلية" />

      <div class="mb-6 flex justify-between items-center print:hidden">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white font-arabic">الهيكل التنظيمي والقوة الفعلية</h1>
          <p class="text-gray-500 dark:text-gray-400 mt-1">تقرير تفصيلي يعرض الشجرة التنظيمية للإدارات، الفروع، الأقسام، والوحدات مع أعداد القوة</p>
        </div>
        
        <div class="flex gap-3 print:hidden">
          <button @click="printReport" class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-300 rounded-lg shadow-theme-sm transition-colors font-bold">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
            طباعة التقرير
          </button>
          <button @click="exportToExcel" :disabled="exporting" class="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg shadow-theme-sm transition-colors font-bold disabled:opacity-50">
            <svg v-if="exporting" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            {{ exporting ? 'جاري التصدير...' : 'تصدير إلى Excel' }}
          </button>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-theme-sm border border-gray-200 dark:border-gray-700 overflow-hidden print:shadow-none print:border-none print:rounded-none">
        <!-- Header -->
        <div class="grid grid-cols-12 gap-4 px-6 py-4 bg-gray-50/80 dark:bg-gray-700/80 border-b border-gray-200 dark:border-gray-600 text-sm font-bold text-gray-700 dark:text-gray-300 print:bg-gray-100 print:border-b-2 print:border-gray-800 print:text-black">
          <div class="col-span-8">الجهة / القسم / الوحدة</div>
          <div class="col-span-1 text-center text-blue-700 dark:text-blue-400">الضباط</div>
          <div class="col-span-1 text-center text-emerald-700 dark:text-emerald-400">الأفراد</div>
          <div class="col-span-2 text-center text-indigo-700 dark:text-indigo-400">الإجمالي العام</div>
        </div>

        <!-- Body -->
        <div class="divide-y divide-gray-100 dark:divide-gray-700 max-h-[70vh] overflow-y-auto print:max-h-none print:overflow-visible print:divide-gray-300">
          <div v-if="loading" class="p-12 flex flex-col items-center justify-center">
            <svg class="h-10 w-10 animate-spin text-brand-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            <p class="text-gray-500 dark:text-gray-400 font-bold">جاري بناء الشجرة التنظيمية...</p>
          </div>
          
          <div v-else-if="!treeData.length" class="p-12 text-center text-gray-500 dark:text-gray-400 font-bold">
            لا توجد بيانات متاحة
          </div>

          <div v-else class="flex flex-col">
            <tree-node v-for="(node, index) in treeData" :key="index" :node="node" :level="0" />
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import TreeNode from './components/TreeNode.vue'
import api from '@/lib/api'

const loading = ref(true)
const exporting = ref(false)
const treeData = ref<any[]>([])

const printReport = () => {
  window.print()
}

const fetchTree = async () => {
  loading.value = true
  try {
    const res = await api.get('/personnel/reports/hierarchical-workforce/')
    treeData.value = res.data.data
  } catch (error) {
    console.error('Failed to fetch tree', error)
  } finally {
    loading.value = false
  }
}

const exportToExcel = async () => {
  if (exporting.value) return
  exporting.value = true
  try {
    const response = await api.get('/personnel/reports/hierarchical-workforce/?export=true', {
      responseType: 'blob'
    })
    
    // Create a download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    const dateStr = new Date().toISOString().split('T')[0]
    link.setAttribute('download', `الهيكل_التنظيمي_والقوة_${dateStr}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.parentNode?.removeChild(link)
    
  } catch (error) {
    console.error('Export failed', error)
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  fetchTree()
})
</script>
