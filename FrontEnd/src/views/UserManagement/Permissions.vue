<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('roles.permissions') || 'الصلاحيات (Permissions)'" />
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">إدارة الصلاحيات المباشرة</h2>
          <p class="text-sm text-gray-500">سجل بجميع الصلاحيات المُعرّفة في النظام، مع إمكانية ربطها بالمجموعات.</p>
        </div>
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          تسجيل صلاحية جديدة
        </button>
      </div>

      <!-- Table -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <div class="p-4 border-b border-gray-100 dark:border-gray-800 flex gap-4">
          <input type="text" v-model="search" placeholder="ابحث بكود الصلاحية أو الاسم..." class="block w-full max-w-md rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
        </div>

        <div v-if="loading" class="flex justify-center p-12">
          <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else-if="error" class="p-8 text-center text-error-500">
          {{ error }}
        </div>

        <div v-else-if="filteredPermissions.length === 0" class="p-8 text-center text-gray-500">
          لا توجد صلاحيات لعرضها.
        </div>

        <div v-else class="mt-4">
          <DataTable
            :columns="tableColumns"
            :data="filteredPermissions"
            row-key="id"
          >
            <template #cell-code="{ value }">
              <span class="font-mono text-sm text-gray-900 dark:text-white bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">{{ value }}</span>
            </template>
            <template #cell-module="{ value }">
              <span class="inline-flex rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 dark:bg-blue-500/10 dark:text-blue-400">{{ value }}</span>
            </template>
            <template #cell-group_name="{ value }">
              {{ value || 'غير محدد' }}
            </template>
            <template #cell-is_active="{ value }">
              <span v-if="value" class="inline-flex items-center gap-1 rounded-full bg-success-50 px-2.5 py-0.5 text-xs font-medium text-success-700 dark:bg-success-500/10 dark:text-success-400">نشط</span>
              <span v-else class="inline-flex items-center gap-1 rounded-full bg-error-50 px-2.5 py-0.5 text-xs font-medium text-error-700 dark:bg-error-500/10 dark:text-error-400">معطل</span>
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
      <div class="relative w-full max-w-lg rounded-2xl bg-white shadow-2xl dark:bg-gray-800">
        <!-- Modal Header -->
        <div class="flex items-center justify-between border-b border-gray-100 p-5 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ isEditing ? 'تعديل الصلاحية' : 'إضافة صلاحية جديدة' }}
          </h3>
          <button @click="closeModal" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white transition-colors">
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <!-- Modal Body -->
        <form @submit.prevent="savePermission" class="p-5 space-y-4">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">اسم الصلاحية (مقروء) <span class="text-red-500">*</span></label>
            <input v-model="formData.label" type="text" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="مثال: قراءة بيانات الأفراد" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">الوحدة (Module) <span class="text-red-500">*</span></label>
              <input v-model="formData.module" type="text" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="مثال: personnel" />
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">الإجراء (Action) <span class="text-red-500">*</span></label>
              <select v-model="formData.action" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400">
                <option value="read">قراءة (Read)</option>
                <option value="write">كتابة (Write)</option>
                <option value="delete">حذف (Delete)</option>
                <option value="export">تصدير (Export)</option>
                <option value="approve">اعتماد (Approve)</option>
                <option value="manage">إدارة كاملة (Manage)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">النطاق (Scope) <span class="text-red-500">*</span></label>
              <select v-model="formData.scope" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400">
                <option value="global">شامل (Global)</option>
                <option value="department">القسم (Department)</option>
                <option value="self">شخصي (Self)</option>
              </select>
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">مجموعة الصلاحية <span class="text-red-500">*</span></label>
              <select v-model="formData.group" required class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400">
                <option value="" disabled>اختر المجموعة...</option>
                <option v-for="g in permissionGroups" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">التصنيف (Category)</label>
            <input v-model="formData.category" type="text" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400" placeholder="مثال: Reports" />
          </div>

          <div class="flex items-center gap-3 pt-2">
            <input id="requires_dual_auth" v-model="formData.requires_dual_auth" type="checkbox" class="h-5 w-5 rounded border-gray-300 bg-gray-100 text-brand-600 focus:ring-2 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-brand-600" />
            <label for="requires_dual_auth" class="text-sm font-medium text-gray-900 dark:text-gray-300">تتطلب اعتماد ثنائي (Dual Auth)</label>
          </div>

          <!-- Modal Footer -->
          <div class="mt-6 flex items-center justify-end gap-3 pt-4 border-t border-gray-100 dark:border-gray-700">
            <button type="button" @click="closeModal" class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-500 hover:bg-gray-50 hover:text-gray-900 focus:z-10 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-gray-700 transition-colors">
              إلغاء
            </button>
            <button type="submit" :disabled="isSaving" class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-brand-600 focus:outline-none focus:ring-4 focus:ring-brand-300 disabled:opacity-50 transition-colors">
              <svg v-if="isSaving" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isEditing ? 'حفظ التعديلات' : 'إضافة الصلاحية' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import axiosInstance from '@/lib/api'
import Swal from 'sweetalert2'

const tableColumns = [
  { key: 'code', label: 'الكود (Code)', sortable: true },
  { key: 'label', label: 'الوصف (Label)', sortable: true },
  { key: 'module', label: 'الشاشة (Module)', sortable: true },
  { key: 'group_name', label: 'مجموعة الصلاحيات', sortable: true },
  { key: 'is_active', label: 'الحالة', sortable: true },
  { key: 'actions', label: 'إجراءات', sortable: false }
]

const permissions = ref([])
const permissionGroups = ref([])
const loading = ref(false)
const error = ref('')
const search = ref('')

const showModal = ref(false)
const isSaving = ref(false)
const isEditing = ref(false)
const currentPermId = ref(null)

const formData = ref({
  label: '',
  module: '',
  action: 'read',
  scope: 'global',
  category: '',
  group: '',
  requires_dual_auth: false
})

const filteredPermissions = computed(() => {
  if (!search.value) return permissions.value
  const q = search.value.toLowerCase()
  return permissions.value.filter(p => p.code.toLowerCase().includes(q) || p.label.toLowerCase().includes(q) || p.module.toLowerCase().includes(q))
})

async function fetchPermissions() {
  loading.value = true
  error.value = ''
  try {
    const res = await axiosInstance.get('/permissions/')
    permissions.value = res.data.results || res.data || []
  } catch (err) {
    console.error(err)
    error.value = 'تعذر جلب الصلاحيات'
  } finally {
    loading.value = false
  }
}

async function fetchGroups() {
  try {
    const res = await axiosInstance.get('/permission-groups/')
    permissionGroups.value = res.data.results || res.data || []
  } catch (err) {
    console.error('Failed to load permission groups:', err)
  }
}

function openCreateModal() {
  isEditing.value = false
  currentPermId.value = null
  formData.value = {
    label: '',
    module: '',
    action: 'read',
    scope: 'global',
    category: '',
    group: '',
    requires_dual_auth: false
  }
  showModal.value = true
}

function openEditModal(perm) {
  isEditing.value = true
  currentPermId.value = perm.id
  formData.value = {
    label: perm.label,
    module: perm.module,
    action: perm.action,
    scope: perm.scope,
    category: perm.category,
    group: perm.group || '',
    requires_dual_auth: perm.requires_dual_auth
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function savePermission() {
  isSaving.value = true
  try {
    // Generate code from module, action, scope
    const payload = { ...formData.value }
    payload.code = `${payload.module}.${payload.action}.${payload.scope}`.toUpperCase()

    if (isEditing.value) {
      await axiosInstance.put(`/permissions/${currentPermId.value}/`, payload)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تعديل الصلاحية بنجاح', showConfirmButton: false, timer: 3000 })
    } else {
      await axiosInstance.post('/permissions/', payload)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم إضافة الصلاحية بنجاح', showConfirmButton: false, timer: 3000 })
    }
    closeModal()
    fetchPermissions()
  } catch (err) {
    console.error(err)
    const errMsg = err.response?.data?.detail || err.response?.data?.error || 'حدث خطأ أثناء الحفظ. تأكد من صحة البيانات أو عدم تكرار الكود.'
    Swal.fire('خطأ', errMsg, 'error')
  } finally {
    isSaving.value = false
  }
}

async function handleDelete(perm) {
  if (perm.is_system) {
    return Swal.fire('مرفوض', 'لا يمكن حذف صلاحيات النظام الأساسية، يمكنك فقط تعطيلها.', 'error')
  }
  
  const res = await Swal.fire({
    title: 'تأكيد الحذف',
    text: `هل أنت متأكد من حذف الصلاحية "${perm.label}"؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء'
  })

  if (res.isConfirmed) {
    try {
      await axiosInstance.delete(`/permissions/${perm.id}/`)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الحذف', showConfirmButton: false, timer: 3000 })
      fetchPermissions()
    } catch (e) {
      Swal.fire('خطأ', 'فشل الحذف.', 'error')
    }
  }
}

onMounted(() => {
  fetchPermissions()
  fetchGroups()
})
</script>
