<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('personnel.edit_profile') || 'تعديل بيانات الفرد'" />
    <div class="space-y-6 pb-12">
      <div v-if="coreStore.loading || fetching" class="flex justify-center p-12">
        <svg class="h-10 w-10 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <div v-else-if="form">
        <PersonnelFormBase 
          mode="edit"
          :initialData="form"
          :loading="loading" 
          :error="errorMsg" 
          @submit="handleSubmit" 
          @cancel="router.push(`/personnel/${route.params.id}`)"
          @request-nid-correction="showUpdateNidModal = true"
        />
      </div>

      <div v-else class="flex flex-col items-center justify-center p-12">
        <div class="text-error-500 mb-4">
          <svg class="h-12 w-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('common.error') || 'خطأ' }}</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-2">{{ errorMsg || 'لم يتم العثور على بيانات الفرد.' }}</p>
        <button @click="router.push('/personnel')" class="mt-4 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700">
          العودة للقائمة
        </button>
      </div>
    </div>

    <!-- Modals -->
    <UpdateNationalIdModal 
      v-if="showUpdateNidModal"
      :military-number="route.params.id as string"
      @close="showUpdateNidModal = false"
      @success="handleNationalIdSuccess"
    />
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import PersonnelFormBase from '@/components/forms/PersonnelFormBase.vue'
import { useCoreStore } from '@/stores/core'
import { usePersonnelStore } from '@/stores/personnel'
import Swal from 'sweetalert2'
import UpdateNationalIdModal from './components/UpdateNationalIdModal.vue'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const coreStore = useCoreStore()
const personnelStore = usePersonnelStore()

const loading = ref(false)
const fetching = ref(true)
const errorMsg = ref('')

const form = ref<any>(null)

const showUpdateNidModal = ref(false)

function handleNationalIdSuccess() {
  showUpdateNidModal.value = false
  Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تقديم طلب تصحيح الرقم الوطني بنجاح', showConfirmButton: false, timer: 3000 })
  fetchPersonData() // Reload to get updated data or correction status
}

async function fetchPersonData() {
  const militaryNumber = route.params.id as string
  if (!militaryNumber) return

  try {
    const data = await personnelStore.getPersonnelById(militaryNumber)
    form.value = { ...data }
  } catch (err: any) {
    errorMsg.value = err.response?.data?.error || t('common.error_loading') || 'حدث خطأ أثناء جلب البيانات.'
  } finally {
    fetching.value = false
  }
}

async function handleSubmit(payload: any) {
  loading.value = true
  errorMsg.value = ''

  try {
    await personnelStore.updatePersonnel(payload.military_number, payload)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم حفظ البيانات بنجاح', showConfirmButton: false, timer: 3000 })
    router.push(`/personnel/${payload.military_number}`)
  } catch (err: any) {
    const fieldLabels: Record<string, string> = {
      job_title: 'المسمى الوظيفي', position: 'المنصب', category: 'الفئة',
      national_id: 'الرقم الوطني', military_number: 'الرقم العسكري',
      full_name: 'الاسم الكامل', phone_number: 'رقم الهاتف',
      birth_date: 'تاريخ الميلاد', join_date: 'تاريخ التجنيد',
      current_rank: 'الرتبة', current_status: 'الحالة',
      security_admin: 'الإدارة الأمنية', central_department: 'القطاع / الإدارة المركزية',
      branch: 'الفرع', district_police: 'المديرية', division: 'القسم', unit: 'الوحدة',
      qualification: 'المؤهل', force_classification: 'قوة السلاح',
      geo_location: 'الموقع الجغرافي', notes: 'الملاحظات',
      detail: 'تفاصيل', non_field_errors: 'أخطاء عامة',
    }

    let mainMsg = 'فشل الحفظ. يرجى مراجعة البيانات.'
    let details = ''
    const responseData = err.response?.data

    if (responseData && typeof responseData === 'object' && !Array.isArray(responseData)) {
      const lines: string[] = []
      Object.keys(responseData).forEach(key => {
        const label = fieldLabels[key] || key
        const val = responseData[key]
        const msg = Array.isArray(val) ? val.join('، ') : (typeof val === 'string' ? val : JSON.stringify(val))
        lines.push(`• ${label}: ${msg}`)
      })
      if (lines.length > 0) {
        mainMsg = 'فشل الحفظ — يوجد أخطاء في البيانات:'
        details = lines.join('\n')
      }
    } else if (typeof responseData === 'string' && responseData.includes('<!DOCTYPE')) {
      mainMsg = 'حدث خطأ داخلي في الخادم. يرجى التحقق من صحة جميع البيانات (خاصة تاريخ الميلاد ويجب أن يكون 18 سنة قبل تاريخ التجنيد).'
    } else if (personnelStore.error) {
      mainMsg = personnelStore.error
    }

    errorMsg.value = mainMsg + (details ? '\n' + details : '')
    Swal.fire({
      icon: 'error',
      title: 'فشل حفظ البيانات',
      html: `<div style="text-align:right;direction:rtl;white-space:pre-line">${mainMsg}${details ? '\n\n' + details : ''}</div>`,
      confirmButtonText: 'حسناً',
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    loading.value = false
  }
}


onMounted(async () => {
  if (coreStore.ranks.length === 0) {
    coreStore.fetchAllReferences()
  }
  await fetchPersonData()
})
</script>
