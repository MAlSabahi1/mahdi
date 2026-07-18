<template>
  <AdminLayout>
  <div>
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">الاستمارات الديناميكية</h1>
        <p class="mt-2 text-sm text-gray-700 dark:text-gray-300">
          إدارة وتصميم الاستمارات الرسمية والنماذج الإدارية.
        </p>
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <router-link
          to="/admin/documents/builder"
          class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-brand-600 border border-transparent rounded-md shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 sm:w-auto"
        >
          <svg class="w-5 h-5 ml-2 -mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
          تصميم استمارة جديدة
        </router-link>
      </div>
    </div>

    <!-- Table Section -->
    <div class="mt-8 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden shadow-sm">
      <div class="p-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/20">
        <h3 class="font-bold text-gray-800 dark:text-gray-200 flex items-center gap-2">
          <FileText class="w-5 h-5 text-gray-400" />
          سجل الاستمارات والنماذج
        </h3>
      </div>
      
      <div v-if="loading" class="p-12 flex flex-col items-center justify-center">
        <Loader2 class="w-8 h-8 text-brand-500 animate-spin mb-4" />
        <p class="text-gray-500 dark:text-gray-400 font-bold">جاري تحميل الاستمارات...</p>
      </div>

      <DataTable
        v-else
        :columns="columns"
        :data="templates"
        row-key="id"
        :search-placeholder="'ابحث عن استمارة بالاسم، الرمز، أو التصنيف...'"
      >
        <template #cell-name="{ row }">
          <div class="flex items-center gap-2">
            <span v-if="row.is_preset" class="px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-800 rounded-md dark:bg-blue-900/30 dark:text-blue-400">جاهز</span>
            <span class="font-bold text-gray-900 dark:text-white">{{ row.name }}</span>
          </div>
        </template>

        <template #cell-status="{ row }">
          <span v-if="row.is_active" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">مفعّل</span>
          <span v-else class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400">معطل</span>
        </template>

        <template #cell-actions="{ row }">
          <div class="flex items-center gap-2">
            <button @click="previewTemplate(row.id)" class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="معاينة">
              <Eye class="w-4 h-4" />
            </button>
            <router-link :to="`/admin/documents/builder/${row.id}`" class="p-1.5 text-gray-400 hover:text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/30 rounded-lg transition-colors cursor-pointer" title="تعديل">
              <FileEdit class="w-4 h-4" />
            </router-link>
            <button @click="deleteTemplate(row.id)" class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors cursor-pointer disabled:opacity-30 disabled:hover:bg-transparent" :disabled="row.is_preset" title="حذف">
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </template>
      </DataTable>
    </div>
  </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/api'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import DataTable from '@/components/tables/DataTable.vue'
import { FileText, Eye, FileEdit, Trash2, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const templates = ref<any[]>([])
const loading = ref(true)

const columns = ref([
  { key: 'name', label: 'اسم الاستمارة', sortable: true },
  { key: 'slug', label: 'الرمز (Slug)', sortable: true },
  { key: 'category', label: 'التصنيف', sortable: true },
  { key: 'status', label: 'الحالة', sortable: true },
  { key: 'actions', label: 'الإجراءات', sortable: false },
])

const fetchTemplates = async () => {
  loading.value = true
  try {
    const response = await api.get('/service-cycle/admin/document-templates/')
    if (response.data.success) {
      templates.value = response.data.results
    }
  } catch (error) {
    console.error('Failed to fetch templates:', error)
    Swal.fire('خطأ', 'حدث خطأ أثناء جلب الاستمارات', 'error')
  } finally {
    loading.value = false
  }
}

const deleteTemplate = async (id: number) => {
  const result = await Swal.fire({
    title: 'هل أنت متأكد؟',
    text: "لن تتمكن من التراجع عن هذا الإجراء!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء'
  })

  if (result.isConfirmed) {
    try {
      await api.delete(`/service-cycle/admin/document-templates/${id}/`)
      Swal.fire('تم الحذف!', 'تم حذف الاستمارة بنجاح.', 'success')
      fetchTemplates()
    } catch (error) {
      console.error('Failed to delete template:', error)
      Swal.fire('خطأ', 'حدث خطأ أثناء الحذف', 'error')
    }
  }
}

const previewTemplate = (id: number) => {
  router.push(`/admin/documents/preview/${id}`)
}

onMounted(() => {
  fetchTemplates()
})
</script>
