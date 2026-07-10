<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('personnel.add_personnel') || 'إضافة فرد جديد'" />
    <div class="space-y-6 pb-12">
      <!-- Tabs for Manual / Bulk Import -->
      <div class="flex border-b border-gray-200 dark:border-gray-800">
        <button 
          @click="activeTab = 'manual'"
          :class="[
            'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
            activeTab === 'manual' 
              ? 'border-brand-500 text-brand-600 dark:text-brand-400' 
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
          ]"
        >
          {{ $t('personnel.manual_add') || 'إضافة يدوية (فرد واحد)' }}
        </button>
        <button 
          @click="activeTab = 'import'"
          :class="[
            'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
            activeTab === 'import' 
              ? 'border-brand-500 text-brand-600 dark:text-brand-400' 
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
          ]"
        >
          {{ $t('personnel.bulk_import') || 'استيراد دفعة (ملف بيانات كثيرة)' }}
        </button>
      </div>

      <div v-if="activeTab === 'import'" class="space-y-6">
        <div class="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900">
          <h3 class="mb-2 text-lg font-bold text-gray-900 dark:text-white">رفع ملف البيانات</h3>
          <p class="text-sm text-gray-500 mb-6">يرجى رفع ملف بصيغة Excel أو CSV يحتوي على بيانات الأفراد لإضافتهم دفعة واحدة.</p>
          
          <div class="flex items-center justify-center w-full">
              <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600 transition-colors">
                  <div class="flex flex-col items-center justify-center pt-5 pb-6">
                      <svg class="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                      <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">اضغط لرفع الملف</span> أو اسحب وأفلت الملف هنا</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">CSV, XLS, XLSX (MAX. 10MB)</p>
                      <p v-if="importFile" class="mt-4 text-sm font-bold text-brand-600 dark:text-brand-400">{{ importFile.name }}</p>
                  </div>
                  <input id="dropzone-file" type="file" class="hidden" @change="handleFileChange" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" />
              </label>
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button @click="router.push('/personnel')"
              class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 cursor-pointer">
              إلغاء
            </button>
            <button @click="submitImport" :disabled="!importFile || loading"
              class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors disabled:opacity-50 cursor-pointer">
              <svg v-if="loading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              بدء الاستيراد
            </button>
          </div>
        </div>
      </div>

      <!-- Manual Form Container -->
      <div v-show="activeTab === 'manual'">
        <PersonnelFormBase 
          mode="create" 
          :loading="loading" 
          :error="errorMsg" 
          @submit="handleSubmit" 
          @cancel="router.push('/personnel')" 
        />
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import PersonnelFormBase from '@/components/forms/PersonnelFormBase.vue'
import { usePersonnelStore } from '@/stores/personnel'
import Swal from 'sweetalert2'

const router = useRouter()
const personnelStore = usePersonnelStore()

const loading = ref(false)
const errorMsg = ref('')
const activeTab = ref('manual')
const importFile = ref<File | null>(null)

async function handleSubmit(payload: any) {
  loading.value = true
  errorMsg.value = ''

  try {
    const newPerson = await personnelStore.createPersonnel(payload)
    router.push(`/personnel/${newPerson.military_number}`) 
  } catch (err: any) {
    errorMsg.value = err.response?.data?.message || personnelStore.error || 'فشل الحفظ. الباك إند رفض البيانات بسبب تعارض مع القواعد الإدارية.'
    
    // Attempt to map backend validation errors to fields
    if (err.response?.data) {
      const beErrors = err.response.data
      if (typeof beErrors === 'object') {
        Object.keys(beErrors).forEach(key => {
          if (key === 'job_title') errorMsg.value += '\n- نوع العمل: ' + beErrors[key]
          if (key === 'position') errorMsg.value += '\n- المنصب: ' + beErrors[key]
          if (key === 'category') errorMsg.value += '\n- الفئة: ' + beErrors[key]
        })
      }
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    loading.value = false
  }
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    importFile.value = target.files[0]
  }
}

async function submitImport() {
  if (!importFile.value) return
  
  loading.value = true
  try {
    const res = await personnelStore.importLegacyData(importFile.value, false)
    Swal.fire({
      icon: 'success',
      title: 'تم الاستيراد بنجاح',
      text: `تم استيراد ${res.created_count || 0} سجل بنجاح.`,
      confirmButtonText: 'حسناً'
    })
    importFile.value = null
    router.push('/personnel')
  } catch (err: any) {
    Swal.fire({
      icon: 'error',
      title: 'فشل الاستيراد',
      text: err.response?.data?.message || err.message || 'حدث خطأ أثناء استيراد البيانات',
      confirmButtonText: 'حسناً'
    })
  } finally {
    loading.value = false
  }
}

</script>
