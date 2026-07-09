<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('roles.permission_groups') || 'مجموعات الصلاحيات'" />
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">إدارة مجموعات الصلاحيات</h2>
          <p class="text-sm text-gray-500">قم بتنظيم الصلاحيات في مجموعات منطقية لسهولة إدارتها.</p>
        </div>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          إضافة مجموعة جديدة
        </button>
      </div>

      <!-- Table -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div v-if="loading" class="flex justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="error" class="p-8 text-center text-error-500">
          {{ error }}
        </div>

        <div v-else-if="groups.length === 0" class="p-8 text-center text-gray-500">
          لا توجد مجموعات لعرضها.
        </div>

        <div v-else class="mt-4">
          <DataTable
            :columns="tableColumns"
            :data="groups"
            row-key="id"
          >
            <template #cell-name="{ row }">
              <div class="flex items-center gap-3">
                <div class="h-8 w-8 rounded-lg bg-brand-50 flex items-center justify-center text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                  <i :class="row.icon || 'mdi mdi-folder-outline'" class="text-lg"></i>
                </div>
                <span class="font-medium text-gray-900 dark:text-white">{{ row.name }}</span>
              </div>
            </template>
            <template #cell-module_name="{ value }">
              <span class="inline-flex rounded-md bg-gray-100 px-2 py-1 text-xs font-medium text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                {{ value || 'عام' }}
              </span>
            </template>
            <template #cell-created_at="{ value }">
              {{ new Date(value).toLocaleDateString('ar-YE') }}
            </template>
            <template #actions="{ row }">
              <div class="flex items-center gap-2">
                <button @click="openEditModal(row)" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-brand-600 dark:hover:bg-gray-800 transition-colors" title="تعديل">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                </button>
                <button @click="handleDelete(row)" class="rounded-lg p-2 text-gray-500 hover:bg-error-50 hover:text-error-600 dark:hover:bg-error-500/10 transition-colors" title="حذف">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </template>
          </DataTable>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden bg-black/50 p-4">
      <div class="relative w-full max-w-md rounded-2xl bg-white shadow-2xl dark:bg-gray-800">
        <!-- Modal Header -->
        <div class="flex items-center justify-between border-b border-gray-100 p-5 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ isEditing ? 'تعديل مجموعة الصلاحيات' : 'إضافة مجموعة جديدة' }}
          </h3>
          <button @click="closeModal" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white transition-colors">
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <!-- Modal Body -->
        <form @submit.prevent="saveGroup" class="p-5 space-y-4">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">الرمز البرمجي (Code) <span class="text-red-500">*</span></label>
            <input v-model="formData.code" type="text" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="مثال: HR_MANAGEMENT" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">اسم المجموعة <span class="text-red-500">*</span></label>
            <input v-model="formData.name" type="text" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="مثال: إدارة الموارد البشرية" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">الوصف</label>
            <textarea v-model="formData.description" rows="2" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="وصف الصلاحيات..."></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">ترتيب العرض</label>
              <input v-model.number="formData.display_order" type="number" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" />
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">أيقونة</label>
              <input v-model="formData.icon" type="text" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="mdi mdi-account" />
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="mt-6 flex items-center justify-end gap-3 pt-2">
            <button type="button" @click="closeModal" class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-500 hover:bg-gray-50 hover:text-gray-900 focus:z-10 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-gray-700 transition-colors">
              إلغاء
            </button>
            <button type="submit" :disabled="isSaving" class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-brand-600 focus:outline-none focus:ring-4 focus:ring-brand-300 disabled:opacity-50 transition-colors">
              <svg v-if="isSaving" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isEditing ? 'حفظ التعديلات' : 'إضافة المجموعة' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import axiosInstance from '@/lib/api'
import Swal from 'sweetalert2'

const tableColumns = [
  { key: 'name', label: 'اسم المجموعة', sortable: true },
  { key: 'module_name', label: 'الوحدة (Module)', sortable: true },
  { key: 'display_order', label: 'ترتيب العرض', sortable: true },
  { key: 'created_at', label: 'تاريخ الإنشاء', sortable: true },
  { key: 'actions', label: 'إجراءات', sortable: false }
]

const groups = ref([])
const loading = ref(false)
const error = ref('')

const showModal = ref(false)
const isSaving = ref(false)
const isEditing = ref(false)
const currentGroupId = ref(null)

const formData = ref({
  code: '',
  name: '',
  description: '',
  icon: '',
  display_order: 10
})

async function fetchGroups() {
  loading.value = true
  error.value = ''
  try {
    const res = await axiosInstance.get('/permission-groups/')
    groups.value = res.data.results || res.data || []
  } catch (err) {
    console.error(err)
    error.value = 'تعذر جلب مجموعات الصلاحيات'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  isEditing.value = false
  currentGroupId.value = null
  formData.value = {
    code: '',
    name: '',
    description: '',
    icon: '',
    display_order: 10
  }
  showModal.value = true
}

function openEditModal(group) {
  isEditing.value = true
  currentGroupId.value = group.id
  formData.value = {
    code: group.code,
    name: group.name,
    description: group.description,
    icon: group.icon,
    display_order: group.display_order
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function saveGroup() {
  isSaving.value = true
  try {
    if (isEditing.value) {
      await axiosInstance.put(`/permission-groups/${currentGroupId.value}/`, formData.value)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تعديل المجموعة بنجاح', showConfirmButton: false, timer: 3000 })
    } else {
      await axiosInstance.post('/permission-groups/', formData.value)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم إضافة المجموعة بنجاح', showConfirmButton: false, timer: 3000 })
    }
    closeModal()
    fetchGroups()
  } catch (err) {
    console.error(err)
    const errMsg = err.response?.data?.detail || 'حدث خطأ أثناء الحفظ. يرجى التحقق من المدخلات.'
    Swal.fire('خطأ', errMsg, 'error')
  } finally {
    isSaving.value = false
  }
}

async function handleDelete(group) {
  const res = await Swal.fire({
    title: 'تأكيد الحذف',
    text: `هل أنت متأكد من حذف مجموعة "${group.name}"؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء'
  })

  if (res.isConfirmed) {
    try {
      await axiosInstance.delete(`/permission-groups/${group.id}/`)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الحذف', showConfirmButton: false, timer: 3000 })
      fetchGroups()
    } catch (e) {
      Swal.fire('خطأ', 'فشل الحذف. قد تكون هناك صلاحيات مرتبطة بهذه المجموعة.', 'error')
    }
  }
}

onMounted(() => {
  fetchGroups()
})
</script>
